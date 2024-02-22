"""ViewSet utility tools"""

from functools import wraps
from contextlib import contextmanager

from django.utils.translation import gettext as _
from rest_framework.exceptions import PermissionDenied, APIException


def nested_action(wrap_method=None, *, action=None, detail=False):
    """Nested action decorator for nested viewsets"""

    def decorator(method):

        @wraps(method)
        def wrapper(self, request, *args, **kwargs):
            self._action = action or method.__name__
            setattr(self, self.root_obj_name, self.get_object())
            self._curr_action = self._action
            self._nested_detail = detail
            if detail:
                self.set_nested_lookup()
            return method(self, request, *args, **kwargs)

        return wrapper

    if wrap_method is not None and callable(wrap_method):
        return decorator(wrap_method)
    return decorator


@contextmanager
def exc_manager(
    def_msg: str = "Something went wrong",
    main_exc: type = PermissionDenied,
    def_exc: type = APIException,
):
    """Api Exception manager to handle validations"""
    try:
        yield
    except AssertionError as msg:
        raise main_exc(_(str(msg)))
    except Exception as e:
        print(e)
        raise def_exc(detail=_(def_msg), code=406)
