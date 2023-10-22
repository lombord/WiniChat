from django.http import HttpRequest
from rest_framework import permissions


class isNotAuthenticated(permissions.BasePermission):
    """
    Checks if user is not authenticated
    """

    def has_permission(self, request: HttpRequest, view):
        return not request.user.is_authenticated
