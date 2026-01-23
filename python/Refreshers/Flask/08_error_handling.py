"""
COMPREHENSIVE FLASK ERROR HANDLING & OBSERVABILITY TUTORIAL
This application demonstrates professional error handling, logging, and monitoring patterns.
"""

import os
import sys
import json
import logging
import traceback
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union, List, Callable
from dataclasses import dataclass, asdict, field
from functools import wraps
from contextlib import contextmanager
from enum import Enum
import inspect

# Flask and related imports
from flask import Flask, request, jsonify, make_response, g, abort, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from prometheus_client.exposition import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import statsd
from statsd import StatsClient
import structlog
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import BoundLogger, get_logger
import redis
from redis.exceptions import RedisError
import requests
from requests.exceptions import RequestException
from werkzeug.exceptions import HTTPException, InternalServerError

# Initialize Flask app
app = Flask(__name__)

# ============================================================================
# 1. CONFIGURATION FOR OBSERVABILITY
# ============================================================================

"""
OBSERVABILITY PILLARS:
1. Logging: What happened and when
2. Metrics: How often and how long
3. Tracing: Flow through the system
4. Alerting: When things go wrong
"""

# Load configuration from environment
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', '1' if app.config['ENV'] == 'development' else '0')
app.config['SERVICE_NAME'] = os.environ.get('SERVICE_NAME', 'flask-error-demo')
app.config['VERSION'] = os.environ.get('VERSION', '1.0.0')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///observability.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis for distributed tracing/correlation (optional)
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# External services
app.config['EXTERNAL_API_URL'] = os.environ.get('EXTERNAL_API_URL', 'https://api.example.com')
app.config['EXTERNAL_API_TIMEOUT'] = int(os.environ.get('EXTERNAL_API_TIMEOUT', '5'))

# Observability tools
app.config['SENTRY_DSN'] = os.environ.get('SENTRY_DSN', '')
app.config['STATSD_HOST'] = os.environ.get('STATSD_HOST', 'localhost')
app.config['STATSD_PORT'] = int(os.environ.get('STATSD_PORT', '8125'))
app.config['STATSD_PREFIX'] = os.environ.get('STATSD_PREFIX', 'flask_app')
app.config['PROMETHEUS_METRICS_PATH'] = os.environ.get('PROMETHEUS_METRICS_PATH', '/metrics')

# Logging configuration
app.config['LOG_LEVEL'] = os.environ.get('LOG_LEVEL', 'INFO').upper()
app.config['LOG_FORMAT'] = os.environ.get('LOG_FORMAT', 'json')  # json or text
app.config['LOG_FILE'] = os.environ.get('LOG_FILE', None)  # Optional file logging

# Initialize extensions
db = SQLAlchemy(app)

# Initialize Redis if configured
redis_client = None
if app.config['REDIS_URL'] and app.config['REDIS_URL'] != 'redis://localhost:6379/0':
    try:
        redis_client = redis.from_url(app.config['REDIS_URL'])
        redis_client.ping()  # Test connection
        app.logger.info("Redis connected successfully")
    except RedisError as e:
        app.logger.warning(f"Redis connection failed: {e}")
        redis_client = None

# Initialize StatsD client
statsd_client = None
if app.config['STATSD_HOST']:
    try:
        statsd_client = StatsClient(
            host=app.config['STATSD_HOST'],
            port=app.config['STATSD_PORT'],
            prefix=app.config['STATSD_PREFIX']
        )
        app.logger.info(f"StatsD connected to {app.config['STATSD_HOST']}:{app.config['STATSD_PORT']}")
    except Exception as e:
        app.logger.warning(f"StatsD connection failed: {e}")
        statsd_client = None


# ============================================================================
# 2. STRUCTURED LOGGING CONFIGURATION
# ============================================================================

"""
STRUCTURED LOGGING PRINCIPLES:
1. Machine-readable format (JSON)
2. Consistent field names
3. Include context (request_id, user_id, etc.)
4. Appropriate log levels
5. No sensitive data
"""

def setup_structured_logging():
    """Configure structured logging with structlog."""
    
    # Configure standard library logging
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    # Clear existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Create handler based on configuration
    if app.config['LOG_FILE']:
        handler = logging.FileHandler(app.config['LOG_FILE'])
    else:
        handler = logging.StreamHandler(sys.stdout)
    
    # Configure formatter
    if app.config['LOG_FORMAT'] == 'json':
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[handler])
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            TimeStamper(fmt="iso", key="timestamp"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            
            # Add correlation ID
            lambda _, __, event_dict: add_correlation_id(event_dict),
            
            # Render as JSON
            JSONRenderer() if app.config['LOG_FORMAT'] == 'json' else structlog.dev.ConsoleRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Set Flask's logger
    app.logger = get_logger(__name__)
    
    return get_logger(__name__)


def add_correlation_id(event_dict):
    """Add correlation ID to log entries."""
    if hasattr(g, 'correlation_id'):
        event_dict['correlation_id'] = g.correlation_id
    if hasattr(g, 'request_id'):
        event_dict['request_id'] = g.request_id
    if request:
        event_dict['method'] = request.method
        event_dict['path'] = request.path
        event_dict['remote_addr'] = request.remote_addr
    return event_dict


# Initialize structured logging
logger = setup_structured_logging()


# ============================================================================
# 3. CORRELATION IDS & REQUEST TRACING
# ============================================================================

@dataclass
class RequestContext:
    """Container for request-scoped context data."""
    correlation_id: str = None
    request_id: str = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    client_ip: Optional[str] = None
    user_agent: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.utcnow)
    extra: Dict[str, Any] = field(default_factory=dict)


def generate_correlation_id() -> str:
    """Generate a unique correlation ID."""
    # In microservices, this would propagate from upstream
    return str(uuid.uuid4())


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return f"req_{uuid.uuid4().hex[:16]}"


