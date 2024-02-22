"""Group Viewsets"""

import re

from django.db.models import Q, Subquery, OuterRef, F
from django.db.models.functions import Greatest
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from ...models import GroupMessageFile, FILE_TYPES, User, Group, UNIQUE_NAME_RE

from ..serializers import (
    UserSerializer,
    GroupSerializer,
    RoleSerializer,
    GMessageSerializer,
    MemberSerializer,
    GroupBanSerializer,
    GFileSerializer,
)

from .utils import nested_action, exc_manager
from .mixins import NestedViewSetMixin


class MessageMixin:
    """Mixin to handle group message requests"""

    def messages_queryset(self):
        if self.request.method == "DELETE":
            return self.group.messages.all()
        qs = self.group.messages.common_fetch()
        lookup = getattr(self, "messages_lookup", None)
        if lookup:
            qs = qs.filter(lookup)
        return qs

    def messages_ser_class(self):
        return GMessageSerializer

    def messages_create(self, serializer):
        serializer.save(owner=self.request.user, group=self.group)

    @action(detail=True, methods=["get"])
    @nested_action
    def messages(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @messages.mapping.post
    @nested_action(action="messages")
    def post_message(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["get"],
        url_path=r"messages/(?P<pk>\d+)",
        url_name="message",
    )
    @nested_action(action="messages", detail=True)
    def message_detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @message_detail.mapping.put
    @nested_action(action="messages", detail=True)
    def message_update(self, request, *args, **kwargs):
        self.messages_lookup = Q(owner=request.user)
        return self.update(request, *args, **kwargs)

    @message_detail.mapping.patch
    @nested_action(action="messages", detail=True)
    def message_partial_update(self, request, *args, **kwargs):
        self.messages_lookup = Q(owner=self.request.user)
        return self.partial_update(request, *args, **kwargs)

    @message_detail.mapping.delete
    @nested_action(action="messages", detail=True)
    def message_destroy(self, request, *args, **kwargs):
        if not self.group.can_delete(request.user):
            self.messages_lookup = Q(owner=self.request.user)
        return self.destroy(request, *args, **kwargs)


class RoleMixin:
    """Mixin to handle group role requests"""

    def roles_queryset(self):
        qs = self.group.roles.all()
        if self.nested_detail:
            return qs
        query = self.request.GET.get("q")
        qs = self.group.roles.order_by("priority")
        if query:
            qs = (
                qs.filter(name__icontains=query)
                .alias(query_priority=Q(name__istartswith=query))
                .order_by("-query_priority", "name")
            )
        return qs

    def roles_ser_class(self):
        return RoleSerializer

    def roles_create(self, serializer):
        serializer.save(
            group=self.group,
            created_by=self.request.user,
            is_default=False,
            is_owner=False,
        )

    def roles_update(self, serializer: RoleSerializer):
        with exc_manager():
            assert self.group.manage_role_over(
                self.request.user.pk, serializer.instance
            ), "You can't edit this role"
        serializer.save()

    def roles_destroy(self, role):
        with exc_manager():
            assert not role.is_special, "Special roles cannot be deleted"
            assert self.group.manage_role_over(
                self.request.user.pk, role
            ), "You can't delete this role"
            role.delete()

    @action(detail=True, methods=["get"])
    @nested_action
    def roles(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @roles.mapping.post
    @nested_action(action="roles")
    def add_role(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(
        detail=True, methods=["get"], url_path=r"roles/(?P<pk>\d+)", url_name="role"
    )
    @nested_action(action="roles", detail=True)
    def role_detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @role_detail.mapping.put
    @nested_action(action="roles", detail=True)
    def role_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @role_detail.mapping.patch
    @nested_action(action="roles", detail=True)
    def role_partial_update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @role_detail.mapping.delete
    @nested_action(action="roles", detail=True)
    def delete_role(self, request, *args, **kwargs):
        role = self.get_object()
        self.roles_destroy(role)
        def_role = self.group.default_role
        serializer = self.get_serializer(def_role)
        return Response(serializer.data)


class RoleOptionsMixin:
    """Mixin to handle group role option requests"""

    def role_opts_queryset(self):
        lookup = Q(priority__gt=self.user_role.priority)
        query = self.request.GET.get("q")
        if query:
            lookup &= Q(name__icontains=query)
        return (
            self.group.roles.filter(lookup)
            .order_by("priority")
            .only("name", "group", "priority")
        )

    def role_opts_ser_class(self):
        return RoleSerializer

    def role_opts_ser_kwargs(self):
        return {"include": ["id", "name", "priority", "group"]}

    @action(
        detail=True, methods=["get"], url_path="role-options", url_name="role_options"
    )
    @nested_action
    def role_opts(self, request, *args, **kwargs):
        with exc_manager(def_exc=PermissionDenied):
            user_role = self.user_role = self.group.get_user_role(
                request.user.pk, ["manage_role"]
            )
            assert user_role.has_perm("manage_role"), _(
                "You are not allowed to manage roles"
            )
        return self.list(request, *args, **kwargs)


class MemberMixin:
    """Mixin to handle group member requests"""

    def members_queryset(self):
        if self.nested_detail:
            return self.group.members.select_related("user", "role")
        query = self.request.GET.get("q")
        if query:
            qs = self.group.search_member(query)
        else:
            sub_q = Subquery(
                self.group.messages.filter(owner_id=OuterRef("user_id"))
                .order_by("-created")
                .values("created")[:1]
            )
            qs = self.group.allowed_members.annotate(
                last_activity=Greatest(sub_q, F("joint"))
            ).order_by("-last_activity")
        return qs.select_related("user", "role").only(
            "joint",
            "group",
            "user",
            "user__first_name",
            "user__last_name",
            "user__photo",
            "user__status",
            "role",
            "role__name",
        )

    def members_ser_class(self):
        return MemberSerializer

    def members_ser_kwargs(self):
        if self.nested_detail:
            return {"role_kwargs": {"include": None}}
        return {}

    def members_create(self, serializer: MemberSerializer):
        serializer.save(
            added_by=self.request.user, group=self.group, role=self.group.default_role
        )

    def members_update(self, serializer: MemberSerializer):
        with exc_manager():
            user = self.request.user
            user_role = self.group.get_user_role(
                user,
                [
                    "manage_role",
                ],
            )
            member_role = serializer.instance.role
            assert user_role.manage_role_over(member_role), _(
                "This member's role has higher priority than yours and cannot be managed by you."
            )
            new_role = serializer.validated_data["role"]
            assert user_role.has_priority_over(new_role), _(
                "This role has higher priority than yours and cannot be set to this member."
            )
            serializer.save()

    def members_destroy(self, instance):
        user = self.request.user
        with exc_manager():
            assert not instance.role.is_owner, "Owner cannot be kicked out."
            assert user == instance.user or self.group.can_kick(
                user.pk, instance.role
            ), "You are not allowed to kick this member out."
            instance.delete()

    def members_bulk_clean(self, data):
        user = self.request.user
        with exc_manager("Users are not valid.", def_exc=ValidationError):
            people = user.chatted_people.filter(pk__in=data["users"])
            g_people = self.group.all_people.values("pk")
            return list(people.exclude(pk__in=g_people))

    def members_bulk_create(self, users: list):
        group = self.group
        model = group.members.model
        role = group.default_role
        add_user = self.request.user
        members = model.objects.bulk_create(
            model(user=user, group=group, role=role, added_by=add_user)
            for user in users
        )
        return members

    def members_bulk_try(self, request):
        if not self.group.has_perm(request.user, "add_user"):
            raise PermissionDenied(_("You do not have a permission to add members"))

        with exc_manager(main_exc=ValidationError):
            users = self.members_bulk_clean(request.data)
            assert users, "No valid users were passed."
            return self.members_bulk_create(users)

    def members_bulk(self, request, *args, **kwargs):
        members = self.members_bulk_try(request)
        serializer = self.get_serializer(instance=members, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["get"])
    @nested_action
    def members(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @members.mapping.post
    @nested_action(action="members")
    def add_member(self, request, *args, **kwargs):
        if "users" in request.data:
            return self.members_bulk(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    @action(
        detail=True, methods=["get"], url_path=r"members/(?P<pk>\d+)", url_name="member"
    )
    @nested_action(action="members", detail=True)
    def member_detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @member_detail.mapping.put
    @nested_action(action="members", detail=True)
    def member_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @member_detail.mapping.patch
    @nested_action(action="members", detail=True)
    def member_partial_update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @member_detail.mapping.delete
    @nested_action(action="members", detail=True)
    def kick_member(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @action(methods=["delete"], detail=True)
    @nested_action(action="members")
    def leave(self, request, *args, **kwargs):
        member = get_object_or_404(self.group.members, user_id=request.user)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberBanMixin:
    """Mixin to handle group ban requests"""

    def bans_queryset(self):
        query = self.request.GET.get("q")
        qs = self.group.bans.select_related("user", "banned_by")
        if query:
            qs = (
                qs.filter(
                    Q(user__username__icontains=query)
                    | Q(user__first_name__icontains=query)
                    | Q(user__last_name__icontains=query)
                )
                .alias(
                    q_priority=(
                        Q(user__username__istartswith=query)
                        | Q(user__first_name__istartswith=query)
                    )
                )
                .order_by("-q_priority", "user__username")
            )
        return qs

    def bans_ser_class(self):
        return GroupBanSerializer

    def bans_create(self, serializer):
        serializer.save(banned_by=self.request.user, group=self.group)

    def bans_destroy(self, instance):
        with exc_manager():
            assert self.group.can_unban(
                self.request.user.pk, instance.banned_by_id
            ), "You are not allowed to unban this user"
            instance.delete()

    @action(detail=True, methods=["get"])
    @nested_action
    def bans(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @bans.mapping.post
    @nested_action(action="bans")
    def ban_member(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path=r"bans/(?P<pk>\d+)", url_name="ban")
    @nested_action(action="bans", detail=True)
    def ban_detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @ban_detail.mapping.delete
    @nested_action(action="bans", detail=True)
    def unban_member(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GroupInviteMixin:
    """Mixin to handle group invitation requests"""

    def invites_queryset(self):
        query = self.request.GET.get("q", "")
        qs = User.objects.search_friends(query, self.request.user)
        return qs.exclude(pk__in=self.group.all_people.values("pk"))

    def invites_ser_class(self):
        return UserSerializer

    def invites_ser_kwargs(self):
        return {"include": ("id", "username", "full_name", "photo", "url", "chat_id")}

    @action(detail=True, methods=["get"])
    @nested_action
    def invites(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GroupFilesMixin:
    """Mixin to handle group file requests"""

    def files_queryset(self):
        type_ = self.request.GET.get("type", "")
        expr = Q(message__group_id=self.group.pk)
        if type_.lower() in FILE_TYPES:
            expr &= Q(file_type=type_)
        return GroupMessageFile.objects.filter(expr)

    def files_ser_class(self):
        return GFileSerializer

    @action(detail=True, methods=["get"])
    @nested_action
    def files(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GroupViewSet(
    NestedViewSetMixin,
    RoleMixin,
    RoleOptionsMixin,
    MemberMixin,
    MemberBanMixin,
    MessageMixin,
    GroupFilesMixin,
    GroupInviteMixin,
    ModelViewSet,
):
    """ViewSet to handle group requests including nested actions"""

    serializer_class = GroupSerializer
    lookup_field = "pk"
    lookup_url_kwarg = "group_pk"
    root_obj_name = "group"

    def root_queryset(self):
        user = self.request.user
        qs = user.allowed_groups.all().order_by()
        if self.is_nested:
            return qs.only("public", "owner")
        if self.request.method == "DELETE":
            return qs
        sub_q = qs.values("pk")
        return Group.objects.common_fetch().filter(pk__in=sub_q)

    def root_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def root_update(self, serializer):
        group = serializer.instance
        with exc_manager():
            role = group.get_user_role(self.request.user.pk, ["edit_group"])
            assert role.has_perm("edit_group"), _(
                "You're not allowed to edit this group"
            )

        data = serializer.validated_data
        if not role.is_owner:
            data.pop("public", None)
            data.pop("unique_name", None)
        else:
            if not data.get("public", True):
                data["unique_name"] = None
        if data:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        if self.is_nested:
            return super().destroy(request, *args, **kwargs)
        group = self.get_object()
        if not group.is_owner(self.request.user.pk):
            raise PermissionDenied(_("You're not allowed to delete this group"))
        members = list(group.online_ids)
        group.delete()
        return Response(members)

    @action(detail=True, methods=["get"], url_path=r"my-role", url_name="my-role")
    @nested_action
    def my_role(self, request, *args, **kwargs):
        """Action method to get request user's role in this group"""
        role = get_object_or_404(
            self.group.members.select_related("role"), user=request.user
        ).role
        role.group = self.group
        context = self.get_serializer_context()
        data = RoleSerializer(role, context=context).data
        return Response(data)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"check-name",
        url_name="check-group-name",
    )
    def check_group_name(self, request, *args, **kwargs):
        """Action method to validate group unique name"""
        name = request.GET.get("q")
        is_valid = False
        if name and re.match(UNIQUE_NAME_RE, name, flags=re.IGNORECASE):
            qs = Group.objects.filter(public=True, unique_name=name)
            is_valid = not qs.exists()
        return Response({"is_valid": is_valid})
