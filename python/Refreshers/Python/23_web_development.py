"""
COMPREHENSIVE PYTHON WEB DEVELOPMENT DEMONSTRATION
===================================================

This module demonstrates key Python web development concepts:
1. Flask & Django fundamentals
2. REST API design principles
3. Database ORM usage (SQLAlchemy, Django ORM)
4. Authentication & Authorization systems
"""

# ============================================================================
# SECTION 1: IMPORTS AND SETUP
# ============================================================================

import os
import sys
import json
import time
import hashlib
import secrets
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from functools import wraps
import sqlite3

# Web Framework Imports
from flask import Flask, request, jsonify, make_response, session, redirect, url_for, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import jwt  # PyJWT for token-based auth
from werkzeug.security import generate_password_hash, check_password_hash

# For demonstration - we'll simulate Django patterns
import django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email

# Data Processing (from previous sections)
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Create necessary directories
demo_dir = Path("demo_web_dev")
demo_dir.mkdir(exist_ok=True)

# ============================================================================
# SECTION 2: FLASK FUNDAMENTALS DEMONSTRATION
# ============================================================================

class FlaskFundamentals:
    """Demonstrates Flask web framework fundamentals."""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'demo-secret-key-2024'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo_web_dev/flask_demo.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize extensions
        self.db = SQLAlchemy(self.app)
        self.login_manager = LoginManager(self.app)
        self.login_manager.login_view = 'login'
        
        self.setup_database()
        self.setup_routes()
        
    def setup_database(self):
        """Set up database models."""
        
        # User model for authentication
        class User(UserMixin, self.db.Model):
            __tablename__ = 'users'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(80), unique=True, nullable=False)
            email = self.db.Column(self.db.String(120), unique=True, nullable=False)
            password_hash = self.db.Column(self.db.String(200), nullable=False)
            role = self.db.Column(self.db.String(50), default='user')  # user, admin
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            is_active = self.db.Column(self.db.Boolean, default=True)
            
            # Relationships
            posts = self.db.relationship('Post', backref='author', lazy=True)
            
            def set_password(self, password):
                self.password_hash = generate_password_hash(password)
            
            def check_password(self, password):
                return check_password_hash(self.password_hash, password)
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'username': self.username,
                    'email': self.email,
                    'role': self.role,
                    'created_at': self.created_at.isoformat() if self.created_at else None
                }
        
        # Blog post model
        class Post(self.db.Model):
            __tablename__ = 'posts'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            title = self.db.Column(self.db.String(200), nullable=False)
            content = self.db.Column(self.db.Text, nullable=False)
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('users.id'), nullable=False)
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            updated_at = self.db.Column(self.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            is_published = self.db.Column(self.db.Boolean, default=True)
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'title': self.title,
                    'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
                    'author_id': self.user_id,
                    'author': self.author.username if self.author else None,
                    'created_at': self.created_at.isoformat() if self.created_at else None,
                    'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                    'is_published': self.is_published
                }
        
        # Product model for e-commerce example
        class Product(self.db.Model):
            __tablename__ = 'products'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            name = self.db.Column(self.db.String(100), nullable=False)
            description = self.db.Column(self.db.Text)
            price = self.db.Column(self.db.Float, nullable=False)
            stock_quantity = self.db.Column(self.db.Integer, default=0)
            category = self.db.Column(self.db.String(50))
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'name': self.name,
                    'description': self.description,
                    'price': self.price,
                    'stock_quantity': self.stock_quantity,
                    'category': self.category,
                    'created_at': self.created_at.isoformat() if self.created_at else None
                }
        
        # Order model
        class Order(self.db.Model):
            __tablename__ = 'orders'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            user_id = self.db.Column(self.db.Integer, self.db.ForeignKey('users.id'), nullable=False)
            total_amount = self.db.Column(self.db.Float, nullable=False)
            status = self.db.Column(self.db.String(50), default='pending')  # pending, paid, shipped, delivered
            created_at = self.db.Column(self.db.DateTime, default=datetime.utcnow)
            
            # Relationship
            user = self.db.relationship('User', backref='orders')
            items = self.db.relationship('OrderItem', backref='order', lazy=True)
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'user_id': self.user_id,
                    'total_amount': self.total_amount,
                    'status': self.status,
                    'created_at': self.created_at.isoformat() if self.created_at else None
                }
        
        # Order item model
        class OrderItem(self.db.Model):
            __tablename__ = 'order_items'
            
            id = self.db.Column(self.db.Integer, primary_key=True)
            order_id = self.db.Column(self.db.Integer, self.db.ForeignKey('orders.id'), nullable=False)
            product_id = self.db.Column(self.db.Integer, self.db.ForeignKey('products.id'), nullable=False)
            quantity = self.db.Column(self.db.Integer, nullable=False)
            unit_price = self.db.Column(self.db.Float, nullable=False)
            
            # Relationship
            product = self.db.relationship('Product')
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'order_id': self.order_id,
                    'product_id': self.product_id,
                    'product_name': self.product.name if self.product else None,
                    'quantity': self.quantity,
                    'unit_price': self.unit_price,
                    'total_price': self.quantity * self.unit_price
                }
        
        # Store model classes
        self.User = User
        self.Post = Post
        self.Product = Product
        self.Order = Order
        self.OrderItem = OrderItem
        
        # Create all tables
        with self.app.app_context():
            self.db.create_all()
            
            # Create default admin user if not exists
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin'
                )
                admin.set_password('admin123')
                self.db.session.add(admin)
                
                # Create some sample data
                user1 = User(username='alice', email='alice@example.com', role='user')
                user1.set_password('password123')
                
                user2 = User(username='bob', email='bob@example.com', role='user')
                user2.set_password('password123')
                
                self.db.session.add_all([user1, user2])
                
                # Create sample products
                products = [
                    Product(name='Laptop', description='High-performance laptop', price=999.99, stock_quantity=10, category='Electronics'),
                    Product(name='Mouse', description='Wireless mouse', price=29.99, stock_quantity=50, category='Electronics'),
                    Product(name='Keyboard', description='Mechanical keyboard', price=89.99, stock_quantity=30, category='Electronics'),
                    Product(name='Book', description='Python programming book', price=39.99, stock_quantity=100, category='Books'),
                ]
                
                self.db.session.add_all(products)
                self.db.session.commit()
                
                print("✓ Created default admin user (username: admin, password: admin123)")
                print("✓ Created sample users (alice, bob) with password: password123")
                print("✓ Created sample products")
    
    @staticmethod
    def role_required(role):
        """Decorator to require specific role."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    return jsonify({'error': 'Authentication required'}), 401
                if current_user.role != role and current_user.role != 'admin':
                    return jsonify({'error': 'Insufficient permissions'}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def setup_routes(self):
        """Set up Flask routes for demonstration."""
        
        @self.login_manager.user_loader
        def load_user(user_id):
            return self.User.query.get(int(user_id))
        
        # ====================
        # HTML TEMPLATES (for demonstration)
        # ====================
        
        HOME_PAGE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask Demo - Web Development</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .api-section { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
                .endpoint { background: white; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
                code { background: #eee; padding: 2px 4px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Flask Web Development Demo</h1>
                <p>This demonstrates Flask fundamentals with database ORM and authentication.</p>
                
                <div class="api-section">
                    <h2>Available Endpoints:</h2>
                    
                    <div class="endpoint">
                        <h3>Authentication</h3>
                        <p><code>POST /api/register</code> - Register new user</p>
                        <p><code>POST /api/login</code> - Login with credentials</p>
                        <p><code>POST /api/logout</code> - Logout current user</p>
                        <p><code>GET /api/profile</code> - Get current user profile</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>Products (Public)</h3>
                        <p><code>GET /api/products</code> - List all products</p>
                        <p><code>GET /api/products/&lt;id&gt;</code> - Get product details</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>Orders (Authenticated)</h3>
                        <p><code>GET /api/orders</code> - Get user's orders</p>
                        <p><code>POST /api/orders</code> - Create new order</p>
                        <p><code>GET /api/orders/&lt;id&gt;</code> - Get order details</p>
                    </div>
                    
                    <div class="endpoint">
                        <h3>Admin Endpoints (Admin only)</h3>
                        <p><code>GET /api/admin/users</code> - List all users</p>
                        <p><code>POST /api/admin/products</code> - Create new product</p>
                        <p><code>PUT /api/admin/products/&lt;id&gt;</code> - Update product</p>
                        <p><code>DELETE /api/admin/products/&lt;id&gt;</code> - Delete product</p>
                    </div>
                </div>
                
                <div class="api-section">
                    <h2>Try it out:</h2>
                    <p>Use tools like curl, Postman, or JavaScript fetch to test the API.</p>
                    <p>Default admin: <code>admin / admin123</code></p>
                    <p>Sample user: <code>alice / password123</code></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        LOGIN_PAGE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - Flask Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .login-form { max-width: 400px; margin: 0 auto; }
                .form-group { margin: 15px 0; }
                label { display: block; margin-bottom: 5px; }
                input { width: 100%; padding: 8px; box-sizing: border-box; }
                button { background: #007bff; color: white; padding: 10px 15px; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="login-form">
                <h2>Login to Flask Demo</h2>
                <form method="POST" action="/api/login">
                    <div class="form-group">
                        <label>Username:</label>
                        <input type="text" name="username" required>
                    </div>
                    <div class="form-group">
                        <label>Password:</label>
                        <input type="password" name="password" required>
                    </div>
                    <button type="submit">Login</button>
                </form>
                <p>Don't have an account? <a href="/api/register-form">Register here</a></p>
                <p>Try: admin/admin123 or alice/password123</p>
            </div>
        </body>
        </html>
        """
        
        # ====================
        # BASIC ROUTES
        # ====================
        
        @self.app.route('/')
        def home():
            return HOME_PAGE
        
        @self.app.route('/api/login-form')
        def login_form():
            return LOGIN_PAGE
        
        # ====================
        # AUTHENTICATION ROUTES
        # ====================
        
        @self.app.route('/api/register', methods=['POST'])
        def register():
            """User registration endpoint."""
            data = request.get_json()
            
            if not data or not data.get('username') or not data.get('password') or not data.get('email'):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Check if user exists
            if self.User.query.filter_by(username=data['username']).first():
                return jsonify({'error': 'Username already exists'}), 409
            
            if self.User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 409
            
            # Create new user
            user = self.User(
                username=data['username'],
                email=data['email'],
                role=data.get('role', 'user')
            )
            user.set_password(data['password'])
            
            self.db.session.add(user)
            self.db.session.commit()
            
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict()
            }), 201
        
        @self.app.route('/api/login', methods=['POST'])
        def login():
            """User login endpoint (supports both form and JSON)."""
            if request.content_type == 'application/json':
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
            else:
                username = request.form.get('username')
                password = request.form.get('password')
            
            user = self.User.query.filter_by(username=username).first()
            
            if not user or not user.check_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user.is_active:
                return jsonify({'error': 'Account is disabled'}), 403
            
            login_user(user)
            
            # Generate JWT token for API authentication
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, self.app.config['SECRET_KEY'], algorithm='HS256')
            
            response_data = {
                'message': 'Login successful',
                'user': user.to_dict(),
                'token': token
            }
            
            # If it's a form submission, redirect to home
            if request.content_type != 'application/json':
                return redirect('/')
            
            return jsonify(response_data)
        
        @self.app.route('/api/logout', methods=['POST'])
        @login_required
        def logout():
            """User logout endpoint."""
            logout_user()
            return jsonify({'message': 'Logout successful'})
        
        @self.app.route('/api/profile', methods=['GET'])
        @login_required
        def profile():
            """Get current user profile."""
            return jsonify({
                'user': current_user.to_dict(),
                'posts_count': len(current_user.posts)
            })
        
        # ====================
        # PRODUCT ROUTES (Public & Protected)
        # ====================
        
        @self.app.route('/api/products', methods=['GET'])
        def get_products():
            """Get all products (public endpoint)."""
            products = self.Product.query.all()
            return jsonify({
                'products': [p.to_dict() for p in products],
                'count': len(products)
            })
        
        @self.app.route('/api/products/<int:product_id>', methods=['GET'])
        def get_product(product_id):
            """Get specific product details (public endpoint)."""
            product = self.Product.query.get_or_404(product_id)
            return jsonify({'product': product.to_dict()})
        
        @self.app.route('/api/admin/products', methods=['POST'])
        @login_required
        @self.role_required('admin')
        def create_product():
            """Create new product (admin only)."""
            data = request.get_json()
            
            if not data or not data.get('name') or not data.get('price'):
                return jsonify({'error': 'Missing required fields'}), 400
            
            product = self.Product(
                name=data['name'],
                description=data.get('description', ''),
                price=float(data['price']),
                stock_quantity=data.get('stock_quantity', 0),
                category=data.get('category', 'Uncategorized')
            )
            
            self.db.session.add(product)
            self.db.session.commit()
            
            return jsonify({
                'message': 'Product created successfully',
                'product': product.to_dict()
            }), 201
        
        @self.app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
        @login_required
        @self.role_required('admin')
        def update_product(product_id):
            """Update product (admin only)."""
            product = self.Product.query.get_or_404(product_id)
            data = request.get_json()
            
            # Update fields if provided
            if 'name' in data:
                product.name = data['name']
            if 'description' in data:
                product.description = data['description']
            if 'price' in data:
                product.price = float(data['price'])
            if 'stock_quantity' in data:
                product.stock_quantity = int(data['stock_quantity'])
            if 'category' in data:
                product.category = data['category']
            
            self.db.session.commit()
            
            return jsonify({
                'message': 'Product updated successfully',
                'product': product.to_dict()
            })
        
        @self.app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
        @login_required
        @self.role_required('admin')
        def delete_product(product_id):
            """Delete product (admin only)."""
            product = self.Product.query.get_or_404(product_id)
            
            self.db.session.delete(product)
            self.db.session.commit()
            
            return jsonify({'message': 'Product deleted successfully'})
        
        # ====================
        # ORDER ROUTES (Authenticated Users)
        # ====================
        
        @self.app.route('/api/orders', methods=['GET'])
        @login_required
        def get_user_orders():
            """Get all orders for current user."""
            orders = self.Order.query.filter_by(user_id=current_user.id).all()
            return jsonify({
                'orders': [order.to_dict() for order in orders],
                'count': len(orders)
            })
        
        @self.app.route('/api/orders', methods=['POST'])
        @login_required
        def create_order():
            """Create new order."""
            data = request.get_json()
            
            if not data or 'items' not in data:
                return jsonify({'error': 'Missing order items'}), 400
            
            # Calculate total and validate products
            total_amount = 0
            order_items = []
            
            for item in data['items']:
                product = self.Product.query.get(item['product_id'])
                
                if not product:
                    return jsonify({'error': f"Product {item['product_id']} not found"}), 404
                
                if product.stock_quantity < item.get('quantity', 1):
                    return jsonify({'error': f"Insufficient stock for {product.name}"}), 400
                
                quantity = item.get('quantity', 1)
                total_amount += product.price * quantity
                
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'unit_price': product.price
                })
            
            # Create order
            order = self.Order(
                user_id=current_user.id,
                total_amount=total_amount,
                status='pending'
            )
            self.db.session.add(order)
            self.db.session.flush()  # Get order ID
            
            # Create order items and update stock
            for item_data in order_items:
                order_item = self.OrderItem(
                    order_id=order.id,
                    product_id=item_data['product'].id,
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price']
                )
                self.db.session.add(order_item)
                
                # Update product stock
                item_data['product'].stock_quantity -= item_data['quantity']
            
            self.db.session.commit()
            
            return jsonify({
                'message': 'Order created successfully',
                'order': order.to_dict(),
                'order_id': order.id
            }), 201
        
        @self.app.route('/api/orders/<int:order_id>', methods=['GET'])
        @login_required
        def get_order(order_id):
            """Get specific order details."""
            order = self.Order.query.get_or_404(order_id)
            
            # Check authorization
            if order.user_id != current_user.id and current_user.role != 'admin':
                return jsonify({'error': 'Access denied'}), 403
            
            order_data = order.to_dict()
            order_data['items'] = [item.to_dict() for item in order.items]
            
            return jsonify({'order': order_data})
        
        # ====================
        # ADMIN ROUTES
        # ====================
        
        @self.app.route('/api/admin/users', methods=['GET'])
        @login_required
        @self.role_required('admin')
        def get_all_users():
            """Get all users (admin only)."""
            users = self.User.query.all()
            return jsonify({
                'users': [user.to_dict() for user in users],
                'count': len(users)
            })
        
        @self.app.route('/api/admin/orders', methods=['GET'])
        @login_required
        @self.role_required('admin')
        def get_all_orders():
            """Get all orders (admin only)."""
            orders = self.Order.query.all()
            return jsonify({
                'orders': [order.to_dict() for order in orders],
                'count': len(orders)
            })
        
        # ====================
        # ERROR HANDLERS
        # ====================
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Resource not found'}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500
        
        @self.app.errorhandler(401)
        def unauthorized(error):
            return jsonify({'error': 'Authentication required'}), 401
        
        @self.app.errorhandler(403)
        def forbidden(error):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
    def demonstrate_flask_features(self):
        """Run demonstration of Flask features."""
        print("\n" + "="*60)
        print("FLASK WEB FRAMEWORK DEMONSTRATION")
        print("="*60)
        
        print("\n1. Flask Application Structure:")
        print("   • App initialization with configuration")
        print("   • Database setup with SQLAlchemy ORM")
        print("   • Model definitions with relationships")
        print("   • Route definitions with decorators")
        
        print("\n2. Key Features Demonstrated:")
        print("   • User authentication with Flask-Login")
        print("   • Role-based authorization")
        print("   • RESTful API design")
        print("   • Database CRUD operations")
        print("   • Error handling")
        print("   • Session management")
        
        print("\n3. Database Models Created:")
        print("   • User (id, username, email, password_hash, role)")
        print("   • Post (id, title, content, user_id)")
        print("   • Product (id, name, description, price, stock)")
        print("   • Order (id, user_id, total_amount, status)")
        print("   • OrderItem (id, order_id, product_id, quantity)")
        
        print("\n4. API Endpoints Available:")
        print("   • Authentication: /api/register, /api/login, /api/logout")
        print("   • Products: /api/products, /api/products/<id>")
        print("   • Orders: /api/orders, /api/orders/<id>")
        print("   • Admin: /api/admin/users, /api/admin/products")
        
        print("\nTo start the Flask server, run: flask_demo.start_server()")
    
    def start_server(self, port=5000):
        """Start the Flask development server."""
        print(f"\nStarting Flask development server on http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        self.app.run(debug=True, port=port)

# ============================================================================
# SECTION 3: DJANGO FUNDAMENTALS DEMONSTRATION
# ============================================================================

class DjangoFundamentals:
    """Demonstrates Django web framework fundamentals."""
    
    def __init__(self):
        self.setup_django_environment()
        self.create_django_app_structure()
        
    def setup_django_environment(self):
        """Setup Django environment for demonstration."""
        print("\n" + "="*60)
        print("DJANGO WEB FRAMEWORK DEMONSTRATION")
        print("="*60)
        
        # Simulate Django project structure
        print("\n1. Django Project Structure:")
        print("   myproject/")
        print("   ├── manage.py")
        print("   ├── myproject/")
        print("   │   ├── __init__.py")
        print("   │   ├── settings.py")
        print("   │   ├── urls.py")
        print("   │   └── wsgi.py")
        print("   └── myapp/")
        print("       ├── __init__.py")
        print("       ├── models.py")
        print("       ├── views.py")
        print("       ├── urls.py")
        print("       └── serializers.py")
        
        print("\n2. Django Key Concepts:")
        print("   • MTV Architecture (Model-Template-View)")
        print("   • Built-in ORM with migrations")
        print("   • Admin interface")
        print("   • Class-based views")
        print("   • URL routing with regex patterns")
        print("   • Middleware system")
        print("   • Form handling")
        
    def create_django_app_structure(self):
        """Create Django-like code structure for demonstration."""
        
        # Create Django-like files for demonstration
        django_dir = demo_dir / "django_demo"
        django_dir.mkdir(exist_ok=True)
        
        # Create settings.py equivalent
        settings_content = '''
"""
Django Settings Example
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = 'django-insecure-demo-key-2024'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'myapp',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# URLs
ROOT_URLCONF = 'myproject.urls'

# Templates
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
}]
'''
        
        # Create models.py equivalent
        models_content = '''
"""
Django Models Example
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """Extended user model with additional fields."""
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Category(models.Model):
    """Product category model."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    """Product model for e-commerce."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class Order(models.Model):
    """Order model."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

class OrderItem(models.Model):
    """Order item model."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def total_price(self):
        return self.quantity * self.unit_price

class Review(models.Model):
    """Product review model."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']
'''
        
        # Create views.py equivalent
        views_content = '''
"""
Django Views Example (Class-based views)
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import CustomUser, Product, Order, Review, Category
from .serializers import (
    UserSerializer, ProductSerializer, OrderSerializer, 
    ReviewSerializer, CategorySerializer
)

# ====================
# FUNCTION-BASED VIEWS
# ====================

@api_view(['GET'])
def api_root(request):
    """API root endpoint."""
    return Response({
        'users': request.build_absolute_uri('api/users/'),
        'products': request.build_absolute_uri('api/products/'),
        'categories': request.build_absolute_uri('api/categories/'),
    })

@api_view(['POST'])
def register_user(request):
    """User registration endpoint."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """User login endpoint."""
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ====================
# CLASS-BASED VIEWS
# ====================

class ProductListView(ListView):
    """List all products (traditional Django view)."""
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset.filter(is_available=True)

class ProductDetailView(DetailView):
    """Product detail view."""
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

# ====================
# DRF VIEWSETS
# ====================

class UserViewSet(viewsets.ModelViewSet):
    """User viewset for CRUD operations."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    """Product viewset."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.filter(is_available=True)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """Add review to product."""
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    """Order viewset."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see their own orders (admins see all)."""
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Set user when creating order."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order."""
        order = self.get_object()
        if order.user != request.user and not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=403)
        
        order.status = 'cancelled'
        order.save()
        return Response({'status': 'Order cancelled'})

class CategoryViewSet(viewsets.ModelViewSet):
    """Category viewset."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# ====================
# CUSTOM PERMISSIONS
# ====================

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission for admin-only write access."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
'''
        
        # Create serializers.py equivalent
        serializers_content = '''
"""
Django REST Framework Serializers
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser, Product, Order, OrderItem, Review, Category

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password2', 
                 'first_name', 'last_name', 'phone', 'date_of_birth', 'is_premium']
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """Validate password match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields don't match."})
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user."""
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    product_count = serializers.IntegerField(source='product_set.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'product_count']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    review_count = serializers.IntegerField(source='reviews.count', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id',
                 'stock_quantity', 'is_available', 'created_at', 'updated_at',
                 'average_rating', 'review_count']

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'total_amount', 'status', 
                 'shipping_address', 'created_at', 'updated_at', 'items']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create order with calculated total."""
        items_data = self.context['request'].data.get('items', [])
        
        # Calculate total from items
        total = 0
        order_items = []
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data.get('quantity', 1)
            unit_price = product.price
            
            total += quantity * unit_price
            order_items.append({
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price
            })
        
        order = Order.objects.create(
            user=validated_data['user'],
            total_amount=total,
            shipping_address=validated_data.get('shipping_address', '')
        )
        
        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
        
        return order

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = UserSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'product_name', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def validate(self, data):
        """Validate review data."""
        user = self.context['request'].user
        product = data['product']
        
        # Check if user already reviewed this product
        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        return data
'''
        
        # Create urls.py equivalent
        urls_content = '''
"""
Django URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    # API Root
    path('', views.api_root, name='api-root'),
    
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Include router URLs
    path('', include(router.urls)),
    
    # Traditional views (for comparison)
    path('products-list/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
'''
        
        # Create admin.py equivalent
        admin_content = '''
"""
Django Admin Configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Category, Order, Review

class CustomUserAdmin(UserAdmin):
    """Custom admin for User model."""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_premium')
    list_filter = ('is_staff', 'is_superuser', 'is_premium')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'date_of_birth', 'is_premium')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'date_of_birth', 'is_premium')}),
    )

class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model."""
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity', 'is_available')
    readonly_fields = ('created_at', 'updated_at')

class OrderAdmin(admin.ModelAdmin):
    """Admin for Order model."""
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
'''
        
        # Write files
        (django_dir / "settings.py").write_text(settings_content)
        (django_dir / "models.py").write_text(models_content)
        (django_dir / "views.py").write_text(views_content)
        (django_dir / "serializers.py").write_text(serializers_content)
        (django_dir / "urls.py").write_text(urls_content)
        (django_dir / "admin.py").write_text(admin_content)
        
        print("\n3. Django Application Components:")
        print("   • Models: Database schema with relationships")
        print("   • Views: Class-based and function-based views")
        print("   • Serializers: Data transformation and validation")
        print("   • URLs: Route configuration with patterns")
        print("   • Admin: Custom admin interface")
        
        print("\n4. Django REST Framework Features:")
        print("   • ViewSets for CRUD operations")
        print("   • Serializers with nested relationships")
        print("   • Custom permissions and authentication")
        print("   • Pagination and filtering")
        print("   • Browsable API interface")
        
        print("\n✓ Created Django-like project structure in:", django_dir)

# ============================================================================
# SECTION 4: REST API DESIGN PRINCIPLES
# ============================================================================

class RestApiDesign:
    """Demonstrates REST API design principles and best practices."""
    
    def __init__(self):
        pass
    
    def demonstrate_rest_principles(self):
        """Explain REST API design principles."""
        print("\n" + "="*60)
        print("REST API DESIGN PRINCIPLES")
        print("="*60)
        
        print("\n1. REST Architectural Constraints:")
        print("   • Client-Server Architecture")
        print("   • Statelessness: Each request contains all information")
        print("   • Cacheability: Responses must define cacheability")
        print("   • Uniform Interface: Consistent resource identification")
        print("   • Layered System: Intermediary servers can be added")
        print("   • Code on Demand (optional): Client can download code")
        
        print("\n2. Resource Naming Conventions:")
        print("   • Use nouns for resources, not verbs")
        print("   • Use plural nouns for collections")
        print("   • Use hyphens for multi-word resources")
        print("   • Use lowercase letters")
        print("   • Avoid file extensions in URLs")
        
        print("\n3. HTTP Methods and Semantics:")
        print("   • GET: Retrieve resource(s)")
        print("   • POST: Create new resource")
        print("   • PUT: Replace/update entire resource")
        print("   • PATCH: Partially update resource")
        print("   • DELETE: Remove resource")
        print("   • HEAD: Get headers only")
        print("   • OPTIONS: Get allowed methods")
        
        print("\n4. Status Code Guidelines:")
        print("   2xx - Success:")
        print("     • 200 OK: Standard success")
        print("     • 201 Created: Resource created")
        print("     • 204 No Content: Success with no body")
        
        print("\n   3xx - Redirection:")
        print("     • 301 Moved Permanently")
        print("     • 304 Not Modified (caching)")
        
        print("\n   4xx - Client Errors:")
        print("     • 400 Bad Request: Invalid syntax")
        print("     • 401 Unauthorized: Authentication needed")
        print("     • 403 Forbidden: No permission")
        print("     • 404 Not Found: Resource doesn't exist")
        print("     • 409 Conflict: Resource conflict")
        print("     • 422 Unprocessable Entity: Validation failed")
        
        print("\n   5xx - Server Errors:")
        print("     • 500 Internal Server Error")
        print("     • 501 Not Implemented")
        print("     • 503 Service Unavailable")
        
        print("\n5. API Versioning Strategies:")
        print("   • URL Versioning: /api/v1/resource")
        print("   • Header Versioning: Accept: application/vnd.api.v1+json")
        print("   • Query Parameter: /api/resource?version=1")
        print("   • Media Type Versioning: Content-Type with version")
        
        print("\n6. Response Format Best Practices:")
        print("   • Always return JSON for APIs")
        print("   • Use consistent error format:")
        print("     {\"error\": {\"code\": \"...\", \"message\": \"...\"}}")
        print("   • Include pagination metadata")
        print("   • Use HATEOAS for discoverability")
        print("   • Include rate limiting headers")
        
        print("\n7. Authentication & Authorization:")
        print("   • API Keys: Simple but less secure")
        print("   • JWT Tokens: Stateless, self-contained")
        print("   • OAuth 2.0: Industry standard for delegation")
        print("   • OpenID Connect: Identity layer on OAuth 2.0")
        
        print("\n8. Rate Limiting Strategies:")
        print("   • Fixed Window: X requests per minute")
        print("   • Sliding Window: More accurate time window")
        print("   • Token Bucket: Burst allowance")
        print("   • Include headers: X-RateLimit-Limit, X-RateLimit-Remaining")
        
        print("\n9. Documentation Standards:")
        print("   • OpenAPI/Swagger specification")
        print("   • Interactive API documentation")
        print("   • Include examples for all endpoints")
        print("   • Document error responses")
        
    def create_rest_api_example(self):
        """Create a complete REST API example following best practices."""
        
        print("\n" + "="*60)
        print("COMPLETE REST API EXAMPLE")
        print("="*60)
        
        rest_api_dir = demo_dir / "rest_api_example"
        rest_api_dir.mkdir(exist_ok=True)
        
        # Create main API file
        api_content = '''
"""
Complete REST API Example Following Best Practices
"""
from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api-secret-key-2024'
app.config['API_VERSION'] = 'v1'

# Security and Rate Limiting
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

# In-memory database for demo
users_db = {}
products_db = {}
orders_db = {}

# ====================
# DECORATORS & HELPERS
# ====================

def token_required(f):
    """JWT token authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'error': {
                    'code': 'MISSING_TOKEN',
                    'message': 'Authentication token is required'
                }
            }), 401
        
        try:
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['user_id'])
            if not current_user:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': {
                    'code': 'TOKEN_EXPIRED',
                    'message': 'Token has expired'
                }
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': 'Invalid authentication token'
                }
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def role_required(role):
    """Role-based authorization decorator."""
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user['role'] != role and current_user['role'] != 'admin':
                return jsonify({
                    'error': {
                        'code': 'INSUFFICIENT_PERMISSIONS',
                        'message': f'Requires {role} role'
                    }
                }), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

# ====================
# ERROR HANDLING
# ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': {
            'code': 'RESOURCE_NOT_FOUND',
            'message': 'The requested resource was not found'
        }
    }), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': {
            'code': 'RATE_LIMIT_EXCEEDED',
            'message': 'Rate limit exceeded. Please try again later.'
        }
    }), 429

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': {
            'code': 'INTERNAL_SERVER_ERROR',
            'message': 'An internal server error occurred'
        }
    }), 500

# ====================
# HEALTH & INFO ENDPOINTS
# ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': app.config['API_VERSION']
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'E-Commerce API',
        'version': app.config['API_VERSION'],
        'documentation': 'https://api.example.com/docs',
        'endpoints': {
            'auth': '/api/auth/*',
            'products': '/api/products',
            'orders': '/api/orders',
            'users': '/api/users'
        }
    })

# ====================
# AUTHENTICATION ENDPOINTS
# ====================

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """User registration."""
    data = request.get_json()
    
    # Validation
    required_fields = ['email', 'password', 'username']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': f'{field} is required',
                    'field': field
                }
            }), 400
    
    # Check if user exists
    for user in users_db.values():
        if user['email'] == data['email']:
            return jsonify({
                'error': {
                    'code': 'EMAIL_EXISTS',
                    'message': 'Email already registered'
                }
            }), 409
    
    # Create user
    user_id = str(uuid.uuid4())
    user = {
        'id': user_id,
        'email': data['email'],
        'username': data['username'],
        'password': data['password'],  # In production, hash this!
        'role': data.get('role', 'user'),
        'created_at': datetime.utcnow().isoformat(),
        'is_active': True
    }
    
    users_db[user_id] = user
    
    # Generate token
    token = jwt.encode({
        'user_id': user_id,
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'user': {
            'id': user_id,
            'email': user['email'],
            'username': user['username'],
            'role': user['role']
        },
        'token': token,
        'expires_in': 86400  # 24 hours in seconds
    }), 201

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """User login."""
    data = request.get_json()
    
    # Find user
    user = None
    for u in users_db.values():
        if u['email'] == data.get('email') and u['password'] == data.get('password'):
            user = u
            break
    
    if not user or not user['is_active']:
        return jsonify({
            'error': {
                'code': 'INVALID_CREDENTIALS',
                'message': 'Invalid email or password'
            }
        }), 401
    
    # Generate token
    token = jwt.encode({
        'user_id': user['id'],
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'role': user['role']
        },
        'token': token,
        'expires_in': 86400
    })

# ====================
# PRODUCT ENDPOINTS
# ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with filtering and pagination."""
    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Filtering
    filtered_products = list(products_db.values())
    
    category = request.args.get('category')
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    min_price = request.args.get('min_price')
    if min_price:
        filtered_products = [p for p in filtered_products if p['price'] >= float(min_price)]
    
    max_price = request.args.get('max_price')
    if max_price:
        filtered_products = [p for p in filtered_products if p['price'] <= float(max_price)]
    
    # Pagination calculation
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_products = filtered_products[start_idx:end_idx]
    
    # Build response
    response = {
        'data': paginated_products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': len(filtered_products),
            'total_pages': (len(filtered_products) + per_page - 1) // per_page
        },
        'links': {
            'self': f'/api/products?page={page}&per_page={per_page}',
            'next': f'/api/products?page={page + 1}&per_page={per_page}' if end_idx < len(filtered_products) else None,
            'prev': f'/api/products?page={page - 1}&per_page={per_page}' if page > 1 else None
        }
    }
    
    return jsonify(response)

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID."""
    product = products_db.get(product_id)
    if not product:
        return jsonify({
            'error': {
                'code': 'PRODUCT_NOT_FOUND',
                'message': f'Product with ID {product_id} not found'
            }
        }), 404
    
    return jsonify({'data': product})

@app.route('/api/products', methods=['POST'])
@token_required
@role_required('admin')
def create_product(current_user):
    """Create new product (admin only)."""
    data = request.get_json()
    
    # Validation
    required_fields = ['name', 'price', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': f'{field} is required',
                    'field': field
                }
            }), 400
    
    # Create product
    product_id = str(uuid.uuid4())
    product = {
        'id': product_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'price': float(data['price']),
        'category': data['category'],
        'stock': int(data.get('stock', 0)),
        'created_by': current_user['id'],
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    products_db[product_id] = product
    
    return jsonify({'data': product}), 201

# ====================
# ORDER ENDPOINTS
# ====================

@app.route('/api/orders', methods=['GET'])
@token_required
def get_user_orders(current_user):
    """Get orders for current user."""
    user_orders = [o for o in orders_db.values() if o['user_id'] == current_user['id']]
    
    return jsonify({
        'data': user_orders,
        'count': len(user_orders)
    })

@app.route('/api/orders', methods=['POST'])
@token_required
def create_order(current_user):
    """Create new order."""
    data = request.get_json()
    
    if not data or 'items' not in data or not data['items']:
        return jsonify({
            'error': {
                'code': 'NO_ITEMS',
                'message': 'Order must contain at least one item'
            }
        }), 400
    
    # Validate items and calculate total
    total = 0
    order_items = []
    
    for item in data['items']:
        product = products_db.get(item['product_id'])
        if not product:
            return jsonify({
                'error': {
                    'code': 'PRODUCT_NOT_FOUND',
                    'message': f'Product {item["product_id"]} not found'
                }
            }), 404
        
        quantity = item.get('quantity', 1)
        if product['stock'] < quantity:
            return jsonify({
                'error': {
                    'code': 'INSUFFICIENT_STOCK',
                    'message': f'Insufficient stock for {product["name"]}'
                }
            }), 400
        
        item_total = product['price'] * quantity
        total += item_total
        
        order_items.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total': item_total
        })
    
    # Create order
    order_id = str(uuid.uuid4())
    order = {
        'id': order_id,
        'user_id': current_user['id'],
        'items': order_items,
        'total': total,
        'status': 'pending',
        'shipping_address': data.get('shipping_address', ''),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    orders_db[order_id] = order
    
    # Update product stock (in a real app, use transactions)
    for item in data['items']:
        product = products_db[item['product_id']]
        product['stock'] -= item.get('quantity', 1)
    
    return jsonify({'data': order}), 201

if __name__ == '__main__':
    # Initialize with some sample data
    sample_products = {
        '1': {'id': '1', 'name': 'Laptop', 'price': 999.99, 'category': 'electronics', 'stock': 10},
        '2': {'id': '2', 'name': 'Mouse', 'price': 29.99, 'category': 'electronics', 'stock': 50},
        '3': {'id': '3', 'name': 'Keyboard', 'price': 89.99, 'category': 'electronics', 'stock': 30},
    }
    products_db.update(sample_products)
    
    app.run(debug=True, port=5001)
'''
        
        (rest_api_dir / "rest_api.py").write_text(api_content)
        
        # Create API documentation
        docs_content = '''
# REST API Documentation

## Base URL