"""
COMPREHENSIVE FLASK SECURITY IMPLEMENTATION
This guide covers all major security aspects for Flask applications with practical examples.
"""

import os
import re
import secrets
import bcrypt
import bleach
import hashlib
import time
from datetime import datetime, timedelta
from functools import wraps
import jwt
from cryptography.fernet import Fernet
import redis
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse
import logging
from typing import Optional, Tuple, List, Dict, Any

# ============================================================================
# 1. FLASK APPLICATION SETUP WITH SECURITY CONFIGURATION
# ============================================================================

from flask import Flask, request, jsonify, session, g, make_response, abort
from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import validates
from sqlalchemy.exc import SQLAlchemyError
import validators

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
csp = {
    'default-src': "'self'",
    'script-src': "'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
    'style-src': "'self' 'unsafe-inline' https://cdnjs.cloudflare.com",
    'img-src': "'self' data: https:",
    'font-src': "'self' https://cdnjs.cloudflare.com",
    'object-src': "'none'",
    'base-uri': "'self'",
    'form-action': "'self'"
}

# ============================================================================
# 1.1 SECURITY-CONSCIOUS CONFIGURATION
# ============================================================================

def create_app():
    """Application factory with security-focused configuration"""
    
    app = Flask(__name__)
    
    # ============== CRITICAL SECURITY SETTINGS ==============
    
    # 1. SECRET KEY MANAGEMENT (Never hardcode in production!)
    # In production, use environment variables or secret management service
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # 2. SESSION SECURITY
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Session timeout
    app.config['SESSION_COOKIE_NAME'] = '__Secure-sessionid'  # Secure cookie prefix
    
    # 3. DATABASE SECURITY
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,  # Recycle connections every 5 minutes
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30
    }
    
    # 4. CSRF PROTECTION
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token validity
    app.config['WTF_CSRF_SSL_STRICT'] = True  # Ensure SSL for CSRF
    
    # 5. FILE UPLOAD SECURITY
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    app.config['UPLOAD_FOLDER'] = '/secure/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Initialize Talisman for security headers
    Talisman(
        app,
        content_security_policy=csp,
        force_https=True,
        force_https_permanent=True,
        frame_options='DENY',  # Prevent clickjacking
        frame_options_allow_from=None,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year HSTS
        strict_transport_security_include_subdomains=True,
        strict_transport_security_preload=True,
        referrer_policy='strict-origin-when-cross-origin',
        session_cookie_secure=True,
        session_cookie_httponly=True
    )
    
    # Configure CORS securely
    CORS(app, resources={
        r"/api/*": {
            "origins": os.environ.get('ALLOWED_ORIGINS', 'https://example.com').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-CSRF-Token"],
            "expose_headers": ["X-CSRF-Token"],
            "supports_credentials": True,
            "max_age": 600
        }
    })
    
    # ============== SECURITY MIDDLEWARE ==============
    
    @app.before_request
    def security_checks():
        """Perform security checks before each request"""
        
        # 1. Check for HTTPS (in production)
        if not request.is_secure and app.config['ENV'] == 'production':
            # This should be handled by Talisman, but extra check
            abort(400, description="HTTPS required")
        
        # 2. Validate Content-Type for POST/PUT requests
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('Content-Type', '')
            if not content_type.startswith('application/json'):
                abort(415, description="Content-Type must be application/json")
        
        # 3. Add security headers (complementing Talisman)
        g.request_start_time = time.time()
    
    @app.after_request
    def security_headers(response):
        """Add additional security headers after each request"""
        
        # Security Headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Performance headers with security considerations
        response.headers['X-Request-Time'] = str(time.time() - g.request_start_time)
        
        # Cache control for sensitive data
        if '/api/' in request.path:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        
        return response
    
    # ============== ERROR HANDLERS ==============
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle bad requests securely (don't expose details)"""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood'
        }), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors securely (log but don't expose details)"""
        app.logger.error(f'Server Error: {error}')
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        """Handle CSRF errors"""
        return jsonify({
            'error': 'CSRF Token Error',
            'message': 'CSRF token is missing or invalid'
        }), 400
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        """Handle rate limit errors"""
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded. Please try again later.',
            'retry_after': error.description
        }), 429
    
    return app

# Create the application
app = create_app()

# ============================================================================
# 2. CSRF PROTECTION - COMPREHENSIVE IMPLEMENTATION
# ============================================================================

class CSRFProtectionStrategies:
    """
    Comprehensive CSRF (Cross-Site Request Forgery) protection strategies
    """
    
    @staticmethod
    def demonstrate_csrf_attack():
        """
        Demonstration of CSRF vulnerability and protection
        
        VULNERABLE FORM (without CSRF protection):
        <form action="https://bank.com/transfer" method="POST">
            <input type="hidden" name="amount" value="1000">
            <input type="hidden" name="to_account" value="attacker">
            <input type="submit" value="Click for free money!">
        </form>
        
        This form on a malicious site would transfer money if user is logged into bank.com
        """
        
        print("\n" + "="*60)
        print("CSRF (CROSS-SITE REQUEST FORGERY) PROTECTION")
        print("="*60)
        
        print("""
        WHAT IS CSRF?
        -------------
        An attack that tricks the victim into submitting a malicious request.
        It inherits the identity and privileges of the victim to perform an undesired function.
        
        EXAMPLE VULNERABLE ENDPOINT (NO CSRF):
        --------------------------------------
        @app.route('/transfer', methods=['POST'])
        def transfer_money():
            # Without CSRF check, this is vulnerable!
            amount = request.form.get('amount')
            to_account = request.form.get('to_account')
            # Process transfer...
        
        HOW TO EXPLOIT:
        ---------------
        Attacker creates a form on their site:
        
        <form action="https://bank.com/transfer" method="POST">
          <input type="hidden" name="amount" value="1000">
          <input type="hidden" name="to_account" value="attacker">
          <input type="submit" value="Win Free Money!">
        </form>
        
        If user is logged into bank.com and clicks the button,
        the transfer happens without their knowledge!
        """)
    
    @staticmethod
    @app.route('/api/csrf/token', methods=['GET'])
    def get_csrf_token():
        """
        Endpoint to get CSRF token for AJAX requests
        Should be called before making POST/PUT/DELETE requests
        """
        token = generate_csrf()
        return jsonify({'csrf_token': token})
    
    @staticmethod
    @app.route('/api/csrf/protected-transfer', methods=['POST'])
    @csrf.exempt  # We'll handle CSRF manually for demonstration
    def protected_transfer():
        """
        Manually protected endpoint with CSRF validation
        Demonstrates both automatic and manual CSRF protection
        """
        
        # Get CSRF token from header or form
        csrf_token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
        
        if not csrf_token:
            return jsonify({
                'error': 'CSRF token required',
                'message': 'Include X-CSRF-Token header or csrf_token form field'
            }), 403
        
        # In real app, you would validate against the stored token
        # Flask-WTF does this automatically when CSRF is enabled
        
        # For demonstration, just check if token exists
        if csrf_token == 'valid_csrf_token_example':
            # Process the transfer
            amount = request.json.get('amount')
            account = request.json.get('to_account')
            
            return jsonify({
                'message': f'Transfer of ${amount} to {account} processed',
                'csrf_protected': True
            })
        else:
            return jsonify({
                'error': 'Invalid CSRF token',
                'message': 'CSRF validation failed'
            }), 403
    
    @staticmethod
    def csrf_best_practices():
        """
        CSRF protection best practices
        """
        
        practices = [
            ("1. ENABLE CSRF PROTECTION GLOBALLY", """
            # In Flask app configuration
            app.config['WTF_CSRF_ENABLED'] = True
            csrf = CSRFProtect(app)
            
            # This protects ALL non-GET requests automatically
            """),
            
            ("2. EXEMPT SPECIFIC ENDPOINTS CAREFULLY", """
            # Only exempt if absolutely necessary
            @app.route('/webhook', methods=['POST'])
            @csrf.exempt
            def webhook():
                # External services can't have CSRF tokens
                # But implement other authentication!
                pass
            
            # Always validate webhook signatures
            """),
            
            ("3. AJAX/SPA INTEGRATION", """
            // Frontend JavaScript
            // 1. Get CSRF token on page load
            fetch('/api/csrf/token')
                .then(res => res.json())
                .then(data => {
                    window.csrfToken = data.csrf_token;
                });
            
            // 2. Include in all mutating requests
            fetch('/api/transfer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': window.csrfToken
                },
                body: JSON.stringify(data)
            });
            """),
            
            ("4. DOUBLE SUBMIT COOKIE PATTERN", """
            # Alternative pattern for stateless APIs
            # 1. Set CSRF token in cookie (HttpOnly, Secure, SameSite)
            # 2. Require same token in request header
            # 3. Server compares cookie token with header token
            
            @app.before_request
            def validate_csrf():
                if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                    cookie_token = request.cookies.get('csrf_token')
                    header_token = request.headers.get('X-CSRF-Token')
                    
                    if not cookie_token or cookie_token != header_token:
                        abort(403, description='CSRF validation failed')
            """),
            
            ("5. SAME-SITE COOKIES", """
            # Modern browser protection
            app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # or 'Strict'
            
            # 'Strict': Cookie never sent on cross-site requests
            # 'Lax': Cookie sent on safe top-level navigation (recommended)
            # 'None': Cookie always sent (requires Secure flag)
            
            # This provides defense-in-depth with CSRF tokens
            """)
        ]
        
        print("\n" + "="*60)
        print("CSRF PROTECTION BEST PRACTICES")
        print("="*60)
        
        for title, content in practices:
            print(f"\n{title}")
            print(content)

