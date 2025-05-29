from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address']
