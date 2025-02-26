from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(ModelViewSet):
    """Permite que donos de restaurantes atualizem pedidos"""
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Clientes só podem ver seus pedidos. Donos veem pedidos do seu restaurante."""
        if self.request.user.role == 'cliente':
            return Order.objects.filter(customer=self.request.user)
        if self.request.user.role in ['funcionario', 'dono']:  # Ajustado para permitir donos de restaurantes
            return Order.objects.filter(restaurant__owner=self.request.user)
        return Order.objects.all()  # Admin vê tudo

    def perform_update(self, serializer):
        """Apenas o dono do restaurante pode alterar o status do pedido"""
        order = self.get_object()
        if order.restaurant.owner != self.request.user:
            raise PermissionDenied("Você não tem permissão para modificar este pedido.")
        serializer.save()

class OrderItemViewSet(ReadOnlyModelViewSet):  # Agora é apenas leitura
    """Itens de pedidos não podem ser modificados depois da criação"""
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class RestaurantOrdersViewSet(ReadOnlyModelViewSet):
    """Permite que donos de restaurantes vejam apenas os pedidos do seu restaurante"""
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Dono só vê pedidos do seu restaurante. Admins veem tudo."""
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(restaurant__owner=self.request.user)  # Correção do filtro
