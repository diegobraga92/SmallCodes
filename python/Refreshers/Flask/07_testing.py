"""
COMPREHENSIVE FLASK TESTING DEMONSTRATION
This application illustrates various testing concepts in Flask using pytest.
It includes a complete Flask app with testing examples for all mentioned concepts.
"""

import os
import sys
from datetime import datetime
from unittest.mock import Mock, patch
from functools import wraps
import json

# ============================================================================
# 1. FLASK APPLICATION SETUP WITH APPLICATION FACTORY
# ============================================================================

from flask import Flask, request, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import requests

# Initialize SQLAlchemy without binding to a specific app (for app factory pattern)
db = SQLAlchemy()

# ============================================================================
# 1.1 DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for authentication demonstration"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        }


class Product(db.Model):
    """Product model for demonstrating database operations"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'category': self.category
        }


# ============================================================================
# 1.2 EXTERNAL SERVICE CLIENT (FOR MOCKING DEMONSTRATION)
# ============================================================================

class ExternalPaymentService:
    """Mock external payment service to demonstrate mocking in tests"""
    
    @staticmethod
    def process_payment(amount, card_token):
        """
        Simulate calling an external payment API
        In reality, this would be an HTTP request to a service like Stripe
        """
        # This is where we'd make actual HTTP requests
        # For demonstration, we'll simulate it
        response = requests.post(
            'https://api.paymentservice.com/charge',
            json={'amount': amount, 'token': card_token},
            timeout=5
        )
        return response.json()


# ============================================================================
# 1.3 APPLICATION FACTORY
# ============================================================================

def create_app(config_name=None):
    """
    Application Factory Pattern
    This allows creating Flask instances with different configurations
    Essential for testing with isolated environments
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    if config_name == 'testing':
        # Testing configuration
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    elif config_name == 'development':
        # Development configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    else:
        # Production configuration would go here
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prod.db'
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Create tables within app context
    with app.app_context():
        db.create_all()
    
    # ============================================================================
    # 1.4 HELPER FUNCTIONS AND DECORATORS
    # ============================================================================
    
    def token_required(f):
        """Decorator for requiring JWT authentication"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Check for token in Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    return jsonify({'message': 'Token is missing!'}), 401
            
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401
            
            try:
                # Decode the token
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['user_id'])
                
                if not current_user:
                    return jsonify({'message': 'User not found!'}), 401
                
                # Add user to Flask's global context
                g.current_user = current_user
                
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401
            
            return f(*args, **kwargs)
        
        return decorated
    
    # ============================================================================
    # 1.5 ROUTES
    # ============================================================================
    
    @app.route('/')
    def index():
        """Home route"""
        return jsonify({
            'message': 'Flask Testing Demo API',
            'endpoints': {
                'auth': '/api/auth/*',
                'products': '/api/products/*',
                'payments': '/api/payments/*'
            }
        })
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """User registration endpoint"""
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'User already exists'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data.get('email', f"{data['username']}@example.com")
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """User login endpoint - returns JWT token"""
        data = request.get_json()
        
        # Validation
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Missing credentials'}), 400
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow().timestamp() + 3600},
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        })
    
    @app.route('/api/auth/protected')
    @token_required
    def protected():
        """Protected endpoint requiring authentication"""
        return jsonify({
            'message': f'Hello {g.current_user.username}!',
            'user': g.current_user.to_dict()
        })
    
    @app.route('/api/products', methods=['GET'])
    def get_products():
        """Get all products with optional filtering"""
        category = request.args.get('category')
        
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        products = query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'count': len(products)
        })
    
    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        """Get specific product"""
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict())
    
    @app.route('/api/products', methods=['POST'])
    @token_required
    def create_product():
        """Create a new product (authenticated users only)"""
        if not g.current_user.is_active:
            return jsonify({'message': 'Account is not active'}), 403
        
        data = request.get_json()
        
        # Validation
        if not data or not data.get('name') or not data.get('price'):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Create product
        product = Product(
            name=data['name'],
            price=float(data['price']),
            stock=int(data.get('stock', 0)),
            category=data.get('category', 'uncategorized')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
    
    @app.route('/api/payments/process', methods=['POST'])
    @token_required
    def process_payment():
        """Process payment using external service"""
        data = request.get_json()
        
        # Validation
        if not data or not data.get('amount') or not data.get('card_token'):
            return jsonify({'message': 'Missing payment details'}), 400
        
        # Use external payment service
        payment_service = ExternalPaymentService()
        
        try:
            result = payment_service.process_payment(
                amount=data['amount'],
                card_token=data['card_token']
            )
            
            if result.get('status') == 'success':
                return jsonify({
                    'message': 'Payment processed successfully',
                    'transaction_id': result.get('transaction_id')
                })
            else:
                return jsonify({
                    'message': 'Payment failed',
                    'error': result.get('error')
                }), 400
                
        except requests.exceptions.RequestException as e:
            return jsonify({
                'message': 'Payment service unavailable',
                'error': str(e)
            }), 503
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat()
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
    
    return app


# ============================================================================
# 2. TESTING MODULE - PYTEST WITH FLASK
# ============================================================================

"""
To run these tests:
1. Install pytest: pip install pytest pytest-cov pytest-flask
2. Run: pytest test_flask_app.py -v
3. Run with coverage: pytest test_flask_app.py --cov=. --cov-report=html
"""

import pytest
from flask.testing import FlaskClient

# ============================================================================
# 2.1 FIXTURES
# ============================================================================

@pytest.fixture(scope='session')
def app():
    """
    Pytest fixture that creates a Flask application for testing
    Uses application factory pattern with testing configuration
    """
    app = create_app(config_name='testing')
    
    # Additional test configuration
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    # Establish application context
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def client(app):
    """
    Test client fixture
    Provides a client for making requests to the application
    """
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """
    Database fixture for isolation
    Creates fresh database for each test function
    """
    # Create all tables
    db.create_all()
    
    yield db  # This is where the test runs
    
    # Cleanup after test
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def auth_headers(client, init_database):
    """
    Fixture that creates a test user and returns auth headers
    Demonstrates fixture composition
    """
    # Create test user
    user = User(
        username='testuser',
        email='test@example.com'
    )
    user.set_password('testpass123')
    
    db.session.add(user)
    db.session.commit()
    
    # Login to get token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    token = response.get_json()['token']
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope='function')
def sample_products(init_database):
    """
    Fixture that creates sample products for testing
    Demonstrates data setup in fixtures
    """
    products = [
        Product(name='Laptop', price=999.99, stock=10, category='electronics'),
        Product(name='Mouse', price=29.99, stock=50, category='electronics'),
        Product(name='Book', price=19.99, stock=100, category='books'),
        Product(name='Chair', price=149.99, stock=15, category='furniture'),
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    return products


# ============================================================================
# 2.2 BASIC ROUTE TESTS
# ============================================================================

def test_index_route(client):
    """
    Basic test for the index route
    Demonstrates simple test client usage
    """
    response = client.get('/')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Flask Testing Demo API'


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


# ============================================================================
# 2.3 AUTHENTICATION FLOW TESTS
# ============================================================================

class TestAuthentication:
    """Test class for authentication flows"""
    
    def test_user_registration(self, client, init_database):
        """Test user registration endpoint"""
        response = client.post('/api/auth/register', json={
            'username': 'newuser',
            'password': 'securepassword',
            'email': 'newuser@example.com'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User created successfully'
        assert data['user']['username'] == 'newuser'
        
        # Verify user was actually created in database
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
    
    def test_user_registration_duplicate(self, client, init_database):
        """Test registration with duplicate username"""
        # First registration
        client.post('/api/auth/register', json={
            'username': 'duplicate',
            'password': 'pass123'
        })
        
        # Second registration with same username
        response = client.post('/api/auth/register', json={
            'username': 'duplicate',
            'password': 'pass456'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'already exists' in data['message']
    
    def test_user_login_success(self, client, init_database):
        """Test successful login"""
        # First register a user
        client.post('/api/auth/register', json={
            'username': 'loginuser',
            'password': 'loginpass'
        })
        
        # Then login
        response = client.post('/api/auth/login', json={
            'username': 'loginuser',
            'password': 'loginpass'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Login successful'
        assert 'token' in data
        assert len(data['token']) > 0
    
    def test_user_login_failure(self, client, init_database):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid credentials' in data['message']
    
    def test_protected_route_without_token(self, client):
        """Test accessing protected route without authentication"""
        response = client.get('/api/auth/protected')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'Token is missing' in data['message']
    
    def test_protected_route_with_token(self, client, auth_headers):
        """Test accessing protected route with valid token"""
        response = client.get('/api/auth/protected', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'Hello testuser!' in data['message']


# ============================================================================
# 2.4 DATABASE OPERATION TESTS WITH ISOLATION
# ============================================================================

class TestProductOperations:
    """Tests for product-related operations with database isolation"""
    
    def test_create_product_unauthenticated(self, client):
        """Test creating product without authentication"""
        response = client.post('/api/products', json={
            'name': 'Test Product',
            'price': 99.99
        })
        
        assert response.status_code == 401  # Should require auth
    
    def test_create_product_authenticated(self, client, auth_headers):
        """Test creating product with authentication"""
        response = client.post('/api/products', json={
            'name': 'New Product',
            'price': 49.99,
            'stock': 25,
            'category': 'test'
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Product created successfully'
        assert data['product']['name'] == 'New Product'
        assert data['product']['price'] == 49.99
        
        # Verify in database
        product = Product.query.first()
        assert product is not None
        assert product.name == 'New Product'
    
    def test_get_all_products(self, client, sample_products):
        """Test retrieving all products"""
        response = client.get('/api/products')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'products' in data
        assert 'count' in data
        assert data['count'] == 4  # From sample_products fixture
    
    def test_get_products_filtered(self, client, sample_products):
        """Test retrieving products with category filter"""
        response = client.get('/api/products?category=electronics')
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Should only get electronics products
        assert all(p['category'] == 'electronics' for p in data['products'])
        assert data['count'] == 2  # Laptop and Mouse
    
    @pytest.mark.parametrize('product_id, expected_status', [
        (1, 200),   # Existing product
        (999, 404), # Non-existent product
    ])
    def test_get_single_product(self, client, sample_products, product_id, expected_status):
        """
        Test retrieving single product with parametrization
        Demonstrates pytest parametrization
        """
        response = client.get(f'/api/products/{product_id}')
        
        assert response.status_code == expected_status
        
        if expected_status == 200:
            data = response.get_json()
            assert 'id' in data
            assert data['id'] == product_id


# ============================================================================
# 2.5 MOCKING EXTERNAL SERVICES
# ============================================================================

class TestPaymentProcessing:
    """Tests for payment processing with mocked external service"""
    
    @patch('requests.post')
    def test_successful_payment(self, mock_post, client, auth_headers):
        """
        Test successful payment processing
        Demonstrates mocking external HTTP service
        """
        # Mock the external service response
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'transaction_id': 'txn_123456'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        response = client.post('/api/payments/process', json={
            'amount': 100.00,
            'card_token': 'tok_visa_test'
        }, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Payment processed successfully'
        assert data['transaction_id'] == 'txn_123456'
        
        # Verify the mock was called correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check URL
        assert 'https://api.paymentservice.com/charge' in call_args[0][0]
        
        # Check payload
        assert call_args[1]['json']['amount'] == 100.00
        assert call_args[1]['json']['token'] == 'tok_visa_test'
    
    @patch('requests.post')
    def test_failed_payment(self, mock_post, client, auth_headers):
        """Test payment processing when external service returns failure"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'failed',
            'error': 'Insufficient funds'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        response = client.post('/api/payments/process', json={
            'amount': 100.00,
            'card_token': 'tok_visa_test'
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['message'] == 'Payment failed'
        assert data['error'] == 'Insufficient funds'
    
    @patch('requests.post')
    def test_payment_service_unavailable(self, mock_post, client, auth_headers):
        """Test payment processing when external service is down"""
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )
        
        response = client.post('/api/payments/process', json={
            'amount': 100.00,
            'card_token': 'tok_visa_test'
        }, headers=auth_headers)
        
        assert response.status_code == 503
        data = response.get_json()
        assert data['message'] == 'Payment service unavailable'


# ============================================================================
# 2.6 CONTRACT TESTING
# ============================================================================

class TestAPIContracts:
    """
    Contract testing for API endpoints
    Ensures API responses maintain expected structure
    """
    
    def test_user_response_contract(self, client, init_database):
        """Test that user response follows expected contract"""
        # Register a user
        response = client.post('/api/auth/register', json={
            'username': 'contractuser',
            'password': 'contractpass'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Contract: user object must have these fields
        user = data['user']
        required_fields = ['id', 'username', 'email', 'is_active']
        
        for field in required_fields:
            assert field in user, f"Missing field in user contract: {field}"
        
        # Contract: fields must have correct types
        assert isinstance(user['id'], int)
        assert isinstance(user['username'], str)
        assert isinstance(user['email'], str)
        assert isinstance(user['is_active'], bool)
    
    def test_product_response_contract(self, client, auth_headers):
        """Test that product response follows expected contract"""
        # Create a product
        response = client.post('/api/products', json={
            'name': 'Contract Product',
            'price': 29.99,
            'stock': 10,
            'category': 'test'
        }, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        
        # Contract: product object must have these fields
        product = data['product']
        required_fields = ['id', 'name', 'price', 'stock', 'category']
        
        for field in required_fields:
            assert field in product, f"Missing field in product contract: {field}"
        
        # Contract: field type validation
        assert isinstance(product['id'], int)
        assert isinstance(product['name'], str)
        assert isinstance(product['price'], float)
        assert isinstance(product['stock'], int)
        assert isinstance(product['category'], str)
    
    def test_error_response_contract(self, client):
        """Test that error responses follow expected contract"""
        # Trigger a 404 error
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = response.get_json()
        
        # Contract: error response must have 'message' field
        assert 'message' in data
        assert isinstance(data['message'], str)


# ============================================================================
# 2.7 DATABASE ISOLATION TESTS
# ============================================================================

def test_database_isolation(client, init_database):
    """
    Demonstrates database isolation between tests
    Each test gets a fresh database
    """
    # Add data in this test
    user = User(username='isolated', email='isolated@test.com')
    user.set_password('pass123')
    db.session.add(user)
    db.session.commit()
    
    # Verify data exists in this test
    assert User.query.filter_by(username='isolated').first() is not None


def test_database_isolation_verification(client, init_database):
    """
    Verify that the database is isolated from previous test
    This should NOT find the user from test_database_isolation
    """
    # This should be None if isolation is working
    user = User.query.filter_by(username='isolated').first()
    assert user is None, "Database isolation failed - data leaked between tests"


# ============================================================================
# 2.8 COMPREHENSIVE INTEGRATION TEST
# ============================================================================

class TestCompleteWorkflow:
    """Test a complete user workflow from registration to payment"""
    
    def test_user_journey(self, client, init_database):
        """Complete user journey test"""
        # 1. Register
        register_response = client.post('/api/auth/register', json={
            'username': 'journeyuser',
            'password': 'journeypass',
            'email': 'journey@example.com'
        })
        assert register_response.status_code == 201
        
        # 2. Login
        login_response = client.post('/api/auth/login', json={
            'username': 'journeyuser',
            'password': 'journeypass'
        })
        assert login_response.status_code == 200
        
        token = login_response.get_json()['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Create a product
        product_response = client.post('/api/products', json={
            'name': 'Journey Product',
            'price': 199.99,
            'stock': 5,
            'category': 'journey'
        }, headers=headers)
        assert product_response.status_code == 201
        
        product_id = product_response.get_json()['product']['id']
        
        # 4. Get the created product
        get_product_response = client.get(f'/api/products/{product_id}')
        assert get_product_response.status_code == 200
        
        # 5. Access protected route
        protected_response = client.get('/api/auth/protected', headers=headers)
        assert protected_response.status_code == 200
        
        # Verify all steps were successful
        user_data = login_response.get_json()['user']
        product_data = get_product_response.get_json()
        
        assert user_data['username'] == 'journeyuser'
        assert product_data['name'] == 'Journey Product'


# ============================================================================
# 2.9 EDGE CASES AND ERROR HANDLING
# ============================================================================

def test_malformed_json(client):
    """Test sending malformed JSON"""
    response = client.post(
        '/api/auth/register',
        data='{"malformed": json,',
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    
def test_missing_required_fields(client):
    """Test requests with missing required fields"""
    response = client.post('/api/auth/register', json={
        'username': 'missingfield'
        # Missing password
    })
    
    assert response.status_code == 400


# ============================================================================
# 3. RUNNING TESTS WITH COVERAGE ANALYSIS
# ============================================================================
"""
Coverage analysis shows how much of your code is tested.

To run tests with coverage:
1. Install pytest-cov: pip install pytest-cov
2. Run: pytest test_flask_app.py --cov=. --cov-report=html
3. Open htmlcov/index.html in browser to see coverage report

Coverage reports show:
- Which lines of code were executed during tests
- Which branches were taken
- Overall percentage of code covered
- Missing coverage areas
"""


# ============================================================================
# 4. TEST CONFIGURATION AND SETUP
# ============================================================================
"""
Create a pytest.ini file for configuration:

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short

Or use setup.cfg:

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""


# ============================================================================
# 5. ADDITIONAL TESTING UTILITIES
# ============================================================================

class TestUtilities:
    """Additional testing utility examples"""
    
    @staticmethod
    def assert_valid_jwt(token):
        """Utility to validate JWT structure"""
        parts = token.split('.')
        assert len(parts) == 3, "JWT should have 3 parts"
    
    @staticmethod
    def assert_error_response(response, expected_status, expected_message=None):
        """Utility for validating error responses"""
        assert response.status_code == expected_status
        data = response.get_json()
        assert 'message' in data
        if expected_message:
            assert expected_message in data['message']


# ============================================================================
# 6. RUNNING THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    """
    Main entry point for running the application
    Usage:
        python flask_testing_demo.py              # Run in development mode
        python flask_testing_demo.py --test       # Run tests
        python flask_testing_demo.py --coverage   # Run tests with coverage
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask Testing Demo')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    
    args = parser.parse_args()
    
    if args.test or args.coverage:
        # Run tests using pytest
        import subprocess
        
        cmd = ['pytest', __file__, '-v']
        if args.coverage:
            cmd.extend(['--cov=.', '--cov-report=html', '--cov-report=term'])
        
        print(f"Running tests with command: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    
    else:
        # Run the Flask application
        app = create_app('development')
        
        print(f"Starting Flask application on http://localhost:{args.port}")
        print("Available endpoints:")
        print("  GET  /                    - API information")
        print("  POST /api/auth/register   - Register new user")
        print("  POST /api/auth/login      - Login and get token")
        print("  GET  /api/auth/protected  - Protected endpoint (requires auth)")
        print("  GET  /api/products        - List products")
        print("  POST /api/products        - Create product (requires auth)")
        print("  POST /api/payments/process - Process payment (requires auth)")
        
        app.run(debug=True, port=args.port)