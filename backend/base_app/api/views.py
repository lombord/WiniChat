from django.db.models import Max, F
from rest_framework import generics as G
from rest_framework.pagination import LimitOffsetPagination

from ..models import User

from . import serializers as S
from . import permissions as P


class MyLimitPagination(LimitOffsetPagination):
    default_limit = 10


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


class ChatsAPIView(G.ListCreateAPIView):
    """
    API view to get private chats that user have 
    """
    serializer_class = S.ChatSerializer
    pagination_class = MyLimitPagination

    def get_queryset(self):
        chat_id = self.request.GET.get('id')
        if chat_id:
            return self.request.user.get_chats().filter(id=chat_id)
        chats = self.request.user.get_chats().annotate(
            last_created=Max('messages__created', default=F('created')))
        return chats.order_by('-last_created')


class ChatAPIView(G.ListCreateAPIView):
    """
    API view to get messages from a private chat
    """
    serializer_class = S.MessageSerializer
    _chat = None

    @property
    def chat(self):
        """
        Getter for the chat. Checks if the
        chat belongs to user
        """
        if not self._chat:
            user = self.request.user
            self._chat = G.get_object_or_404(
                user.get_chats(), pk=self.kwargs.get('pk'))
        return self._chat

    def get_queryset(self):
        return self.chat.messages.all()

    def perform_create(self, serializer: S.MessageSerializer):
        return serializer.save(chat=self.chat, owner=self.request.user)
