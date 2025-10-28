from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .jwt_serializers import EmailOrUsernameLoginSerializer

User = get_user_model()


class EmailOrUsernameLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailOrUsernameLoginSerializer  #  link serializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]
        password = serializer.validated_data["password"]

        # Try authentication directly
        user = authenticate(request, username=identifier, password=password)

        if user is None:
            # Try via email
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid login credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        if not user.is_active:
            return Response(
                {"detail": "User account is not active"},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
