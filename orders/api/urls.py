from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.api.viewsets import OrderViewSet, OrderItemViewSet
from orders.views import RestaurantStatsView, UpdateOrderStatusView, OrderAuditLogView

router = DefaultRouter()
router.register(r'', OrderViewSet)
router.register(r'items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('stats/', RestaurantStatsView.as_view(), name='restaurant-stats'),
    path("audit/", OrderAuditLogView.as_view(), name="order-audit-log"),
]
