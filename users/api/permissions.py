from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Permite acesso apenas para administradores"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
