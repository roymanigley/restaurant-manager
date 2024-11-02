from rest_framework import permissions

from apps.core.models import Item, ItemImage


class ItemImagePermission(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        item_id = view.kwargs.get('pk')
        item = Item.objects.get(id=item_id)
        return has_permission and request.user.restaurant_id == item.restaurant_id

    def has_object_permission(self, request, view, obj: ItemImage):
        return request.user.restaurant.id == obj.item.restaurant_id
