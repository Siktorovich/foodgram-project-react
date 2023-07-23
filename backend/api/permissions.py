from rest_framework import permissions


class OwnerSuperUserOrReadOnly(permissions.BasePermission):
    """Permission class that allows to endpoint only
    owner or superuser users.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.owner == request.user
            or request.user.is_superuser
            or request.user.check_is_admin
        )
