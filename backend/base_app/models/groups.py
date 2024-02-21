# built in libraries
import os
from uuid import uuid4
from itertools import chain


# django libraries
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F, Prefetch, Count
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinLengthValidator


# custom modules
from .abstract import MessageBase, MessageFileBase
from .utils import MessageFilePath, FILE_VALIDATOR, delete_file, delete_old_file


UNIQUE_NAME_RE = r"^[_a-z][_a-z0-9]{2,50}$"


class GroupQuerySet(models.QuerySet):

    def search_groups(self, query: str, user):
        exp = Q(public=False) | Q(pk__any=user.all_groups.values("pk").order_by())
        qs = self.exclude(exp)
        if query:
            exp = Q(unique_name__icontains=query) | Q(name__icontains=query)
            qs = (
                qs.alias(
                    group_order=(
                        Q(unique_name__istartswith=query) | Q(name__istartswith=query)
                    )
                )
                .filter(exp)
                .order_by("-group_order", "unique_name")
            )
        return qs

    def prefetch_latest(self):
        qs = GroupMessage.objects.annotate_owner_name().order_by("-created")
        return self.prefetch_related(
            Prefetch("messages", queryset=qs, to_attr="latest")
        )

    def annotate_count(self):
        return self.annotate(
            members_count=Count("members"),
            online_count=Count("people", filter=Q(people__status__gt=0)),
        )


class GroupManager(models.Manager):

    def get_queryset(self) -> GroupQuerySet:
        return GroupQuerySet(self.model, using=self._db)

    def search_groups(self, query: str, user):
        return self.get_queryset().annotate_count().search_groups(query, user)

    def common_fetch(self):
        return self.get_queryset().annotate_count().prefetch_latest()


def group_photo_path(group: "Group", fname: str):
    ext = os.path.splitext(fname)[-1]
    name = uuid4().hex
    return f"groups/{group.pk}/{name}{ext}"


class Group(models.Model):

    name = models.CharField(_("group name"), max_length=50)
    unique_name = models.CharField(
        _("unique name"),
        max_length=100,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(5, _("Unique name must contain at least 5 characters"))
        ],
    )
    photo = models.ImageField(
        _("group photo"),
        upload_to=group_photo_path,
        default="defaults/group/default.png",
        blank=True,
    )
    description = models.TextField(
        _("group description"), max_length=500, default="", blank=True
    )
    public = models.BooleanField(_("is public group"), default=False)
    owner = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_groups"
    )
    created = models.DateTimeField(_("group created"), auto_now_add=True)
    edited = models.DateTimeField(_("group edited"), auto_now=True)

    objects = GroupManager()

    people = models.ManyToManyField(
        "User",
        through="GroupMember",
        related_name="user_groups",
        through_fields=["group", "user"],
    )

    banned_people = models.ManyToManyField(
        "User",
        through="GroupBan",
        related_name="banned_groups",
        through_fields=["group", "user"],
    )

    objects = GroupManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("unique_name"),
                condition=Q(public=True),
                name="unique_group_name",
                violation_error_message=_("Public group name should be unique."),
            ),
            models.CheckConstraint(
                check=Q(public=False) | Q(unique_name__iregex=UNIQUE_NAME_RE),
                name="check_valid_public_name",
                violation_error_message=_("Invalid unique group name"),
            ),
        ]
        indexes = [
            models.Index(Lower("name"), name="group_name_idx"),
            models.Index(F("created").desc(), name="group_created_idx"),
            models.Index(F("public").desc(), name="group_public_idx"),
        ]
        ordering = ("-created",)

    @property
    def type(self):
        return "group"

    @cached_property
    def default_role(self):
        return self.roles.get(is_default=True)

    @property
    def banned_ids(self):
        return self.banned_people.values_list("id", flat=True)

    @property
    def allowed_members(self) -> models.QuerySet:
        return self.members.exclude(user_id__in=self.banned_ids)

    @property
    def all_people(self):
        return (self.people.all() | self.banned_people.all()).distinct().order_by()

    @property
    def allowed_people(self):
        return self.people.exclude(pk__in=self.banned_ids)

    @property
    def online_people(self):
        return self.allowed_people.filter(status__gt=0)

    @property
    def online_ids(self):
        return self.online_people.values_list("pk", flat=True)

    def search_member(self, query: str):
        return (
            self.allowed_members.filter(
                Q(user__username__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
            )
            .alias(
                member_order=(
                    Q(user__username__istartswith=query)
                    | Q(user__first_name__istartswith=query)
                )
            )
            .order_by("-member_order", "user__first_name")
        )

    def setup_group(self):
        owner_role = GroupRole.create_owner_role(self, self.owner)
        GroupMember.objects.create(group=self, user=self.owner, role=owner_role)
        GroupRole.create_default_role(self, self.owner)

    # Group permission related methods
    def is_banned(self, user_id) -> bool:
        try:
            return self.banned_ids.filter(id=user_id).exists()
        except Exception:
            return False

    def has_member(self, user_id):
        return self.members.filter(user_id=user_id).order_by().exists()

    def can_send(self, user_id) -> bool:
        return self.has_perm(user_id, "send_msg")

    def can_delete(self, user_id) -> bool:
        return self.has_perm(user_id, "delete_msg")

    def can_kick(self, user1, user2) -> bool:
        return self.has_perm_over(user1, user2, "kick_user")

    def can_join(self, user_id):
        return not self.banned_people.filter(id=user_id).exists()

    def can_join_public(self, user_id):
        return self.public and self.can_join(user_id)

    def can_add(self, user1, user2) -> bool:
        try:
            role = self.get_user_role(
                user1.pk,
                [
                    "add_user",
                ],
            )
            assert role.has_perm("add_user")
            assert self.can_join(user2.pk)
            return user1.has_chat(user2)
        except Exception:
            return False

    def can_ban(self, user1, user2) -> bool:
        return self.has_perm_over(user1, user2, "ban_user")

    def can_unban(self, user, banned_by) -> bool:
        try:
            roles = self.get_user_roles(
                user,
                banned_by,
                perms=[
                    "unban_user",
                ],
            )
            role1, role2 = roles[user], roles.get(banned_by)
            return role1.has_perm("unban_user") and (
                not role2 or role1.priority <= role2.priority
            )
        except Exception:
            return False

    def can_edit(self, user_id) -> bool:
        return self.has_perm(user_id, "edit_group")

    def can_manage_role(self, user_id) -> bool:
        return self.has_perm(user_id, "manage_role")

    def manage_role_over(self, user1, user2) -> bool:
        return self.has_perm_over(user1, user2, "manage_role")

    def is_admin(self, user_id) -> bool:
        return self.has_perm(user_id, "super_admin")

    def is_owner(self, user_id) -> bool:
        try:
            role = self.get_user_role(user_id, 0)
            return role.is_owner
        except Exception:
            return False

    def defer_member_qs(self, perms=None) -> models.QuerySet:
        qs = self.members.select_related("role")
        if perms is None:
            qs = qs.defer("joint", "added_by")
        else:
            perms = set(chain(GroupRole.SPECIAL_PROPS, perms))
            qs = qs.only("group", "user", *("role__%s" % p for p in perms))
        return qs

    def get_user_role(self, user_id, perms=None) -> "GroupRole":
        return self.defer_member_qs(perms).get(user_id=user_id).role

    def get_user_roles(self, user1, user2, perms=None):
        qs = self.defer_member_qs(perms).filter(user_id__in=[user1, user2])
        return {member.user_id: member.role for member in qs}

    def has_perm_over(self, user1, user2, perm: str) -> bool:
        if not user2:
            return self.has_perm(user1, perm)
        if isinstance(user2, GroupRole):
            return self.has_perm_over_role(user1, user2, perm)
        try:
            roles = self.get_user_roles(
                user1,
                user2,
                perms=[
                    perm,
                ],
            )
            role1, role2 = roles[user1], roles[user2]
            return role1.has_perm_over(role2, perm)
        except Exception:
            return False

    def has_perm_over_role(self, user_id, role, perm: str) -> bool:
        try:
            user_role = self.get_user_role(
                user_id,
                [
                    perm,
                ],
            )
            return user_role.has_perm_over(role, perm)
        except Exception as e:
            print(e)
            return False

    def has_perm(self, user_id, perm: str) -> bool:
        try:
            assert user_id
            role = self.get_user_role(
                user_id,
                [
                    perm,
                ],
            )
            return role.has_perm(perm)
        except Exception:
            return False

    def is_owner(self, user_id) -> bool:
        return self.owner_id == user_id

    def get_absolute_url(self, name="group-detail"):
        return reverse(name, kwargs={"group_pk": self.pk})

    def __str__(self) -> str:
        return f"{'Public' if self.public else 'Private'} group: {self.name}"


@receiver(models.signals.post_delete, sender=Group)
def delete_group_files(sender, instance, **kwargs):
    delete_file(instance.photo)


class GroupRole(models.Model):
    SPECIAL_PROPS = ("is_default", "is_owner", "priority", "super_admin")

    name = models.CharField(_("group role"), max_length=50)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="roles", related_query_name="role"
    )
    created_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)

    # special properties
    is_default = models.BooleanField(_("is default role"), default=False)
    is_owner = models.BooleanField(_("is owner role"), default=False)
    priority = models.PositiveSmallIntegerField(
        _("role priority"),
        default=100,
        validators=[MaxValueValidator(100, _("Priority must be less or equal to 100"))],
    )

    # permissions
    send_msg = models.BooleanField(_("can send message"), default=True)
    delete_msg = models.BooleanField(_("can delete message"), default=False)
    kick_user = models.BooleanField(_("can kick user"), default=False)
    add_user = models.BooleanField(_("can add user"), default=True)
    ban_user = models.BooleanField(_("can ban user"), default=False)
    unban_user = models.BooleanField(_("can unban user"), default=False)
    edit_group = models.BooleanField(_("can edit group"), default=False)
    manage_role = models.BooleanField(_("can manage role"), default=False)

    # has all the permissions
    super_admin = models.BooleanField(_("is super admin"), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "name"],
                name="unique_group_role",
                violation_error_message=_(
                    "This group already has a role with this name!"
                ),
            ),
            models.UniqueConstraint(
                F("group"),
                F("is_default").desc(),
                name="unique_default_role",
                condition=Q(is_default=True),
                violation_error_message=_("Group can have only one default role"),
            ),
            models.UniqueConstraint(
                F("group"),
                F("is_owner").desc(),
                name="unique_owner_role",
                condition=Q(is_owner=True),
                violation_error_message=_("Group can have only one owner role"),
            ),
            models.CheckConstraint(
                check=Q(priority__gte=0) & Q(priority__lte=100),
                name="check_priority_range",
                violation_error_message=_("Priority should be in range [0, 100]"),
            ),
        ]
        indexes = [
            models.Index(F("name"), name="group_role_idx"),
            models.Index(F("priority").asc(), name="role_priority_idx"),
        ]
        ordering = ("-id",)

    @property
    def is_special(self):
        return self.is_default or self.is_owner

    def clean(self):
        if self.pk:
            return
        try:
            assert not self.is_special, "Special roles cannot be created manually."
            role = self.group.get_user_role(
                self.created_by_id,
                [
                    "manage_role",
                ],
            )
            assert role.has_perm_over(
                self, "manage_role"
            ), "You cannot create this role."
        except AssertionError as msg:
            raise ValidationError(_(str(msg)))
        except Exception as e:
            raise ValidationError(_("Permission is denied."))

    @classmethod
    def create_owner_role(cls, group, user) -> "GroupRole":
        return cls.objects.create(
            name="owner",
            group=group,
            is_owner=True,
            super_admin=True,
            priority=0,
            created_by=user,
        )

    @classmethod
    def create_default_role(cls, group, user) -> "GroupRole":
        return cls.objects.create(
            name="member", group=group, is_default=True, priority=100, created_by=user
        )

    def has_perm(self, perm: str) -> bool:
        return getattr(self, perm, False) or self.super_admin or self.is_owner

    def has_priority_over(self, role: "GroupRole") -> bool:
        try:
            return not role.is_owner and (
                self.is_owner or self.priority < role.priority
            )
        except Exception:
            return False

    def has_perm_over(self, role: "GroupRole", perm: str) -> bool:
        return self.has_perm(perm) and self.has_priority_over(role)

    def manage_role_over(self, role):
        return self.has_perm_over(role, "manage_role")

    def __str__(self) -> str:
        return f"Group-{self.group_id}:{self.name}"

    def get_absolute_url(self, name="group-role"):
        return reverse(name, kwargs={"group_pk": self.group_id, "pk": self.pk})


