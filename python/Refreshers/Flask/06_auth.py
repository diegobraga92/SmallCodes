"""
COMPREHENSIVE FLASK AUTHENTICATION & AUTHORIZATION TUTORIAL
This application demonstrates professional authentication and authorization patterns.
"""

import os
import datetime
import json
from typing import Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, asdict
from functools import wraps
from enum import Enum

# Flask and related imports
from flask import Flask, request, jsonify, make_response, abort, g, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_, or_
from sqlalchemy.exc import SQLAlchemyError
import bcrypt
import jwt
from jwt import PyJWTError
from cryptography.fernet import Fernet
import secrets
import uuid
from datetime import datetime, timedelta, timezone

# Security imports
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized, Forbidden, BadRequest

# Initialize Flask app
app = Flask(__name__)

# ============================================================================
# 1. CONFIGURATION & SECURITY SETTINGS
# ============================================================================

"""
SECURITY CONFIGURATION PRINCIPLES:
1. Never hardcode secrets in code
2. Use environment variables for sensitive data
3. Implement proper key rotation
4. Use strong encryption algorithms
5. Set reasonable expiration times
"""

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))
app.config['REFRESH_TOKEN_SECRET'] = os.environ.get('REFRESH_TOKEN_SECRET', secrets.token_hex(32))
app.config['ENCRYPTION_KEY'] = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key())

# JWT Configuration
app.config['JWT_ALGORITHM'] = 'HS256'  # Use RS256 with public/private keys in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # Short-lived access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)     # Longer-lived refresh token
app.config['JWT_COOKIE_SECURE'] = True  # Only send over HTTPS in production
app.config['JWT_COOKIE_HTTPONLY'] = True  # Prevent XSS attacks
app.config['JWT_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security headers
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', secrets.token_hex(16))
app.config['RATE_LIMIT_PER_MINUTE'] = 60  # Requests per minute for auth endpoints

db = SQLAlchemy(app)

# Initialize encryption
fernet = Fernet(app.config['ENCRYPTION_KEY'])


# ============================================================================
# 2. DATABASE MODELS FOR AUTHENTICATION
# ============================================================================

class User(db.Model):
    """
    User model with authentication fields.
    
    Best Practices:
    1. Never store plain text passwords
    2. Use strong hashing algorithms (bcrypt recommended)
    3. Include timestamps for security auditing
    4. Implement account locking mechanisms
    5. Track failed login attempts
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)  # Store hashed passwords only
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    
    # Security tracking
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_login_at = db.Column(db.DateTime)
    password_changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    account_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Multi-factor authentication
    mfa_enabled = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(32))  # Encrypted TOTP secret
    
    # Relationships
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    sessions = db.relationship('UserSession', back_populates='user', 
                              cascade='all, delete-orphan')
    refresh_tokens = db.relationship('RefreshToken', back_populates='user',
                                    cascade='all, delete-orphan')
    
    # Password reset
    reset_token = db.Column(db.String(100))
    reset_token_expires = db.Column(db.DateTime)
    
    def __init__(self, **kwargs):
        """Override init to hash password automatically."""
        if 'password' in kwargs:
            password = kwargs.pop('password')
            self.set_password(password)
        super().__init__(**kwargs)
    
    def set_password(self, password: str):
        """
        Hash and store password securely.
        
        Uses bcrypt with appropriate work factor.
        NEVER store plain text passwords.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=12)  # Appropriate work factor
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        self.password_changed_at = datetime.utcnow()
    
    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash.
        
        Uses constant-time comparison to prevent timing attacks.
        """
        if not self.password_hash:
            return False
        
        # Use constant-time comparison
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False
    
    def increment_failed_attempts(self):
        """Increment failed login attempts and lock account if threshold reached."""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts (adjust as needed)
        if self.failed_login_attempts >= 5:
            self.is_locked = True
        
        db.session.commit()
    
    def reset_failed_attempts(self):
        """Reset failed login attempts (call on successful login)."""
        self.failed_login_attempts = 0
        self.is_locked = False
        self.last_login_at = datetime.utcnow()
        db.session.commit()
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_name: str) -> bool:
        """Check if user has a specific permission."""
        for role in self.roles:
            if any(perm.name == permission_name for perm in role.permissions):
                return True
        return False
    
    def generate_mfa_secret(self) -> str:
        """Generate a new MFA secret (would use pyotp in real implementation)."""
        # In production, use: pyotp.random_base32()
        self.mfa_secret = fernet.encrypt(secrets.token_hex(16).encode()).decode()
        return self.mfa_secret
    
    def verify_mfa(self, token: str) -> bool:
        """Verify MFA token (placeholder implementation)."""
        if not self.mfa_enabled or not self.mfa_secret:
            return True  # MFA not required
        
        # In production, use: pyotp.TOTP(fernet.decrypt(self.mfa_secret)).verify(token)
        return True  # Placeholder
    
    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model):
    """
    Role model for Role-Based Access Control (RBAC).
    
    RBAC Principles:
    1. Assign permissions to roles, not users
    2. Assign roles to users
    3. Hierarchical roles can inherit permissions
    4. Separation of duties
    """
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_default = db.Column(db.Boolean, default=False)  # Auto-assign to new users
    
    # Hierarchical RBAC (optional)
    parent_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    parent = db.relationship('Role', remote_side=[id], backref='children')
    
    # Relationships
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    permissions = db.relationship('Permission', secondary='role_permissions',
                                 back_populates='roles')
    
    def has_permission(self, permission_name: str) -> bool:
        """Check if role has permission (including inherited)."""
        # Check direct permissions
        if any(perm.name == permission_name for perm in self.permissions):
            return True
        
        # Check inherited permissions from parent roles
        if self.parent:
            return self.parent.has_permission(permission_name)
        
        return False
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model):
    """
    Permission model for fine-grained access control.
    
    Common permission patterns:
    1. Resource-based: 'user:read', 'user:write', 'order:delete'
    2. Action-based: 'can_view_dashboard', 'can_manage_users'
    3. Scope-based: 'read:own_profile', 'write:any_order'
    """
    
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    # Resource type and action (e.g., 'user:create', 'order:read')
    resource = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    
    # Scope: 'own', 'team', 'any'
    scope = db.Column(db.String(20), default='any')
    
    # Relationships
    roles = db.relationship('Role', secondary='role_permissions', back_populates='permissions')
    
    def __repr__(self):
        return f'<Permission {self.name}>'


# Association tables
class UserRole(db.Model):
    """Association table for User-Role many-to-many relationship."""
    
    __tablename__ = 'user_roles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Optional: expiration for temporary role assignments
    expires_at = db.Column(db.DateTime)


class RolePermission(db.Model):
    """Association table for Role-Permission many-to-many relationship."""
    
    __tablename__ = 'role_permissions'
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)


class RefreshToken(db.Model):
    """
    Refresh token model for token rotation and revocation.
    
    Security Best Practices:
    1. Store hashed refresh tokens (not plain text)
    2. Implement token rotation
    3. Allow token revocation
    4. Track device information
    """
    
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False, unique=True, index=True)
    
    # Device tracking
    device_id = db.Column(db.String(100))  # Unique device identifier
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # Supports IPv6
    
    # Token metadata
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)
    revoked_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', back_populates='refresh_tokens')
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not expired or revoked)."""
        return not self.is_expired and not self.is_revoked
    
    def revoke(self):
        """Revoke this refresh token."""
        self.is_revoked = True
        self.revoked_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def create_token(cls, user_id: int, device_id: str = None, 
                    user_agent: str = None, ip_address: str = None) -> Tuple[str, 'RefreshToken']:
        """
        Create a new refresh token.
        
        Returns:
            tuple: (plain_text_token, token_instance)
        """
        # Generate random token
        plain_token = secrets.token_urlsafe(64)
        token_hash = bcrypt.hashpw(plain_token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create token instance
        expires_at = datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        
        token = cls(
            user_id=user_id,
            token_hash=token_hash,
            device_id=device_id,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=expires_at
        )
        
        db.session.add(token)
        db.session.commit()
        
        return plain_token, token
    
    @classmethod
    def verify_token(cls, token: str) -> Optional['RefreshToken']:
        """
        Verify a refresh token.
        
        Returns the token instance if valid, None otherwise.
        """
        if not token:
            return None
        
        # Find all active tokens for this user (optimization: add user_id to token for lookup)
        tokens = cls.query.filter(
            cls.is_revoked == False,
            cls.expires_at > datetime.utcnow()
        ).all()
        
        for token_instance in tokens:
            try:
                if bcrypt.checkpw(token.encode('utf-8'), token_instance.token_hash.encode('utf-8')):
                    return token_instance
            except (ValueError, TypeError):
                continue
        
        return None
    
    def __repr__(self):
        return f'<RefreshToken {self.id} for User {self.user_id}>'


class UserSession(db.Model):
    """
    User session model for session management.
    
    Useful for:
    1. Tracking active sessions
    2. Forcing logout from specific devices
    3. Session analytics
    4. Security auditing
    """
    
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(100), unique=True, nullable=False)
    
    # Device information
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    device_type = db.Column(db.String(50))  # mobile, desktop, tablet
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    
    # Session metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Termination
    terminated_at = db.Column(db.DateTime)
    termination_reason = db.Column(db.String(100))  # logout, expired, security
    
    # Relationships
    user = db.relationship('User', back_populates='sessions')
    
    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False
    
    def refresh_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
        db.session.commit()
    
    def terminate(self, reason: str = "logout"):
        """Terminate this session."""
        self.is_active = False
        self.terminated_at = datetime.utcnow()
        self.termination_reason = reason
        db.session.commit()
    
    def __repr__(self):
        return f'<UserSession {self.id} for User {self.user_id}>'