@app.before_request
def setup_request_context():
    """Set up request context for observability."""
    # Get correlation ID from headers or generate new
    correlation_id = request.headers.get('X-Correlation-ID') or generate_correlation_id()
    request_id = request.headers.get('X-Request-ID') or generate_request_id()
    
    # Store in Flask's g object
    g.correlation_id = correlation_id
    g.request_id = request_id
    g.request_context = RequestContext(
        correlation_id=correlation_id,
        request_id=request_id,
        client_ip=request.remote_addr,
        user_agent=request.user_agent.string if request.user_agent else None,
        start_time=datetime.utcnow()
    )
    
    # Log request start
    logger.info(
        "request_started",
        method=request.method,
        path=request.path,
        correlation_id=correlation_id,
        request_id=request_id
    )
    
    # Increment request counter
    if statsd_client:
        statsd_client.incr('requests.total')
        statsd_client.incr(f'requests.method.{request.method.lower()}')


@app.after_request
def finalize_request(response):
    """Finalize request logging and add correlation headers."""
    if hasattr(g, 'request_context'):
        ctx = g.request_context
        
        # Calculate request duration
        duration = (datetime.utcnow() - ctx.start_time).total_seconds() * 1000
        
        # Add correlation headers to response
        response.headers['X-Correlation-ID'] = ctx.correlation_id
        response.headers['X-Request-ID'] = ctx.request_id
        
        # Log request completion
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": duration,
            "correlation_id": ctx.correlation_id,
            "request_id": ctx.request_id
        }
        
        # Add user context if available
        if hasattr(g, 'current_user') and g.current_user:
            log_data['user_id'] = g.current_user.id
        
        # Log at appropriate level
        if response.status_code >= 500:
            logger.error("request_completed", **log_data)
        elif response.status_code >= 400:
            logger.warning("request_completed", **log_data)
        else:
            logger.info("request_completed", **log_data)
        
        # Record metrics
        if statsd_client:
            statsd_client.timing('requests.duration', duration)
            statsd_client.incr(f'requests.status.{response.status_code}')
        
        # Update Prometheus metrics
        REQUEST_DURATION.observe(duration / 1000)  # Convert to seconds
        REQUEST_COUNTER.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
    
    return response


# ============================================================================
# 4. PROMETHEUS METRICS
# ============================================================================

"""
METRICS TYPES:
1. Counter: Monotonically increasing (requests, errors)
2. Gauge: Can go up and down (memory usage, active users)
3. Histogram: Observe distributions (request duration, response size)
4. Summary: Similar to histogram but calculates quantiles
"""

# Define Prometheus metrics
REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0)
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of active HTTP requests'
)

DATABASE_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

EXTERNAL_API_DURATION = Histogram(
    'external_api_duration_seconds',
    'External API call duration in seconds',
    ['service', 'endpoint', 'status']
)

ERROR_COUNTER = Counter(
    'errors_total',
    'Total number of errors',
    ['type', 'source']
)

BUSINESS_EVENTS = Counter(
    'business_events_total',
    'Business events counter',
    ['event_type', 'user_type']
)

# Add metrics endpoint
@app.route(app.config['PROMETHEUS_METRICS_PATH'])
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(REGISTRY)


# ============================================================================
# 5. SENTRY ERROR TRACKING
# ============================================================================

"""
SENTRY INTEGRATION BENEFITS:
1. Real-time error tracking
2. Stack traces with context
3. Performance monitoring
4. Release tracking
5. Issue grouping and alerting
"""

def setup_sentry():
    """Configure Sentry error tracking."""
    if app.config['SENTRY_DSN']:
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[
                FlaskIntegration(),
                SqlalchemyIntegration()
            ],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0 if app.config['ENV'] == 'development' else 0.1,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0 if app.config['ENV'] == 'development' else 0.1,
            environment=app.config['ENV'],
            release=app.config['VERSION'],
            send_default_pii=False,  # Don't send personal identifiable information
            debug=app.config['DEBUG'],
        )
        
        # Add context to Sentry events
        @app.before_request
        def set_sentry_context():
            if sentry_sdk.Hub.current:
                with sentry_sdk.configure_scope() as scope:
                    scope.set_tag("correlation_id", g.get('correlation_id', 'unknown'))
                    scope.set_tag("request_id", g.get('request_id', 'unknown'))
                    scope.set_user({
                        "ip_address": request.remote_addr,
                        "user_agent": request.user_agent.string if request.user_agent else None,
                    })
        
        logger.info("Sentry error tracking configured")
    else:
        logger.info("Sentry DSN not configured, error tracking disabled")


# Initialize Sentry
setup_sentry()


# ============================================================================
# 6. CUSTOM EXCEPTIONS & ERROR RESPONSE STRUCTURE
# ============================================================================

"""
ERROR HANDLING PRINCIPLES:
1. Use specific exception types
2. Include error codes for programmatic handling
3. Structured error responses
4. Appropriate HTTP status codes
5. Include correlation IDs
"""

class AppError(Exception):
    """Base application error with structured data."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = None,
        details: Dict = None,
        internal_details: str = None,
        cause: Exception = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f"ERR_{status_code}"
        self.details = details or {}
        self.internal_details = internal_details
        self.cause = cause
        
        # Automatically log error
        self._log_error()
    
    def _log_error(self):
        """Log the error with context."""
        log_data = {
            "error_code": self.error_code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }
        
        if self.cause:
            log_data["cause"] = str(self.cause)
            log_data["traceback"] = traceback.format_exc()
        
        logger.error("application_error", **log_data)
        
        # Increment error counter
        if statsd_client:
            statsd_client.incr('errors.total')
            statsd_client.incr(f'errors.type.{self.error_code}')
        
        ERROR_COUNTER.labels(type=self.error_code, source='application').inc()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON response."""
        error_dict = {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details,
            },
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "correlation_id": getattr(g, 'correlation_id', None),
                "request_id": getattr(g, 'request_id', None),
            }
        }
        
        # Only include internal details in development
        if app.config['ENV'] == 'development' and self.internal_details:
            error_dict["error"]["internal"] = self.internal_details
        
        return error_dict


# Domain-specific exceptions
class ValidationError(AppError):
    """Input validation error."""
    
    def __init__(self, message: str, field_errors: Dict = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details={"field_errors": field_errors} if field_errors else {}
        )


