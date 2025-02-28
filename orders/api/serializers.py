from rest_framework import serializers
from orders.models import Order, OrderItem, OrderAuditLog

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'status', 'total', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'quantity', 'subtotal']

class OrderAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = OrderAuditLog
        fields = ["id", "order", "user", "old_status", "new_status", "timestamp"]