# ============================================================================
# 3. XSS & INPUT SANITIZATION - COMPREHENSIVE DEFENSE
# ============================================================================

class XSSProtection:
    """
    Cross-Site Scripting (XSS) prevention and input sanitization
    """
    
    @staticmethod
    def demonstrate_xss_vulnerabilities():
        """
        Show common XSS vulnerabilities
        """
        
        print("\n" + "="*60)
        print("XSS (CROSS-SITE SCRIPTING) PROTECTION")
        print("="*60)
        
        print("""
        TYPES OF XSS ATTACKS:
        ---------------------
        
        1. REFLECTED XSS:
           - Malicious script in URL parameters
           - Server reflects it back in response
           Example: https://example.com/search?q=<script>alert('XSS')</script>
        
        2. STORED XSS:
           - Malicious script stored in database
           - Served to other users
           Example: Comment field: <script>stealCookies()</script>
        
        3. DOM-BASED XSS:
           - Client-side JavaScript vulnerability
           - Not server-side issue but still dangerous
        
        VULNERABLE FLASK CODE:
        ----------------------
        @app.route('/search')
        def search():
            query = request.args.get('q', '')
            # DANGER: Directly rendering user input!
            return f'<h1>Results for: {query}</h1>'
        
        If user visits: /search?q=<script>alert('XSS')</script>
        The script executes in victim's browser!
        """)
    
    @staticmethod
    def html_sanitization_demo():
        """
        Demonstrate HTML sanitization techniques
        """
        
        # User input that could contain malicious content
        malicious_input = """
        <script>alert('XSS Attack!')</script>
        <img src=x onerror="alert('XSS')">
        <a href="javascript:alert('XSS')">Click me</a>
        <div style="background: url(javascript:alert('XSS'))">
        <iframe src="http://evil.com"></iframe>
        """
        
        # 1. BLEACH - HTML sanitizer (Recommended)
        safe_html = bleach.clean(
            malicious_input,
            tags=['p', 'b', 'i', 'u', 'em', 'strong', 'a'],
            attributes={'a': ['href', 'title']},
            protocols=['http', 'https', 'mailto'],
            strip=True,  # Remove disallowed tags instead of escaping
            strip_comments=True
        )
        
        print(f"\nOriginal malicious input:")
        print(malicious_input)
        print(f"\nSanitized with Bleach:")
        print(safe_html)
        
        # 2. JINJA2 AUTOESCAPING (Enabled by default in Flask)
        print("""
        
        JINJA2 TEMPLATE AUTOESCAPING:
        -----------------------------
        Jinja2 auto-escapes variables by default:
        
        {{ user_input }}  # Auto-escaped (safe)
        {{ user_input|safe }}  # Explicitly marked safe (dangerous!)
        
        NEVER use |safe filter with untrusted input!
        """)
    
    @staticmethod
    @app.route('/api/sanitize', methods=['POST'])
    def sanitize_input_endpoint():
        """
        API endpoint demonstrating input sanitization
        """
        data = request.json
        
        if not data or 'input' not in data:
            return jsonify({'error': 'No input provided'}), 400
        
        user_input = data['input']
        
        # Different sanitization strategies based on context
        sanitized = {
            'original': user_input,
            'for_html': bleach.clean(user_input, strip=True),
            'for_url': XSSProtection.sanitize_url(user_input),
            'for_js': XSSProtection.sanitize_javascript(user_input),
            'for_sql': XSSProtection.sanitize_sql(user_input)
        }
        
        return jsonify(sanitized)
    
    @staticmethod
    def sanitize_url(url: str) -> str:
        """Sanitize URL input"""
        if not url:
            return ''
        
        # Parse URL
        parsed = urlparse(url)
        
        # Only allow http/https
        if parsed.scheme not in ('http', 'https', ''):
            return ''
        
        # Reconstruct safe URL
        safe_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}" if parsed.scheme else parsed.path
        
        # URL encode query parameters
        if parsed.query:
            from urllib.parse import quote
            safe_url += '?' + quote(parsed.query, safe='=&')
        
        return safe_url
    
    @staticmethod
    def sanitize_javascript(js: str) -> str:
        """Sanitize JavaScript input"""
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'eval\s*\(', r'Function\s*\(', r'setTimeout\s*\(', r'setInterval\s*\(',
            r'document\.', r'window\.', r'\.innerHTML', r'\.outerHTML',
            r'\.write\s*\(', r'\.writeln\s*\(', r'\.createElement\s*\('
        ]
        
        for pattern in dangerous_patterns:
            js = re.sub(pattern, '', js, flags=re.IGNORECASE)
        
        # Escape special characters
        js = (js.replace('\\', '\\\\')
                .replace('\'', '\\\'')
                .replace('\"', '\\"')
                .replace('\n', '\\n')
                .replace('\r', '\\r'))
        
        return js
    
    @staticmethod
    def sanitize_sql(sql_input: str) -> str:
        """Basic SQL input sanitization (Use parameterized queries instead!)"""
        # Remove SQL comment patterns
        sql_input = re.sub(r'--.*$', '', sql_input, flags=re.MULTILINE)
        sql_input = re.sub(r'/\*.*?\*/', '', sql_input, flags=re.DOTALL)
        
        # Remove common SQL injection patterns
        sql_input = re.sub(r'\b(OR|AND)\b\s*[\'"]?\s*\d+\s*=\s*\d+', '', sql_input, flags=re.IGNORECASE)
        sql_input = re.sub(r'\bUNION\b.*?\bSELECT\b', '', sql_input, flags=re.IGNORECASE | re.DOTALL)
        
        return sql_input
    
    @staticmethod
    def xss_prevention_guide():
        """
        Comprehensive XSS prevention guide
        """
        
        print("\n" + "="*60)
        print("XSS PREVENTION STRATEGIES")
        print("="*60)
        
        strategies = [
            ("1. OUTPUT ENCODING (Context-Sensitive)", """
            Always encode based on output context:
            
            HTML Context: Use HTML entity encoding
                & → &amp;
                < → &lt;
                > → &gt;
                " → &quot;
                ' → &#x27;
            
            JavaScript Context: Use Unicode escaping
                < → \\u003c
            
            URL Context: Use URL encoding
                < → %3C
            
            CSS Context: Use CSS escaping
                < → \\3c 
            """),
            
            ("2. CONTENT SECURITY POLICY (CSP)", """
            # In Flask-Talisman or response headers:
            
            Content-Security-Policy: 
                default-src 'self';
                script-src 'self' https://trusted.cdn.com;
                style-src 'self' 'unsafe-inline';
                img-src 'self' data: https:;
                font-src 'self';
                object-src 'none';
                base-uri 'self';
                form-action 'self';
            
            CSP prevents XSS by restricting resource loading
            """),
            
            ("3. INPUT VALIDATION", """
            Validate on both client and server:
            
            def validate_email(email):
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$', email):
                    raise ValueError('Invalid email format')
                return email.lower().strip()
            
            Use libraries:
                - email-validator for emails
                - validators for URLs, IPs
                - marshmallow for complex validation
            """),
            
            ("4. SAFE TEMPLATING PRACTICES", """
            # Jinja2 (Flask's template engine) auto-escapes by default
            
            SAFE:
                {{ user_input }}  # Auto-escaped
                {{ user_input|e }}  # Explicit escaping
            
            DANGEROUS:
                {{ user_input|safe }}  # Disables auto-escaping!
                {{ user_input|safe }}  # NEVER with untrusted input!
            
            Use markupsafe for manual escaping:
                from markupsafe import escape
                safe_output = escape(user_input)
            """),
            
            ("5. HTTPONLY AND SECURE COOKIES", """
            # Prevent JavaScript access to cookies
            
            app.config.update(
                SESSION_COOKIE_HTTPONLY=True,  # No JS access
                SESSION_COOKIE_SECURE=True,    # HTTPS only
                SESSION_COOKIE_SAMESITE='Lax'  # CSRF protection
            )
            
            This prevents cookie theft via XSS
            """)
        ]
        
        for title, content in strategies:
            print(f"\n{title}")
            print(content)

