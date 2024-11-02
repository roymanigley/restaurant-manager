from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Occupation
from apps.staff.permissions import OccupationPermission
from apps.staff.serializers import OccupationSerializer


@extend_schema(tags=['Staff - Occupations'])
class OccupationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, OccupationPermission]
    serializer_class = OccupationSerializer

    def get_queryset(self):
        return Occupation.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )
