from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F, Count, Prefetch
from django.db.models.functions import Greatest, Least, Lower

from .abstract import MessageBase, MessageFileBase
from .utils import MessageFilePath, FILE_VALIDATOR, delete_file, delete_old_file


class ChatQuerySet(models.QuerySet):

    def annotate_unread(self, user):
        exp = ~Q(messages__owner=user) & Q(messages__seen=False)
        return self.annotate(unread=Count("messages", filter=exp))

    def prefetch_latest(self):
        qs = PMessage.objects.annotate_owner_name().order_by("-created")
        return self.prefetch_related(Prefetch("messages", queryset=qs))

    def select_companion(self):
        return self.prefetch_related("from_user", "to_user")

    def common_fetch(self, user):
        return self.select_companion().prefetch_latest().annotate_unread(user)


class ChatManager(models.Manager):

    def get_queryset(self) -> ChatQuerySet:
        return ChatQuerySet(self.model, using=self._db)

    def common_fetch(self, user):
        return self.get_queryset().common_fetch(user)


class PChat(models.Model):
    """
    Chat model for private chats between two users
    """

    from_user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="from_me",
        verbose_name=_("User One"),
    )

    to_user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="to_me",
        verbose_name=_("User Two"),
    )

    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created datetime")
    )

    objects = ChatManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Least("from_user", "to_user"),
                Greatest("from_user", "to_user"),
                name="unique_chat",
                violation_error_message=_("You already have a chat with this person."),
            ),
            models.CheckConstraint(
                check=~Q(from_user=F("to_user")),
                name="not_the_same_user",
                violation_error_message=_("Can't start chat with yourself."),
            ),
        ]
        indexes = [
            models.Index(
                F("created").desc(),
                name="pchat_created_idx",
            ),
        ]

        ordering = ("-created",)

    @property
    def type(self):
        return "chat"

    def get_name(self, user):
        return self.get_companion(user).get_full_name()

    def get_photo(self, user):
        return self.get_companion(user).photo

    def get_absolute_url(self, name="chat"):
        return reverse(name, kwargs={"pk": self.pk})

    def get_companion(self, user):
        """
        Returns a companion based on the user
        """
        return self.from_user if user == self.to_user else self.to_user

    def get_companion_id(self, user_id):
        return self.from_user_id if user_id == self.to_user_id else self.to_user_id

    def get_members_id(self):
        return (self.from_user_id, self.to_user_id)

    def __str__(self) -> str:
        return f"Chat: {self.from_user} and {self.to_user}"


class PMessage(MessageBase):
    """
    Message model for private chats
    """

    chat = models.ForeignKey(
        PChat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Message PChat"),
    )

    class Meta(MessageBase.Meta):
        indexes = [
            models.Index(F("created").desc(), name="pmsg_created_idx"),
            models.Index(F("seen").asc(), name="pmsg_seen_idx"),
        ]

    def get_absolute_url(self):
        return reverse("message-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.chat_id}:{super().__str__()}"


message_file_path = MessageFilePath("pchat", "message.chat_id")


class MessageFile(MessageFileBase):
    file = models.FileField(
        upload_to=message_file_path,
        validators=[
            FILE_VALIDATOR,
        ],
    )
    message = models.ForeignKey(
        "PMessage", on_delete=models.CASCADE, related_name="files"
    )

    class Meta(MessageFileBase.Meta):
        indexes = [
            models.Index(Lower("file_type"), name="pmsg_file_type_idx"),
        ]


@receiver(models.signals.post_delete, sender=MessageFile)
def auto_delete_file(sender, instance: MessageFile, **kwargs):
    delete_file(instance.file)


@receiver(models.signals.pre_save, sender=MessageFile)
def on_file_save(sender: MessageFile, instance: MessageFile, **kwargs):
    delete_old_file(sender, instance)
