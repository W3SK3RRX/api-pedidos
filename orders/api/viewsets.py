from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer
from restaurants.api.permissions import IsRestaurantOwner
from rest_framework.exceptions import PermissionDenied

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Clientes só podem ver seus pedidos, restaurantes veem pedidos recebidos"""
        if self.request.user.role == 'cliente':
            return Order.objects.filter(customer=self.request.user)
        elif self.request.user.role == 'funcionario':
            return Order.objects.filter(restaurant__owner=self.request.user)
        return Order.objects.all()

    def perform_create(self, serializer):
        """Clientes só podem criar pedidos para restaurantes existentes"""
        if self.request.user.role != 'cliente':
            raise PermissionDenied("Somente clientes podem criar pedidos.")
        serializer.save(customer=self.request.user)

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
