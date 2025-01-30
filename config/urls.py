from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.shared.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/guests/', include('apps.guest.urls')),
    path('api/staff/', include('apps.staff.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI route
    # path(
    #     'api/docs/',
    #     SpectacularSwaggerView.as_view(url_name='schema'),
    #     name='swagger-ui'
    # ),
    # ReDoc route
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
