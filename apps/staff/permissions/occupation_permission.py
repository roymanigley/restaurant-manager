from rest_framework import permissions

from apps.core.models import Occupation, Table, RestaurantUser


class OccupationPermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if request.data.get('table'):
            has_table_permission = Table.objects.get_by_restaurant_id(
                restaurant_id=request.user.restaurant_id
            ).filter(
                id=int(request.data['table'])
            ).exists()
            has_permission &= has_table_permission
        if request.data.get('waiter'):
            has_waiter_permission = RestaurantUser.objects.get_by_restaurant_id(
                restaurant_id=request.user.restaurant_id
            ).filter(
                id=int(request.data['waiter'])
            ).exists()
            has_permission &= has_waiter_permission
        return has_permission

    def has_object_permission(self, request, view, obj: Occupation):
        return (
                request.user.restaurant.id == obj.table.restaurant.id
                and
                request.user.restaurant.id == obj.waiter.restaurant.id
        )