# ============================================================================
# 4. SQL INJECTION PREVENTION - COMPREHENSIVE DEFENSE
# ============================================================================

class SQLInjectionProtection:
    """
    SQL Injection prevention strategies
    """
    
    @staticmethod
    def demonstrate_sql_injection():
        """
        Show SQL injection vulnerabilities and prevention
        """
        
        print("\n" + "="*60)
        print("SQL INJECTION PREVENTION")
        print("="*60)
        
        print("""
        WHAT IS SQL INJECTION?
        -----------------------
        An attack where malicious SQL is inserted into queries.
        
        VULNERABLE CODE:
        ----------------
        user_id = request.args.get('id')
        query = f"SELECT * FROM users WHERE id = {user_id}"
        
        If attacker provides: 1 OR 1=1 --
        Resulting query: SELECT * FROM users WHERE id = 1 OR 1=1 --
        This returns ALL users!
        
        MORE DANGEROUS:
        id = "1; DROP TABLE users; --"
        Query: SELECT * FROM users WHERE id = 1; DROP TABLE users; --
        This DROPS the users table!
        """)
    
    @staticmethod
    def safe_database_models():
        """
        SQLAlchemy models with validation
        """
        
        class User(db.Model):
            __tablename__ = 'users'
            
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            
            @validates('username')
            def validate_username(self, key, username):
                """Validate username input"""
                if not username or len(username) < 3:
                    raise ValueError('Username must be at least 3 characters')
                
                # Only allow alphanumeric and underscores
                if not re.match(r'^[a-zA-Z0-9_]+$', username):
                    raise ValueError('Username can only contain letters, numbers, and underscores')
                
                return username
            
            @validates('email')
            def validate_email(self, key, email):
                """Validate email input"""
                if not email:
                    raise ValueError('Email is required')
                
                # Simple email validation
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    raise ValueError('Invalid email format')
                
                return email.lower()
    
    @staticmethod
    @app.route('/api/users/<user_id>', methods=['GET'])
    def get_user_safely(user_id):
        """
        Safely retrieve user using SQLAlchemy (no SQL injection)
        """
        
        # SAFE METHOD 1: Use SQLAlchemy ORM
        try:
            # Parameterized query via ORM
            user = db.session.query(User).filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email
            })
            
        except SQLAlchemyError as e:
            app.logger.error(f'Database error: {e}')
            return jsonify({'error': 'Database error occurred'}), 500
    
    @staticmethod
    @app.route('/api/users/search', methods=['GET'])
    def search_users_safely():
        """
        Safely search users with dynamic filters
        """
        search_term = request.args.get('q', '')
        
        # SAFE METHOD 2: Use SQLAlchemy with bind parameters
        try:
            # Never do: f"WHERE username LIKE '%{search_term}%'"
            # Always use parameterized queries
            
            query = text("""
                SELECT id, username, email 
                FROM users 
                WHERE username LIKE :pattern 
                AND is_active = :active
                LIMIT :limit
            """)
            
            result = db.session.execute(query, {
                'pattern': f'%{search_term}%',
                'active': True,
                'limit': 50
            })
            
            users = [dict(row) for row in result]
            return jsonify({'users': users})
            
        except SQLAlchemyError as e:
            app.logger.error(f'Database error: {e}')
            return jsonify({'error': 'Database error occurred'}), 500
    
    @staticmethod
    def raw_sql_with_psycopg2():
        """
        Example of safe raw SQL with psycopg2
        """
        
        print("\n" + "="*60)
        print("SAFE RAW SQL WITH PSYCOPG2")
        print("="*60)
        
        safe_code = """
        # UNSAFE - String concatenation (VULNERABLE)
        user_id = request.args.get('id')
        query = f"SELECT * FROM users WHERE id = {user_id}"
        
        # SAFE - Parameterized queries
        user_id = request.args.get('id')
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))  # Parameter tuple
        
        # SAFE - Named parameters
        query = "SELECT * FROM users WHERE username = %(username)s AND status = %(status)s"
        cursor.execute(query, {'username': username, 'status': 'active'})
        
        # SAFE - SQL composition with psycopg2.sql
        from psycopg2 import sql
        
        table_name = 'users'
        column = 'id'
        value = user_id
        
        query = sql.SQL("SELECT * FROM {} WHERE {} = %s").format(
            sql.Identifier(table_name),
            sql.Identifier(column)
        )
        cursor.execute(query, (value,))
        """
        
        print(safe_code)
    
    @staticmethod
    def sql_injection_prevention_rules():
        """
        Rules for preventing SQL injection
        """
        
        rules = [
            ("1. ALWAYS USE PARAMETERIZED QUERIES", """
            NEVER concatenate user input into SQL strings.
            
            # BAD - Vulnerable to SQL injection
            query = f"SELECT * FROM users WHERE username = '{username}'"
            
            # GOOD - Parameterized query
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            
            Database drivers handle escaping automatically.
            """),
            
            ("2. USE ORM OR QUERY BUILDER", """
            Higher-level abstraction = safer code.
            
            SQLAlchemy, Django ORM, Peewee all use
            parameterized queries internally.
            
            user = User.query.filter_by(username=username).first()
            # SQLAlchemy automatically parameterizes
            """),
            
            ("3. VALIDATE AND SANITIZE INPUT", """
            Input validation provides defense in depth:
            
            def validate_user_id(user_id):
                # Must be numeric
                if not user_id.isdigit():
                    raise ValueError('User ID must be numeric')
                
                # Within valid range
                if int(user_id) < 1 or int(user_id) > 1000000:
                    raise ValueError('Invalid user ID')
                
                return int(user_id)
            """),
            
            ("4. USE LEAST PRIVILEGE DATABASE ACCOUNTS", """
            Application should connect with minimal privileges:
            
            CREATE USER app_user WITH PASSWORD 'secure_password';
            GRANT SELECT, INSERT, UPDATE ON users TO app_user;
            -- NO DROP, NO ALTER, NO CREATE
            
            If SQL injection occurs, damage is limited.
            """),
            
            ("5. ESCAPE WILDCARDS IN LIKE CLAUSES", """
            LIKE clauses need special handling:
            
            search = request.args.get('search', '')
            
            # Escape SQL wildcards
            safe_search = search.replace('%', '\\\\%').replace('_', '\\\\_')
            
            query = "SELECT * FROM products WHERE name LIKE %s"
            cursor.execute(query, (f'%{safe_search}%',))
            
            Without escaping, % and _ have special meaning.
            """)
        ]
        
        print("\n" + "="*60)
        print("SQL INJECTION PREVENTION RULES")
        print("="*60)
        
        for title, content in rules:
            print(f"\n{title}")
            print(content)

# ============================================================================
# 5. SECURE HEADERS IMPLEMENTATION
# ============================================================================

