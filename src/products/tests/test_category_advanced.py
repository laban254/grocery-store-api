import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from products.models import Category, Product


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def category_tree():
    """Create a tree of categories for testing advanced MPTT functionality."""
    # Root level
    root = Category.objects.create(name="All Products", slug="all-products")

    # Level 1
    groceries = Category.objects.create(name="Groceries", slug="groceries", parent=root)
    electronics = Category.objects.create(name="Electronics", slug="electronics", parent=root)

    # Level 2 under Groceries
    fruits = Category.objects.create(name="Fruits", slug="fruits", parent=groceries)
    vegetables = Category.objects.create(name="Vegetables", slug="vegetables", parent=groceries)
    dairy = Category.objects.create(name="Dairy", slug="dairy", parent=groceries)

    # Level 2 under Electronics
    computers = Category.objects.create(name="Computers", slug="computers", parent=electronics)
    phones = Category.objects.create(name="Phones", slug="phones", parent=electronics)

    # Level 3
    citrus = Category.objects.create(name="Citrus", slug="citrus", parent=fruits)
    berries = Category.objects.create(name="Berries", slug="berries", parent=fruits)

    laptops = Category.objects.create(name="Laptops", slug="laptops", parent=computers)

    # Create a dictionary to access all categories easily in tests
    categories = {
        "root": root,
        "groceries": groceries,
        "electronics": electronics,
        "fruits": fruits,
        "vegetables": vegetables,
        "dairy": dairy,
        "computers": computers,
        "phones": phones,
        "citrus": citrus,
        "berries": berries,
        "laptops": laptops,
    }

    return categories


@pytest.fixture
def products_by_category(category_tree):
    """Create products for different categories."""
    products = {}

    # Create products for citrus
    products["orange"] = Product.objects.create(
        name="Orange",
        slug="orange",
        category=category_tree["citrus"],
        description="Juicy oranges",
        price=3.49,
        stock=80,
    )

    products["lemon"] = Product.objects.create(
        name="Lemon",
        slug="lemon",
        category=category_tree["citrus"],
        description="Fresh lemons",
        price=2.99,
        stock=60,
    )

    # Create products for berries
    products["strawberry"] = Product.objects.create(
        name="Strawberry",
        slug="strawberry",
        category=category_tree["berries"],
        description="Sweet strawberries",
        price=4.99,
        stock=40,
    )

    # Create products for vegetables
    products["carrot"] = Product.objects.create(
        name="Carrot",
        slug="carrot",
        category=category_tree["vegetables"],
        description="Fresh carrots",
        price=1.99,
        stock=100,
    )

    # Create products for laptops
    products["macbook"] = Product.objects.create(
        name="MacBook Pro",
        slug="macbook-pro",
        category=category_tree["laptops"],
        description="Apple MacBook Pro",
        price=1299.99,
        stock=10,
    )

    return products


