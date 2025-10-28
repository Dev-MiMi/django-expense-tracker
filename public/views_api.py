from rest_framework import generics
from .serializers import RegisterSerializer
from .models import CustomUser

# Register view api
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
