from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """
    Позволяет доступ только администраторам.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
