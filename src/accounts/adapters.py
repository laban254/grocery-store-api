from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db import transaction
from .models import Customer


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social accounts that links OIDC users to Customer records.
    """
    def save_user(self, request, sociallogin, form=None):
        """
        Save the user and create/link a Customer record.
        """
        with transaction.atomic():
            # First, save the user using the default adapter
            user = super().save_user(request, sociallogin, form)
            
            # Get user info from the social account
            user_data = sociallogin.account.extra_data
            
            # Store OIDC-specific information
            user.oidc_id = sociallogin.account.uid
            user.oidc_provider = sociallogin.account.provider
            user.save()
            
            # Try to find an existing customer with the same email
            try:
                customer = Customer.objects.get(email=user.email)
                # Link the customer to the user if found
                customer.user = user
                customer.save()
            except Customer.DoesNotExist:
                # Create a new customer if one doesn't exist
                first_name = user_data.get('given_name', user.first_name)
                last_name = user_data.get('family_name', user.last_name)
                
                Customer.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=user.email
                )
                
        return user
