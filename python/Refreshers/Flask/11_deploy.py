"""
COMPREHENSIVE FLASK DEPLOYMENT & PRODUCTION READINESS TUTORIAL
This application demonstrates professional deployment patterns and production best practices.
"""

import os
import sys
import json
import logging
import signal
import time
import threading
import subprocess
import socket
import multiprocessing
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from functools import wraps
from contextlib import contextmanager
import secrets
import psutil
import redis
from redis.exceptions import RedisError
import docker
import kubernetes
import requests
from requests.exceptions import RequestException
import prometheus_client
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from healthcheck import HealthCheck, EnvironmentDump

# Flask and related imports
from flask import Flask, request, jsonify, make_response, g, current_app, abort
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate
from sqlalchemy import event, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

# ============================================================================
# 1. ENVIRONMENT-SPECIFIC CONFIGURATION
# ============================================================================

"""
CONFIGURATION MANAGEMENT PRINCIPLES:
1. Never hardcode secrets in code
2. Use environment variables for configuration
3. Different configurations for different environments
4. Use .env files for local development
5. Use secret management in production (Vault, AWS Secrets Manager, etc.)
"""

class Config:
    """Base configuration with sensible defaults."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    DEBUG = False
    TESTING = False
    
    # Security settings
    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/flask_prod'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', '10')),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', '3600')),
        'pool_pre_ping': os.environ.get('DB_POOL_PRE_PING', 'true').lower() == 'true',
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', '20')),
        'connect_args': {
            'connect_timeout': int(os.environ.get('DB_CONNECT_TIMEOUT', '10')),
            'application_name': os.environ.get('APP_NAME', 'flask_app'),
        }
    }
    
    # Redis settings
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_CACHE_TTL = int(os.environ.get('REDIS_CACHE_TTL', '300'))  # 5 minutes
    
    # Cache settings
    CACHE_TYPE = 'redis' if os.environ.get('REDIS_URL') else 'simple'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))
    
    # External services
    EXTERNAL_API_URL = os.environ.get('EXTERNAL_API_URL', 'https://api.example.com')
    EXTERNAL_API_TIMEOUT = int(os.environ.get('EXTERNAL_API_TIMEOUT', '10'))
    
    # Observability
    SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'json')
    
    # Application settings
    APP_NAME = os.environ.get('APP_NAME', 'flask-production-demo')
    VERSION = os.environ.get('APP_VERSION', '1.0.0')
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_STORAGE_URL = os.environ.get('RATE_LIMIT_STORAGE_URL', 'memory://')
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Content-Security-Policy': (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' https://api.example.com;"
        )
    }
    
    # Deployment settings
    DEPLOYMENT_ID = os.environ.get('DEPLOYMENT_ID', socket.gethostname())
    POD_NAME = os.environ.get('POD_NAME', 'local')
    NAMESPACE = os.environ.get('NAMESPACE', 'default')
    
    # Graceful shutdown settings
    GRACEFUL_SHUTDOWN_TIMEOUT = int(os.environ.get('GRACEFUL_SHUTDOWN_TIMEOUT', '30'))
    
    # Health check settings
    HEALTH_CHECK_PATH = os.environ.get('HEALTH_CHECK_PATH', '/health')
    READINESS_PATH = os.environ.get('READINESS_PATH', '/ready')
    LIVENESS_PATH = os.environ.get('LIVENESS_PATH', '/live')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = True
    ENVIRONMENT = 'development'
    
    # Less secure settings for development
    SESSION_COOKIE_SECURE = False
    
    # Log more details
    LOG_LEVEL = 'DEBUG'
    
    # Use simpler cache for development
    CACHE_TYPE = 'simple'
    
    # Disable some security features for easier debugging
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
    }
    
    # Local database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/flask_dev'
    )


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    ENVIRONMENT = 'testing'
    
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF protection for testing
    WTF_CSRF_ENABLED = False
    
    # Use simple cache
    CACHE_TYPE = 'simple'
    
    # Mock external services
    EXTERNAL_API_URL = 'http://mock-api:8080'


class StagingConfig(Config):
    """Staging configuration."""
    DEBUG = False
    ENVIRONMENT = 'staging'
    
    # Staging database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://staging_user:password@staging-db:5432/flask_staging'
    )
    
    # Less aggressive caching
    CACHE_DEFAULT_TIMEOUT = 60


class ProductionConfig(Config):
    """Production configuration - most secure."""
    DEBUG = False
    ENVIRONMENT = 'production'
    
    # Production database - must come from environment
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
    # Strict security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Aggressive caching
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Enable all security features
    RATE_LIMIT_ENABLED = True


# Configuration mapping
configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig,
}

# Determine which configuration to use
env = os.environ.get('FLASK_ENV', 'production').lower()
config_class = configs.get(env, configs['default'])

# Initialize Flask app with configuration
app = Flask(__name__)
app.config.from_object(config_class)

# Apply proxy fix for running behind reverse proxies
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,  # Trust one proxy (adjust based on your infrastructure)
    x_proto=1,
    x_host=1,
    x_port=1,
    x_prefix=1
)


# ============================================================================
# 2. DATABASE & EXTENSIONS INITIALIZATION
# ============================================================================

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Redis cache if configured
cache = Cache(app)

# Initialize Redis connection pool
redis_client = None
if app.config['REDIS_URL']:
    try:
        redis_client = redis.from_url(
            app.config['REDIS_URL'],
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            max_connections=int(os.environ.get('REDIS_MAX_CONNECTIONS', '50'))
        )
        # Test connection
        redis_client.ping()
        app.logger.info(f"Redis connected to {app.config['REDIS_URL']}")
    except RedisError as e:
        app.logger.error(f"Redis connection failed: {e}")
        redis_client = None


# ============================================================================
# 3. DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for demonstration."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Order(db.Model):
    """Order model for demonstration."""
    
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='orders')
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class DeploymentLog(db.Model):
    """Log deployment events."""
    
    __tablename__ = 'deployment_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.String(100), nullable=False, index=True)
    pod_name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    environment = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # startup, shutdown, health_check
    event_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<DeploymentLog {self.event_type} - {self.pod_name}>'


# ============================================================================
# 4. APPLICATION METRICS
# ============================================================================

"""
PRODUCTION METRICS TO MONITOR:
1. Request rate and latency
2. Error rates
3. Resource utilization (CPU, memory)
4. Database connection pool status
5. Cache hit rates
6. External service availability
"""

# Prometheus metrics
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status']
)

REQUEST_COUNTER = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of active HTTP requests'
)

ERROR_COUNTER = Counter(
    'errors_total',
    'Total number of errors',
    ['type', 'endpoint']
)

DATABASE_CONNECTIONS = Gauge(
    'database_connections',
    'Number of database connections',
    ['state']  # active, idle, total
)

REDIS_CONNECTIONS = Gauge(
    'redis_connections',
    'Number of Redis connections'
)

MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)

DEPLOYMENT_EVENTS = Counter(
    'deployment_events_total',
    'Deployment events',
    ['environment', 'event_type']
)


# ============================================================================
# 5. HEALTH CHECKS & READINESS/LIVENESS PROBES
# ============================================================================

"""
KUBERNETES PROBES:
- Readiness: Is the application ready to receive traffic?
- Liveness: Is the application running correctly?
- Startup: Has the application started successfully?

