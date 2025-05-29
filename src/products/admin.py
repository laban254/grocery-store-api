from django.contrib import admin
from .models import Product


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
