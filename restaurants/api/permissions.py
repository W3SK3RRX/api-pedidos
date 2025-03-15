from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRestaurantOwner(BasePermission):
    """Permite que apenas o dono do restaurante faça alterações"""
    
    def has_permission(self, request, view):
        # Permitir GET para qualquer autenticado, e POST para qualquer usuário logado
        if request.method in SAFE_METHODS or request.method == "POST":
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Apenas o dono pode modificar
        return request.user.is_authenticated and obj.owner == request.user


class IsOwnerOrAdmin(BasePermission):
    """Permite que apenas o dono do restaurante ou um administrador faça alterações"""

    def has_permission(self, request, view):
        # Permite POST para usuários autenticados
        if request.method == "POST":
            return request.user.is_authenticated
        # Para outros métodos, permite acesso a usuários autenticados
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Apenas o dono ou admin pode modificar o objeto
        return request.user.is_authenticated and (
            request.user.role == "admin" or obj.owner == request.user
        )