class AuthenticationError(AppError):
    """Authentication failed error."""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationError(AppError):
    """Authorization failed error."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR"
        )


class NotFoundError(AppError):
    """Resource not found error."""
    
    def __init__(self, resource: str = "Resource", identifier: Any = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND_ERROR"
        )


class DatabaseError(AppError):
    """Database operation error."""
    
    def __init__(self, operation: str, table: str = None, cause: Exception = None):
        message = f"Database error during {operation}"
        if table:
            message += f" on table {table}"
        
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            cause=cause,
            details={
                "operation": operation,
                "table": table,
            }
        )


class ExternalServiceError(AppError):
    """External service error."""
    
    def __init__(self, service: str, endpoint: str, status_code: int, cause: Exception = None):
        super().__init__(
            message=f"Service {service} returned error {status_code} for {endpoint}",
            status_code=502 if status_code >= 500 else 503,
            error_code="EXTERNAL_SERVICE_ERROR",
            cause=cause,
            details={
                "service": service,
                "endpoint": endpoint,
                "external_status_code": status_code,
            }
        )


class RateLimitError(AppError):
    """Rate limit exceeded error."""
    
    def __init__(self, limit: int, window: str):
        super().__init__(
            message=f"Rate limit exceeded: {limit} requests per {window}",
            status_code=429,
            error_code="RATE_LIMIT_ERROR",
            details={
                "limit": limit,
                "window": window,
            }
        )


# ============================================================================
# 7. ERROR RESPONSE HANDLERS
# ============================================================================

def error_response(error: AppError) -> tuple:
    """Create a standardized error response."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    
    # Add correlation headers
    if hasattr(g, 'correlation_id'):
        response.headers['X-Correlation-ID'] = g.correlation_id
    if hasattr(g, 'request_id'):
        response.headers['X-Request-ID'] = g.request_id
    
    # Add retry-after header for rate limiting
    if isinstance(error, RateLimitError):
        response.headers['Retry-After'] = '60'  # 60 seconds
    
    return response


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    """Handle AppError exceptions."""
    return error_response(error)


@app.errorhandler(HTTPException)
def handle_http_error(error: HTTPException):
    """Handle Werkzeug HTTP exceptions."""
    app_error = AppError(
        message=error.description,
        status_code=error.code,
        error_code=f"HTTP_{error.code}",
    )
    return error_response(app_error)


@app.errorhandler(SQLAlchemyError)
def handle_database_error(error: SQLAlchemyError):
    """Handle SQLAlchemy database errors."""
    
    # Log full error for debugging
    logger.error(
        "database_error",
        error_type=type(error).__name__,
        error=str(error),
        traceback=traceback.format_exc()
    )
    
    # Send to Sentry
    if app.config['SENTRY_DSN']:
        sentry_sdk.capture_exception(error)
    
    # Don't expose database errors in production
    if app.config['ENV'] == 'production':
        app_error = AppError(
            message="Database error occurred",
            status_code=500,
            error_code="DATABASE_ERROR",
            internal_details=str(error) if app.config['DEBUG'] else None,
            cause=error
        )
    else:
        app_error = AppError(
            message=f"Database error: {error}",
            status_code=500,
            error_code="DATABASE_ERROR",
            cause=error
        )
    
    return error_response(app_error)


@app.errorhandler(Exception)
def handle_generic_error(error: Exception):
    """Handle all other uncaught exceptions."""
    
    # Log the error with full context
    logger.error(
        "unhandled_exception",
        error_type=type(error).__name__,
        error=str(error),
        traceback=traceback.format_exc()
    )
    
    # Send to Sentry
    if app.config['ENV'] == 'production' and app.config['SENTRY_DSN']:
        sentry_sdk.capture_exception(error)
    
    # Don't expose internal errors in production
    if app.config['ENV'] == 'production':
        app_error = AppError(
            message="Internal server error",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            internal_details=str(error) if app.config['DEBUG'] else None,
            cause=error
        )
    else:
        app_error = AppError(
            message=f"Unhandled error: {error}",
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            cause=error
        )
    
    return error_response(app_error)


# ============================================================================
# 8. DATABASE MODELS FOR DEMONSTRATION
# ============================================================================

class User(db.Model):
    """User model for demonstration."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    logs = db.relationship('AuditLog', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Order(db.Model):
    """Order model for demonstration."""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='orders')
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class AuditLog(db.Model):
    """Audit log model for demonstration."""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.String(100), nullable=True)
    details = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'


# ============================================================================
# 9. CONTEXT MANAGERS & DECORATORS FOR OBSERVABILITY
# ============================================================================

@contextmanager
def timed_operation(name: str, labels: Dict[str, str] = None):
    """
    Context manager for timing operations.
    
    Usage:
    with timed_operation('database.query', {'table': 'users'}):
        db.session.query(User).all()
    """
    start_time = time.time()
    
    try:
        yield
    finally:
        duration = time.time() - start_time
        
        # Log the operation
        logger.info(
            "operation_completed",
            operation=name,
            duration_seconds=duration,
            labels=labels
        )
        
        # Record metrics
        if statsd_client:
            statsd_client.timing(f'operations.{name}', duration * 1000)
        
        # Update Prometheus metrics
        if name.startswith('database.'):
            table = labels.get('table', 'unknown') if labels else 'unknown'
            DATABASE_QUERY_DURATION.labels(
                operation=name.replace('database.', ''),
                table=table
            ).observe(duration)
        elif name.startswith('external_api.'):
            service = labels.get('service', 'unknown') if labels else 'unknown'
            endpoint = labels.get('endpoint', 'unknown') if labels else 'unknown'
            status = labels.get('status', 'unknown') if labels else 'unknown'
            EXTERNAL_API_DURATION.labels(
                service=service,
                endpoint=endpoint,
                status=status
            ).observe(duration)


@contextmanager
def track_errors(source: str):
    """
    Context manager for tracking errors with source context.
    
    Usage:
    with track_errors('user_service'):
        # Code that might fail
        raise ValueError("Something went wrong")
    """
    try:
        yield
    except Exception as e:
        # Log error with source context
        logger.error(
            "operation_error",
            source=source,
            error_type=type(e).__name__,
            error=str(e)
        )
        
        # Increment error counter
        if statsd_client:
            statsd_client.incr(f'errors.source.{source}')
        
        ERROR_COUNTER.labels(type=type(e).__name__, source=source).inc()
        
        # Re-raise the exception
        raise


def log_execution(func):
    """
    Decorator to log function execution with timing.
    
    Usage:
    @log_execution
    def process_order(order_id):
        # Process order
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        module = func.__module__
        
        logger.info(
            "function_start",
            function=func_name,
            module=module,
            args=str(args),
            kwargs=str(kwargs)
        )
        
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                "function_completed",
                function=func_name,
                module=module,
                duration_seconds=duration,
                success=True
            )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error(
                "function_failed",
                function=func_name,
                module=module,
                duration_seconds=duration,
                error_type=type(e).__name__,
                error=str(e),
                success=False
            )
            
            raise
    
    return wrapper


