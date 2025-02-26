from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurants.api.viewsets import RestaurantViewSet, MenuItemViewSet
from restaurants.views import ApproveRestaurantView, RestaurantBySlugView

router = DefaultRouter()
router.register(r'', RestaurantViewSet)
router.register(r'menu', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/approve/', ApproveRestaurantView.as_view(), name='approve-restaurant'),
    path('slug/<str:slug>/', RestaurantBySlugView.as_view(), name='restaurant-by-slug'),
]
