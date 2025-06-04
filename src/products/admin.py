from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    Admin interface for Category model using MPTT for hierarchical display.
    """

    list_display = ("name", "slug", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("parent",)
    mptt_level_indent = 20
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model.
    """

    list_display = ("name", "category", "price", "stock", "stock_status", "created_at")
    list_filter = ("category", "created_at")
    list_editable = ("price", "stock")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["category"]
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "description")}),
        ("Inventory", {"fields": ("price", "stock")}),
    )

    def stock_status(self, obj):
        if obj.stock <= 0:
            return "❌ Out of stock"
        elif obj.stock <= 5:
            return "⚠️ Low stock"
        else:
            return "✅ In stock"

    stock_status.short_description = "Stock Status"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all().order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
