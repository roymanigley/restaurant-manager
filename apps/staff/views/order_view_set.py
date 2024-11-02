from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Order
from apps.staff.filters import OrderFilter
from apps.staff.permissions import OrderPermission
from apps.staff.serializers import OrderSerializer


@extend_schema(tags=['Staff - Orders'])
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, OrderPermission]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='date_range_after',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Start date for filtering (YYYY-MM-DD)',
                required=False
            ),
            OpenApiParameter(
                name='date_range_before',
                type=str,
                location=OpenApiParameter.QUERY,
                description='End date for filtering (YYYY-MM-DD)',
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)