from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added

from .models import User


@receiver(social_account_added)
def handle_social_account_added(request, sociallogin, **kwargs):
    """
    Signal handler to update User when a social account is added.
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
