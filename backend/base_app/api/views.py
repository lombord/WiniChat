from collections import OrderedDict
from itertools import chain

from django.db.models import Max, F, Q
from django.utils.functional import cached_property

from rest_framework import generics as G
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.utils.urls import replace_query_param

from ..models import User, PChat, Group, FILE_TYPES, MessageFile

from . import serializers as S
from . import permissions as P


class SessionAPIView(G.RetrieveUpdateAPIView):
    """
    API view for session related requests
    """
    serializer_class = S.UserSerializer

    def get_object(self):
        user = self.request.user
        # make user online
        user.status = 1
        return user


class UserRegisterAPIView(G.CreateAPIView):
    """
    API view for user registration
    """
    serializer_class = S.UserRegisterSerializer
    permission_classes = [P.isNotAuthenticated]


class PeopleAPIView(G.ListAPIView):
    """
    API view to get all people that user 
    has no chat with
    """
    serializer_class = S.UserSerializer

    def get_queryset(self):
        qr = self.request.GET.get('qr', '')
        user = self.request.user
        people = user.get_chat_people()
        qs = User.objects.search_people(qr, user.pk).difference(people)
        return qs[:30]


class ChatsLimitPagination(LimitOffsetPagination):
    default_limit = 10


class ChatsAPIView(G.ListCreateAPIView):
    """
    API view to get private chats that user have 
    """
    serializer_class = S.ChatSerializer
    pagination_class = ChatsLimitPagination

    def get_queryset(self):
        chat_id = self.request.GET.get('id')
        if chat_id:
            return self.request.user.get_chats().filter(id=chat_id)
        chats = self.request.user.get_chats().annotate(
            last_created=Max('messages__created', default=F('created')))
        return chats.order_by('-last_created')


class ChatLimitPagination(LimitOffsetPagination):
    default_limit = 30

    def get_previous_link(self):
        url = super().get_previous_link()
        try:
            assert url and self.offset
            if self.offset - self.limit <= 0:
                return replace_query_param(url, self.limit_query_param, self.offset)
        except:
            pass
        return url


class ChatMixin:

    @cached_property
    def chat(self):
        """
        Getter for the chat. Checks if the
        chat belongs to user
        """
        user = self.request.user
        return G.get_object_or_404(
            user.get_chats(), pk=self.kwargs.get('pk'))


class ChatAPIView(ChatMixin, G.ListCreateAPIView):
    """
    API view to get messages from a private chat
    """
    serializer_class = S.MessageSerializer
    pagination_class = ChatLimitPagination

    def get_queryset(self):
        return self.chat.messages.all()

    def perform_create(self, serializer: S.MessageSerializer):
        return serializer.save(chat=self.chat, owner=self.request.user)


class ChatFilesView(ChatMixin, G.ListAPIView):
    """
    API view for chat files
    """
    serializer_class = S.FileSerializer

    def get_queryset(self):
        type_ = self.request.GET.get('type', '')
        expr = Q(message__chat_id=self.chat.pk)
        if type_.lower() in FILE_TYPES:
            expr &= Q(file_type=type_)
        return MessageFile.objects.filter(expr)


class AllChatsAPIView(G.ListAPIView):
    serializer_class = S.GenericChatSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.get_generic_chats()

    def paginate_queryset(self, queryset):
        chats_ = super().paginate_queryset(queryset)
        generics = OrderedDict((chat['id'], chat)
                               for chat in chats_)
        chats = {id_ for id_, chat in generics.items()
                 if chat['type'] == 'chat'}
        groups = generics.keys() - chats
        qs = chain(PChat.objects.filter(id__in=chats),
                   Group.objects.filter(id__in=groups))
        generics.update((chat.id, chat) for chat in qs)
        return generics.values()