class SecureHeadersImplementation:
    """
    Implementation of secure HTTP headers
    """
    
    @staticmethod
    def demonstrate_secure_headers():
        """
        Show important security headers
        """
        
        print("\n" + "="*60)
        print("SECURE HTTP HEADERS")
        print("="*60)
        
        headers = {
            'Content-Security-Policy': {
                'purpose': 'Prevents XSS and other code injection attacks',
                'example': "default-src 'self'; script-src 'self' https://trusted.cdn.com;",
                'flask': "Talisman(app, content_security_policy={...})"
            },
            'X-Content-Type-Options': {
                'purpose': 'Prevents MIME type sniffing',
                'example': 'nosniff',
                'flask': "response.headers['X-Content-Type-Options'] = 'nosniff'"
            },
            'X-Frame-Options': {
                'purpose': 'Prevents clickjacking',
                'example': 'DENY',
                'flask': "response.headers['X-Frame-Options'] = 'DENY'"
            },
            'X-XSS-Protection': {
                'purpose': 'Enables XSS filtering in older browsers',
                'example': '1; mode=block',
                'flask': "response.headers['X-XSS-Protection'] = '1; mode=block'"
            },
            'Referrer-Policy': {
                'purpose': 'Controls referrer information sent',
                'example': 'strict-origin-when-cross-origin',
                'flask': "response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'"
            },
            'Strict-Transport-Security': {
                'purpose': 'Enforces HTTPS connections',
                'example': 'max-age=31536000; includeSubDomains; preload',
                'flask': "Talisman(app, strict_transport_security=True, strict_transport_security_max_age=31536000)"
            }
        }
        
        for header, info in headers.items():
            print(f"\n{header}:")
            print(f"  Purpose: {info['purpose']}")
            print(f"  Example: {info['example']}")
            print(f"  Flask: {info['flask']}")
    
    @staticmethod
    def custom_header_middleware():
        """
        Custom middleware for security headers
        """
        
        @app.after_request
        def add_security_headers(response):
            """Add security headers to all responses"""
            
            # Security Headers
            headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Referrer-Policy': 'strict-origin-when-cross-origin',
                
                # Prevent browsers from storing sensitive data
                'Cache-Control': 'no-store, no-cache, must-revalidate, private',
                'Pragma': 'no-cache',
                'Expires': '0',
                
                # Feature Policy (deprecated but still useful)
                'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
                
                # Custom headers for monitoring
                'X-Request-ID': secrets.token_hex(16),
                'X-Powered-By': 'Flask Security Framework'  # Can obfuscate
            }
            
            for header, value in headers.items():
                response.headers[header] = value
            
            # Remove potentially dangerous headers
            dangerous_headers = ['Server', 'X-Powered-By']  # Keep X-Powered-By if set above
            for header in dangerous_headers:
                if header in response.headers and header != 'X-Powered-By':
                    response.headers.pop(header)
            
            return response
    
    @staticmethod
    def content_security_policy_examples():
        """
        CSP configuration examples for different scenarios
        """
        
        csp_configs = {
            'strict': {
                'description': 'Maximum security - very restrictive',
                'policy': {
                    'default-src': "'self'",
                    'script-src': "'self'",
                    'style-src': "'self'",
                    'img-src': "'self' data:",
                    'font-src': "'self'",
                    'connect-src': "'self'",
                    'object-src': "'none'",
                    'base-uri': "'self'",
                    'form-action': "'self'",
                    'frame-ancestors': "'none'",
                    'block-all-mixed-content': True
                }
            },
            'modern_web_app': {
                'description': 'For modern web apps with CDNs',
                'policy': {
                    'default-src': "'self'",
                    'script-src': "'self' https://cdnjs.cloudflare.com 'unsafe-inline'",
                    'style-src': "'self' https://cdnjs.cloudflare.com 'unsafe-inline'",
                    'img-src': "'self' data: https:",
                    'font-src': "'self' https://cdnjs.cloudflare.com",
                    'connect-src': "'self' https://api.example.com",
                    'object-src': "'none'",
                    'base-uri': "'self'",
                    'form-action': "'self'",
                    'frame-ancestors': "'self'"
                }
            },
            'report_only': {
                'description': 'Monitoring mode - doesn\'t block, only reports',
                'policy': {
                    'default-src': "'self'",
                    'script-src': "'self'",
                    'report-uri': '/csp-violation-report'
                },
                'report_only': True
            }
        }
        
        print("\n" + "="*60)
        print("CONTENT SECURITY POLICY CONFIGURATIONS")
        print("="*60)
        
        for config_name, config in csp_configs.items():
            print(f"\n{config_name.upper()} - {config['description']}:")
            for directive, value in config['policy'].items():
                print(f"  {directive}: {value}")

# ============================================================================
# 6. RATE LIMITING IMPLEMENTATION
# ============================================================================

class RateLimitingStrategies:
    """
    Rate limiting to prevent abuse and DoS attacks
    """
    
    @staticmethod
    def demonstrate_rate_limiting():
        """
        Show rate limiting implementation
        """
        
        print("\n" + "="*60)
        print("RATE LIMITING STRATEGIES")
        print("="*60)
        
        print("""
        WHY RATE LIMITING?
        ------------------
        1. Prevent brute force attacks
        2. Prevent DoS/DDoS attacks
        3. Prevent API abuse
        4. Fair resource allocation
        5. Cost control (for paid APIs)
        
        TYPES OF RATE LIMITS:
        ---------------------
        - IP-based: Limit by client IP
        - User-based: Limit by authenticated user
        - API Key-based: Limit by API key
        - Endpoint-based: Different limits per endpoint
        
        STORAGE BACKENDS:
        -----------------
        - In-memory: Simple but doesn't work with multiple workers
        - Redis: Distributed, persistent, recommended for production
        - Database: Persistent but slower
        """)
    
    @staticmethod
    @app.route('/api/public/unlimited')
    def unlimited_endpoint():
        """Unlimited endpoint (use carefully)"""
        return jsonify({'message': 'This endpoint has no rate limits'})
    
    @staticmethod
    @app.route('/api/public/limited')
    @limiter.limit("10 per minute")
    def limited_endpoint():
        """Endpoint with rate limiting"""
        return jsonify({
            'message': 'This endpoint is rate limited',
            'remaining': request.rate_limiting.remaining if hasattr(request, 'rate_limiting') else 'unknown'
        })
    
    @staticmethod
    @app.route('/api/auth/login', methods=['POST'])
    @limiter.limit("5 per minute", key_func=lambda: request.json.get('username') if request.json else get_remote_address())
    def login_with_username_limit():
        """
        Login endpoint with username-based rate limiting
        Limits login attempts per username
        """
        username = request.json.get('username')
        password = request.json.get('password')
        
        # Authentication logic here...
        
        return jsonify({'message': 'Login endpoint - rate limited by username'})
    
    @staticmethod
    def custom_rate_limit_strategies():
        """
        Custom rate limiting strategies
        """
        
        # Strategy 1: Different limits for different user tiers
        def get_user_tier():
            """Determine user tier for rate limiting"""
            if hasattr(g, 'user'):
                if g.user.is_premium:
                    return 'premium'
                elif g.user.is_authenticated:
                    return 'authenticated'
            return 'anonymous'
        
        # Apply different limits based on tier
        tier_limits = {
            'premium': "1000 per hour",
            'authenticated': "100 per hour",
            'anonymous': "10 per hour"
        }
        
        @app.route('/api/tiered-endpoint')
        @limiter.limit(lambda: tier_limits.get(get_user_tier(), "10 per hour"))
        def tiered_endpoint():
            return jsonify({'tier': get_user_tier()})
        
        # Strategy 2: Dynamic limits based on system load
        def dynamic_limit():
            """Dynamic rate limit based on system load"""
            load = os.getloadavg()[0]  # 1-minute load average
            
            if load > 5.0:
                return "10 per minute"  # Strict under high load
            elif load > 2.0:
                return "50 per minute"  # Moderate
            else:
                return "200 per minute"  # Normal
        
        # Strategy 3: Burst vs sustained limits
        @app.route('/api/burst-sensitive')
        @limiter.limit("100 per hour; 10 per minute")
        def burst_sensitive_endpoint():
            """
            100 requests per hour total
            But no more than 10 requests in any minute (burst protection)
            """
            return jsonify({'message': 'Burst protected endpoint'})
    
    @staticmethod
    def rate_limit_storage_backends():
        """
        Different storage backends for rate limiting
        """
        
        print("\n" + "="*60)
        print("RATE LIMIT STORAGE BACKENDS")
        print("="*60)
        
        backends = [
            ("MEMORY (SimpleLimiter)", """
            # Simple in-memory storage
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_address
            
            limiter = Limiter(
                key_func=get_remote_address,
                default_limits=["200 per day", "50 per hour"],
                storage_uri="memory://"  # Default
            )
            
            Pros: Simple, no dependencies
            Cons: Doesn't work with multiple workers
            Use: Development, single-process apps
            """),
            
            ("REDIS (Production)", """
            # Redis storage for distributed systems
            limiter = Limiter(
                key_func=get_remote_address,
                default_limits=["200 per day", "50 per hour"],
                storage_uri="redis://localhost:6379/0",
                storage_options={
                    'socket_connect_timeout': 5,
                    'retry_on_timeout': True
                },
                strategy="fixed-window"  # or "moving-window"
            )
            
            Pros: Distributed, persistent, fast
            Cons: Requires Redis
            Use: Production, multiple workers
            """),
            
            ("MEMCACHED", """
            # Memcached storage
            limiter = Limiter(
                storage_uri="memcached://localhost:11211",
                strategy="fixed-window"
            )
            
            Pros: Fast, distributed
            Cons: Memory only, no persistence
            """),
            
            ("DATABASE (SQL)", """
            # Database storage
            limiter = Limiter(
                storage_uri="postgresql://user:pass@localhost/dbname",
                storage_options={
                    'table_name': 'rate_limits',
                    'sync_window': 10
                }
            )
            
            Pros: Persistent, no extra services
            Cons: Slower, database load
            """)
        ]
        
        for backend_name, backend_info in backends:
            print(f"\n{backend_name}:")
            print(backend_info)
    
    @staticmethod
    def advanced_rate_limiting_patterns():
        """
        Advanced rate limiting patterns
        """
        
        patterns = [
            ("SLIDING WINDOW", """
            More accurate than fixed window
            
            Fixed window: 100/hour (resets at hour mark)
            Sliding window: 100/hour (looks back 1 hour from now)
            
            Implementation with Redis:
            
            import redis
            import time
            
            def sliding_window_rate_limit(key, limit, window):
                conn = redis.Redis()
                now = time.time()
                
                # Remove old timestamps
                conn.zremrangebyscore(key, 0, now - window)
                
                # Count requests in window
                current = conn.zcard(key)
                
                if current < limit:
                    # Add current request
                    conn.zadd(key, {now: now})
                    conn.expire(key, window)
                    return True  # Allowed
                
                return False  # Denied
            """),
            
            ("TOKEN BUCKET", """
            Smooths out bursts
            
            Bucket holds tokens (e.g., 100 tokens)
            Each request consumes 1 token
            Tokens refill at steady rate (e.g., 10 tokens/minute)
            
            Pros: Allows bursts but controls average rate
            Cons: More complex implementation
            """),
            
            ("LEAKY BUCKET", """
            Similar to token bucket but different approach
            
            Requests pour into bucket
            Bucket leaks at constant rate
            If bucket overflows, requests are denied
            
            Pros: Smooth output rate
            Cons: Can delay requests
            """),
            
            ("ADAPTIVE RATE LIMITING", """
            Adjust limits based on behavior
            
            Example:
            - Normal users: 100/hour
            - Suspicious IPs: 10/hour
            - Banned IPs: 0/hour
            
            Implement with machine learning or rules:
            
            def adaptive_limit(ip):
                if ip in suspicious_ips:
                    return "10 per hour"
                elif ip in malicious_ips:
                    return "1 per hour"
                else:
                    return "100 per hour"
            """)
        ]
        
        print("\n" + "="*60)
        print("ADVANCED RATE LIMITING PATTERNS")
        print("="*60)
        
        for pattern_name, pattern_info in patterns:
            print(f"\n{pattern_name}:")
            print(pattern_info)

