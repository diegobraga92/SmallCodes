"""
FLASK LARGE-SCALE APPLICATION STRUCTURE
Blueprint Modularization and Project Organization

This example demonstrates a production-ready Flask application structure
with proper separation of concerns for large-scale projects.

Project Structure:
myapp/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration classes
│   ├── extensions.py        # Flask extensions initialization
│   │
│   ├── api/                 # API layer (HTTP/JSON interfaces)
│   │   ├── __init__.py
│   │   ├── v1/              # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── products.py
│   │   │   │   └── orders.py
│   │   │   ├── schemas/     # Marshmallow schemas
│   │   │   ├── resources/   # RESTful resources
│   │   │   └── decorators/  # Custom decorators
│   │   │
│   │   └── v2/              # API version 2 (future)
│   │
│   ├── web/                 # Web layer (HTML templates)
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── auth.py
│   │   │   └── admin.py
│   │   ├── templates/
│   │   ├── static/
│   │   └── forms.py         # WTForms
│   │
│   ├── domain/              # Business logic layer
│   │   ├── __init__.py
│   │   ├── models/          # Business models (not DB models!)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   ├── services/        # Business services
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   ├── product_service.py
│   │   │   └── order_service.py
│   │   ├── exceptions/      # Business exceptions
│   │   ├── events/          # Domain events
│   │   └── value_objects/   # Value objects
│   │
│   ├── application/         # Application services layer
│   │   ├── __init__.py
│   │   ├── services/        # Application services
│   │   ├── commands/        # Command handlers
│   │   ├── queries/         # Query handlers (CQRS pattern)
│   │   └── interfaces/      # Service interfaces
│   │
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py    # SQLAlchemy models
│   │   │   ├── repositories/ # Data access layer
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── user_repository.py
│   │   │   │   └── product_repository.py
│   │   │   └── migrations/  # Alembic migrations
│   │   │
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   └── redis_client.py
│   │   │
│   │   ├── external_apis/
│   │   │   ├── __init__.py
│   │   │   ├── payment_gateway.py
│   │   │   ├── email_service.py
│   │   │   └── sms_service.py
│   │   │
│   │   ├── message_queue/
│   │   │   ├── __init__.py
│   │   │   └── rabbitmq.py
│   │   │
│   │   └── storage/
│   │       ├── __init__.py
│   │       ├── file_storage.py
│   │       └── s3_storage.py
│   │
│   ├── shared/              # Shared utilities
│   │   ├── __init__.py
│   │   ├── utils/
│   │   ├── decorators/
│   │   ├── middleware/
│   │   ├── errors.py        # Shared error classes
│   │   └── logging.py       # Logging configuration
│   │
│   └── auth/                # Authentication module
│       ├── __init__.py
│       ├── routes.py
│       ├── service.py
│       ├── jwt_handler.py
│       └── permissions.py
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── migrations/              # Database migrations (Alembic)
├── scripts/                 # Deployment/maintenance scripts
├── .env.example            # Environment variables template
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── docker-compose.yml      # Container orchestration
├── Dockerfile             # Container definition
└── pyproject.toml         # Project configuration
"""

# ============================================================================
# 1. BLUEPRINT MODULARIZATION
# ============================================================================
"""
BLUEPRINT MODULARIZATION

Blueprints allow you to organize your application into reusable components.
Each blueprint is essentially a mini-application with its own:
- Routes
- Templates
- Static files
- Error handlers
- Before/after request hooks

Key Benefits:
1. Modularity: Different teams can work on different blueprints
2. Reusability: Blueprints can be reused across projects
3. Namespacing: Routes are prefixed with blueprint name
4. Isolation: Each blueprint can have its own configuration
"""

# Example: Creating a blueprint with comprehensive features
# File: app/api/v1/__init__.py

from flask import Blueprint, jsonify, current_app
from .routes import users, products, orders
from ..middleware import api_auth, rate_limit, request_logging

