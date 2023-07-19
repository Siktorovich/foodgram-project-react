from rest_framework import permissions


class CurrentUserOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_superuser
            or request.user.role == 'admin'
        )
    

class SuperUserOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )
