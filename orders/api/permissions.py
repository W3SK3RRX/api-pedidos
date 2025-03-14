from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """Permite que apenas clientes criem pedidos"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'cliente'
