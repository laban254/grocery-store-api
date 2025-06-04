import logging
import africastalking
from django.conf import settings

username = settings.AFRICAS_TALKING_USERNAME
api_key = settings.AFRICAS_TALKING_API_KEY
africastalking.initialize(username, api_key)

sms_service = africastalking.SMS

logger = logging.getLogger('customer_orders') 

def send_sms(phone_number, message):
    """
    Sends an SMS using Africa's Talking API.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The message content to be sent.

    Returns:
        dict: A dictionary containing the status and response from Africa's Talking.
    """
    try:
        response = sms_service.send(message, [phone_number])
        logger.info('SMS sent successfully to %s: %s', phone_number, message)
        return {"status": "success", "response": response}
    
    except Exception as e:
        logger.error('Failed to send SMS to %s: %s', phone_number, str(e))
        return {"status": "error", "message": str(e)}