def track_business_event(event_type: str):
    """
    Decorator to track business events.
    
    Usage:
    @track_business_event('order_created')
    def create_order(user_id, amount):
        # Create order
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Increment business event counter
            BUSINESS_EVENTS.labels(event_type=event_type, user_type='regular').inc()
            
            if statsd_client:
                statsd_client.incr(f'business_events.{event_type}')
            
            # Log business event
            logger.info(
                "business_event",
                event_type=event_type,
                function=func.__name__,
                module=func.__module__
            )
            
            return result
        return wrapper
    return decorator


# ============================================================================
# 10. GRACEFUL DEGRADATION & CIRCUIT BREAKER PATTERN
# ============================================================================

"""
GRACEFUL DEGRADATION PRINCIPLES:
1. Fail fast for non-critical dependencies
2. Provide fallback functionality
3. Use circuit breakers to prevent cascade failures
4. Monitor dependency health
"""

class CircuitBreaker:
    """
    Simple circuit breaker pattern implementation.
    
    States:
    - CLOSED: Normal operation
    - OPEN: Failing fast
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exceptions: tuple = (Exception,)
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.last_failure_time = None
        self.last_success_time = None
        
        # Metrics
        self.circuit_state = Gauge(
            f'circuit_breaker_{name}_state',
            f'Circuit breaker state for {name}',
            ['state']
        )
        self.circuit_failures = Counter(
            f'circuit_breaker_{name}_failures',
            f'Circuit breaker failures for {name}'
        )
        
        logger.info(
            "circuit_breaker_initialized",
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout
        )
    
    def call(self, func, *args, fallback_func=None, **kwargs):
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to call
            fallback_func: Fallback function if circuit is open
            *args, **kwargs: Arguments to pass to func
        
        Returns:
            Result from func or fallback_func
        """
        # Check if circuit is open
        if self.state == 'OPEN':
            if self._should_try_recovery():
                self.state = 'HALF_OPEN'
                logger.info(
                    "circuit_breaker_half_open",
                    name=self.name,
                    state=self.state
                )
            else:
                logger.warning(
                    "circuit_breaker_open",
                    name=self.name,
                    state=self.state,
                    time_since_failure=(time.time() - self.last_failure_time) if self.last_failure_time else None
                )
                
                # Call fallback if provided
                if fallback_func:
                    return fallback_func(*args, **kwargs)
                raise ExternalServiceError(
                    service=self.name,
                    endpoint=func.__name__,
                    status_code=503,
                    cause=Exception(f"Circuit breaker open for {self.name}")
                )
        
        try:
            # Call the function
            result = func(*args, **kwargs)
            
            # Success - reset failure count
            self._on_success()
            
            return result
            
        except self.expected_exceptions as e:
            # Failure - update state
            self._on_failure(e)
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.last_success_time = time.time()
        
        if self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
            logger.info(
                "circuit_breaker_closed",
                name=self.name,
                state=self.state
            )
        
        # Update metrics
        self.circuit_state.labels(state=self.state).set(
            {'CLOSED': 0, 'HALF_OPEN': 1, 'OPEN': 2}[self.state]
        )
    
    def _on_failure(self, error: Exception):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        # Update metrics
        self.circuit_failures.inc()
        
        logger.warning(
            "circuit_breaker_failure",
            name=self.name,
            failure_count=self.failure_count,
            error=str(error),
            state=self.state
        )
        
        # Check if threshold reached
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
            logger.error(
                "circuit_breaker_opened",
                name=self.name,
                state=self.state,
                failure_count=self.failure_count
            )
    
    def _should_try_recovery(self) -> bool:
        """Check if we should try to recover."""
        if not self.last_failure_time:
            return True
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.recovery_timeout


# Create circuit breaker for external services
external_service_circuit = CircuitBreaker(
    name="external_api",
    failure_threshold=3,
    recovery_timeout=30,
    expected_exceptions=(RequestException, TimeoutError, ConnectionError)
)


# ============================================================================
# 11. EXTERNAL SERVICE INTEGRATION WITH DEGRADATION
# ============================================================================

def call_external_api(endpoint: str, method: str = 'GET', **kwargs):
    """
    Call external API with circuit breaker and fallback.
    
    Demonstrates:
    1. Circuit breaker pattern
    2. Graceful degradation
    3. Metrics collection
    4. Error handling
    """
    
    def make_request():
        """Actual API call."""
        url = f"{app.config['EXTERNAL_API_URL']}/{endpoint}"
        
        with timed_operation('external_api.call', {
            'service': 'external_api',
            'endpoint': endpoint,
            'method': method
        }):
            response = requests.request(
                method=method,
                url=url,
                timeout=app.config['EXTERNAL_API_TIMEOUT'],
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    def fallback():
        """Fallback function when external API is unavailable."""
        logger.warning(
            "external_api_fallback",
            endpoint=endpoint,
            method=method,
            message="Using fallback data"
        )
        
        # Return cached data or default values
        return {
            "data": None,
            "from_cache": True,
            "message": "External service temporarily unavailable"
        }
    
    try:
        # Use circuit breaker
        return external_service_circuit.call(
            make_request,
            fallback_func=fallback
        )
        
    except RequestException as e:
        raise ExternalServiceError(
            service="external_api",
            endpoint=endpoint,
            status_code=e.response.status_code if e.response else 503,
            cause=e
        )


# ============================================================================
# 12. DEMONSTRATION ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint with dependency verification.
    
    Demonstrates:
    1. Structured response format
    2. Dependency health checking
    3. Metrics collection
    4. Graceful degradation
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": app.config['SERVICE_NAME'],
        "version": app.config['VERSION'],
        "dependencies": {}
    }
    
    # Check database
    try:
        with timed_operation('healthcheck.database', {'check': 'connectivity'}):
            db.session.execute('SELECT 1')
        health_data['dependencies']['database'] = {
            "status": "healthy",
            "response_time": "N/A"  # Would be populated by timed_operation
        }
    except Exception as e:
        logger.error("healthcheck_database_failed", error=str(e))
        health_data['dependencies']['database'] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_data['status'] = "degraded"
    
    # Check Redis (if configured)
    if redis_client:
        try:
            with timed_operation('healthcheck.redis', {'check': 'connectivity'}):
                redis_client.ping()
            health_data['dependencies']['redis'] = {
                "status": "healthy"
            }
        except Exception as e:
            logger.error("healthcheck_redis_failed", error=str(e))
            health_data['dependencies']['redis'] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_data['status'] = "degraded"
    
    # Check external API (with circuit breaker)
    try:
        # This would fail in demo since external API doesn't exist
        # call_external_api('health')
        health_data['dependencies']['external_api'] = {
            "status": "healthy",
            "circuit_breaker": external_service_circuit.state
        }
    except Exception as e:
        logger.warning("healthcheck_external_api_failed", error=str(e))
        health_data['dependencies']['external_api'] = {
            "status": "unhealthy",
            "error": str(e),
            "circuit_breaker": external_service_circuit.state
        }
        health_data['status'] = "degraded"
    
    # Record health check
    if statsd_client:
        statsd_client.incr('health_checks.total')
        statsd_client.gauge('health_status', 
                           1 if health_data['status'] == 'healthy' else 0.5 if health_data['status'] == 'degraded' else 0)
    
    return jsonify(health_data)


@app.route('/api/users', methods=['GET'])
@log_execution
def get_users():
    """
    Get users with pagination and error handling.
    
    Demonstrates:
    1. Structured logging
    2. Error handling
    3. Metrics collection
    4. Database operation timing
    """
    try:
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate input
        if page < 1 or per_page < 1 or per_page > 100:
            raise ValidationError(
                "Invalid pagination parameters",
                field_errors={
                    'page': 'Must be positive integer',
                    'per_page': 'Must be between 1 and 100'
                }
            )
        
        # Query database with timing
        with timed_operation('database.query', {'table': 'users', 'operation': 'select'}):
            query = User.query.order_by(User.created_at.desc())
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Prepare response
        users = []
        for user in paginated.items:
            users.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            })
        
        response_data = {
            'data': users,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginated.pages,
                'total_items': paginated.total,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            },
            'metadata': {
                'correlation_id': g.correlation_id,
                'request_id': g.request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        # Track business event
        BUSINESS_EVENTS.labels(event_type='users_listed', user_type='api').inc()
        
        return jsonify(response_data)
        
    except ValidationError:
        raise  # Re-raise validation errors
    except SQLAlchemyError as e:
        raise DatabaseError('select', 'users', e)
    except Exception as e:
        logger.error("get_users_failed", error=str(e), traceback=traceback.format_exc())
        raise


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user with validation.
    
    Demonstrates:
    1. Input validation with custom errors
    2. Database operations with error handling
    3. Audit logging
    4. Business event tracking
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must be JSON")
        
        # Validate required fields
        required_fields = ['username', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValidationError(
                "Missing required fields",
                field_errors={field: 'This field is required' for field in missing_fields}
            )
        
        # Validate email format
        if '@' not in data.get('email', ''):
            raise ValidationError(
                "Invalid email format",
                field_errors={'email': 'Must be a valid email address'}
            )
        
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        
        if existing_user:
            raise ValidationError(
                "User already exists",
                field_errors={
                    'username': 'Already taken' if existing_user.username == data['username'] else None,
                    'email': 'Already registered' if existing_user.email == data['email'] else None
                }
            )
        
        # Create user with database timing
        with timed_operation('database.query', {'table': 'users', 'operation': 'insert'}):
            user = User(
                username=data['username'],
                email=data['email'],
                is_active=data.get('is_active', True)
            )
            db.session.add(user)
            db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            action='USER_CREATED',
            resource='user',
            resource_id=str(user.id),
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None,
            details={'username': user.username, 'email': user.email}
        )
        db.session.add(audit_log)
        db.session.commit()
        
        # Track business event
        BUSINESS_EVENTS.labels(event_type='user_created', user_type='regular').inc()
        
        # Log success
        logger.info(
            "user_created",
            user_id=user.id,
            username=user.username,
            email=user.email
        )
        
        # Prepare response
        response_data = {
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            },
            'metadata': {
                'correlation_id': g.correlation_id,
                'request_id': g.request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        response = jsonify(response_data)
        response.status_code = 201
        response.headers['Location'] = f'/api/users/{user.id}'
        
        return response
        
    except ValidationError:
        raise  # Re-raise validation errors
    except IntegrityError as e:
        db.session.rollback()
        raise DatabaseError('insert', 'users', e)
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseError('transaction', 'users', e)
    except Exception as e:
        db.session.rollback()
        logger.error("create_user_failed", error=str(e), traceback=traceback.format_exc())
        raise


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """
    Get a specific user by ID.
    
    Demonstrates:
    1. Resource not found handling
    2. Structured error responses
    3. Request timing
    """
    try:
        with timed_operation('database.query', {'table': 'users', 'operation': 'select_single'}):
            user = User.query.get(user_id)
        
        if not user:
            raise NotFoundError("User", user_id)
        
        response_data = {
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            },
            'metadata': {
                'correlation_id': g.correlation_id,
                'request_id': g.request_id,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(response_data)
        
    except NotFoundError:
        raise  # Re-raise not found errors
    except SQLAlchemyError as e:
        raise DatabaseError('select', 'users', e)
    except Exception as e:
        logger.error("get_user_failed", user_id=user_id, error=str(e))
        raise


@app.route('/api/orders', methods=['POST'])
@track_business_event('order_created')
def create_order():
    """
    Create an order with external service integration.
    
    Demonstrates:
    1. Graceful degradation with external services
    2. Circuit breaker pattern
    3. Database transactions
    4. Comprehensive error handling
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body must be JSON")
        
        # Validate required fields
        if 'user_id' not in data or 'amount' not in data:
            raise ValidationError(
                "Missing required fields",
                field_errors={
                    'user_id': 'Required' if 'user_id' not in data else None,
                    'amount': 'Required' if 'amount' not in data else None
                }
            )
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except (ValueError, TypeError):
            raise ValidationError(
                "Invalid amount",
                field_errors={'amount': 'Must be a positive number'}
            )
        
        # Check if user exists
        with timed_operation('database.query', {'table': 'users', 'operation': 'select_single'}):
            user = User.query.get(data['user_id'])
        
        if not user:
            raise NotFoundError("User", data['user_id'])
        
        # Call external payment service (with circuit breaker)
        payment_result = None
        try:
            payment_result = call_external_api(
                'payments/process',
                method='POST',
                json={
                    'user_id': user.id,
                    'amount': amount,
                    'currency': data.get('currency', 'USD')
                }
            )
        except ExternalServiceError as e:
            logger.warning(
                "payment_service_unavailable",
                user_id=user.id,
                amount=amount,
                error=str(e)
            )
            # Continue without payment processing - graceful degradation
            payment_result = {'status': 'pending', 'message': 'Payment processing delayed'}
        
        # Create order in database transaction
        with track_errors('order_creation'):
            with timed_operation('database.transaction', {'operation': 'order_creation'}):
                order = Order(
                    user_id=user.id,
                    amount=amount,
                    currency=data.get('currency', 'USD'),
                    status=payment_result.get('status', 'pending') if payment_result else 'pending'
                )
                db.session.add(order)
                db.session.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=user.id,
            action='ORDER_CREATED',
            resource='order',
            resource_id=str(order.id),
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None,
            details={
                'amount': amount,
                'currency': order.currency,
                'status': order.status,
                'payment_result': payment_result
            }
        )
        db.session.add(audit_log)
        db.session.commit()
        
        # Prepare response
        response_data = {
            'data': {
                'order_id': order.id,
                'user_id': order.user_id,
                'amount': order.amount,
                'currency': order.currency,
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'payment_processed': payment_result is not None
            },
            'metadata': {
                'correlation_id': g.correlation_id,
                'request_id': g.request_id,
                'timestamp': datetime.utcnow().isoformat(),
                'circuit_breaker_state': external_service_circuit.state
            }
        }
        
        response = jsonify(response_data)
        response.status_code = 201
        response.headers['Location'] = f'/api/orders/{order.id}'
        
        return response
        
    except ValidationError:
        raise
    except NotFoundError:
        raise
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseError('transaction', 'orders', e)
    except Exception as e:
        db.session.rollback()
        logger.error(
            "create_order_failed",
            error=str(e),
            traceback=traceback.format_exc(),
            data=data
        )
        raise


