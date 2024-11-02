from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import Restaurant
from apps.staff.permissions import RestaurantPermission
from apps.staff.serializers import RestaurantSerializer


@extend_schema(tags=['Staff - Restaurant'])
class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, RestaurantPermission]

    def get_queryset(self):
        return Restaurant.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )
