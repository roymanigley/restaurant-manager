from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.models import RestaurantUser
from apps.staff.permissions import RestaurantUserPermission
from apps.staff.serializers import RestaurantUserSerializer, RestaurantUserDetailSerializer, PasswordSerializer


@extend_schema(tags=['Staff - RestaurantUsers'])
class RestaurantUserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, RestaurantUserPermission]
    serializer_class = RestaurantUserSerializer

    def get_queryset(self):
        return RestaurantUser.objects.get_by_restaurant_id(
            restaurant_id=self.request.user.restaurant.id
        )

    @action(
        url_path='me', detail=False, methods=['GET'], serializer_class=RestaurantUserDetailSerializer,
        permission_classes=[IsAuthenticated]
    )
    def get_current_user(self, request: Request) -> Response:
        serializer = RestaurantUserDetailSerializer(instance=request.user)
        return Response(data=serializer.data)

    @action(
        url_path='me/password', detail=False, methods=['PUT'], serializer_class=PasswordSerializer,
        permission_classes=[IsAuthenticated]
    )
    def set_current_users_password(self, request: Request) -> Response:
        serializer = PasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.get_validated_password())
        return Response(status=status.HTTP_204_NO_CONTENT)

