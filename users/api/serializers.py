from rest_framework import serializers
from users.models import User, AccessLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'password']

    def validate(self, data):
        """Garante que donos de restaurantes informem um e-mail"""
        if data.get("role") == "funcionario" and not data.get("email"):
            raise serializers.ValidationError("Donos de restaurantes precisam fornecer um e-mail válido para ativar o 2FA.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone'),
            role=validated_data.get('role', 'cliente'),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'is_2fa_enabled']


class AccessLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = AccessLog
        fields = ["id", "user", "ip_address", "endpoint", "method", "status_code", "timestamp"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adiciona o role do usuário ao token JWT"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role  # Adiciona o role ao payload do token
        return data