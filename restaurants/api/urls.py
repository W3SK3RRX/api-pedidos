from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.api.viewsets import RestaurantViewSet, MenuItemViewSet, CategoryItemViewSet, CategoryRestaurantViewSet
from restaurants.views import (
    ApproveRestaurantView,
    RestaurantBySlugView,
    PendingRestaurantNotifications,
    MyRestaurantsView,
    CreateRestaurantView,
    OperatingHoursCreateView
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename="restaurants")
router.register(r"menu-items", MenuItemViewSet, basename="menu-items")
router.register(r"restaurant-categories", CategoryRestaurantViewSet, basename="restaurant-categories")
router.register(r"menu-categories", CategoryItemViewSet, basename="menu-categories")

urlpatterns = [
    path('create/', CreateRestaurantView.as_view(), name="create-restaurant"),
    path('restaurants/<int:restaurant_id>/operating-hours/', OperatingHoursCreateView.as_view(), name="manage-operating-hours"),
    path('', include(router.urls)),

    path("admin/pending-notifications/", PendingRestaurantNotifications.as_view(), name="pending-notifications"),
    path('<int:pk>/approve/', ApproveRestaurantView.as_view(), name='approve-restaurant'),
    path('slug/<str:slug>/', RestaurantBySlugView.as_view(), name='restaurant-by-slug'),
    path("my-restaurants/", MyRestaurantsView.as_view(), name="my-restaurants"),
]

