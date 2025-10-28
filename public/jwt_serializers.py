from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers

#login api
class EmailOrUsernameLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "username_or_email"

    username_or_email = serializers.CharField()

    def validate(self, attrs):
        login_value = attrs.get("username_or_email")
        password = attrs.get("password")

        user = authenticate(username=login_value, password=password)

        if not user:
            raise serializers.ValidationError({"detail": "Invalid login credentials"})

        attrs["username"] = user.username
        return super().validate(attrs)
