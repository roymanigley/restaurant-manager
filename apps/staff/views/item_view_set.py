from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Item, ItemImage
from apps.staff.permissions import ItemPermission, ItemImagePermission
from apps.staff.serializers import ItemSerializer, ItemImageSerializer


@extend_schema(tags=['Staff - Items'])
class ItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ItemPermission]
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )

    @action(
        url_path='image', detail=True, methods=['POST'], serializer_class=ItemImageSerializer,
        permission_classes=[IsAuthenticated, ItemImagePermission]
    )
    def set_image(self, request: Request, pk: int) -> Response:
        image_instance = ItemImage.objects.get_by_item_id(item_id=pk)
        if image_instance is None:
            image_instance = ItemImage.objects.create(item_id=pk)
        serializer = ItemImageSerializer(
            instance=image_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