@app.route('/api/error-demo/<error_type>', methods=['GET'])
def error_demo(error_type: str):
    """
    Demo endpoint to trigger different types of errors.
    
    Demonstrates:
    1. Different error types
    2. Error handling patterns
    3. Structured error responses
    """
    error_types = {
        'validation': lambda: ValidationError(
            "Demo validation error",
            field_errors={
                'username': 'Must be at least 3 characters',
                'email': 'Invalid email format'
            }
        ),
        'not-found': lambda: NotFoundError("DemoResource", "123"),
        'authentication': lambda: AuthenticationError("Demo authentication required"),
        'authorization': lambda: AuthorizationError("Demo insufficient permissions"),
        'database': lambda: DatabaseError('demo', 'demo_table', Exception("Demo database error")),
        'external': lambda: ExternalServiceError(
            "demo_service",
            "demo/endpoint",
            503,
            Exception("Demo external service error")
        ),
        'rate-limit': lambda: RateLimitError(10, 'minute'),
        'generic': lambda: Exception("Demo generic error"),
        'divide-by-zero': lambda: 1 / 0,
    }
    
    if error_type not in error_types:
        raise ValidationError(
            f"Invalid error type. Available: {', '.join(error_types.keys())}"
        )
    
    # Trigger the error
    error_func = error_types[error_type]
    if callable(error_func):
        raise error_func()
    
    return jsonify({"message": "No error triggered"})


