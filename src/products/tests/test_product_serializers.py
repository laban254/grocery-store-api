from decimal import Decimal

import pytest

from products.models import Category, Product
from products.serializers import CategorySerializer, ProductSerializer


@pytest.fixture
def parent_category():
    """Create a parent category for testing."""
    return Category.objects.create(name="Groceries", slug="groceries")


@pytest.fixture
def child_category(parent_category):
    """Create a child category for testing."""
    return Category.objects.create(name="Fruits", slug="fruits", parent=parent_category)


@pytest.fixture
def category():
    """Create a test category."""
    return Category.objects.create(name="Fruits", slug="fruits")


@pytest.fixture
def product(category):
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


class TestCategorySerializer:
    """Test cases for the CategorySerializer."""

    def test_category_serializer_contains_expected_fields(self, db, parent_serializer):
        """Test that the serializer contains the expected fields."""
        data = parent_serializer.data
        assert "id" in data
        assert "name" in data
        assert "slug" in data
        assert "parent" in data

    def test_category_serializer_field_content(
        self, db, parent_serializer, child_serializer, parent_category
    ):
        """Test that the serializer correctly represents the category data."""
        parent_data = parent_serializer.data
        assert parent_data["name"] == "Groceries"
        assert parent_data["slug"] == "groceries"
        assert parent_data["parent"] is None

        child_data = child_serializer.data
        assert child_data["name"] == "Fruits"
        assert child_data["slug"] == "fruits"
        assert child_data["parent"] == parent_category.id


class TestProductSerializer:
    """Test cases for the ProductSerializer."""

    def test_product_serializer_contains_expected_fields(self, db, product_serializer):
        """Test that the serializer contains the expected fields."""
        data = product_serializer.data
        assert "id" in data
        assert "name" in data
        assert "slug" in data
        assert "category" in data
        assert "description" in data
        assert "price" in data
        assert "stock" in data

    def test_product_serializer_field_content(self, db, product_serializer, category):
        """Test that the serializer correctly represents the product data."""
        data = product_serializer.data
        assert data["name"] == "Apple"
        assert data["slug"] == "apple"
        assert data["description"] == "Fresh red apples"
        assert Decimal(data["price"]) == Decimal("2.99")
        assert data["stock"] == 100

        # Check that the category is serialized correctly
        assert data["category"]["name"] == "Fruits"
        assert data["category"]["slug"] == "fruits"
