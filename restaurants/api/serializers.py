from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'owner', 'address', 'phone', 'status']
        read_only_fields = ['status']  # O status não pode ser definido no POST


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'available']
