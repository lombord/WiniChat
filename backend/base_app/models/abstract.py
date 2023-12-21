import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .utils import get_file_type


class MessageBase(models.Model):
    """
    Message model for private chats
    """
    owner = models.ForeignKey('User', on_delete=models.CASCADE,
                              null=True, related_name='+',
                              verbose_name=_('Message owner'))
    content = models.TextField(_('Message content'),
                               blank=True, null=True)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    edited = models.DateTimeField(editable=False)

    class Meta:
        abstract = True
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = self.edited = timezone.now()
        else:
            self.edited = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_edited(self):
        return self.edited != self.created

    def __str__(self) -> str:
        return f"{self.owner} -> {self.content[:50]}"


class MessageFileBase(models.Model):
    file_type = models.CharField(_('File type'), max_length=50)
    metadata = models.JSONField()

    class Meta:
        abstract = True
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if not self.pk:
            ext = os.path.splitext(self.file.name)[-1]
            self.file_type = get_file_type(ext)
        super().save(*args, **kwargs)
