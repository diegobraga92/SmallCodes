"""
COMPREHENSIVE FLASK API DESIGN & REST PRINCIPLES TUTORIAL
This application demonstrates professional API design patterns with detailed explanations.
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from functools import wraps
from enum import Enum

# Flask and related imports
from flask import Flask, request, jsonify, make_response, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, func, or_, and_
from sqlalchemy.exc import SQLAlchemyError
import marshmallow as ma
from marshmallow import fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import apispec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
import uuid
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False  # Preserve JSON key order
app.config['PAGINATION_PER_PAGE'] = 20  # Default items per page

db = SQLAlchemy(app)


# ============================================================================
# 1. API VERSIONING STRATEGIES
# ============================================================================

"""
API VERSIONING STRATEGIES:

1. URL Path Versioning: /api/v1/users
   - Pros: Simple, clear, cacheable
   - Cons: URL pollution, breaking browser caching

2. Header Versioning: Accept: application/json; version=1
   - Pros: Clean URLs, content negotiation
   - Cons: Less discoverable, harder to test

3. Query Parameter: /api/users?version=1
   - Pros: Simple, flexible
   - Cons: Not RESTful, caching issues

4. Media Type Versioning: Accept: application/vnd.company.v1+json
   - Pros: Standards-compliant, explicit
   - Cons: Complex, verbose

This app demonstrates URL path versioning (most common approach).
"""

# API Blueprints for different versions
from flask import Blueprint

# Create versioned blueprints
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')


# ============================================================================
# 2. DATABASE MODELS FOR API DEMONSTRATION
# ============================================================================

class User(db.Model):
    """User model for API demonstration."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    profile = db.relationship('UserProfile', back_populates='user', uselist=False,
                             cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    """User profile with detailed information."""
    
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    
    user = db.relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f'<UserProfile {self.first_name} {self.last_name}>'


class Order(db.Model):
    """Order model for demonstrating complex API operations."""
    
    __tablename__ = 'orders'
    
    # Using UUID for public ID to avoid enumeration attacks
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    id = db.Column(db.Integer, primary_key=True)  # Internal ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', 
                       nullable=False)  # pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', 
                           cascade='all, delete-orphan')
    
    # Status enum for validation
    class Status(Enum):
        PENDING = 'pending'
        PROCESSING = 'processing'
        SHIPPED = 'shipped'
        DELIVERED = 'delivered'
        CANCELLED = 'cancelled'
    
    def __repr__(self):
        return f'<Order {self.public_id}>'


class OrderItem(db.Model):
    """Order items for many-to-many relationship with products."""
    
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # In real app, would be ForeignKey
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    order = db.relationship('Order', back_populates='items')
    
    @property
    def total_price(self):
        return self.unit_price * self.quantity
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'


# ============================================================================
# 3. MARSHMALLOW SCHEMAS FOR SERIALIZATION & VALIDATION
# ============================================================================

"""
MARSHMALLOW SCHEMAS:
- Define data structure for serialization/deserialization
- Provide validation rules
- Handle field transformations
- Separate from database models (concern separation)
"""

class UserProfileSchema(SQLAlchemyAutoSchema):
    """Schema for user profile serialization."""
    
    class Meta:
        model = UserProfile
        include_fk = True
        load_instance = True
    
    # Custom validation example
    date_of_birth = fields.Date(format='%Y-%m-%d')
    
    # Computed field
    full_name = fields.Method("get_full_name")
    
    def get_full_name(self, obj):
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return None


class UserSchema(SQLAlchemyAutoSchema):
    """Schema for user serialization with proper nesting."""
    
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)  # Never expose sensitive data
    
    # Nested schema for relationships
    profile = fields.Nested(UserProfileSchema, allow_none=True)
    orders = fields.Nested('OrderSchema', many=True, exclude=('user',))
    
    # HATEOAS links (self-reference)
    links = fields.Method("get_links")
    
    def get_links(self, obj):
        """Generate HATEOAS links for this resource."""
        return {
            "self": url_for('api_v1.get_user', user_id=obj.id, _external=True),
            "orders": url_for('api_v1.get_user_orders', user_id=obj.id, _external=True),
            "profile": url_for('api_v1.get_user_profile', user_id=obj.id, _external=True)
        }
    
    # Metadata
    created_at = fields.DateTime(format='iso')
    updated_at = fields.DateTime(format='iso')


class OrderItemSchema(SQLAlchemyAutoSchema):
    """Schema for order items."""
    
    class Meta:
        model = OrderItem
        load_instance = True
        include_fk = True
    
    # Computed fields
    total_price = fields.Decimal(places=2, as_string=True)
    
    # Custom serialization
    unit_price = fields.Decimal(places=2, as_string=True)


class OrderSchema(SQLAlchemyAutoSchema):
    """Schema for order serialization with proper relationships."""
    
    class Meta:
        model = Order
        load_instance = True
    
    # Use public_id instead of internal id in API
    id = fields.String(attribute='public_id', dump_only=True)
    
    # Nested relationships
    items = fields.Nested(OrderItemSchema, many=True)
    user = fields.Nested(UserSchema, only=('id', 'username', 'email', 'links'))
    
    # Status as enum validation
    status = fields.String(
        validate=validate.OneOf([s.value for s in Order.Status])
    )
    
    # Monetary fields
    total_amount = fields.Decimal(places=2, as_string=True)
    
    # Timestamps
    created_at = fields.DateTime(format='iso')
    updated_at = fields.DateTime(format='iso')
    
    # HATEOAS links
    links = fields.Method("get_links")
    
    def get_links(self, obj):
        """Generate HATEOAS links for orders."""
        return {
            "self": url_for('api_v1.get_order', order_id=obj.public_id, _external=True),
            "user": url_for('api_v1.get_user', user_id=obj.user_id, _external=True),
            "cancel": url_for('api_v1.cancel_order', order_id=obj.public_id, _external=True)
        }


