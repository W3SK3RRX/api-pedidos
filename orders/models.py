from django.db import models
from users.models import User
from restaurants.models import Restaurant, MenuItem


class Order(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em preparo', 'Em Preparo'),
        ('saiu para entrega', 'Saiu para Entrega'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.restaurant.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    
class OrderAuditLog(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="audit_logs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.order.id} atualizado de {self.old_status} para {self.new_status}"