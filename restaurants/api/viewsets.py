from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from restaurants.models import Restaurant
from restaurants.api.serializers import RestaurantSerializer, MenuItemSerializer
from restaurants.models import MenuItem
from restaurants.api.permissions import IsRestaurantOwner
from users.api.permissions import IsAdmin


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Admins veem todos os restaurantes. Donos só veem os seus."""
        if self.request.user.role == 'admin':
            return Restaurant.objects.all()
        return Restaurant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Restaurantes são criados como 'pendente', admin deve aprovar."""
        serializer.save(owner=self.request.user, status='pendente')

    def perform_update(self, serializer):
        """Apenas admins podem alterar o status do restaurante."""
        restaurant = self.get_object()
        if 'status' in self.request.data and self.request.user.role != 'admin':
            raise PermissionDenied("Somente administradores podem aprovar ou rejeitar restaurantes.")
        serializer.save()


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
