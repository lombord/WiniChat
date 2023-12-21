from django.http import HttpRequest
from django.utils.functional import cached_property

from rest_framework import serializers as S

from .utils import AbsoluteURLField


class LatestSerializer(S.Serializer):
    owner_name = S.CharField(source='owner.username')
    content = S.CharField()
    created = S.DateTimeField()
    seen = S.BooleanField()


class GenericChatSerializer(S.Serializer):
    type = S.CharField()
    id = S.IntegerField()
    name = S.SerializerMethodField()
    photo = S.SerializerMethodField()
    unread = S.SerializerMethodField()
    latest = S.SerializerMethodField()
    url = AbsoluteURLField()

    @cached_property
    def request(self) -> HttpRequest:
        return self.context.get('request')

    def get_name(self, chat):
        return getattr(chat, 'name', None) or chat.get_name(self.request.user)

    def get_photo(self, chat):
        file = getattr(chat, 'photo', None) or chat.get_photo(
            self.request.user)
        return self.request.build_absolute_uri(file.url)

    def get_unread(self, chat):
        try:
            return chat.get_unread(self.request.user)
        except:
            return 0

    def get_latest(self, chat):
        try:
            msg = chat.messages.latest('created')
            return LatestSerializer(msg, context=self.context).data
        except Exception as e:
            return
