from rest_framework import permissions

from apps.core.models import Item


class ItemPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if request.data.get('restaurant'):
            has_permission &= int(request.data['restaurant']) == request.user.restaurant_id
        return has_permission

    def has_object_permission(self, request, view, obj: Item):
        return request.user.restaurant.id == obj.restaurant.id
