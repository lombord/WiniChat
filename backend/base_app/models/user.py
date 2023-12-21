import os
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Q, F, Value, Max


class UserQuerySet(models.QuerySet):
    """
    Custom user query set
    """

    def get_people(self):
        """
        Returns queryset of active people excluding
        admins
        """
        exp = (Q(is_superuser=True) |
               Q(is_staff=True) |
               Q(is_active=False))
        return self.exclude(exp)

    def exclude_user(self, user_pk):
        """
        Excludes given user from queryset
        """
        return self.exclude(pk=user_pk)

    def search_people(self, query: str):
        """
        Simple people search by given query
        """
        qs = self.get_people()
        if query:
            exp = (Q(username__icontains=query) |
                   Q(first_name__icontains=query) |
                   Q(last_name__icontains=query))
            qs = qs.filter(exp)
        return qs


class MyUserManager(UserManager):
    """Custom user manager class"""

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def get_people(self):
        return self.get_queryset().get_people()

    def exclude_user(self, user_pk):
        return self.get_people().exclude_user(user_pk)

    def search_people(self, query: str, user_pk=None):
        qs = self.get_queryset().search_people(query)
        if user_pk:
            qs = qs.exclude_user(user_pk)
        return qs


def user_photo_path(user: 'User', fname: str):
    """
    Generates a path to a photo based on the user
    Args:
        user (User): instance of User model
        fname (str): The filename that was originally given to the file
    Returns:
        str: generated path
    """
    ext = os.path.splitext(fname)[-1]
    name = uuid4().hex
    return f"user/{user.username}/profile/{name}{ext}"


class User(AbstractUser):
    """
    Main User model
    """
    first_name = models.CharField(_('first name'),
                                  max_length=150, blank=True)
    last_name = models.CharField(_('last name'),
                                 max_length=150, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to=user_photo_path,
                              max_length=255,
                              default='defaults/user/default.png')

    status = models.PositiveSmallIntegerField(_('user status'), default=0)

    chat_to = models.ManyToManyField(
        'self',
        through_fields=('from_user', 'to_user'),
        related_name="chat_from",
        symmetrical=False,
        through='PChat',
    )

    user_groups = models.ManyToManyField(
        'Group',
        through='GroupMember',
        related_name='people',
        through_fields=['user', 'group'])

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            models.UniqueConstraint(
                fields=['email',],
                name='unique_email',
                violation_error_message=_("This email already exists.")
            ),]
        indexes = [models.Index(fields=['first_name', 'last_name'],
                                name='user_fullname_idx'),
                   models.Index(F('status').desc(), name='user_status_idx')]

    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = self.username
        super().save(*args, **kwargs)

    def get_chats(self) -> models.QuerySet:
        """
        Get all available private chats of a user
        """
        return self.from_me.all() | self.to_me.all()

    def get_generic_chats(self):
        created = Max('messages__created', default=F('created'))
        values = ('id', 'last_created', 'type')
        chats = self.get_chats().annotate(
            type=Value('chat'), last_created=created).values(*values).order_by()
        groups = self.user_groups.annotate(
            type=Value('group'), last_created=created).values(*values).order_by()
        return chats.union(groups).order_by('-last_created')

    def get_chat_people(self):
        """
        Get all people that user has a chat with
        """
        return self.chat_to.all() | self.chat_from.all()

    def update_status(self, value):
        """
        Update user status
        """
        type(self).objects.filter(pk=self.pk).update(
            status=F('status')*0 + value)

    @property
    def is_online(self):
        """
        Defines if user is online
        """
        return self.status > 0
