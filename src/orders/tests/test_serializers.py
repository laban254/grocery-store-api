from decimal import Decimal

from django.contrib.auth import get_user_model

from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderItemCreateSerializer, OrderSerializer

User = get_user_model()


class TestOrderItemCreateSerializer:
    """Test cases for the OrderItemCreateSerializer."""

    def test_serializer_contains_expected_fields(self, db, product):
        """Test that the serializer contains the expected fields."""
        data = {"product_id": product.id, "quantity": 5}
        serializer = OrderItemCreateSerializer(data=data)
        assert serializer.is_valid()
        assert set(serializer.fields.keys()) == {"product_id", "quantity"}

    def test_serializer_validates_product_exists(self, db):
        """Test that the serializer validates that the product exists."""
        data = {"product_id": 999, "quantity": 5}  # Non-existent product ID
        serializer = OrderItemCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "product_id" in serializer.errors


class TestOrderSerializer:
    """Test cases for the OrderSerializer."""

    def test_serializer_contains_expected_fields(self, db, order):
        """Test that the serializer contains the expected fields."""
        serializer = OrderSerializer(instance=order)
        data = serializer.data
        assert set(data.keys()) == {
            "id",
            "order_number",
            "total_amount",
            "shipping_address",
            "created_at",
        }

    def test_serializer_field_content(self, db, order):
        """Test that the serializer correctly represents the order data."""
        serializer = OrderSerializer(instance=order)
        data = serializer.data
        assert data["order_number"] == "ORD-123ABC"
        assert Decimal(data["total_amount"]) == Decimal("29.90")
        assert data["shipping_address"] == "123 Test Street, Nairobi, Kenya"
        assert "created_at" in data


class TestOrderCreateSerializer:
    """Test cases for the OrderCreateSerializer."""

    def test_serializer_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        serializer = OrderCreateSerializer()
        assert set(serializer.fields.keys()) == {"shipping_address", "items"}

    def test_validate_items_empty(self, db):
        """Test validation when items array is empty."""
        data = {"shipping_address": "123 Test Street, Nairobi, Kenya", "items": []}
        serializer = OrderCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "items" in serializer.errors
        assert "An order must contain at least one item" in str(serializer.errors["items"][0])

    def test_validate_insufficient_stock(self, db, product):
        """Test validation when product stock is insufficient."""
        # Set product stock lower than requested quantity
        product.stock = 5
        product.save()

        data = {
            "shipping_address": "123 Test Street, Nairobi, Kenya",
            "items": [{"product_id": product.id, "quantity": 10}],
        }
        serializer = OrderCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert "items" in serializer.errors
        assert "Not enough stock" in str(serializer.errors["items"][0])

    def test_validate_user_without_phone(self, db, user, product, api_client):
        """Test validation when user has no phone number."""
        # Remove phone number from user
        user.phone = ""
        user.save()

        data = {
            "shipping_address": "123 Test Street, Nairobi, Kenya",
            "items": [{"product_id": product.id, "quantity": 5}],
        }

        # Need to create context with request that has user
        context = {"request": type("obj", (object,), {"user": user})}
        serializer = OrderCreateSerializer(data=data, context=context)

        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
        assert "phone number" in str(serializer.errors["non_field_errors"][0])

    def test_create_order(self, db, user, products):
        """Test creating an order with the serializer."""
        # Initial stock values
        initial_stock_0 = products[0].stock
        initial_stock_1 = products[1].stock

        data = {
            "shipping_address": "456 Test Avenue, Nairobi, Kenya",
            "items": [
                {"product_id": products[0].id, "quantity": 3},
                {"product_id": products[1].id, "quantity": 2},
            ],
        }

        # Create context with request that has user
        context = {"request": type("obj", (object,), {"user": user})}
        serializer = OrderCreateSerializer(data=data, context=context)

        assert serializer.is_valid(), serializer.errors
        order = serializer.save()

        # Check order was created correctly
        assert isinstance(order, Order)
        assert order.user == user
        assert order.shipping_address == "456 Test Avenue, Nairobi, Kenya"
        assert order.items.count() == 2

        # Expected total amount
        expected_total = (products[0].price * 3) + (products[1].price * 2)
        assert order.total_amount == expected_total

        # Check stock levels were updated
        products[0].refresh_from_db()
        products[1].refresh_from_db()
        assert products[0].stock == initial_stock_0 - 3
        assert products[1].stock == initial_stock_1 - 2
