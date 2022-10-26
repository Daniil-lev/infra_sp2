from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    message = 'Изменение разрешены толлько администратору'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser))


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and obj == request.user)


class ReadOnly(permissions.BasePermission):
    message = 'Доступ только на чтение'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorAdminModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or obj.author == request.user
                     )
                )
