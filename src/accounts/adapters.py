from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db import transaction


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social accounts that handles OIDC authentication.
    """

    def save_user(self, request, sociallogin, form=None):
        """
        Save the user with OIDC information.
        """
        with transaction.atomic():
            user = super().save_user(request, sociallogin, form)

            user_data = sociallogin.account.extra_data

            user.oidc_id = sociallogin.account.uid
            user.oidc_provider = sociallogin.account.provider

            first_name = user_data.get("given_name", user.first_name)
            last_name = user_data.get("family_name", user.last_name)

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            user.save()

        return user