def create_api_v1_blueprint() -> Blueprint:
    """
    Factory function to create API v1 blueprint.
    
    This pattern allows:
    - Dynamic configuration
    - Dependency injection
    - Testing with different configs
    """
    
    # Create blueprint with custom settings
    api_v1_bp = Blueprint(
        'api_v1',
        __name__,
        url_prefix='/api/v1',  # All routes will be prefixed with /api/v1
        template_folder='templates',  # Blueprint-specific templates
        static_folder='static',       # Blueprint-specific static files
        static_url_path='/static/api/v1'  # URL for static files
    )
    
    # ========================================================================
    # Blueprint-specific configuration
    # ========================================================================
    @api_v1_bp.record
    def record_params(setup_state):
        """
        Called when blueprint is registered.
        Allows access to parent app configuration.
        """
        app = setup_state.app
        # Blueprint can access app config
        api_v1_bp.config = app.config.copy()
        
        # Blueprint-specific config overrides
        api_v1_bp.config.setdefault('API_RATE_LIMIT', '100/hour')
        api_v1_bp.config.setdefault('API_VERSION', '1.0.0')
    
    # ========================================================================
    # Blueprint-wide error handlers
    # ========================================================================
    @api_v1_bp.errorhandler(404)
    def api_not_found(error):
        """API-specific 404 handler."""
        return jsonify({
            'error': 'Not Found',
            'message': 'API endpoint does not exist',
            'api_version': 'v1'
        }), 404
    
    @api_v1_bp.errorhandler(429)
    def rate_limit_exceeded(error):
        """Rate limit error handler."""
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded',
            'retry_after': error.description.get('retry_after', 60)
        }), 429
    
    # ========================================================================
    # Blueprint-wide before/after request hooks
    # ========================================================================
    @api_v1_bp.before_request
    def before_api_request():
        """API-specific before request processing."""
        # Log API request
        current_app.logger.info(f"API v1 Request: {request.method} {request.path}")
        
        # Set API-specific headers
        request.api_version = 'v1'
        
        # Validate API key (example)
        api_key = request.headers.get('X-API-Key')
        if not is_valid_api_key(api_key):
            abort(401, description="Invalid API key")
    
    @api_v1_bp.after_request
    def after_api_request(response):
        """API-specific after request processing."""
        # Add API version header
        response.headers['X-API-Version'] = 'v1'
        response.headers['X-Request-ID'] = getattr(g, 'request_id', 'unknown')
        return response
    
    # ========================================================================
    # Register route modules
    # ========================================================================
    # Method 1: Import and register blueprint from module
    api_v1_bp.register_blueprint(users.bp)
    api_v1_bp.register_blueprint(products.bp)
    api_v1_bp.register_blueprint(orders.bp)
    
    # Method 2: Register routes directly
    from .routes.auth import login, logout, register
    api_v1_bp.add_url_rule('/auth/login', view_func=login, methods=['POST'])
    api_v1_bp.add_url_rule('/auth/logout', view_func=logout, methods=['POST'])
    api_v1_bp.add_url_rule('/auth/register', view_func=register, methods=['POST'])
    
    return api_v1_bp

def is_valid_api_key(api_key: str) -> bool:
    """Validate API key (simplified example)."""
    # In real app, check against database or cache
    return api_key == current_app.config.get('API_KEY')

# ============================================================================
# 2. REGISTERING BLUEPRINTS DYNAMICALLY
# ============================================================================
"""
REGISTERING BLUEPRINTS DYNAMICALLY

Dynamic registration allows:
1. Conditional blueprint loading (based on config, features, etc.)
2. Plugin architecture
3. Feature flags
4. Multi-tenant applications with different modules per tenant
"""

# File: app/__init__.py - Application factory with dynamic blueprint registration

import importlib
import os
from typing import Dict, List, Any
from flask import Flask