# Input schemas (for POST/PUT/PATCH validation)
class UserCreateSchema(ma.Schema):
    """Schema for creating users (input validation)."""
    
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=80),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error="Only alphanumeric and underscore allowed")
        ]
    )
    
    email = fields.Email(required=True)
    
    # Nested profile data
    profile = fields.Nested(lambda: ProfileCreateSchema(), required=False)
    
    # Field with default
    is_active = fields.Boolean(missing=True)
    
    class Meta:
        ordered = True  # Preserve field order in JSON


class ProfileCreateSchema(ma.Schema):
    """Schema for creating user profiles."""
    
    first_name = fields.String(validate=validate.Length(max=50))
    last_name = fields.String(validate=validate.Length(max=50))
    bio = fields.String(validate=validate.Length(max=500))
    date_of_birth = fields.Date(format='%Y-%m-%d', required=False)
    
    class Meta:
        ordered = True


class OrderCreateSchema(ma.Schema):
    """Schema for creating orders."""
    
    user_id = fields.Integer(required=True)
    items = fields.List(
        fields.Nested(lambda: OrderItemCreateSchema()),
        required=True,
        validate=validate.Length(min=1, error="At least one item required")
    )
    notes = fields.String(required=False)
    currency = fields.String(
        missing='USD',
        validate=validate.OneOf(['USD', 'EUR', 'GBP', 'JPY'])
    )
    
    class Meta:
        ordered = True


class OrderItemCreateSchema(ma.Schema):
    """Schema for order items in creation."""
    
    product_id = fields.Integer(required=True)
    product_name = fields.String(required=True, validate=validate.Length(max=200))
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1, max=100)
    )
    unit_price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0.01, max=100000)
    )


class OrderUpdateSchema(ma.Schema):
    """Schema for updating orders (partial updates with PATCH)."""
    
    status = fields.String(
        validate=validate.OneOf([s.value for s in Order.Status])
    )
    notes = fields.String()
    
    class Meta:
        ordered = True


# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
user_create_schema = UserCreateSchema()
order_create_schema = OrderCreateSchema()
order_update_schema = OrderUpdateSchema()


# ============================================================================
# 4. API RESPONSE STANDARDS & ERROR HANDLING
# ============================================================================

@dataclass
class APIResponse:
    """Standard API response structure."""
    
    success: bool
    data: Any = None
    errors: List[Dict] = None
    meta: Dict = None
    links: Dict = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        result = {"success": self.success}
        
        if self.data is not None:
            result["data"] = self.data
        
        if self.errors:
            result["errors"] = self.errors
        
        if self.meta:
            result["meta"] = self.meta
        
        if self.links:
            result["links"] = self.links
        
        return result


class APIError(Exception):
    """Custom exception for API errors."""
    
    def __init__(self, message, status_code=400, error_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


def standard_response(data=None, meta=None, links=None, status_code=200):
    """Create a standardized successful API response."""
    response = APIResponse(
        success=True,
        data=data,
        meta=meta,
        links=links
    )
    
    return jsonify(response.to_dict()), status_code


def error_response(message, status_code=400, error_code=None, details=None):
    """Create a standardized error API response."""
    error_obj = {
        "message": message,
        "code": error_code or f"HTTP_{status_code}"
    }
    
    if details:
        error_obj["details"] = details
    
    response = APIResponse(
        success=False,
        errors=[error_obj]
    )
    
    return jsonify(response.to_dict()), status_code


@app.errorhandler(APIError)
def handle_api_error(error):
    """Handle APIError exceptions."""
    return error_response(
        message=error.message,
        status_code=error.status_code,
        error_code=error.error_code,
        details=error.details
    )


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle Marshmallow validation errors."""
    return error_response(
        message="Validation failed",
        status_code=422,
        error_code="VALIDATION_ERROR",
        details=error.messages
    )


@app.errorhandler(404)
def handle_not_found(error):
    """Handle 404 errors."""
    return error_response(
        message="Resource not found",
        status_code=404,
        error_code="NOT_FOUND"
    )


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """Handle 405 errors."""
    return error_response(
        message="Method not allowed",
        status_code=405,
        error_code="METHOD_NOT_ALLOWED"
    )


@app.errorhandler(500)
def handle_internal_error(error):
    """Handle 500 errors."""
    # Log the actual error internally
    app.logger.error(f"Internal server error: {error}")
    
    # Return generic message to client
    return error_response(
        message="Internal server error",
        status_code=500,
        error_code="INTERNAL_ERROR"
    )


# ============================================================================
# 5. PAGINATION, FILTERING, AND SORTING
# ============================================================================

@dataclass
class PaginationParams:
    """Encapsulate pagination parameters."""
    
    page: int = 1
    per_page: int = 20
    total: int = 0
    pages: int = 0
    
    @classmethod
    def from_request(cls, request):
        """Extract pagination params from request."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 
                                   app.config['PAGINATION_PER_PAGE'], 
                                   type=int)
        
        # Validate parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:  # Enforce reasonable limits
            per_page = app.config['PAGINATION_PER_PAGE']
        
        return cls(page=page, per_page=per_page)
    
    def get_links(self, base_url, total_items):
        """Generate pagination links for HATEOAS."""
        self.total = total_items
        self.pages = (total_items + self.per_page - 1) // self.per_page
        
        links = {
            "self": f"{base_url}?page={self.page}&per_page={self.per_page}",
            "first": f"{base_url}?page=1&per_page={self.per_page}",
            "last": f"{base_url}?page={self.pages}&per_page={self.per_page}" if self.pages > 0 else None
        }
        
        if self.page > 1:
            links["prev"] = f"{base_url}?page={self.page-1}&per_page={self.per_page}"
        
        if self.page < self.pages:
            links["next"] = f"{base_url}?page={self.page+1}&per_page={self.per_page}"
        
        return {k: v for k, v in links.items() if v is not None}