class AuditLog(db.Model):
    """
    Audit log for security events.
    
    Critical for:
    1. Security monitoring
    2. Compliance requirements (GDPR, HIPAA, etc.)
    3. Incident investigation
    4. User behavior analytics
    """
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # User information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    username = db.Column(db.String(80))
    ip_address = db.Column(db.String(45))
    
    # Event details
    event_type = db.Column(db.String(50), nullable=False)  # login, logout, permission_granted, etc.
    event_subtype = db.Column(db.String(50))  # success, failure, attempt
    severity = db.Column(db.String(20))  # info, warning, error, critical
    
    # Resource affected
    resource_type = db.Column(db.String(50))  # user, order, payment, etc.
    resource_id = db.Column(db.String(100))
    
    # Event data (JSON)
    details = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    @classmethod
    def log_event(cls, event_type: str, user_id: int = None, username: str = None,
                  ip_address: str = None, **kwargs):
        """Helper method to log security events."""
        log = cls(
            event_type=event_type,
            user_id=user_id,
            username=username,
            ip_address=ip_address or request.remote_addr if request else None,
            **kwargs
        )
        
        db.session.add(log)
        db.session.commit()
    
    def __repr__(self):
        return f'<AuditLog {self.event_type} at {self.timestamp}>'


# ============================================================================
# 3. JWT TOKEN MANAGEMENT
# ============================================================================

@dataclass
class TokenPair:
    """Container for access and refresh tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON response."""
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in
        }


