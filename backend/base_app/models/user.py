"""User models"""

import os
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import (
    Q,
    F,
    Value,
    Max,
    Subquery,
    OuterRef,
)
from django.db.models.functions import Coalesce

from .groups import GroupMessage


class UserQuerySet(models.QuerySet):
    """
    Custom user query set
    """

    def filter_people(self, user):
        """
        Returns queryset of active people excluding admins,
        inactive people and user himself
        """
        exp = (
            Q(is_superuser=True) | Q(is_staff=True) | Q(is_active=False) | Q(pk=user.pk)
        )
        return self.exclude(exp)

    def get_chats(self, user):
        """
        Returns queryset of user chats
        """

        from .pchats import PChat

        exp = (Q(from_user=user) & Q(to_user=OuterRef("pk"))) | (
            Q(from_user=OuterRef("pk")) & Q(to_user=user)
        )
        return PChat.objects.filter(exp).values("pk").order_by()

    def search_query(self, query):

        exp = (
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return (
            self.alias(
                user_order=(
                    Q(username__istartswith=query) | Q(first_name__istartswith=query)
                )
            )
            .filter(exp)
            .order_by("-user_order", "first_name", "last_name")
        )

    def search_people(self, query: str, user: "User"):
        """
        Simple people searching by given query and user
        """
        qs = self.filter_people(user).alias_chat(user)
        if query:
            qs = qs.search_query(query)
        return qs.filter(chat_id__isnull=True)

    def search_friends(self, query: str, user):
        """Search people that user has common chat with"""

        qs = self.exclude(pk=user.pk).annotate_chat(user)
        if query:
            qs = qs.search_query(query)
        return qs.filter(chat_id__isnull=False)

    def annotate_chat(self, user):
        sub_q = self.get_chats(user)
        return self.annotate(chat_id=Subquery(sub_q[:1]))

    def alias_chat(self, user):
        sub_q = self.get_chats(user)
        return self.alias(chat_id=Subquery(sub_q[:1]))


class MyUserManager(UserManager):
    """Custom user manager class"""

    def get_queryset(self) -> UserQuerySet:
        return UserQuerySet(self.model, using=self._db)

    def search_people(self, query: str, user) -> UserQuerySet:
        return self.get_queryset().search_people(query, user)

    def search_friends(self, query: str, user) -> UserQuerySet:
        return self.get_queryset().search_friends(query, user)


def user_photo_path(user: "User", fname: str):
    """
    Generates a path to a photo based on user
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
    App User model
    """

    email = models.EmailField(_("email address"), blank=False, null=False)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    photo = models.ImageField(
        upload_to=user_photo_path, max_length=255, default="defaults/user/default.png"
    )

    # user sessions number
    status = models.PositiveSmallIntegerField(_("user status"), default=0)

    # people whom user started chat with
    chat_to = models.ManyToManyField(
        "self",
        through_fields=("from_user", "to_user"),
        # people who user got chat from
        related_name="chat_from",
        symmetrical=False,
        through="PChat",
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            # User email must be unique
            models.UniqueConstraint(
                fields=[
                    "email",
                ],
                name="unique_email",
                violation_error_message=_("This email already exists."),
            ),
        ]
        indexes = [
            # Indexing user first and last name to speed up ordering
            models.Index(fields=["first_name", "last_name"], name="user_fullname_idx"),
            # Indexing user status to speed up sorting
            models.Index(F("status").desc(), name="user_status_idx"),
        ]
        ordering = ("first_name", "last_name")

    @property
    def allowed_groups(self):
        """Returns valid user groups"""
        return self.user_groups.exclude(banned_people=self)

    @property
    def all_groups(self):
        """Returns all user groups including banned ones"""
        return (self.user_groups.all() | self.banned_groups.all()).distinct().order_by()

    @property
    def chatted_people(self):
        """
        Get all people that user has a chat with
        """
        return (self.chat_to.all() | self.chat_from.all()).distinct()

    def has_chat(self, user):
        """Checks if user has a chat with this user"""
        return self.chatted_people.contains(user)

    def get_absolute_url(self):
        return reverse("user", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # set first name same as username if not specified
        if not self.first_name:
            self.first_name = self.username
        super().save(*args, **kwargs)

    def get_chats(self) -> models.QuerySet:
        """
        Get all available private chats of a user
        """
        return self.from_me.all() | self.to_me.all()

    def get_generic_chats(self):
        """Get queryset of all types of available user chats"""

        created = Max("messages__created", default=F("created"))
        sub_q = (
            GroupMessage.objects.filter(group=OuterRef("pk"))
            .values("group__pk")
            .annotate(last_created=Max("created"))
            .values("last_created")
        )
        values = ("id", "last_created", "type")
        chats = (
            self.get_chats()
            .annotate(type=Value("chat"), last_created=created)
            .values(*values)
            .order_by()
        )
        groups = (
            self.allowed_groups.annotate(
                type=Value("group"),
                last_created=Coalesce(Subquery(sub_q), F("created")),
            )
            .values(*values)
            .order_by()
        )
        return chats.union(groups, all=True).order_by("-last_created")

    def update_status(self, value):
        """
        Update user status
        """
        type(self).objects.filter(pk=self.pk).update(status=F("status") * 0 + value)

    @property
    def is_online(self):
        """
        Indicates whether user is online
        """
        return self.status > 0
