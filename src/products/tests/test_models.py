import pytest
from django.db import IntegrityError
from django.utils.text import slugify

from products.models import Category, Product


@pytest.fixture
def parent_category():
    """Create a parent category for testing."""
    return Category.objects.create(name="Groceries", slug="groceries")


@pytest.fixture
def child_category(parent_category):
    """Create a child category for testing."""
    return Category.objects.create(name="Fruits", slug="fruits", parent=parent_category)


@pytest.fixture
def product(child_category):
    """Create a test product."""
    return Product.objects.create(
        name="Apple",
        slug="apple",
        category=child_category,
        description="Fresh red apples",
        price=2.99,
        stock=100,
    )


class TestCategoryModel:
    """Test cases for the Category model."""

    def test_category_creation(self, db, parent_category):
        """Test that a category can be created successfully."""
        assert Category.objects.count() == 1
        assert parent_category.name == "Groceries"
        assert parent_category.slug == "groceries"
        assert parent_category.parent is None

    def test_category_str_representation(self, db, parent_category):
        """Test the string representation of a category."""
        assert str(parent_category) == "Groceries"

    def test_category_hierarchy(self, db, parent_category, child_category):
        """Test the MPTT hierarchy functionality."""
        assert child_category.parent == parent_category
        assert child_category in parent_category.children.all()

        # Test MPTT specific methods
        assert child_category.get_root() == parent_category
        assert list(child_category.get_ancestors()) == [parent_category]
        assert child_category.is_child_node()
        assert parent_category.is_root_node()

    def test_slug_auto_generation(self, db):
        """Test that slug is auto-generated if not provided."""
        category = Category.objects.create(name="Test Category")
        assert category.slug == "test-category"
        assert category.slug == slugify(category.name)

    @pytest.mark.django_db
    def test_category_unique_constraints(self):
        """Test that category name and slug must be unique."""
        Category.objects.create(name="Groceries", slug="groceries")

        # Test unique name constraint
        with pytest.raises(Exception):
            Category.objects.create(name="Groceries", slug="groceries-duplicate")

        # Test unique slug constraint
        with pytest.raises(Exception):
            Category.objects.create(name="Groceries Duplicate", slug="groceries")


class TestProductModel:
    """Test cases for the Product model."""

    def test_product_creation(self, db, product, child_category):
        """Test that a product can be created successfully."""
        assert Product.objects.count() == 1
        assert product.name == "Apple"
        assert product.slug == "apple"
        assert product.category.name == "Fruits"
        assert product.description == "Fresh red apples"
        assert product.price == 2.99
        assert product.stock == 100
        assert product.created_at is not None
        assert product.updated_at is not None

    def test_product_str_representation(self, db, product):
        """Test the string representation of a product."""
        assert str(product) == "Apple"

    def test_slug_auto_generation(self, db, child_category):
        """Test that slug is auto-generated if not provided."""
        product = Product.objects.create(
            name="Test Product", category=child_category, price=1.99, stock=50
        )
        assert product.slug == "test-product"
        assert product.slug == slugify(product.name)

    def test_product_unique_constraints(self, db, product, child_category):
        """Test that product slug must be unique."""
        with pytest.raises(IntegrityError):
            Product.objects.create(
                name="Apple Duplicate",
                slug="apple",  # This should cause the constraint violation
                category=child_category,
                price=3.99,
                stock=200,
            )