class JWTManager:
    """
    JWT Token Manager for creating and validating tokens.
    
    JWT Best Practices:
    1. Keep tokens short-lived (15-30 minutes for access tokens)
    2. Use refresh tokens for long-lived sessions
    3. Include minimal necessary claims
    4. Validate token signature and claims
    5. Implement token blacklisting/revocation for sensitive operations
    """
    
    @staticmethod
    def create_access_token(user: User, additional_claims: Dict = None) -> str:
        """
        Create a JWT access token.
        
        Claims should include:
        - Subject (user identifier)
        - Expiration time
        - Issued at time
        - User roles/permissions (optional)
        - Custom claims
        """
        # Calculate expiration
        expires_delta = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        expires_at = datetime.utcnow() + expires_delta
        
        # Base claims
        claims = {
            'sub': str(user.id),  # Subject (user ID)
            'exp': expires_at,    # Expiration time
            'iat': datetime.utcnow(),  # Issued at
            'type': 'access',     # Token type
            'username': user.username,
            'email': user.email,
            'is_verified': user.is_verified,
            'mfa_enabled': user.mfa_enabled
        }
        
        # Add roles and permissions (be careful not to make token too large)
        if user.roles:
            claims['roles'] = [role.name for role in user.roles]
            
            # Add permissions if needed (consider token size)
            permissions = set()
            for role in user.roles:
                for perm in role.permissions:
                    permissions.add(perm.name)
            claims['permissions'] = list(permissions)
        
        # Add any additional claims
        if additional_claims:
            claims.update(additional_claims)
        
        # Create JWT
        token = jwt.encode(
            claims,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        # Log token issuance
        AuditLog.log_event(
            event_type='token_issued',
            event_subtype='access',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr if request else None,
            details={'token_type': 'access', 'expires_at': expires_at.isoformat()}
        )
        
        return token
    
    @staticmethod
    def create_refresh_token(user: User, device_info: Dict = None) -> Tuple[str, RefreshToken]:
        """
        Create a refresh token and store it in database.
        
        Refresh tokens:
        1. Are long-lived (days/weeks)
        2. Stored securely in database (hashed)
        3. Can be revoked
        4. Used to obtain new access tokens
        """
        device_id = device_info.get('device_id') if device_info else None
        user_agent = device_info.get('user_agent') if device_info else request.user_agent.string
        ip_address = device_info.get('ip_address') if device_info else request.remote_addr
        
        # Create and store refresh token
        plain_token, token_instance = RefreshToken.create_token(
            user_id=user.id,
            device_id=device_id,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        # Log refresh token issuance
        AuditLog.log_event(
            event_type='token_issued',
            event_subtype='refresh',
            user_id=user.id,
            username=user.username,
            ip_address=ip_address,
            details={'token_type': 'refresh', 'device_id': device_id}
        )
        
        return plain_token, token_instance
    
    @staticmethod
    def create_token_pair(user: User, device_info: Dict = None) -> TokenPair:
        """
        Create both access and refresh tokens.
        
        This is the standard pattern:
        1. Short-lived access token for API calls
        2. Long-lived refresh token for obtaining new access tokens
        """
        access_token = JWTManager.create_access_token(user)
        refresh_token, _ = JWTManager.create_refresh_token(user, device_info)
        
        expires_in = int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )
    
    @staticmethod
    def verify_access_token(token: str) -> Dict:
        """
        Verify JWT access token.
        
        Validates:
        1. Signature
        2. Expiration time
        3. Token type
        4. Required claims
        """
        if not token:
            raise ValueError("Token is required")
        
        try:
            # Decode and verify token
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']],
                options={
                    'require': ['exp', 'iat', 'sub', 'type'],
                    'verify_exp': True,
                    'verify_iat': True
                }
            )
            
            # Additional validation
            if payload.get('type') != 'access':
                raise jwt.InvalidTokenError("Invalid token type")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            AuditLog.log_event(
                event_type='token_verification',
                event_subtype='expired',
                details={'error': 'Token expired'}
            )
            raise Unauthorized("Token has expired")
        except jwt.InvalidTokenError as e:
            AuditLog.log_event(
                event_type='token_verification',
                event_subtype='invalid',
                severity='warning',
                details={'error': str(e)}
            )
            raise Unauthorized("Invalid token")
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> TokenPair:
        """
        Use refresh token to get new access token.
        
        Token Rotation Pattern:
        1. Verify refresh token
        2. Create new access token
        3. Optionally create new refresh token (rotation)
        4. Revoke old refresh token
        """
        # Verify refresh token
        token_instance = RefreshToken.verify_token(refresh_token)
        if not token_instance or not token_instance.is_valid:
            raise Unauthorized("Invalid or expired refresh token")
        
        # Get user
        user = User.query.get(token_instance.user_id)
        if not user or not user.is_active:
            raise Unauthorized("User not found or inactive")
        
        # Optional: Implement refresh token rotation
        # Revoke old token and issue new one
        token_instance.revoke()
        
        # Create new token pair
        device_info = {
            'device_id': token_instance.device_id,
            'user_agent': token_instance.user_agent,
            'ip_address': token_instance.ip_address
        }
        
        new_tokens = JWTManager.create_token_pair(user, device_info)
        
        # Log token refresh
        AuditLog.log_event(
            event_type='token_refreshed',
            user_id=user.id,
            username=user.username,
            ip_address=token_instance.ip_address,
            details={'old_token_id': token_instance.id}
        )
        
        return new_tokens
    
    @staticmethod
    def revoke_all_user_tokens(user_id: int, reason: str = "security"):
        """Revoke all refresh tokens for a user (e.g., on password change)."""
        tokens = RefreshToken.query.filter_by(user_id=user_id, is_revoked=False).all()
        
        for token in tokens:
            token.revoke()
        
        AuditLog.log_event(
            event_type='tokens_revoked',
            event_subtype='all',
            user_id=user_id,
            details={'reason': reason, 'count': len(tokens)}
        )
    
    @staticmethod
    def set_token_cookies(response, token_pair: TokenPair):
        """
        Set JWT tokens as HTTP-only cookies.
        
        Cookie Security:
        1. httpOnly: Prevent JavaScript access (XSS protection)
        2. Secure: Only send over HTTPS
        3. SameSite: CSRF protection
        4. Path: Restrict cookie scope
        """
        # Access token cookie (short-lived)
        response.set_cookie(
            'access_token',
            token_pair.access_token,
            max_age=int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
            httponly=current_app.config['JWT_COOKIE_HTTPONLY'],
            secure=current_app.config['JWT_COOKIE_SECURE'],
            samesite=current_app.config['JWT_COOKIE_SAMESITE'],
            path='/api'
        )
        
        # Refresh token cookie (long-lived)
        response.set_cookie(
            'refresh_token',
            token_pair.refresh_token,
            max_age=int(current_app.config['JWT_REFRESH_TOKEN_EXPIRES'].total_seconds()),
            httponly=True,  # Always httpOnly for refresh tokens
            secure=current_app.config['JWT_COOKIE_SECURE'],
            samesite=current_app.config['JWT_COOKIE_SAMESITE'],
            path='/api/auth/refresh'  # Only sent to refresh endpoint
        )
        
        return response


# ============================================================================
# 4. AUTHENTICATION & AUTHORIZATION DECORATORS
# ============================================================================

def get_current_user() -> Optional[User]:
    """
    Get current user from request.
    
    Supports multiple authentication methods:
    1. Bearer token in Authorization header
    2. JWT in cookie
    3. API key in header (for service-to-service)
    """
    # Try to get token from Authorization header
    auth_header = request.headers.get('Authorization')
    token = None
    
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header[7:]  # Remove 'Bearer ' prefix
    elif 'access_token' in request.cookies:
        token = request.cookies.get('access_token')
    
    if not token:
        return None
    
    try:
        # Verify token
        payload = JWTManager.verify_access_token(token)
        user_id = int(payload['sub'])
        
        # Get user from database
        user = User.query.get(user_id)
        
        # Additional checks
        if not user or not user.is_active:
            return None
        
        # Store user in Flask's g object for request lifetime
        g.current_user = user
        g.token_payload = payload
        
        return user
        
    except (Unauthorized, PyJWTError, ValueError):
        return None


