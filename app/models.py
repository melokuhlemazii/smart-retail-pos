from flask import Flask
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), default='staff')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales = db.relationship('Sale', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"
    
    def is_low_stock(self):
        """Check if product stock is below 10"""
        return self.stock_quantity < 10


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cashier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cashier = db.relationship('User', backref='transactions')
    subtotal = db.Column(db.Float, nullable=False)
    vat_amount = db.Column(db.Float, nullable=False)
    grand_total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), default='cash')  # 'cash', 'card'
    status = db.Column(db.String(20), default='completed')  # 'completed', 'voided'
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    sales = db.relationship('Sale', backref='transaction', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Transaction {self.id} - R{self.grand_total:.2f}>"


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale {self.id} - {self.quantity}x {self.product.name}>"






