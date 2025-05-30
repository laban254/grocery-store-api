from rest_framework import serializers
from .models import User, Customer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'oidc_provider']
        read_only_fields = ['id', 'email', 'oidc_provider']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'email', 'created_at']


class CustomerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Customer information.
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'address']
