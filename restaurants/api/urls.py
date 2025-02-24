from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.api.viewsets import RestaurantViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'', RestaurantViewSet)
router.register(r'menu', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
