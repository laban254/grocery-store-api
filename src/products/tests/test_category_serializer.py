import pytest

from products.models import Category
from products.serializers import CategorySerializer


@pytest.fixture
def category_tree():
    """Create a tree of categories for testing serializers."""
    # Root level
    root = Category.objects.create(name="All Products", slug="all-products")

    # Level 1
    groceries = Category.objects.create(name="Groceries", slug="groceries", parent=root)
    electronics = Category.objects.create(name="Electronics", slug="electronics", parent=root)

    # Level 2 under Groceries
    fruits = Category.objects.create(name="Fruits", slug="fruits", parent=groceries)

    # Level 3
    citrus = Category.objects.create(name="Citrus", slug="citrus", parent=fruits)

    # Create a dictionary to access all categories easily in tests
    categories = {
        "root": root,
        "groceries": groceries,
        "electronics": electronics,
        "fruits": fruits,
        "citrus": citrus,
    }

    return categories


class TestCategorySerializer:
    """Test cases for the CategorySerializer."""

    def test_root_category_serialization(self, db, category_tree):
        """Test serializing a root category."""
        root = category_tree["root"]
        serializer = CategorySerializer(instance=root)
        data = serializer.data

        assert data["id"] == root.id
        assert data["name"] == "All Products"
        assert data["slug"] == "all-products"
        assert data["parent"] is None

    def test_child_category_serialization(self, db, category_tree):
        """Test serializing a child category."""
        groceries = category_tree["groceries"]
        serializer = CategorySerializer(instance=groceries)
        data = serializer.data

        assert data["id"] == groceries.id
        assert data["name"] == "Groceries"
        assert data["slug"] == "groceries"
        assert data["parent"] == category_tree["root"].id

    def test_nested_category_serialization(self, db, category_tree):
        """Test serializing a deeply nested category."""
        citrus = category_tree["citrus"]
        serializer = CategorySerializer(instance=citrus)
        data = serializer.data

        assert data["id"] == citrus.id
        assert data["name"] == "Citrus"
        assert data["slug"] == "citrus"
        assert data["parent"] == category_tree["fruits"].id

    def test_multiple_categories_serialization(self, db, category_tree):
        """Test serializing multiple categories."""
        categories = list(category_tree.values())
        serializer = CategorySerializer(instance=categories, many=True)
        data = serializer.data

        assert len(data) == 5

        # Check that all categories are in the response
        category_names = [category["name"] for category in data]
        expected_names = ["All Products", "Groceries", "Electronics", "Fruits", "Citrus"]
        for name in expected_names:
            assert name in category_names

    def test_deserialization_not_allowed(self, db, category_tree):
        """Test that deserialization is not allowed (read-only fields)."""
        data = {"name": "New Category", "slug": "new-category", "parent": category_tree["root"].id}

        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()

        # Check that the fields are read-only and no data was created
        result = serializer.validated_data
        assert "name" not in result
        assert "slug" not in result
        assert "parent" not in result