HEALTH CHECK PATTERNS:
1. Check all dependencies (database, cache, external services)
2. Check application-specific logic
3. Return detailed status for each component
4. Include version and deployment information
"""

class HealthChecker:
    """Comprehensive health checking system."""
    
    def __init__(self):
        self.checks = []
        self.environment_data = {}
    
    def add_check(self, name: str, check_func: callable):
        """Add a health check."""
        self.checks.append((name, check_func))
    
    def add_environment_data(self, name: str, data_func: callable):
        """Add environment data."""
        self.environment_data[name] = data_func
    
    def check_all(self) -> Dict[str, Any]:
        """Run all health checks and return results."""
        results = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {},
            'environment': self._get_environment_data(),
            'metadata': self._get_metadata()
        }
        
        for name, check_func in self.checks:
            try:
                check_result = check_func()
                results['checks'][name] = {
                    'status': 'healthy',
                    'output': check_result
                }
            except Exception as e:
                results['checks'][name] = {
                    'status': 'unhealthy',
                    'output': str(e)
                }
                results['status'] = 'unhealthy'
        
        return results
    
    def _get_environment_data(self) -> Dict[str, Any]:
        """Collect environment data."""
        data = {}
        for name, data_func in self.environment_data.items():
            try:
                data[name] = data_func()
            except Exception as e:
                data[name] = f"Error: {e}"
        return data
    
    def _get_metadata(self) -> Dict[str, Any]:
        """Get application metadata."""
        return {
            'app_name': app.config['APP_NAME'],
            'version': app.config['VERSION'],
            'environment': app.config['ENVIRONMENT'],
            'deployment_id': app.config['DEPLOYMENT_ID'],
            'pod_name': app.config['POD_NAME'],
            'namespace': app.config['NAMESPACE']
        }


# Initialize health checker
health_checker = HealthChecker()

# Add database health check
def check_database():
    """Check database connectivity and performance."""
    try:
        # Test connection
        with db.engine.connect() as conn:
            result = conn.execute(text('SELECT 1')).scalar()
            if result != 1:
                raise Exception('Database query failed')
        
        # Get connection pool stats (if supported)
        try:
            pool = db.engine.pool
            if hasattr(pool, 'status'):
                return {
                    'connected': True,
                    'pool_size': pool.size(),
                    'checked_out': pool.checkedout(),
                    'overflow': pool.overflow()
                }
        except:
            pass
        
        return {'connected': True}
    except Exception as e:
        raise Exception(f'Database connection failed: {e}')


# Add Redis health check
def check_redis():
    """Check Redis connectivity."""
    if not redis_client:
        return {'available': False, 'reason': 'Redis not configured'}
    
    try:
        # Test connection and basic operations
        redis_client.ping()
        
        # Test set/get
        test_key = f'health_check:{datetime.utcnow().isoformat()}'
        redis_client.setex(test_key, 10, 'test_value')
        value = redis_client.get(test_key)
        redis_client.delete(test_key)
        
        if value != 'test_value':
            raise Exception('Redis data integrity check failed')
        
        # Get Redis info
        info = redis_client.info()
        return {
            'available': True,
            'version': info.get('redis_version'),
            'connected_clients': info.get('connected_clients'),
            'used_memory': info.get('used_memory_human'),
            'uptime': info.get('uptime_in_seconds')
        }
    except Exception as e:
        raise Exception(f'Redis connection failed: {e}')


# Add external service health check
def check_external_service():
    """Check external service availability."""
    try:
        response = requests.get(
            f"{app.config['EXTERNAL_API_URL']}/health",
            timeout=5
        )
        response.raise_for_status()
        return {
            'available': True,
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except Exception as e:
        return {
            'available': False,
            'error': str(e)
        }


# Add disk space check
def check_disk_space():
    """Check available disk space."""
    try:
        disk = psutil.disk_usage('/')
        return {
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent_used': disk.percent
        }
    except Exception as e:
        raise Exception(f'Disk check failed: {e}')


# Add memory check
def check_memory():
    """Check system memory."""
    try:
        memory = psutil.virtual_memory()
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'percent_used': memory.percent,
            'process_memory_mb': round(psutil.Process().memory_info().rss / (1024**2), 2)
        }
    except Exception as e:
        raise Exception(f'Memory check failed: {e}')


# Add application-specific check
def check_application_logic():
    """Check application-specific logic."""
    try:
        # Example: Check if we can perform a simple database operation
        user_count = User.query.count()
        order_count = Order.query.count()
        
        return {
            'users_count': user_count,
            'orders_count': order_count,
            'status': 'operational'
        }
    except Exception as e:
        raise Exception(f'Application logic check failed: {e}')


# Add environment data providers
def get_system_info():
    """Get system information."""
    return {
        'hostname': socket.gethostname(),
        'python_version': sys.version,
        'platform': sys.platform,
        'cpu_count': multiprocessing.cpu_count(),
        'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
    }


def get_application_info():
    """Get application information."""
    return {
        'flask_version': '2.0.1',  # This would be imported
        'sqlalchemy_version': '1.4.0',  # This would be imported
        'start_time': app_start_time.isoformat() if 'app_start_time' in globals() else None,
        'uptime_seconds': (datetime.utcnow() - app_start_time).total_seconds() if 'app_start_time' in globals() else None
    }


# Register all checks and environment data
health_checker.add_check('database', check_database)
health_checker.add_check('redis', check_redis)
health_checker.add_check('external_service', check_external_service)
health_checker.add_check('disk_space', check_disk_space)
health_checker.add_check('memory', check_memory)
health_checker.add_check('application_logic', check_application_logic)

health_checker.add_environment_data('system', get_system_info)
health_checker.add_environment_data('application', get_application_info)

# Track application start time
app_start_time = datetime.utcnow()

# Health check endpoints
@app.route('/health', methods=['GET'])
def health():
    """
    Comprehensive health check endpoint.
    
    Returns detailed health status of all dependencies.
    """
    health_data = health_checker.check_all()
    status_code = 200 if health_data['status'] == 'healthy' else 503
    
    response = jsonify(health_data)
    response.status_code = status_code
    
    # Add cache headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    return response


@app.route('/ready', methods=['GET'])
def readiness():
    """
    Readiness probe for Kubernetes/load balancers.
    
    Checks if application is ready to receive traffic.
    Quick check - only verifies critical dependencies.
    """
    quick_checks = [
        ('database', check_database),
        ('redis', check_redis) if redis_client else None
    ]
    
    status = 'ready'
    checks = {}
    
    for check in quick_checks:
        if check is None:
            continue
        
        name, check_func = check
        try:
            result = check_func()
            checks[name] = {
                'status': 'healthy',
                'output': result
            }
        except Exception as e:
            checks[name] = {
                'status': 'unhealthy',
                'output': str(e)
            }
            status = 'not_ready'
    
    response_data = {
        'status': status,
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks
    }
    
    status_code = 200 if status == 'ready' else 503
    response = jsonify(response_data)
    response.status_code = status_code
    
    # Add retry-after header if not ready
    if status != 'ready':
        response.headers['Retry-After'] = '5'
    
    return response


@app.route('/live', methods=['GET'])
def liveness():
    """
    Liveness probe for Kubernetes.
    
    Simple check - is the application process running?
    Should be very fast and not check dependencies.
    """
    response_data = {
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat(),
        'process_id': os.getpid(),
        'uptime_seconds': (datetime.utcnow() - app_start_time).total_seconds()
    }
    
    return jsonify(response_data), 200


@app.route('/startup', methods=['GET'])
def startup():
    """
    Startup probe for Kubernetes.
    
    Checks if application has started successfully.
    Can be more comprehensive than liveness but runs only at startup.
    """
    # Log startup event
    try:
        log = DeploymentLog(
            deployment_id=app.config['DEPLOYMENT_ID'],
            pod_name=app.config['POD_NAME'],
            version=app.config['VERSION'],
            environment=app.config['ENVIRONMENT'],
            event_type='startup',
            event_data={'timestamp': datetime.utcnow().isoformat()}
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Failed to log startup: {e}")
    
    # Run comprehensive checks
    health_data = health_checker.check_all()
    
    response_data = {
        'status': health_data['status'],
        'timestamp': datetime.utcnow().isoformat(),
        'deployment_id': app.config['DEPLOYMENT_ID'],
        'pod_name': app.config['POD_NAME'],
        'checks_passed': len([c for c in health_data['checks'].values() if c['status'] == 'healthy']),
        'checks_failed': len([c for c in health_data['checks'].values() if c['status'] == 'unhealthy'])
    }
    
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return jsonify(response_data), status_code


# Metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint."""
    # Update dynamic metrics
    update_dynamic_metrics()
    
    return generate_latest(prometheus_client.REGISTRY)


