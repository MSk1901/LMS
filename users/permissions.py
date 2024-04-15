from rest_framework.permissions import BasePermission


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()