def login_required(f):
    """
    Decorator to require authentication.
    
    How to secure an endpoint and why:
    1. Verify identity (authentication)
    2. Check account status (active, verified, not locked)
    3. Log access attempts
    4. Return proper error responses
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get current user
        user = get_current_user()
        
        if not user:
            # Log failed authentication attempt
            AuditLog.log_event(
                event_type='authentication',
                event_subtype='failed',
                severity='warning',
                ip_address=request.remote_addr,
                details={
                    'reason': 'no_valid_token',
                    'endpoint': request.endpoint,
                    'method': request.method
                }
            )
            
            return jsonify({
                'error': 'Authentication required',
                'code': 'UNAUTHENTICATED'
            }), 401
        
        # Check account status
        if not user.is_active:
            AuditLog.log_event(
                event_type='authentication',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                details={'reason': 'account_inactive'}
            )
            return jsonify({
                'error': 'Account is deactivated',
                'code': 'ACCOUNT_INACTIVE'
            }), 403
        
        if user.is_locked:
            AuditLog.log_event(
                event_type='authentication',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                details={'reason': 'account_locked'}
            )
            return jsonify({
                'error': 'Account is locked due to too many failed attempts',
                'code': 'ACCOUNT_LOCKED'
            }), 423  # 423 Locked
        
        # Log successful authentication
        AuditLog.log_event(
            event_type='authentication',
            event_subtype='success',
            user_id=user.id,
            username=user.username,
            details={'endpoint': request.endpoint}
        )
        
        return f(*args, **kwargs)
    
    return decorated_function


def role_required(*role_names):
    """
    Decorator to require specific roles.
    
    Role-Based Access Control (RBAC):
    1. Define roles with specific permissions
    2. Assign roles to users
    3. Check roles at endpoint level
    4. Hierarchical roles (optional)
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user = g.current_user
            
            # Check if user has any of the required roles
            user_roles = {role.name for role in user.roles}
            required_roles = set(role_names)
            
            if not required_roles.intersection(user_roles):
                # Log authorization failure
                AuditLog.log_event(
                    event_type='authorization',
                    event_subtype='failed',
                    severity='warning',
                    user_id=user.id,
                    username=user.username,
                    details={
                        'required_roles': list(required_roles),
                        'user_roles': list(user_roles),
                        'endpoint': request.endpoint
                    }
                )
                
                return jsonify({
                    'error': 'Insufficient permissions',
                    'code': 'INSUFFICIENT_ROLES',
                    'required': list(required_roles),
                    'has': list(user_roles)
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def permission_required(permission_name: str, resource_id: str = None):
    """
    Decorator to require specific permission.
    
    Fine-grained access control:
    1. Check specific permission
    2. Optional resource ownership check
    3. Support for different scopes (own, team, any)
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user = g.current_user
            
            # Check if user has permission
            if not user.has_permission(permission_name):
                # Log permission failure
                AuditLog.log_event(
                    event_type='authorization',
                    event_subtype='failed',
                    severity='warning',
                    user_id=user.id,
                    username=user.username,
                    details={
                        'required_permission': permission_name,
                        'endpoint': request.endpoint
                    }
                )
                
                return jsonify({
                    'error': 'Insufficient permissions',
                    'code': 'INSUFFICIENT_PERMISSIONS',
                    'required_permission': permission_name
                }), 403
            
            # Check resource ownership if resource_id is provided
            if resource_id:
                # This is a simplified example - implement based on your resource model
                # For example, check if user owns the resource
                pass
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def mfa_required(f):
    """
    Decorator to require Multi-Factor Authentication.
    
    MFA Best Practices:
    1. Require for sensitive operations
    2. Allow temporary bypass for trusted devices
    3. Support different MFA methods (TOTP, SMS, biometric)
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        user = g.current_user
        
        # Check if MFA is enabled and verified
        if user.mfa_enabled:
            mfa_token = request.headers.get('X-MFA-Token') or request.json.get('mfa_token')
            
            if not mfa_token:
                return jsonify({
                    'error': 'MFA token required',
                    'code': 'MFA_REQUIRED'
                }), 403
            
            if not user.verify_mfa(mfa_token):
                AuditLog.log_event(
                    event_type='mfa_verification',
                    event_subtype='failed',
                    severity='warning',
                    user_id=user.id,
                    username=user.username
                )
                return jsonify({
                    'error': 'Invalid MFA token',
                    'code': 'INVALID_MFA_TOKEN'
                }), 403
            
            # Log successful MFA
            AuditLog.log_event(
                event_type='mfa_verification',
                event_subtype='success',
                user_id=user.id,
                username=user.username
            )
        
        return f(*args, **kwargs)
    
    return decorated_function


def rate_limit(requests_per_minute: int = 60, key_func: Callable = None):
    """
    Decorator for rate limiting.
    
    Important for:
    1. Preventing brute force attacks
    2. Protecting against DoS
    3. Fair usage enforcement
    """
    # Simple in-memory rate limiter (use Redis in production)
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Determine rate limit key
            if key_func:
                key = key_func()
            else:
                key = request.remote_addr  # Default: IP-based limiting
            
            current_time = datetime.utcnow()
            minute_key = current_time.strftime('%Y-%m-%d-%H-%M')
            full_key = f"{key}:{minute_key}"
            
            # Get or initialize count
            if full_key not in request_counts:
                request_counts[full_key] = 0
            
            # Check limit
            if request_counts[full_key] >= requests_per_minute:
                AuditLog.log_event(
                    event_type='rate_limit',
                    event_subtype='exceeded',
                    severity='warning',
                    ip_address=request.remote_addr,
                    details={
                        'key': key,
                        'limit': requests_per_minute,
                        'count': request_counts[full_key]
                    }
                )
                
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'code': 'RATE_LIMIT_EXCEEDED',
                    'retry_after': 60
                }), 429
            
            # Increment counter
            request_counts[full_key] += 1
            
            # Cleanup old entries (simplified)
            old_keys = [k for k in request_counts.keys() 
                       if k.split(':')[1] < minute_key]
            for k in old_keys:
                del request_counts[k]
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ============================================================================
# 5. AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
@rate_limit(requests_per_minute=5)  # Strict rate limiting for registration
def register():
    """
    Register a new user.
    
    Security Considerations:
    1. Validate input thoroughly
    2. Hash password immediately
    3. Assign default roles
    4. Send verification email
    5. Log registration attempt
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'username', 'password']
        for field in required_fields:
            if field not in data:
                raise BadRequest(f"Missing required field: {field}")
        
        # Validate email format
        if '@' not in data['email']:
            raise BadRequest("Invalid email format")
        
        # Validate password strength
        password = data['password']
        if len(password) < 8:
            raise BadRequest("Password must be at least 8 characters")
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            raise BadRequest("Email already registered")
        
        if User.query.filter_by(username=data['username']).first():
            raise BadRequest("Username already taken")
        
        # Create user
        user = User(
            email=data['email'],
            username=data['username'],
            password=password  # Will be hashed in __init__
        )
        
        # Assign default role
        default_role = Role.query.filter_by(is_default=True).first()
        if default_role:
            user.roles.append(default_role)
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Create initial audit log
        AuditLog.log_event(
            event_type='registration',
            event_subtype='success',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr,
            details={'method': 'email'}
        )
        
        # In production: Send verification email
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user.id,
            'requires_verification': True
        }), 201
        
    except BadRequest as e:
        AuditLog.log_event(
            event_type='registration',
            event_subtype='failed',
            severity='warning',
            ip_address=request.remote_addr,
            details={'error': str(e), 'data': data}
        )
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/auth/login', methods=['POST'])
@rate_limit(requests_per_minute=10)  # Prevent brute force attacks
def login():
    """
    Authenticate user and issue tokens.
    
    Authentication Flow:
    1. Validate credentials
    2. Check account status
    3. Update security metrics
    4. Issue tokens
    5. Log successful/failed attempts
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'username' not in data or 'password' not in data:
            raise BadRequest("Username and password required")
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username']) | (User.email == data['username'])
        ).first()
        
        # Authentication failed scenarios
        if not user:
            AuditLog.log_event(
                event_type='login',
                event_subtype='failed',
                severity='warning',
                ip_address=request.remote_addr,
                details={'reason': 'user_not_found', 'username': data['username']}
            )
            
            # Don't reveal whether user exists (security through obscurity)
            return jsonify({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS'
            }), 401
        
        # Check if account is locked
        if user.is_locked:
            AuditLog.log_event(
                event_type='login',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                details={'reason': 'account_locked'}
            )
            return jsonify({
                'error': 'Account is locked. Please reset your password.',
                'code': 'ACCOUNT_LOCKED'
            }), 423
        
        # Verify password
        if not user.check_password(data['password']):
            # Increment failed attempts
            user.increment_failed_attempts()
            
            AuditLog.log_event(
                event_type='login',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                ip_address=request.remote_addr,
                details={
                    'reason': 'invalid_password',
                    'failed_attempts': user.failed_login_attempts
                }
            )
            
            return jsonify({
                'error': 'Invalid credentials',
                'code': 'INVALID_CREDENTIALS',
                'remaining_attempts': 5 - user.failed_login_attempts
            }), 401
        
        # Check if account is active
        if not user.is_active:
            AuditLog.log_event(
                event_type='login',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                details={'reason': 'account_inactive'}
            )
            return jsonify({
                'error': 'Account is deactivated',
                'code': 'ACCOUNT_INACTIVE'
            }), 403
        
        # Successful authentication
        user.reset_failed_attempts()
        
        # Collect device information
        device_info = {
            'device_id': request.headers.get('X-Device-ID'),
            'user_agent': request.user_agent.string,
            'ip_address': request.remote_addr
        }
        
        # Create tokens
        token_pair = JWTManager.create_token_pair(user, device_info)
        
        # Log successful login
        AuditLog.log_event(
            event_type='login',
            event_subtype='success',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr,
            details={'device_id': device_info['device_id']}
        )
        
        # Prepare response
        response_data = {
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_verified': user.is_verified,
                'mfa_enabled': user.mfa_enabled,
                'roles': [role.name for role in user.roles]
            },
            'tokens': token_pair.to_dict()
        }
        
        response = jsonify(response_data)
        
        # Set cookies if requested
        if data.get('remember_me'):
            response = JWTManager.set_token_cookies(response, token_pair)
        
        return response
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500


