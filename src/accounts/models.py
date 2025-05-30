from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model that combines authentication and customer information.
    """
    oidc_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    oidc_provider = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make email required and unique
    email = models.EmailField(_('email address'), unique=True)
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username still required by Django admin
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return self.get_full_name() or self.email
        
    @property
    def full_name(self):
        return self.get_full_name()
