"""
FLASK CONFIGURATION & ENVIRONMENTS MASTER GUIDE

Comprehensive implementation covering all aspects of Flask configuration
with detailed explanations and practical examples.

Author: Flask Configuration Expert
Date: 2024
"""

# ============================================================================
# SECTION 1: IMPORTS AND SETUP
# ============================================================================

import os
import sys
import json
import logging
import secrets
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import timedelta
from decimal import Decimal

# Third-party imports for enhanced configuration
import yaml
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, ValidationError, Field, validator
from cryptography.fernet import Fernet

# Flask imports
from flask import Flask, current_app, jsonify, request
from flask.logging import default_handler

# ============================================================================
# SECTION 2: UNDERSTANDING FLASK CONFIGURATION PRECEDENCE
# ============================================================================
"""
FLASK CONFIGURATION PRECEDENCE (Highest to Lowest):

1. Flask instance configuration (app.config['KEY'] = value)
   - Set directly on the app instance
   - Highest priority, runtime override

2. Environment variables with FLASK_ prefix
   - FLASK_DEBUG=1, FLASK_SECRET_KEY=xxx
   - Auto-loaded by Flask's from_prefixed_env()

3. Config file specified in FLASK_CONFIG_FILE env var
   - FLASK_CONFIG_FILE=/path/to/config.py
   - Loaded via from_pyfile()

4. Instance folder config (instance/config.py)
   - app.config.from_pyfile('config.py', silent=True)

5. Class-based configuration
   - app.config.from_object('config.ProductionConfig')
   - Loads all uppercase attributes

6. Default Flask configuration values
   - DEBUG, TESTING, PROPAGATE_EXCEPTIONS, etc.

BEST PRACTICE ORDER OF LOADING:
1. Load defaults from config class
2. Load from instance folder (for dev overrides)
3. Load from environment file (.env)
4. Load from environment variables
5. Runtime overrides if needed

This ensures proper inheritance and override capability.
"""

# ============================================================================
# SECTION 3: ENVIRONMENT DETECTION & VALIDATION
# ============================================================================

