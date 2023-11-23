import os
from uuid import uuid4

from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Q, F
from django.db.models.functions import Greatest, Least


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


def photo_path(user: 'User', fname: str):
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
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    bio = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to=photo_path,
                              max_length=255,
                              default='defaults/user/default.png')
    chat_to = models.ManyToManyField(
        'self',
        through_fields=('from_user', 'to_user'),
        related_name="chat_from",
        symmetrical=False,
        through='PChat',
    )
    status = models.PositiveSmallIntegerField(_('user status'), default=0)

    objects = MyUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [models.UniqueConstraint(
            fields=['email',],
            name='unique_email',
            violation_error_message=_("This email already exists.")
        )]

    def get_chats(self):
        """
        Get all available chats of a user
        """
        return self.from_me.all() | self.to_me.all()

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


class PChat(models.Model):
    """
    Chat model for private chats between two users
    """
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='from_me',
                                  verbose_name=_('User One'))

    to_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True,
                                related_name='to_me',
                                verbose_name=_('User Two'))

    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('Created datetime'))

    def get_absolute_url(self, name='chat'):
        return reverse(name, kwargs={"pk": self.pk})

    def get_companion(self, user):
        """
        Returns a companion based on the user
        """
        return self.from_user if user == self.to_user else self.to_user

    def get_companion_id(self, user_id):
        return self.from_user_id if user_id == self.to_user_id else self.to_user_id

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Least('from_user', 'to_user'),
                Greatest('from_user', 'to_user'),
                name='unique_chat',
                violation_error_message=_('You already have a chat with this person.')),
            models.CheckConstraint(
                check=~Q(from_user=F('to_user')),
                name='not_the_same_user',
                violation_error_message=_("Can't start chat with yourself."),)
        ]

        ordering = '-created',

    def __str__(self) -> str:
        return f"Chat: {self.from_user} and {self.to_user}"


IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif'}
AUDIO_EXTS = {'mp3', 'ogg', 'wav', }
VIDEO_EXTS = {'mp4', 'mkv', 'avi', 'mov',
              'wmv', 'flv', 'webm', }
DOC_EXTS = {'doc', 'docx', 'txt', 'pdf', 'rtf', 'odt', 'ott', 'xls',
            'xlsx', 'csv', 'ppt', 'pptx', 'odp', 'ods',
            'html', 'htm', 'xml'}

exts_dict = {'image': IMAGE_EXTS, 'audio': AUDIO_EXTS,
             'video': VIDEO_EXTS, 'doc': DOC_EXTS}

file_validator = FileExtensionValidator(IMAGE_EXTS | AUDIO_EXTS | VIDEO_EXTS)


def get_file_type(ext: str):
    ext = ext[1:].lower()
    for k, v in exts_dict.items():
        if ext in v:
            return k


def message_filepath(instance: 'PMessage', fname: str):
    ext = os.path.splitext(fname)[-1]
    ftype = get_file_type(ext)
    instance.file_type = ftype
    name = uuid4().hex
    return f"pchat/{instance.chat_id}/{ftype}s/{name}{ext}"


class PMessage(models.Model):
    """
    Message model for private chats
    """
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='pMessages',
                              verbose_name=_('Message owner'))
    chat = models.ForeignKey(PChat, on_delete=models.CASCADE,
                             related_name='messages',
                             verbose_name=_('Message PChat'))
    content = models.TextField(_('Message content'),
                               blank=True, null=True)
    file = models.FileField(upload_to=message_filepath,
                            validators=[file_validator,],
                            null=True, blank=True)
    file_type = models.CharField(
        _('File type'), max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = '-created',

    def __str__(self) -> str:
        return f"{self.chat}:{self.owner} -> {self.content[:50]}"
