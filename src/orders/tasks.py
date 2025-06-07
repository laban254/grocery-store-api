from celery import shared_task

from .models import Order
from .services import send_sms


@shared_task
def send_order_confirmation_sms(order_id):
    """
    Celery task to send SMS notification for a new order.

    Args:
        order_id (int): The ID of the newly created order
    """
    try:
        order = Order.objects.get(id=order_id)
        name = order.user.first_name or "Customer"
        num = order.order_number

        message = f"Hi {name}, order #{num} confirmed. Thanks!"

        phone_number = order.user.phone
        if phone_number:
            return send_sms(phone_number, message)

        return {"status": "error", "message": "No phone number available for customer"}

    except Order.DoesNotExist:
        return {"status": "error", "message": f"Order {order_id} not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@shared_task
def send_order_status_update_sms(order_id, status):
    """
    Celery task to send SMS notification when order status changes.

    Args:
        order_id (int): The ID of the order
        status (str): The new status of the order
    """
    try:
        order = Order.objects.get(id=order_id)

        name = order.user.first_name or "Customer"
        num = order.order_number

        msgs = {
            "processing": f"Hi {name}, order #{num} processing.",
            "shipped": f"Hi {name}, order #{num} shipped!",
            "delivered": f"Hi {name}, order #{num} delivered!",
            "cancelled": f"Hi {name}, order #{num} cancelled.",
        }

        message = msgs.get(status, f"Hi {name}, order #{num}: {status}.")

        phone_number = order.user.phone
        if phone_number:
            return send_sms(phone_number, message)

        return {"status": "error", "message": "No phone number available for customer"}

    except Order.DoesNotExist:
        return {"status": "error", "message": f"Order {order_id} not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
