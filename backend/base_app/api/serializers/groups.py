from django.db import transaction

from rest_framework import serializers as S, exceptions as EX

from ...models import (
    Group,
    GroupRole,
    GroupMember,
    GroupBan,
    GroupMessage,
    GroupMessageFile,
)

from .users import UserSerializer
from .utils import AbsoluteURLField, clean_old_photo
from .mixins import (
    ReprSerializerMixin,
    DynamicFieldsMixin,
    GroupMixin,
    ModelSerializerMixin,
    MessageMixin,
    FileMixin,
    ChatMixin,
)


class GFileSerializer(FileMixin, S.ModelSerializer):

    class Meta(FileMixin.Meta):
        model = GroupMessageFile


class GMessageSerializer(MessageMixin, ModelSerializerMixin, S.ModelSerializer):

    pass_instance = True
    url = AbsoluteURLField(read_only=True)

    class Meta(MessageMixin.Meta):
        model = GroupMessage
        fields = MessageMixin.Meta.fields + ("group", "url")
        read_only_fields = MessageMixin.Meta.read_only_fields + ("group",)

    def get_file_serializer(self):
        return GFileSerializer


class RoleSerializer(DynamicFieldsMixin, ModelSerializerMixin, S.ModelSerializer):
    pass_instance = True

    url = AbsoluteURLField()

    class Meta:
        model = GroupRole
        fields = "__all__"
        read_only_fields = ("id", "group", "is_owner", "is_default")


class PublicGroupSerializer(GroupMixin, S.ModelSerializer):
    url = AbsoluteURLField(url_name="public-group-detail")

    class Meta:
        model = Group
        fields = (
            "type",
            "url",
            "id",
            "name",
            "unique_name",
            "members",
            "online",
            "photo",
            "public",
        )

    def __init__(self, *args, **kwargs):
        kwargs["read_only"] = True
        super().__init__(*args, **kwargs)


class GroupSerializer(ChatMixin, GroupMixin, ModelSerializerMixin, S.ModelSerializer):

    class Meta(ChatMixin.Meta):
        model = Group
        fields = ChatMixin.Meta.fields + (
            "name",
            "unique_name",
            "members",
            "online",
            "photo",
            "description",
            "public",
            "edited",
        )
        read_only_fields = ("id",)

        msg_serializer_class = GMessageSerializer

    def get_message(self, group):
        return group.latest[0]

    def validate_photo(self, val):
        if self.instance:
            clean_old_photo(self.instance.photo)
        return val

    def create(self, validated_data):
        try:
            with transaction.atomic():
                group = super().create(validated_data)
                group.setup_group()
        except Exception as e:
            raise EX.ValidationError({"unknown": "Something went wrong."})
        return group


class MemberSerializer(ReprSerializerMixin, ModelSerializerMixin, S.ModelSerializer):
    url = AbsoluteURLField()
    last_activity = S.SerializerMethodField()

    class Meta:
        model = GroupMember
        fields = ("id", "url", "user", "role", "joint", "last_activity")
        read_only_fields = ("id",)
        extra_kwargs = {"role": {"required": False, "allow_null": True}}

    def get_last_activity(self, member):
        try:
            return getattr(member, "last_activity", member.joint)
        except Exception:
            pass

    def __init__(self, *args, **kwargs):
        self.user_kwargs = kwargs.pop("user_kwargs", {})
        self.role_kwargs = kwargs.pop("role_kwargs", {})
        super().__init__(*args, **kwargs)

    def get_repr_fields(self):
        user_kwargs = self.user_kwargs
        user_kwargs.setdefault(
            "include", ("id", "photo", "url", "status", "first_name", "last_name")
        )
        role_kwargs = self.role_kwargs
        role_kwargs.setdefault("include", ("id", "name"))
        return {
            "user": UserSerializer(read_only=True, **user_kwargs),
            "role": RoleSerializer(read_only=True, **role_kwargs),
        }

    def update(self, instance, validated_data):
        validated_data.pop("user", None)
        validated_data.pop("group", None)
        return super().update(instance, validated_data)


class GroupBanSerializer(ReprSerializerMixin, ModelSerializerMixin, S.ModelSerializer):
    url = AbsoluteURLField()

    class Meta:
        model = GroupBan
        fields = (
            "id",
            "user",
            "banned_by",
            "url",
            "reason",
            "created",
        )
        read_only_fields = ("id", "banned_by")

    def get_repr_fields(self):
        return {
            "user": UserSerializer(read_only=True),
            "banned_by": UserSerializer(read_only=True),
        }

    def update(self, instance, validated_data):
        validated_data.pop("user", None)
        validated_data.pop("group", None)
        validated_data.pop("banned_by", None)
        return super().update(instance, validated_data)
