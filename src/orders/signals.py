from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import send_order_status_update_sms


@receiver(post_save, sender=Order)
def order_status_change_handler(sender, instance, created, **kwargs):
    """
    Signal handler to track order status changes and send SMS notifications.

    Args:
        sender: The model class (Order)
        instance: The actual order instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    if not created and hasattr(instance, "_original_status"):
        if instance._original_status != instance.status:
            send_order_status_update_sms.delay(instance.id, instance.status)
