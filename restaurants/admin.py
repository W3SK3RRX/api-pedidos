from django.contrib import admin
from restaurants.models import Restaurant, Address, MenuItem

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "street", "number", "neighborhood", "city", "cep")
    search_fields = ("street", "neighborhood", "city", "cep")

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status")
    list_filter = ("status",)
    search_fields = ("name", "owner__username")
    actions = ["approve_restaurants"]

    def approve_restaurants(self, request, queryset):
        queryset.update(status="ativo")
    approve_restaurants.short_description = "Aprovar restaurantes selecionados"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "restaurant", "available")
    list_filter = ("available", "restaurant")
    search_fields = ("name",)
