from unittest.mock import patch

from orders.models import Order


class TestOrderSignals:
    """Test cases for the Order model signals."""

    @patch("orders.signals.send_order_status_update_sms")
    def test_status_change_signal(self, mock_task, db, order):
        """Test that changing an order's status triggers the signal."""
        # Change the order status
        order.status = "shipped"
        order.save()

        # Verify the task was called with correct arguments
        mock_task.delay.assert_called_once_with(order.id, "shipped")

    @patch("orders.signals.send_order_status_update_sms")
    def test_no_status_change_no_signal(self, mock_task, db, order):
        """Test that signal is not triggered when status doesn't change."""
        # Save without changing status
        order.shipping_address = "Updated address"  # Change another field
        order.save()

        # Verify the task was not called
        mock_task.delay.assert_not_called()

    @patch("orders.signals.send_order_status_update_sms")
    def test_signal_with_new_order(self, mock_task, db, user):
        """Test that signal is not triggered for new orders."""
        # Create a new order
        Order.objects.create(
            user=user,
            order_number="ORD-TEST123",
            status="pending",
            total_amount=19.99,
            shipping_address="Test Address",
        )

        # Verify the task was not called (creation doesn't count as status change)
        mock_task.delay.assert_not_called()

    @patch("orders.signals.send_order_status_update_sms")
    def test_multiple_status_changes(self, mock_task, db, order):
        """Test multiple status changes trigger the signal each time."""
        # Change status multiple times
        statuses = ["processing", "shipped", "delivered"]

        for status in statuses:
            # Reset mock for each status change
            mock_task.delay.reset_mock()

            # Change the status
            order.status = status
            order.save()

            # Verify the task was called with the correct status
            mock_task.delay.assert_called_once_with(order.id, status)
