from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.core.models import Occupation


class ActiveOccupationPermission(BasePermission):

    def has_permission(self, request, view):
        occupation_id = view.kwargs['occupation_id']
        if Occupation.objects.is_occupation_active(occupation_id=occupation_id):
            return True
        raise PermissionDenied('the occupation is already closed')