@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh access token using refresh token.
    
    Token Refresh Flow:
    1. Accept refresh token from cookie or body
    2. Verify refresh token
    3. Issue new access token
    4. Optionally rotate refresh token
    """
    try:
        # Get refresh token from cookie or request body
        refresh_token = (
            request.cookies.get('refresh_token') or 
            request.json.get('refresh_token') if request.is_json else None
        )
        
        if not refresh_token:
            raise BadRequest("Refresh token required")
        
        # Get new tokens
        token_pair = JWTManager.refresh_access_token(refresh_token)
        
        response = jsonify({
            'message': 'Token refreshed',
            'tokens': token_pair.to_dict()
        })
        
        # Update cookies if using cookie-based auth
        if request.cookies.get('refresh_token'):
            response = JWTManager.set_token_cookies(response, token_pair)
        
        return response
        
    except Unauthorized as e:
        return jsonify({'error': str(e)}), 401
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Token refresh error: {e}")
        return jsonify({'error': 'Token refresh failed'}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """
    Log out user and revoke tokens.
    
    Proper Logout:
    1. Revoke current refresh token
    2. Clear cookies
    3. Log logout event
    4. Optionally revoke all user sessions
    """
    user = g.current_user
    
    try:
        # Get refresh token from cookie
        refresh_token = request.cookies.get('refresh_token')
        
        # Revoke the refresh token if found
        if refresh_token:
            token_instance = RefreshToken.verify_token(refresh_token)
            if token_instance:
                token_instance.revoke()
        
        # Log logout event
        AuditLog.log_event(
            event_type='logout',
            event_subtype='success',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr
        )
        
        # Prepare response
        response = jsonify({'message': 'Logged out successfully'})
        
        # Clear cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
        
    except Exception as e:
        app.logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Logout failed'}), 500


@app.route('/api/auth/logout/all', methods=['POST'])
@login_required
def logout_all():
    """
    Log out from all devices.
    
    Useful for:
    1. Security breaches
    2. Lost/stolen device
    3. User request
    """
    user = g.current_user
    
    try:
        # Revoke all refresh tokens for this user
        JWTManager.revoke_all_user_tokens(user.id, "logout_all")
        
        # Log event
        AuditLog.log_event(
            event_type='logout',
            event_subtype='all_devices',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr
        )
        
        response = jsonify({
            'message': 'Logged out from all devices',
            'devices_logged_out': True
        })
        
        # Clear cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
        
    except Exception as e:
        app.logger.error(f"Logout all error: {e}")
        return jsonify({'error': 'Logout failed'}), 500


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user_info():
    """
    Get current authenticated user's information.
    
    Demonstrates:
    1. Protected endpoint
    2. User context access
    3. Minimal information exposure
    """
    user = g.current_user
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_verified': user.is_verified,
        'mfa_enabled': user.mfa_enabled,
        'roles': [role.name for role in user.roles],
        'permissions': sorted(list({
            perm.name 
            for role in user.roles 
            for perm in role.permissions
        })),
        'last_login': user.last_login_at.isoformat() if user.last_login_at else None,
        'account_created': user.account_created_at.isoformat()
    }
    
    return jsonify(user_data)


@app.route('/api/auth/change-password', methods=['POST'])
@login_required
@mfa_required  # Require MFA for sensitive operation
def change_password():
    """
    Change user password.
    
    Password Change Security:
    1. Require current password
    2. Enforce password strength
    3. Revoke all existing tokens
    4. Log password change
    """
    user = g.current_user
    
    try:
        data = request.get_json()
        
        if not data or 'current_password' not in data or 'new_password' not in data:
            raise BadRequest("Current and new password required")
        
        # Verify current password
        if not user.check_password(data['current_password']):
            AuditLog.log_event(
                event_type='password_change',
                event_subtype='failed',
                severity='warning',
                user_id=user.id,
                username=user.username,
                details={'reason': 'incorrect_current_password'}
            )
            return jsonify({
                'error': 'Current password is incorrect',
                'code': 'INCORRECT_PASSWORD'
            }), 401
        
        # Validate new password
        new_password = data['new_password']
        if len(new_password) < 8:
            raise BadRequest("New password must be at least 8 characters")
        
        # Don't allow reusing same password
        if user.check_password(new_password):
            raise BadRequest("New password must be different from current password")
        
        # Change password
        user.set_password(new_password)
        
        # Revoke all existing tokens (security best practice)
        JWTManager.revoke_all_user_tokens(user.id, "password_change")
        
        db.session.commit()
        
        # Log password change
        AuditLog.log_event(
            event_type='password_change',
            event_subtype='success',
            user_id=user.id,
            username=user.username,
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Password changed successfully'})
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Password change error: {e}")
        return jsonify({'error': 'Password change failed'}), 500


# ============================================================================
# 6. DEMONSTRATION ENDPOINTS WITH DIFFERENT ACCESS LEVELS
# ============================================================================

# Public endpoint (no authentication required)
@app.route('/api/public/info', methods=['GET'])
def public_info():
    """Public endpoint accessible to anyone."""
    return jsonify({
        'message': 'This is public information',
        'timestamp': datetime.utcnow().isoformat(),
        'requires_auth': False
    })


# Authenticated endpoint (requires login)
@app.route('/api/private/profile', methods=['GET'])
@login_required
def private_profile():
    """Private endpoint accessible to any authenticated user."""
    user = g.current_user
    
    return jsonify({
        'message': f'Welcome, {user.username}!',
        'user_id': user.id,
        'access_level': 'authenticated',
        'timestamp': datetime.utcnow().isoformat()
    })


# Role-protected endpoint
@app.route('/api/admin/dashboard', methods=['GET'])
@role_required('admin', 'superadmin')
def admin_dashboard():
    """Admin-only endpoint."""
    user = g.current_user
    
    return jsonify({
        'message': 'Welcome to the admin dashboard',
        'user': user.username,
        'roles': [role.name for role in user.roles],
        'access_level': 'admin',
        'stats': {
            'total_users': User.query.count(),
            'active_sessions': UserSession.query.filter_by(is_active=True).count()
        }
    })


# Permission-protected endpoint
@app.route('/api/users/<int:user_id>', methods=['GET'])
@permission_required('user:read')
def get_user_by_id(user_id):
    """Get user by ID (requires specific permission)."""
    user = User.query.get_or_404(user_id)
    
    # Check if user has permission to view this specific user
    # Implement resource-level permission check here
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'account_created': user.account_created_at.isoformat()
    })


# MFA-protected endpoint for sensitive operations
@app.route('/api/sensitive/transfer', methods=['POST'])
@login_required
@mfa_required
@permission_required('transfer:create')
def money_transfer():
    """Sensitive operation requiring MFA."""
    data = request.get_json()
    
    # Business logic for money transfer
    # ...
    
    return jsonify({
        'message': 'Transfer initiated',
        'transaction_id': str(uuid.uuid4()),
        'requires_mfa': True,
        'status': 'pending'
    })


# Rate-limited sensitive endpoint
@app.route('/api/auth/reset-password', methods=['POST'])
@rate_limit(requests_per_minute=3)  # Very strict rate limiting
def request_password_reset():
    """
    Request password reset (heavily rate-limited).
    
    Security Considerations:
    1. Prevent email enumeration
    2. Rate limit to prevent abuse
    3. Use time-based tokens
    4. Don't reveal if email exists
    """
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            raise BadRequest("Email required")
        
        # Don't reveal if email exists (security through obscurity)
        user = User.query.filter_by(email=email).first()
        
        if user and user.is_active:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = bcrypt.hashpw(
                reset_token.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
            
            db.session.commit()
            
            # In production: Send email with reset link
            # send_reset_email(user.email, reset_token)
        
        # Always return same response regardless of email existence
        AuditLog.log_event(
            event_type='password_reset',
            event_subtype='requested',
            ip_address=request.remote_addr,
            details={'email_provided': email}
        )
        
        return jsonify({
            'message': 'If the email exists, a reset link has been sent',
            'reset_token_expires_in': 3600  # 1 hour in seconds
        })
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Password reset request error: {e}")
        return jsonify({'error': 'Password reset request failed'}), 500


# ============================================================================
# 7. SECURITY MIDDLEWARE AND HEADERS
# ============================================================================

@app.after_request
def add_security_headers(response):
    """
    Add security headers to all responses.
    
    Important Security Headers:
    1. CSP: Prevent XSS attacks
    2. HSTS: Force HTTPS
    3. X-Frame-Options: Clickjacking protection
    4. X-Content-Type-Options: MIME sniffing prevention
    5. Referrer-Policy: Control referrer information
    """
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' https://api.example.com;"
    )
    
    # HTTP Strict Transport Security (enable in production)
    if app.config.get('ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Other security headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Remove potentially dangerous headers
    if 'Server' in response.headers:
        del response.headers['Server']
    
    return response


@app.before_request
def check_maintenance_mode():
    """
    Global check for maintenance mode or other security measures.
    """
    # Example: Maintenance mode check
    if app.config.get('MAINTENANCE_MODE', False) and request.path.startswith('/api/'):
        return jsonify({
            'error': 'Service temporarily unavailable for maintenance',
            'code': 'MAINTENANCE_MODE'
        }), 503
    
    # Check for suspicious user agents or IPs
    user_agent = request.user_agent.string.lower() if request.user_agent else ''
    suspicious_agents = ['sqlmap', 'nikto', 'zap', 'w3af']
    
    if any(agent in user_agent for agent in suspicious_agents):
        AuditLog.log_event(
            event_type='security',
            event_subtype='suspicious_ua',
            severity='warning',
            ip_address=request.remote_addr,
            details={'user_agent': user_agent}
        )
        
        # Could return 403 or just log, depending on security policy
        # return jsonify({'error': 'Access denied'}), 403


# ============================================================================
# 8. COMMON AUTH PITFALLS AND HOW TO AVOID THEM
# ============================================================================

"""
COMMON AUTH PITFALLS AND SOLUTIONS:

1. PITFALL: Storing plain text passwords
   SOLUTION: Always use strong hashing (bcrypt with appropriate work factor)

2. PITFALL: Short or no token expiration
   SOLUTION: Use short-lived access tokens (15-30 min) with refresh tokens

3. PITFALL: Not validating JWT signatures
   SOLUTION: Always verify JWT signature and claims

4. PITFALL: Exposing sensitive information in tokens
   SOLUTION: Include minimal claims, never include passwords or secrets

5. PITFALL: No rate limiting on auth endpoints
   SOLUTION: Implement strict rate limiting for login, registration, password reset

6. PITFALL: Not logging auth events
   SOLUTION: Log all authentication attempts (success and failure)

7. PITFALL: Weak password policies
   SOLUTION: Enforce minimum length, complexity, and prevent common passwords

8. PITFALL: Not implementing account lockout
   SOLUTION: Lock accounts after too many failed attempts

9. PITFALL: Not using HTTPS in production
   SOLUTION: Always use HTTPS, enforce with HSTS header

10. PITFALL: Not invalidating tokens on password change
    SOLUTION: Revoke all tokens when password changes or account is compromised
"""


# ============================================================================
# 9. ADMINISTRATION ENDPOINTS (DEMONSTRATION ONLY)
# ============================================================================

@app.route('/api/admin/users', methods=['GET'])
@role_required('admin')
def list_users():
    """Admin endpoint to list all users."""
    users = User.query.all()
    
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'is_locked': user.is_locked,
            'roles': [role.name for role in user.roles],
            'last_login': user.last_login_at.isoformat() if user.last_login_at else None,
            'failed_attempts': user.failed_login_attempts
        })
    
    return jsonify({
        'users': user_list,
        'total': len(users)
    })


@app.route('/api/admin/audit-logs', methods=['GET'])
@role_required('admin')
def get_audit_logs():
    """Admin endpoint to view audit logs."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    query = AuditLog.query.order_by(AuditLog.timestamp.desc())
    logs = query.paginate(page=page, per_page=per_page, error_out=False)
    
    log_list = []
    for log in logs.items:
        log_list.append({
            'id': log.id,
            'timestamp': log.timestamp.isoformat(),
            'event_type': log.event_type,
            'event_subtype': log.event_subtype,
            'user_id': log.user_id,
            'username': log.username,
            'ip_address': log.ip_address,
            'severity': log.severity,
            'details': json.loads(log.details) if log.details else None
        })
    
    return jsonify({
        'logs': log_list,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': logs.pages,
            'total_items': logs.total,
            'has_next': logs.has_next,
            'has_prev': logs.has_prev
        }
    })


# ============================================================================
# 10. DATABASE INITIALIZATION AND SAMPLE DATA
# ============================================================================

