"""App WS routes"""

from django.urls import path

from . import consumers as C

websocket_urlpatterns = [
    path("session/", C.SessionConsumer.as_asgi()),
]
