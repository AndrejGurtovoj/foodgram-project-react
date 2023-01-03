from rest_framework import permissions


class IsAuthOwnerOrReadOnly(permissions.IsAuthenticated):
    """
    Полный доступ для авторизованного создателя рецепта,
    Для остальных только чтение.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
