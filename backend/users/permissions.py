from rest_framework import permissions


class IsAuthOrCreateList(permissions.IsAuthenticated):
    """Доступ на чтение и создание."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.method == 'POST')

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated
