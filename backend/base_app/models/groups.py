import os
from uuid import uuid4

from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models.functions import Lower
from django.dispatch import receiver

from shortuuid.django_fields import ShortUUIDField

from .abstract import MessageBase, MessageFileBase
from .mixins import ChatMixin
from .utils import (MessageFilePath, FILE_VALIDATOR,
                    delete_file, msg_file_change, delete_old_file)


def group_photo_path(group: 'Group', fname: str):
    ext = os.path.splitext(fname)[-1]
    name = uuid4().hex
    return f"groups/{group.unique_id}/{name}{ext}"


class GroupQuerySet(models.QuerySet):
    pass


class GroupManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return GroupQuerySet(self.model, using=self._db)

    def public_groups(self):
        return self.get_queryset().filter(public=True)


class Group(ChatMixin, models.Model):
    name = models.CharField(_('group name'), max_length=50)
    unique_name = models.CharField(_('unique name'), max_length=100,
                                   null=True, blank=True)
    unique_id = ShortUUIDField(verbose_name=_('unique group id'))
    photo = models.ImageField(_('group photo'), upload_to=group_photo_path,
                              default='defaults/group/default.png', blank=True)
    description = models.TextField(
        _('group description'), max_length=500, default='', blank=True)
    public = models.BooleanField(_('is public group'), default=False)
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True,
                              related_name='created_groups')
    created = models.DateTimeField(_('group created'), auto_now_add=True)
    edited = models.DateTimeField(_('group edited'), auto_now=True)

    objects = GroupManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                'unique_id',
                name='unique_group_id'),
            models.UniqueConstraint(
                Lower('unique_name'),
                condition=Q(public=True),
                name='unique_group_name',
                violation_error_message=_('Public group name should be unique.')),
            models.CheckConstraint(
                check=Q(public=False) | Q(unique_name__isnull=False),
                name='check_public_name_notnull',
                violation_error_message=_('Public group name should not be null.'))
        ]
        indexes = [models.Index(Lower('name'),
                                name='group_name_idx'),
                   models.Index(F('created').desc(),
                                name='group_created_idx'),
                   models.Index(F('public').desc(),
                                name='group_public_idx'),]
        ordering = ('-created',)

    @property
    def type(self):
        return 'group'

    @property
    def default_role(self):
        return self.roles.get(is_default=True)

    @property
    def allowed_members(self):
        banned_people = self.banned_people.values_list('user_id')
        qs = (self.members
              .exclude(user_id__in=banned_people)
              .select_related('role'))
        return qs

    def setup_group(self, create_default=False):
        try:
            owner_role = GroupRole.create_owner_role(self)
            GroupMember.objects.create(
                group=self, user=self.owner, role=owner_role)
        except:
            return
        if create_default:
            GroupRole.create_default_role(self)

    def has_member(self, user_id):
        return self.members.filter(user_id=user_id).exists()

    def can_send(self, user_id) -> bool:
        return self.has_permission(user_id, 'send_msg')

    def can_delete(self, user_id) -> bool:
        return self.has_permission(user_id, 'delete_msg')

    def can_kick(self, user_id) -> bool:
        return self.has_permission(user_id, 'kick_user')

    def can_add(self, user_id) -> bool:
        return self.has_permission(user_id, 'add_user')

    def can_ban(self, user_id) -> bool:
        return self.has_permission(user_id, 'ban_user')

    def can_unban(self, user_id) -> bool:
        return self.has_permission(user_id, 'unban_user')

    def can_edit(self, user_id) -> bool:
        return self.has_permission(user_id, 'edit_group')

    def is_admin(self, user_id) -> bool:
        return self.has_permission(user_id, 'super_admin')

    def has_permission(self, user_id, permission: str) -> bool:
        if self.is_owner(user_id):
            return True
        try:
            member = self.allowed_members.get(user_id=user_id)
        except:
            return False
        role = member.role
        return bool(getattr(role, permission, None) or
                    getattr(role, 'super_admin', None))

    def is_owner(self, user_id) -> bool:
        return self.owner_id == user_id

    def get_absolute_url(self, name='group-detail'):
        return reverse(name, kwargs={"uuid": self.unique_id})

    def __str__(self) -> str:
        return f"{'Public' if self.public else 'Private'} group: {self.name}"


@receiver(models.signals.post_delete, sender=Group)
def delete_group_files(sender, instance, **kwargs):
    delete_file(instance.photo)


@receiver(models.signals.pre_save, sender=Group)
def on_group_change(sender, instance, **kwargs):
    delete_old_file(sender, instance, 'photo')


