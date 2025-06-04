from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for OrderItems within Orders.
    """
    model = OrderItem
    extra = 1
    raw_id_fields = ('product',)
    readonly_fields = ('price',)
    autocomplete_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.
    """
    list_display = ('order_number', 'get_user_name', 'status_colored', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__first_name', 'user__last_name', 'user__email', 'shipping_address')
    readonly_fields = ('order_number', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'order_number', 'status')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'shipping_address', 'created_at', 'updated_at')
        }),
    )
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.email
    get_user_name.short_description = 'Customer'
    get_user_name.admin_order_field = 'user__email'
    
    def status_colored(self, obj):
        colors = {
            'pending': '#FF8C00',      # Dark Orange
            'processing': '#1E90FF',   # Dodger Blue
            'shipped': '#9370DB',      # Medium Purple
            'delivered': '#2E8B57',    # Sea Green
            'cancelled': '#DC143C',    # Crimson
        }
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as delivered"