def create_app(config_name: str = None) -> Flask:
    """
    Enhanced application factory with dynamic blueprint registration.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(f'app.config.{config_name.capitalize()}Config' 
                          if config_name else 'app.config.Config')
    
    # Load environment-specific config
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)
    
    # ========================================================================
    # Initialize extensions
    # ========================================================================
    from .extensions import db, cache, jwt, cors, migrate
    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)
    
    # ========================================================================
    # Dynamic blueprint discovery and registration
    # ========================================================================
    register_blueprints_dynamically(app)
    
    # ========================================================================
    # Register error handlers
    # ========================================================================
    register_error_handlers(app)
    
    # ========================================================================
    # Register CLI commands
    # ========================================================================
    register_cli_commands(app)
    
    # ========================================================================
    # Register context processors
    # ========================================================================
    register_context_processors(app)
    
    return app

def register_blueprints_dynamically(app: Flask) -> None:
    """
    Dynamically discover and register blueprints based on configuration.
    
    This enables:
    - Feature toggles
    - Plugin system
    - Multi-tenant module loading
    """
    
    # Blueprint configuration from app config
    blueprint_config = app.config.get('BLUEPRINTS', {
        'api_v1': {'enabled': True, 'url_prefix': '/api/v1'},
        'api_v2': {'enabled': False, 'url_prefix': '/api/v2'},
        'web': {'enabled': True, 'url_prefix': '/'},
        'admin': {'enabled': True, 'url_prefix': '/admin', 'require_auth': True},
        'docs': {'enabled': app.config['DEBUG'], 'url_prefix': '/docs'},
    })
    
    # Load blueprints based on configuration
    for blueprint_name, config in blueprint_config.items():
        if not config.get('enabled', True):
            app.logger.info(f"Blueprint '{blueprint_name}' is disabled")
            continue
        
        try:
            # Dynamic import of blueprint module
            module_path = f"app.{blueprint_name}"
            module = importlib.import_module(module_path)
            
            # Get blueprint factory function (convention: create_{name}_blueprint)
            factory_name = f"create_{blueprint_name}_blueprint"
            blueprint_factory = getattr(module, factory_name, None)
            
            if blueprint_factory:
                # Create blueprint instance with app context if needed
                with app.app_context():
                    blueprint = blueprint_factory()
                
                # Register blueprint with app
                url_prefix = config.get('url_prefix', f'/{blueprint_name}')
                app.register_blueprint(blueprint, url_prefix=url_prefix)
                
                app.logger.info(f"Registered blueprint: {blueprint_name} at {url_prefix}")
                
                # Apply blueprint-specific middleware if configured
                if config.get('require_auth'):
                    apply_auth_middleware(blueprint)
                    
            else:
                app.logger.warning(f"No factory found for blueprint: {blueprint_name}")
                
        except ImportError as e:
            app.logger.error(f"Failed to import blueprint {blueprint_name}: {e}")
        except Exception as e:
            app.logger.error(f"Failed to register blueprint {blueprint_name}: {e}")

def apply_auth_middleware(blueprint: Blueprint) -> None:
    """Apply authentication middleware to blueprint routes."""
    @blueprint.before_request
    def require_authentication():
        """Require authentication for all routes in this blueprint."""
        from flask import request, jsonify
        from app.auth.service import verify_token
        
        # Skip auth for certain endpoints
        if request.endpoint in ['auth.login', 'auth.register', 'static']:
            return
        
        # Check for authentication token
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token or not verify_token(token):
            return jsonify({'error': 'Authentication required'}), 401

# Example of feature-based blueprint registration
def register_feature_based_blueprints(app: Flask, features: List[str]) -> None:
    """
    Register blueprints based on enabled features.
    
    This allows different deployments to have different feature sets.
    """
    feature_blueprint_map = {
        'api': ['api_v1', 'api_v2'],
        'web_interface': ['web', 'admin'],
        'documentation': ['docs'],
        'monitoring': ['metrics', 'health'],
        'authentication': ['auth'],
    }
    
    for feature in features:
        if feature in feature_blueprint_map:
            for blueprint_name in feature_blueprint_map[feature]:
                register_single_blueprint(app, blueprint_name)

# ============================================================================
# 3. LARGE-SCALE PROJECT LAYOUT WITH SEPARATION OF CONCERNS
# ============================================================================
"""
SEPARATION OF CONCERNS

Clean Architecture / Hexagonal Architecture principles:
1. Domain Layer (Core Business Logic) - Independent of frameworks
2. Application Layer (Use Cases) - Orchestrates domain objects
3. Infrastructure Layer (External Concerns) - DB, APIs, Cache
4. Interface Layer (Delivery Mechanisms) - Web, API, CLI
"""

# Let's walk through a complete example with User management

# ============================================================================
# 3.1 DOMAIN LAYER - Pure business logic
# ============================================================================
# File: app/domain/models/user.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserStatus(Enum):
    """User status enum - domain concept."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"

