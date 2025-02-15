from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/api/staff/restaurant-users/me/')
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logout(request)

        return Response({}, status=status.HTTP_200_OK)

class PermissionSerializer(serializers.ModelSerializer):

    app = serializers.CharField(source="content_type.app_label", read_only=True)
    class Meta:
        model = Permission
        fields = "__all__"

class PermissionsViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.filter(
        content_type__app_label='core'
    )
    serializer_class = PermissionSerializer
