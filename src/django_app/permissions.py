from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated.")
        return True


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_superuser and request.user.is_staff:
            raise PermissionDenied(
                "You do not have the necessary permissions to access this resource. Admin privileges are required."
            )
        return True
