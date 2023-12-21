from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from rest_framework import serializers as S
from rest_framework import exceptions as EX

from .utils import AbsoluteURLField


class ReprSerializerMixin:
    def to_representation(self, args, **kwargs):
        self.fields.update(self.get_repr_fields())
        return super().to_representation(args, **kwargs)

    def get_repr_fields(self):
        return {}


class ModelSerializerMixin:
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

    def save_instance(self, instance):
        instance.save()
        return instance


class FileMixin(metaclass=S.SerializerMetaclass):
    url = S.FileField(source='file', read_only=True)

    class Meta:
        fields = ('id', 'file', 'url', 'file_type',
                  'metadata', 'message')
        read_only_fields = ('file_type', 'metadata')
        extra_kwargs = {'message': {'write_only': True},
                        'file': {'write_only': True}}


class MessageMixin(metaclass=S.SerializerMetaclass):
    url = AbsoluteURLField()

    class Meta:
        fields = ('id', 'url', 'owner',
                  'content', 'files', 'seen',
                  'created', 'edited', 'is_edited')
        read_only_fields = ('id', 'owner', 'files')

    def create(self, validated_data: dict):
        try:
            files = self.initial_data.getlist('files', [])
        except:
            files = None
        msg = super().create(validated_data)
        if files:
            try:
                self.create_files(files, msg)
            except Exception as e:
                print(e)
        return msg

    def create_files(self, files: list, msg):
        serializer = self.get_file_serializer()(
            data=[{'file': file, 'message': msg.pk}
                  for file in files], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def get_file_serializer(self):
        return
