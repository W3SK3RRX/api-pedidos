from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    """Permite que apenas o dono do restaurante faça alterações"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user


class IsOwnerOrAdmin(BasePermission):
    """Permite que apenas o dono do restaurante ou um administrador faça alterações"""
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or obj.owner == request.user
        )