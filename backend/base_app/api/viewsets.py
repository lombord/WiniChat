from functools import wraps

from django.db.models import Q
from django.http import Http404

from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins as MX
from rest_framework.decorators import action


from .serializers import (
    MessageSerializer, GroupSerializer, RoleSerializer,
    GMessageSerializer, MemberSerializer, GroupBanSerializer,
    GFileSerializer)
from ..models import PMessage, GroupMessageFile


class MessageViewSet(MX.RetrieveModelMixin,
                     MX.UpdateModelMixin,
                     MX.DestroyModelMixin,
                     GenericViewSet):
    serializer_class = MessageSerializer
    queryset = PMessage.objects.all()

    def get_object(self):
        msg = super().get_object()
        if not self.request.user.get_chats().contains(msg.chat):
            raise Http404
        return msg

    def perform_update(self, serializer: MessageSerializer):
        v_data = serializer.validated_data
        if len(v_data) == 1 and 'seen' in v_data:
            msg = serializer.instance
            expr = (~Q(owner=self.request.user) &
                    Q(created__lte=msg.created) & Q(seen=False))
            msg.chat.messages.filter(expr).update(seen=True)
            msg.seen = True
            return msg
        return serializer.save()


def group_action(*args, action=None):

    def decorator(method):

        @wraps(method)
        def wrapper(self, request, *args, **kwargs):
            self.group = self.get_object()
            self._action = action or method.__name__
            return method(self, request, *args, **kwargs)
        return wrapper

    if args and callable(args[0]):
        return decorator(args[0])
    return decorator