def update_dynamic_metrics():
    """Update dynamic metrics like memory usage."""
    try:
        # Update memory usage
        memory = psutil.Process().memory_info()
        MEMORY_USAGE.set(memory.rss)
        
        # Update CPU usage
        cpu_percent = psutil.Process().cpu_percent(interval=None)
        CPU_USAGE.set(cpu_percent)
        
        # Update database connection pool metrics
        if hasattr(db.engine.pool, '_conn'):
            pool = db.engine.pool
            DATABASE_CONNECTIONS.labels(state='checked_out').set(len(pool._conn))
            DATABASE_CONNECTIONS.labels(state='idle').set(pool.size() - len(pool._conn))
            DATABASE_CONNECTIONS.labels(state='total').set(pool.size())
        
        # Update Redis connections
        if redis_client:
            try:
                info = redis_client.info()
                REDIS_CONNECTIONS.set(info.get('connected_clients', 0))
            except:
                pass
                
    except Exception as e:
        app.logger.error(f"Failed to update metrics: {e}")


# ============================================================================
# 6. GRACEFUL SHUTDOWN HANDLING
# ============================================================================

"""
GRACEFUL SHUTDOWN PRINCIPLES:
1. Stop accepting new requests
2. Allow existing requests to complete
3. Close connections gracefully
4. Perform cleanup tasks
5. Exit process cleanly
"""

