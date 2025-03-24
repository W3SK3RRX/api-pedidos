from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from restaurants.models import Restaurant, MenuItem, CategoryMenuItem, CategoryRestaurant, OperatingHours
from restaurants.api.serializers import RestaurantSerializer, MenuItemSerializer, CategorySerializer, OperatingHoursSerializer
from restaurants.api.permissions import IsOwnerOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryRestaurantViewSet(ModelViewSet):
    """ViewSet para gerenciar categorias de restaurantes"""
    queryset = CategoryRestaurant.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class RestaurantViewSet(ModelViewSet):
    """ViewSet para gerenciar restaurantes"""
    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """Admins veem todos os restaurantes. Donos só veem os seus."""
        if self.request.user.role == "admin":
            return Restaurant.objects.all()
        return Restaurant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Restaurantes são criados como 'pendente' e vinculados ao usuário logado."""
        serializer.save(owner=self.request.user, status='pendente')

    @action(detail=True, methods=["GET", "POST"], permission_classes=[IsAuthenticated])
    def operating_hours(self, request, pk=None):
        """Retorna ou adiciona horários de funcionamento do restaurante"""
        restaurant = self.get_object()

        # Verifica se o usuário é dono do restaurante
        if restaurant.owner != request.user and request.user.role != "admin":
            return Response({"error": "Você não tem permissão para modificar esses horários."}, status=403)

        if request.method == "POST":
            serializer = OperatingHoursSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(restaurant=restaurant)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        # Se for GET, retorna os horários existentes
        hours = OperatingHours.objects.filter(restaurant=restaurant)
        serializer = OperatingHoursSerializer(hours, many=True)
        return Response(serializer.data)


class CategoryItemViewSet(ModelViewSet):
    """ViewSet para gerenciar categorias de itens do menu"""
    queryset = CategoryMenuItem.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class MenuItemViewSet(ModelViewSet):
    """ViewSet para gerenciar itens do menu"""
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # 🔹 Suporte para uploads de imagens

    def get_queryset(self):
        """Filtra os itens de menu com base no tipo de usuário"""
        user = self.request.user

        if user.role == "admin":
            return MenuItem.objects.all()

        if user.role == "funcionario":
            return MenuItem.objects.filter(restaurant__owner=user)

        if user.role == "cliente":
            return MenuItem.objects.filter(restaurant__status="ativo")

        return MenuItem.objects.none()

    def perform_create(self, serializer):
        """Garante que apenas o dono do restaurante pode adicionar itens ao menu."""
        restaurant = serializer.validated_data.get("restaurant")
        if restaurant.owner != self.request.user and self.request.user.role != "admin":
            raise PermissionDenied("Você não tem permissão para adicionar itens neste restaurante.")
        serializer.save()
