import os

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers as S

from ...models import User


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
