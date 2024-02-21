from rest_framework import serializers as S

from ...models import PChat, MessageFile, PMessage

from .users import UserSerializer
from .utils import AbsoluteURLField
from .mixins import ModelSerializerMixin, MessageMixin, FileMixin, ChatMixin


class FileSerializer(FileMixin, S.ModelSerializer):

    class Meta(FileMixin.Meta):
        model = MessageFile


class MessageSerializer(MessageMixin, S.ModelSerializer):
    """
    Serializer for private messages
    """

    pass_instance = True

    class Meta(MessageMixin.Meta):
        model = PMessage
        fields = MessageMixin.Meta.fields + ("chat",)
        read_only_fields = MessageMixin.Meta.read_only_fields + ("chat",)

    def get_file_serializer(self):
        return FileSerializer


class ChatSerializer(ChatMixin, ModelSerializerMixin, S.ModelSerializer):
    """
    Private chat serializer to get and create
    """

    companion = S.SerializerMethodField()
    files_url = AbsoluteURLField(url_name="chat_files")

    class Meta(ChatMixin.Meta):
        model = PChat
        fields = ChatMixin.Meta.fields + ("companion", "files_url", "to_user")
        read_only_fields = ("id",)
        extra_kwargs = {"to_user": {"write_only": True}}
        msg_serializer_class = MessageSerializer

    def validate(self, attrs):
        attrs["from_user"] = self.request.user
        return super().validate(attrs)

    def get_companion(self, pChat: PChat):
        user = self.request.user
        companion = pChat.get_companion(user)
        return UserSerializer(companion, context=self.context).data
