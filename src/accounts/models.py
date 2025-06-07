from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model that combines authentication and customer information.
    """

    oidc_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    oidc_provider = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(
        max_length=15,
        blank=True,
        help_text="Phone number in international format (e.g., +254722000000)",
    )
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def full_name(self):
        return self.get_full_name()

    def clean(self):
        """Validate and format phone number"""
        if self.phone:
            cleaned_phone = "".join(filter(str.isdigit, self.phone))

            if cleaned_phone.startswith("0"):
                cleaned_phone = "254" + cleaned_phone[1:]

            if not self.phone.startswith("+"):
                cleaned_phone = "+" + cleaned_phone

            self.phone = cleaned_phone

        super().clean()
