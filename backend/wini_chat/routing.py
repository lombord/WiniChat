from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from base_app.api.routing import websocket_urlpatterns
from .middleware import JWTAuthMiddlewareStack

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

routes = URLRouter([path("ws/", URLRouter(websocket_urlpatterns))])


application = ProtocolTypeRouter(
    {
        # http requests handler
        "http": django_asgi_app,
        # ws requests handler
        "websocket": AllowedHostsOriginValidator(JWTAuthMiddlewareStack(routes)),
    }
)