class TestCategoryAdvancedMPTT:
    """Test cases for advanced MPTT functionality in the Category model."""

    def test_get_descendants(self, db, category_tree):
        """Test getting all descendants of a category."""
        groceries = category_tree["groceries"]
        descendants = groceries.get_descendants()

        assert len(descendants) == 5  # fruits, vegetables, dairy, citrus, berries
        assert category_tree["fruits"] in descendants
        assert category_tree["vegetables"] in descendants
        assert category_tree["dairy"] in descendants
        assert category_tree["citrus"] in descendants
        assert category_tree["berries"] in descendants

    def test_get_descendants_include_self(self, db, category_tree):
        """Test getting all descendants including self."""
        groceries = category_tree["groceries"]
        descendants = groceries.get_descendants(include_self=True)

        assert len(descendants) == 6  # groceries, fruits, vegetables, dairy, citrus, berries
        assert groceries in descendants

    def test_get_children(self, db, category_tree):
        """Test getting immediate children of a category."""
        groceries = category_tree["groceries"]
        children = groceries.get_children()

        assert len(children) == 3  # fruits, vegetables, dairy
        assert category_tree["fruits"] in children
        assert category_tree["vegetables"] in children
        assert category_tree["dairy"] in children

        # Grandchildren should not be included
        assert category_tree["citrus"] not in children
        assert category_tree["berries"] not in children

    def test_get_ancestors(self, db, category_tree):
        """Test getting all ancestors of a category."""
        citrus = category_tree["citrus"]
        ancestors = citrus.get_ancestors()

        assert len(ancestors) == 3  # root, groceries, fruits
        assert category_tree["root"] in ancestors
        assert category_tree["groceries"] in ancestors
        assert category_tree["fruits"] in ancestors

    def test_get_root(self, db, category_tree):
        """Test getting the root of a category."""
        citrus = category_tree["citrus"]
        root = citrus.get_root()

        assert root == category_tree["root"]

        # Also test from a different branch
        laptops = category_tree["laptops"]
        root = laptops.get_root()

        assert root == category_tree["root"]

    def test_is_child_of(self, db, category_tree):
        """Test checking if a category is a child of another category."""
        fruits = category_tree["fruits"]
        groceries = category_tree["groceries"]

        assert fruits.is_child_node()
        assert fruits in groceries.get_children()

    def test_is_descendant_of(self, db, category_tree):
        """Test checking if a category is a descendant of another category."""
        citrus = category_tree["citrus"]
        groceries = category_tree["groceries"]
        electronics = category_tree["electronics"]

        assert citrus.is_descendant_of(groceries)
        assert not citrus.is_descendant_of(electronics)

    def test_get_level(self, db, category_tree):
        """Test getting the level of a category in the tree."""
        root = category_tree["root"]
        groceries = category_tree["groceries"]
        fruits = category_tree["fruits"]
        citrus = category_tree["citrus"]

        assert root.get_level() == 0
        assert groceries.get_level() == 1
        assert fruits.get_level() == 2
        assert citrus.get_level() == 3


class TestCategoryHierarchyAPI:
    """Test cases for the CategoryViewSet with hierarchical data."""

    def test_nonexistent_category(self, db, api_client):
        """Test retrieving a nonexistent category."""
        url = reverse("category-detail", args=[999])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_with_children(self, db, api_client, category_tree):
        """Test retrieving a category with children."""
        groceries = category_tree["groceries"]
        url = reverse("category-detail", args=[groceries.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == groceries.id
        assert response.data["name"] == "Groceries"

        # Note: The current CategorySerializer doesn't include children
        # If it did, we would test that here

    def test_deep_hierarchy_navigation(self, db, api_client, category_tree):
        """Test navigating through the category hierarchy."""
        # Start at root
        root = category_tree["root"]
        url = reverse("category-detail", args=[root.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "All Products"
        assert response.data["parent"] is None

        # Navigate to groceries (using the known ID from the response)
        groceries = category_tree["groceries"]
        url = reverse("category-detail", args=[groceries.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Groceries"
        assert response.data["parent"] == root.id

        # Navigate to fruits
        fruits = category_tree["fruits"]
        url = reverse("category-detail", args=[fruits.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Fruits"
        assert response.data["parent"] == groceries.id


class TestCategoryProducts:
    """Test cases for retrieving products within categories."""

    def test_products_by_category(self, db, api_client, category_tree, products_by_category):
        """Test retrieving products for a specific category."""
        citrus = category_tree["citrus"]
        url = f"{reverse('product-list')}?category_id={citrus.id}"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # orange, lemon

        product_names = [product["name"] for product in response.data]
        assert "Orange" in product_names
        assert "Lemon" in product_names

    def test_average_price_for_category_with_subcategories(
        self, db, api_client, category_tree, products_by_category
    ):
        """Test calculating average price for a category including subcategories."""
        fruits = category_tree["fruits"]
        base_url = reverse("product-category-average-price")
        url = f"{base_url}?category_id={fruits.id}&include_subcategories=true"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "average_price" in response.data

        # Calculate expected average: (3.49 + 2.99 + 4.99) / 3
        expected_avg = (3.49 + 2.99 + 4.99) / 3
        assert float(response.data["average_price"]) == pytest.approx(expected_avg)

    def test_average_price_for_category_without_subcategories(
        self, db, api_client, category_tree, products_by_category
    ):
        """Test calculating average price for a category excluding subcategories."""
        fruits = category_tree["fruits"]
        base_url = reverse("product-category-average-price")
        url = f"{base_url}?category_id={fruits.id}&include_subcategories=false"
        response = api_client.get(url)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "average_price" in response.data

        # There are no products directly in the fruits category (only in subcategories)
        assert float(response.data["average_price"]) == 0
