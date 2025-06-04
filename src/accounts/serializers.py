from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model that includes both authentication and customer information.
    """

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "address",
            "oidc_provider",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email", "oidc_provider", "created_at", "updated_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating User information.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "address"]
        read_only_fields = ["email"]
