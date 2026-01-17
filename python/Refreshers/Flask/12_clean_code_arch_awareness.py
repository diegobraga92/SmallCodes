"""
Flask Application Demonstrating Modern Development Practices
=============================================================
This comprehensive example illustrates key concepts for building maintainable,
scalable Flask applications following clean architecture principles.
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from abc import ABC, abstractmethod

from flask import Flask, request, jsonify, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError
import redis
import requests
from celery import Celery
import events

# ============================================================================
# PART 1: CLEAN CODE & MAINTAINABILITY
# ============================================================================

# --------------------------------------
# 1.1 AVOID "FAT ROUTES" - Keep controllers thin
# --------------------------------------

# BAD PRACTICE EXAMPLE (commented out):
# @app.route('/order', methods=['POST'])
# def create_order():
#     # Too much logic in route handler - this becomes unmaintainable
#     data = request.get_json()
#     if not data.get('user_id'):
#         return jsonify({'error': 'User ID required'}), 400
#     if not data.get('items'):
#         return jsonify({'error': 'Items required'}), 400
#     # Price calculation
#     total = 0
#     for item in data['items']:
#         total += item['price'] * item['quantity']
#     # Inventory check
#     for item in data['items']:
#         db.query(Inventory).filter_by(product_id=item['id']).first()
#     # User validation
#     user = db.query(User).filter_by(id=data['user_id']).first()
#     # Payment processing
#     # ... and so on - THIS IS A "FAT ROUTE"

# GOOD PRACTICE: Thin controller with extracted logic

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['REDIS_URL'] = 'redis://localhost:6379/0'

# Initialize extensions
db = SQLAlchemy(app)

# --------------------------------------
# 1.2 KEEP BUSINESS LOGIC OUT OF CONTROLLERS
# --------------------------------------

# Domain Models (Business Entities)
@dataclass
class OrderItem:
    """Business domain entity - pure Python, no Flask dependencies"""
    product_id: int
    quantity: int
    unit_price: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price

class Order:
    """Business logic container - independent of web framework"""
    def __init__(self, user_id: int, items: List[OrderItem]):
        self.user_id = user_id
        self.items = items
        self.created_at = datetime.utcnow()
        self.status = 'pending'
    
    def calculate_total(self) -> float:
        """Business logic: price calculation"""
        return sum(item.total_price for item in self.items)
    
    def validate(self) -> List[str]:
        """Business logic: validation rules"""
        errors = []
        if not self.items:
            errors.append("Order must contain items")
        if any(item.quantity <= 0 for item in self.items):
            errors.append("All items must have positive quantity")
        return errors

# --------------------------------------
# 1.3 WRITE REUSABLE SERVICES
# --------------------------------------

class NotificationService(ABC):
    """Abstract service - following Dependency Inversion Principle"""
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class EmailNotificationService(NotificationService):
    """Concrete implementation - can be swapped easily"""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def send(self, recipient: str, message: str) -> bool:
        # Simulate email sending
        print(f"Email to {recipient}: {message}")
        return True

class SMSService(NotificationService):
    """Another implementation - same interface"""
    def __init__(self, account_sid: str, auth_token: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
    
    def send(self, recipient: str, message: str) -> bool:
        # Simulate SMS sending
        print(f"SMS to {recipient}: {message}")
        return True

# --------------------------------------
# 1.4 USE DEPENDENCY INJECTION PATTERNS
# --------------------------------------

class OrderProcessor:
    """
    Service class with dependencies injected through constructor.
    This makes testing easier and dependencies explicit.
    """
    def __init__(
        self,
        notification_service: NotificationService,
        inventory_service: 'InventoryService',
        payment_gateway: 'PaymentGateway'
    ):
        self.notifier = notification_service
        self.inventory = inventory_service
        self.payment = payment_gateway
    
    def process(self, order: Order) -> Dict[str, Any]:
        """Orchestrates order processing using injected dependencies"""
        # Check inventory
        if not self.inventory.check_availability(order.items):
            return {"success": False, "error": "Items out of stock"}
        
        # Process payment
        payment_result = self.payment.charge(order.calculate_total())
        if not payment_result.success:
            return {"success": False, "error": payment_result.message}
        
        # Send notification
        self.notifier.send(
            recipient=f"user_{order.user_id}@example.com",
            message=f"Order processed: ${order.calculate_total():.2f}"
        )
        
        return {"success": True, "order_id": 123}

# Factory function for dependency injection
def create_order_processor() -> OrderProcessor:
    """Centralized dependency creation - easy to configure and test"""
    return OrderProcessor(
        notification_service=EmailNotificationService(
            api_key=os.getenv('EMAIL_API_KEY')
        ),
        inventory_service=InventoryService(db.session),
        payment_gateway=StripePaymentGateway(
            api_key=os.getenv('STRIPE_KEY')
        )
    )

# --------------------------------------
# 1.5 APPLY SOLID PRINCIPLES PRAGMATICALLY
# --------------------------------------

# S - Single Responsibility Principle
class OrderValidator:
    """Only responsible for validation"""
    def validate_items(self, items: List[OrderItem]) -> List[str]:
        return []  # Simplified

class OrderPersister:
    """Only responsible for persistence"""
    def save(self, order: Order) -> int:
        return 123  # Simplified

# O - Open/Closed Principle
class DiscountCalculator(ABC):
    """Open for extension, closed for modification"""
    @abstractmethod
    def calculate(self, order: Order) -> float:
        pass

class PercentageDiscount(DiscountCalculator):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, order: Order) -> float:
        return order.calculate_total() * (self.percentage / 100)

class FixedAmountDiscount(DiscountCalculator):
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate(self, order: Order) -> float:
        return min(self.amount, order.calculate_total())

# L - Liskov Substitution Principle
class BaseRepository(ABC):
    @abstractmethod
    def get(self, id: int):
        pass

class UserRepository(BaseRepository):
    def get(self, id: int):
        # Can be substituted for BaseRepository
        return {"id": id, "name": "John"}

# I - Interface Segregation Principle
class ReadOnlyRepository(ABC):
    """Small, focused interface"""
    @abstractmethod
    def get(self, id: int):
        pass

class WriteRepository(ABC):
    """Another small interface"""
    @abstractmethod
    def save(self, entity):
        pass

# D - Dependency Inversion Principle
# (Already shown with NotificationService abstraction)

# --------------------------------------
# 1.6 REFACTOR LEGACY FLASK APPS SAFELY
# --------------------------------------

# Legacy route (simplified)
@app.route('/legacy/order', methods=['POST'])
def legacy_create_order():
    """
    Legacy endpoint - to be refactored incrementally.
    Strategy: Extract pieces gradually, maintain backward compatibility.
    """
    try:
        # Step 1: Extract validation
        validator = OrderValidator()
        errors = validator.validate_items([])  # Pass actual items
        
        if errors:
            return jsonify({"errors": errors}), 400
        
        # Step 2: Extract business logic (call new service)
        processor = create_order_processor()
        result = processor.process(Order(user_id=1, items=[]))
        
        # Step 3: Return response
        return jsonify(result)
    
    except Exception as e:
        # Add proper error handling during refactoring
        logging.error(f"Order creation failed: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# ============================================================================
# PART 2: ARCHITECTURAL AWARENESS
# ============================================================================

# --------------------------------------
# 2.1 MONOLITH VS MODULAR MONOLITH
# --------------------------------------

# MONOLITHIC STRUCTURE (naive approach):
# app/
# ├── __init__.py
# ├── models.py      # ALL models
# ├── routes.py      # ALL routes
# └── utils.py       # ALL utilities

# MODULAR MONOLITH (recommended for most Flask apps):
# app/
# ├── auth/
# │   ├── __init__.py
# │   ├── models.py
# │   ├── routes.py
# │   └── services.py
# ├── orders/
# │   ├── __init__.py
# │   ├── models.py
# │   ├── routes.py
# │   └── services.py
# ├── products/
# │   ├── __init__.py
# │   ├── models.py
# │   ├── routes.py
# │   └── services.py
# └── shared/
#     ├── database.py
#     └── utils.py

# Implementing Modular Monolith with Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')
products_bp = Blueprint('products', __name__, url_prefix='/products')

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Thin controller in orders module"""
    # Input validation
    data = request.get_json()
    
    # Create business object
    order = Order(
        user_id=data['user_id'],
        items=[OrderItem(**item) for item in data['items']]
    )
    
    # Process with service
    processor = create_order_processor()
    result = processor.process(order)
    
    return jsonify(result)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(products_bp)

