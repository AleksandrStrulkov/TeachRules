from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializer


# работа с Django REST Framework
class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


# работа с Django
