from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRestaurantOwner(BasePermission):
    """Permite que apenas o dono do restaurante faça alterações"""

    def has_permission(self, request, view):
        # Permitir GET para qualquer autenticado, mas POST, PUT e DELETE só para donos
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return False  # 🔹 Apenas donos podem modificar

    def has_object_permission(self, request, view, obj):
        # Apenas o dono do restaurante pode modificar
        return request.user.is_authenticated and obj.owner == request.user


class IsOwnerOrAdmin(BasePermission):
    """Permite que apenas o dono do restaurante ou um administrador faça alterações"""

    def has_permission(self, request, view):
        # Apenas usuários autenticados podem acessar
        if not request.user.is_authenticated:
            return False

        # Admins podem acessar qualquer coisa
        if request.user.role == "admin":
            return True

        # Para GET, usuários veem apenas seus próprios restaurantes
        if request.method in SAFE_METHODS:
            return True

        # Para outros métodos (POST, PUT, DELETE), apenas donos podem acessar
        return False

    def has_object_permission(self, request, view, obj):
        # Apenas o dono ou admin pode modificar ou deletar
        return request.user.role == "admin" or obj.owner == request.user
