"""Common abstract models"""

import os
from mutagen import File

from django.db import models
from django.db.models import Prefetch, Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .utils import get_file_type, AUDIO_EXTS


class MessageQuerySet(models.QuerySet):
    """Abstract class for message querysets"""

    def annotate_owner_name(self):
        """Annotates message owners full name"""
        return self.annotate(
            owner_name=Concat("owner__first_name", Value(" "), "owner__last_name")
        )

    def prefetch_files(self):
        """Prefetches message files"""
        return self.prefetch_related(Prefetch("files", to_attr="_cached_files"))


class MessageManager(models.Manager):
    """Abstract class for message model manager"""

    def get_queryset(self) -> MessageQuerySet:
        return MessageQuerySet(self.model, using=self._db)

    def annotate_owner_name(self):
        return self.get_queryset().annotate_owner_name()

    def common_fetch(self):
        """Base common fetch method for messages"""
        return self.get_queryset().prefetch_files().annotate_owner_name()


class MessageBase(models.Model):
    """
    Abstract model class for messages
    """

    owner = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        related_name="+",
        verbose_name=_("Message owner"),
    )
    content = models.TextField(_("Message content"), blank=True, null=True)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    edited = models.DateTimeField(editable=False)

    objects = MessageManager()

    class Meta:
        abstract = True
        ordering = ("-created",)

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
    """
    Abstract model class for message files
    """

    file_type = models.CharField(_("File type"), max_length=50)
    metadata = models.JSONField()

    class Meta:
        abstract = True
        ordering = ("-id",)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.before_create()
        super().save(*args, **kwargs)

    def before_create(self):
        self.set_metadata()
        ext = os.path.splitext(self.file.name)[-1]
        self.file_type = get_file_type(ext)
        return self

    def set_metadata(self):
        file = self.file
        metadata = {"file_name": file.name, "size": file.size}
        ext = os.path.splitext(file.name)[-1][1:]

        if ext in AUDIO_EXTS:
            author = title = duration = None
            try:
                audio = File(file.open("rb"), easy=True)
                duration = audio.info.length
                tags = audio.tags
                title = tags.get("title", [None])[0]
                author = (tags.get("artist") or tags.get("author") or [None])[0]
            except Exception as e:
                print(e)
            metadata.update({"title": title, "author": author, "duration": duration})
        self.metadata = metadata
