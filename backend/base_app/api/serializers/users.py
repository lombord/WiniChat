import os

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers as S, exceptions as EX

from ...models import User


class UserEditMixin:

    def validate_password(self, value):
        """
        Validates base password requirements of django
        """
        try:
            validate_password(value)
        except Exception as e:
            raise S.ValidationError(e.messages)
        return value


class UserSerializer(UserEditMixin, S.ModelSerializer):
    """
    User serializer for update and to get main info
    """

    old_password = S.CharField(max_length=128,
                               label="Password",
                               write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username',  'first_name',
                  'last_name', 'full_name', 'bio',
                  'photo', 'status', 'old_password',
                  'password')
        extra_kwargs = {
            'full_name': {'source': 'get_full_name'},
            'status': {'source': 'is_online'},
            'password': {'write_only': True,
                         'label': 'New Password'},
        }
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = getattr(self, 'initial_data', None)
        if data and data.keys() & {'password', 'old_password'}:
            data.setdefault('password', '')
            data.setdefault('old_password', '')

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

    def validate_old_password(self, val):
        if not self.instance.check_password(val):
            raise EX.ValidationError(
                {'old_password': "Old password is not valid."})
        return val

    def validate_password(self, value):
        if value == self.initial_data.get('old_password'):
            raise EX.ValidationError(
                'Your new password must be different from your current password.')
        return super().validate_password(value)

    def update(self, instance, validated_data):
        validated_data.pop('old_password', None)
        pwd = validated_data.pop('password', None)
        if pwd:
            instance.set_password(pwd)
        return super().update(instance, validated_data)


class UserRegisterSerializer(UserEditMixin, S.ModelSerializer):
    """
    Serializer to register a user
    """
    password2 = S.CharField(max_length=128,
                            label='Confirm Password',
                            write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username',
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

    def create(self, validated_data: dict):
        """
        Creates a new user after validation
        """
        validated_data.pop('password2')
        password = validated_data.pop('password')
        try:
            user = User(**validated_data)
            user.set_password(password)
            user.full_clean()
        except ValidationError as e:
            raise EX.ValidationError(e.message_dict)
        user.save()
        return user