# ============================================================================
# 7. SECRETS MANAGEMENT - COMPREHENSIVE GUIDE
# ============================================================================

class SecretsManagement:
    """
    Secure secrets management for Flask applications
    """
    
    @staticmethod
    def demonstrate_secrets_management():
        """
        Show secrets management strategies
        """
        
        print("\n" + "="*60)
        print("SECRETS MANAGEMENT STRATEGIES")
        print("="*60)
        
        print("""
        WHAT ARE SECRETS?
        -----------------
        Sensitive configuration data:
        - Database passwords
        - API keys
        - Encryption keys
        - JWT secrets
        - OAuth client secrets
        
        NEVER DO THIS:
        ---------------
        # Hardcoded secrets (BAD!)
        app.config['SECRET_KEY'] = 'my-super-secret-key-123'
        app.config['DATABASE_PASSWORD'] = 'password123'
        
        These get committed to version control!
        """)
    
    @staticmethod
    def environment_variables():
        """
        Using environment variables (basic approach)
        """
        
        print("\n" + "="*60)
        print("ENVIRONMENT VARIABLES")
        print("="*60)
        
        env_vars = """
        # .env file (DO NOT COMMIT TO VERSION CONTROL!)
        SECRET_KEY=your-super-secure-secret-key-here
        DATABASE_URL=postgresql://user:password@localhost/dbname
        REDIS_URL=redis://localhost:6379/0
        API_KEY=sk_test_123456789
        DEBUG=False
        
        # Load in Flask
        from dotenv import load_dotenv
        load_dotenv()  # Load from .env file
        
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
        
        # Production (no .env file)
        # Set environment variables on server:
        # export SECRET_KEY="your-key"
        # Or use systemd, Docker, etc.
        
        SECURITY NOTES:
        - .env files are for development only
        - In production, use system environment variables
        - Never commit .env files to version control
        - Add .env to .gitignore
        """
        
        print(env_vars)
    
    @staticmethod
    def secret_rotation_strategy():
        """
        Secret rotation implementation
        """
        
        class RotatingSecretManager:
            """Manages rotating secrets without downtime"""
            
            def __init__(self):
                self.current_secret = os.environ.get('CURRENT_SECRET')
                self.previous_secret = os.environ.get('PREVIOUS_SECRET')
                self.next_secret = os.environ.get('NEXT_SECRET')
            
            def validate_token(self, token):
                """Validate token with current or previous secret"""
                try:
                    # Try with current secret
                    payload = jwt.decode(token, self.current_secret, algorithms=["HS256"])
                    return payload, 'current'
                except jwt.InvalidTokenError:
                    try:
                        # Try with previous secret (during rotation)
                        payload = jwt.decode(token, self.previous_secret, algorithms=["HS256"])
                        return payload, 'previous'
                    except jwt.InvalidTokenError:
                        return None, 'invalid'
            
            def rotate_secrets(self):
                """Rotate secrets (run periodically)"""
                # In production, this would fetch from secrets manager
                new_secret = secrets.token_hex(32)
                
                # Update environment (in memory only)
                self.previous_secret = self.current_secret
                self.current_secret = self.next_secret
                self.next_secret = new_secret
                
                # In real app, you'd update the secrets manager
                # and gradually update application instances
        
        print("\n" + "="*60)
        print("SECRET ROTATION STRATEGY")
        print("="*60)
        print("""
        WHY ROTATE SECRETS?
        -------------------
        1. Limit exposure if secret is compromised
        2. Compliance requirements (PCI DSS, HIPAA)
        3. Security best practice
        
        ROTATION STRATEGY:
        ------------------
        1. Have multiple valid secrets:
           - Current (active)
           - Previous (accepting during rotation)
           - Next (prepared for next rotation)
        
        2. Gradual rotation:
           - Update some instances first
           - Validate with both old and new
           - Update remaining instances
        
        3. Automated rotation:
           - Schedule regular rotation
           - Use secrets manager with auto-rotation
        """)
    
    @staticmethod
    def production_secrets_managers():
        """
        Production secrets management solutions
        """
        
        print("\n" + "="*60)
        print("PRODUCTION SECRETS MANAGERS")
        print("="*60)
        
        managers = [
            ("HASHICORP VAULT", """
            # Flask-Vault integration example
            from hvac import Client
            
            vault_client = Client(
                url=os.environ.get('VAULT_ADDR'),
                token=os.environ.get('VAULT_TOKEN')
            )
            
            # Read secret
            secret = vault_client.secrets.kv.v2.read_secret_version(
                path='database/creds'
            )
            
            db_password = secret['data']['data']['password']
            
            Features:
            - Dynamic secrets
            - Encryption as a service
            - Access policies
            - Audit logging
            """),
            
            ("AWS SECRETS MANAGER", """
            # boto3 integration
            import boto3
            from botocore.exceptions import ClientError
            
            def get_secret():
                secret_name = "prod/database"
                region_name = "us-east-1"
                
                session = boto3.session.Session()
                client = session.client(
                    service_name='secretsmanager',
                    region_name=region_name
                )
                
                try:
                    response = client.get_secret_value(
                        SecretId=secret_name
                    )
                except ClientError as e:
                    raise e
                
                return response['SecretString']
            
            Features:
            - Automatic rotation
            - Integration with RDS
            - Fine-grained permissions
            """),
            
            ("AZURE KEY VAULT", """
            # azure-keyvault-secrets integration
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient
            
            credential = DefaultAzureCredential()
            client = SecretClient(
                vault_url="https://my-vault.vault.azure.net/",
                credential=credential
            )
            
            secret = client.get_secret("database-password")
            db_password = secret.value
            
            Features:
            - Hardware security modules
            - Access policies
            - Monitoring and auditing
            """),
            
            ("GOOGLE CLOUD SECRET MANAGER", """
            # google-cloud-secret-manager integration
            from google.cloud import secretmanager
            
            client = secretmanager.SecretManagerServiceClient()
            
            secret_name = f"projects/my-project/secrets/db-password/versions/latest"
            response = client.access_secret_version(request={"name": secret_name})
            db_password = response.payload.data.decode("UTF-8")
            
            Features:
            - Automatic replication
            - IAM integration
            - Audit logging
            """)
        ]
        
        for manager_name, manager_info in managers:
            print(f"\n{manager_name}:")
            print(manager_info)
    
    @staticmethod
    def encryption_at_rest():
        """
        Encrypting sensitive data at rest
        """
        
        class DataEncryptor:
            """Encrypt sensitive data before storage"""
            
            def __init__(self):
                # In production, get from secrets manager
                key = os.environ.get('ENCRYPTION_KEY')
                if not key:
                    key = Fernet.generate_key()
                self.cipher = Fernet(key)
            
            def encrypt(self, data: str) -> str:
                """Encrypt sensitive data"""
                encrypted = self.cipher.encrypt(data.encode())
                return encrypted.decode()
            
            def decrypt(self, encrypted_data: str) -> str:
                """Decrypt sensitive data"""
                decrypted = self.cipher.decrypt(encrypted_data.encode())
                return decrypted.decode()
        
        print("\n" + "="*60)
        print("ENCRYPTION AT REST")
        print("="*60)
        print("""
        WHAT TO ENCRYPT:
        ----------------
        - Credit card numbers
        - Social security numbers
        - Medical records
        - API keys (if stored in DB)
        - Personal identification data
        
        IMPLEMENTATION:
        ---------------
        1. Use Fernet (symmetric encryption)
        2. Store encryption key in secrets manager
        3. Encrypt before storing in database
        4. Decrypt only when needed
        
        EXAMPLE DATABASE FIELD:
        -----------------------
        class User(db.Model):
            # Store encrypted
            ssn_encrypted = db.Column(db.String(255))
            
            @property
            def ssn(self):
                if self.ssn_encrypted:
                    return encryptor.decrypt(self.ssn_encrypted)
                return None
            
            @ssn.setter
            def ssn(self, value):
                if value:
                    self.ssn_encrypted = encryptor.encrypt(value)
                else:
                    self.ssn_encrypted = None
        
        SECURITY NOTES:
        ---------------
        - Never store encryption keys with data
        - Use key rotation
        - Back up encryption keys securely
        - Consider hardware security modules (HSM) for highest security
        """)

