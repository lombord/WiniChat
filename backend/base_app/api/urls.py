from django.urls import include, path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views as V
from . import viewsets as VS

router = SimpleRouter()
router.register('messages', VS.MessageViewSet,
                basename='messages')
router.register('groups', VS.GroupViewSet,
                basename='group')

token_urls = [
    path('', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    # urls related with token
    path('token/', include(token_urls)),
    path('session/', V.SessionAPIView.as_view(), name='session'),
    path('register/', V.UserRegisterAPIView.as_view(), name='register'),
    path('people/', V.PeopleAPIView.as_view(), name='people'),
    # urls related with DM chats
    path('chats/', include([
        path('', V.ChatsAPIView.as_view(), name='chats'),
        path('<int:pk>/', include([
            path('', V.ChatAPIView.as_view(), name='chat'),
            path('files/', V.ChatFilesView.as_view(), name='chat_files'),
        ])),
    ])),
    path('all-chats/', V.AllChatsAPIView.as_view(), name='all-chats'),
    * router.urls,
]
