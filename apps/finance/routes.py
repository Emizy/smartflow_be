from rest_framework.routers import DefaultRouter
from apps.finance.views import SalesViewSet

router = DefaultRouter()
router.register(r'sales', SalesViewSet, basename='api-blog')
