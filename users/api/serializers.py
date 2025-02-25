from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'password']

    def create(self, validated_data):
        role = validated_data.pop('role', 'cliente')  # Retira o campo 'role' antes de criar o usuário
        user = User.objects.create_user(**validated_data)  # Cria usuário sem 'role'
        user.role = role  # Atribui a role separadamente
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']
