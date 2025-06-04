from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta

from products.models import Product, Category
from orders.models import Order, OrderItem
from accounts.models import User


class GroceryAdminSite(admin.AdminSite):
    """
    Custom admin site for Grocery API with custom branding and dashboard.
    """
    # Branding
    site_header = _("Grocery Store Management")
    site_title = _("Grocery Admin")
    index_title = _("Dashboard")
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        """
        Override the index view to add dashboard statistics
        """
        # Get basic statistics
        context = extra_context or {}
        
        # Product stats
        total_products = Product.objects.count()
        low_stock_products = Product.objects.filter(stock__lte=5).count()
        out_of_stock_products = Product.objects.filter(stock=0).count()
        
        # Order stats
        recent_orders = Order.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        pending_orders = Order.objects.filter(status='pending').count()
        
        # Sales stats for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        monthly_sales = Order.objects.filter(
            created_at__gte=thirty_days_ago,
            status__in=['processing', 'shipped', 'delivered']
        ).aggregate(
            total_sales=Sum('total_amount'),
            order_count=Count('id'),
            avg_order_value=Avg('total_amount')
        )
        
        # User stats
        total_users = User.objects.filter(is_staff=False).count()
        new_users = User.objects.filter(
            created_at__gte=thirty_days_ago,
            is_staff=False
        ).count()
        
        context.update({
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'recent_orders': recent_orders,
            'pending_orders': pending_orders,
            'monthly_sales': monthly_sales,
            'total_users': total_users,
            'new_users': new_users,
        })
        
        return super().index(request, context)
    
    def dashboard_view(self, request):
        """
        Custom dashboard view with more detailed statistics and charts
        """
        # Date ranges
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Daily orders for the last 30 days
        daily_orders = Order.objects.filter(
            created_at__date__gte=thirty_days_ago
        ).annotate(
            day=TruncDay('created_at')
        ).values('day').annotate(
            count=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('day')
        
        # Top selling products
        top_products = OrderItem.objects.values(
            'product__name'
        ).annotate(
            total_sold=Sum('quantity'),
            revenue=Sum('price')
        ).order_by('-total_sold')[:10]
        
        # Top categories
        top_categories = OrderItem.objects.values(
            'product__category__name'
        ).annotate(
            total_sold=Sum('quantity'),
            revenue=Sum('price')
        ).order_by('-total_sold')[:5]
        
        # Inventory status
        inventory_status = {
            'in_stock': Product.objects.filter(stock__gt=5).count(),
            'low_stock': Product.objects.filter(stock__gt=0, stock__lte=5).count(),
            'out_of_stock': Product.objects.filter(stock=0).count(),
        }
        
        return render(request, 'admin/dashboard.html', {
            'title': 'Dashboard',
            'daily_orders': daily_orders,
            'top_products': top_products,
            'top_categories': top_categories,
            'inventory_status': inventory_status,
        })


# Create custom admin site instance
grocery_admin_site = GroceryAdminSite(name='grocery_admin')
