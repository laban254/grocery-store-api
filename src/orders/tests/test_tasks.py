from unittest.mock import patch

from orders.tasks import send_order_confirmation_sms, send_order_status_update_sms


class TestOrderTasks:
    """Test cases for Celery tasks in the orders app."""

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms(self, mock_send_sms, db, order):
        """Test the order confirmation SMS task."""
        # Setup mock
        mock_send_sms.return_value = {"status": "success", "response": "test_response"}

        # Call task
        result = send_order_confirmation_sms(order.id)

        # Assertions
        assert mock_send_sms.called
        # Check that the phone number and a message were passed to send_sms
        call_args = mock_send_sms.call_args[0]
        assert call_args[0] == order.user.phone  # Phone number
        assert order.order_number in call_args[1]  # Message contains order number
        # The message format has changed, so we check for basic elements instead
        assert order.user.first_name in call_args[1]  # Contains user's name

        # Check return value
        assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_no_phone(self, mock_send_sms, db, order):
        """Test the order confirmation SMS task when user has no phone number."""
        # Remove phone number
        order.user.phone = ""
        order.user.save()

        # Call task
        result = send_order_confirmation_sms(order.id)

        # Assertions
        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "No phone number" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_nonexistent_order(self, mock_send_sms, db):
        """Test the order confirmation SMS task with a nonexistent order ID."""
        # Call task with non-existent order ID
        result = send_order_confirmation_sms(999)

        # Assertions
        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "Order" in result["message"] and "not found" in result["message"]

    @patch("orders.tasks.Order.objects.get")
    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_exception(self, mock_send_sms, mock_get):
        """Test the order confirmation SMS task when an exception occurs."""
        # Setup mock to raise exception
        mock_get.side_effect = Exception("Test exception")

        # Call task
        result = send_order_confirmation_sms(1)

        # Assertions
        assert result["status"] == "error"
        assert "Test exception" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms(self, mock_send_sms, db, order):
        """Test the order status update SMS task."""
        # Setup mock
        mock_send_sms.return_value = {"status": "success", "response": "test_response"}

        # Call task with "shipped" status
        result = send_order_status_update_sms(order.id, "shipped")

        # Assertions
        assert mock_send_sms.called
        # Check that the phone number and a message were passed to send_sms
        call_args = mock_send_sms.call_args[0]
        assert call_args[0] == order.user.phone  # Phone number
        assert order.order_number in call_args[1]  # Message contains order number
        assert "shipped" in call_args[1].lower()  # Message contains the status

        # Check return value
        assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_all_statuses(self, mock_send_sms, db, order):
        """Test the order status update SMS task with all possible statuses."""
        # Test all status messages
        statuses = ["processing", "shipped", "delivered", "cancelled"]

        for status in statuses:
            # Reset mock
            mock_send_sms.reset_mock()
            mock_send_sms.return_value = {"status": "success", "response": "test_response"}

            # Call task
            result = send_order_status_update_sms(order.id, status)

            # Assertions
            assert mock_send_sms.called
            message = mock_send_sms.call_args[0][1]  # Get the message
            assert order.order_number in message

            # Check return value
            assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_no_phone(self, mock_send_sms, db, order):
        """Test the order status update SMS task when user has no phone number."""
        # Remove phone number
        order.user.phone = ""
        order.user.save()

        # Call task
        result = send_order_status_update_sms(order.id, "shipped")

        # Assertions
        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "No phone number" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_nonexistent_order(self, mock_send_sms, db):
        """Test the order status update SMS task with a nonexistent order ID."""
        # Call task with non-existent order ID
        result = send_order_status_update_sms(999, "shipped")

        # Assertions
        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "Order" in result["message"] and "not found" in result["message"]
