"""
FLASK EXTENSIONS: COMPREHENSIVE GUIDE WITH DECISION TREES

This guide explains WHEN, WHY, and HOW to use each major Flask extension,
with practical examples and decision matrices.
"""

# ============================================================================
# EXTENSION SELECTION FLOWCHART (MENTAL MODEL)
# ============================================================================
"""
QUICK DECISION TREE FOR COMMON SCENARIOS:

1. DO YOU NEED A DATABASE?
   ├── YES → Use Flask-SQLAlchemy (ORM layer)
   │   ├── Need schema migrations? → Add Flask-Migrate
   │   └── Complex async needs? → Consider plain async SQLAlchemy
   └── NO → Skip database extensions

2. DO YOU NEED AUTHENTICATION?
   ├── Traditional website with sessions → Flask-Login
   ├── API/SPA/Mobile app → Flask-JWT-Extended
   ├── Both web and API → Use both
   └── Simple API keys → Custom implementation

3. DO YOU NEED INPUT VALIDATION/SERIALIZATION?
   ├── Tight SQLAlchemy integration → Flask-Marshmallow
   ├── Type hints/FastAPI future → Pydantic (not Flask-specific)
   └── Simple forms → WTForms (built into Flask)

4. IS THIS AN API SERVING EXTERNAL CLIENTS?
   ├── YES → Flask-CORS (configure carefully!)
   └── NO → Skip CORS

5. IS THIS A PUBLIC API OR NEEDS SECURITY?
   ├── YES → Flask-Limiter (rate limiting)
   └── Internal only → Optional

6. DO YOU HAVE PERFORMANCE ISSUES/HIGH TRAFFIC?
   ├── YES → Flask-Caching (Redis recommended)
   └── NO → Defer until needed
"""

# ============================================================================
# 1. FLASK-SQLALCHEMY vs PLAIN SQLALCHEMY
# ============================================================================

"""
WHY USE FLASK-SQLALCHECHEMY:
1. Automatic request-scoped sessions (db.session tied to Flask context)
2. Simplified model definition with db.Model
3. Built-in query interface on model classes
4. Flask CLI integration
5. Easier testing with app context

WHEN TO USE FLASK-SQLALCHEMY:
✅ Most Flask web applications
✅ When you want request-scoped sessions automatically
✅ When using Flask-Migrate (tight integration)
✅ Team projects where consistency matters

WHEN TO USE PLAIN SQLALCHEMY:
✅ Non-Flask projects
✅ Complex async/await applications
✅ Need multiple independent database sessions
✅ Advanced transaction management scenarios
✅ Microservices where Flask might be replaced later
"""

# Example: Flask-SQLAlchemy setup
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):  # Inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    
# Automatic session management per request
users = User.query.filter_by(active=True).all()  # Simple query interface

# ============================================================================
# 2. FLASK-MIGRATE (ALEMBIC)
# ============================================================================

"""
WHY USE FLASK-MIGRATE:
1. Automatic migration generation from model changes
2. Flask CLI integration (flask db migrate/upgrade)
3. Manages database schema versioning
4. Team collaboration on schema changes
5. Production deployment safety

WHEN TO USE FLASK-MIGRATE:
✅ Any production application with database
✅ Team development (schema consistency)
✅ Need rollback capability (downgrade)
✅ Frequent schema changes
✅ Multiple environments (dev/staging/prod)

WHEN NOT TO USE:
❌ Quick prototypes without database
❌ Simple apps with fixed schema
❌ Using NoSQL databases
"""

from flask_migrate import Migrate
migrate = Migrate(app, db)

# CLI commands:
# flask db init           # Initialize migration repository
# flask db migrate -m "message"  # Auto-generate migration
# flask db upgrade       # Apply migrations
# flask db downgrade     # Rollback migration

# ============================================================================
# 3. FLASK-LOGIN vs FLASK-JWT-EXTENDED
# ============================================================================

"""
FLASK-LOGIN (Session-based):
WHY: Traditional web authentication, server-side sessions
WHEN TO USE:
✅ Server-rendered websites (Jinja templates)
✅ Need "remember me" functionality
✅ Simple permission systems
✅ When cookies/sessions are acceptable

FLASK-JWT-EXTENDED (Token-based):
WHY: Stateless authentication for APIs, SPAs, mobile apps
WHEN TO USE:
✅ REST APIs consumed by frontend frameworks
✅ Single Page Applications (React/Vue/Angular)
✅ Mobile app backends
✅ Microservices architecture
✅ Need stateless, scalable auth
"""

