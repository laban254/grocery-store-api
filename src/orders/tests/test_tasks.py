from unittest.mock import patch

from orders.tasks import send_order_confirmation_sms, send_order_status_update_sms


class TestOrderTasks:
    """Test cases for Celery tasks in the orders app."""

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms(self, mock_send_sms, db, order):
        """Test the order confirmation SMS task."""
        mock_send_sms.return_value = {"status": "success", "response": "test_response"}

        result = send_order_confirmation_sms(order.id)

        assert mock_send_sms.called
        call_args = mock_send_sms.call_args[0]
        assert call_args[0] == order.user.phone
        assert order.order_number in call_args[1]
        assert order.user.first_name in call_args[1]

        assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_no_phone(self, mock_send_sms, db, order):
        """Test the order confirmation SMS task when user has no phone number."""
        order.user.phone = ""
        order.user.save()

        result = send_order_confirmation_sms(order.id)

        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "No phone number" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_nonexistent_order(self, mock_send_sms, db):
        """Test the order confirmation SMS task with a nonexistent order ID."""
        result = send_order_confirmation_sms(999)

        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "Order" in result["message"] and "not found" in result["message"]

    @patch("orders.tasks.Order.objects.get")
    @patch("orders.tasks.send_sms")
    def test_send_order_confirmation_sms_exception(self, mock_send_sms, mock_get):
        """Test the order confirmation SMS task when an exception occurs."""
        mock_get.side_effect = Exception("Test exception")

        result = send_order_confirmation_sms(1)

        assert result["status"] == "error"
        assert "Test exception" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms(self, mock_send_sms, db, order):
        """Test the order status update SMS task."""
        mock_send_sms.return_value = {"status": "success", "response": "test_response"}

        result = send_order_status_update_sms(order.id, "shipped")

        assert mock_send_sms.called
        call_args = mock_send_sms.call_args[0]
        assert call_args[0] == order.user.phone
        assert order.order_number in call_args[1]
        assert "shipped" in call_args[1].lower()

        assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_all_statuses(self, mock_send_sms, db, order):
        """Test the order status update SMS task with all possible statuses."""
        statuses = ["processing", "shipped", "delivered", "cancelled"]

        for status in statuses:
            mock_send_sms.reset_mock()
            mock_send_sms.return_value = {"status": "success", "response": "test_response"}

            result = send_order_status_update_sms(order.id, status)

            assert mock_send_sms.called
            message = mock_send_sms.call_args[0][1]
            assert order.order_number in message

            assert result["status"] == "success"

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_no_phone(self, mock_send_sms, db, order):
        """Test the order status update SMS task when user has no phone number."""
        order.user.phone = ""
        order.user.save()

        result = send_order_status_update_sms(order.id, "shipped")

        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "No phone number" in result["message"]

    @patch("orders.tasks.send_sms")
    def test_send_order_status_update_sms_nonexistent_order(self, mock_send_sms, db):
        """Test the order status update SMS task with a nonexistent order ID."""
        result = send_order_status_update_sms(999, "shipped")

        assert not mock_send_sms.called
        assert result["status"] == "error"
        assert "Order" in result["message"] and "not found" in result["message"]
