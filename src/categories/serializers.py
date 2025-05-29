from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent']


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with nested children.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'children']
    
    def get_children(self, obj):
        children = obj.get_children()
        serializer = CategoryTreeSerializer(children, many=True)
        return serializer.data