class UserRole(Enum):
    """User role enum - domain concept."""
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

@dataclass
class User:
    """
    Domain model for User.
    Contains business logic and validation rules.
    """
    id: str
    email: str
    username: str
    hashed_password: str
    status: UserStatus
    roles: List[UserRole]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    def is_active(self) -> bool:
        """Business rule: Check if user is active."""
        return self.status == UserStatus.ACTIVE
    
    def has_role(self, role: UserRole) -> bool:
        """Business rule: Check if user has specific role."""
        return role in self.roles
    
    def can_access_admin_panel(self) -> bool:
        """Business rule: Determine admin panel access."""
        return UserRole.ADMIN in self.roles or UserRole.MODERATOR in self.roles
    
    def change_password(self, new_hashed_password: str) -> None:
        """Business operation: Change password."""
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()
    
    def suspend(self, reason: str) -> None:
        """Business operation: Suspend user."""
        if self.status == UserStatus.BANNED:
            raise ValueError("Cannot suspend a banned user")
        self.status = UserStatus.SUSPENDED
        self.updated_at = datetime.utcnow()
        # Domain event could be raised here
    
    @classmethod
    def create(cls, email: str, username: str, password: str) -> 'User':
        """Factory method: Create new user with business rules."""
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        return cls(
            id=str(uuid.uuid4()),
            email=email.lower().strip(),
            username=username.strip(),
            hashed_password=hash_password(password),  # Domain service
            status=UserStatus.ACTIVE,
            roles=[UserRole.USER],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

# File: app/domain/services/user_service.py

class UserService:
    """
    Domain service for user operations.
    Contains business logic that doesn't fit in a single entity.
    """
    
    def __init__(self, user_repository, email_service):
        # Dependencies are interfaces, not implementations
        self.user_repository = user_repository
        self.email_service = email_service
    
    def register_user(self, email: str, username: str, password: str) -> User:
        """Business use case: Register new user."""
        # Check if user already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create user using domain factory
        user = User.create(email, username, password)
        
        # Save to repository
        self.user_repository.save(user)
        
        # Send welcome email (infrastructure concern, called through interface)
        self.email_service.send_welcome_email(user.email, user.username)
        
        # Could raise domain event here
        # DomainEventPublisher.publish(UserRegisteredEvent(user))
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Business use case: Authenticate user."""
        user = self.user_repository.find_by_email(email)
        
        if not user or not user.is_active():
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.user_repository.save(user)
        
        return user

# ============================================================================
# 3.2 APPLICATION LAYER - Use cases/application services
# ============================================================================
# File: app/application/services/user_application_service.py

from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.models.user import User
from app.domain.services.user_service import UserService

class IUserRepository(ABC):
    """Repository interface - abstraction for data access."""
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> None:
        pass

class UserApplicationService:
    """
    Application service for user operations.
    Orchestrates domain objects and handles transactions.
    """
    
    def __init__(self, 
                 user_repository: IUserRepository,
                 email_service,
                 cache_service):
        self.user_service = UserService(user_repository, email_service)
        self.user_repository = user_repository
        self.cache_service = cache_service
    
    def register_user(self, registration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Application use case: Register user.
        Handles application concerns like caching, DTO conversion.
        """
        try:
            # Call domain service
            user = self.user_service.register_user(
                email=registration_data['email'],
                username=registration_data['username'],
                password=registration_data['password']
            )
            
            # Application-level concerns
            self.cache_service.invalidate(f'users:{user.id}')
            
            # Convert to DTO for response
            return {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'status': user.status.value,
                'created_at': user.created_at.isoformat()
            }
            
        except ValueError as e:
            # Application-specific error handling
            raise RegistrationError(str(e))
    
    def login_user(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Application use case: Login user."""
        user = self.user_service.authenticate_user(
            email=credentials['email'],
            password=credentials['password']
        )
        
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # Generate JWT token (application concern)
        token = generate_jwt_token(user.id)
        
        # Update cache
        self.cache_service.set(f'user_token:{user.id}', token, expiry=3600)
        
        return {
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'roles': [role.value for role in user.roles]
            }
        }

# ============================================================================
# 3.3 INFRASTRUCTURE LAYER - External concerns
# ============================================================================
# File: app/infrastructure/database/repositories/user_repository.py

from sqlalchemy.orm import Session
from app.domain.models.user import User, UserStatus, UserRole
from app.application.services.user_application_service import IUserRepository
from app.infrastructure.database.models import UserModel

class SQLAlchemyUserRepository(IUserRepository):
    """
    Infrastructure: SQLAlchemy implementation of UserRepository.
    Handles persistence concerns.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        user_model = self.db_session.query(UserModel).filter_by(id=user_id).first()
        
        if not user_model:
            return None
        
        return self._to_domain(user_model)
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        user_model = self.db_session.query(UserModel).filter_by(email=email).first()
        
        if not user_model:
            return None
        
        return self._to_domain(user_model)
    
    def save(self, user: User) -> None:
        """Save user to database."""
        user_model = self._to_model(user)
        self.db_session.merge(user_model)
        self.db_session.commit()
    
    def delete(self, user_id: str) -> None:
        """Delete user from database."""
        user_model = self.db_session.query(UserModel).filter_by(id=user_id).first()
        if user_model:
            self.db_session.delete(user_model)
            self.db_session.commit()
    
    def _to_domain(self, model: UserModel) -> User:
        """Convert database model to domain model."""
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            hashed_password=model.hashed_password,
            status=UserStatus(model.status),
            roles=[UserRole(role) for role in model.roles.split(',')],
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login
        )
    
    def _to_model(self, user: User) -> UserModel:
        """Convert domain model to database model."""
        return UserModel(
            id=user.id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            status=user.status.value,
            roles=','.join([role.value for role in user.roles]),
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )

# File: app/infrastructure/cache/redis_client.py

import redis
from typing import Any, Optional

class RedisCache:
    """Infrastructure: Redis cache implementation."""
    
    def __init__(self, host: str, port: int, db: int):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = self.client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, expiry: int = 3600) -> None:
        """Set value in cache with expiry."""
        self.client.setex(key, expiry, json.dumps(value))
    
    def invalidate(self, pattern: str) -> None:
        """Invalidate cache keys matching pattern."""
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)

