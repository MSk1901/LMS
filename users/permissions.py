from rest_framework.permissions import BasePermission


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class OwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