# ============================================================================
# 8. HTTPS ENFORCEMENT - COMPREHENSIVE GUIDE
# ============================================================================

class HTTPSEnforcement:
    """
    HTTPS/SSL/TLS enforcement strategies
    """
    
    @staticmethod
    def demonstrate_https_importance():
        """
        Show why HTTPS is critical
        """
        
        print("\n" + "="*60)
        print("HTTPS ENFORCEMENT")
        print("="*60)
        
        print("""
        WHY HTTPS IS NON-NEGOTIABLE:
        ----------------------------
        1. DATA CONFIDENTIALITY
           - Encrypts data in transit
           - Prevents eavesdropping on public WiFi
        
        2. DATA INTEGRITY
           - Prevents man-in-the-middle attacks
           - Ensures data isn't modified in transit
        
        3. AUTHENTICATION
           - Verifies server identity
           - Prevents phishing attacks
        
        4. SEO BENEFITS
           - Google ranks HTTPS sites higher
           - Required for modern browser features
        
        5. USER TRUST
           - Shows security padlock in browser
           - Required for PWAs, geolocation, etc.
        
        WHAT HAPPENS WITHOUT HTTPS:
        ---------------------------
        - Passwords sent in plain text
        - Session cookies can be stolen
        - Users vulnerable to MITM attacks
        - Search engines flag as "Not Secure"
        """)
    
    @staticmethod
    def flask_https_configuration():
        """
        Configure Flask for HTTPS
        """
        
        print("\n" + "="*60)
        print("FLASK HTTPS CONFIGURATION")
        print("="*60)
        
        config = """
        # DEVELOPMENT (with self-signed certificate)
        if __name__ == '__main__':
            app.run(
                ssl_context=('cert.pem', 'key.pem'),
                debug=True
            )
        
        # PRODUCTION (behind reverse proxy)
        # Flask should NOT handle SSL directly in production
        # Use Nginx/Apache as reverse proxy
        
        Nginx configuration:
        -------------------
        server {
            listen 443 ssl http2;
            server_name example.com;
            
            ssl_certificate /etc/ssl/certs/example.com.crt;
            ssl_certificate_key /etc/ssl/private/example.com.key;
            
            # Modern SSL configuration
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
            ssl_prefer_server_ciphers off;
            
            location / {
                proxy_pass http://localhost:5000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        
        # Redirect HTTP to HTTPS
        server {
            listen 80;
            server_name example.com;
            return 301 https://$server_name$request_uri;
        }
        """
        
        print(config)
    
    @staticmethod
    @app.before_request
    def https_redirect():
        """
        Redirect HTTP to HTTPS (when behind proxy)
        Only use if your Flask app receives X-Forwarded-Proto header
        """
        # In production, this should be handled by reverse proxy
        # This is a backup mechanism
        
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
    
    @staticmethod
    def hsts_implementation():
        """
        HTTP Strict Transport Security implementation
        """
        
        print("\n" + "="*60)
        print("HSTS (HTTP STRICT TRANSPORT SECURITY)")
        print("="*60)
        
        hsts_info = """
        WHAT IS HSTS?
        -------------
        Tells browsers to always use HTTPS for your domain
        
        Header: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
        
        COMPONENTS:
        -----------
        1. max-age=31536000
           - Cache for 1 year (in seconds)
           - Should be at least 1 year for preload
        
        2. includeSubDomains
           - Apply to all subdomains
           - Be careful: all subdomains must support HTTPS
        
        3. preload
           - Submit to browser preload lists
           - Hardcoded in browsers
           - https://hstspreload.org/
        
        IMPLEMENTATION IN FLASK:
        -----------------------
        # Using Flask-Talisman (recommended)
        Talisman(
            app,
            force_https=True,
            force_https_permanent=True,
            strict_transport_security=True,
            strict_transport_security_max_age=31536000,
            strict_transport_security_include_subdomains=True,
            strict_transport_security_preload=True
        )
        
        # Manual implementation
        @app.after_request
        def add_hsts(response):
            response.headers['Strict-Transport-Security'] = 
                'max-age=31536000; includeSubDomains; preload'
            return response
        
        WARNING:
        -------
        Once set, browsers will refuse HTTP connections
        Test thoroughly before enabling includeSubDomains or preload
        """
        
        print(hsts_info)
    
    @staticmethod
    def ssl_certificate_management():
        """
        SSL certificate management strategies
        """
        
        print("\n" + "="*60)
        print("SSL CERTIFICATE MANAGEMENT")
        print("="*60)
        
        cert_managers = [
            ("LET'S ENCRYPT", """
            Free, automated certificates
            
            # Certbot installation
            sudo apt-get install certbot python3-certbot-nginx
            
            # Obtain certificate
            sudo certbot --nginx -d example.com -d www.example.com
            
            # Auto-renewal setup
            sudo certbot renew --dry-run
            
            Features:
            - Free
            - Automated renewal
            - 90-day certificates (auto-renewed)
            - Wildcard certificates available
            """),
            
            ("AWS CERTIFICATE MANAGER", """
            Free SSL/TLS certificates for AWS services
            
            # Create certificate
            aws acm request-certificate \\
                --domain-name example.com \\
                --validation-method DNS
            
            # Use with ALB/CloudFront
            # Automatically renews
            
            Features:
            - Free when used with AWS services
            - Automatic renewal
            - Integration with ALB, CloudFront, API Gateway
            """),
            
            ("AUTOMATED CERTIFICATE MANAGEMENT", """
            # Using cert-manager with Kubernetes
            
            apiVersion: cert-manager.io/v1
            kind: Certificate
            metadata:
              name: example-com
            spec:
              secretName: example-com-tls
              duration: 2160h # 90d
              renewBefore: 720h # 30d
              issuerRef:
                name: letsencrypt-prod
                kind: ClusterIssuer
              commonName: example.com
              dnsNames:
              - example.com
              - www.example.com
            
            Features:
            - Automated issuance and renewal
            - Kubernetes-native
            - Multiple issuer types
            """),
            
            ("MONITORING AND ALERTING", """
            # Monitor certificate expiration
            
            import ssl
            import socket
            from datetime import datetime
            
            def check_cert_expiry(domain, port=443):
                context = ssl.create_default_context()
                conn = context.wrap_socket(
                    socket.socket(socket.AF_INET),
                    server_hostname=domain
                )
                conn.connect((domain, port))
                cert = conn.getpeercert()
                
                expiry_date = datetime.strptime(
                    cert['notAfter'], '%b %d %H:%M:%S %Y %Z'
                )
                days_left = (expiry_date - datetime.now()).days
                
                if days_left < 30:
                    send_alert(f"Certificate for {domain} expires in {days_left} days!")
                
                return days_left
            
            # Schedule with cron or Kubernetes CronJob
            """)
        ]
        
        for manager_name, manager_info in cert_managers:
            print(f"\n{manager_name}:")
            print(manager_info)
    
    @staticmethod
    def ssl_tls_best_practices():
        """
        SSL/TLS configuration best practices
        """
        
        print("\n" + "="*60)
        print("SSL/TLS BEST PRACTICES")
        print("="*60)
        
        practices = [
            ("PROTOCOLS", """
            Use only TLS 1.2 and 1.3
            
            # Nginx configuration
            ssl_protocols TLSv1.2 TLSv1.3;
            
            # Disable old protocols
            # SSLv2, SSLv3, TLS 1.0, TLS 1.1 are insecure
            
            Why:
            - TLS 1.0/1.1 have known vulnerabilities
            - PCI DSS requires TLS 1.2+
            - Modern browsers deprecating old versions
            """),
            
            ("CIPHER SUITES", """
            Use strong, modern cipher suites
            
            # Nginx configuration (intermediate compatibility)
            ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
            ssl_prefer_server_ciphers off;
            
            # Modern configuration (TLS 1.3 only)
            ssl_ciphers TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;
            
            Test your configuration:
            $ openssl s_client -connect example.com:443 -tls1_2
            
            Use SSL Labs test: https://www.ssllabs.com/ssltest/
            """),
            
            ("PERFECT FORWARD SECRECY", """
            Ensure PFS is enabled
            
            # Use ECDHE or DHE key exchange
            ssl_ciphers "ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384";
            
            Why:
            - Compromised private key doesn't decrypt past sessions
            - Each session uses unique key
            - Required for modern security
            """),
            
            ("OCSP STAPLING", """
            Improve SSL validation performance
            
            # Nginx configuration
            ssl_stapling on;
            ssl_stapling_verify on;
            ssl_trusted_certificate /path/to/chain.pem;
            resolver 8.8.8.8 8.8.4.4 valid=300s;
            
            Benefits:
            - Faster SSL handshake
            - Better privacy (client doesn't query OCSP server)
            - Required for some browser features
            """),
            
            ("SECURE RENEGOTIATION", """
            # Nginx configuration
            ssl_session_tickets off;
            ssl_session_timeout 1d;
            ssl_session_cache shared:SSL:50m;
            
            Why:
            - Prevents certain attacks
            - Improves performance for returning visitors
            - Controls session resumption
            """)
        ]
        
        for practice_name, practice_info in practices:
            print(f"\n{practice_name}:")
            print(practice_info)

