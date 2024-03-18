"""Utility classes and function for serializers"""

import os

from django.http import HttpRequest

from rest_framework import serializers as S


class AbsoluteURLField(S.Field):
    """Absolute url field for model instances"""

    def __init__(self, *, url_name=None, **kwargs):
        self.url_name = url_name
        kwargs["read_only"] = True
        kwargs.setdefault("source", "*")
        super().__init__(**kwargs)

    def to_representation(self, value):
        args = [self.url_name] if self.url_name else []
        try:
            abs_url = value.get_absolute_url(*args)
            request: HttpRequest = self.context.get("request")
            return request.build_absolute_uri(abs_url)
        except Exception as e:
            print(e)
            return


def clean_old_photo(file):
    """Cleans old file if it exists and is not default"""
    name = os.path.basename(file.name)
    if name.startswith("default"):
        return
    try:
        os.remove(file.path)
    except Exception:
        pass
