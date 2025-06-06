from decimal import Decimal

from orders.models import Order, OrderItem


class TestOrderModel:
    """Test cases for the Order model."""

    def test_order_creation(self, db, order, user):
        """Test that an order can be created successfully."""
        assert Order.objects.count() == 1
        assert order.user == user
        assert order.order_number == "ORD-123ABC"
        assert order.status == "pending"
        assert order.total_amount == Decimal("29.90")
        assert order.shipping_address == "123 Test Street, Nairobi, Kenya"
        assert order.created_at is not None
        assert order.updated_at is not None

    def test_order_str_representation(self, db, order):
        """Test the string representation of an order."""
        assert str(order) == "Order ORD-123ABC"

    def test_order_items_relationship(self, db, order, product):
        """Test the relationship between orders and order items."""
        items = order.items.all()
        assert items.count() == 1

        item = items.first()
        assert item.product == product
        assert item.quantity == 10
        assert item.price == product.price

    def test_order_status_choices(self, db, user):
        """Test that order status is limited to choices."""
        order = Order.objects.create(
            user=user,
            order_number="ORD-TEST123",
            status="processing",
            total_amount=Decimal("19.99"),
            shipping_address="Test Address",
        )
        assert order.status == "processing"

        valid_statuses = ["pending", "shipped", "delivered", "cancelled"]
        for status in valid_statuses:
            order.status = status
            order.save()
            assert order.status == status

    def test_order_meta_ordering(self, db, orders):
        """Test that orders are ordered by created_at in descending order."""
        db_orders = list(Order.objects.all())
        assert db_orders[0].order_number == orders[1].order_number
        assert db_orders[1].order_number == orders[0].order_number


class TestOrderItemModel:
    """Test cases for the OrderItem model."""

    def test_orderitem_creation(self, db, order, product):
        """Test that an order item can be created successfully."""
        items = OrderItem.objects.filter(order=order)
        assert items.count() == 1

        item = items.first()
        assert item.product == product
        assert item.quantity == 10
        assert item.price == product.price

    def test_orderitem_str_representation(self, db, order):
        """Test the string representation of an order item."""
        item = order.items.first()
        assert str(item) == f"10x {item.product.name}"

    def test_orderitem_subtotal_property(self, db, order):
        """Test the subtotal property of an order item."""
        item = order.items.first()
        expected_subtotal = item.price * item.quantity
        assert item.subtotal == expected_subtotal

    def test_order_with_multiple_items(self, db, orders, products):
        """Test an order with multiple items."""
        order = orders[1]
        items = order.items.all()

        assert items.count() == 2

        # Check each item
        products_in_order = [item.product for item in items]
        assert products[1] in products_in_order
        assert products[2] in products_in_order