# File: app/infrastructure/external_apis/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SMTPEmailService:
    """Infrastructure: Email service using SMTP."""
    
    def __init__(self, smtp_host: str, smtp_port: int, 
                 username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_welcome_email(self, to_email: str, username: str) -> None:
        """Send welcome email to new user."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Welcome to Our Service!'
        msg['From'] = self.username
        msg['To'] = to_email
        
        html = f"""
        <html>
          <body>
            <h1>Welcome, {username}!</h1>
            <p>Thank you for registering with our service.</p>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)

# ============================================================================
# 3.4 INTERFACE LAYER - Delivery mechanisms (Web/API)
# ============================================================================
# File: app/api/v1/routes/users.py

from flask import Blueprint, request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.application.services.user_application_service import UserApplicationService
from app.api.v1.schemas import UserRegistrationSchema, UserLoginSchema

# Create blueprint
bp = Blueprint('users', __name__)

# Validation schemas
registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()

@bp.route('/users/register', methods=['POST'])
@inject
def register(
    user_service: UserApplicationService = Provide[Container.user_service]
):
    """API endpoint: Register new user."""
    # Validate input
    errors = registration_schema.validate(request.json)
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        # Call application service
        result = user_service.register_user(request.json)
        
        return jsonify({
            'message': 'User registered successfully',
            'data': result
        }), 201
        
    except RegistrationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/login', methods=['POST'])
