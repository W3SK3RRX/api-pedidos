from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from restaurants.models import Restaurant, Address
from rest_framework import status
from restaurants.api.serializers import RestaurantSerializer


class CreateRestaurantView(APIView):
    """API para criar restaurantes"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Cria um restaurante associado ao usuário autenticado"""

        print(f"🟢 Usuário autenticado: {request.user}")  # DEBUG
        
        serializer = RestaurantSerializer(data=request.data, context={"request": request})  

        if serializer.is_valid():
            address_data = serializer.validated_data.pop("address", None)
            serializer.validated_data.pop("owner", None)  # 🔹 Removendo owner antes de criar o restaurante
            
            if not address_data:
                return Response({"error": "O campo 'address' é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
            
            address = Address.objects.create(**address_data)
            restaurant = Restaurant.objects.create(
                address=address, 
                owner=request.user,  # 🔹 Agora passamos `owner` corretamente
                **serializer.validated_data
            )

            return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PendingRestaurantNotifications(APIView):
    permission_classes = [IsAdminUser]  # Apenas admins podem acessar

    def get(self, request):
        pending_count = Restaurant.objects.filter(status="pending").count()
        return Response({"pending_requests": pending_count})


class ApproveRestaurantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Permite que apenas administradores aprovem restaurantes"""
        if request.user.role != 'admin':
            raise PermissionDenied("Apenas administradores podem aprovar restaurantes.")

        restaurant = Restaurant.objects.get(pk=pk)
        restaurant.status = 'ativo'
        restaurant.save()
        return Response({"message": f"Restaurante '{restaurant.name}' aprovado com sucesso."})


class RestaurantBySlugView(RetrieveAPIView):
    """Permite buscar um restaurante pelo slug"""
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