def init_database():
    """Initialize database with roles, permissions, and sample users."""
    with app.app_context():
        db.create_all()
        
        # Create default roles if they don't exist
        if not Role.query.first():
            # Create permissions
            permissions = [
                # User permissions
                Permission(name='user:read', resource='user', action='read', scope='any'),
                Permission(name='user:write', resource='user', action='write', scope='any'),
                Permission(name='user:delete', resource='user', action='delete', scope='any'),
                
                # Own profile permissions
                Permission(name='profile:read', resource='profile', action='read', scope='own'),
                Permission(name='profile:write', resource='profile', action='write', scope='own'),
                
                # Admin permissions
                Permission(name='admin:dashboard', resource='admin', action='read', scope='any'),
                Permission(name='admin:users', resource='admin', action='manage', scope='any'),
                Permission(name='admin:audit', resource='admin', action='read', scope='any'),
                
                # Financial permissions
                Permission(name='transfer:create', resource='transfer', action='create', scope='own'),
                Permission(name='transfer:read', resource='transfer', action='read', scope='own'),
            ]
            
            # Create roles
            roles = [
                Role(name='user', description='Regular user', is_default=True),
                Role(name='premium', description='Premium user'),
                Role(name='admin', description='Administrator'),
                Role(name='superadmin', description='Super Administrator'),
            ]
            
            # Assign permissions to roles
            # User role gets basic permissions
            for perm in permissions[:5]:  # user and profile permissions
                roles[0].permissions.append(perm)
            
            # Premium role gets additional permissions
            roles[1].permissions.extend(permissions[:7])  # All user/profile plus some
            
            # Admin role gets all permissions
            for perm in permissions:
                roles[2].permissions.append(perm)
            
            # Superadmin gets all permissions (inherits from admin in real implementation)
            for perm in permissions:
                roles[3].permissions.append(perm)
            
            # Add to database
            db.session.add_all(permissions)
            db.session.add_all(roles)
            
            # Create sample users
            users = [
                User(
                    username='alice',
                    email='alice@example.com',
                    password='Password123!',  # Will be hashed
                    is_verified=True
                ),
                User(
                    username='bob',
                    email='bob@example.com',
                    password='Password123!',
                    is_verified=True
                ),
                User(
                    username='admin',
                    email='admin@example.com',
                    password='AdminPassword123!',
                    is_verified=True
                ),
            ]
            
            # Assign roles
            users[0].roles.append(roles[0])  # Alice is regular user
            users[1].roles.append(roles[1])  # Bob is premium user
            users[2].roles.append(roles[2])  # Admin user is admin
            users[2].roles.append(roles[3])  # Admin user is also superadmin
            
            db.session.add_all(users)
            db.session.commit()
            
            print("Database initialized with sample data!")
            print("\nSample users created:")
            print("1. alice (password: Password123!) - Regular user")
            print("2. bob (password: Password123!) - Premium user")
            print("3. admin (password: AdminPassword123!) - Admin user")


# ============================================================================
# 11. DEMONSTRATION ROUTE FOR EDUCATIONAL PURPOSES
# ============================================================================

@app.route('/auth-tutorial')
def auth_tutorial():
    """Interactive tutorial page demonstrating auth concepts."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Authentication & Authorization Tutorial</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
                color: #333;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .concept {
                background: #f8f9fa;
                border-left: 4px solid #007bff;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border-radius: 0 5px 5px 0;
            }
            .endpoint {
                background: #e9ecef;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 5px;
                font-family: monospace;
            }
            .method {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 0.5rem;
                font-size: 0.9rem;
            }
            .post { background: #28a745; color: white; }
            .get { background: #007bff; color: white; }
            .put { background: #ffc107; color: black; }
            .delete { background: #dc3545; color: white; }
            .danger {
                background: #fff5f5;
                border-left: 4px solid #dc3545;
                padding: 1rem;
                margin: 1rem 0;
            }
            .warning {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 1rem;
                margin: 1rem 0;
            }
            .success {
                background: #d4edda;
                border-left: 4px solid #28a745;
                padding: 1rem;
                margin: 1rem 0;
            }
            .demo-buttons {
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
                margin: 2rem 0;
            }
            .demo-btn {
                padding: 0.75rem 1.5rem;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .demo-btn:hover {
                background: #0056b3;
            }
            .test-area {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 1.5rem;
                border-radius: 5px;
                margin: 2rem 0;
            }
            code {
                background: #e9ecef;
                padding: 0.2rem 0.4rem;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            h2, h3 {
                color: #2c3e50;
                margin-top: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔐 Flask Authentication & Authorization Tutorial</h1>
            <p>Comprehensive demonstration of security best practices</p>
        </div>
        
        <div class="success">
            <strong>🚀 Ready to Test!</strong> The API is running with sample users. Use the demo buttons or curl commands below.
        </div>
        
        <h2>📚 Core Concepts Demonstrated</h2>
        
        <div class="concept">
            <h3>1. JWT-Based Authentication</h3>
            <p>JSON Web Tokens for stateless authentication with proper expiration and refresh.</p>
            <ul>
                <li>Access tokens (short-lived: 15 minutes)</li>
                <li>Refresh tokens (long-lived: 7 days)</li>
                <li>Token rotation and revocation</li>
                <li>Secure storage in HTTP-only cookies</li>
            </ul>
        </div>
        
        <div class="concept">
            <h3>2. Role-Based Access Control (RBAC)</h3>
            <p>Fine-grained permission system with roles and permissions.</p>
            <ul>
                <li>Predefined roles: user, premium, admin, superadmin</li>
                <li>Resource-based permissions: <code>user:read</code>, <code>admin:dashboard</code></li>
                <li>Scope-based permissions: <code>own</code>, <code>team</code>, <code>any</code></li>
                <li>Hierarchical role inheritance</li>
            </ul>
        </div>
        
        <div class="concept">
            <h3>3. Security Best Practices</h3>
            <ul>
                <li>Password hashing with bcrypt (12 rounds)</li>
                <li>Rate limiting on auth endpoints</li>
                <li>Account lockout after failed attempts</li>
                <li>Security headers (CSP, HSTS, X-Frame-Options)</li>
                <li>Comprehensive audit logging</li>
                <li>MFA support</li>
                <li>CSRF protection with SameSite cookies</li>
            </ul>
        </div>
        
        <div class="danger">
            <h3>⚠️ Common Auth Pitfalls & Solutions</h3>
            <ul>
                <li><strong>Pitfall:</strong> Storing plain text passwords<br>
                    <strong>Solution:</strong> Always use bcrypt with appropriate work factor</li>
                <li><strong>Pitfall:</strong> Long-lived access tokens<br>
                    <strong>Solution:</strong> 15-30 minute tokens with refresh mechanism</li>
                <li><strong>Pitfall:</strong> No rate limiting<br>
                    <strong>Solution:</strong> Strict limits on login/registration (5-10 requests/minute)</li>
                <li><strong>Pitfall:</strong> Exposing user existence<br>
                    <strong>Solution:</strong> Generic error messages for login failures</li>
                <li><strong>Pitfall:</strong> Not logging auth events<br>
                    <strong>Solution:</strong> Comprehensive audit logging of all attempts</li>
            </ul>
        </div>
        
        <h2>🔧 Available Endpoints</h2>
        
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/register</code> - Register new user
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/login</code> - Login and get tokens
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/refresh</code> - Refresh access token
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <code>/api/auth/logout</code> - Logout (revoke token)
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/auth/me</code> - Get current user info (protected)
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/public/info</code> - Public endpoint (no auth)
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/private/profile</code> - Private endpoint (login required)
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <code>/api/admin/dashboard</code> - Admin-only endpoint
        </div>
        
        <h2>🎯 How to Secure an Endpoint (and Why)</h2>
        
        <div class="test-area">
            <h3>Example: Securing a User Profile Endpoint</h3>
            
            <pre><code>from auth_decorators import login_required, permission_required

@app.route('/api/users/&lt;user_id&gt;/profile', methods=['GET'])
@login_required  # 1. Verify user is authenticated
@permission_required('profile:read')  # 2. Check specific permission
def get_user_profile(user_id):
    # 3. Additional resource-level permission check
    current_user = get_current_user()
    
    if current_user.id != int(user_id):
        # Check if user has permission to view others' profiles
        if not current_user.has_permission('profile:read:any'):
            return jsonify({'error': 'Not authorized'}), 403
    
    # 4. Business logic here
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'username': user.username,
        'email': user.email
    })</code></pre>
            
            <p><strong>Why each step is important:</strong></p>
            <ol>
                <li><code>@login_required</code>: Verifies identity (authentication)</li>
                <li><code>@permission_required</code>: Checks authorization (permissions)</li>
                <li>Resource-level check: Ensures user can only access authorized resources</li>
                <li>Business logic: Implements the actual functionality</li>
            </ol>
        </div>
        
        <h2>🚀 Quick Demo</h2>
        
        <div class="demo-buttons">
            <button class="demo-btn" onclick="testPublic()">Test Public Endpoint</button>
            <button class="demo-btn" onclick="testLogin()">Test Login</button>
            <button class="demo-btn" onclick="testProtected()">Test Protected Endpoint</button>
            <button class="demo-btn" onclick="testAdmin()">Test Admin Endpoint</button>
            <button class="demo-btn" onclick="showCurlExamples()">Show CURL Examples</button>
        </div>
        
        <div id="test-results" style="margin: 2rem 0; padding: 1rem; border: 1px solid #dee2e6; border-radius: 5px;">
            <h3>Test Results</h3>
            <pre id="results" style="background: #f8f9fa; padding: 1rem; border-radius: 3px; min-height: 100px;"></pre>
        </div>
        
        <div id="curl-examples" style="display: none;">
            <h3>📝 CURL Examples</h3>
            
            <div class="endpoint">
                <strong>1. Register a new user:</strong><br>
                <code>curl -X POST http://localhost:5000/api/auth/register \<br>
  -H "Content-Type: application/json" \<br>
  -d '{"username": "testuser", "email": "test@example.com", "password": "TestPass123!"}'</code>
            </div>
            
            <div class="endpoint">
                <strong>2. Login (get tokens):</strong><br>
                <code>curl -X POST http://localhost:5000/api/auth/login \<br>
  -H "Content-Type: application/json" \<br>
  -d '{"username": "alice", "password": "Password123!"}'</code>
            </div>
            
            <div class="endpoint">
                <strong>3. Access protected endpoint:</strong><br>
                <code>curl -X GET http://localhost:5000/api/private/profile \<br>
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"</code>
            </div>
            
            <div class="endpoint">
                <strong>4. Refresh token:</strong><br>
                <code>curl -X POST http://localhost:5000/api/auth/refresh \<br>
  -H "Content-Type: application/json" \<br>
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'</code>
            </div>
            
            <div class="endpoint">
                <strong>5. Access admin endpoint (will fail for regular users):</strong><br>
                <code>curl -X GET http://localhost:5000/api/admin/dashboard \<br>
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"</code>
            </div>
        </div>
        
        <script>
            const results = document.getElementById('results');
            
            async function testPublic() {
                results.innerHTML = 'Testing public endpoint...';
                try {
                    const response = await fetch('/api/public/info');
                    const data = await response.json();
                    results.innerHTML = JSON.stringify(data, null, 2);
                } catch (error) {
                    results.innerHTML = 'Error: ' + error.message;
                }
            }
            
            async function testLogin() {
                results.innerHTML = 'Testing login...';
                try {
                    const response = await fetch('/api/auth/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            username: 'alice',
                            password: 'Password123!'
                        })
                    });
                    const data = await response.json();
                    results.innerHTML = JSON.stringify(data, null, 2);
                    
                    // Store token for later use
                    if (data.tokens && data.tokens.access_token) {
                        localStorage.setItem('access_token', data.tokens.access_token);
                        localStorage.setItem('refresh_token', data.tokens.refresh_token);
                    }
                } catch (error) {
                    results.innerHTML = 'Error: ' + error.message;
                }
            }
            
            async function testProtected() {
                results.innerHTML = 'Testing protected endpoint...';
                const token = localStorage.getItem('access_token');
                
                if (!token) {
                    results.innerHTML = 'Please login first (use Test Login button)';
                    return;
                }
                
                try {
                    const response = await fetch('/api/private/profile', {
                        headers: {'Authorization': 'Bearer ' + token}
                    });
                    
                    if (response.status === 401) {
                        results.innerHTML = 'Token expired, please login again';
                        return;
                    }
                    
                    const data = await response.json();
                    results.innerHTML = JSON.stringify(data, null, 2);
                } catch (error) {
                    results.innerHTML = 'Error: ' + error.message;
                }
            }
            
            async function testAdmin() {
                results.innerHTML = 'Testing admin endpoint...';
                const token = localStorage.getItem('access_token') || 'invalid';
                
                try {
                    const response = await fetch('/api/admin/dashboard', {
                        headers: {'Authorization': 'Bearer ' + token}
                    });
                    const data = await response.json();
                    results.innerHTML = JSON.stringify(data, null, 2);
                } catch (error) {
                    results.innerHTML = 'Error: ' + error.message;
                }
            }
            
            function showCurlExamples() {
                document.getElementById('curl-examples').style.display = 'block';
                results.innerHTML = 'Scroll down to see CURL examples';
            }
        </script>
    </body>
    </html>
    """
    return html


