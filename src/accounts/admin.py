from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for custom User model.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('OpenID Connect Information', {'fields': ('oidc_id', 'oidc_provider')}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    """
    list_display = ('full_name', 'email', 'phone', 'created_at', 'user')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address',)
        }),
    )
