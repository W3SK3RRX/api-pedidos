from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import User
from users.api.serializers import UserSerializer, RegisterSerializer
from users.api.permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Permite que qualquer um se registre
    serializer_class = RegisterSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Apenas usuários logados podem acessar
