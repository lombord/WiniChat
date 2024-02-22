"""General mixins for serializers"""

from django.http import HttpRequest
from django.utils.functional import cached_property
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from rest_framework import serializers as S, exceptions as EX

from .utils import AbsoluteURLField


class ReprSerializerMixin:
    """Mixin to customize the representation serializer for fields"""

    def to_representation(self, args, **kwargs):
        self.fields.update(self.get_repr_fields())
        return super().to_representation(args, **kwargs)

    def get_repr_fields(self):
        """
        Hook to return representation serializers as a mapping
        where keys are the name of the fields
        """
        return {}


class DynamicFieldsMixin:
    """
    Mixin to add dynamic fields feature
    """

    def __init__(self, *args, include=None, exclude=None, **kwargs):
        """Specify fields to include or exclude for serialization

        Args:
            include (list[str], optional): fields to include. Defaults to None.
            exclude (list[str], optional): fields to exclude. Defaults to None.
        """

        assert not (include and exclude), "Can't have both include and exclude!"
        super().__init__(*args, **kwargs)
        if include or exclude:
            if include:
                exclude = set(self.fields) - set(include)
            for field_name in exclude:
                self.fields.pop(field_name)


class RequestMixin:
    """Mixin to add request objet as property"""

    @cached_property
    def request(self) -> HttpRequest:
        return self.context.get("request")


class ModelSerializerMixin:
    """Mixin to add model level validation when creating"""

    # defines whether to save and pass instance created for validation
    pass_instance = False

    def create(self, validated_data):
        try:
            with transaction.atomic():
                instance = self.Meta.model(**validated_data)
                instance.clean()
                instance.validate_unique()
                instance.validate_constraints()
                if self.pass_instance:
                    return self.save_instance(instance)
                return super().create(validated_data)

        except (EX.ValidationError, ValidationError) as exc:
            raise EX.ValidationError(detail=S.as_serializer_error(exc))
        except IntegrityError as error:
            raise EX.ValidationError from error

    def update(self, instance, validated_data):
        try:
            super().update(instance, validated_data)
        except IntegrityError as error:
            raise EX.ValidationError from error
        return instance

    def save_instance(self, instance):
        """Hook to save instance"""
        instance.save()
        return instance


class ChatMixin(DynamicFieldsMixin, RequestMixin, metaclass=S.SerializerMetaclass):
    """Main Mixin for chats that includes common actions and fields"""

    url = AbsoluteURLField()
    latest = S.SerializerMethodField()
    unread = S.SerializerMethodField()

    class Meta:
        fields = (
            "type",
            "id",
            "unread",
            "url",
            "latest",
            "created",
        )
        msg_serializer_class = None

    @property
    def msg_serializer_class(self):
        return self.Meta.msg_serializer_class

    def get_latest(self, chat):
        """
        Gets latest message from a chat
        """
        try:
            msg = self.get_message(chat)
            assert msg
            return self.msg_serializer_class(
                msg,
                context=self.context,
                exclude=(
                    "files",
                    "url",
                    "edited",
                ),
            ).data
        except Exception:
            return None

    def get_message(self, chat):
        return chat.messages.first()

    def get_unread(self, chat):
        try:
            return chat.unread or 0
        except Exception:
            return 0


class GroupMixin(metaclass=S.SerializerMetaclass):
    """Mixin for common group serializer fields, methods and etc."""

    members = S.SerializerMethodField()
    online = S.SerializerMethodField()

    def get_members(self, group):
        return getattr(group, "members_count", 0)

    def get_online(self, group):
        return getattr(group, "online_count", 0)


class FileMixin(metaclass=S.SerializerMetaclass):
    """Mixin for common file serializer fields, methods, etc."""

    url = S.FileField(source="file", read_only=True)

    class Meta:
        fields = ("id", "file", "url", "file_type", "metadata")
        read_only_fields = ("file_type", "metadata")
        extra_kwargs = {"file": {"write_only": True}}


class MessageMixin(DynamicFieldsMixin, metaclass=S.SerializerMetaclass):
    """Mixin for common message serializer fields, methods, etc."""

    url = AbsoluteURLField()
    owner_name = S.SerializerMethodField()
    files = S.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "url",
            "owner",
            "owner_name",
            "content",
            "files",
            "seen",
            "created",
            "edited",
            "is_edited",
        )
        read_only_fields = ("id", "owner", "files")

    def get_owner_name(self, msg):
        try:
            return msg.owner_name
        except Exception as e:
            return msg.owner.get_full_name()

    def get_files(self, msg):
        try:
            ser_cls = self.get_file_serializer()
            # try to get cached files
            files = getattr(msg, "_cached_files", None)
            if files is None:
                files = list(msg.files.all())
            assert files
            return ser_cls(
                instance=files, many=True, read_only=True, context=self.context
            ).data
        except Exception as e:
            print(e)

    def create(self, validated_data: dict):
        """Creates message with its files if passed"""

        try:
            files = self.initial_data.getlist("files", [])
        except Exception as e:
            files = None
        msg = super().create(validated_data)
        if files:
            try:
                [data, model] = self.validate_files(files)
                files = model.objects.bulk_create(
                    [model(**attrs, message=msg).before_create() for attrs in data]
                )
                msg._cached_files = files
            except Exception as e:
                print(e)
        return msg

    def validate_files(self, files: list):
        """Validates files using file serializer"""
        ser_cls = self.get_file_serializer()
        serializer = ser_cls(data=[{"file": file} for file in files], many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data, ser_cls.Meta.model

    def get_file_serializer(self):
        """Hook to return file serializer"""
        return
