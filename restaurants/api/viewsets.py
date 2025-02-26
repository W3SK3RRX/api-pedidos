from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from restaurants.models import Restaurant
from restaurants.api.serializers import RestaurantSerializer
from restaurants.api.permissions import IsOwnerOrAdmin
from restaurants.models import MenuItem
from restaurants.api.serializers import MenuItemSerializer  

class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """Admins veem todos os restaurantes. Donos só veem os seus."""
        if self.request.user.role == 'admin':
            return Restaurant.objects.all()
        return Restaurant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Restaurantes são criados como 'pendente' e vinculados ao usuário logado."""
        serializer.save(owner=self.request.user, status='pendente')

    def perform_update(self, serializer):
        """Apenas o dono ou um admin pode editar o restaurante."""
        restaurant = self.get_object()
        if restaurant.owner != self.request.user and self.request.user.role != 'admin':
            raise PermissionDenied("Você não tem permissão para modificar este restaurante.")
        serializer.save()


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
