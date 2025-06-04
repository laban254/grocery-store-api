from django.db.models import Avg
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .schemas import (
    category_average_price_schema,
    list_categories_schema,
    list_products_schema,
    retrieve_category_schema,
    retrieve_product_schema,
)
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Read-only ViewSet for categories.
    Admin interface should be used for category management.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(**list_categories_schema)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(**retrieve_category_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Read-only ViewSet for products:
    - List products
    - Get product details
    - Calculate average price for a category

    Admin interface should be used for product management.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(**list_products_schema)
    def list(self, request, *args, **kwargs):
        category_id = self.request.query_params.get("category_id")
        queryset = self.get_queryset()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(**retrieve_product_schema)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(**category_average_price_schema)
    @action(detail=False, methods=["get"])
    def category_average_price(self, request):
        """
        Get the average product price for a given category.
        """
        category_id = request.query_params.get("category_id")
        include_subcategories = (
            request.query_params.get("include_subcategories", "false").lower() == "true"
        )

        if not category_id:
            return Response(
                {"error": "category_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response(
                {"error": f"Category with ID {category_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if include_subcategories:
            categories = category.get_descendants(include_self=True)
            queryset = self.get_queryset().filter(category__in=categories)
        else:
            queryset = self.get_queryset().filter(category=category)

        avg_price = queryset.aggregate(avg_price=Avg("price"))["avg_price"] or 0

        return Response({"average_price": avg_price})
