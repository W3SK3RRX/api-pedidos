from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Permite acesso apenas para administradores"""

    def has_permission(self, request, view):
        if request.user and hasattr(request.user, 'role'):
            return request.user.role == 'admin'
        return False
