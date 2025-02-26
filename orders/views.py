from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from orders.models import Order


class UpdateOrderStatusView(APIView):
    """Permite que donos de restaurantes aceitem, rejeitem ou atualizem o status do pedido"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Permite atualizar o status de um pedido"""
        order = Order.objects.get(pk=pk)

        if order.restaurant.owner != request.user:
            raise PermissionDenied("Você não tem permissão para modificar este pedido.")

        new_status = request.data.get("status")
        if new_status not in ['em preparo', 'saiu para entrega', 'entregue', 'cancelado']:
            return Response({"error": "Status inválido."}, status=400)

        order.status = new_status
        order.save()
        return Response({"message": f"Pedido atualizado para '{order.status}'."})


class RestaurantStatsView(APIView):
    """Retorna estatísticas de pedidos e faturamento para donos de restaurantes"""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna estatísticas de pedidos"""
        if request.user.role == 'admin':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(restaurant__owner=request.user)

        total_pedidos = orders.count()
        total_vendas = sum(order.total for order in orders)
        pedidos_por_status = orders.values('status').annotate(count=models.Count('id'))

        return Response({
            "total_pedidos": total_pedidos,
            "total_vendas": total_vendas,
            "pedidos_por_status": pedidos_por_status
        })
