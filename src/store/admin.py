from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Category, Customer, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Admin interface for Category model with drag-and-drop functionality
    for managing the hierarchical structure.
    """
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    """
    list_display = ('full_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address', {
            'fields': ('address',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.
    """
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at')
    list_filter = ('available', 'category', 'created_at')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Inventory', {
            'fields': ('price', 'stock', 'available', 'sku')
        }),
    )


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
