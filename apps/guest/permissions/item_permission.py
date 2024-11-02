from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from apps.core.models import Restaurant, Item


class ItemPermission(BasePermission):

    def has_permission(self, request: Request, view):
        occupation_id = view.kwargs['occupation_id']
        item_id = request.data.get('item')
        if item_id:
            restaurant = Restaurant.objects.get_by_occupation_id(occupation_id=occupation_id)
            item = Item.objects.get(id=item_id)
            if item.restaurant_id != restaurant.id:
                raise PermissionDenied('the selected item is assigned to an other restaurant')
        return True