# --------------------------------------
# 2.2 FLASK IN MICROSERVICES
# --------------------------------------

# Flask is excellent for microservices when:
# 1. Service boundaries are well-defined
# 2. Team autonomy is required
# 3. Different scaling needs per service

# Example: Orders Microservice
orders_service = Flask(__name__)

@orders_service.route('/orders', methods=['POST'])
def create_order_ms():
    """Microservice endpoint - focused only on orders"""
    # Lightweight, focused responsibility
    data = request.get_json()
    
    # Call internal services via HTTP/RPC
    user_service_url = os.getenv('USER_SERVICE_URL')
    response = requests.get(f"{user_service_url}/users/{data['user_id']}")
    
    if response.status_code != 200:
        return jsonify({"error": "User not found"}), 400
    
    # Process order
    order = Order(user_id=data['user_id'], items=[])
    processor = create_order_processor()
    result = processor.process(order)
    
    # Publish event for other services
    publish_order_created_event(result['order_id'])
    
    return jsonify(result)

def publish_order_created_event(order_id: int):
    """Publish domain event for other microservices"""
    # Could use RabbitMQ, Kafka, Redis Pub/Sub, etc.
    pass

# --------------------------------------
# 2.3 ASYNC WORKERS ALONGSIDE FLASK
# --------------------------------------

