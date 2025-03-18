from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "neighborhood", "street", "number", "cep"]

class RestaurantSerializer(serializers.ModelSerializer):
    address = AddressSerializer()  # 🔹 Serializador aninhado

    class Meta:
        model = Restaurant
        fields = [
            "id", "name", "description", "category", "owner",
            "address", "phone", "image", "status", "slug", "created_at"
        ]
        read_only_fields = ["owner", "status", "slug", "created_at"]  # 🔹 Evita alteração desses campos

    def update(self, instance, validated_data):
        """Atualiza restaurante e endereço"""
        address_data = validated_data.pop("address", None)  # 🔹 Extraindo os dados do endereço
        
        # Atualizar os dados do restaurante
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Se o endereço foi enviado, atualizar separadamente
        if address_data:
            Address.objects.filter(id=instance.address.id).update(**address_data)

        instance.save()
        return instance


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'available']
