from rest_framework import serializers
from mptt.models import TreeForeignKey
from .models import Category, Product, Order, OrderItem
from accounts.models import Customer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model with nested children.
    """
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'children']
    
    def get_children(self, obj):
        """
        Get all children for this category.
        """
        # Only process children if this is a top-level request
        if self.context.get('depth', 0) > 3:
            return []
        
        children = obj.get_children()
        serializer = CategorySerializer(
            children, 
            many=True, 
            context={'depth': self.context.get('depth', 0) + 1}
        )
        return serializer.data


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving the complete category tree.
    Only used for root categories (those with no parent).
    """
    children = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'children']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'phone', 'address']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name', 
            'description', 'price', 'stock', 'available', 'sku'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    subtotal = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    customer_name = serializers.ReadOnlyField(source='customer.full_name')
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'customer_name',
            'status', 'total_amount', 'shipping_address', 
            'items', 'created_at'
        ]