@inject
def login(
    user_service: UserApplicationService = Provide[Container.user_service]
):
    """API endpoint: Login user."""
    # Validate input
    errors = login_schema.validate(request.json)
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        # Call application service
        result = user_service.login_user(request.json)
        
        return jsonify({
            'message': 'Login successful',
            'data': result
        }), 200
        
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/users/<user_id>', methods=['GET'])
@inject
@require_auth
def get_user(
    user_id: str,
    user_service: UserApplicationService = Provide[Container.user_service],
    current_user: dict = Provide[Container.current_user]
):
    """API endpoint: Get user profile."""
    # Check permissions
    if user_id != current_user['id'] and 'admin' not in current_user['roles']:
        return jsonify({'error': 'Permission denied'}), 403
    
    user = user_service.get_user_profile(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'data': user}), 200

# ============================================================================
# 4. DEPENDENCY INJECTION CONTAINER
# ============================================================================
# File: app/container.py

from dependency_injector import containers, providers
from flask import current_app
from app.infrastructure.database import get_db_session
from app.infrastructure.cache import RedisCache
from app.infrastructure.external_apis import SMTPEmailService
from app.infrastructure.database.repositories import SQLAlchemyUserRepository
from app.application.services import UserApplicationService

class Container(containers.DeclarativeContainer):
    """Dependency Injection Container."""
    
    # Configuration
    config = providers.Configuration()
    
    # Infrastructure
    db_session = providers.Singleton(
        get_db_session,
        database_url=config.database.url
    )
    
    cache = providers.Singleton(
        RedisCache,
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db
    )
    
    email_service = providers.Singleton(
        SMTPEmailService,
        smtp_host=config.email.smtp_host,
        smtp_port=config.email.smtp_port,
        username=config.email.username,
        password=config.email.password
    )
    
    # Repositories
    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        db_session=db_session
    )
    
    # Application Services
    user_service = providers.Factory(
        UserApplicationService,
        user_repository=user_repository,
        email_service=email_service,
        cache_service=cache
    )
    
    # Current User Provider (for request context)
    current_user = providers.Object(None)

# File: app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extensions (but don't bind to app yet)
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()

# ============================================================================
# 5. WEB LAYER (HTML TEMPLATES)
# ============================================================================
# File: app/web/routes/main.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.web.forms import ContactForm, SearchForm

web_bp = Blueprint('web', __name__, template_folder='templates')

@web_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@web_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    return render_template('dashboard.html', user=current_user)

