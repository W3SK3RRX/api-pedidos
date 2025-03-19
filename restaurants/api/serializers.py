from rest_framework import serializers
from restaurants.models import Restaurant, MenuItem, Address, Category


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


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorias"""
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer para itens do menu"""
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "restaurant", "category", "category_id", "name", "description", "price", "available"]

    def validate(self, data):
        """Garante que o usuário é o dono do restaurante ao criar um item"""
        request = self.context["request"]
        restaurant = data["restaurant"]

        if restaurant.owner != request.user and not request.user.is_staff:
            raise serializers.ValidationError("Você não tem permissão para modificar este menu.")
        
        return data