@receiver(models.signals.pre_delete, sender=GroupRole)
def on_role_delete(sender, instance: GroupRole, origin, **kwargs):
    if isinstance(origin, Group):
        return
    if instance.is_special:
        raise ValidationError(_("Special roles cannot be deleted."))
    instance.members.update(role=instance.group.default_role)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="+")
    role = models.ForeignKey(
        GroupRole,
        on_delete=models.CASCADE,
        related_name="members",
        related_query_name="member",
    )
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_members",
    )
    joint = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "group"],
                name="join_group_once",
                violation_error_message=_("You're already in the group."),
            ),
            models.CheckConstraint(
                check=~Q(user=F("added_by")),
                name="check_added_by",
                violation_error_message=_("Can't add yourself to the group."),
            ),
        ]
        indexes = [models.Index(F("joint").desc(), name="group_joint_date_idx")]
        ordering = ("-joint",)

    def save(self, *args, **kwargs):
        if not self.role:
            self.role = self.group.default_role
        super().save(*args, **kwargs)

    def clean(self):
        if self.added_by == self.user:
            self.added_by = None
        try:
            assert (
                not self.added_by and self.group.can_join_public(self.user_id)
            ) or self.group.can_add(
                self.added_by, self.user
            ), "This operation cannot be done."
            assert (
                self.group_id == self.role.group_id
            ), "User role must belong to the joining group."
        except AssertionError as msg:
            raise ValidationError(_(str(msg)))
        except Exception:
            raise ValidationError("Something went wrong.")

    def get_absolute_url(self, name="group-member"):
        return reverse(name, kwargs={"group_pk": self.group_id, "pk": self.pk})

    def __str__(self) -> str:
        return f"{self.group_id}: {self.user.username}({self.user_id})"