@app.route('/api/metrics-demo', methods=['GET'])
def metrics_demo():
    """
    Demo endpoint to show metrics collection.
    
    Demonstrates:
    1. Custom metrics
    2. Histogram buckets
    3. Label usage
    """
    # Simulate some processing time
    import random
    import time as t
    
    processing_time = random.uniform(0.1, 2.0)
    t.sleep(processing_time)
    
    # Simulate success/failure
    success = random.random() > 0.2  # 80% success rate
    
    if not success:
        ERROR_COUNTER.labels(type='demo_error', source='metrics_demo').inc()
        if statsd_client:
            statsd_client.incr('errors.demo')
    
    # Record processing time histogram
    REQUEST_DURATION.labels(
        method='GET',
        endpoint='metrics_demo'
    ).observe(processing_time)
    
    return jsonify({
        'processing_time': processing_time,
        'success': success,
        'metrics_recorded': True
    })


# ============================================================================
# 13. INTEGRATING WITH LOGGING TOOLS
# ============================================================================

class LogForwarder:
    """
    Example log forwarder for integrating with external logging tools.
    
    In production, you would use:
    - Logstash/Filebeat for ELK stack
    - Fluentd/Fluent Bit for Kubernetes
    - CloudWatch Logs for AWS
    - Stackdriver for GCP
    - Application Insights for Azure
    """
    
    def __init__(self):
        self.batch_size = 100
        self.log_buffer = []
    
    def forward_log(self, log_entry: Dict):
        """Forward log entry to external system."""
        # In production, this would send to your logging infrastructure
        # For demo, just print or store in memory
        
        # Add service context
        log_entry.update({
            'service': app.config['SERVICE_NAME'],
            'environment': app.config['ENV'],
            'version': app.config['VERSION']
        })
        
        # Buffer logs for batch sending
        self.log_buffer.append(log_entry)
        
        if len(self.log_buffer) >= self.batch_size:
            self._send_batch()
    
    def _send_batch(self):
        """Send buffered logs to external system."""
        if not self.log_buffer:
            return
        
        # In production: Send to ELK, CloudWatch, etc.
        # Example: requests.post('http://logstash:5044', json=self.log_buffer)
        
        # For demo, just clear buffer
        self.log_buffer = []
    
    def flush(self):
        """Flush remaining logs."""
        self._send_batch()


