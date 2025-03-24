from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Address, CategoryRestaurant, CategoryMenuItem, OperatingHours


class AddressSerializer(serializers.ModelSerializer):
    """Serializer para endereços"""

    class Meta:
        model = Address
        fields = ["city", "neighborhood", "street", "number", "cep"]

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorias de restaurantes"""

    class Meta:
        model = CategoryRestaurant
        fields = ["id", "name"]

class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer para restaurantes"""
    address = AddressSerializer()  
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=CategoryRestaurant.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Restaurant
        fields = [
            "id", "name", "description", "category_id", "phone", "address", "image", 
            "status", "slug", "created_at"
        ]
        read_only_fields = ["status", "slug", "created_at"]

    def create(self, validated_data):
        """Criação do restaurante sem horários de funcionamento"""
        address_data = validated_data.pop("address")  
        address = Address.objects.create(**address_data)  
        restaurant = Restaurant.objects.create(address=address, **validated_data)  
        return restaurant

    def update(self, instance, validated_data):
        """Atualização do restaurante e do endereço"""
        address_data = validated_data.pop("address", None)  # Remove os dados do endereço
        if address_data:
            address_instance = instance.address
            for attr, value in address_data.items():
                setattr(address_instance, attr, value)
            address_instance.save()  # Salva as mudanças no endereço

        return super().update(instance, validated_data)  # Atualiza os outros campos



class OperatingHoursSerializer(serializers.ModelSerializer):
    """Serializer para cadastrar horários de funcionamento de um restaurante"""

    class Meta:
        model = OperatingHours
        fields = ["id", "restaurant", "day_of_week", "open_time", "close_time"]

    def validate(self, data):
        """Validação para garantir que o usuário é dono do restaurante"""
        request = self.context.get("request")  # 🔹 Use `.get()` para evitar erros

        if request and request.user != data["restaurant"].owner and not request.user.is_staff:
            raise serializers.ValidationError("Você não tem permissão para modificar os horários deste restaurante.")
        
        return data



class CategoryMenuItemSerializer(serializers.ModelSerializer):
    """Serializer para categorias dos itens do menu"""

    class Meta:
        model = CategoryMenuItem
        fields = ["id", "name"]


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer para itens do menu"""
    category_id = serializers.PrimaryKeyRelatedField(queryset=CategoryMenuItem.objects.all(), source="category", write_only=True)
    category = CategoryMenuItemSerializer(read_only=True)  # 🔹 Serializador aninhado
    image = serializers.ImageField(required=False, allow_null=True)  # 🔹 Adicionando suporte para imagens

    class Meta:
        model = MenuItem
        fields = ["id", "restaurant", "category", "category_id", "name", "description", "price", "available", "image"]

    def validate(self, data):
        """Garante que o usuário é o dono do restaurante ao criar um item"""
        request = self.context["request"]
        restaurant = data["restaurant"]

        if restaurant.owner != request.user and not request.user.is_staff:
            raise serializers.ValidationError("Você não tem permissão para modificar este menu.")
        
        return data