# ============================================================================
# 9. COMPREHENSIVE SECURITY MIDDLEWARE
# ============================================================================

class SecurityMiddleware:
    """
    Comprehensive security middleware for Flask
    """
    
    @staticmethod
    def create_security_middleware(app):
        """
        Add comprehensive security middleware to Flask app
        """
        
        # ============== REQUEST VALIDATION ==============
        
        @app.before_request
        def validate_request():
            """Validate all incoming requests"""
            
            # 1. Check request size
            if request.content_length and request.content_length > app.config['MAX_CONTENT_LENGTH']:
                abort(413, description="Request too large")
            
            # 2. Validate JSON for POST/PUT/PATCH
            if request.method in ['POST', 'PUT', 'PATCH']:
                if request.is_json:
                    try:
                        request.get_json()
                    except:
                        abort(400, description="Invalid JSON")
            
            # 3. Check for malicious patterns in URL
            malicious_patterns = [
                r'\.\./',  # Directory traversal
                r'<script',  # XSS attempt
                r'%3Cscript',  # URL-encoded XSS
                r'union.*select',  # SQL injection
                r'/\*.*\*/',  # SQL comment
            ]
            
            for pattern in malicious_patterns:
                if re.search(pattern, request.full_path, re.IGNORECASE):
                    app.logger.warning(f"Potential attack detected: {request.remote_addr} - {request.full_path}")
                    abort(400, description="Invalid request")
        
        # ============== RATE LIMITING PER CLIENT ==============
        
        def get_rate_limit_key():
            """Get key for rate limiting"""
            # Use API key if provided, otherwise IP
            api_key = request.headers.get('X-API-Key')
            if api_key:
                return f"api_key:{api_key}"
            return get_remote_address()
        
        # Apply global rate limits
        limiter.key_func = get_rate_limit_key
        
        # ============== SECURITY HEADERS ==============
        
        @app.after_request
        def add_security_headers(response):
            """Add comprehensive security headers"""
            
            headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Referrer-Policy': 'strict-origin-when-cross-origin',
                'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
                'Cache-Control': 'no-store, no-cache, must-revalidate, private',
                'Pragma': 'no-cache',
                'Expires': '0',
            }
            
            for header, value in headers.items():
                response.headers[header] = value
            
            return response
        
        # ============== LOGGING & MONITORING ==============
        
        @app.after_request
        def log_request(response):
            """Log all requests for security monitoring"""
            
            # Don't log sensitive endpoints (login, etc.)
            if request.path not in ['/api/auth/login', '/api/auth/register']:
                app.logger.info(
                    f"{request.remote_addr} - "
                    f"{request.method} {request.path} - "
                    f"{response.status_code} - "
                    f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
                )
            
            # Log security events
            if response.status_code in [400, 401, 403, 404, 429, 500]:
                app.logger.warning(
                    f"Security Event - IP: {request.remote_addr} - "
                    f"Path: {request.path} - Status: {response.status_code}"
                )
            
            return response
        
        # ============== ERROR HANDLING ==============
        
        @app.errorhandler(Exception)
        def handle_all_errors(error):
            """Handle all uncaught exceptions securely"""
            app.logger.error(f"Unhandled exception: {error}", exc_info=True)
            
            # Don't expose internal error details
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500

# ============================================================================
# 10. SECURITY AUDIT & TESTING UTILITIES
# ============================================================================

class SecurityAuditTools:
    """
    Tools for auditing and testing Flask security
    """
    
    @staticmethod
    def security_checklist():
        """
        Comprehensive security checklist
        """
        
        checklist = [
            ("AUTHENTICATION & SESSIONS", [
                "✓ Use strong password hashing (bcrypt, Argon2)",
                "✓ Implement account lockout after failed attempts",
                "✓ Use secure, HttpOnly, SameSite cookies",
                "✓ Implement session timeout",
                "✓ Use multi-factor authentication for sensitive operations",
                "✓ Invalidate sessions on logout",
                "✓ Regenerate session ID after login"
            ]),
            
            ("AUTHORIZATION", [
                "✓ Implement role-based access control (RBAC)",
                "✓ Principle of least privilege",
                "✓ Validate permissions on every request",
                "✓ Log authorization failures",
                "✓ Implement API key authentication for services",
                "✓ Use OAuth2 for third-party authentication"
            ]),
            
            ("INPUT VALIDATION", [
                "✓ Validate all user input",
                "✓ Use whitelist validation where possible",
                "✓ Sanitize HTML output",
                "✓ Validate file uploads (type, size, content)",
                "✓ Use parameterized queries for SQL",
                "✓ Escape output based on context (HTML, JS, URL)"
            ]),
            
            ("CRYPTOGRAPHY", [
                "✓ Use TLS 1.2+ everywhere",
                "✓ Implement HSTS",
                "✓ Store secrets in secure vault (not in code)",
                "✓ Encrypt sensitive data at rest",
                "✓ Use strong, random secrets",
                "✓ Implement secret rotation"
            ]),
            
            ("ERROR HANDLING & LOGGING", [
                "✓ Don't expose sensitive information in errors",
                "✓ Log security events",
                "✓ Monitor logs for attack patterns",
                "✓ Implement centralized logging",
                "✓ Set up alerts for security events",
                "✓ Regular log review"
            ]),
            
            ("INFRASTRUCTURE", [
                "✓ Keep dependencies updated",
                "✓ Use Web Application Firewall (WAF)",
                "✓ Implement DDoS protection",
                "✓ Regular security scanning",
                "✓ Penetration testing",
                "✓ Security headers configured"
            ]),
            
            ("API SECURITY", [
                "✓ Rate limiting implemented",
                "✓ API versioning",
                "✓ Input validation for all endpoints",
                "✓ Authentication for all endpoints",
                "✓ CORS properly configured",
                "✓ Request/response validation"
            ])
        ]
        
        print("\n" + "="*60)
        print("FLASK SECURITY CHECKLIST")
        print("="*60)
        
        for category, items in checklist:
            print(f"\n{category}:")
            for item in items:
                print(f"  {item}")
    
    @staticmethod
    def security_testing_tools():
        """
        Tools for testing Flask security
        """
        
        print("\n" + "="*60)
        print("SECURITY TESTING TOOLS")
        print("="*60)
        
        tools = [
            ("DEPENDENCY SCANNING", """
            # pip-audit - Scan for vulnerable dependencies
            pip install pip-audit
            pip-audit
            
            # safety - Check installed packages for vulnerabilities
            pip install safety
            safety check
            
            # GitHub Dependabot / GitLab Dependency Scanning
            # Automated vulnerability detection in dependencies
            """),
            
            ("STATIC CODE ANALYSIS", """
            # bandit - Security-focused static analyzer
            pip install bandit
            bandit -r . -f html -o bandit_report.html
            
            # semgrep - Advanced static analysis
            pip install semgrep
            semgrep --config auto .
            
            # SonarQube - Comprehensive code quality
            # Includes security vulnerability detection
            """),
            
            ("DYNAMIC TESTING", """
            # OWASP ZAP - Automated security scanner
            # Can test running Flask applications
            zap-baseline.py -t https://localhost:5000
            
            # Burp Suite - Manual security testing
            # Professional web vulnerability scanner
            
            # nikto - Web server scanner
            nikto -h https://localhost:5000
            """),
            
            ("CUSTOM SECURITY TESTS", """
            # Pytest with security focus
            def test_sql_injection():
                # Test endpoints for SQL injection vulnerabilities
                response = client.get('/api/users/1 OR 1=1')
                assert response.status_code != 200
                
            def test_xss_protection():
                # Test XSS protection
                xss_payload = '<script>alert("xss")</script>'
                response = client.post('/api/search', json={'q': xss_payload})
                assert '<script>' not in response.text
                
            def test_rate_limiting():
                # Test rate limiting
                for i in range(11):
                    response = client.get('/api/limited')
                assert response.status_code == 429
            """),
            
            ("CONFIGURATION AUDITING", """
            # Check Flask configuration
            def test_security_config():
                assert app.config['SESSION_COOKIE_SECURE'] == True
                assert app.config['SESSION_COOKIE_HTTPONLY'] == True
                assert app.config['SESSION_COOKIE_SAMESITE'] == 'Lax'
                assert 'DEBUG' not in app.config or app.config['DEBUG'] == False
                assert 'SECRET_KEY' in app.config and len(app.config['SECRET_KEY']) >= 32
            """)
        ]
        
        for tool_name, tool_info in tools:
            print(f"\n{tool_name}:")
            print(tool_info)

