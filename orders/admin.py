from django.contrib import admin
from orders.models import Order, OrderAuditLog

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "restaurant", "status", "total", "created_at")
    list_filter = ("status", "restaurant")
    search_fields = ("customer__username", "restaurant__name")
    ordering = ("-created_at",)
    actions = ["mark_as_delivered"]

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="entregue")
    mark_as_delivered.short_description = "Marcar pedidos como entregues"

@admin.register(OrderAuditLog)
class OrderAuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "user", "old_status", "new_status", "timestamp")
    list_filter = ("new_status",)
    search_fields = ("order__id", "user__username")
    ordering = ("-timestamp",)
