from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.viewsets import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet)
router.register(r'items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
