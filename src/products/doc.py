"""
Products App Schema Documentation

This module documents the database schema for the products app,
which manages product categories and product items in the grocery store.

Models:
-------

Category:
    A hierarchical model for organizing products using MPTT (Modified Preorder Tree Traversal).
    This allows for unlimited nesting of categories (e.g., Produce > Fruits > Citrus).

    Fields:
    - name (CharField): Unique name of the category (max_length=100)
    - slug (SlugField): URL-friendly version of the name (max_length=120, unique)
    - parent (TreeForeignKey): Self-reference for hierarchical structure
        - Can be null/blank for top-level categories
        - Related name: 'children'

    Methods:
    - __str__(): Returns the name of the category
    - save(): Automatically generates slug from name if not provided

    Meta:
    - MPTT options: Categories are ordered by name
    - Provides tree traversal methods: get_descendants(), get_ancestors(), etc.

Product:
    Represents items available for purchase in the grocery store.
    
    Fields:
    - name (CharField): Product name (max_length=200)
    - slug (SlugField): URL-friendly version of the name (max_length=220, unique)
    - category (TreeForeignKey): Link to the Category model
        - Related name: 'products'
    - description (TextField): Optional product description
    - price (DecimalField): Product price (max_digits=10, decimal_places=2)
    - stock (PositiveIntegerField): Current inventory quantity (default=0)
    - created_at (DateTimeField): When the product was added
    - updated_at (DateTimeField): When the product was last modified

    Methods:
    - __str__(): Returns the name of the product
    - save(): Automatically generates slug from name if not provided

    Meta:
    - Products are ordered by name

Relationships:
-------------
1. Category (parent) <--> Category (children): One-to-many self-reference 
   - A category can have multiple child categories
   - A category can have at most one parent category

2. Category <--> Product: One-to-many relationship
   - A category can have multiple products
   - A product belongs to exactly one category

Example Hierarchical Structure:
------------------------------
- All Products (parent=None)
    - Bakery (parent=All Products)
        - Bread (parent=Bakery)
        - Cookies (parent=Bakery)
    - Produce (parent=All Products)
        - Fruits (parent=Produce)
            - Apples (parent=Fruits)
            - Citrus (parent=Fruits)
                - Oranges (parent=Citrus)
                - Lemons (parent=Citrus)
        - Vegetables (parent=Produce)

API Features:
------------
1. Read-only access to products and categories
2. Category average price calculation with option to include subcategories
"""
