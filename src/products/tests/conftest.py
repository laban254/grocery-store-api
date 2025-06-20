from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def parent_category(db):
    """Create a parent category for testing."""
    return Category.objects.create(name="Groceries", slug="groceries")


@pytest.fixture
def child_category(db, parent_category):
    """Create a child category for testing."""
    return Category.objects.create(name="Fruits", slug="fruits", parent=parent_category)


@pytest.fixture
def category(db):
    """Create a test category."""
    return Category.objects.create(name="Fruits", slug="fruits")


@pytest.fixture
def product(db, category):
    """Create a test product."""
    return Product.objects.create(
        name="Apple",
        slug="apple",
        category=category,
        description="Fresh red apples",
        price=Decimal("2.99"),
        stock=100,
    )


@pytest.fixture
def products(db, child_category):
    """Create multiple products for testing."""
    products = [
        Product.objects.create(
            name="Apple",
            slug="apple",
            category=child_category,
            description="Fresh red apples",
            price=Decimal("2.99"),
            stock=100,
        ),
        Product.objects.create(
            name="Banana",
            slug="banana",
            category=child_category,
            description="Yellow bananas",
            price=Decimal("1.99"),
            stock=150,
        ),
        Product.objects.create(
            name="Orange",
            slug="orange",
            category=child_category,
            description="Juicy oranges",
            price=Decimal("3.49"),
            stock=80,
        ),
    ]
    return products


@pytest.fixture
def parent_serializer(parent_category):
    """Create a serializer for the parent category."""
    return CategorySerializer(instance=parent_category)


@pytest.fixture
def child_serializer(child_category):
    """Create a serializer for the child category."""
    return CategorySerializer(instance=child_category)


@pytest.fixture
def product_serializer(product):
    """Create a serializer for the product."""
    return ProductSerializer(instance=product)


@pytest.fixture
def bulk_product_data(category):
    """Create bulk product data for testing."""
    return {
        "products": [
            {
                "name": "Apple",
                "slug": "apple",
                "category": category,
                "description": "Fresh red apples",
                "price": Decimal("2.99"),
                "stock": 100,
            },
            {
                "name": "Banana",
                "slug": "banana",
                "category": category,
                "description": "Yellow bananas",
                "price": Decimal("1.99"),
                "stock": 150,
            },
            {
                "name": "Orange",
                "slug": "orange",
                "category": category,
                "description": "Juicy oranges",
                "price": Decimal("3.49"),
                "stock": 80,
            },
        ]
    }
