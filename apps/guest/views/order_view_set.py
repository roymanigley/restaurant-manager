from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Order
from apps.guest.permissions import ActiveOccupationPermission
from apps.guest.serializers import OrderSerializer


@extend_schema(tags=['Guest - Orders'])
class OrderViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [ActiveOccupationPermission]
    queryset = Order.objects.none()

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={status.HTTP_200_OK: OrderSerializer(many=True)},
    )
    @action(
        url_path='(?P<occupation_id>[^/.]+)', detail=False, methods=['GET'],
        serializer_class=OrderSerializer, permission_classes=[ActiveOccupationPermission]
    )
    def get_orders_by_occupation(self, request: Request, occupation_id: str) -> Response:
        orders = Order.objects.get_by_occupation_id(occupation_id=occupation_id)
        orders_paged = self.paginate_queryset(orders)
        serializer = OrderSerializer(orders_paged, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        url_path='(?P<occupation_id>[^/.]+)/add', detail=False, methods=['POST'],
        serializer_class=OrderSerializer, permission_classes=[ActiveOccupationPermission]
    )
    def create_order(self, request: Request, occupation_id: str) -> Response:
        serializer = OrderSerializer(data=request.data, context={'occupation_id': occupation_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )
