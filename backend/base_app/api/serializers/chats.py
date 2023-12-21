from django.http import HttpRequest
from django.utils.functional import cached_property

from rest_framework import serializers as S

from ...models import PChat, MessageFile, PMessage

from .users import UserSerializer
from .utils import AbsoluteURLField
from .mixins import ModelSerializerMixin, MessageMixin, FileMixin


class FileSerializer(FileMixin, S.ModelSerializer):

    class Meta(FileMixin.Meta):
        model = MessageFile


class MessageSerializer(MessageMixin, S.ModelSerializer):
    """
    Serializer for private messages
    """
    files = FileSerializer(many=True, read_only=True)
    url = AbsoluteURLField()

    class Meta(MessageMixin.Meta):
        model = PMessage
        fields = MessageMixin.Meta.fields + ('chat',)
        read_only_fields = MessageMixin.Meta.read_only_fields + ('chat',)

    def get_file_serializer(self):
        return FileSerializer


class ChatSerializer(ModelSerializerMixin, S.ModelSerializer):
    """
    Private chat serializer to get and create
    """
    companion = S.SerializerMethodField()
    latest = S.SerializerMethodField()
    url = AbsoluteURLField()
    files_url = AbsoluteURLField(url_name='chat_files')
    unread = S.SerializerMethodField()

    class Meta:
        model = PChat
        fields = ('id', 'companion', 'latest', 'created',
                  'url', 'files_url', 'to_user', 'unread')
        read_only_fields = ('id',)
        extra_kwargs = {
            'to_user': {'write_only': True}
        }

    def get_latest(self, pChat: PChat):
        """
        Gets latest message from a chat
        """
        try:
            msg = pChat.messages.latest('created')
            return MessageSerializer(msg, context=self.context).data
        except Exception as e:
            print(e)
            return None

    @cached_property
    def request(self) -> HttpRequest:
        return self.context.get('request')

    def validate(self, attrs):
        attrs['from_user'] = self.request.user
        return super().validate(attrs)

    def get_companion(self, pChat: PChat):
        user = self.request.user
        companion = pChat.get_companion(user)
        return UserSerializer(companion, context=self.context).data

    def get_unread(self, pChat: PChat):
        return pChat.get_unread(self.request.user)