# Flask-Login Example (Sessions)
from flask_login import LoginManager, login_required
login_manager = LoginManager(app)

@app.route('/dashboard')
@login_required  # Redirects to login if not authenticated
def dashboard():
    return f"Hello {current_user.name}"

# Flask-JWT-Extended Example (Tokens)
from flask_jwt_extended import JWTManager, jwt_required
jwt = JWTManager(app)

@app.route('/api/protected')
@jwt_required()  # Validates JWT in Authorization header
def protected():
    return jsonify(message="Access granted")

# DECISION MATRIX:
# | Client Type        | Flask-Login | Flask-JWT |
# |--------------------|-------------|-----------|
# | Traditional Website| ✅ Best     | ⚠️ Possible |
# | SPA (React/Vue)    | ⚠️ Difficult | ✅ Best   |
# | Mobile App         | ❌ Poor     | ✅ Best   |
# | API for 3rd parties| ❌ Poor     | ✅ Best   |

# ============================================================================
# 4. FLASK-MARSHMALLOW vs PYDANTIC
# ============================================================================

"""
FLASK-MARSHMALLOW:
WHY: SQLAlchemy integration, schema-based validation
WHEN TO USE:
✅ Already using SQLAlchemy extensively
✅ Need automatic serialization of SQLAlchemy models
✅ Complex relationships with nested serialization
✅ Prefer declarative schema style

PYDANTIC:
WHY: Type-driven validation, FastAPI compatibility, performance
WHEN TO USE:
✅ Type hints and mypy support important
✅ Future FastAPI migration possible
✅ Want validation separate from DB models
✅ Prefer Python's native type annotations
✅ Need excellent JSON Schema generation
"""

# Flask-Marshmallow Example
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User  # Tied to SQLAlchemy model
    id = ma.auto_field()
    name = ma.auto_field()

# Pydantic Example
from pydantic import BaseModel
class UserCreate(BaseModel):
    name: str
    email: str

# CHOICE MATRIX:
# | Requirement          | Marshmallow | Pydantic  |
# |----------------------|-------------|-----------|
# | SQLAlchemy integration | ✅ Excellent | ⚠️ Manual |
# | Type hints/mypy      | ⚠️ Limited  | ✅ Excellent |
# | FastAPI compatibility| ❌ No       | ✅ Perfect |
# | Performance          | ✅ Good     | ✅ Excellent |
# | Nested validation    | ✅ Good     | ✅ Excellent |

# ============================================================================
# 5. FLASK-CORS
# ============================================================================

"""
WHY USE FLASK-CORS:
1. Browser security blocks cross-origin requests
2. Needed for APIs serving web frontends on different domains
3. Configures proper CORS headers automatically

WHEN TO USE:
✅ API serving JavaScript frontend on different domain
✅ Mobile app backends
✅ Public APIs
✅ Development with separate frontend servers

WHEN NOT TO USE:
❌ Same-origin applications
❌ Internal microservices (use API gateway)
❌ Server-rendered pages only
"""

from flask_cors import CORS

# Development (permissive)
if app.config['ENV'] == 'development':
    CORS(app, origins=['http://localhost:3000'])

# Production (restrictive)
if app.config['ENV'] == 'production':
    CORS(app, origins=['https://example.com'])

# NEVER USE IN PRODUCTION:
# CORS(app)  # Allows ALL origins - security risk!

# ============================================================================
# 6. FLASK-LIMITER
# ============================================================================

"""
WHY USE FLASK-LIMITER:
1. Prevent abuse and DoS attacks
2. Fair usage policy enforcement
3. API cost control
4. Brute force protection

WHEN TO USE:
✅ Public APIs
✅ Authentication endpoints (login/password reset)
✅ Expensive operations (search, reports)
✅ Paid API tiers with different limits
✅ Security-sensitive endpoints

WHEN NOT TO USE:
❌ Internal-only APIs with trusted clients
❌ Very low-traffic applications
❌ Static content delivery
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

# Essential for security:
@app.route('/login')
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    pass

@app.route('/api/search')
@limiter.limit("30 per minute")  # Prevent abuse
def search():
    pass

# Storage backends (choose one):
# - Redis: ✅ Production, distributed, persistent
# - Memory: ❌ Development only, single process
# - Database: ⚠️ Fallback option, slower

# ============================================================================
# 7. FLASK-CACHING
# ============================================================================

"""
WHY USE FLASK-CACHING:
1. Improve application performance
2. Reduce database load
3. Faster response times
4. Handle traffic spikes

