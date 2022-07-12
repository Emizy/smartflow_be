from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, UserViewSet

router = DefaultRouter()
router.register(r'', RegisterViewSet, basename='api-register')
router.register(r'user', UserViewSet, basename='api-user')