class GroupBan(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="bans")
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="group_bans"
    )
    banned_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        verbose_name=_("banned by user"),
        null=True,
        related_name="banned_people",
    )
    reason = models.TextField(_("ban reason"), max_length=1000, default=_("No Reason"))
    created = models.DateTimeField(_("banned datetime"), auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "group"],
                name="ban_user_once",
                violation_error_message=_("This user has already been banned"),
            ),
            models.CheckConstraint(
                check=~Q(user=F("banned_by")),
                name="check_banned_by",
                violation_error_message=_("Can't ban yourself from group!"),
            ),
        ]
        indexes = [
            models.Index(F("created").desc(), name="ban_created_idx"),
        ]
        ordering = ("-created",)

    def clean(self):
        if not self.group.can_ban(self.banned_by_id, self.user_id):
            raise ValidationError(_("You can't ban this person."))

    def get_absolute_url(self, name="group-ban"):
        return reverse(name, kwargs={"group_pk": self.group_id, "pk": self.pk})


class GroupMessage(MessageBase):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")

    class Meta(MessageBase.Meta):
        indexes = [models.Index(F("created").desc(), name="group_msg_created_idx")]

    def __str__(self) -> str:
        return f"{self.group_id}:{super().__str__()}"

    def clean(self):
        if not self.group.can_send(self.owner_id):
            raise ValidationError(_("You are not allowed to send messages."))

    def get_absolute_url(self, name="group-message"):
        return reverse(name, kwargs={"group_pk": self.group_id, "pk": self.pk})


message_file_path = MessageFilePath("group_media", "message.group_id")


class GroupMessageFile(MessageFileBase):
    file = models.FileField(
        upload_to=message_file_path,
        validators=[
            FILE_VALIDATOR,
        ],
    )
    message = models.ForeignKey(
        GroupMessage, on_delete=models.CASCADE, related_name="files"
    )

    class Meta(MessageFileBase.Meta):
        indexes = [
            models.Index(Lower("file_type"), name="group_file_type_idx"),
        ]


@receiver(models.signals.post_delete, sender=GroupMessageFile)
def clean_message_files(sender, instance, **kwargs):
    delete_file(instance.file)


@receiver(models.signals.pre_save, sender=GroupMessageFile)
def message_file_change(sender, instance, **kwargs):
    delete_old_file(sender, instance)
