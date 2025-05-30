from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItems within Orders.
    """
    model = OrderItem
    extra = 1
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.
    """
    list_display = ('order_number', 'get_user_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__first_name', 'user__last_name', 'user__email')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'order_number', 'status')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'shipping_address')
        }),
    )

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
    get_user_name.short_description = 'User'
    get_user_name.admin_order_field = 'user__email'
