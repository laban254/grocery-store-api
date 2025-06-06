from unittest.mock import patch

from orders.models import Order


class TestOrderSignals:
    """Test cases for the Order model signals."""

    @patch("orders.signals.send_order_status_update_sms")
    def test_status_change_signal(self, mock_task, db, order):
        """Test that changing an order's status triggers the signal."""
        order.status = "shipped"
        order.save()

        mock_task.delay.assert_called_once_with(order.id, "shipped")

    @patch("orders.signals.send_order_status_update_sms")
    def test_no_status_change_no_signal(self, mock_task, db, order):
        """Test that signal is not triggered when status doesn't change."""
        order.shipping_address = "Updated address"
        order.save()

        mock_task.delay.assert_not_called()

    @patch("orders.signals.send_order_status_update_sms")
    def test_signal_with_new_order(self, mock_task, db, user):
        """Test that signal is not triggered for new orders."""
        Order.objects.create(
            user=user,
            order_number="ORD-TEST123",
            status="pending",
            total_amount=19.99,
            shipping_address="Test Address",
        )

        mock_task.delay.assert_not_called()

    @patch("orders.signals.send_order_status_update_sms")
    def test_multiple_status_changes(self, mock_task, db, order):
        """Test multiple status changes trigger the signal each time."""
        statuses = ["processing", "shipped", "delivered"]

        for status in statuses:
            mock_task.delay.reset_mock()

            order.status = status
            order.save()

            mock_task.delay.assert_called_once_with(order.id, status)
