from drf_spectacular.utils import extend_schema
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Occupation
from apps.staff.serializers import OccupationSerializer


@extend_schema(tags=['Guest - Occupations'])
class OccupationViewSet(RetrieveModelMixin, GenericViewSet):
    permission_classes = []
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer