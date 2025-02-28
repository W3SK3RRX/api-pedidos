from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from orders.models import Order, OrderAuditLog
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from orders.api.serializers import OrderAuditLogSerializer
from users.api.permissions import IsAdmin  # Permissão para admin

class UpdateOrderStatusView(APIView):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)

        if order.restaurant.owner != request.user:
            raise PermissionDenied("Você não tem permissão para modificar este pedido.")

        new_status = request.data.get("status")
        if new_status not in ['em preparo', 'saiu para entrega', 'entregue', 'cancelado']:
            return Response({"error": "Status inválido."}, status=400)

        # Criar um log de auditoria
        OrderAuditLog.objects.create(
            order=order,
            user=request.user,
            old_status=order.status,
            new_status=new_status
        )

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
        total_vendas = orders.aggregate(Sum("total"))["total__sum"] or 0
        pedidos_por_status = orders.values("status").annotate(count=Count("id"))

        # Faturamento dos últimos 6 meses
        today = datetime.today()
        last_6_months = [today - timedelta(days=30*i) for i in range(6)]
        faturamento_mensal = {
            month.strftime("%Y-%m"): orders.filter(created_at__year=month.year, created_at__month=month.month).aggregate(Sum("total"))["total__sum"] or 0
            for month in reversed(last_6_months)
        }

        return Response({
            "total_pedidos": total_pedidos,
            "total_vendas": total_vendas,
            "pedidos_por_status": pedidos_por_status,
            "faturamento_mensal": faturamento_mensal
        })
    

class OrderAuditLogView(ListAPIView):
    """Lista o histórico de mudanças de pedidos (apenas para admin)"""
    
    queryset = OrderAuditLog.objects.all().order_by("-timestamp")
    serializer_class = OrderAuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        """Filtrar por usuário ou pedido, se passado na query string"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user")
        order_id = self.request.query_params.get("order")
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        
        return queryset