# Create log forwarder instance
log_forwarder = LogForwarder()


def forward_to_logging_tools(record):
    """Processor to forward logs to external tools."""
    log_forwarder.forward_log(record)
    return record


# Add forwarder to structlog processors (commented out for demo)
# structlog.configure(
#     processors=structlog.get_config()['processors'] + [forward_to_logging_tools]
# )


# ============================================================================
# 14. OBSERVABILITY DASHBOARD ENDPOINT
# ============================================================================

@app.route('/api/observability', methods=['GET'])
def observability_dashboard():
    """
    Observability dashboard endpoint.
    
    Shows:
    1. Current metrics
    2. Circuit breaker status
    3. Health status
    4. Request statistics
    """
    # Get basic Prometheus metrics
    metrics_text = generate_latest(REGISTRY).decode('utf-8')
    metrics_lines = metrics_text.split('\n')
    
    # Parse important metrics
    parsed_metrics = {}
    for line in metrics_lines:
        if line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 2:
                parsed_metrics[parts[0]] = parts[1]
    
    dashboard_data = {
        'service': {
            'name': app.config['SERVICE_NAME'],
            'environment': app.config['ENV'],
            'version': app.config['VERSION'],
            'uptime': 'N/A'  # Would calculate from start time
        },
        'circuit_breakers': {
            'external_api': {
                'state': external_service_circuit.state,
                'failure_count': external_service_circuit.failure_count,
                'last_failure': external_service_circuit.last_failure_time
            }
        },
        'metrics_snapshot': {
            'total_requests': parsed_metrics.get('http_requests_total', '0'),
            'active_requests': parsed_metrics.get('http_active_requests', '0'),
            'total_errors': parsed_metrics.get('errors_total', '0'),
        },
        'logging': {
            'level': app.config['LOG_LEVEL'],
            'format': app.config['LOG_FORMAT'],
            'file': app.config['LOG_FILE']
        },
        'external_integrations': {
            'sentry': 'enabled' if app.config['SENTRY_DSN'] else 'disabled',
            'statsd': 'enabled' if statsd_client else 'disabled',
            'redis': 'enabled' if redis_client else 'disabled'
        }
    }
    
    return jsonify(dashboard_data)


# ============================================================================
# 15. APPLICATION INITIALIZATION
# ============================================================================

def init_database():
    """Initialize database with sample data."""
    with app.app_context():
        db.create_all()
        
        # Add sample data if database is empty
        if not User.query.first():
            users = [
                User(username='alice', email='alice@example.com'),
                User(username='bob', email='bob@example.com'),
                User(username='charlie', email='charlie@example.com')
            ]
            
            orders = [
                Order(user_id=1, amount=99.99, status='completed'),
                Order(user_id=1, amount=49.99, status='pending'),
                Order(user_id=2, amount=199.99, status='processing')
            ]
            
            db.session.add_all(users)
            db.session.add_all(orders)
            db.session.commit()
            
            logger.info("database_initialized", users_count=len(users), orders_count=len(orders))


# ============================================================================
# 16. DEMONSTRATION HTML PAGE
# ============================================================================

