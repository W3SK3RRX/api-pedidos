from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.api.viewsets import RestaurantViewSet, MenuItemViewSet
from restaurants.views import (
    ApproveRestaurantView,
    RestaurantBySlugView,
    PendingRestaurantNotifications,
    MyRestaurantsView,
    CreateRestaurantView
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename="restaurants")  # 🔹 Restaurando a rota principal
router.register(r'menu', MenuItemViewSet, basename='menu')

urlpatterns = [
    path('create/', CreateRestaurantView.as_view(), name="create-restaurant"),
    path('', include(router.urls)),  # 🔹 Registrar todas as rotas do `ViewSet`
    
    path("admin/pending-notifications/", PendingRestaurantNotifications.as_view(), name="pending-notifications"),
    path('<int:pk>/approve/', ApproveRestaurantView.as_view(), name='approve-restaurant'),
    path('slug/<str:slug>/', RestaurantBySlugView.as_view(), name='restaurant-by-slug'),
    path("my-restaurants/", MyRestaurantsView.as_view(), name="my-restaurants"),
]