class GracefulShutdown:
    """Handle graceful shutdown of the application."""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.shutdown_requested = False
        self.active_requests = 0
        self.lock = threading.Lock()
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self.handle_shutdown_signal)
        signal.signal(signal.SIGINT, self.handle_shutdown_signal)
        
        app.logger.info("Graceful shutdown handler initialized")
    
    def handle_shutdown_signal(self, signum, frame):
        """Handle shutdown signals."""
        app.logger.warning(f"Received shutdown signal {signum}")
        self.initiate_shutdown()
    
    def initiate_shutdown(self):
        """Initiate graceful shutdown."""
        with self.lock:
            if self.shutdown_requested:
                return
            
            self.shutdown_requested = True
            app.logger.info(f"Initiating graceful shutdown (timeout: {self.timeout}s)")
            
            # Log shutdown event
            self.log_shutdown_event()
            
            # Stop accepting new requests
            app.logger.info("Stopping acceptance of new requests")
            
            # Wait for active requests to complete
            self.wait_for_active_requests()
            
            # Perform cleanup
            self.cleanup()
            
            # Exit
            app.logger.info("Shutdown complete, exiting")
            sys.exit(0)
    
    def wait_for_active_requests(self):
        """Wait for active requests to complete."""
        start_time = time.time()
        
        while self.active_requests > 0 and (time.time() - start_time) < self.timeout:
            app.logger.info(f"Waiting for {self.active_requests} active requests to complete...")
            time.sleep(1)
        
        if self.active_requests > 0:
            app.logger.warning(f"Forcefully terminating {self.active_requests} active requests")
        else:
            app.logger.info("All active requests completed")
    
    def cleanup(self):
        """Perform cleanup tasks."""
        try:
            app.logger.info("Closing database connections...")
            db.session.remove()
            db.engine.dispose()
            
            if redis_client:
                app.logger.info("Closing Redis connections...")
                redis_client.close()
            
            app.logger.info("Cleanup complete")
        except Exception as e:
            app.logger.error(f"Error during cleanup: {e}")
    
    def log_shutdown_event(self):
        """Log shutdown event to database."""
        try:
            log = DeploymentLog(
                deployment_id=app.config['DEPLOYMENT_ID'],
                pod_name=app.config['POD_NAME'],
                version=app.config['VERSION'],
                environment=app.config['ENVIRONMENT'],
                event_type='shutdown',
                event_data={
                    'timestamp': datetime.utcnow().isoformat(),
                    'signal': 'SIGTERM',
                    'active_requests': self.active_requests
                }
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            app.logger.error(f"Failed to log shutdown event: {e}")
    
    def request_start(self):
        """Track request start."""
        with self.lock:
            if self.shutdown_requested:
                raise RuntimeError("Server is shutting down")
            self.active_requests += 1
    
    def request_end(self):
        """Track request end."""
        with self.lock:
            self.active_requests -= 1


# Initialize graceful shutdown handler
shutdown_handler = GracefulShutdown(timeout=app.config['GRACEFUL_SHUTDOWN_TIMEOUT'])


# Middleware to track requests
@app.before_request
def track_request_start():
    """Track request start for graceful shutdown."""
    shutdown_handler.request_start()


@app.after_request
def track_request_end(response):
    """Track request end for graceful shutdown."""
    shutdown_handler.request_end()
    return response


# ============================================================================
# 7. APPLICATION ENDPOINTS WITH PRODUCTION FEATURES
# ============================================================================

@app.route('/')
def index():
    """Main endpoint with deployment information."""
    info = {
        'application': app.config['APP_NAME'],
        'version': app.config['VERSION'],
        'environment': app.config['ENVIRONMENT'],
        'deployment_id': app.config['DEPLOYMENT_ID'],
        'pod_name': app.config['POD_NAME'],
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'health': '/health',
            'ready': '/ready',
            'live': '/live',
            'metrics': '/metrics',
            'users': '/api/users',
            'orders': '/api/orders'
        }
    }
    return jsonify(info)


