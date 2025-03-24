from django.contrib import admin
from restaurants.models import Restaurant, Address, MenuItem, CategoryRestaurant, CategoryMenuItem, OperatingHours

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "street", "number", "neighborhood", "city", "cep")
    search_fields = ("street", "neighborhood", "city", "cep")

@admin.register(CategoryRestaurant)
class CategoryRestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status")
    list_filter = ("status",)
    search_fields = ("name", "owner__username")
    actions = ["approve_restaurants"]

    def approve_restaurants(self, request, queryset):
        queryset.update(status="ativo")
    approve_restaurants.short_description = "Aprovar restaurantes selecionados"

@admin.register(OperatingHours)
class OperatingHoursAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "day_of_week", "open_time", "close_time")
    list_filter = ("day_of_week", "restaurant")  # 🔹 Adiciona filtro por restaurante
    search_fields = ("restaurant__name",)
    ordering = ("restaurant", "day_of_week")  # 🔹 Ordena por restaurante e dia da semana

@admin.register(CategoryMenuItem)
class CategoryMenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "restaurant", "available")
    list_filter = ("available", "restaurant")
    search_fields = ("name",)
