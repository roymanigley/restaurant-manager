from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Item
from apps.guest.permissions import ActiveOccupationPermission
from apps.guest.serializers import ItemSerializer


@extend_schema(tags=['Guest - Items'])
class ItemViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [ActiveOccupationPermission]

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary='guests_items_available_retrieve_by_category')
    @action(url_path='available/(?P<occupation_id>[^/.]+)/(?P<category>[^/.]+)', detail=False,
            serializer_class=ItemSerializer, permission_classes=[ActiveOccupationPermission]
            )
    def get_items_by_category(self, request: Request, occupation_id: str, category: str) -> Response:
        items = Item.objects.get_active().get_by_occupation_id(
            occupation_id=occupation_id
        ).get_by_category(
            category=category
        )
        items_paged = self.paginate_queryset(items)
        serializer = ItemSerializer(items_paged, many=True)
        return self.get_paginated_response(serializer.data)

    @action(url_path='available/(?P<occupation_id>[^/.]+)', detail=False, serializer_class=ItemSerializer,
            permission_classes=[ActiveOccupationPermission]
            )
    def get_items(self, request: Request, occupation_id: str) -> Response:
        items = Item.objects.get_active().get_by_occupation_id(occupation_id=occupation_id)
        items_paged = self.paginate_queryset(items)
        serializer = ItemSerializer(items_paged, many=True)
        return self.get_paginated_response(serializer.data)
