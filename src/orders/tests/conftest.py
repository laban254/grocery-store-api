from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from orders.models import Order, OrderItem
from products.models import Category, Product

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="User",
        phone="+254722000000",
        address="123 Test Street, Nairobi, Kenya",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def category():
    """Create a test category."""
    return Category.objects.create(name="Groceries", slug="groceries")


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
def products(category):
    """Create multiple products for testing."""
    products = [
        Product.objects.create(
            name="Apple",
            slug="apple",
            category=category,
            description="Fresh red apples",
            price=Decimal("2.99"),
            stock=100,
        ),
        Product.objects.create(
            name="Banana",
            slug="banana",
            category=category,
            description="Yellow bananas",
            price=Decimal("1.99"),
            stock=150,
        ),
        Product.objects.create(
            name="Orange",
            slug="orange",
            category=category,
            description="Juicy oranges",
            price=Decimal("3.49"),
            stock=80,
        ),
    ]
    return products


@pytest.fixture
def order(user, product):
    """Create a test order."""
    order = Order.objects.create(
        user=user,
        order_number="ORD-123ABC",
        status="pending",
        total_amount=Decimal("29.90"),
        shipping_address="123 Test Street, Nairobi, Kenya",
    )

    # Create order item
    OrderItem.objects.create(order=order, product=product, quantity=10, price=product.price)

    return order


@pytest.fixture
def orders(user, products):
    """Create multiple orders for testing."""
    orders = []

    # Create first order with one item
    order1 = Order.objects.create(
        user=user,
        order_number="ORD-123ABC",
        status="pending",
        total_amount=Decimal("29.90"),
        shipping_address="123 Test Street, Nairobi, Kenya",
    )

    OrderItem.objects.create(
        order=order1, product=products[0], quantity=10, price=products[0].price
    )

    orders.append(order1)

    # Create second order with multiple items
    order2 = Order.objects.create(
        user=user,
        order_number="ORD-456DEF",
        status="processing",
        total_amount=Decimal("42.85"),
        shipping_address="456 Test Avenue, Nairobi, Kenya",
    )

    OrderItem.objects.create(order=order2, product=products[1], quantity=5, price=products[1].price)

    OrderItem.objects.create(order=order2, product=products[2], quantity=7, price=products[2].price)

    orders.append(order2)

    return orders
