from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "neighborhood", "street", "number", "cep"]

class RestaurantSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Restaurant
        fields = [
            "id", "name", "description", "category", "owner",
            "address", "phone", "image", "status", "slug"
        ]

    def create(self, validated_data):
        """Criar restaurante com endereço"""
        address_data = validated_data.pop('address', None)
        
        if not address_data:
            raise serializers.ValidationError({"address": "O campo endereço é obrigatório."})

        address = Address.objects.create(**address_data)
        restaurant = Restaurant.objects.create(address=address, **validated_data)
        return restaurant



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'available']
