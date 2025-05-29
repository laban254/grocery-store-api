from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category


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
