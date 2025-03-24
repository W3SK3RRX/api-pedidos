from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from restaurants.models import Restaurant, Address, OperatingHours
from restaurants.api.serializers import RestaurantSerializer, OperatingHoursSerializer
from restaurants.api.permissions import IsOwnerOrAdmin
from django.db import transaction


class CreateRestaurantView(APIView):
    """API para criar restaurantes"""

    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def post(self, request):
        """Cria um restaurante associado ao usuário autenticado"""
        if request.user.role not in ["admin", "funcionario"]:
            return Response(
                {"detail": "Apenas funcionários ou administradores podem criar restaurantes."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RestaurantSerializer(data=request.data, context={"request": request})  

        if serializer.is_valid():
            with transaction.atomic():  # 🔹 Garante rollback em caso de erro
                address_data = serializer.validated_data.pop("address", None)
                operating_hours_data = request.data.get("operating_hours", [])  # 🔹 Captura horários do request
                
                if not address_data:
                    return Response({"error": "O campo 'address' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

                address = Address.objects.create(**address_data)

                restaurant = Restaurant.objects.create(
                    address=address, 
                    owner=request.user,  # 🔹 Define o dono corretamente
                    **serializer.validated_data
                )

                # 🔹 Criando os horários de funcionamento um por um
                for oh_data in operating_hours_data:
                    OperatingHours.objects.create(restaurant=restaurant, **oh_data)

                return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OperatingHoursCreateView(APIView):
    """API para adicionar ou listar horários de funcionamento de um restaurante"""

    permission_classes = [IsAuthenticated]

    def get(self, request, restaurant_id):
        """Retorna os horários de funcionamento de um restaurante"""
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurante não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        operating_hours = OperatingHours.objects.filter(restaurant=restaurant)
        serializer = OperatingHoursSerializer(operating_hours, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_id):
        """Cadastra novos horários de funcionamento para um restaurante"""
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id, owner=request.user)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurante não encontrado ou você não tem permissão."}, status=status.HTTP_404_NOT_FOUND)

        # `many=True` permite cadastrar vários horários de uma vez
        serializer = OperatingHoursSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingRestaurantNotifications(APIView):
    """Verifica quantos restaurantes estão pendentes de aprovação"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        pending_count = Restaurant.objects.filter(status="pendente").count()
        return Response({"pending_requests": pending_count})


class ApproveRestaurantView(APIView):
    """Permite que apenas administradores aprovem restaurantes"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != 'admin':
            raise PermissionDenied("Apenas administradores podem aprovar restaurantes.")

        try:
            restaurant = Restaurant.objects.get(pk=pk)
            restaurant.status = 'ativo'
            restaurant.save()
            return Response({"message": f"Restaurante '{restaurant.name}' aprovado com sucesso."})
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurante não encontrado"}, status=status.HTTP_404_NOT_FOUND)


class RestaurantBySlugView(RetrieveAPIView):
    """Busca um restaurante pelo slug"""
    queryset = Restaurant.objects.filter(status='ativo')
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'


class MyRestaurantsView(APIView):
    """Retorna a lista de restaurantes do usuário autenticado"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurants = Restaurant.objects.filter(owner=request.user)
        
        if not restaurants.exists():
            return Response({"message": "Você ainda não cadastrou um restaurante."}, status=404)

        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
