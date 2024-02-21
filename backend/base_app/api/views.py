import re
from itertools import chain

from django.db.models import Max, F, Q
from django.http import HttpRequest
from django.utils.functional import cached_property
from django.core.validators import validate_email

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics as G, mixins as MX
from rest_framework.pagination import LimitOffsetPagination

from ..models import User, PChat, Group, FILE_TYPES, MessageFile

from . import serializers as S
from . import permissions as P
from .pagination import ChatLimitPagination


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


@api_view()
@permission_classes([])
def check_username(request: HttpRequest):
    username = request.GET.get("q")
    is_valid = False
    if username:
        try:
            User.username_validator(username)
            is_valid = not User.objects.filter(username=username).exists()
        except Exception:
            pass
    return Response({"is_valid": is_valid})


@api_view()
@permission_classes([])
def check_user_mail(request: HttpRequest):
    email = request.GET.get("q")
    is_valid = False
    if email:
        try:
            validate_email(email)
            is_valid = not User.objects.filter(email=email).exists()
        except Exception:
            pass
    return Response({"is_valid": is_valid})


class MultiSerializerMixin:
    options: dict[type, dict[str]] = None

    def multi_serialize(self, objs, **kwargs) -> list[dict]:
        result = []
        options = self.options
        append = result.append
        context = self.get_serializer_context()
        for obj in objs:
            cls_name = type(obj).__name__
            option = options[cls_name]
            data: dict = option["ser"](instance=obj, context=context, **kwargs).data
            data["type"] = option.get("type", cls_name.lower())
            append(data)
        return result


class SearchAPIView(MultiSerializerMixin, G.ListAPIView):
    options = {
        "Group": {"ser": S.PublicGroupSerializer},
        "User": {"ser": S.UserSerializer},
    }

    @staticmethod
    def calc_user(user, query: str):
        priority = not bool(
            re.match(query, user.username) or re.match(query, user.first_name)
        )
        return (priority, user.username)

    @staticmethod
    def calc_group(group, query: str):
        priority = not bool(
            re.match(query, group.unique_name) or re.match(query, group.name)
        )
        return (priority, group.unique_name)

    @classmethod
    def calc_dispatcher(cls, obj, query: str):
        return (cls.calc_user if isinstance(obj, User) else cls.calc_group)(obj, query)

    def get_queryset(self):
        qr = self.request.GET.get("q", "")
        user = self.request.user
        user_qs = User.objects.search_people(qr, user)[:5]
        group_qs = Group.objects.search_groups(qr, user)[:5]
        return sorted(
            chain(user_qs, group_qs), key=lambda obj: self.calc_dispatcher(obj, qr)
        )

    def list(self, request, *args, **kwargs):
        qs_list = self.get_queryset()
        data = self.multi_serialize(qs_list)
        return Response(
            {
                "count": len(data),
                "results": data,
            }
        )


class UsersAPIView(MX.RetrieveModelMixin, MX.ListModelMixin, G.GenericAPIView):
    serializer_class = S.UserSerializer

    def get_queryset(self):
        return User.objects.all().annotate_chat(self.request.user)

    def get_serializer(self, *args, **kwargs):
        kwargs["exclude_chat"] = False
        return super().get_serializer(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.lookup_field in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class ChatsLimitPagination(LimitOffsetPagination):
    default_limit = 10

    def get_count(self, queryset):
        return self._count_qs.count()


class ChatsAPIView(G.ListCreateAPIView):
    """
    API view to get private chats that user have
    """

    serializer_class = S.ChatSerializer
    pagination_class = ChatsLimitPagination

    def get_queryset(self):
        chat_id = self.request.GET.get("id")
        user = self.request.user
        qs = user.get_chats().common_fetch(user)
        if chat_id:
            return qs.filter(id=chat_id)
        chats = qs.alias(last_created=Max("messages__created", default=F("created")))
        return chats.order_by("-last_created")

    def paginate_queryset(self, queryset):
        if self.paginator is not None:
            self.paginator._count_qs = self.get_count_qs()
        return super().paginate_queryset(queryset)

    def get_count_qs(self):
        return self.request.user.get_chats().values("pk")


class ChatMixin:

    @cached_property
    def chat(self):
        """
        Getter for the chat. Checks if the
        chat belongs to user
        """
        user = self.request.user
        return G.get_object_or_404(user.get_chats(), pk=self.kwargs.get("pk"))


class ChatAPIView(G.RetrieveAPIView):
    """
    API view to get messages from a private chat
    """

    serializer_class = S.ChatSerializer

    def get_queryset(self):
        return self.request.user.get_chats()


class ChatMessagesAPIView(ChatMixin, G.ListCreateAPIView):
    serializer_class = S.MessageSerializer
    pagination_class = ChatLimitPagination

    def get_queryset(self):
        return self.chat.messages.common_fetch()

    def perform_create(self, serializer: S.MessageSerializer):
        return serializer.save(chat=self.chat, owner=self.request.user)


class ChatFilesView(ChatMixin, G.ListAPIView):
    """
    API view for chat files
    """

    serializer_class = S.FileSerializer

    def get_queryset(self):
        type_ = self.request.GET.get("type", "")
        expr = Q(message__chat_id=self.chat.pk)
        if type_.lower() in FILE_TYPES:
            expr &= Q(file_type=type_)
        return MessageFile.objects.filter(expr)


class AllChatsAPIView(MultiSerializerMixin, G.ListAPIView):
    options = {
        "Group": {"ser": S.GroupSerializer},
        "PChat": {"ser": S.ChatSerializer, "type": "chat"},
    }

    def get_queryset(self):
        return self.request.user.get_generic_chats()

    def paginate_queryset(self, queryset):
        chats_ = super().paginate_queryset(queryset)
        generics = dict.fromkeys("%(type)s:%(id)s" % chat for chat in chats_)
        chats = set()
        groups = set()
        for chat in chats_:
            if chat["type"] == "chat":
                chats.add(chat["id"])
            else:
                groups.add(chat["id"])
        user = self.request.user
        qs = chain(
            PChat.objects.common_fetch(user).filter(id__in=chats).order_by(),
            Group.objects.common_fetch().filter(id__in=groups).order_by(),
        )
        generics.update((f"{chat.type}:{chat.pk}", chat) for chat in qs)
        return generics.values()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        chats = self.paginate_queryset(queryset)
        data = self.multi_serialize(chats)
        return self.get_paginated_response(data)
