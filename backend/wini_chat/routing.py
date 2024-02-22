from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from .middleware import JWTAuthMiddlewareStack
from base_app.api.routing import websocket_urlpatterns

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

routes = URLRouter([path("ws/", URLRouter(websocket_urlpatterns))])


application = ProtocolTypeRouter(
    {
        # http requests handler
        "http": django_asgi_app,
        # ws requests handler
        "websocket": AllowedHostsOriginValidator(JWTAuthMiddlewareStack(routes)),
    }
)
