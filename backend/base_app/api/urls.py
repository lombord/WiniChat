"""App API urls"""

from django.urls import include, path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views as V
from . import viewsets as VS

# ViewSet routes
router = SimpleRouter()
router.register("messages", VS.MessageViewSet, basename="message")
router.register("groups", VS.GroupViewSet, basename="group")
router.register("public-groups", VS.PGroupViewSet, basename="public-group")

# Token related routes
token_urls = [
    path("", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]


# Private Chat related routes
chat_urls = [
    path("", V.ChatsAPIView.as_view(), name="chats"),
    path(
        "<int:pk>/",
        include(
            [
                path("", V.ChatAPIView.as_view(), name="chat"),
                path(
                    "messages/", V.ChatMessagesAPIView.as_view(), name="chat_messages"
                ),
                path("files/", V.ChatFilesView.as_view(), name="chat_files"),
            ]
        ),
    ),
]


urlpatterns = [
    # token related urls
    path("token/", include(token_urls)),
    # User related urls
    path("session/", V.SessionAPIView.as_view(), name="session"),
    path("check-username/", V.check_username, name="check-username"),
    path("check-user-email/", V.check_user_mail, name="check-user-email"),
    path("register/", V.UserRegisterAPIView.as_view(), name="register"),
    path("search/", V.SearchAPIView.as_view(), name="search"),
    path(
        "users/",
        include(
            [
                path("", V.UsersAPIView.as_view(), name="users"),
                path("<int:pk>/", V.UsersAPIView.as_view(), name="user"),
            ]
        ),
    ),
    # chats related urls
    path("chats/", include(chat_urls)),
    path("all-chats/", V.AllChatsAPIView.as_view(), name="all-chats"),
    *router.urls,
]