WHEN TO USE:
✅ High-traffic endpoints
✅ Expensive database queries/calculations
✅ Data that changes infrequently
✅ API responses that can be cached
✅ Reduce external API calls

WHEN NOT TO USE:
❌ User-specific data that changes frequently
❌ Real-time data
❌ Simple applications with minimal traffic
❌ Data that must always be fresh
"""

from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# What to cache:
@app.route('/api/products')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_products():
    # Product listings change infrequently
    pass

@app.route('/api/stats')
@cache.cached(timeout=3600)  # Cache for 1 hour
def get_stats():
    # Expensive aggregation queries
    pass

# What NOT to cache:
@app.route('/api/user/profile')
@login_required
def get_profile():
    # User-specific, changes frequently
    pass

# Cache backends ranking:
# 1. Redis: ✅ Best for production, distributed, feature-rich
# 2. Memcached: ✅ Good for high read volume
# 3. Filesystem: ⚠️ Multiple processes, slower
# 4. SimpleCache: ❌ Development only, single process

# ============================================================================
# PROJECT TYPE RECOMMENDATIONS
# ============================================================================

"""
1. TRADITIONAL WEBSITE (Server-rendered):
   - Flask-SQLAlchemy
   - Flask-Migrate
   - Flask-Login
   - Flask-Caching (optional)
   - WTForms (built-in)

2. REST API (Backend for frontend):
   - Flask-SQLAlchemy
   - Flask-Migrate
   - Flask-JWT-Extended
   - Flask-CORS
   - Flask-Limiter
   - Flask-Caching
   - Pydantic or Flask-Marshmallow

3. SPA BACKEND (React/Vue/Angular):
   - Flask-SQLAlchemy
   - Flask-Migrate
   - Flask-JWT-Extended
   - Flask-CORS (configured for frontend origin)
   - Flask-Limiter
   - Flask-Caching (Redis)

4. MICROSERVICE:
   - Flask (minimal extensions)
   - Flask-JWT-Extended (if auth needed)
   - Pydantic (validation)
   - Consider async SQLAlchemy if high concurrency

5. QUICK PROTOTYPE:
   - Flask-SQLAlchemy (optional)
   - Skip migrations initially
   - Minimal authentication
   - Add extensions as needed
"""

# ============================================================================
# EXTENSION COMBINATION PATTERNS
# ============================================================================

def setup_extensions(app, project_type):
    """Configure extensions based on project type."""
    
    extensions = {}
    
    # Always initialize in correct order
    if project_type in ['website', 'api', 'spa']:
        # Database
        from flask_sqlalchemy import SQLAlchemy
        extensions['db'] = SQLAlchemy(app)
        
        # Migrations (if using database)
        from flask_migrate import Migrate
        extensions['migrate'] = Migrate(app, extensions['db'])
    
    # Authentication
    if project_type == 'website':
        from flask_login import LoginManager
        extensions['login_manager'] = LoginManager(app)
    elif project_type in ['api', 'spa']:
        from flask_jwt_extended import JWTManager
        extensions['jwt'] = JWTManager(app)
    
    # CORS for APIs/SPAs
    if project_type in ['api', 'spa']:
        from flask_cors import CORS
        extensions['cors'] = CORS(app)  # Configure appropriately
    
    # Rate limiting for public endpoints
    if project_type in ['api', 'spa']:
        from flask_limiter import Limiter
        extensions['limiter'] = Limiter(app)
    
    # Caching for performance
    if project_type in ['website', 'api', 'spa']:
        from flask_caching import Cache
        extensions['cache'] = Cache(app)
    
    return extensions

# ============================================================================
# SECURITY CONSIDERATIONS BY EXTENSION
# ============================================================================

"""
CRITICAL SECURITY CONFIGURATIONS:

