from rest_framework import permissions

from apps.core.models import Restaurant


class RestaurantPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        return has_permission and request.method != 'POST'

    def has_object_permission(self, request, view, obj: Restaurant):
        return request.user.restaurant.id == obj.id
