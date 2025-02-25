from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    """Permite que apenas o dono do restaurante faça alterações"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user