class Environment(str, Enum):
    """Supported environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"
    DOCKER = "docker"
    CI = "ci"

def detect_environment() -> Environment:
    """
    Intelligently detect the current environment.
    
    Checks multiple sources in order of precedence:
    1. FLASK_ENV environment variable (Flask standard)
    2. APP_ENV environment variable (application standard)
    3. ENVIRONMENT environment variable (cloud/container standard)
    4. Detect based on hostname, debug mode, or other heuristics
    """
    # Order of precedence for environment detection
    env_var_sources = ['FLASK_ENV', 'APP_ENV', 'ENVIRONMENT', 'NODE_ENV']
    
    for env_var in env_var_sources:
        env_value = os.environ.get(env_var)
        if env_value:
            try:
                return Environment(env_value.lower())
            except ValueError:
                # Try to map common aliases
                mapping = {
                    'dev': Environment.DEVELOPMENT,
                    'prod': Environment.PRODUCTION,
                    'test': Environment.TESTING,
                    'stage': Environment.STAGING,
                    'local': Environment.LOCAL,
                    'docker': Environment.DOCKER,
                    'ci': Environment.CI,
                }
                return mapping.get(env_value.lower(), Environment.DEVELOPMENT)
    
    # Heuristic detection
    if 'pytest' in sys.modules or 'unittest' in sys.argv:
        return Environment.TESTING
    
    if os.environ.get('PYTHON_ENV') == 'testing':
        return Environment.TESTING
    
    if os.environ.get('DOCKER_CONTAINER'):
        return Environment.DOCKER
    
    if 'localhost' in os.environ.get('HOSTNAME', '') or '127.0.0.1' in os.environ.get('HOST', ''):
        return Environment.LOCAL
    
    # Default to development if running locally with debug likely enabled
    if os.environ.get('USER') and not os.environ.get('CI'):
        return Environment.DEVELOPMENT
    
    # Conservative default for safety
    return Environment.PRODUCTION

# ============================================================================
# SECTION 4: SECRETS MANAGEMENT & ENCRYPTION
# ============================================================================

class SecretManager:
    """
    Advanced secrets management with encryption support.
    
    Implements multiple strategies for secret handling:
    1. Environment variables (primary)
    2. Encrypted .env files
    3. Cloud secret managers (AWS Secrets Manager, HashiCorp Vault)
    4. Docker secrets
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize secret manager.
        
        Args:
            encryption_key: Optional encryption key for decrypting secrets.
                          If not provided, looks for ENCRYPTION_KEY env var.
        """
        self.encryption_key = encryption_key or os.environ.get('ENCRYPTION_KEY')
        self.fernet = None
        
        if self.encryption_key:
            try:
                self.fernet = Fernet(self.encryption_key.encode())
            except Exception as e:
                logging.warning(f"Failed to initialize encryption: {e}")
    
    def get_secret(self, key: str, default: Any = None) -> Any:
        """
        Get secret from multiple sources with fallback.
        
        Search order:
        1. Environment variable
        2. Docker secrets (/run/secrets/)
        3. Encrypted .env.enc file
        4. Default value
        
        Args:
            key: Secret key name
            default: Default value if secret not found
            
        Returns:
            Secret value
        """
        # 1. Check environment variable
        value = os.environ.get(key)
        if value is not None:
            return self._decrypt_if_needed(value)
        
        # 2. Check Docker secrets
        docker_secret_path = Path(f'/run/secrets/{key}')
        if docker_secret_path.exists():
            try:
                value = docker_secret_path.read_text().strip()
                return self._decrypt_if_needed(value)
            except Exception as e:
                logging.error(f"Failed to read Docker secret {key}: {e}")
        
        # 3. Check encrypted .env file
        if self.fernet:
            encrypted_value = self._get_from_encrypted_env(key)
            if encrypted_value:
                return encrypted_value
        
        # 4. Return default
        return default
    
    def _decrypt_if_needed(self, value: str) -> str:
        """Decrypt value if it appears to be encrypted."""
        if not self.fernet or not value.startswith('gAAAAA'):
            return value
        
        try:
            return self.fernet.decrypt(value.encode()).decode()
        except Exception:
            # Not actually encrypted or wrong key
            return value
    
    def _get_from_encrypted_env(self, key: str) -> Optional[str]:
        """Get secret from encrypted .env file."""
        encrypted_env_path = Path('.env.enc')
        if encrypted_env_path.exists():
            try:
                with open('.env.enc', 'r') as f:
                    for line in f:
                        if line.startswith(f'{key}='):
                            encrypted_value = line.split('=', 1)[1].strip()
                            return self.fernet.decrypt(encrypted_value.encode()).decode()
            except Exception as e:
                logging.error(f"Failed to read encrypted .env: {e}")
        return None
    
    @staticmethod
    def generate_encryption_key() -> str:
        """Generate a new Fernet encryption key."""
        return Fernet.generate_key().decode()
    
    @staticmethod
    def generate_secret_key(length: int = 32) -> str:
        """Generate a secure random secret key."""
        return secrets.token_urlsafe(length)

# ============================================================================
# SECTION 5: CONFIGURATION CLASSES WITH VALIDATION
# ============================================================================

class DatabaseConfig(BaseModel):
    """Database configuration model with validation."""
    
    url: str = Field(..., description="Database connection URL")
    pool_size: int = Field(10, ge=1, le=50, description="Connection pool size")
    max_overflow: int = Field(20, ge=0, description="Max overflow connections")
    pool_timeout: int = Field(30, ge=1, description="Connection timeout in seconds")
    pool_recycle: int = Field(3600, ge=60, description="Connection recycle time")
    echo: bool = Field(False, description="Log SQL queries")
    
    @validator('url')
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if not v:
            raise ValueError("Database URL cannot be empty")
        
        # Check for common database URLs
        valid_schemes = ['postgresql', 'mysql', 'sqlite', 'oracle', 'mssql']
        scheme = v.split('://')[0] if '://' in v else ''
        
        if scheme not in valid_schemes:
            logging.warning(f"Unusual database scheme: {scheme}")
        
        return v

class RedisConfig(BaseModel):
    """Redis configuration model."""
    
    host: str = Field("localhost", description="Redis host")
    port: int = Field(6379, ge=1, le=65535, description="Redis port")
    db: int = Field(0, ge=0, le=15, description="Redis database number")
    password: Optional[str] = Field(None, description="Redis password")
    ssl: bool = Field(False, description="Use SSL connection")
    decode_responses: bool = Field(True, description="Decode responses as strings")
    
    @property
    def connection_string(self) -> str:
        """Get Redis connection string."""
        auth = f":{self.password}@" if self.password else ""
        scheme = "rediss" if self.ssl else "redis"
        return f"{scheme}://{auth}{self.host}:{self.port}/{self.db}"

class APIConfig(BaseModel):
    """API-specific configuration."""
    
    title: str = Field("My Flask API", description="API title")
    version: str = Field("1.0.0", description="API version")
    description: str = Field("Flask REST API", description="API description")
    docs_url: Optional[str] = Field("/docs", description="API documentation URL")
    rate_limit: str = Field("100/hour", description="Default rate limit")
    cors_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Allowed CORS origins"
    )
    
    @validator('rate_limit')
    def validate_rate_limit(cls, v):
        """Validate rate limit format (e.g., '100/hour', '10/minute')."""
        if not any(x in v for x in ['/second', '/minute', '/hour', '/day']):
            raise ValueError("Rate limit must include unit: /second, /minute, /hour, or /day")
        return v

class SecurityConfig(BaseModel):
    """Security configuration with secure defaults."""
    
    secret_key: str = Field(..., min_length=32, description="Flask secret key")
    jwt_secret_key: str = Field(..., min_length=32, description="JWT secret key")
    bcrypt_rounds: int = Field(12, ge=4, le=20, description="BCrypt rounds")
    token_expiry: int = Field(3600, ge=60, description="Token expiry in seconds")
    session_timeout: int = Field(86400, ge=300, description="Session timeout in seconds")
    password_min_length: int = Field(8, ge=6, description="Minimum password length")
    require_https: bool = Field(True, description="Require HTTPS in production")
    csrf_enabled: bool = Field(True, description="Enable CSRF protection")
    secure_cookies: bool = Field(True, description="Use secure cookies")
    
    @validator('secret_key', 'jwt_secret_key', pre=True)
    def generate_secret_if_missing(cls, v):
        """Generate secret key if not provided."""
        if not v or v == "change-me-in-production":
            logging.warning("Generating new secret key - not suitable for production!")
            return secrets.token_urlsafe(32)
        return v

# ============================================================================
# SECTION 6: MAIN CONFIGURATION CLASSES
# ============================================================================

class BaseConfig:
    """
    Base configuration with SECURE DEFAULTS.
    
    Follows principle of secure-by-default:
    - All security features enabled by default
    - Production-safe values
    - Explicit opt-out for development
    """
    
    # ========================================================================
    # Flask Core Configuration
    # ========================================================================
    # Security: Explicitly set for production safety
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'change-me-in-production')
    
    # Never run in debug mode by default (security risk!)
    DEBUG: bool = False
    TESTING: bool = False
    
    # Propagate exceptions to error handlers
    PROPAGATE_EXCEPTIONS: bool = True
    
    # Session configuration (secure defaults)
    SESSION_COOKIE_NAME: str = 'session'
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SECURE: bool = True  # Require HTTPS
    SESSION_COOKIE_SAMESITE: str = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME: int = 86400  # 24 hours
    
    # ========================================================================
    # Database Configuration
    # ========================================================================
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///app.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'max_overflow': 20,
    }
    
    # ========================================================================
    # Redis Configuration
    # ========================================================================
    REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # ========================================================================
    # Security Configuration (Secure Defaults)
    # ========================================================================
    # Password hashing
    BCRYPT_LOG_ROUNDS: int = 12  # Reasonable default (4-31 range)
    
    # JWT Configuration
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hour
    JWT_TOKEN_LOCATION: List[str] = ['headers', 'cookies']
    JWT_COOKIE_SECURE: bool = True
    JWT_COOKIE_CSRF_PROTECT: bool = True
    
    # CORS - Restricted by default
    CORS_ORIGINS: List[str] = []  # Empty = no CORS by default
    
    # ========================================================================
    # Logging Configuration
    # ========================================================================
    LOG_LEVEL: str = 'INFO'
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE: Optional[str] = None
    
    # ========================================================================
    # Feature Flags & Environment Toggles
    # ========================================================================
    # Feature flags (can be toggled by environment)
    FEATURE_API_V2: bool = False
    FEATURE_WEBSOCKETS: bool = False
    FEATURE_GRAPHQL: bool = False
    FEATURE_METRICS: bool = True  # Metrics enabled by default
    FEATURE_HEALTH_CHECKS: bool = True  # Health checks enabled
    
    # External service toggles
    ENABLE_EMAIL_SERVICE: bool = False
    ENABLE_SMS_SERVICE: bool = False
    ENABLE_PAYMENT_GATEWAY: bool = False
    
    # Performance toggles
    ENABLE_CACHING: bool = True
    ENABLE_COMPRESSION: bool = True
    ENABLE_QUERY_LOGGING: bool = False
    
    # ========================================================================
    # Application Settings
    # ========================================================================
    APP_NAME: str = 'Flask Application'
    APP_VERSION: str = '1.0.0'
    
    # API Configuration
    API_PREFIX: str = '/api/v1'
    API_TITLE: str = 'Flask API'
    API_DESCRIPTION: str = 'RESTful API built with Flask'
    API_DOCS_URL: str = '/docs'  # None to disable
    
    # File upload configuration
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER: str = 'uploads'
    ALLOWED_EXTENSIONS: set = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # ========================================================================
    # External Services (empty by default - must be explicitly configured)
    # ========================================================================
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Cloud Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    DATADOG_API_KEY: Optional[str] = None
    
    # ========================================================================
    # Rate Limiting
    # ========================================================================
    RATELIMIT_ENABLED: bool = True
    RATELIMIT_DEFAULT: str = '100/hour'
    RATELIMIT_STORAGE_URL: str = REDIS_URL
    
    # ========================================================================
    # 12-Factor App Compliance
    # ========================================================================
    # Store config in environment variables (already done above)
    # Logs to stdout (configured in setup_logging)
    # Backing services treated as attached resources
    # Build, release, run stages separated
    # Processes are stateless and share-nothing
    # Port binding via environment
    # Concurrency via process model
    # Disposability with fast startup/shutdown
    # Dev/prod parity maintained through configuration
    # Logs as event streams
    # Admin processes run as one-off processes
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate configuration and return list of warnings."""
        warnings = []
        
        # Security warnings
        if cls.SECRET_KEY == 'change-me-in-production':
            warnings.append("SECRET_KEY is using default value - change in production!")
        
        if cls.DEBUG and cls.ENVIRONMENT == Environment.PRODUCTION:
            warnings.append("DEBUG mode enabled in production - security risk!")
        
        if not cls.SESSION_COOKIE_SECURE and cls.ENVIRONMENT == Environment.PRODUCTION:
            warnings.append("SESSION_COOKIE_SECURE is False in production - security risk!")
        
        # Database warnings
        if 'sqlite' in cls.SQLALCHEMY_DATABASE_URI and cls.ENVIRONMENT == Environment.PRODUCTION:
            warnings.append("Using SQLite in production is not recommended")
        
        # Feature flag warnings
        if cls.FEATURE_API_V2 and not cls.API_PREFIX.startswith('/api/v2'):
            warnings.append("FEATURE_API_V2 is True but API_PREFIX doesn't reflect v2")
        
        return warnings


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration.
    
    Features:
    - Debug mode enabled
    - Detailed error pages
    - Local database
    - Development-specific features
    - Less restrictive security
    """
    
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    # Enable debug mode for development
    DEBUG: bool = True
    TESTING: bool = False
    
    # Security relaxations for development
    SESSION_COOKIE_SECURE: bool = False  # Allow HTTP
    JWT_COOKIE_SECURE: bool = False
    PROPAGATE_EXCEPTIONS: bool = True  # Show detailed errors
    
    # Database - use local SQLite for convenience
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///dev.db'
    )
    SQLALCHEMY_ECHO: bool = True  # Log SQL queries
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        'pool_size': 5,
        'pool_timeout': 10,
        'pool_recycle': 1800,
        'max_overflow': 10,
        'echo': True,  # Show SQL queries in logs
    }
    
    # Enable all CORS for development
    CORS_ORIGINS: List[str] = ['*']  # Allow all origins in dev
    
    # Feature flags - enable experimental features
    FEATURE_API_V2: bool = True
    FEATURE_WEBSOCKETS: bool = True
    FEATURE_GRAPHQL: bool = True
    
    # Logging - more verbose
    LOG_LEVEL: str = 'DEBUG'
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
    
    # External services - use mock/stub services
    ENABLE_EMAIL_SERVICE: bool = False  # Use mailcatcher or print to console
    ENABLE_SMS_SERVICE: bool = False    # Use mock SMS service
    
    # Development tools
    FLASK_RUN_EXTRA_FILES: List[str] = ['templates/**/*', 'static/**/*']  # Auto-reload templates
    EXPLAIN_TEMPLATE_LOADING: bool = False
    
    # API Documentation enabled
    API_DOCS_URL: str = '/docs'
    
    # Rate limiting - relaxed for development
    RATELIMIT_DEFAULT: str = '1000/hour'
    
    # File upload - more permissive
    MAX_CONTENT_LENGTH: int = 32 * 1024 * 1024  # 32MB for dev


class TestingConfig(BaseConfig):
    """
    Testing environment configuration.
    
    Features:
    - Test mode enabled
    - In-memory database
    - Disabled CSRF protection
    - Mock external services
    """
    
    ENVIRONMENT: Environment = Environment.TESTING
    
    # Testing flags
    TESTING: bool = True
    DEBUG: bool = False  # Don't use debug mode for tests
    
    # Security relaxations for testing
    WTF_CSRF_ENABLED: bool = False  # Disable CSRF for testing
    SESSION_COOKIE_SECURE: bool = False
    JWT_COOKIE_SECURE: bool = False
    
    # Database - use in-memory SQLite
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO: bool = False
    
    # Disable rate limiting for tests
    RATELIMIT_ENABLED: bool = False
    
    # Feature flags - minimal for testing
    FEATURE_API_V2: bool = False
    FEATURE_WEBSOCKETS: bool = False
    FEATURE_METRICS: bool = False
    
    # External services disabled
    ENABLE_EMAIL_SERVICE: bool = False
    ENABLE_SMS_SERVICE: bool = False
    ENABLE_PAYMENT_GATEWAY: bool = False
    
    # Logging - minimal for tests
    LOG_LEVEL: str = 'WARNING'
    
    # API documentation disabled
    API_DOCS_URL: Optional[str] = None
    
    # Preserve context for testing
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False


class StagingConfig(BaseConfig):
    """
    Staging environment configuration.
    
    Features:
    - Production-like but with development aids
    - Real external services (test credentials)
    - Monitoring enabled
    - Stricter than dev but not full production
    """
    
    ENVIRONMENT: Environment = Environment.STAGING
    
    # Production-like settings
    DEBUG: bool = False
    TESTING: bool = False
    
    # Security - nearly production level
    SESSION_COOKIE_SECURE: bool = True  # Staging should use HTTPS
    JWT_COOKIE_SECURE: bool = True
    
    # Database - real database but possibly separate instance
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'postgresql://user:pass@staging-db.example.com/app'
    )
    
    # CORS - restricted to staging domains
    CORS_ORIGINS: List[str] = [
        'https://staging.example.com',
        'https://api-staging.example.com',
    ]
    
    # Feature flags - enable for staging testing
    FEATURE_API_V2: bool = True  # Test new API in staging
    FEATURE_WEBSOCKETS: bool = False  # Not ready for staging yet
    
    # External services - use test credentials
    ENABLE_EMAIL_SERVICE: bool = True
    SMTP_HOST: str = 'smtp.mailtrap.io'  # Test SMTP service
    SMTP_PORT: int = 2525
    
    # Monitoring - enabled but to staging tools
    SENTRY_DSN: Optional[str] = os.environ.get('SENTRY_DSN_STAGING')
    
    # Logging - more verbose than production
    LOG_LEVEL: str = 'INFO'
    LOG_FILE: Optional[str] = '/var/log/app-staging.log'
    
    # API Rate limiting
    RATELIMIT_DEFAULT: str = '500/hour'


class ProductionConfig(BaseConfig):
    """
    Production environment configuration.
    
    Features:
    - Maximum security
    - Performance optimizations
    - Production monitoring
    - Real external services
    - Minimal logging noise
    """
    
    ENVIRONMENT: Environment = Environment.PRODUCTION
    
    # Security first!
    DEBUG: bool = False
    TESTING: bool = False
    
    # Maximum security settings
    SESSION_COOKIE_SECURE: bool = True  # HTTPS required
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Strict'
    JWT_COOKIE_SECURE: bool = True
    JWT_COOKIE_CSRF_PROTECT: bool = True
    
    # Require HTTPS in production
    PREFERRED_URL_SCHEME: str = 'https'
    
    # Database - production database with optimized settings
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'postgresql://user:pass@production-db.example.com/app'
    )
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        'pool_size': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'max_overflow': 40,
        'pool_pre_ping': True,  # Verify connections before using
    }
    
    # CORS - restricted to production domains only
    CORS_ORIGINS: List[str] = [
        'https://example.com',
        'https://www.example.com',
        'https://api.example.com',
    ]
    
    # Feature flags - stable features only
    FEATURE_API_V2: bool = False  # Keep v1 as default
    FEATURE_WEBSOCKETS: bool = True  # If proven stable
    FEATURE_METRICS: bool = True
    
    # External services - production credentials
    ENABLE_EMAIL_SERVICE: bool = True
    SMTP_HOST: str = os.environ.get('SMTP_HOST', 'smtp.sendgrid.net')
    SMTP_PORT: int = int(os.environ.get('SMTP_PORT', 587))
    
    # Monitoring - production monitoring tools
    SENTRY_DSN: Optional[str] = os.environ.get('SENTRY_DSN')
    DATADOG_API_KEY: Optional[str] = os.environ.get('DATADOG_API_KEY')
    
    # Logging - structured logging for production
    LOG_LEVEL: str = 'WARNING'  # Less verbose
    LOG_FORMAT: str = json.dumps({
        'timestamp': '%(asctime)s',
        'level': '%(levelname)s',
        'name': '%(name)s',
        'message': '%(message)s',
        'request_id': '%(request_id)s',
    })
    LOG_FILE: Optional[str] = '/var/log/app-production.log'
    
    # Performance optimizations
    ENABLE_CACHING: bool = True
    ENABLE_COMPRESSION: bool = True
    
    # Rate limiting - stricter for production
    RATELIMIT_DEFAULT: str = '100/hour'
    RATELIMIT_STORAGE_URL: str = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # API documentation - possibly disabled or limited
    API_DOCS_URL: Optional[str] = '/docs'  # Or None to disable
    
    # File upload limits
    MAX_CONTENT_LENGTH: int = 10 * 1024 * 1024  # 10MB for production


class DockerConfig(ProductionConfig):
    """
    Docker-specific configuration.
    
    Extends production config with Docker optimizations.
    """
    
    ENVIRONMENT: Environment = Environment.DOCKER
    
    # Docker-specific database connection
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@db:5432/app'
    )
    
    # Docker Redis connection
    REDIS_URL: str = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
    
    # Docker health check settings
    HEALTH_CHECK_TIMEOUT: int = 5
    HEALTH_CHECK_INTERVAL: int = 30
    
    # Docker logging - to stdout for container logging
    LOG_FILE: Optional[str] = None  # Log to stdout for Docker
    LOG_LEVEL: str = 'INFO'
    
    # CORS - allow from any origin in Docker (for testing)
    CORS_ORIGINS: List[str] = ['*']


# ============================================================================
# SECTION 7: ENVIRONMENT FILE (.env) HANDLING
# ============================================================================

class EnvironmentFileHandler:
    """
    Advanced .env file handling with multiple file support.
    
    Supports:
    - Multiple .env files (.env, .env.local, .env.production, etc.)
    - Environment-specific overrides
    - Validation and type conversion
    - Secret encryption/decryption
    """
    
    # Order of precedence for .env files (first found wins)
    ENV_FILE_PRECEDENCE = [
        '.env.{environment}.local',  # Environment-specific local overrides
        '.env.local',                 # Local overrides (not in version control)
        '.env.{environment}',         # Environment-specific
        '.env',                       # Base .env file
    ]
    
    @classmethod
    def load_environment_files(cls, environment: Environment) -> None:
        """
        Load environment files in order of precedence.
        
        Args:
            environment: Current environment for file selection
        """
        env_files = []
        
        # Generate list of potential .env files
        for pattern in cls.ENV_FILE_PRECEDENCE:
            env_file = pattern.format(environment=environment.value)
            if Path(env_file).exists():
                env_files.append(env_file)
        
        # Also check for .env file without environment suffix
        if Path('.env').exists():
            env_files.append('.env')
        
        # Load files
        loaded_files = []
        for env_file in env_files:
            try:
                # Use python-dotenv to load the file
                result = load_dotenv(env_file, override=True)
                if result:
                    loaded_files.append(env_file)
                    logging.info(f"Loaded environment file: {env_file}")
            except Exception as e:
                logging.error(f"Failed to load {env_file}: {e}")
        
        if not loaded_files:
            logging.warning("No .env files found, using environment variables only")
        
        return loaded_files
    
    @classmethod
    def validate_required_variables(cls, required_vars: List[str]) -> List[str]:
        """
        Validate that required environment variables are set.
        
        Args:
            required_vars: List of required variable names
            
        Returns:
            List of missing variables
        """
        missing = []
        for var in required_vars:
            if not os.environ.get(var):
                missing.append(var)
        
        if missing:
            logging.error(f"Missing required environment variables: {missing}")
        
        return missing
    
    @classmethod
    def create_env_template(cls, config_class, output_file: str = '.env.example') -> None:
        """
        Create a .env.example template from configuration class.
        
        Args:
            config_class: Configuration class to extract variables from
            output_file: Output file path
        """
        template_lines = [
            "# Environment Configuration Template",
            "# Copy this file to .env and fill in the values",
            "#",
            "# !!! NEVER COMMIT .env FILES WITH SECRETS !!!",
            "#",
            ""
        ]
        
        # Group variables by category
        categories = {
            'Flask Core': ['SECRET_KEY', 'DEBUG', 'TESTING'],
            'Database': ['DATABASE_URL', 'SQLALCHEMY_ECHO'],
            'Redis': ['REDIS_URL'],
            'Security': ['JWT_SECRET_KEY', 'BCRYPT_LOG_ROUNDS'],
            'Email': ['SMTP_HOST', 'SMTP_PORT', 'SMTP_USERNAME', 'SMTP_PASSWORD'],
            'External Services': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'SENTRY_DSN'],
            'Application': ['APP_NAME', 'LOG_LEVEL'],
        }
        
        for category, variables in categories.items():
            template_lines.append(f"# {category}")
            for var in variables:
                # Get default value if exists
                default = getattr(config_class, var, '')
                if default:
                    template_lines.append(f"# {var}={default}")
                else:
                    template_lines.append(f"{var}=")
            template_lines.append("")
        
        # Write template file
        with open(output_file, 'w') as f:
            f.write('\n'.join(template_lines))
        
        logging.info(f"Created environment template: {output_file}")

# ============================================================================
# SECTION 8: CONFIGURATION MANAGER
# ============================================================================

class ConfigurationManager:
    """
    Centralized configuration management.
    
    Handles:
    - Environment detection
    - Configuration loading from multiple sources
    - Validation and transformation
    - Feature flag management
    - Configuration access
    """
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.environment = detect_environment()
        self.config_class = self._get_config_class()
        self.secret_manager = SecretManager()
        self.feature_flags = {}
        self.loaded_sources = []
        
    def _get_config_class(self):
        """Get appropriate configuration class for environment."""
        config_map = {
            Environment.DEVELOPMENT: DevelopmentConfig,
            Environment.TESTING: TestingConfig,
            Environment.STAGING: StagingConfig,
            Environment.PRODUCTION: ProductionConfig,
            Environment.DOCKER: DockerConfig,
            Environment.LOCAL: DevelopmentConfig,
            Environment.CI: TestingConfig,
        }
        return config_map.get(self.environment, ProductionConfig)
    
    def load_configuration(self, app: Flask) -> None:
        """
        Load configuration from all sources in correct order.
        
        Order of precedence (highest to lowest):
        1. Runtime configuration (app.config[] = value)
        2. Environment variables (FLASK_*)
        3. Instance folder configuration
        4. Config class (DevelopmentConfig, ProductionConfig, etc.)
        5. Default Flask configuration
        """
        self.app = app
        
        # Step 1: Load .env files (lowest priority for Flask config, but sets env vars)
        EnvironmentFileHandler.load_environment_files(self.environment)
        
        # Step 2: Load from configuration class (BaseConfig or subclass)
        app.config.from_object(self.config_class)
        
        # Step 3: Load from instance folder (instance/config.py)
        instance_config_path = app.instance_path / 'config.py'
        if instance_config_path.exists():
            app.config.from_pyfile('config.py', silent=True)
            self.loaded_sources.append('instance_config')
        
        # Step 4: Load from environment-specific config file
        env_config_file = os.environ.get('FLASK_CONFIG_FILE')
        if env_config_file and Path(env_config_file).exists():
            app.config.from_pyfile(env_config_file)
            self.loaded_sources.append(f'file:{env_config_file}')
        
        # Step 5: Load Flask environment variables (FLASK_*)
        app.config.from_prefixed_env()
        if 'FLASK_' in ''.join(os.environ.keys()):
            self.loaded_sources.append('flask_env_vars')
        
        # Step 6: Validate configuration
        self._validate_configuration()
        
        # Step 7: Initialize feature flags
        self._initialize_feature_flags()
        
        # Step 8: Apply runtime overrides
        self._apply_runtime_overrides()
        
        # Log configuration summary
        self._log_configuration_summary()
    
    def _validate_configuration(self) -> None:
        """Validate loaded configuration."""
        if not self.app:
            return
        
        # Check for required variables
        required_vars = ['SECRET_KEY']
        missing = EnvironmentFileHandler.validate_required_variables(required_vars)
        
        if missing:
            raise ValueError(f"Missing required configuration: {missing}")
        
        # Get configuration warnings
        warnings = self.config_class.validate()
        for warning in warnings:
            logging.warning(f"Configuration warning: {warning}")
        
        # Validate specific values
        if self.app.config.get('DEBUG') and self.environment == Environment.PRODUCTION:
            logging.critical("DEBUG mode enabled in production! This is a security risk.")
        
        if self.app.config['SECRET_KEY'] == 'change-me-in-production':
            logging.critical("Using default SECRET_KEY in production! Change immediately.")
    
    def _initialize_feature_flags(self) -> None:
        """Initialize feature flags from configuration."""
        if not self.app:
            return
        
        # Extract all FEATURE_* configuration values
        self.feature_flags = {
            key: value for key, value in self.app.config.items()
            if key.startswith('FEATURE_') or key.startswith('ENABLE_')
        }
        
        # Add environment-based feature flags
        self.feature_flags.update({
            'IS_DEVELOPMENT': self.environment == Environment.DEVELOPMENT,
            'IS_PRODUCTION': self.environment == Environment.PRODUCTION,
            'IS_TESTING': self.environment == Environment.TESTING,
            'IS_STAGING': self.environment == Environment.STAGING,
            'ENVIRONMENT': self.environment.value,
        })
    
    def _apply_runtime_overrides(self) -> None:
        """Apply runtime configuration overrides."""
        if not self.app:
            return
        
        # Always force certain settings in production
        if self.environment == Environment.PRODUCTION:
            self.app.config['DEBUG'] = False
            self.app.config['TESTING'] = False
            
            # Ensure secure cookies in production
            self.app.config['SESSION_COOKIE_SECURE'] = True
            self.app.config['JWT_COOKIE_SECURE'] = True
            
            # Ensure secret key is not default
            if self.app.config['SECRET_KEY'] == 'change-me-in-production':
                # Generate a temporary one (should be set via env var)
                self.app.config['SECRET_KEY'] = self.secret_manager.generate_secret_key()
                logging.warning("Generated temporary SECRET_KEY for production")
    
    def _log_configuration_summary(self) -> None:
        """Log configuration summary (excluding secrets)."""
        if not self.app:
            return
        
        safe_config = {}
        for key, value in self.app.config.items():
            # Hide sensitive values
            if any(secret_word in key.lower() for secret_word in ['key', 'secret', 'password', 'token', 'dsn']):
                safe_config[key] = '***HIDDEN***' if value else value
            elif isinstance(value, (str, int, float, bool, type(None))):
                safe_config[key] = value
            else:
                safe_config[key] = type(value).__name__
        
        logging.info(f"Environment: {self.environment.value}")
        logging.info(f"Configuration class: {self.config_class.__name__}")
        logging.info(f"Loaded sources: {', '.join(self.loaded_sources)}")
        logging.info(f"Feature flags: {self.feature_flags}")
        logging.debug(f"Safe configuration: {json.dumps(safe_config, indent=2, default=str)}")
    
    def get_feature_flag(self, flag_name: str, default: bool = False) -> bool:
        """Get feature flag value."""
        return self.feature_flags.get(flag_name, default)
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled."""
        # Try different naming conventions
        variants = [
            f'FEATURE_{feature_name.upper()}',
            f'ENABLE_{feature_name.upper()}',
            feature_name.upper(),
        ]
        
        for variant in variants:
            if variant in self.feature_flags:
                return self.feature_flags[variant]
        
        return False
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback."""
        if not self.app:
            return default
        
        # Try to get from app config
        value = self.app.config.get(key)
        if value is not None:
            return value
        
        # Try to get from environment variable
        env_value = os.environ.get(key)
        if env_value is not None:
            return self._parse_env_value(env_value)
        
        return default
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        # Boolean values
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        if value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # Numeric values
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        
        # List values (comma-separated)
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        
        # JSON values
        if value.startswith('{') or value.startswith('['):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        
        # Default: string
        return value

# ============================================================================
# SECTION 9: 12-FACTOR APP IMPLEMENTATION
# ============================================================================

class TwelveFactorApp:
    """
    Implementation of 12-Factor App principles.
    
    The Twelve Factors:
    1. Codebase - One codebase tracked in revision control, many deploys
    2. Dependencies - Explicitly declare and isolate dependencies
    3. Config - Store config in the environment
    4. Backing services - Treat backing services as attached resources
    5. Build, release, run - Strictly separate build and run stages
    6. Processes - Execute the app as one or more stateless processes
    7. Port binding - Export services via port binding
    8. Concurrency - Scale out via the process model
    9. Disposability - Maximize robustness with fast startup and graceful shutdown
    10. Dev/prod parity - Keep development, staging, and production as similar as possible
    11. Logs - Treat logs as event streams
    12. Admin processes - Run admin/management tasks as one-off processes
    """
    
    @staticmethod
    def check_compliance(config_manager: ConfigurationManager) -> Dict[str, bool]:
        """
        Check 12-Factor App compliance.
        
        Returns:
            Dictionary mapping factor to compliance status
        """
        compliance = {}
        
        # Factor 1: Codebase (assumed compliant if using version control)
        compliance['codebase'] = True
        
        # Factor 2: Dependencies (check requirements.txt/pyproject.toml)
        compliance['dependencies'] = Path('requirements.txt').exists() or Path('pyproject.toml').exists()
        
        # Factor 3: Config in environment
        compliance['config'] = all([
            os.environ.get('SECRET_KEY') != 'change-me-in-production',
            os.environ.get('DATABASE_URL') is not None,
        ])
        
        # Factor 4: Backing services as attached resources
        compliance['backing_services'] = all([
            config_manager.get_config_value('SQLALCHEMY_DATABASE_URI'),
            config_manager.get_config_value('REDIS_URL'),
        ])
        
        # Factor 5: Build, release, run separation
        compliance['build_release_run'] = os.environ.get('FLASK_ENV') is not None
        
        # Factor 6: Stateless processes
        compliance['stateless_processes'] = not config_manager.get_config_value('SESSION_TYPE') == 'filesystem'
        
        # Factor 7: Port binding
        compliance['port_binding'] = True  # Flask binds to port by default
        
        # Factor 8: Concurrency
        compliance['concurrency'] = config_manager.get_config_value('WEB_CONCURRENCY') is not None
        
        # Factor 9: Disposability
        compliance['disposability'] = config_manager.get_config_value('GRACEFUL_SHUTDOWN_TIMEOUT') is not None
        
        # Factor 10: Dev/prod parity
        compliance['dev_prod_parity'] = (
            config_manager.environment != Environment.PRODUCTION or
            not config_manager.get_config_value('DEBUG', False)
        )
        
        # Factor 11: Logs as event streams
        compliance['logs'] = config_manager.get_config_value('LOG_FILE') is None  # Should log to stdout
        
        # Factor 12: Admin processes
        compliance['admin_processes'] = True  # Flask CLI provides this
        
        return compliance

# ============================================================================
# SECTION 10: APPLICATION FACTORY WITH ADVANCED CONFIG
# ============================================================================

def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Application factory with comprehensive configuration.
    
    Args:
        config_name: Optional configuration name to force
        
    Returns:
        Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Initialize configuration manager
    config_manager = ConfigurationManager(app)
    
    # Override environment if specified
    if config_name:
        config_manager.environment = Environment(config_name)
    
    # Load configuration
    config_manager.load_configuration(app)
    
    # ========================================================================
    # Apply configuration-based settings
    # ========================================================================
    
    # Setup logging based on configuration
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register before/after request hooks
    register_hooks(app, config_manager)
    
    # Register blueprints (conditionally based on feature flags)
    register_blueprints(app, config_manager)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Register context processors
    register_context_processors(app, config_manager)
    
    # ========================================================================
    # Add configuration endpoints (for debugging/config inspection)
    # ========================================================================
    if config_manager.get_feature_flag('FEATURE_CONFIG_ENDPOINTS', False):
        register_config_endpoints(app, config_manager)
    
    # ========================================================================
    # Check 12-Factor compliance
    # ========================================================================
    if app.config.get('CHECK_12FACTOR', False):
        compliance = TwelveFactorApp.check_compliance(config_manager)
        non_compliant = [k for k, v in compliance.items() if not v]
        if non_compliant:
            logging.warning(f"12-Factor non-compliant factors: {non_compliant}")
    
    return app

def setup_logging(app: Flask) -> None:
    """Setup logging based on configuration."""
    # Remove default Flask handler
    app.logger.removeHandler(default_handler)
    
    # Configure logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    log_format = app.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    app.logger.addHandler(console_handler)
    
    # File handler if configured
    log_file = app.config.get('LOG_FILE')
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(file_handler)
    
    app.logger.setLevel(log_level)
    
    # Set other loggers to same level
    logging.getLogger('werkzeug').setLevel(log_level)
    logging.getLogger('sqlalchemy.engine').setLevel(
        logging.DEBUG if app.config.get('SQLALCHEMY_ECHO') else logging.WARNING
    )

def register_config_endpoints(app: Flask, config_manager: ConfigurationManager) -> None:
    """Register configuration inspection endpoints."""
    
    @app.route('/config/environment', methods=['GET'])
    def get_environment():
        """Get current environment information."""
        return jsonify({
            'environment': config_manager.environment.value,
            'config_class': config_manager.config_class.__name__,
            'loaded_sources': config_manager.loaded_sources,
        })
    
    @app.route('/config/features', methods=['GET'])
    def get_features():
        """Get feature flags."""
        return jsonify({
            'feature_flags': config_manager.feature_flags,
        })
    
    @app.route('/config/values', methods=['GET'])
    def get_config_values():
        """Get safe configuration values (secrets hidden)."""
        safe_config = {}
        for key, value in app.config.items():
            if any(secret_word in key.lower() for secret_word in 
                   ['key', 'secret', 'password', 'token', 'dsn']):
                safe_config[key] = '***HIDDEN***'
            else:
                safe_config[key] = value
        
        return jsonify(safe_config)
    
    @app.route('/config/12factor', methods=['GET'])
    def get_12factor_compliance():
        """Check 12-Factor App compliance."""
        compliance = TwelveFactorApp.check_compliance(config_manager)
        return jsonify({
            'compliance': compliance,
            'score': f"{sum(compliance.values())}/{len(compliance)}",
        })

# ============================================================================
# SECTION 11: USAGE EXAMPLES
# ============================================================================

# Example 1: Creating app with automatic environment detection
app = create_app()

# Example 2: Creating app with specific environment
production_app = create_app('production')

# Example 3: Accessing configuration in routes
@app.route('/config-demo')
def config_demo():
    """Demonstrate configuration access patterns."""
    
    # Method 1: Direct from app.config (preferred)
    debug_mode = current_app.config['DEBUG']
    secret_key = current_app.config['SECRET_KEY'][:8] + '...'  # Show partial
    
    # Method 2: Using configuration manager
    config_manager = current_app.extensions['config_manager']
    is_production = config_manager.get_feature_flag('IS_PRODUCTION')
    
    # Method 3: Feature flag check
    api_v2_enabled = config_manager.is_feature_enabled('api_v2')
    
    # Method 4: Environment-based logic
    if current_app.config['ENVIRONMENT'] == 'development':
        # Development-specific logic
        pass
    
    return jsonify({
        'debug': debug_mode,
        'secret_key_preview': secret_key,
        'is_production': is_production,
        'api_v2_enabled': api_v2_enabled,
        'environment': current_app.config['ENVIRONMENT'],
    })

# Example 4: Environment-based feature toggles
@app.route('/experimental-feature')
def experimental_feature():
    """Route that's only available in certain environments."""
    
    config_manager = current_app.extensions['config_manager']
    
    # Check if feature is enabled
    if not config_manager.is_feature_enabled('experimental'):
        return jsonify({'error': 'Feature not available'}), 404
    
    # Feature-specific logic
    return jsonify({'message': 'Experimental feature is enabled!'})

