from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False


class NotPatientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type != 1:
            return True
        return False


class YaoshiPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated and request.user.type == 3) or request.user.is_superuser:
            return True
        return False

class SuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
