from rest_framework import serializers
from .models import Account, Record, Budget
from datetime import datetime, date, time


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "name",
            "acct_num",
            "balance",
            "account_type",
            "currency",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]


class RecordSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = "__all__"

    def get_date(self, obj):
        value = getattr(obj, "date", None)
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return None

    def get_time(self, obj):
        value = getattr(obj, "time", None)
        if isinstance(value, datetime):
            return value.time()
        if isinstance(value, time):
            return value
        return None

    def create(self, validated_data):
        if isinstance(validated_data.get("date"), datetime):
            validated_data["date"] = validated_data["date"].date()
        if isinstance(validated_data.get("time"), datetime):
            validated_data["time"] = validated_data["time"].time()
        return super().create(validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    # Accept a list from the API
    categories = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    class Meta:
        model = Budget
        fields = "__all__"
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        # Convert list comma-separated string for MultiSelectField
        categories = validated_data.pop("categories", [])
        validated_data["categories"] = ",".join(categories)
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        # Convert comma-separated string -> list when returning data
        data = super().to_representation(instance)
        data["categories"] = (
            instance.categories.split(",") if instance.categories else []
        )
        return data