# Example 5: Secure configuration access with defaults
def get_database_config():
    """Get database configuration with secure defaults."""
    return {
        'url': current_app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:'),
        'pool_size': current_app.config.get('SQLALCHEMY_POOL_SIZE', 5),
        'echo': current_app.config.get('SQLALCHEMY_ECHO', False),
    }

# ============================================================================
# SECTION 12: CONFIGURATION FILES EXAMPLE
# ============================================================================

"""
Example .env file:
# Flask Application Configuration
# Environment: development

# Flask Core
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dev_db
SQLALCHEMY_ECHO=True

# Redis
REDIS_URL=redis://localhost:6379/0

# Feature Flags
FEATURE_API_V2=True
FEATURE_WEBSOCKETS=True

Example .env.production file:
# Production Configuration
# NEVER COMMIT THIS FILE!

SECRET_KEY=${PRODUCTION_SECRET_KEY}  # Set via CI/CD pipeline
DEBUG=False
DATABASE_URL=${PRODUCTION_DATABASE_URL}
REDIS_URL=${PRODUCTION_REDIS_URL}
SENTRY_DSN=${SENTRY_DSN}
FEATURE_API_V2=False  # Keep v1 stable in production

Example instance/config.py (local overrides):
# Instance-specific configuration
# This file is in instance/ folder (not in version control)

DEBUG = True  # Override for local development
SQLALCHEMY_DATABASE_URI = 'sqlite:///local_dev.db'
FEATURE_EXPERIMENTAL = True  # Enable experimental feature locally
"""

