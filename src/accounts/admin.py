from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for custom User model that combines authentication and customer information.
    """
    list_display = ('email', 'username', 'full_name', 'phone', 'is_staff', 'created_at')
    ordering = ('email',)
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'address')
    list_filter = ('is_staff', 'is_active', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'phone', 'address')}),
        (_('Authentication'), {'fields': ('oidc_id', 'oidc_provider')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def full_name(self, obj):
        return obj.get_full_name() or "-"
    full_name.short_description = _('Full Name')
