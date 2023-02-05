from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.admin or request.user.is_staff
        )


class IsAdminModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.moderator
            or request.user.admin
        )


class IsadminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.admin
        return False