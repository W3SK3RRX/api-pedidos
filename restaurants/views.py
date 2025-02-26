from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from restaurants.models import Restaurant
from restaurants.api.serializers import RestaurantSerializer


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