from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from allauth.socialaccount.signals import social_account_added

from .models import User, Customer


@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Customer when a User is saved.
    """
    if created:  # Only for newly created users
        # Check if a customer with this email already exists
        try:
            customer = Customer.objects.get(email=instance.email)
            # Link the customer to the user
            customer.user = instance
            customer.save()
        except Customer.DoesNotExist:
            # Create a new customer for this user
            Customer.objects.create(
                user=instance,
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name
            )
    elif not created and instance.email:
        # For existing users, update the email if it changed
        try:
            customer = Customer.objects.get(user=instance)
            if customer.email != instance.email:
                customer.email = instance.email
                customer.save()
        except Customer.DoesNotExist:
            pass


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    """
    Signal handler to update User and Customer when a social account is added.
    """
    user = sociallogin.user
    user_data = sociallogin.account.extra_data
    
    # Update OIDC-specific information
    user.oidc_id = sociallogin.account.uid
    user.oidc_provider = sociallogin.account.provider
    
    # Update user fields from social account data if available
    if 'given_name' in user_data and not user.first_name:
        user.first_name = user_data['given_name']
    if 'family_name' in user_data and not user.last_name:
        user.last_name = user_data['family_name']
    
    user.save()
    
    # Ensure there's a customer record
    try:
        customer = Customer.objects.get(user=user)
        # Update customer fields if they're blank
        if not customer.first_name and user.first_name:
            customer.first_name = user.first_name
        if not customer.last_name and user.last_name:
            customer.last_name = user.last_name
        customer.save()
    except Customer.DoesNotExist:
        # The post_save signal on User should have created a Customer,
        # but just in case, we create one here
        Customer.objects.create(
            user=user,
            email=user.email,
            first_name=user.first_name or '',
            last_name=user.last_name or ''
        )