def apply_pagination_filter_sort(query, model, allowed_filters=None, allowed_sorts=None):
    """
    Apply pagination, filtering, and sorting to a SQLAlchemy query.
    
    Query parameters:
    - page: Page number
    - per_page: Items per page
    - sort: Field to sort by (prefix with - for descending)
    - filter[field]: Filter by field value
    - search: Full-text search
    """
    
    # Default allowed filters and sorts
    if allowed_filters is None:
        allowed_filters = []
    if allowed_sorts is None:
        allowed_sorts = []
    
    # 1. APPLY FILTERING
    filter_params = {}
    for key, value in request.args.items():
        if key.startswith('filter[') and key.endswith(']'):
            field = key[7:-1]  # Extract field name from filter[field]
            
            # Only filter on allowed fields
            if field in allowed_filters:
                filter_params[field] = value
    
    if filter_params:
        filter_conditions = []
        for field, value in filter_params.items():
            if hasattr(model, field):
                # Handle different filter types
                if isinstance(getattr(model, field).type, db.String):
                    # Use LIKE for string fields
                    filter_conditions.append(getattr(model, field).like(f"%{value}%"))
                else:
                    # Exact match for other fields
                    filter_conditions.append(getattr(model, field) == value)
        
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))
    
    # 2. APPLY SEARCH (if model has searchable fields)
    search_term = request.args.get('search')
    if search_term and hasattr(model, 'search'):
        # If model has a search method, use it
        query = model.search(query, search_term)
    
    # 3. APPLY SORTING
    sort_param = request.args.get('sort')
    if sort_param:
        sort_fields = sort_param.split(',')
        
        for sort_field in sort_fields:
            direction = asc
            if sort_field.startswith('-'):
                direction = desc
                sort_field = sort_field[1:]
            
            # Only sort on allowed fields
            if sort_field in allowed_sorts and hasattr(model, sort_field):
                query = query.order_by(direction(getattr(model, sort_field)))
    else:
        # Default sorting
        if hasattr(model, 'created_at'):
            query = query.order_by(desc(model.created_at))
    
    return query


# ============================================================================
# 6. RESTFUL RESOURCE DESIGN WITH PROPER HTTP METHODS
# ============================================================================

"""
RESTFUL RESOURCE DESIGN PRINCIPLES:

1. Resources are nouns, not verbs
2. Use HTTP methods correctly:
   - GET: Retrieve resource(s)
   - POST: Create new resource
   - PUT: Replace entire resource
   - PATCH: Partially update resource
   - DELETE: Remove resource
3. Statelessness
4. Proper status codes
5. HATEOAS (Hypermedia as the Engine of Application State)
"""

# ========== USERS RESOURCE ==========

@api_v1.route('/users', methods=['GET'])
def get_users():
    """
    GET /api/v1/users
    Retrieve all users with pagination, filtering, and sorting.
    
    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20)
    - sort: Sort field (- for descending, e.g., -created_at)
    - filter[username]: Filter by username
    - filter[email]: Filter by email
    - search: Search in username and email
    """
    try:
        # Build base query
        query = User.query
        
        # Apply filtering, sorting, and pagination
        allowed_filters = ['username', 'email', 'is_active']
        allowed_sorts = ['id', 'username', 'email', 'created_at', 'updated_at']
        
        query = apply_pagination_filter_sort(
            query, User, allowed_filters, allowed_sorts
        )
        
        # Get pagination params
        pagination = PaginationParams.from_request(request)
        
        # Execute paginated query
        paginated = query.paginate(
            page=pagination.page,
            per_page=pagination.per_page,
            error_out=False
        )
        
        # Serialize results
        users_data = users_schema.dump(paginated.items)
        
        # Build metadata
        meta = {
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_items": paginated.total,
                "total_pages": paginated.pages,
                "has_prev": paginated.has_prev,
                "has_next": paginated.has_next
            }
        }
        
        # Build HATEOAS links
        base_url = url_for('api_v1.get_users', _external=True)
        links = pagination.get_links(base_url, paginated.total)
        
        return standard_response(data=users_data, meta=meta, links=links)
        
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        raise APIError("Failed to fetch users", status_code=500)


