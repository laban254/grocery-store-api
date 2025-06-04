from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Simple serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        read_only_fields = ["id", "name", "slug", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for the Product model.
    """

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "category", "description", "price", "stock"]
        read_only_fields = fields


class BulkProductCreateSerializer(serializers.Serializer):
    """
    Serializer for creating multiple products at once.
    """

    products = ProductSerializer(many=True)

    def create(self, validated_data):
        products_data = validated_data.get("products")
        products = []

        for product_data in products_data:
            product = Product.objects.create(**product_data)
            products.append(product)

        return {"products": products}