# ============================================================================
# 12. APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    print("\n" + "="*70)
    print("🔐 FLASK AUTHENTICATION & AUTHORIZATION TUTORIAL")
    print("="*70)
    
    init_database()
    
    print("\n📚 Key Concepts Demonstrated:")
    print("1. JWT-Based Authentication (Access & Refresh Tokens)")
    print("2. Token Expiration & Refresh Mechanisms")
    print("3. Secure Cookies vs Headers Tradeoffs")
    print("4. Role-Based Access Control (RBAC)")
    print("5. Fine-Grained Permissions System")
    print("6. Endpoint Protection with Decorators")
    print("7. Common Auth Pitfalls & Solutions")
    print("8. Security Headers & Best Practices")
    print("9. Audit Logging & Monitoring")
    print("10. Rate Limiting & Account Lockout")
    
    print("\n👥 Sample Users Created:")
    print("   • alice:password123! (Regular user)")
    print("   • bob:password123! (Premium user)")
    print("   • admin:AdminPassword123! (Admin user)")
    
    print("\n🌐 Available Endpoints:")
    print("   • http://localhost:5000/auth-tutorial - Interactive tutorial")
    print("   • POST /api/auth/register - Register new user")
    print("   • POST /api/auth/login - Login and get tokens")
    print("   • GET  /api/auth/me - Get current user (protected)")
    print("   • GET  /api/public/info - Public endpoint")
    print("   • GET  /api/private/profile - Protected endpoint")
    print("   • GET  /api/admin/dashboard - Admin-only endpoint")
    
    print("\n🔧 Testing with curl:")
    print('   curl -X POST http://localhost:5000/api/auth/login \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"username": "alice", "password": "Password123!"}\'')
    
    print("\n⚠️  Security Notes:")
    print("   • Passwords are hashed with bcrypt (12 rounds)")
    print("   • Access tokens expire in 15 minutes")
    print("   • Refresh tokens expire in 7 days")
    print("   • Rate limiting is enabled on auth endpoints")
    print("   • Account locks after 5 failed attempts")
    print("="*70 + "\n")
    
    # Run the application
    app.run(debug=True, port=5000)