1. FLASK-SQLALCHEMY:
   - Use connection pooling
   - Set SQLALCHEMY_TRACK_MODIFICATIONS = False
   - Parameterize all queries (automatic with ORM)

2. FLASK-JWT-EXTENDED:
   - Strong JWT_SECRET_KEY (environment variable)
   - Reasonable token expiration times
   - Use HTTPS in production
   - Implement token blacklisting for logout

3. FLASK-CORS:
   - NEVER use wildcard origins in production
   - Specify exact allowed origins
   - Limit allowed methods and headers
   - Use credentials carefully

4. FLASK-LIMITER:
   - Implement on authentication endpoints
   - Use Redis storage in production
   - Different limits for different user types
   - Monitor breach logs

5. FLASK-CACHING:
   - Never cache sensitive data
   - Use appropriate cache timeouts
   - Implement cache invalidation
   - Secure Redis/Memcached access
"""

# ============================================================================
# PERFORMANCE IMPLICATIONS
# ============================================================================

"""
EXTENSION PERFORMANCE IMPACT:

1. FLASK-SQLALCHEMY:
   - ⚠️ Over-fetching data (N+1 query problem)
   - Solution: Use eager loading (.options(joinedload()))

2. FLASK-CACHING:
   - ✅ Major performance improvement
   - Risk: Stale data if not invalidated properly

3. FLASK-MARSHMALLOW:
   - ⚠️ Serialization overhead for large datasets
   - Solution: Use only needed fields, pagination

4. FLASK-LIMITER:
   - ⚠️ Redis calls add latency
   - Necessary trade-off for security

5. ALL EXTENSIONS:
   - Each adds some overhead
   - Profile before optimizing
   - Use only needed extensions
"""

# ============================================================================
# MIGRATION GUIDE (ADDING EXTENSIONS LATER)
# ============================================================================

"""
ADDING EXTENSIONS TO EXISTING PROJECT:

1. Flask-SQLAlchemy to existing SQLAlchemy:
   - Replace Base with db.Model
   - Update session usage to db.session
   - Update queries to Model.query pattern

2. Adding Flask-Migrate:
   - flask db init
   - Create initial migration
   - Apply to database
   - Add to deployment pipeline

3. Flask-Login to Flask-JWT (or vice versa):
   - Support both during transition
   - Update frontend/auth clients gradually
   - Run both systems in parallel

4. Adding Flask-Caching:
   - Identify cacheable endpoints
   - Add @cache.cached() decorators
   - Implement cache invalidation
   - Monitor cache hit rates

5. Adding Flask-Limiter:
   - Start with generous limits
   - Monitor usage patterns
   - Adjust limits based on data
   - Add stricter limits gradually
"""

# ============================================================================
# FINAL RECOMMENDATIONS
# ============================================================================

"""
GOLDEN RULES:

1. START MINIMAL: Add extensions only when needed
2. PRODUCTION READY: Configure extensions differently per environment
3. SECURITY FIRST: Always secure auth, CORS, and rate limiting
4. MONITOR: Track extension performance and errors
5. UPDATE: Keep extensions updated for security patches
6. DOCUMENT: Extension configuration can be complex
7. TEST: Test with extensions enabled/disabled
8. PLAN SCALE: Choose extensions that support growth

COMMON MISTAKES TO AVOID:

1. Using Flask-SQLAlchemy in non-Flask projects
2. Wildcard CORS in production (*)
3. No rate limiting on public endpoints
4. Caching sensitive/user-specific data
5. Default secret keys in production
6. No database migrations in team projects
7. Using memory cache in production
8. Not monitoring extension performance
"""

# ============================================================================
# EXAMPLE: COMPLETE API PROJECT SETUP
# ============================================================================

"""
A typical REST API project would use:

# requirements.txt
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
Flask-CORS
Flask-Limiter
Flask-Caching
redis  # For caching and rate limiting
PyJWT
pydantic  # For validation
python-dotenv  # For environment variables

# app/__init__.py
def create_api_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.ProductionConfig')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config['ALLOWED_ORIGINS'])
    limiter.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'redis'})
    
    # Register blueprints
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    return app

This setup provides:
- Database with migrations
- JWT authentication
- CORS for frontend
- Rate limiting for security
- Redis caching for performance
- Structured project layout
"""