@api_v1.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET /api/v1/users/{id}
    Retrieve a specific user by ID.
    
    Demonstrates:
    - Proper 404 handling
    - Nested resource serialization
    - HATEOAS links
    """
    user = User.query.get_or_404(user_id)
    user_data = user_schema.dump(user)
    
    # Add additional metadata
    meta = {
        "fetched_at": datetime.utcnow().isoformat(),
        "cache_control": "public, max-age=300"  # 5 minutes cache
    }
    
    return standard_response(data=user_data, meta=meta)


@api_v1.route('/users', methods=['POST'])
def create_user():
    """
    POST /api/v1/users
    Create a new user.
    
    Demonstrates:
    - Input validation with Marshmallow
    - Proper 201 Created status code
    - Location header for new resource
    - JSON request body parsing
    """
    try:
        # Validate and parse input
        data = user_create_schema.load(request.json)
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            is_active=data.get('is_active', True)
        )
        
        # Create profile if provided
        if 'profile' in data:
            profile_data = data['profile']
            profile = UserProfile(
                first_name=profile_data.get('first_name'),
                last_name=profile_data.get('last_name'),
                bio=profile_data.get('bio'),
                date_of_birth=profile_data.get('date_of_birth')
            )
            user.profile = profile
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Serialize response
        user_data = user_schema.dump(user)
        
        # Return 201 Created with Location header
        response = jsonify(APIResponse(success=True, data=user_data).to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api_v1.get_user', 
                                              user_id=user.id, 
                                              _external=True)
        return response
        
    except ValidationError as e:
        raise  # Will be caught by validation error handler
    
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error creating user: {e}")
        raise APIError("Failed to create user", status_code=500)


@api_v1.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    PUT /api/v1/users/{id}
    Replace entire user resource.
    
    Demonstrates:
    - PUT vs PATCH semantics (complete replacement)
    - 404 for non-existent resources
    - Idempotency (same request, same result)
    """
    user = User.query.get_or_404(user_id)
    
    try:
        # For PUT, we need all required fields
        data = user_create_schema.load(request.json)
        
        # Update user
        user.username = data['username']
        user.email = data['email']
        user.is_active = data.get('is_active', True)
        user.updated_at = datetime.utcnow()
        
        # Handle profile (replace entirely)
        if 'profile' in data:
            if user.profile:
                # Update existing profile
                profile_data = data['profile']
                user.profile.first_name = profile_data.get('first_name')
                user.profile.last_name = profile_data.get('last_name')
                user.profile.bio = profile_data.get('bio')
                user.profile.date_of_birth = profile_data.get('date_of_birth')
            else:
                # Create new profile
                profile_data = data['profile']
                profile = UserProfile(
                    user_id=user.id,
                    first_name=profile_data.get('first_name'),
                    last_name=profile_data.get('last_name'),
                    bio=profile_data.get('bio'),
                    date_of_birth=profile_data.get('date_of_birth')
                )
                db.session.add(profile)
        elif user.profile:
            # If no profile in request, remove existing profile
            db.session.delete(user.profile)
        
        db.session.commit()
        
        user_data = user_schema.dump(user)
        return standard_response(data=user_data)
        
    except ValidationError as e:
        raise
    
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error updating user: {e}")
        raise APIError("Failed to update user", status_code=500)


@api_v1.route('/users/<int:user_id>', methods=['PATCH'])
def partial_update_user(user_id):
    """
    PATCH /api/v1/users/{id}
    Partially update a user resource.
    
    Demonstrates:
    - PATCH semantics (partial update)
    - Partial validation
    - JSON Merge Patch or JSON Patch (we use simple partial update)
    """
    user = User.query.get_or_404(user_id)
    
    try:
        data = request.json
        
        # Validate partial data
        if 'username' in data:
            if not isinstance(data['username'], str) or len(data['username']) < 3:
                raise ValidationError("Username must be at least 3 characters", 'username')
            user.username = data['username']
        
        if 'email' in data:
            # Simple email validation
            if '@' not in data['email']:
                raise ValidationError("Invalid email format", 'email')
            user.email = data['email']
        
        if 'is_active' in data:
            if not isinstance(data['is_active'], bool):
                raise ValidationError("is_active must be boolean", 'is_active')
            user.is_active = data['is_active']
        
        # Update timestamp
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        user_data = user_schema.dump(user)
        return standard_response(data=user_data)
        
    except ValidationError as e:
        raise APIError(str(e), status_code=422, error_code="VALIDATION_ERROR")
    
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error patching user: {e}")
        raise APIError("Failed to update user", status_code=500)


