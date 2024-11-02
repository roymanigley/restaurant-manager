from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Table
from apps.staff.permissions import TablePermission
from apps.staff.serializers import TableSerializer


@extend_schema(tags=['Staff - Table'])
class TableViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, TablePermission]
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )
