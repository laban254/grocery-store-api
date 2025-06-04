import os
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from accounts.models import User
from orders.models import Order, OrderItem


class Command(BaseCommand):
    """
    Django management command to populate the database with sample data for the grocery store.
    Creates a hierarchy of product categories, user accounts, products, and sample orders.
    """
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        """Execute the command to populate the database with sample data."""
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        self.create_categories()
        self.create_customers()
        self.create_products()
        self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
    
    def create_categories(self):
        """
        Create a hierarchical structure of product categories.
        
        Builds a four-level deep tree of categories using MPTT:
        - Root category (All Products)
        - Department categories (Bakery, Produce, etc.)
        - Subcategories (Bread, Fruits, etc.)
        - Specialized categories (Tropical Fruits, Root Vegetables, etc.)
        """
        Category.objects.all().delete()
        
        root = Category.objects.create(name='All Products', slug='all-products')
        
        bakery = Category.objects.create(name='Bakery', slug='bakery', parent=root)
        produce = Category.objects.create(name='Produce', slug='produce', parent=root)
        dairy = Category.objects.create(name='Dairy', slug='dairy', parent=root)
        meat = Category.objects.create(name='Meat', slug='meat', parent=root)
        beverages = Category.objects.create(name='Beverages', slug='beverages', parent=root)
        
        Category.objects.create(name='Bread', slug='bread', parent=bakery)
        Category.objects.create(name='Cookies', slug='cookies', parent=bakery)
        Category.objects.create(name='Cakes', slug='cakes', parent=bakery)
        Category.objects.create(name='Pastries', slug='pastries', parent=bakery)
        
        fruits = Category.objects.create(name='Fruits', slug='fruits', parent=produce)
        vegetables = Category.objects.create(name='Vegetables', slug='vegetables', parent=produce)
        
        Category.objects.create(name='Tropical Fruits', slug='tropical-fruits', parent=fruits)
        Category.objects.create(name='Berries', slug='berries', parent=fruits)
        Category.objects.create(name='Citrus', slug='citrus', parent=fruits)
        
        Category.objects.create(name='Leafy Greens', slug='leafy-greens', parent=vegetables)
        Category.objects.create(name='Root Vegetables', slug='root-vegetables', parent=vegetables)
        
        Category.objects.create(name='Milk', slug='milk', parent=dairy)
        Category.objects.create(name='Cheese', slug='cheese', parent=dairy)
        Category.objects.create(name='Yogurt', slug='yogurt', parent=dairy)
        
        Category.objects.create(name='Beef', slug='beef', parent=meat)
        Category.objects.create(name='Poultry', slug='poultry', parent=meat)
        Category.objects.create(name='Pork', slug='pork', parent=meat)
        Category.objects.create(name='Seafood', slug='seafood', parent=meat)
        
        Category.objects.create(name='Soft Drinks', slug='soft-drinks', parent=beverages)
        Category.objects.create(name='Coffee & Tea', slug='coffee-tea', parent=beverages)
        Category.objects.create(name='Juices', slug='juices', parent=beverages)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
    
    def create_customers(self):
        """
        Create sample user accounts with customer information.
        
        Creates users with Kenyan names, contact information, and addresses
        in Nairobi. Each user is created with a default password.
        """
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        
        # Sample customers data
        customers_data = [
            {'first_name': 'Kamau', 'last_name': 'Njoroge', 'email': 'kamau.njoroge@example.com', 'phone': '0712345678', 'address': '123 Kenyatta Avenue, CBD, Nairobi, Kenya'},
            {'first_name': 'Wanjiku', 'last_name': 'Muthoni', 'email': 'wanjiku.muthoni@example.com', 'phone': '0723456789', 'address': '456 Moi Avenue, CBD, Nairobi, Kenya'},
            {'first_name': 'Otieno', 'last_name': 'Odhiambo', 'email': 'otieno.odhiambo@example.com', 'phone': '0734567890', 'address': '789 Ngong Road, Kilimani, Nairobi, Kenya'},
            {'first_name': 'Akinyi', 'last_name': 'Atieno', 'email': 'akinyi.atieno@example.com', 'phone': '0745678901', 'address': '101 Kimathi Street, CBD, Nairobi, Kenya'},
            {'first_name': 'Kipchoge', 'last_name': 'Keino', 'email': 'kipchoge.keino@example.com', 'phone': '0756789012', 'address': '202 Waiyaki Way, Westlands, Nairobi, Kenya'},
        ]
        
        for data in customers_data:
            User.objects.create_user(
                username=data['email'].split('@')[0],
                email=data['email'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                address=data['address']
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.filter(is_staff=False, is_superuser=False).count()} customers'))
    
    def create_products(self):
        """
        Create realistic Kenyan grocery products for each category.
        
        Generates products for leaf categories (those without children) with:
        - Kenyan-specific product names based on category
        - Realistic prices and stock levels
        - Descriptive text indicating Kenyan origin
        """
        Product.objects.all().delete()
        
        categories = Category.objects.filter(children__isnull=True)
        
        products_data = []
        for category in categories:
            category_name = category.name.lower()
            
            for i in range(random.randint(3, 5)):
                if 'fruits' in category_name:
                    products = ['Mangoes', 'Bananas', 'Pineapples', 'Avocados', 'Passion Fruits']
                    name = f"Kenyan {products[i % len(products)]}"
                elif 'vegetables' in category_name:
                    products = ['Sukuma Wiki', 'Terere', 'Managu', 'Carrots', 'Tomatoes']
                    name = f"Fresh {products[i % len(products)]}"
                elif 'bread' in category_name:
                    products = ['Chapati', 'Mandazi', 'White Bread', 'Brown Bread', 'Buns']
                    name = f"{products[i % len(products)]}"
                elif 'milk' in category_name:
                    products = ['Fresh Milk', 'Mala', 'Yoghurt', 'Butter', 'Cream']
                    name = f"{products[i % len(products)]}"
                else:
                    name = f"{category_name.title()} Product {i+1}"
                    
                price = round(random.uniform(1.99, 99.99), 2)
                stock = random.randint(0, 100)
                
                products_data.append({
                    'name': name,
                    'slug': slugify(name),
                    'category': category,
                    'description': f"This is a quality {name.lower()} from Kenya, available in the {category.name} category.",
                    'price': price,
                    'stock': stock,
                })
        
        for data in products_data:
            Product.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Product.objects.count()} products'))
    
    def create_orders(self):
        """
        Create sample orders with random products and quantities.
        
        Each order:
        - Is assigned to a random customer
        - Contains 1-5 random products
        - Has a unique order number
        - Has a random status (pending, processing, etc.)
        - Calculates total based on product prices and quantities
        """
        Order.objects.all().delete()
        
        customers = User.objects.filter(is_staff=False, is_superuser=False)
        products = Product.objects.filter(stock__gt=0)
        
        if not customers or not products:
            self.stdout.write(self.style.WARNING('No customers or products available to create orders'))
            return
        
        for i in range(10):
            customer = random.choice(customers)
            
            order = Order.objects.create(
                user=customer,
                order_number=f"ORD-{i+1:04d}",
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                shipping_address=customer.address,
                total_amount=0  # Will update after adding items
            )
            
            order_total = 0
            num_items = random.randint(1, 5)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                order_total += price * quantity
            
            order.total_amount = order_total
            order.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {Order.objects.count()} orders with {OrderItem.objects.count()} order items'))