@api_v1.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    DELETE /api/v1/users/{id}
    Delete a user resource.
    
    Demonstrates:
    - Proper 204 No Content response
    - Idempotency (deleting non-existent returns 204)
    - Cascade deletion handling
    """
    user = User.query.get(user_id)
    
    if user:
        try:
            # In production, you might want to soft delete
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Database error deleting user: {e}")
            raise APIError("Failed to delete user", status_code=500)
    
    # Return 204 No Content (even if user didn't exist - idempotent)
    return '', 204


# ========== NESTED RESOURCES ==========

@api_v1.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    """
    GET /api/v1/users/{id}/orders
    Retrieve orders for a specific user.
    
    Demonstrates:
    - Nested resource endpoints
    - Proper parent resource validation (404 if user doesn't exist)
    - Filtering nested resources
    """
    # Verify user exists
    user = User.query.get_or_404(user_id)
    
    # Build query for user's orders
    query = Order.query.filter_by(user_id=user_id)
    
    # Apply pagination, filtering, sorting
    allowed_filters = ['status', 'currency']
    allowed_sorts = ['created_at', 'updated_at', 'total_amount']
    
    query = apply_pagination_filter_sort(query, Order, allowed_filters, allowed_sorts)
    
    # Get pagination params
    pagination = PaginationParams.from_request(request)
    
    # Execute paginated query
    paginated = query.paginate(
        page=pagination.page,
        per_page=pagination.per_page,
        error_out=False
    )
    
    # Serialize results
    orders_data = orders_schema.dump(paginated.items)
    
    # Build metadata
    meta = {
        "user_id": user_id,
        "username": user.username,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_items": paginated.total,
            "total_pages": paginated.pages
        }
    }
    
    # Build HATEOAS links
    base_url = url_for('api_v1.get_user_orders', user_id=user_id, _external=True)
    links = pagination.get_links(base_url, paginated.total)
    
    return standard_response(data=orders_data, meta=meta, links=links)


@api_v1.route('/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """
    GET /api/v1/users/{id}/profile
    Get user's profile.
    
    Demonstrates:
    - One-to-one relationship endpoints
    - 404 for missing nested resources
    """
    user = User.query.get_or_404(user_id)
    
    if not user.profile:
        raise APIError("Profile not found", status_code=404, error_code="PROFILE_NOT_FOUND")
    
    profile_schema = UserProfileSchema()
    profile_data = profile_schema.dump(user.profile)
    
    return standard_response(data=profile_data)


# ========== ORDERS RESOURCE ==========

@api_v1.route('/orders', methods=['GET'])
def get_orders():
    """
    GET /api/v1/orders
    Retrieve all orders with advanced filtering.
    
    Demonstrates:
    - Complex filtering (date ranges, status, etc.)
    - Field selection (sparse fieldsets)
    - Including related resources
    """
    query = Order.query
    
    # Apply filtering, sorting, and pagination
    allowed_filters = ['status', 'currency', 'user_id']
    allowed_sorts = ['created_at', 'updated_at', 'total_amount', 'status']
    
    # Additional custom filters
    created_after = request.args.get('created_after')
    created_before = request.args.get('created_before')
    
    if created_after:
        try:
            created_after_date = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
            query = query.filter(Order.created_at >= created_after_date)
        except ValueError:
            raise APIError("Invalid date format for created_after", status_code=400)
    
    if created_before:
        try:
            created_before_date = datetime.fromisoformat(created_before.replace('Z', '+00:00'))
            query = query.filter(Order.created_at <= created_before_date)
        except ValueError:
            raise APIError("Invalid date format for created_before", status_code=400)
    
    query = apply_pagination_filter_sort(query, Order, allowed_filters, allowed_sorts)
    
    # Field selection (sparse fieldsets)
    fields = request.args.get('fields')
    if fields:
        # In a real implementation, you would dynamically adjust serialization
        pass
    
    # Include related resources
    include = request.args.get('include')
    if include and 'user' in include:
        # Eager load user to avoid N+1 queries
        query = query.options(db.joinedload(Order.user))
    
    # Get pagination params
    pagination = PaginationParams.from_request(request)
    
    # Execute paginated query
    paginated = query.paginate(
        page=pagination.page,
        per_page=pagination.per_page,
        error_out=False
    )
    
    # Serialize results
    orders_data = orders_schema.dump(paginated.items)
    
    # Build metadata
    meta = {
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_items": paginated.total,
            "total_pages": paginated.pages
        },
        "filters_applied": {
            "created_after": created_after,
            "created_before": created_before
        }
    }
    
    # Build HATEOAS links
    base_url = url_for('api_v1.get_orders', _external=True)
    links = pagination.get_links(base_url, paginated.total)
    
    return standard_response(data=orders_data, meta=meta, links=links)


@api_v1.route('/orders', methods=['POST'])
def create_order():
    """
    POST /api/v1/orders
    Create a new order.
    
    Demonstrates:
    - Complex nested object creation
    - Business logic validation
    - Atomic transactions
    - Idempotency key support
    """
    try:
        # Check for idempotency key (prevent duplicate requests)
        idempotency_key = request.headers.get('Idempotency-Key')
        if idempotency_key:
            # Check if request with this key was already processed
            # In production, you'd use Redis or database for this
            pass
        
        # Validate and parse input
        data = order_create_schema.load(request.json)
        
        # Verify user exists
        user = User.query.get(data['user_id'])
        if not user:
            raise APIError("User not found", status_code=404, error_code="USER_NOT_FOUND")
        
        # Start transaction
        db.session.begin_nested()
        
        # Create order
        order = Order(
            user_id=data['user_id'],
            currency=data['currency'],
            notes=data.get('notes')
        )
        
        # Calculate total and create order items
        total_amount = Decimal('0.00')
        for item_data in data['items']:
            item = OrderItem(
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            order.items.append(item)
            total_amount += item.total_price
        
        order.total_amount = total_amount
        
        # Business logic: Minimum order amount
        if total_amount < Decimal('1.00'):
            raise APIError("Minimum order amount is 1.00", status_code=422,
                          error_code="MIN_ORDER_AMOUNT")
        
        # Save order
        db.session.add(order)
        db.session.commit()
        
        # Serialize response
        order_data = order_schema.dump(order)
        
        # Return 201 Created
        response = jsonify(APIResponse(success=True, data=order_data).to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api_v1.get_order', 
                                              order_id=order.public_id, 
                                              _external=True)
        
        # Store idempotency key if provided
        if idempotency_key:
            response.headers['Idempotency-Key-Processed'] = idempotency_key
        
        return response
        
    except ValidationError as e:
        db.session.rollback()
        raise
    
    except APIError as e:
        db.session.rollback()
        raise
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating order: {e}")
        raise APIError("Failed to create order", status_code=500)


@api_v1.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """
    GET /api/v1/orders/{id}
    Retrieve a specific order by public ID.
    
    Demonstrates:
    - Using public IDs instead of internal IDs
    - 404 with custom error messages
    - Conditional requests (ETag/Last-Modified)
    """
    order = Order.query.filter_by(public_id=order_id).first_or_404()
    
    order_data = order_schema.dump(order)
    
    # Add cache headers
    response = make_response(
        jsonify(APIResponse(success=True, data=order_data).to_dict())
    )
    
    # ETag for conditional requests
    etag = hash(order.updated_at.isoformat())
    response.headers['ETag'] = f'"{etag}"'
    response.headers['Last-Modified'] = order.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
    response.headers['Cache-Control'] = 'private, max-age=60'  # Cache for 1 minute
    
    return response


@api_v1.route('/orders/<string:order_id>', methods=['PATCH'])
def update_order(order_id):
    """
    PATCH /api/v1/orders/{id}
    Partially update an order.
    
    Demonstrates:
    - Business logic in updates
    - State machine validation (order status transitions)
    - Conditional requests with ETag
    """
    order = Order.query.filter_by(public_id=order_id).first_or_404()
    
    try:
        # Check ETag for optimistic concurrency control
        if_match = request.headers.get('If-Match')
        if if_match:
            current_etag = hash(order.updated_at.isoformat())
            if if_match != f'"{current_etag}"':
                raise APIError("Resource has been modified", status_code=412,
                              error_code="PRECONDITION_FAILED")
        
        # Validate and parse input
        data = order_update_schema.load(request.json)
        
        # Update fields if provided
        if 'status' in data:
            # Validate status transition
            valid_transitions = {
                Order.Status.PENDING.value: [Order.Status.PROCESSING.value, Order.Status.CANCELLED.value],
                Order.Status.PROCESSING.value: [Order.Status.SHIPPED.value, Order.Status.CANCELLED.value],
                Order.Status.SHIPPED.value: [Order.Status.DELIVERED.value],
                Order.Status.DELIVERED.value: [],  # Final state
                Order.Status.CANCELLED.value: []   # Final state
            }
            
            current_status = order.status
            new_status = data['status']
            
            if new_status not in valid_transitions.get(current_status, []):
                raise APIError(
                    f"Cannot transition from {current_status} to {new_status}",
                    status_code=422,
                    error_code="INVALID_STATUS_TRANSITION"
                )
            
            order.status = new_status
        
        if 'notes' in data:
            order.notes = data['notes']
        
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        order_data = order_schema.dump(order)
        
        # Update ETag in response
        response = jsonify(APIResponse(success=True, data=order_data).to_dict())
        new_etag = hash(order.updated_at.isoformat())
        response.headers['ETag'] = f'"{new_etag}"'
        
        return response
        
    except ValidationError as e:
        raise
    
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error updating order: {e}")
        raise APIError("Failed to update order", status_code=500)


@api_v1.route('/orders/<string:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    POST /api/v1/orders/{id}/cancel
    Cancel an order (custom action).
    
    Demonstrates:
    - Custom action endpoints when appropriate
    - POST for actions that modify state
    - Business logic with validation
    """
    order = Order.query.filter_by(public_id=order_id).first_or_404()
    
    # Business logic: Can only cancel pending or processing orders
    if order.status not in [Order.Status.PENDING.value, Order.Status.PROCESSING.value]:
        raise APIError(
            f"Cannot cancel order with status {order.status}",
            status_code=422,
            error_code="ORDER_NOT_CANCELLABLE"
        )
    
    # Business logic: Cannot cancel orders older than 24 hours
    age = datetime.utcnow() - order.created_at
    if age > timedelta(hours=24):
        raise APIError(
            "Cannot cancel orders older than 24 hours",
            status_code=422,
            error_code="ORDER_TOO_OLD"
        )
    
    try:
        order.status = Order.Status.CANCELLED.value
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        order_data = order_schema.dump(order)
        return standard_response(data=order_data)
        
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error cancelling order: {e}")
        raise APIError("Failed to cancel order", status_code=500)


# ============================================================================
# 7. API VERSION 2 - DEMONSTRATING API EVOLUTION
# ============================================================================

@api_v2.route('/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    """
    GET /api/v2/users/{id}
    Version 2 of user endpoint with extended data.
    
    Demonstrates:
    - API version evolution
    - Backward compatibility considerations
    - Extended response format
    """
    user = User.query.get_or_404(user_id)
    
    # Extended serialization for v2
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "statistics": {
            "total_orders": len(user.orders),
            "active_since": user.created_at.strftime('%Y-%m-%d')
        },
        "_links": {
            "self": {"href": url_for('api_v2.get_user_v2', user_id=user.id, _external=True)},
            "orders": {"href": url_for('api_v1.get_user_orders', user_id=user.id, _external=True)},
            "avatar": {"href": user.profile.avatar_url if user.profile and user.profile.avatar_url else None}
        },
        "_version": "2.0"
    }
    
    # Add profile if exists
    if user.profile:
        user_data["profile"] = {
            "full_name": f"{user.profile.first_name} {user.profile.last_name}",
            "bio": user.profile.bio,
            "date_of_birth": user.profile.date_of_birth.isoformat() if user.profile.date_of_birth else None
        }
    
    return standard_response(data=user_data)


# ============================================================================
# 8. API SCHEMA DOCUMENTATION WITH OPENAPI/SWAGGER
# ============================================================================

# Configure Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API Design Demo",
        'docExpansion': 'none',
        'operationsSorter': 'method'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/swagger.json')
def swagger_spec():
    """
    Generate OpenAPI/Swagger specification dynamically.
    
    Demonstrates:
    - API documentation as code
    - OpenAPI specification generation
    - Integration with Swagger UI
    """
    spec = apispec.APISpec(
        title="Flask API Design Demo",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
        info={
            "description": """
            Comprehensive Flask API demonstrating REST principles and best practices.
            
            ## Key Concepts Demonstrated:
            
            1. **RESTful Resource Design**
               - Proper HTTP method usage
               - Resource nesting
               - HATEOAS links
            
            2. **API Standards**
               - Consistent JSON serialization
               - Proper HTTP status codes
               - Standard error responses
            
            3. **Advanced Features**
               - Pagination, filtering, sorting
               - API versioning strategies
               - Idempotency
               - Validation standards
            
            4. **Documentation**
               - OpenAPI/Swagger integration
               - Interactive API documentation
            """,
            "contact": {
                "name": "API Support",
                "email": "api@example.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        servers=[
            {"url": "http://localhost:5000", "description": "Development server"},
            {"url": "https://api.example.com", "description": "Production server"}
        ],
        components={
            "schemas": {
                "User": user_schema,
                "Order": order_schema,
                "Error": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "message": {"type": "string"},
                                    "code": {"type": "string"},
                                    "details": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    )
    
    # Register routes with spec
    with app.test_request_context():
        # Users endpoints
        spec.path(view=get_users)
        spec.path(view=get_user)
        spec.path(view=create_user)
        spec.path(view=update_user)
        spec.path(view=partial_update_user)
        spec.path(view=delete_user)
        
        # Orders endpoints
        spec.path(view=get_orders)
        spec.path(view=get_order)
        spec.path(view=create_order)
        spec.path(view=update_order)
        spec.path(view=cancel_order)
        
        # Nested resources
        spec.path(view=get_user_orders)
        spec.path(view=get_user_profile)
        
        # Version 2
        spec.path(view=get_user_v2)
    
    return jsonify(spec.to_dict())


# ============================================================================
# 9. MIDDLEWARE AND ADDITIONAL API FEATURES
# ============================================================================

@app.after_request
def after_request(response):
    """
    Global response processing.
    
    Demonstrates:
    - CORS headers
    - Security headers
    - Content negotiation
    - Rate limiting headers
    """
    # CORS headers (in production, restrict origins)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Idempotency-Key'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # API-specific headers
    response.headers['X-API-Version'] = '1.0'
    response.headers['X-Request-ID'] = request.headers.get('X-Request-ID', 'N/A')
    
    # Content negotiation
    if request.accept_mimetypes.best == 'application/json':
        response.headers['Content-Type'] = 'application/json'
    
    return response


@app.before_request
def before_request():
    """
    Global request processing.
    
    Demonstrates:
    - Request logging
    - Content type validation
    - API key validation (simplified)
    - Request timing
    """
    # Start timer for request duration
    request.start_time = datetime.utcnow()
    
    # Log request
    app.logger.info(f"{request.method} {request.path} - {request.remote_addr}")
    
    # Validate content type for POST/PUT/PATCH
    if request.method in ['POST', 'PUT', 'PATCH']:
        if not request.is_json:
            raise APIError(
                "Content-Type must be application/json",
                status_code=415,
                error_code="UNSUPPORTED_MEDIA_TYPE"
            )
    
    # Simple API key validation (in production, use proper authentication)
    api_key = request.headers.get('X-API-Key')
    if api_key and api_key != 'demo-key':
        raise APIError("Invalid API key", status_code=401, error_code="INVALID_API_KEY")


@app.after_request
def log_request(response):
    """
    Log request completion with timing.
    """
    if hasattr(request, 'start_time'):
        duration = (datetime.utcnow() - request.start_time).total_seconds() * 1000
        app.logger.info(
            f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms"
        )
    
    return response


# ============================================================================
# 10. DEMONSTRATION ROUTES FOR SPECIFIC CONCEPTS
# ============================================================================

@app.route('/api-concepts')
def api_concepts_overview():
    """
    Overview of all API concepts demonstrated.
    """
    html = """
    <html>
        <head>
            <title>Flask API Design Concepts Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                .concept { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                .concept h2 { color: #007bff; margin-top: 0; }
                .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 3px solid #28a745; }
                .method { display: inline-block; padding: 3px 8px; border-radius: 3px; font-weight: bold; margin-right: 10px; }
                .get { background: #28a745; color: white; }
                .post { background: #007bff; color: white; }
                .put { background: #ffc107; color: black; }
                .patch { background: #6f42c1; color: white; }
                .delete { background: #dc3545; color: white; }
                .code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
                .note { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>Flask API Design & REST Principles Demo</h1>
            
            <div class="note">
                <strong>Interactive Documentation:</strong> 
                <a href="/api/docs" target="_blank">OpenAPI/Swagger UI</a>
            </div>
            
            <div class="concept">
                <h2>1. RESTful Resource Design</h2>
                <p>Resources are nouns, HTTP methods indicate actions:</p>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <code>/api/v1/users</code> - List users
                </div>
                
                <div class="endpoint">
                    <span class="method post">POST</span>
                    <code>/api/v1/users</code> - Create user
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <code>/api/v1/users/{id}</code> - Get specific user
                </div>
                
                <div class="endpoint">
                    <span class="method put">PUT</span>
                    <code>/api/v1/users/{id}</code> - Replace entire user
                </div>
                
                <div class="endpoint">
                    <span class="method patch">PATCH</span>
                    <code>/api/v1/users/{id}</code> - Partial update
                </div>
                
                <div class="endpoint">
                    <span class="method delete">DELETE</span>
                    <code>/api/v1/users/{id}</code> - Delete user
                </div>
            </div>
            
            <div class="concept">
                <h2>2. HTTP Methods Semantics</h2>
                <ul>
                    <li><strong>GET</strong>: Safe, idempotent, retrieve data</li>
                    <li><strong>POST</strong: Create new resource, not idempotent</li>
                    <li><strong>PUT</strong>: Replace resource, idempotent</li>
                    <li><strong>PATCH</strong>: Partial update, not necessarily idempotent</li>
                    <li><strong>DELETE</strong>: Remove resource, idempotent</li>
                </ul>
            </div>
            
            <div class="concept">
                <h2>3. Proper Status Codes</h2>
                <ul>
                    <li><span class="code">200 OK</span> - Successful GET, PUT, PATCH</li>
                    <li><span class="code">201 Created</span> - Successful POST</li>
                    <li><span class="code">204 No Content</span> - Successful DELETE</li>
                    <li><span class="code">400 Bad Request</span> - Client error</li>
                    <li><span class="code">401 Unauthorized</span> - Authentication needed</li>
                    <li><span class="code">403 Forbidden</span> - No permission</li>
                    <li><span class="code">404 Not Found</span> - Resource doesn't exist</li>
                    <li><span class="code">422 Unprocessable Entity</span> - Validation error</li>
                    <li><span class="code">500 Internal Server Error</span> - Server error</li>
                </ul>
            </div>
            
            <div class="concept">
                <h2>4. Pagination, Filtering, Sorting</h2>
                <p>Try these query parameters:</p>
                <ul>
                    <li><code>?page=2&per_page=10</code> - Pagination</li>
                    <li><code>?sort=-created_at</code> - Sort by newest first</li>
                    <li><code>?filter[status]=pending</code> - Filter by status</li>
                    <li><code>?search=john</code> - Search across fields</li>
                    <li><code>?created_after=2024-01-01</code> - Date range filter</li>
                    <li><code>?fields=id,username</code> - Sparse fieldsets</li>
                    <li><code>?include=user</code> - Include related resources</li>
                </ul>
            </div>
            
            <div class="concept">
                <h2>5. API Versioning</h2>
                <p>Multiple versioning strategies demonstrated:</p>
                <ul>
                    <li><strong>URL Path</strong>: <code>/api/v1/users</code> (primary method used)</li>
                    <li><strong>Header</strong>: <code>Accept: application/json; version=2</code></li>
                    <li>Compare: <a href="/api/v1/users/1">v1 User</a> vs <a href="/api/v2/users/1">v2 User</a></li>
                </ul>
            </div>
            
            <div class="concept">
                <h2>6. Idempotency</h2>
                <p>Safe retry of operations:</p>
                <ul>
                    <li>GET, PUT, DELETE are naturally idempotent</li>
                    <li>POST with <code>Idempotency-Key</code> header</li>
                    <li>Delete returns 204 even if resource doesn't exist</li>
                </ul>
            </div>
            
            <div class="concept">
                <h2>7. Consistent JSON Serialization</h2>
                <p>All responses follow this structure:</p>
                <pre>{
    "success": true/false,
    "data": { ... },
    "errors": [ { "message": "...", "code": "..." } ],
    "meta": { "pagination": { ... } },
    "links": { "self": "...", "next": "..." }
}</pre>
            </div>
            
            <div class="concept">
                <h2>8. Validation & Error Standards</h2>
                <p>Consistent error responses:</p>
                <pre>{
    "success": false,
    "errors": [{
        "message": "Validation failed",
        "code": "VALIDATION_ERROR",
        "details": {
            "username": ["Already taken"],
            "email": ["Invalid format"]
        }
    }]
}</pre>
            </div>
            
            <div class="concept">
                <h2>9. HATEOAS (Hypermedia Links)</h2>
                <p>Discoverable API with embedded links:</p>
                <pre>{
    "data": { ... },
    "links": {
        "self": "/api/v1/users/1",
        "orders": "/api/v1/users/1/orders",
        "profile": "/api/v1/users/1/profile"
    }
}</pre>
            </div>
            
            <div class="concept">
                <h2>10. API Documentation</h2>
                <p>Interactive OpenAPI/Swagger documentation:</p>
                <ul>
                    <li><a href="/api/docs" target="_blank">Swagger UI</a></li>
                    <li><a href="/api/swagger.json" target="_blank">OpenAPI Spec (JSON)</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    return html


# ============================================================================
# 11. APPLICATION INITIALIZATION
# ============================================================================

def init_database():
    """Initialize database with sample data."""
    with app.app_context():
        db.create_all()
        
        # Add sample data if database is empty
        if not User.query.first():
            # Create users
            users = [
                User(username='alice', email='alice@example.com'),
                User(username='bob', email='bob@example.com'),
                User(username='charlie', email='charlie@example.com')
            ]
            
            # Create profiles
            profiles = [
                UserProfile(first_name='Alice', last_name='Smith', 
                           bio='Software Developer', user=users[0]),
                UserProfile(first_name='Bob', last_name='Johnson',
                           bio='Product Manager', user=users[1])
            ]
            
            # Create orders
            orders = [
                Order(user_id=1, status='pending', total_amount=99.99, currency='USD'),
                Order(user_id=1, status='delivered', total_amount=49.99, currency='USD'),
                Order(user_id=2, status='processing', total_amount=199.99, currency='EUR')
            ]
            
            # Create order items
            order_items = [
                OrderItem(order=orders[0], product_id=101, 
                         product_name='Python Book', quantity=1, unit_price=99.99),
                OrderItem(order=orders[1], product_id=102,
                         product_name='Coffee Mug', quantity=2, unit_price=24.995),
                OrderItem(order=orders[2], product_id=103,
                         product_name='Headphones', quantity=1, unit_price=199.99)
            ]
            
            # Add everything to session
            db.session.add_all(users)
            db.session.add_all(profiles)
            db.session.add_all(orders)
            db.session.add_all(order_items)
            
            db.session.commit()
            print("Database initialized with sample data!")


# Register blueprints
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)


# ============================================================================
# 12. APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Print available endpoints
    print("\n" + "="*60)
    print("FLASK API DESIGN & REST PRINCIPLES DEMO")
    print("="*60)
    print("\nKey Concepts Demonstrated:")
    print("1. RESTful Resource Design")
    print("2. HTTP Methods Semantics")
    print("3. Proper Status Codes")
    print("4. Pagination, Filtering, Sorting")
    print("5. API Versioning Strategies")
    print("6. Idempotency")
    print("7. JSON Serialization Consistency")
    print("8. Validation & Error Standards")
    print("9. HATEOAS Awareness")
    print("10. OpenAPI/Swagger Documentation")
    print("\nAvailable Endpoints:")
    print("• http://localhost:5000/api-concepts - Concepts overview")
    print("• http://localhost:5000/api/docs - Interactive Swagger UI")
    print("• http://localhost:5000/api/v1/users - Users API")
    print("• http://localhost:5000/api/v1/orders - Orders API")
    print("• http://localhost:5000/api/v2/users/1 - Version 2 API")
    print("\nExample API Calls:")
    print("• GET /api/v1/users?page=2&per_page=5&sort=-created_at")
    print("• GET /api/v1/orders?filter[status]=pending&created_after=2024-01-01")
    print("• POST /api/v1/orders with JSON body")
    print("• PATCH /api/v1/users/1 with partial JSON")
    print("="*60 + "\n")
    
    # Run the application
    app.run(debug=True, port=5000)