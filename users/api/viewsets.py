from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.api.serializers import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
