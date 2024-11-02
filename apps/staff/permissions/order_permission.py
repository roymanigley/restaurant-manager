from rest_framework import permissions

from apps.core.models import Order, Occupation, Item


class OrderPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if request.data.get('item'):
            has_permission_for_item = Item.objects.get_by_restaurant_id(
                restaurant_id=request.user.restaurant.id
            ).filter(
                id=request.data['item']
            ).exists()
            has_permission &= has_permission_for_item
        if request.data.get('occupation'):
            has_permission_for_occupation = Occupation.objects.get_by_restaurant_id(
                restaurant_id=request.user.restaurant.id
            ).filter(
                id=request.data['occupation']
            ).exists()
            has_permission &= has_permission_for_occupation
        return has_permission

    def has_object_permission(self, request, view, obj: Order):
        return (
                request.user.restaurant.id == obj.item.restaurant.id
                and
                request.user.restaurant.id == obj.occupation.table.restaurant.id
        )
