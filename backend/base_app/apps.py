from django.apps import AppConfig


def db_connected():
    from .models import User
    from django.db.models import Q
    try:
        User.objects.filter(~Q(status=0)).update(status=0)
    except:
        pass


class BaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_app'

    def ready(self) -> None:
        db_connected()
