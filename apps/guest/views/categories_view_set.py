from builtins import str

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Item
from apps.guest.permissions import ActiveOccupationPermission


@extend_schema(tags=['Guest - Categories'])
class CategoriesViewSet(GenericViewSet):
    permission_classes = [ActiveOccupationPermission]

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={
            200: {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    )
    @action(url_path='(?P<occupation_id>[^/.]+)', detail=False, permission_classes=[ActiveOccupationPermission],
            serializer_class=serializers.ListSerializer)
    def get_categories(self, request: Request, occupation_id: str) -> Response:
        categories = Item.Category.choices
        return Response(
            data={
                'count': len(categories),
                'previous': None,
                'next': None,
                'results': categories
            }
        )