class MessageMixin:

    def messages_queryset(self):
        manager = self.group.messages
        lookup = getattr(self, 'messages_lookup', None)
        if lookup:
            return manager.filter(lookup)
        return manager.all()

    def messages_serializer(self):
        return GMessageSerializer

    def messages_create(self, serializer):
        serializer.save(owner=self.request.user,
                        group=self.group)

    @action(detail=True,
            methods=['get'])
    @group_action
    def messages(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @messages.mapping.post
    @group_action(action='messages')
    def post_message(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True,
            methods=['get'],
            url_path=r'messages/(?P<pk>\d+)',
            url_name='message')
    @group_action(action='messages')
    def message_detail(self, request, *args, **kwargs):
        self.action_detail()
        return self.retrieve(request, *args, **kwargs)

    @message_detail.mapping.put
    @group_action(action='messages')
    def message_update(self, request, *args, **kwargs):
        self.action_detail()
        self.messages_lookup = Q(owner=request.user)
        return self.update(request, *args, **kwargs)

    @message_detail.mapping.patch
    @group_action(action='messages')
    def message_partial_update(self, request, *args, **kwargs):
        self.action_detail()
        self.messages_lookup = Q(owner=self.request.user)
        return self.partial_update(request, *args, **kwargs)

    @message_detail.mapping.delete
    @group_action(action='messages')
    def message_destroy(self, request, *args, **kwargs):
        self.action_detail()
        if not self.group.can_delete(request.user):
            self.messages_lookup = Q(owner=self.request.user)
        return self.destroy(request, *args, **kwargs)


class MemberMixin:

    def members_queryset(self):
        return self.group.allowed_members

    def members_create(self, serializer):
        serializer.save(added_by=self.request.user,
                        group=self.group,
                        role=self.group.default_role)

    def members_serializer(self):
        return MemberSerializer

    @action(detail=True,
            methods=['get'])
    @group_action
    def members(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @members.mapping.post
    @group_action(action='members')
    def add_member(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True,
            methods=['get'],
            url_path=r'members/(?P<pk>\d+)',
            url_name='member')
    @group_action(action='members')
    def member_detail(self, request, *args, **kwargs):
        self.action_detail()
        return self.retrieve(request, *args, **kwargs)

    @member_detail.mapping.put
    @group_action(action='members')
    def member_update(self, request, *args, **kwargs):
        self.safe_update()
        return self.update(request, *args, **kwargs)

    @member_detail.mapping.patch
    @group_action(action='members')
    def member_partial_update(self, request, *args, **kwargs):
        self.safe_update()
        return self.partial_update(request, *args, **kwargs)

    @member_detail.mapping.delete
    @group_action(action='members')
    def kick_member(self, request, *args, **kwargs):
        if not self.group.can_kick(request.user.pk):
            raise PermissionDenied(
                detail="You are not allowed to kick members in this group")
        self.action_detail()
        return self.destroy(request, *args, **kwargs)


class MemberBanMixin:

    def bans_queryset(self):
        return self.group.banned_people.all()

    def bans_create(self, serializer):
        serializer.save(banned_by=self.request.user,
                        group=self.group)

    def bans_serializer(self):
        return GroupBanSerializer

    @action(detail=True,
            methods=['get'])
    @group_action
    def bans(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @bans.mapping.post
    @group_action(action='bans')
    def ban_member(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True,
            methods=['get'],
            url_path=r'bans/(?P<pk>\d+)',
            url_name='ban')
    @group_action(action='bans')
    def ban_detail(self, request, *args, **kwargs):
        self.action_detail()
        return self.retrieve(request, *args, **kwargs)

    @ban_detail.mapping.delete
    @group_action(action='bans')
    def unban_member(self, request, *args, **kwargs):
        if not self.group.can_unban(request.user.pk):
            raise PermissionDenied(
                detail="You are not allowed to unban members in this group")
        self.action_detail()
        return self.destroy(request, *args, **kwargs)


class RoleMixin:

    def roles_queryset(self):
        return self.group.roles.all()

    def roles_create(self, serializer):
        serializer.save(group=self.group)

    def roles_serializer(self):
        return RoleSerializer

    def roles_destroy(self, role):
        if role.is_default:
            raise PermissionDenied(_("Can't delete default role"))
        role.members.update(role=role.group.default_role)
        role.delete()

    @action(detail=True,
            methods=['get'])
    @group_action
    def roles(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @roles.mapping.post
    @group_action(action='roles')
    def add_role(self, request, *args, **kwargs):
        self.check_admin()
        return self.create(request, *args, **kwargs)

    @action(detail=True,
            methods=['get'],
            url_path=r'roles/(?P<pk>\d+)',
            url_name='role')
    @group_action(action='roles')
    def role_detail(self, request, *args, **kwargs):
        self.action_detail()
        return self.retrieve(request, *args, **kwargs)

    @role_detail.mapping.put
    @group_action(action='roles')
    def role_update(self, request, *args, **kwargs):
        self.safe_update()
        return self.update(request, *args, **kwargs)

    @role_detail.mapping.patch
    @group_action(action='roles')
    def role_partial_update(self, request, *args, **kwargs):
        self.safe_update()
        return self.partial_update(request, *args, **kwargs)

    @role_detail.mapping.delete
    @group_action(action='roles')
    def delete_role(self, request, *args, **kwargs):
        self.safe_update()
        return self.destroy(request, *args, **kwargs)


class GroupCommonActions:
    def files_queryset(self):
        return GroupMessageFile.objects.filter(
            message__group_id=self.group.pk)

    def files_serializer(self):
        return GFileSerializer

    @action(detail=True,
            methods=['get'])
    @group_action
    def files(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GroupViewSet(
        GroupCommonActions,
        RoleMixin,
        MemberMixin,
        MemberBanMixin,
        MessageMixin,
        ModelViewSet):
    serializer_class = GroupSerializer
    lookup_field = 'unique_id'
    lookup_url_kwarg = 'uuid'
    _action = None
    CREATE_PAT = '%s_create'
    DESTROY_PAT = '%s_destroy'
    QS_PAT = '%s_queryset'
    SER_PAT = '%s_serializer'

    def perform_create(self, serializer):
        if not self._action:
            serializer.save(owner=self.request.user)
            return
        method = getattr(self, self.CREATE_PAT % self._action,
                         super().perform_create)
        method(serializer)

    def perform_destroy(self, instance):
        method = getattr(self, self.DESTROY_PAT % self._action,
                         super().perform_destroy)
        method(instance)

    def get_queryset(self):
        if not self._action:
            return self.request.user.user_groups.all()
        method = getattr(self, self.QS_PAT % self._action,
                         super().get_queryset)
        return method()

    def get_serializer_class(self):
        method = getattr(self, self.SER_PAT % self._action,
                         super().get_serializer_class)
        return method()

    def update(self, request, *args, **kwargs):
        if not self._action:
            group = self.get_object()
            if not group.can_edit(self.request.user.pk):
                raise PermissionDenied(
                    detail=_("You're not allowed to edit this group"))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not self._action:
            group = self.get_object()
            if not group.can_edit(self.request.user.pk):
                raise PermissionDenied(
                    detail=_("You're not allowed to edit this group"))
        return super().partial_update(request, *args, **kwargs)

    def action_detail(self):
        self.lookup_field = 'pk'
        self.lookup_url_kwarg = 'pk'

    def check_admin(self):
        if not self.group.is_admin(self.request.user.pk):
            raise PermissionDenied(
                detail="Only admins can do this action.")

    def safe_update(self):
        self.check_admin()
        self.action_detail()
