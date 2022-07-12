from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from apps.core import routes as core_router
from apps.finance import routes as finance_router
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.core.views import account_logout

schema_view = get_schema_view(
    openapi.Info(
        title="SMARTFLOW INTERVIEW TEST",
        default_version="v1",
        description="Endpoints showing interactable part of the system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(SessionAuthentication, JWTAuthentication),
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/logout/', account_logout),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/", include(core_router.router.urls)),
    path("api/v1/finance/", include(finance_router.router.urls)),
    path("",
         schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui",
         ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
