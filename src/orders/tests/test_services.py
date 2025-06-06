from unittest.mock import patch

from orders.services import send_sms


class TestSmsService:
    """Test cases for the SMS service."""

    @patch("orders.services.sms_service")
    @patch("orders.services.logger")
    def test_send_sms_success(self, mock_logger, mock_sms_service):
        """Test sending SMS successfully."""
        # Setup mock
        mock_response = {"SMSMessageData": {"Recipients": [{"status": "Success"}]}}
        mock_sms_service.send.return_value = mock_response

        # Call function
        phone_number = "+254722000000"
        message = "Test SMS message"
        result = send_sms(phone_number, message)

        # Assert
        mock_sms_service.send.assert_called_once_with(message, [phone_number])
        mock_logger.info.assert_called_once()

        assert result["status"] == "success"
        assert result["response"] == mock_response

    @patch("orders.services.sms_service")
    @patch("orders.services.logger")
    def test_send_sms_failure(self, mock_logger, mock_sms_service):
        """Test sending SMS with failure."""
        # Setup mock to raise exception
        mock_sms_service.send.side_effect = Exception("API Error")

        # Call function
        phone_number = "+254722000000"
        message = "Test SMS message"
        result = send_sms(phone_number, message)

        # Assert
        mock_sms_service.send.assert_called_once_with(message, [phone_number])
        mock_logger.error.assert_called_once()

        assert result["status"] == "error"
        assert result["message"] == "API Error"
