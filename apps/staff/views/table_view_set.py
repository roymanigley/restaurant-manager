import datetime

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Table, Occupation
from apps.staff.permissions import TablePermission
from apps.staff.serializers import TableSerializer
from apps.staff.serializers.table_serializer import TableAvailabilitySerializer


@extend_schema(tags=['Staff - Table'])
class TableViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, TablePermission]
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )

    @extend_schema(
        tags=['Staff - Table'],
        responses={200: TableAvailabilitySerializer(many=True)},
        parameters=[
            OpenApiParameter('date_time', datetime.datetime, required=True,
            examples=[OpenApiExample('', '2025-02-15T10:00')])
        ],
    )
    @action(url_path='available', detail=False, methods=['get'], serializer_class=TableAvailabilitySerializer)
    def get_available_tables(self, request):
        serializer = TableAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date_time = serializer.validated_data['date_time']
        queryset = self.paginate_queryset(self.get_queryset().get_available_tables(date_time=date_time))
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)