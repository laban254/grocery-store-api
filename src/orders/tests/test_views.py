import json
from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from orders.models import Order


class TestOrderViewSet:
    """Test cases for the OrderViewSet."""

    def test_list_orders_authenticated(self, db, authenticated_client, orders):
        """Test listing orders for authenticated user."""
        url = reverse("order-list")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        # Verify order details
        order_numbers = [order["order_number"] for order in response.data]
        assert "ORD-123ABC" in order_numbers
        assert "ORD-456DEF" in order_numbers

    def test_list_orders_unauthenticated(self, db, api_client, orders):
        """Test that unauthenticated users cannot list orders."""
        url = reverse("order-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_order_authenticated_owner(self, db, authenticated_client, orders):
        """Test retrieving a specific order by its owner."""
        order = orders[0]
        url = reverse("order-detail", args=[order.id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["order_number"] == order.order_number
        assert Decimal(response.data["total_amount"]) == order.total_amount
        assert response.data["shipping_address"] == order.shipping_address

    def test_retrieve_order_authenticated_wrong_user(self, db, api_client, orders):
        """Test that a user cannot retrieve another user's order."""
        # Create a different user and authenticate
        from django.contrib.auth import get_user_model

        User = get_user_model()
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="otherpassword123",
            phone="+254722111111",
        )
        api_client.force_authenticate(user=other_user)

        # Try to access the first user's order
        order = orders[0]
        url = reverse("order-detail", args=[order.id])
        response = api_client.get(url)

        # Should return 404 (not 403) as per the queryset filter in the view
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_order_unauthenticated(self, db, api_client, orders):
        """Test that unauthenticated users cannot retrieve orders."""
        order = orders[0]
        url = reverse("order-detail", args=[order.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_order_authenticated(self, db, authenticated_client, products):
        """Test creating a new order by authenticated user."""
        # Get initial stock
        initial_stock = products[0].stock

        # Prepare order data
        data = {
            "shipping_address": "789 Test Road, Nairobi, Kenya",
            "items": [{"product_id": products[0].id, "quantity": 5}],
        }

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "order_number" in response.data
        assert "total_amount" in response.data
        assert response.data["shipping_address"] == "789 Test Road, Nairobi, Kenya"

        # Verify order was created in database
        assert Order.objects.count() == 1
        order = Order.objects.first()

        # Verify order items
        assert order.items.count() == 1
        item = order.items.first()
        assert item.product.id == products[0].id
        assert item.quantity == 5

        # Verify stock was updated
        products[0].refresh_from_db()
        assert products[0].stock == initial_stock - 5

    def test_create_order_unauthenticated(self, db, api_client, products):
        """Test that unauthenticated users cannot create orders."""
        data = {
            "shipping_address": "789 Test Road, Nairobi, Kenya",
            "items": [{"product_id": products[0].id, "quantity": 5}],
        }

        url = reverse("order-list")
        response = api_client.post(url, data=json.dumps(data), content_type="application/json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Order.objects.count() == 0

    def test_create_order_with_invalid_data(self, db, authenticated_client, products):
        """Test creating an order with invalid data."""
        # Missing required field: shipping_address
        data = {"items": [{"product_id": products[0].id, "quantity": 5}]}

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "shipping_address" in response.data
        assert Order.objects.count() == 0

    def test_create_order_with_multiple_items(self, db, authenticated_client, products):
        """Test creating an order with multiple items."""
        # Get initial stock
        initial_stock_0 = products[0].stock
        initial_stock_1 = products[1].stock

        # Prepare order data
        data = {
            "shipping_address": "789 Test Road, Nairobi, Kenya",
            "items": [
                {"product_id": products[0].id, "quantity": 3},
                {"product_id": products[1].id, "quantity": 4},
            ],
        }

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED

        # Verify order was created with correct items
        order = Order.objects.first()
        assert order.items.count() == 2

        # Verify stock was updated for both products
        products[0].refresh_from_db()
        products[1].refresh_from_db()
        assert products[0].stock == initial_stock_0 - 3
        assert products[1].stock == initial_stock_1 - 4

    def test_create_order_with_insufficient_stock(self, db, authenticated_client, products):
        """Test creating an order with insufficient stock."""
        # Set stock lower than requested quantity
        products[0].stock = 2
        products[0].save()

        data = {
            "shipping_address": "789 Test Road, Nairobi, Kenya",
            "items": [{"product_id": products[0].id, "quantity": 5}],
        }

        url = reverse("order-list")
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "items" in response.data
        assert "Not enough stock" in str(response.data["items"][0])

        # Verify no order was created
        assert Order.objects.count() == 0

        # Verify stock was not changed
        products[0].refresh_from_db()
        assert products[0].stock == 2