# Celery for background tasks
celery = Celery(
    app.name,
    broker=app.config['REDIS_URL'],
    backend=app.config['REDIS_URL']
)

@celery.task
def process_large_order(order_data: Dict[str, Any]):
    """
    Long-running task processed asynchronously.
    Keeps Flask responsive for web requests.
    """
    # Simulate long processing
    import time
    time.sleep(10)
    
    # Process order
    order = Order(**order_data)
    processor = create_order_processor()
    return processor.process(order)

@app.route('/async-order', methods=['POST'])
def create_async_order():
    """Delegates heavy processing to Celery worker"""
    data = request.get_json()
    
    # Queue task for async processing
    task = process_large_order.delay(data)
    
    return jsonify({
        "task_id": task.id,
        "status": "processing",
        "check_status": f"/task-status/{task.id}"
    }), 202

# --------------------------------------
# 2.4 EVENT-DRIVEN PATTERNS
# --------------------------------------

# Simple in-memory event bus (for illustration)
class EventBus:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type: str, callback):
        self.subscribers.setdefault(event_type, []).append(callback)
    
    def publish(self, event_type: str, data: Any):
        for callback in self.subscribers.get(event_type, []):
            callback(data)

# Initialize event bus
event_bus = EventBus()

# Event handlers
def send_order_confirmation_email(data):
    """React to ORDER_CREATED event"""
    print(f"Sending confirmation email for order {data['order_id']}")

def update_inventory(data):
    """React to ORDER_CREATED event"""
    print(f"Updating inventory for order {data['order_id']}")

def log_audit_trail(data):
    """React to ORDER_CREATED event"""
    print(f"Audit log: Order {data['order_id']} created")

# Subscribe handlers
event_bus.subscribe('ORDER_CREATED', send_order_confirmation_email)
event_bus.subscribe('ORDER_CREATED', update_inventory)
event_bus.subscribe('ORDER_CREATED', log_audit_trail)

# Publishing events
@app.route('/event-order', methods=['POST'])
def create_event_order():
    """Uses event-driven architecture"""
    data = request.get_json()
    
    # Process order
    order = Order(user_id=data['user_id'], items=[])
    processor = create_order_processor()
    result = processor.process(order)
    
    # Publish event
    event_bus.publish('ORDER_CREATED', {
        'order_id': result['order_id'],
        'user_id': order.user_id,
        'total': order.calculate_total()
    })
    
    return jsonify(result)

# --------------------------------------
# 2.5 WHEN TO MIGRATE TO FASTAPI
# --------------------------------------

"""
Consider migrating from Flask to FastAPI when:

1. You need automatic OpenAPI documentation
   - FastAPI generates Swagger UI automatically

2. Your API is complex with many endpoints
   - FastAPI's dependency injection is more powerful

3. You need async endpoints for I/O-bound operations
   - Native async support with async/await

4. You require data validation with Pydantic
   - Integrated, type-safe request/response models

5. Performance is critical
   - FastAPI is generally faster due to Starlette foundation

However, stick with Flask when:
- You have an existing, stable Flask codebase
- Your team is highly proficient with Flask
- You need extensive third-party extensions
- Simplicity and minimalism are priorities
- You're building a traditional web app (not just API)
"""

# Example of what would be easier in FastAPI:
# (Shown here for comparison)

"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Automatic request validation with Pydantic
class OrderItemModel(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderModel(BaseModel):
    user_id: int
    items: List[OrderItemModel]

@app.post("/orders")
async def create_order(order: OrderModel):
    # Automatic JSON parsing and validation
    # Automatic OpenAPI documentation
    # Async support
    return {"order_id": 123, "total": 456.78}
"""

# ============================================================================
# SUPPORTING CLASSES (for completeness)
# ============================================================================

class InventoryService:
    """Example service for inventory management"""
    def __init__(self, session):
        self.session = session
    
    def check_availability(self, items: List[OrderItem]) -> bool:
        return True  # Simplified

class PaymentResult:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> PaymentResult:
        pass

class StripePaymentGateway(PaymentGateway):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def charge(self, amount: float) -> PaymentResult:
        # Simulate payment processing
        return PaymentResult(success=True, message="Payment processed")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        # Flask is synchronous by default - suitable for:
        # - Traditional web applications
        # - Small to medium APIs
        # - When simplicity > performance
    )