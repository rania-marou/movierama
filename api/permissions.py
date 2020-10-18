from rest_framework import permissions


class AuthenticatedCreate(permissions.BasePermission):
    """
    Custom permission to allow only logged in users to access POST method.
    """

    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_anonymous:
            return False
        return True