@app.route('/api/users', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Cache for 60 seconds
def get_users():
    """Get users with caching and pagination."""
    try:
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate parameters
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({
                'error': 'Invalid pagination parameters',
                'details': {
                    'page': 'Must be >= 1',
                    'per_page': 'Must be between 1 and 100'
                }
            }), 400
        
        # Query database
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
                'cache_hit': False,  # Would be True if served from cache
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        app.logger.error(f"Error fetching users: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
@cache.memoize(timeout=300)  # Cache for 5 minutes per user_id
def get_user(user_id):
    """Get specific user with caching."""
    try:
        user = User.query.get_or_404(user_id)
        
        response_data = {
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        }
        
        return jsonify(response_data)
        
    except HTTPException:
        raise  # Re-raise 404
    except Exception as e:
        app.logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order with rate limiting and validation."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        # Validate required fields
        required_fields = ['user_id', 'amount']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'details': {field: 'This field is required' for field in missing_fields}
            }), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Invalid amount',
                'details': {'amount': 'Must be a positive number'}
            }), 400
        
        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create order
        order = Order(
            user_id=user.id,
            amount=amount,
            currency=data.get('currency', 'USD'),
            status='pending'
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Invalidate cache for user's orders
        if redis_client:
            cache_key = f"user_orders_{user.id}"
            redis_client.delete(cache_key)
        
        response_data = {
            'data': {
                'id': order.id,
                'user_id': order.user_id,
                'amount': order.amount,
                'currency': order.currency,
                'status': order.status,
                'created_at': order.created_at.isoformat()
            }
        }
        
        response = jsonify(response_data)
        response.status_code = 201
        response.headers['Location'] = f'/api/orders/{order.id}'
        
        return response
        
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Database error creating order: {e}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        app.logger.error(f"Error creating order: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/deployment/info', methods=['GET'])
def deployment_info():
    """Get deployment information."""
    try:
        # Get recent deployment logs
        logs = DeploymentLog.query.filter(
            DeploymentLog.deployment_id == app.config['DEPLOYMENT_ID']
        ).order_by(DeploymentLog.created_at.desc()).limit(10).all()
        
        log_data = []
        for log in logs:
            log_data.append({
                'event_type': log.event_type,
                'created_at': log.created_at.isoformat(),
                'event_data': log.event_data
            })
        
        response_data = {
            'deployment': {
                'id': app.config['DEPLOYMENT_ID'],
                'pod_name': app.config['POD_NAME'],
                'environment': app.config['ENVIRONMENT'],
                'version': app.config['VERSION'],
                'namespace': app.config['NAMESPACE'],
                'start_time': app_start_time.isoformat(),
                'uptime_seconds': (datetime.utcnow() - app_start_time).total_seconds()
            },
            'system': {
                'hostname': socket.gethostname(),
                'python_version': sys.version,
                'cpu_count': multiprocessing.cpu_count(),
                'memory_usage_mb': round(psutil.Process().memory_info().rss / (1024**2), 2)
            },
            'recent_logs': log_data
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        app.logger.error(f"Error getting deployment info: {e}")
        return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# 8. SECURITY MIDDLEWARE
# ============================================================================

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    for header, value in app.config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    
    # Add CORS headers if needed
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    # Add deployment info headers
    response.headers['X-Deployment-ID'] = app.config['DEPLOYMENT_ID']
    response.headers['X-Pod-Name'] = app.config['POD_NAME']
    response.headers['X-Environment'] = app.config['ENVIRONMENT']
    response.headers['X-Version'] = app.config['VERSION']
    
    return response


# ============================================================================
# 9. DEPLOYMENT UTILITIES
# ============================================================================

class DeploymentManager:
    """Manage deployment-related operations."""
    
    @staticmethod
    def get_dockerfile():
        """Generate Dockerfile for the application."""
        dockerfile = '''# Production Dockerfile for Flask Application
        
# Stage 1: Build stage
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN groupadd -r flaskgroup && useradd -r -g flaskgroup flaskuser
USER flaskuser

# Create application directory
WORKDIR /app

# Copy application code
COPY --chown=flaskuser:flaskgroup . .

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "gthread", \
     "--threads", "2", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--capture-output", \
     "--log-level", "info", \
     "app:app"]
'''
        return dockerfile
    
    @staticmethod
    def get_docker_compose():
        """Generate docker-compose.yml for local development."""
        compose = '''# Docker Compose for local development
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/flask_dev
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./:/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=flask_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
'''
        return compose
    
    @staticmethod
    def get_nginx_config():
        """Generate NGINX configuration."""
        nginx_config = '''# NGINX configuration for Flask application
events {
    worker_connections 1024;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Upstream configuration for Flask application
    upstream flask_app {
        # Load balancing method (least_conn, ip_hash, etc.)
        least_conn;
        
        # Flask application servers
        server web:8000 max_fails=3 fail_timeout=30s;
        # Add more servers for horizontal scaling
        # server web2:8000 max_fails=3 fail_timeout=30s;
        # server web3:8000 max_fails=3 fail_timeout=30s;
    }

    # Main server block
    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        
        # Static files (if any)
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Media files (if any)
        location /media/ {
            alias /app/media/;
            expires 30d;
            add_header Cache-Control "public";
        }

        # API endpoints
        location /api/ {
            # Rate limiting
            limit_req zone=api burst=20 nodelay;
            
            # Proxy settings
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
            proxy_set_header X-Forwarded-Port $server_port;
            
            # Timeouts
            proxy_connect_timeout 5s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Buffering
            proxy_buffering off;
            proxy_request_buffering off;
        }

        # Health checks (no rate limiting)
        location ~ ^/(health|ready|live|startup)$ {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # Fast timeouts for health checks
            proxy_connect_timeout 2s;
            proxy_send_timeout 5s;
            proxy_read_timeout 5s;
        }

        # Metrics endpoint
        location /metrics {
            # Basic authentication for metrics
            auth_basic "Prometheus Metrics";
            auth_basic_user_file /etc/nginx/.htpasswd;
            
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
        }

        # Default location
        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
'''
        return nginx_config
    
    @staticmethod
    def get_gunicorn_config():
        """Generate Gunicorn configuration file."""
        gunicorn_config = '''# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
worker_connections = 1000
timeout = 30
keepalive = 2

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "flask_app"

# Server hooks
def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")

def pre_request(worker, req):
    worker.log.debug(f"Request start: {req.path}")

def post_request(worker, req, environ, resp):
    worker.log.debug(f"Request end: {req.path}")
'''
        return gunicorn_config
    
    @staticmethod
    def get_kubernetes_manifest():
        """Generate Kubernetes deployment manifest."""
        manifest = '''# Kubernetes Deployment Manifest for Flask Application
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  namespace: default
  labels:
    app: flask-app
    version: v1.0.0
spec:
  replicas: 3  # Horizontal scaling - 3 instances
  strategy:
    type: RollingUpdate  # Zero-downtime deployments
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Ensure at least replicas-1 available during update
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
        version: v1.0.0
    spec:
      containers:
      - name: flask-app
        image: your-registry/flask-app:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: flask-secrets
              key: database-url
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: DEPLOYMENT_ID
          value: "v1.0.0"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 1
        startupProbe:
          httpGet:
            path: /startup
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30  # 5 minutes max startup time
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
      volumes:
      - name: config-volume
        configMap:
          name: flask-config
      terminationGracePeriodSeconds: 30  # Time for graceful shutdown
---
# Service for load balancing
apiVersion: v1
kind: Service
metadata:
  name: flask-service
  namespace: default
spec:
  selector:
    app: flask-app
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP  # Use LoadBalancer for external access
---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---
# ConfigMap for environment-specific configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-config
  namespace: default
data:
  LOG_LEVEL: "INFO"
  CACHE_TIMEOUT: "300"
  RATE_LIMIT_ENABLED: "true"
---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: flask-secrets
  namespace: default
type: Opaque
data:
  database-url: <base64-encoded-database-url>
  secret-key: <base64-encoded-secret-key>
'''
        return manifest
    
    @staticmethod
    def get_blue_green_manifest():
        """Generate Blue/Green deployment manifest."""
        manifest = '''# Blue/Green Deployment Strategy
# 
# Step 1: Deploy Green (new version) alongside Blue (current version)
# Step 2: Test Green deployment
# Step 3: Switch traffic from Blue to Green
# Step 4: Decommission Blue

# Green Deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-green
  namespace: default
  labels:
    app: flask-app
    version: v2.0.0
    deployment: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
      deployment: green
  template:
    metadata:
      labels:
        app: flask-app
        version: v2.0.0
        deployment: green
    spec:
      # ... same as main deployment ...
---
# Service pointing to Green
apiVersion: v1
kind: Service
metadata:
  name: flask-app-green
  namespace: default
spec:
  selector:
    app: flask-app
    deployment: green
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
# Ingress for routing (using nginx-ingress)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-app-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "0"  # Start with 0% traffic to green
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-app  # Blue service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: flask-app-green  # Green service
            port:
              number: 80
---
# Script to switch traffic
# 1. Gradually increase canary weight to 100%
# 2. Update main service to point to green
# 3. Delete blue deployment
'''
        return manifest


@app.route('/api/deployment/configs', methods=['GET'])
def get_deployment_configs():
    """Get deployment configuration files."""
    configs = {
        'dockerfile': DeploymentManager.get_dockerfile(),
        'docker_compose': DeploymentManager.get_docker_compose(),
        'nginx_config': DeploymentManager.get_nginx_config(),
        'gunicorn_config': DeploymentManager.get_gunicorn_config(),
        'kubernetes_manifest': DeploymentManager.get_kubernetes_manifest(),
        'blue_green_manifest': DeploymentManager.get_blue_green_manifest()
    }
    
    return jsonify(configs)


# ============================================================================
# 10. DEPLOYMENT ENDPOINTS
# ============================================================================

@app.route('/api/deployment/scale', methods=['POST'])
def scale_deployment():
    """
    Demo endpoint for scaling operations.
    
    In production, this would integrate with:
    - Kubernetes API
    - Docker Swarm
    - AWS ECS/EC2 Auto Scaling
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    action = data.get('action')
    
    if action == 'get_status':
        # Get current deployment status
        status = {
            'replicas': 3,  # This would come from Kubernetes/Docker
            'active_requests': shutdown_handler.active_requests,
            'memory_usage_mb': round(psutil.Process().memory_info().rss / (1024**2), 2),
            'cpu_percent': psutil.Process().cpu_percent(interval=1),
            'database_connections': 'N/A',  # Would get from database
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify({'status': status})
    
    elif action == 'scale_up':
        # Scale up deployment
        replicas = data.get('replicas', 1)
        
        # In production: Call Kubernetes API to scale deployment
        # kubernetes_api.scale_deployment('flask-app', replicas)
        
        return jsonify({
            'message': f'Scaling up to {replicas} replicas (simulated)',
            'action': 'scale_up',
            'replicas': replicas,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    elif action == 'scale_down':
        # Scale down deployment
        replicas = data.get('replicas', 1)
        
        # In production: Call Kubernetes API to scale deployment
        # kubernetes_api.scale_deployment('flask-app', replicas)
        
        return jsonify({
            'message': f'Scaling down to {replicas} replicas (simulated)',
            'action': 'scale_down',
            'replicas': replicas,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    elif action == 'drain':
        # Drain traffic from this instance (for zero-downtime deployments)
        # This would mark the instance as not ready for traffic
        
        return jsonify({
            'message': 'Instance marked for draining (simulated)',
            'action': 'drain',
            'pod_name': app.config['POD_NAME'],
            'timestamp': datetime.utcnow().isoformat()
        })
    
    else:
        return jsonify({'error': 'Invalid action'}), 400


# ============================================================================
# 11. DEMONSTRATION ROUTE
# ============================================================================

@app.route('/deployment-demo')
def deployment_demo():
    """Interactive deployment demonstration page."""
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Deployment & Production Readiness Demo</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1400px;
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
            .config-btn {
                background: #28a745;
            }
            .config-btn:hover {
                background: #218838;
            }
            .health-btn {
                background: #ffc107;
                color: black;
            }
            .health-btn:hover {
                background: #e0a800;
            }
            .scale-btn {
                background: #17a2b8;
            }
            .scale-btn:hover {
                background: #138496;
            }
            .deploy-btn {
                background: #6f42c1;
            }
            .deploy-btn:hover {
                background: #5a3796;
            }
            pre {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                overflow-x: auto;
                max-height: 400px;
                overflow-y: auto;
            }
            code {
                background: #e9ecef;
                padding: 0.2rem 0.4rem;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            #results {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                min-height: 100px;
                max-height: 600px;
                overflow-y: auto;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1rem;
                margin: 1rem 0;
            }
            .info-card {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 1rem;
            }
            .badge {
                display: inline-block;
                padding: 0.25rem 0.5rem;
                border-radius: 3px;
                font-size: 0.875rem;
                font-weight: bold;
            }
            .badge-success { background: #28a745; color: white; }
            .badge-warning { background: #ffc107; color: black; }
            .badge-danger { background: #dc3545; color: white; }
            .badge-info { background: #17a2b8; color: white; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Flask Deployment & Production Readiness Demo</h1>
            <p>Comprehensive demonstration of production deployment patterns and best practices</p>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>📊 Application Info</h3>
                <p><strong>Name:</strong> <span id="app-name">Loading...</span></p>
                <p><strong>Version:</strong> <span id="app-version">Loading...</span></p>
                <p><strong>Environment:</strong> <span id="app-env" class="badge badge-info">Loading...</span></p>
                <p><strong>Deployment ID:</strong> <code id="deployment-id">Loading...</code></p>
                <p><strong>Pod Name:</strong> <code id="pod-name">Loading...</code></p>
            </div>
            
            <div class="info-card">
                <h3>⚙️ System Status</h3>
                <p><strong>Memory Usage:</strong> <span id="memory-usage">Loading...</span></p>
                <p><strong>CPU Usage:</strong> <span id="cpu-usage">Loading...</span></p>
                <p><strong>Active Requests:</strong> <span id="active-requests">Loading...</span></p>
                <p><strong>Uptime:</strong> <span id="uptime">Loading...</span></p>
            </div>
            
            <div class="info-card">
                <h3>🔗 Quick Links</h3>
                <p><a href="/health" target="_blank">Health Check</a></p>
                <p><a href="/ready" target="_blank">Readiness Probe</a></p>
                <p><a href="/live" target="_blank">Liveness Probe</a></p>
                <p><a href="/metrics" target="_blank">Prometheus Metrics</a></p>
                <p><a href="/api/deployment/info" target="_blank">Deployment Info</a></p>
            </div>
        </div>
        
        <div class="section">
            <h2>🏥 Health & Monitoring</h2>
            <p>Production applications need comprehensive health checks and monitoring.</p>
            <div class="demo-buttons">
                <button class="demo-btn health-btn" onclick="testHealth()">Comprehensive Health Check</button>
                <button class="demo-btn health-btn" onclick="testReadiness()">Readiness Probe</button>
                <button class="demo-btn health-btn" onclick="testLiveness()">Liveness Probe</button>
                <button class="demo-btn health-btn" onclick="testStartup()">Startup Probe</button>
                <button class="demo-btn health-btn" onclick="testMetrics()">Prometheus Metrics</button>
            </div>
        </div>
        
        <div class="section">
            <h2>🐳 Containerization & Orchestration</h2>
            <p>Get configuration files for different deployment scenarios:</p>
            <div class="demo-buttons">
                <button class="demo-btn config-btn" onclick="getConfig('dockerfile')">Dockerfile</button>
                <button class="demo-btn config-btn" onclick="getConfig('docker_compose')">Docker Compose</button>
                <button class="demo-btn config-btn" onclick="getConfig('nginx_config')">NGINX Config</button>
                <button class="demo-btn config-btn" onclick="getConfig('gunicorn_config')">Gunicorn Config</button>
                <button class="demo-btn config-btn" onclick="getConfig('kubernetes_manifest')">K8s Manifest</button>
                <button class="demo-btn config-btn" onclick="getConfig('blue_green_manifest')">Blue/Green Deployment</button>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Horizontal Scaling</h2>
            <p>Simulate scaling operations (in production, these would call real APIs):</p>
            <div class="demo-buttons">
                <button class="demo-btn scale-btn" onclick="scaleAction('get_status')">Get Status</button>
                <button class="demo-btn scale-btn" onclick="scaleAction('scale_up')">Scale Up (Add replicas)</button>
                <button class="demo-btn scale-btn" onclick="scaleAction('scale_down')">Scale Down</button>
                <button class="demo-btn scale-btn" onclick="scaleAction('drain')">Drain Instance</button>
            </div>
        </div>
        
        <div class="section">
            <h2>⚡ Production Deployment Patterns</h2>
            <div class="info-grid">
                <div class="info-card">
                    <h4>🚀 Zero-Downtime Deployments</h4>
                    <ul>
                        <li>Rolling updates in Kubernetes</li>
                        <li>Blue/Green deployments</li>
                        <li>Canary releases</li>
                        <li>Graceful shutdown handling</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h4>🛡️ Security & Hardening</h4>
                    <ul>
                        <li>Running as non-root user</li>
                        <li>Security headers</li>
                        <li>Rate limiting</li>
                        <li>Secret management</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h4>📊 Observability</h4>
                    <ul>
                        <li>Structured logging</li>
                        <li>Prometheus metrics</li>
                        <li>Health checks</li>
                        <li>Distributed tracing</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h4>⚖️ Load Balancing</h4>
                    <ul>
                        <li>NGINX reverse proxy</li>
                        <li>Gunicorn workers</li>
                        <li>Database connection pooling</li>
                        <li>Redis caching</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Deployment Architecture</h2>
            <pre>
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (NGINX)                │
└───────────────────────────┬─────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐    ┌──────▼──────┐    ┌───────▼──────┐
│   Gunicorn   │    │   Gunicorn   │    │   Gunicorn   │
│   Worker 1   │    │   Worker 2   │    │   Worker 3   │
└───────┬──────┘    └──────┬──────┘    └───────┬──────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
            ┌───────────────▼────────────────┐
            │        Flask Application       │
            └───────────────┬────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼──────┐    ┌──────▼──────┐    ┌───────▼──────┐
│   Database    │    │     Redis    │    │ External APIs │
│  (PostgreSQL) │    │   (Cache)    │    │  (Payment)   │
└───────────────┘    └──────────────┘    └──────────────┘
            </pre>
        </div>
        
        <div class="section">
            <h2>📝 Example Deployment Commands</h2>
            <pre><code># Build Docker image
docker build -t flask-app:latest .

# Run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale web=3

# Run database migrations
docker-compose exec web flask db upgrade

# Kubernetes deployment
kubectl apply -f kubernetes-manifest.yaml

# Blue/Green deployment strategy
# 1. Deploy new version (green)
kubectl apply -f green-deployment.yaml
# 2. Test green deployment
kubectl get pods -l deployment=green
# 3. Switch traffic (update ingress)
kubectl patch ingress flask-app -p '{"spec":{"rules":[{"host":"app.example.com","http":{"paths":[{"path":"/","backend":{"serviceName":"flask-app-green"}}]}}]}}'
# 4. Clean up old version (blue)
kubectl delete deployment flask-app-blue</code></pre>
        </div>
        
        <div class="section">
            <h2>🚀 Results & Configuration Files</h2>
            <div id="results">
                <p>Results will appear here...</p>
            </div>
        </div>
        
        <script>
            const results = document.getElementById('results');
            
            // Load initial application info
            async function loadAppInfo() {
                try {
                    const response = await fetch('/');
                    const data = await response.json();
                    
                    document.getElementById('app-name').textContent = data.application;
                    document.getElementById('app-version').textContent = data.version;
                    document.getElementById('app-env').textContent = data.environment;
                    document.getElementById('deployment-id').textContent = data.deployment_id;
                    document.getElementById('pod-name').textContent = data.pod_name;
                    
                    // Update system status periodically
                    updateSystemStatus();
                    setInterval(updateSystemStatus, 5000);
                    
                } catch (error) {
                    console.error('Error loading app info:', error);
                }
            }
            
            async function updateSystemStatus() {
                try {
                    // Get metrics data
                    const metricsResponse = await fetch('/metrics');
                    const metricsText = await metricsResponse.text();
                    
                    // Parse metrics (simplified)
                    const lines = metricsText.split('\\n');
                    let memory = 'N/A';
                    let cpu = 'N/A';
                    let requests = 'N/A';
                    
                    for (const line of lines) {
                        if (line.startsWith('memory_usage_bytes')) {
                            const value = line.split(' ')[1];
                            memory = Math.round(value / (1024 * 1024)) + ' MB';
                        }
                        if (line.startsWith('cpu_usage_percent')) {
                            cpu = line.split(' ')[1] + ' %';
                        }
                        if (line.startsWith('http_active_requests')) {
                            requests = line.split(' ')[1];
                        }
                    }
                    
                    document.getElementById('memory-usage').textContent = memory;
                    document.getElementById('cpu-usage').textContent = cpu;
                    document.getElementById('active-requests').textContent = requests;
                    
                    // Calculate uptime
                    const uptimeResponse = await fetch('/api/deployment/info');
                    const uptimeData = await uptimeResponse.json();
                    const uptimeSeconds = uptimeData.deployment.uptime_seconds;
                    const uptimeHours = Math.floor(uptimeSeconds / 3600);
                    const uptimeMinutes = Math.floor((uptimeSeconds % 3600) / 60);
                    document.getElementById('uptime').textContent = `${uptimeHours}h ${uptimeMinutes}m`;
                    
                } catch (error) {
                    console.error('Error updating system status:', error);
                }
            }
            
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
                    const statusClass = response.ok ? 'badge-success' : 'badge-danger';
                    results.innerHTML += `<p><span class="badge ${statusClass}">Status: ${response.status}</span></p>`;
                    
                } catch (error) {
                    results.innerHTML = `<p class="badge badge-danger">Error: ${error.message}</p>`;
                }
            }
            
            function testHealth() {
                makeRequest('/health');
            }
            
            function testReadiness() {
                makeRequest('/ready');
            }
            
            function testLiveness() {
                makeRequest('/live');
            }
            
            function testStartup() {
                makeRequest('/startup');
            }
            
            function testMetrics() {
                makeRequest('/metrics');
            }
            
            function getConfig(configType) {
                makeRequest('/api/deployment/configs')
                    .then(() => {
                        // Parse the response to show specific config
                        fetch('/api/deployment/configs')
                            .then(r => r.json())
                            .then(data => {
                                if (data[configType]) {
                                    results.innerHTML = `<h3>${configType}</h3><pre>${data[configType]}</pre>`;
                                }
                            });
                    });
            }
            
            function scaleAction(action) {
                let body = {};
                
                if (action === 'scale_up') {
                    const replicas = prompt('Enter number of replicas:', '4');
                    if (replicas) {
                        body = { action: 'scale_up', replicas: parseInt(replicas) };
                    } else {
                        return;
                    }
                } else if (action === 'scale_down') {
                    const replicas = prompt('Enter number of replicas:', '2');
                    if (replicas) {
                        body = { action: 'scale_down', replicas: parseInt(replicas) };
                    } else {
                        return;
                    }
                } else {
                    body = { action: action };
                }
                
                makeRequest('/api/deployment/scale', {
                    method: 'POST',
                    body: JSON.stringify(body)
                });
            }
            
            // Initialize
            loadAppInfo();
            testHealth(); // Initial test
        </script>
    </body>
    </html>
    '''
    return html


# ============================================================================
# 12. GUNICORN ENTRY POINT
# ============================================================================

"""
RUNNING FLASK WITH GUNICORN:

Why Gunicorn?
1. Production-grade WSGI server
2. Multiple worker processes for concurrency
3. Graceful worker management
4. Better performance than Flask development server

Basic command:
gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 2 --timeout 30 app:app

For high performance:
gunicorn --bind 0.0.0.0:8000 \
    --workers $(($(nproc) * 2 + 1)) \
    --worker-class gthread \
    --threads 2 \
    --timeout 30 \
    --keepalive 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app
"""

# This allows running the app with: python app.py
# But in production, use: gunicorn app:app
if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        db.create_all()
        
        # Add sample data
        if not User.query.first():
            users = [
                User(username='admin', email='admin@example.com'),
                User(username='user1', email='user1@example.com'),
                User(username='user2', email='user2@example.com')
            ]
            
            orders = [
                Order(user_id=1, amount=99.99, status='completed'),
                Order(user_id=2, amount=49.99, status='pending')
            ]
            
            db.session.add_all(users)
            db.session.add_all(orders)
            db.session.commit()
            
            app.logger.info("Database initialized with sample data")
    
    # Log startup event
    try:
        log = DeploymentLog(
            deployment_id=app.config['DEPLOYMENT_ID'],
            pod_name=app.config['POD_NAME'],
            version=app.config['VERSION'],
            environment=app.config['ENVIRONMENT'],
            event_type='startup',
            event_data={
                'timestamp': datetime.utcnow().isoformat(),
                'hostname': socket.gethostname(),
                'python_version': sys.version
            }
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Failed to log startup: {e}")
    
    # Print deployment information
    print("\n" + "="*80)
    print("🚀 FLASK DEPLOYMENT & PRODUCTION READINESS DEMO")
    print("="*80)
    
    print(f"\n📊 Application Information:")
    print(f"   Name: {app.config['APP_NAME']}")
    print(f"   Version: {app.config['VERSION']}")
    print(f"   Environment: {app.config['ENVIRONMENT']}")
    print(f"   Deployment ID: {app.config['DEPLOYMENT_ID']}")
    print(f"   Pod Name: {app.config['POD_NAME']}")
    
    print(f"\n🌐 Available Endpoints:")
    print(f"   • http://localhost:5000/deployment-demo - Interactive demo")
    print(f"   • GET  /health - Comprehensive health check")
    print(f"   • GET  /ready - Readiness probe (for load balancers)")
    print(f"   • GET  /live - Liveness probe (for Kubernetes)")
    print(f"   • GET  /startup - Startup probe")
    print(f"   • GET  /metrics - Prometheus metrics")
    print(f"   • GET  /api/deployment/configs - Deployment configurations")
    print(f"   • GET  /api/users - Users API (with caching)")
    
    print(f"\n🔧 Production Deployment Options:")
    print(f"   1. Development server: python app.py")
    print(f"   2. Gunicorn: gunicorn --bind 0.0.0.0:8000 --workers 4 app:app")
    print(f"   3. Docker: docker build -t flask-app . && docker run -p 8000:8000 flask-app")
    print(f"   4. Docker Compose: docker-compose up -d")
    print(f"   5. Kubernetes: kubectl apply -f kubernetes-manifest.yaml")
    
    print(f"\n📈 Monitoring:")
    print(f"   • Health checks: http://localhost:5000/health")
    print(f"   • Metrics: http://localhost:5000/metrics")
    print(f"   • Deployment info: http://localhost:5000/api/deployment/info")
    
    print(f"\n🚀 Getting Started:")
    print(f"   1. Visit http://localhost:5000/deployment-demo for interactive demo")
    print(f"   2. Check health status at /health")
    print(f"   3. View deployment configurations at /api/deployment/configs")
    print(f"   4. Test scaling operations")
    
    print(f"\n⚠️  Production Notes:")
    print(f"   • Never run Flask development server in production")
    print(f"   • Always use Gunicorn or another production WSGI server")
    print(f"   • Use environment variables for configuration")
    print(f"   • Implement proper health checks")
    print(f"   • Use reverse proxy (NGINX) for SSL termination and caching")
    print(f"   • Implement rate limiting")
    print(f"   • Use containerization for consistency")
    print("="*80 + "\n")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG'],
        threaded=True
    )