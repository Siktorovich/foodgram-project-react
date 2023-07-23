from rest_framework import permissions


class CurrentUserOrAdmin(permissions.BasePermission):
    """Permission clas that allows current user or admin."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_superuser
            or request.user.check_is_admin
        )


class SuperUserOrAdmin(permissions.BasePermission):
    """Permission clas that allows super user or admin."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.check_is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.check_is_admin
        )