class GroupRole(models.Model):
    name = models.CharField(_('group role'), max_length=50)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name='roles',
        related_query_name='role')
    is_default = models.BooleanField(_('is default role'), default=False)

    # permissions
    send_msg = models.BooleanField(_('can send message'), default=True)
    delete_msg = models.BooleanField(
        _('can delete message'), default=False)
    kick_user = models.BooleanField(_('can kick user'), default=False)
    add_user = models.BooleanField(_('can add user'), default=True)
    ban_user = models.BooleanField(_('can ban user'), default=False)
    unban_user = models.BooleanField(_('can unban user'), default=False)
    edit_group = models.BooleanField(_('can edit group'), default=False)
    # has the same rights as creator of the group
    super_admin = models.BooleanField(_('is super admin'), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'name'],
                                    name='unique_group_role',
                                    violation_error_message=_(
                                        "Group role with this name already exists!")),
            models.UniqueConstraint(F('is_default').desc(),
                                    F('group'),
                                    name='unique_default_role',
                                    condition=Q(is_default=True),
                                    violation_error_message=_(
                                        "Group can have only one default role"))
        ]
        indexes = [
            models.Index(F('name'), name='group_role_idx')
        ]
        ordering = ('-id',)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__is_default = self.is_default

    def save(self, *args, **kwargs):
        if self.is_default and not (self.__is_default and self.pk):
            self.group.roles.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def create_owner_role(cls, group) -> 'GroupRole':
        return cls.objects.create(name='owner', group=group,
                                  super_admin=True)

    @classmethod
    def create_default_role(cls, group) -> 'GroupRole':
        return cls.objects.create(name='member',
                                  group=group, is_default=True)

    def __str__(self) -> str:
        return f"Group-{self.group_id}:{self.name}"

    def get_absolute_url(self, name='group-role'):
        return reverse(name, kwargs={"uuid": self.group.unique_id,
                                     'pk': self.pk})


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='members')
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             related_name='+')
    role = models.ForeignKey(GroupRole, on_delete=models.CASCADE,
                             related_name='members',
                             related_query_name='member')
    added_by = models.ForeignKey('User', on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='added_members')
    joint = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'group'],
                name='join_group_once',
                violation_error_message=_(
                    "You're already in the group.")),
            models.CheckConstraint(
                check=~Q(user=F('added_by')),
                name='check_added_by',
                violation_error_message=_(
                    "Can't add yourself to the group."))
        ]
        indexes = [models.Index(
            F('joint').desc(), name='group_joint_date_idx')]
        ordering = ('-joint',)

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.group.default_role
        super().save(*args, **kwargs)

    def clean(self):

        if not (self.group.public or
                self.group.can_add(self.added_by_id)):
            raise ValidationError(
                _("You're not allowed to add people to this group"))

        if self.group_id != self.role.group_id:
            raise ValidationError(
                _('User role must belong to the joining group.'))

    def get_absolute_url(self, name='group-member'):
        return reverse(name, kwargs={"uuid": self.group.unique_id, 'pk': self.pk})


class GroupBan(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='banned_people')
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             related_name='banned_groups')
    banned_by = models.ForeignKey('User', on_delete=models.SET_NULL,
                                  verbose_name=_('banned by user'),
                                  null=True, related_name='banned_people')
    reason = models.TextField(_('ban reason'), max_length=1000,
                              default=_('No Reason'))
    created = models.DateTimeField(_('banned datetime'), auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'group'],
                name='ban_user_once',
                violation_error_message=_(
                    'This user has already been banned')),
            models.CheckConstraint(
                check=~Q(user=F('banned_by')),
                name='check_banned_by',
                violation_error_message=_(
                    "Can't ban yourself from group!"))
        ]
        indexes = [models.Index(F('created').desc(),
                                name='ban_created_idx'),]
        ordering = ('-created',)

    def clean(self):
        if not self.group.has_member(self.user_id):
            raise ValidationError(
                _('Can\'t ban non-member user from the group.'))

        if not self.group.can_ban(self.banned_by_id):
            raise ValidationError(
                _("You are not allowed to ban people in this group."))

    def get_absolute_url(self, name='group-ban'):
        return reverse(name, kwargs={"uuid": self.group.unique_id,
                                     'pk': self.pk})


class GroupMessage(MessageBase):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name='messages')

    class Meta(MessageBase.Meta):
        indexes = [models.Index(F('created').desc(),
                                name='group_msg_created_idx')]

    def __str__(self) -> str:
        return f"{self.group_id}:{super().__str__()}"

    def clean(self):
        if not self.group.can_send(self.owner_id):
            raise ValidationError(
                _("You are not allowed to send messages."))

    def get_absolute_url(self, name='group-message'):
        return reverse(name, kwargs={"uuid": self.group.unique_id,
                                     'pk': self.pk})


message_file_path = MessageFilePath('group', 'message.group_id')


class GroupMessageFile(MessageFileBase):
    file = models.FileField(upload_to=message_file_path,
                            validators=[FILE_VALIDATOR,])
    message = models.ForeignKey(
        GroupMessage,
        on_delete=models.CASCADE,
        related_name='files')

    class Meta(MessageFileBase.Meta):
        indexes = [models.Index(Lower('file_type'),
                                name='group_file_type_idx'),]


@receiver(models.signals.post_delete, sender=GroupMessageFile)
def clean_message_files(sender, instance, **kwargs):
    delete_file(instance.file)


@receiver(models.signals.pre_save, sender=GroupMessageFile)
def message_file_change(sender, instance, **kwargs):
    msg_file_change(sender, instance)
