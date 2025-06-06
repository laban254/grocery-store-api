from decimal import Decimal

import pytest

from products.models import Category, Product
from products.serializers import BulkProductCreateSerializer


@pytest.fixture
def category():
    """Create a test category."""
    return Category.objects.create(name="Fruits", slug="fruits")


@pytest.fixture
def bulk_product_data(category):
    """Create bulk product data for testing."""
    return {
        "products": [
            {
                "name": "Apple",
                "slug": "apple",
                "category": category.id,
                "description": "Fresh red apples",
                "price": Decimal("2.99"),
                "stock": 100,
            },
            {
                "name": "Banana",
                "slug": "banana",
                "category": category.id,
                "description": "Yellow bananas",
                "price": Decimal("1.99"),
                "stock": 150,
            },
            {
                "name": "Orange",
                "slug": "orange",
                "category": category.id,
                "description": "Juicy oranges",
                "price": Decimal("3.49"),
                "stock": 80,
            },
        ]
    }


class TestBulkProductCreateSerializer:
    """Test cases for the BulkProductCreateSerializer."""

    def test_bulk_product_creation(self, db, bulk_product_data):
        """Test that multiple products can be created using the serializer."""
        assert Product.objects.count() == 0

        serializer = BulkProductCreateSerializer(data=bulk_product_data)
        assert serializer.is_valid(), serializer.errors

        result = serializer.save()

        assert Product.objects.count() == 3
        assert len(result["products"]) == 3

        for i, product in enumerate(result["products"]):
            expected_data = bulk_product_data["products"][i]
            assert product.name == expected_data["name"]
            assert product.slug == expected_data["slug"]
            assert product.category.id == expected_data["category"]
            assert product.description == expected_data["description"]
            assert product.price == expected_data["price"]
            assert product.stock == expected_data["stock"]

    def test_bulk_product_validation(self, db, category):
        """Test validation in the bulk product serializer."""
        invalid_data = {
            "products": [
                {
                    "name": "Apple",
                    "category": category.id,
                    # Missing price
                    "stock": 100,
                }
            ]
        }

        serializer = BulkProductCreateSerializer(data=invalid_data)
        assert not serializer.is_valid()

        errors = serializer.errors
        assert "products" in errors
        products_errors = errors["products"][0]
        assert "slug" in products_errors
        assert "price" in products_errors

    def test_invalid_category(self, db):
        """Test validation with invalid category ID."""
        invalid_data = {
            "products": [
                {
                    "name": "Apple",
                    "slug": "apple",
                    "category": 9999,
                    "description": "Fresh red apples",
                    "price": Decimal("2.99"),
                    "stock": 100,
                }
            ]
        }

        serializer = BulkProductCreateSerializer(data=invalid_data)
        assert not serializer.is_valid()

        errors = serializer.errors
        assert "products" in errors
        assert "category" in errors["products"][0]