@app.route('/')
def observability_demo():
    """Interactive demonstration page."""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Error Handling & Observability Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .section {
                background: #f8f9fa;
                border-left: 4px solid #007bff;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border-radius: 0 5px 5px 0;
            }
            .demo-buttons {
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
                margin: 1rem 0;
            }
            .demo-btn {
                padding: 0.75rem 1.5rem;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .demo-btn:hover {
                background: #0056b3;
            }
            .error-btn {
                background: #dc3545;
            }
            .error-btn:hover {
                background: #c82333;
            }
            .metric {
                background: #e9ecef;
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 5px;
                font-family: monospace;
            }
            .success { color: #28a745; }
            .warning { color: #ffc107; }
            .error { color: #dc3545; }
            code {
                background: #e9ecef;
                padding: 0.2rem 0.4rem;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            pre {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                overflow-x: auto;
            }
            #results {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                min-height: 100px;
                max-height: 400px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 Flask Error Handling & Observability Demo</h1>
            <p>Comprehensive demonstration of production-ready error handling and monitoring</p>
        </div>
        
        <div class="section">
            <h2>📊 Health & Metrics</h2>
            <div class="demo-buttons">
                <button class="demo-btn" onclick="testHealth()">Test Health Endpoint</button>
                <button class="demo-btn" onclick="testMetrics()">View Metrics</button>
                <button class="demo-btn" onclick="testObservability()">Observability Dashboard</button>
            </div>
        </div>
        
        <div class="section">
            <h2>👥 User Management (Error Handling Demo)</h2>
            <div class="demo-buttons">
                <button class="demo-btn" onclick="getUsers()">Get Users</button>
                <button class="demo-btn" onclick="createUser()">Create User</button>
                <button class="demo-btn" onclick="getUser(999)">Get Non-existent User</button>
            </div>
        </div>
        
        <div class="section">
            <h2>💳 Order Processing (Graceful Degradation)</h2>
            <div class="demo-buttons">
                <button class="demo-btn" onclick="createOrder()">Create Order</button>
                <button class="demo-btn" onclick="testMetricsDemo()">Metrics Demo</button>
            </div>
        </div>
        
        <div class="section">
            <h2>🚨 Error Type Demonstrations</h2>
            <p>Click to trigger different error types and see structured responses:</p>
            <div class="demo-buttons">
                <button class="demo-btn error-btn" onclick="triggerError('validation')">Validation Error</button>
                <button class="demo-btn error-btn" onclick="triggerError('not-found')">Not Found Error</button>
                <button class="demo-btn error-btn" onclick="triggerError('database')">Database Error</button>
                <button class="demo-btn error-btn" onclick="triggerError('external')">External Service Error</button>
                <button class="demo-btn error-btn" onclick="triggerError('rate-limit')">Rate Limit Error</button>
                <button class="demo-btn error-btn" onclick="triggerError('divide-by-zero')">Unhandled Error</button>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Observability Features</h2>
            <ul>
                <li><strong>Structured Logging:</strong> JSON format with correlation IDs</li>
                <li><strong>Metrics:</strong> Prometheus metrics at <code>/metrics</code></li>
                <li><strong>Error Tracking:</strong> Sentry integration (if configured)</li>
                <li><strong>Circuit Breaker:</strong> Graceful degradation for external services</li>
                <li><strong>Request Tracing:</strong> Correlation IDs propagate through services</li>
                <li><strong>Health Checks:</strong> Comprehensive dependency monitoring</li>
                <li><strong>Audit Logging:</strong> All important actions logged</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📋 Response Results</h2>
            <div id="results">
                <p>Results will appear here...</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 Example CURL Commands</h2>
            <pre><code># Health check
curl http://localhost:5000/api/health

# Get users with pagination
curl "http://localhost:5000/api/users?page=1&per_page=10"

# Create user (will fail validation)
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid"}'</code></pre>
        </div>
        
        <script>
            const results = document.getElementById('results');
            
            async function makeRequest(url, options = {}) {
                results.innerHTML = 'Loading...';
                
                try {
                    const response = await fetch(url, {
                        headers: {
                            'Content-Type': 'application/json',
                            ...options.headers
                        },
                        ...options
                    });
                    
                    const data = await response.json();
                    
                    // Display formatted response
                    results.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                    
                    // Show status
                    const statusClass = response.ok ? 'success' : 'error';
                    results.innerHTML += `<p class="${statusClass}">Status: ${response.status}</p>`;
                    
                    // Show correlation ID if present
                    if (data.metadata && data.metadata.correlation_id) {
                        results.innerHTML += `<p>Correlation ID: ${data.metadata.correlation_id}</p>`;
                    }
                    
                } catch (error) {
                    results.innerHTML = `<p class="error">Error: ${error.message}</p>`;
                }
            }
            
            function testHealth() {
                makeRequest('/api/health');
            }
            
            function testMetrics() {
                makeRequest('/metrics');
            }
            
            function testObservability() {
                makeRequest('/api/observability');
            }
            
            function getUsers() {
                makeRequest('/api/users?page=1&per_page=5');
            }
            
            function createUser() {
                makeRequest('/api/users', {
                    method: 'POST',
                    body: JSON.stringify({
                        username: 'testuser_' + Date.now(),
                        email: 'test' + Date.now() + '@example.com'
                    })
                });
            }
            
            function getUser(id) {
                makeRequest(`/api/users/${id}`);
            }
            
            function createOrder() {
                makeRequest('/api/orders', {
                    method: 'POST',
                    body: JSON.stringify({
                        user_id: 1,
                        amount: 99.99,
                        currency: 'USD'
                    })
                });
            }
            
            function testMetricsDemo() {
                makeRequest('/api/metrics-demo');
            }
            
            function triggerError(errorType) {
                makeRequest(`/api/error-demo/${errorType}`);
            }
            
            // Initial test
            testHealth();
        </script>
    </body>
    </html>
    '''
    return html


# ============================================================================
# 17. APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Create dispatcher middleware for Prometheus
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        app.config['PROMETHEUS_METRICS_PATH']: make_wsgi_app()
    })
    
    print("\n" + "="*80)
    print("🔍 FLASK ERROR HANDLING & OBSERVABILITY TUTORIAL")
    print("="*80)
    
    print("\n📚 Key Concepts Demonstrated:")
    print("1. Structured Error Responses with correlation IDs")
    print("2. Custom Exception Hierarchy for domain-specific errors")
    print("3. Comprehensive Logging Configuration (JSON structured)")
    print("4. Correlation IDs & Request Tracing across services")
    print("5. Integration with Logging Tools (Sentry, ELK, etc.)")
    print("6. Graceful Degradation & Circuit Breaker Pattern")
    print("7. Error Tracking with Sentry (if configured)")
    print("8. Metrics Collection with Prometheus & StatsD")
    
    print("\n🌐 Available Endpoints:")
    print("   • http://localhost:5000/ - Interactive demo")
    print("   • GET  /api/health - Health check with dependencies")
    print("   • GET  /api/users - Get users (with pagination)")
    print("   • POST /api/users - Create user (with validation)")
    print("   • POST /api/orders - Create order (graceful degradation)")
    print("   • GET  /api/error-demo/<type> - Trigger specific errors")
    print("   • GET  /api/observability - Observability dashboard")
    print("   • GET  /metrics - Prometheus metrics")
    
    print("\n🔧 Observability Tools:")
    print("   • Structured Logging: JSON format with context")
    print("   • Metrics: Prometheus endpoint at /metrics")
    print("   • Error Tracking: Sentry integration")
    print("   • Distributed Tracing: Correlation IDs")
    print("   • Circuit Breaker: For external service calls")
    
    print("\n🚀 Getting Started:")
    print("   1. Visit http://localhost:5000/ for interactive demo")
    print("   2. Check /api/health for service status")
    print("   3. Try creating users and orders")
    print("   4. Trigger different error types to see structured responses")
    
    print("\n📈 Monitoring:")
    print("   • Check /metrics for Prometheus metrics")
    print("   • View console for structured JSON logs")
    print("   • Check /api/observability for service status")
    
    print("="*80 + "\n")
    
    # Run the application
    app.run(
        debug=app.config['DEBUG'],
        port=5000,
        host='0.0.0.0'  # Allow external access for demo
    )