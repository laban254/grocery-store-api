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
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer__first_name', 'customer__last_name', 'customer__email')
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('customer', 'order_number', 'status')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'shipping_address')
        }),
    )
