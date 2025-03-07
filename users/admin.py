from django.contrib import admin
from users.models import User, AccessLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_active", "is_2fa_enabled")
    list_filter = ("role", "is_active", "is_2fa_enabled")
    search_fields = ("username", "email")
    ordering = ("id",)
    actions = ["activate_users", "deactivate_users"]

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Ativar usuários selecionados"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Desativar usuários selecionados"

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "ip_address", "endpoint", "method", "status_code", "timestamp")
    list_filter = ("user", "status_code", "method")  # Adicionei 'status_code' e 'method' para facilitar o filtro
    search_fields = ("ip_address", "endpoint", "method")  # Permite buscar por ip_address, endpoint e method
    ordering = ("-timestamp",)  # Ordenação por data (do mais recente para o mais antigo)
    date_hierarchy = "timestamp"  # Permite filtrar por data no admin