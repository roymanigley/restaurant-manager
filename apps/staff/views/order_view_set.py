from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Order
from apps.staff.permissions import OrderPermission
from apps.staff.serializers import OrderSerializer


class OrderQuerySerializer(serializers.Serializer):
    start = serializers.DateField(required=False, write_only=True)
    end = serializers.DateField(required=False, write_only=True)

@extend_schema(tags=['Staff - Orders'])
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, OrderPermission]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='start',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Start date for filtering (YYYY-MM-DD)',
                required=False
            ),
            OpenApiParameter(
                name='end',
                type=str,
                location=OpenApiParameter.QUERY,
                description='End date for filtering (YYYY-MM-DD)',
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        serializer = OrderQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start = serializer.validated_data.get('start')
        end = serializer.validated_data.get('end')
        queryset = self.get_queryset()
        if start and end:
            queryset = queryset.filter(
                occupation__start__gte=start,
                occupation__start__lte=end,
            )
        paged_queryset = self.paginate_queryset(queryset)
        data = self.get_serializer(instance=paged_queryset, many=True).data
        return self.get_paginated_response(data)