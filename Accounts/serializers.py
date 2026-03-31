from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "phone_number",
            "role",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]