@web_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form page."""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Process form data
        flash('Thank you for your message!', 'success')
        return redirect(url_for('web.index'))
    
    return render_template('contact.html', form=form)

@web_bp.route('/search')
def search():
    """Search page."""
    form = SearchForm(request.args, meta={'csrf': False})
    results = []
    
    if form.validate():
        # Perform search
        query = form.query.data
        # Call application service
        # results = search_service.search(query)
    
    return render_template('search.html', form=form, results=results)

# ============================================================================
# 6. ADMIN LAYER
# ============================================================================
# File: app/admin/__init__.py

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from functools import wraps

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def create_admin_blueprint() -> Blueprint:
    """Factory function for admin blueprint."""
    admin_bp = Blueprint('admin', __name__, 
                        template_folder='templates/admin',
                        static_folder='static/admin',
                        url_prefix='/admin')
    
    @admin_bp.route('/')
    @admin_required
    def dashboard():
        """Admin dashboard."""
        stats = {
            'total_users': 1500,
            'active_users': 1200,
            'revenue': 50000
        }
        return render_template('admin/dashboard.html', stats=stats)
    
    @admin_bp.route('/users')
    @admin_required
    def user_management():
        """User management page."""
        return render_template('admin/users.html')
    
    @admin_bp.route('/analytics')
    @admin_required
    def analytics():
        """Analytics dashboard."""
        return render_template('admin/analytics.html')
    
    # Admin API endpoints
    @admin_bp.route('/api/users')
    @admin_required
    def api_users():
        """Admin API: Get all users."""
        # In real app, paginate and filter
        users = []  # Get from service
        return jsonify({'users': users})
    
    return admin_bp

# ============================================================================
# 7. CONFIGURATION MANAGEMENT
# ============================================================================
# File: app/config.py

import os
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class BaseConfig:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-me')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Email
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    
    # Blueprints configuration
    BLUEPRINTS: Dict[str, Dict[str, Any]] = {
        'api_v1': {'enabled': True, 'url_prefix': '/api/v1'},
        'web': {'enabled': True, 'url_prefix': '/'},
        'admin': {'enabled': True, 'url_prefix': '/admin', 'require_auth': True},
        'docs': {'enabled': False, 'url_prefix': '/docs'},
    }
    
    # API Configuration
    API_RATE_LIMIT = '100/hour'
    API_VERSION = '1.0.0'

@dataclass
class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    BLUEPRINTS = {
        **BaseConfig.BLUEPRINTS,
        'docs': {'enabled': True, 'url_prefix': '/docs'},
    }

@dataclass
class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    BLUEPRINTS = {
        'api_v1': {'enabled': True, 'url_prefix': '/api/v1'},
        'web': {'enabled': False, 'url_prefix': '/'},
    }

@dataclass
class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    # Override with environment variables
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BLUEPRINTS = {
        'api_v1': {'enabled': True, 'url_prefix': '/api/v1'},
        'web': {'enabled': True, 'url_prefix': '/'},
        'admin': {'enabled': True, 'url_prefix': '/admin', 'require_auth': True},
        'docs': {'enabled': False, 'url_prefix': '/docs'},
    }

# Configuration selector
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# ============================================================================
# 8. MAIN ENTRY POINT
# ============================================================================
# File: run.py

import os
from app import create_app
from app.container import Container

# Determine environment
env = os.environ.get('FLASK_ENV', 'development')

# Create application
app = create_app(env)

# Configure dependency injection container
container = Container()
container.config.from_dict({
    'database': {
        'url': app.config['SQLALCHEMY_DATABASE_URI']
    },
    'redis': {
        'host': app.config['REDIS_HOST'],
        'port': app.config['REDIS_PORT'],
        'db': app.config['REDIS_DB']
    },
    'email': {
        'smtp_host': app.config['SMTP_HOST'],
        'smtp_port': app.config['SMTP_PORT'],
        'username': app.config['SMTP_USERNAME'],
        'password': app.config['SMTP_PASSWORD']
    }
})

# Wire container to app
container.wire(modules=[
    'app.api.v1.routes.users',
    'app.api.v1.routes.products',
    'app.web.routes.main',
])

@app.before_request
def set_request_context():
    """Set up request context for dependency injection."""
    # Extract user from JWT token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token:
        user_data = decode_jwt_token(token)
        container.current_user.override(user_data)

if __name__ == '__main__':
    print(f"Starting Flask application in {env} mode")
    print(f"Registered blueprints:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule}")
    
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )

# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================
"""
BEST PRACTICES FOR LARGE-SCALE FLASK APPLICATIONS:

1. BLUEPRINT ORGANIZATION:
   - Group by feature/domain (users, products, orders)
   - Use blueprint factories for configurability
   - Register dynamically based on configuration

2. SEPARATION OF CONCERNS:
   - Domain Layer: Pure business logic, no framework dependencies
   - Application Layer: Use cases, DTOs, transaction management
   - Infrastructure Layer: DB, Cache, External APIs
   - Interface Layer: Web, API, CLI

3. DEPENDENCY INJECTION:
   - Use interfaces/abstract classes for dependencies
   - Inject dependencies through constructors
   - Use containers for managing dependencies

4. CONFIGURATION MANAGEMENT:
   - Use environment-specific config classes
   - Store sensitive data in environment variables
   - Use configuration for feature toggles

5. ERROR HANDLING:
   - Define domain-specific exceptions
   - Catch exceptions at layer boundaries
   - Provide meaningful error responses

6. TESTING:
   - Test each layer independently
   - Use dependency injection for test doubles
   - Test domain logic without Flask

7. SCALABILITY:
   - Design for horizontal scaling
   - Use external cache (Redis)
   - Implement background tasks with message queues

8. SECURITY:
   - Validate input at boundaries
   - Use parameterized queries
   - Implement proper authentication/authorization
   - Sanitize output

EXAMPLE WORKFLOW:
1. Request arrives at API endpoint
2. Input validation using schemas
3. Dependency injection provides services
4. Application service orchestrates domain logic
5. Domain objects enforce business rules
6. Infrastructure handles persistence/cache
7. Response formatted and returned
"""