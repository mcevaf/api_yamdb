from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """
    Пользователь является superuser
    или имеет роль администратора.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminModeratorPermission(permissions.BasePermission):
    """
    Пользователь является superuser
    или имеет роль администратора или модератора.
    Просмотр доступен всем пользователям.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsadminUserOrReadOnly(permissions.BasePermission):
    """
    Пользователь является superuser
    или имеет роль администратора.
    Просмотр доступен всем пользователями.
    """
    def has_permission(self, request, view):

        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )
