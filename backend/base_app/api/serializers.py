import os
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers as S, exceptions as EX

from ..models import User, PChat, PMessage


class UserSerializer(S.ModelSerializer):
    """
    User serializer for update and to get main info
    """

    class Meta:
        model = User
        fields = ('id', 'username',  'first_name',
                  'last_name', 'full_name', 'bio',
                  'photo', 'status')
        extra_kwargs = {
            'full_name': {'source': 'get_full_name'},
            'status': {'source': 'is_online'},
        }
        read_only_fields = ('id', 'username',)

    def validate_photo(self, val):
        """
        Replaces old photo with new one
        if it exists and is not default
        """
        photo = self.instance.photo
        name = os.path.basename(photo.name)
        if not name.startswith('default'):
            os.remove(photo.path)
        return val


class UserRegisterSerializer(S.ModelSerializer):
    """
    Serializer to register a user
    """
    password2 = S.CharField(max_length=128,
                            label='Confirm Password',
                            write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password', 'password2')
        extra_kwargs = {
            'password': {
                'help_text': 'Your password must contain at least 8 characters.',
            }
        }

    def validate_password2(self, value):
        """
        Validator for password match
        """
        password1 = self.initial_data['password']
        if password1 != value:
            raise S.ValidationError("Passwords didn't match!")
        return value

    def validate_password(self, value):
        """
        Validates base password requirements of django
        """
        try:
            validate_password(value)
        except Exception as e:
            raise S.ValidationError(e.messages)
        return value

    def create(self, validated_data: dict):
        """
        Creates a new user after validation
        """
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class FileSerializer(S.Serializer):
    url = S.FileField(source='file', default=None)
    file_type = S.CharField()
    file_name = S.SerializerMethodField()

    def get_file_name(self, instance: PMessage):
        if instance.file:
            return os.path.basename(instance.file.name)


class MessageSerializer(S.ModelSerializer):
    """
    Serializer for private messages
    """
    files = FileSerializer(source='*', read_only=True)

    class Meta:
        model = PMessage
        fields = ('id', 'owner', 'content', 'file',
                  'files', 'created', 'chat', 'edited')
        read_only_fields = ('id', 'owner', 'chat', 'files')
        extra_kwargs = {
            'file': {'write_only': True,
                     'required': False, 'default': None,
                     'initial': None, 'allow_null': True}
        }


class ChatSerializer(S.ModelSerializer):
    """
    Private chat serializer to get and create
    """
    companion = S.SerializerMethodField()
    latest = S.SerializerMethodField()
    url = S.SerializerMethodField()

    class Meta:
        model = PChat
        fields = ('id', 'companion', 'latest', 'created',
                  'url', 'to_user')
        read_only_fields = ('id',)
        extra_kwargs = {
            'to_user': {'write_only': True}
        }

    def get_latest(self, pChat: PChat):
        """
        Gets latest message from a chat
        """
        try:
            chat = pChat.messages.latest('created')
            return MessageSerializer(chat, context=self.context).data
        except:
            return None

    @cached_property
    def request(self) -> HttpRequest:
        return self.context.get('request')

    def create(self, validated_data):
        validated_data['from_user'] = self.request.user
        try:
            chat = self.Meta.model(**validated_data)
            chat.full_clean()
            chat.save()
        except ValidationError as e:
            raise EX.ValidationError(e.message_dict)
        return chat

    def get_url(self, pChat: PChat):
        """
        Gets absolute url for a chat
        """
        abs_url = pChat.get_absolute_url()
        url = self.request.build_absolute_uri(abs_url)
        return url

    def get_companion(self, pChat: PChat):
        user = self.request.user
        companion = pChat.get_companion(user)
        return UserSerializer(companion, context=self.context).data
