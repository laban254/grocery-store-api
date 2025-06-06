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
def parent_category():
    """Create a parent category for testing."""
    return Category.objects.create(name="Groceries", slug="groceries")


@pytest.fixture
def child_category(parent_category):
    """Create a child category for testing."""
    return Category.objects.create(name="Fruits", slug="fruits", parent=parent_category)


@pytest.fixture
def products(child_category):
    """Create multiple products for testing."""
    products = [
        Product.objects.create(
            name="Apple",
            slug="apple",
            category=child_category,
            description="Fresh red apples",
            price=2.99,
            stock=100,
        ),
        Product.objects.create(
            name="Banana",
            slug="banana",
            category=child_category,
            description="Yellow bananas",
            price=1.99,
            stock=150,
        ),
        Product.objects.create(
            name="Orange",
            slug="orange",
            category=child_category,
            description="Juicy oranges",
            price=3.49,
            stock=80,
        ),
    ]
    return products


class TestCategoryViewSet:
    """Test cases for the CategoryViewSet."""

    def test_list_categories(self, db, api_client, parent_category, child_category):
        """Test listing all categories."""
        url = reverse("category-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # Check that both categories are in the response
        category_ids = [category["id"] for category in response.data]
        assert parent_category.id in category_ids
        assert child_category.id in category_ids

    def test_retrieve_category(self, db, api_client, child_category):
        """Test retrieving a single category."""
        url = reverse("category-detail", args=[child_category.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == child_category.id
        assert response.data["name"] == child_category.name
        assert response.data["slug"] == child_category.slug
        assert response.data["parent"] == child_category.parent.id


class TestProductViewSet:
    """Test cases for the ProductViewSet."""

    def test_list_products(self, db, api_client, products):
        """Test listing all products."""
        url = reverse("product-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(products)

        # Check that all products are in the response
        product_names = [product["name"] for product in response.data]
        expected_names = [product.name for product in products]
        for name in expected_names:
            assert name in product_names

    def test_filter_products_by_category(self, db, api_client, products, child_category):
        """Test filtering products by category."""
        url = f"{reverse('product-list')}?category_id={child_category.id}"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == len(products)

        # All products should be from the child_category
        for product_data in response.data:
            assert product_data["category"]["id"] == child_category.id

    @pytest.mark.django_db
    def test_retrieve_product(self, api_client, products):
        """Test retrieving a single product."""
        product = products[0]
        url = reverse("product-detail", args=[product.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id
        assert response.data["name"] == product.name
        assert response.data["slug"] == product.slug
        assert response.data["description"] == product.description
        assert float(response.data["price"]) == float(product.price)
        assert response.data["stock"] == product.stock

    @pytest.mark.django_db
    def test_category_average_price(self, api_client, products, child_category):
        """Test the category_average_price action."""
        url = f"{reverse('product-category-average-price')}?category_id={child_category.id}"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "average_price" in response.data

        # Calculate expected average manually
        prices = [product.price for product in products]
        expected_avg = sum(prices) / len(prices)
        assert float(response.data["average_price"]) == pytest.approx(expected_avg)

    @pytest.mark.django_db
    def test_category_average_price_with_subcategories(
        self, api_client, products, parent_category, child_category
    ):
        """Test the category_average_price action with include_subcategories=true."""
        base_url = reverse("product-category-average-price")
        url = f"{base_url}?category_id={parent_category.id}&include_subcategories=true"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "average_price" in response.data

        # Since all products are in child_category, which is a subcategory of parent_category,
        # the average should be the same as the previous test
        prices = [product.price for product in products]
        expected_avg = sum(prices) / len(prices)
        assert float(response.data["average_price"]) == pytest.approx(expected_avg)

    @pytest.mark.django_db
    def test_category_average_price_missing_category(self, api_client):
        """Test the category_average_price action without a category_id."""
        url = reverse("product-category-average-price")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "error" in response.data
        assert "category_id parameter is required" in response.data["error"]

    @pytest.mark.django_db
    def test_category_average_price_nonexistent_category(self, api_client):
        """Test the category_average_price action with a nonexistent category_id."""
        url = f"{reverse('product-category-average-price')}?category_id=999"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "error" in response.data
        assert "Category with ID 999 does not exist" in response.data["error"]
