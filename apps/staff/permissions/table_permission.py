from rest_framework import permissions

from apps.core.models import Table


class TablePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if request.data.get('restaurant'):
            return has_permission and int(request.data['restaurant']) == request.user.restaurant_id
        else:
            return has_permission

    def has_object_permission(self, request, view, obj: Table):
        return request.user.restaurant_id == obj.restaurant_id
