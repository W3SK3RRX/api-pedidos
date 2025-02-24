from rest_framework.viewsets import ModelViewSet
from restaurants.models import Restaurant, MenuItem
from restaurants.api.serializers import RestaurantSerializer, MenuItemSerializer

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
