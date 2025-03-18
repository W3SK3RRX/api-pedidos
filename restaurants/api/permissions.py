from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRestaurantOwner(BasePermission):
    """Permite que apenas o dono do restaurante faça alterações"""

    def has_permission(self, request, view):
        # GET é permitido para qualquer usuário autenticado
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # POST, PUT, DELETE são permitidos apenas se for dono do objeto
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Apenas o dono pode modificar ou deletar
        return request.user == obj.owner


class IsOwnerOrAdmin(BasePermission):
    """Permite que apenas o dono do restaurante ou um administrador faça alterações"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False  # Bloquear usuários não autenticados

        if request.user.role == "admin":
            return True  # Admins podem modificar qualquer coisa

        # Permitir GET para todos os usuários autenticados
        if request.method in SAFE_METHODS:
            return True

        # Permitir PUT e DELETE (mas o controle real será no `has_object_permission`)
        return request.method in ["PUT", "DELETE"]

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or obj.owner == request.user