# ============================================================================
# MAIN DEMONSTRATION FUNCTION
# ============================================================================

def run_security_demo():
    """
    Run comprehensive security demonstration
    """
    print("\n" + "="*80)
    print("FLASK SECURITY BEST PRACTICES - COMPREHENSIVE GUIDE")
    print("="*80)
    
    # 1. CSRF Protection
    CSRFProtectionStrategies.demonstrate_csrf_attack()
    CSRFProtectionStrategies.csrf_best_practices()
    
    # 2. XSS & Input Sanitization
    XSSProtection.demonstrate_xss_vulnerabilities()
    XSSProtection.xss_prevention_guide()
    
    # 3. SQL Injection Prevention
    SQLInjectionProtection.demonstrate_sql_injection()
    SQLInjectionProtection.sql_injection_prevention_rules()
    
    # 4. Secure Headers
    SecureHeadersImplementation.demonstrate_secure_headers()
    SecureHeadersImplementation.content_security_policy_examples()
    
    # 5. Rate Limiting
    RateLimitingStrategies.demonstrate_rate_limiting()
    RateLimitingStrategies.advanced_rate_limiting_patterns()
    
    # 6. Secrets Management
    SecretsManagement.demonstrate_secrets_management()
    SecretsManagement.production_secrets_managers()
    
    # 7. HTTPS Enforcement
    HTTPSEnforcement.demonstrate_https_importance()
    HTTPSEnforcement.ssl_tls_best_practices()
    
    # 8. Security Audit
    SecurityAuditTools.security_checklist()
    SecurityAuditTools.security_testing_tools()
    
    print("\n" + "="*80)
    print("SECURITY SUMMARY")
    print("="*80)
    print("""
    CRITICAL SECURITY PRACTICES FOR FLASK:
    
    1. NEVER TRUST USER INPUT
       - Validate all inputs
       - Sanitize all outputs
       - Use parameterized queries
    
    2. ALWAYS USE HTTPS
       - TLS 1.2+ only
       - HSTS with preload
       - Secure cookies
    
    3. IMPLEMENT DEFENSE IN DEPTH
       - CSRF tokens
       - Rate limiting
       - Security headers
       - Input validation
    
    4. SECURE SECRETS MANAGEMENT
       - Never hardcode secrets
       - Use environment variables or vault
       - Regular secret rotation
    
    5. REGULAR SECURITY TESTING
       - Dependency scanning
       - Static code analysis
       - Penetration testing
       - Security audits
    
    6. PROPER ERROR HANDLING
       - Don't expose internal details
       - Log security events
       - Monitor for attacks
    
    7. KEEP DEPENDENCIES UPDATED
       - Regular updates
       - Vulnerability scanning
       - Security patches
    
    REMEMBER: Security is a process, not a product.
    Regular review and updating of security measures is essential.
    """)

# ============================================================================
# EXAMPLE SECURE FLASK APPLICATION
# ============================================================================

def create_secure_flask_app():
    """
    Complete secure Flask application example
    """
    
    app = Flask(__name__)
    
    # ============== SECURITY CONFIGURATION ==============
    
    # Load from environment (never hardcode!)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # ============== SECURITY EXTENSIONS ==============
    
    # CSRF Protection
    csrf = CSRFProtect(app)
    
    # Rate Limiting with Redis
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        storage_uri="redis://localhost:6379/0",
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Security Headers
    Talisman(
        app,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self'",
            'style-src': "'self' 'unsafe-inline'",
            'img-src': "'self' data: https:",
            'font-src': "'self'"
        },
        force_https=True,
        force_https_permanent=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        strict_transport_security_include_subdomains=True,
        strict_transport_security_preload=True
    )
    
    # ============== SECURE ROUTES ==============
    
    @app.route('/api/secure-data', methods=['GET'])
    @limiter.limit("100 per hour")
    def get_secure_data():
        """Secure endpoint with rate limiting and CSRF protection"""
        # This endpoint is automatically protected by CSRF
        # and rate limiting
        
        # Validate input parameters
        user_id = request.args.get('user_id')
        if not user_id or not user_id.isdigit():
            return jsonify({'error': 'Invalid user ID'}), 400
        
        # Use parameterized query (SQLAlchemy)
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Sanitize output
        safe_data = {
            'id': user.id,
            'username': bleach.clean(user.username),
            'email': user.email  # Email doesn't need HTML sanitization
        }
        
        return jsonify(safe_data)
    
    @app.route('/api/login', methods=['POST'])
    @limiter.limit("5 per minute", key_func=lambda: request.json.get('username', get_remote_address()))
    def login():
        """Secure login endpoint"""
        data = request.json
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing credentials'}), 400
        
        username = data['username']
        password = data['password']
        
        # Input validation
        if len(username) > 50 or len(password) > 100:
            return jsonify({'error': 'Invalid input length'}), 400
        
        # Authentication logic here...
        # Use bcrypt for password hashing
        
        return jsonify({'message': 'Login successful', 'token': 'jwt-token-here'})
    
    # ============== ERROR HANDLERS ==============
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(429)
    def ratelimit_error(error):
        return jsonify({
            'error': 'Too many requests',
            'message': 'Rate limit exceeded'
        }), 429
    
    return app

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask Security Demo')
    parser.add_argument('--demo', action='store_true', help='Run security demo')
    parser.add_argument('--run', action='store_true', help='Run secure Flask app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    
    args = parser.parse_args()
    
    if args.demo:
        run_security_demo()
    elif args.run:
        # Run the secure Flask application
        secure_app = create_secure_flask_app()
        
        print(f"\nStarting secure Flask application on https://localhost:{args.port}")
        print("\nSecurity features enabled:")
        print("  ✓ CSRF protection")
        print("  ✓ Rate limiting")
        print("  ✓ Security headers (CSP, HSTS, etc.)")
        print("  ✓ Secure cookies")
        print("  ✓ Input validation")
        print("  ✓ SQL injection prevention")
        print("  ✓ XSS protection")
        
        # For development only - in production use reverse proxy
        context = ('cert.pem', 'key.pem')  # Self-signed certs for demo
        secure_app.run(
            ssl_context=context,
            debug=True,
            port=args.port
        )
    else:
        print("Usage: python flask_security.py [--demo|--run]")
        print("\nOptions:")
        print("  --demo    Run comprehensive security demonstration")
        print("  --run     Run secure Flask application")