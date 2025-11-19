#!/usr/bin/env python
"""
Seed script for Product database
Creates sample products for testing and demonstration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Product

# Create app context
app = create_app()

with app.app_context():
    # Clear existing products (optional - comment out if you want to keep existing data)
    # Product.query.delete()
    
    # Sample products with South African pricing
    sample_products = [
        {
            'product_code': 'COCOLA-500',
            'name': 'Coca Cola 500ml',
            'category': 'Beverages',
            'price': 12.99,
            'stock_quantity': 25
        },
        {
            'product_code': 'BREAD-01',
            'name': 'Brown Bread',
            'category': 'Bakery',
            'price': 16.50,
            'stock_quantity': 12
        },
        {
            'product_code': 'SOAP-750',
            'name': 'Sunlight Dish Soap 750ml',
            'category': 'Cleaning',
            'price': 34.99,
            'stock_quantity': 9
        },
        {
            'product_code': 'MAIZE-5KG',
            'name': 'Mandela Maize Meal 5kg',
            'category': 'Pantry',
            'price': 72.00,
            'stock_quantity': 4
        },
        {
            'product_code': 'RICE-2KG',
            'name': 'Tastic Rice 2kg',
            'category': 'Pantry',
            'price': 48.99,
            'stock_quantity': 15
        }
    ]
    
    # Check if products already exist
    existing_count = Product.query.count()
    
    if existing_count > 0:
        print(f"⚠️  Database already contains {existing_count} product(s).")
        print("Skipping seed to avoid duplicates.")
        print("\nExisting products:")
        products = Product.query.all()
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product.name} (Code: {product.product_code}) - Stock: {product.stock_quantity}")
    else:
        # Add sample products
        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)
        
        try:
            db.session.commit()
            print("✅ Successfully seeded 5 sample products!")
            print("\nAdded products:")
            for i, product_data in enumerate(sample_products, 1):
                print(f"  {i}. {product_data['name']}")
                print(f"     Code: {product_data['product_code']}")
                print(f"     Category: {product_data['category']}")
                print(f"     Price: R{product_data['price']:.2f}")
                print(f"     Stock: {product_data['stock_quantity']} units")
                if product_data['stock_quantity'] < 10:
                    print(f"     ⚠️  LOW STOCK ALERT")
                print()
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding products: {e}")
            sys.exit(1)