# ============================================================================
# SECTION 13: MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    """
    Main entry point demonstrating configuration in action.
    """
    
    # Detect environment
    env = detect_environment()
    print(f"Detected environment: {env.value}")
    
    # Create app with detected environment
    app = create_app()
    
    # Get configuration manager
    config_manager = app.extensions.get('config_manager')
    
    # Print configuration summary
    print(f"\n=== CONFIGURATION SUMMARY ===")
    print(f"Environment: {env.value}")
    print(f"Config class: {config_manager.config_class.__name__}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}")
    
    # Print feature flags
    print(f"\n=== FEATURE FLAGS ===")
    for flag, value in sorted(config_manager.feature_flags.items()):
        if isinstance(value, bool):
            status = "✓" if value else "✗"
            print(f"  {status} {flag}")
    
    # Check 12-Factor compliance
    print(f"\n=== 12-FACTOR COMPLIANCE ===")
    compliance = TwelveFactorApp.check_compliance(config_manager)
    for factor, compliant in compliance.items():
        status = "✓" if compliant else "✗"
        print(f"  {status} {factor}")
    
    # Run the application
    print(f"\n=== STARTING APPLICATION ===")
    print(f"Access configuration endpoints:")
    print(f"  http://localhost:5000/config/environment")
    print(f"  http://localhost:5000/config/features")
    print(f"  http://localhost:5000/config/12factor")
    
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )

# ============================================================================
# SECTION 14: BEST PRACTICES SUMMARY
# ============================================================================
"""
FLASK CONFIGURATION BEST PRACTICES:

