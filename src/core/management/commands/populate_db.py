import os
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product
from accounts.models import User
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Create categories
        self.create_categories()
        
        # Create customers
        self.create_customers()
        
        # Create products
        self.create_products()
        
        # Create orders
        self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
    
    def create_categories(self):
        # Clear existing categories
        Category.objects.all().delete()
        
        # Create root category
        root = Category.objects.create(name='All Products', slug='all-products')
        
        # Create second level categories
        bakery = Category.objects.create(name='Bakery', slug='bakery', parent=root)
        produce = Category.objects.create(name='Produce', slug='produce', parent=root)
        dairy = Category.objects.create(name='Dairy', slug='dairy', parent=root)
        meat = Category.objects.create(name='Meat', slug='meat', parent=root)
        beverages = Category.objects.create(name='Beverages', slug='beverages', parent=root)
        
        # Create third level categories
        # Bakery subcategories
        Category.objects.create(name='Bread', slug='bread', parent=bakery)
        Category.objects.create(name='Cookies', slug='cookies', parent=bakery)
        Category.objects.create(name='Cakes', slug='cakes', parent=bakery)
        Category.objects.create(name='Pastries', slug='pastries', parent=bakery)
        
        # Produce subcategories
        fruits = Category.objects.create(name='Fruits', slug='fruits', parent=produce)
        vegetables = Category.objects.create(name='Vegetables', slug='vegetables', parent=produce)
        
        # Fruits subcategories (fourth level)
        Category.objects.create(name='Tropical Fruits', slug='tropical-fruits', parent=fruits)
        Category.objects.create(name='Berries', slug='berries', parent=fruits)
        Category.objects.create(name='Citrus', slug='citrus', parent=fruits)
        
        # Vegetables subcategories (fourth level)
        Category.objects.create(name='Leafy Greens', slug='leafy-greens', parent=vegetables)
        Category.objects.create(name='Root Vegetables', slug='root-vegetables', parent=vegetables)
        
        # Dairy subcategories
        Category.objects.create(name='Milk', slug='milk', parent=dairy)
        Category.objects.create(name='Cheese', slug='cheese', parent=dairy)
        Category.objects.create(name='Yogurt', slug='yogurt', parent=dairy)
        
        # Meat subcategories
        Category.objects.create(name='Beef', slug='beef', parent=meat)
        Category.objects.create(name='Poultry', slug='poultry', parent=meat)
        Category.objects.create(name='Pork', slug='pork', parent=meat)
        Category.objects.create(name='Seafood', slug='seafood', parent=meat)
        
        # Beverages subcategories
        Category.objects.create(name='Soft Drinks', slug='soft-drinks', parent=beverages)
        Category.objects.create(name='Coffee & Tea', slug='coffee-tea', parent=beverages)
        Category.objects.create(name='Juices', slug='juices', parent=beverages)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
    
    def create_customers(self):
        # Clear existing customers
        Customer.objects.all().delete()
        
        # Sample customers data
        customers_data = [
            {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'phone': '555-123-4567', 'address': '123 Main St, Anytown, USA'},
            {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane.smith@example.com', 'phone': '555-987-6543', 'address': '456 Oak Ave, Somewhere, USA'},
            {'first_name': 'Michael', 'last_name': 'Johnson', 'email': 'michael.johnson@example.com', 'phone': '555-567-8901', 'address': '789 Pine Rd, Nowhere, USA'},
            {'first_name': 'Emily', 'last_name': 'Williams', 'email': 'emily.williams@example.com', 'phone': '555-234-5678', 'address': '101 Maple St, Everywhere, USA'},
            {'first_name': 'Robert', 'last_name': 'Brown', 'email': 'robert.brown@example.com', 'phone': '555-345-6789', 'address': '202 Cedar Ave, Anywhere, USA'},
        ]
        
        for data in customers_data:
            Customer.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Customer.objects.count()} customers'))
    
    def create_products(self):
        # Clear existing products
        Product.objects.all().delete()
        
        # Get all leaf categories
        categories = Category.objects.filter(children__isnull=True)
        
        # Product data - just sample products for each category
        products_data = []
        for category in categories:
            category_name = category.name.lower()
            
            # Create 3-5 products per category
            for i in range(random.randint(3, 5)):
                name = f"{category_name.title()} Product {i+1}"
                price = round(random.uniform(1.99, 99.99), 2)
                stock = random.randint(0, 100)
                sku = f"{category_name[:3].upper()}{i+1:03d}"
                
                products_data.append({
                    'name': name,
                    'slug': slugify(name),
                    'category': category,
                    'description': f"This is a sample {name.lower()} in the {category.name} category.",
                    'price': price,
                    'stock': stock,
                    'available': stock > 0,
                    'sku': sku
                })
        
        for data in products_data:
            Product.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Product.objects.count()} products'))
    
    def create_orders(self):
        # Clear existing orders
        Order.objects.all().delete()
        
        # Get all customers and products
        customers = Customer.objects.all()
        products = Product.objects.filter(available=True)
        
        if not customers or not products:
            self.stdout.write(self.style.WARNING('No customers or products available to create orders'))
            return
        
        # Create 10 sample orders
        for i in range(10):
            # Select a random customer
            customer = random.choice(customers)
            
            # Create order
            order = Order.objects.create(
                customer=customer,
                order_number=f"ORD-{i+1:04d}",
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                shipping_address=customer.address,
                total_amount=0  # Will update after adding items
            )
            
            # Add 1-5 random products to the order
            order_total = 0
            num_items = random.randint(1, 5)
            selected_products = random.sample(list(products), min(num_items, len(products)))
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price  # Use the product's current price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                order_total += price * quantity
            
            # Update order total
            order.total_amount = order_total
            order.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {Order.objects.count()} orders with {OrderItem.objects.count()} order items'))
