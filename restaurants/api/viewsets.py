from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from restaurants.models import Restaurant
from restaurants.api.serializers import RestaurantSerializer
from restaurants.api.permissions import IsOwnerOrAdmin
from restaurants.models import MenuItem
from restaurants.api.serializers import MenuItemSerializer
from rest_framework.response import Response
from rest_framework import status

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]  # 🔹 Verificar autenticação

    def perform_create(self, serializer):
        """Testar se o usuário autenticado está sendo reconhecido"""
        if not self.request.user or not self.request.user.is_authenticated:
            return Response({"error": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        print(f"Usuário autenticado: {self.request.user}")  # 🔹 Exibir no console
        serializer.save(owner=self.request.user, status='pendente')



class MenuItemViewSet(ModelViewSet):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Dono do restaurante vê apenas seus itens. Clientes só veem menus de restaurantes ativos."""
        user = self.request.user
        
        if user.role == 'admin':
            return MenuItem.objects.all()
        
        if user.role == 'funcionario':
            return MenuItem.objects.filter(restaurant__owner=user)

        if user.role == 'cliente':
            return MenuItem.objects.filter(restaurant__status='ativo')

        return MenuItem.objects.none()

    def perform_create(self, serializer):
        """Garante que apenas o dono do restaurante pode adicionar itens ao menu."""
        restaurant = serializer.validated_data.get('restaurant')
        if restaurant.owner != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("Você não tem permissão para adicionar itens neste restaurante.")
        serializer.save()
