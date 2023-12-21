from django.db import transaction

from rest_framework import serializers as S, exceptions as EX

from ...models import (
    Group, GroupRole, GroupMember,
    GroupBan, GroupMessage, GroupMessageFile,)

from .users import UserSerializer
from .utils import AbsoluteURLField
from .mixins import (ReprSerializerMixin, ModelSerializerMixin,
                     MessageMixin, FileMixin)


class RoleSerializer(ModelSerializerMixin, S.ModelSerializer):
    pass_instance = True

    url = AbsoluteURLField()

    class Meta:
        model = GroupRole
        fields = '__all__'
        read_only_fields = ('id', 'group',)

    def create(self, validated_data):
        self.__is_default = validated_data.get('is_default', False)
        validated_data['is_default'] = False
        return super().create(validated_data)

    def save_instance(self, instance):
        instance.is_default = self.__is_default
        instance.save()
        return instance


class GroupSerializer(ModelSerializerMixin, S.ModelSerializer):
    url = AbsoluteURLField()
    files_url = AbsoluteURLField(url_name='group-files')
    messages_url = AbsoluteURLField(url_name='group-messages')
    members_url = AbsoluteURLField(url_name='group-members')
    bans_url = AbsoluteURLField(url_name='group-bans')
    roles_url = AbsoluteURLField(url_name='group-roles')
    user_role = S.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'unique_name',
                  'url', 'messages_url', 'members_url',
                  'roles_url', 'bans_url', 'files_url', 'user_role',
                  'unique_id', 'photo', 'description', 'public',
                  'owner', 'created', 'edited')
        read_only_fields = ('id', 'unique_id', 'owner')

    def get_user_role(self, group: Group):
        user = self.context.get('request').user
        return RoleSerializer(
            group.members.select_related('role').get(user_id=user.pk).role,
            context=self.context).data

    def create(self, validated_data):
        default_role = self.initial_data.get('default_role')
        try:
            with transaction.atomic():
                group = super().create(validated_data)
                if default_role:
                    default_role['is_default'] = True
                    default_role['group_id'] = group.id
                    ser = RoleSerializer(default_role)
                    ser.is_valid(raise_exception=True)
                    ser.save()
                group.setup_group(create_default=not default_role)
        except:
            raise EX.ValidationError({'unknown': "Something went wrong."})
        return group

    def validate(self, attrs):
        return super().validate(attrs)


class MemberRoleSerializer(S.ModelSerializer):

    class Meta:
        model = GroupRole
        fields = ('id', 'name')


class MemberSerializer(ReprSerializerMixin,
                       ModelSerializerMixin,
                       S.ModelSerializer):
    url = AbsoluteURLField()

    class Meta:
        model = GroupMember
        fields = ('id', 'user', 'role', 'url', 'joint')
        read_only_fields = ('id',)

    def get_repr_fields(self):
        return {
            'user': UserSerializer(read_only=True),
            'role': MemberRoleSerializer(read_only=True)
        }

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        validated_data.pop('group', None)
        return super().update(instance, validated_data)


class GroupBanSerializer(ReprSerializerMixin,
                         ModelSerializerMixin,
                         S.ModelSerializer):
    url = AbsoluteURLField()

    class Meta:
        model = GroupBan
        fields = ('id', 'user', 'banned_by', 'url',
                  'reason', 'created', )
        read_only_fields = ('id', 'banned_by')

    def get_repr_fields(self):
        return {
            'user': UserSerializer(read_only=True),
            'banned_by': UserSerializer()
        }

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        validated_data.pop('group', None)
        validated_data.pop('banned_by', None)
        return super().update(instance, validated_data)


class GFileSerializer(FileMixin, S.ModelSerializer):

    class Meta(FileMixin.Meta):
        model = GroupMessageFile


class GMessageSerializer(ModelSerializerMixin,
                         MessageMixin,
                         S.ModelSerializer):
    files = GFileSerializer(many=True, read_only=True)
    url = AbsoluteURLField(read_only=True)

    class Meta(MessageMixin.Meta):
        model = GroupMessage
        fields = MessageMixin.Meta.fields + ('group', 'url')
        read_only_fields = MessageMixin.Meta.read_only_fields + ('group',)

    def get_file_serializer(self):
        return GFileSerializer
