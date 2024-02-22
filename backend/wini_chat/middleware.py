from urllib.parse import parse_qs

from django.db import close_old_connections
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import UntypedToken
from jwt import decode as jwt_decode

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack


@database_sync_to_async
def get_user(token_data):
    """
    Try to get user based on token_data.
    If any error is encountered return AnonymousUser
    """
    try:
        return get_user_model().objects.get(pk=token_data["user_id"])
    except Exception as e:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate users with JWT
    """

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        # get query byte string and decode it to normal str
        qs = scope["query_string"].decode()
        # parse query string to dictionary
        qr_dict = parse_qs(qs)
        # try to get and validate the token
        try:
            # get the token from parsed dictionary
            token = qr_dict["token"][0]
            # Validate the token type
            UntypedToken(token)
        except Exception as e:
            # stop JWT authentication if any error occurred
            print(repr(e))
            return
        # decode the token using jwt_decode function
        token_data = jwt_decode(token, settings.SECRET_KEY, ["HS256"])
        # get user using token_data which contains user id and token info
        scope["user"] = await get_user(token_data)
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    """
    Stack to wrap 'AuthMiddlewareStack' stack with
    'JWTAuthMiddleware' middleware to support both authentications
    """
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
