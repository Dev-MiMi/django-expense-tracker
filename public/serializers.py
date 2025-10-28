from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
