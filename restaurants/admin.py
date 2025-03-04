from django.contrib import admin
from restaurants.models import Restaurant, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "owner__username")
    ordering = ("-created_at",)
    actions = ["approve_restaurants"]

    def approve_restaurants(self, request, queryset):
        queryset.update(status="ativo")
    approve_restaurants.short_description = "Aprovar restaurantes selecionados"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "restaurant", "available")
    list_filter = ("available", "restaurant")
    search_fields = ("name",)