1. SECURE DEFAULTS:
   - Always assume production environment
   - Enable security features by default
   - Generate secure random keys
   - Disable debug mode in production

2. ENVIRONMENT MANAGEMENT:
   - Use FLASK_ENV for Flask-specific settings
   - Use APP_ENV for application environment
   - Support multiple .env files for different environments
   - Never commit .env files with secrets

3. CONFIGURATION PRECEDENCE:
   - Environment variables (highest priority)
   - Instance folder configuration
   - Configuration classes
   - Default values (lowest priority)

4. SECRETS MANAGEMENT:
   - Store secrets in environment variables
   - Use secret managers for production (AWS Secrets Manager, HashiCorp Vault)
   - Encrypt sensitive configuration
   - Rotate secrets regularly

5. FEATURE FLAGS:
   - Use feature flags for gradual rollouts
   - Implement environment-based toggles
   - Separate feature flags from configuration
   - Monitor feature flag usage

6. 12-FACTOR APP PRINCIPLES:
   - Store config in environment
   - Treat backing services as attached resources
   - Build, release, run separation
   - Log to stdout/stderr
   - Stateless processes
   - Port binding
   - Dev/prod parity

7. VALIDATION:
   - Validate configuration on startup
   - Type checking for configuration values
   - Required variable validation
   - Environment-specific validation

8. DOCUMENTATION:
   - Maintain .env.example template
   - Document all configuration options
   - Document feature flags
   - Document environment variables

9. MONITORING:
   - Monitor configuration changes
   - Alert on security misconfigurations
   - Track feature flag usage
   - Monitor 12-Factor compliance

10. TESTING:
    - Test configuration in all environments
    - Test feature flag behavior
    - Test security configurations
    - Test configuration validation
"""