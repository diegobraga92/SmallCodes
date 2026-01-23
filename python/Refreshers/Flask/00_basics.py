"""
Flask Comprehensive Tutorial: Core Concepts Explained with Examples

This file demonstrates various Flask concepts through a comprehensive
application structure. Each section is commented to explain the concepts.

Author: Flask Educator
Date: 2024
"""

# ============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# ============================================================================
import os
import datetime
import uuid
from typing import Dict, Any, Optional

from flask import (
    Flask,              # Main Flask class
    Blueprint,          # For modular applications
    request,            # Request object (context-local)
    session,            # Session object (context-local)
    g,                  # Global context object
    current_app,        # Current application instance (context-local)
    jsonify,            # Create JSON responses
    render_template,    # Render HTML templates
    redirect,           # Redirect responses
    url_for,            # Generate URLs
    abort,              # Abort request with error code
    make_response,      # Create custom responses
    Response            # Response class
)
from werkzeug.exceptions import HTTPException

# ============================================================================
# SECTION 2: APPLICATION FACTORY PATTERN
# ============================================================================
"""
APPLICATION FACTORY PATTERN (create_app)

Purpose:
- Creates Flask application instances dynamically
- Enables multiple app instances with different configurations
- Facilitates testing with different configs
- Supports application extensions initialization

Why use it?
1. Configurability: Different configs for dev, test, production
2. Testability: Easy to create app instances for testing
3. Scalability: Multiple instances can share common setup
4. Clean structure: Separation of app creation and configuration
"""

def create_app(config_name: str = 'development') -> Flask:
    """
    Factory function to create and configure Flask applications.
    
    Args:
        config_name: Configuration profile name ('development', 'testing', 'production')
    
    Returns:
        Configured Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # ========================================================================
    # Configuration based on environment
    # ========================================================================
    configs = {
        'development': {
            'DEBUG': True,
            'SECRET_KEY': 'dev-key-please-change',
            'ENV': 'development',
            'DATABASE_URI': 'sqlite:///dev.db'
        },
        'testing': {
            'DEBUG': True,
            'TESTING': True,
            'SECRET_KEY': 'test-key',
            'DATABASE_URI': 'sqlite:///test.db'
        },
        'production': {
            'DEBUG': False,
            'SECRET_KEY': os.environ.get('SECRET_KEY', 'prod-key-change-me'),
            'DATABASE_URI': os.environ.get('DATABASE_URI')
        }
    }
    
    # Apply configuration
    if config_name in configs:
        app.config.update(configs[config_name])
    else:
        raise ValueError(f"Unknown config name: {config_name}")
    
    # ========================================================================
    # Initialize extensions (demonstrative - no actual extensions here)
    # ========================================================================
    # Example: db.init_app(app)
    # Example: login_manager.init_app(app)
    # Example: mail.init_app(app)
    
    # ========================================================================
    # Register blueprints (modular components)
    # ========================================================================
    from .blueprints.auth import auth_bp
    from .blueprints.api import api_bp
    from .blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # ========================================================================
    # Register custom URL converters
    # ========================================================================
    from .converters import ListConverter
    app.url_map.converters['list'] = ListConverter
    
    # ========================================================================
    # Register error handlers
    # ========================================================================
    register_error_handlers(app)
    
    # ========================================================================
    # Register before/after request hooks
    # ========================================================================
    register_hooks(app)
    
    # ========================================================================
    # Register CLI commands (example)
    # ========================================================================
    @app.cli.command('init-db')
    def init_db_command():
        """Initialize the database."""
        print("Database initialized (demo)")
    
    return app


# ============================================================================
# SECTION 3: BLUEPRINTS - MODULAR APPLICATION STRUCTURE
# ============================================================================
"""
BLUEPRINT USAGE AND WHEN TO SPLIT APPS

What are Blueprints?
- Blueprints are Flask's way to organize applications into modular components
- Each blueprint has its own routes, templates, static files
- Blueprints are registered with the main application

When to use Blueprints vs when to split apps:
1. USE BLUEPRINTS WHEN:
   - Different functional modules in same app (auth, admin, api)
   - Sharing templates/static files across modules
   - Need namespace separation for routes
   - Team collaboration on different modules

2. SPLIT INTO SEPARATE APPS WHEN:
   - Completely independent functionality
   - Different deployment requirements
   - Different teams with separate release cycles
   - Microservices architecture
   - Need complete isolation
"""

# Example of creating a blueprint (usually in separate file)
auth_bp = Blueprint('auth', __name__, 
                   template_folder='templates/auth',
                   static_folder='static/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authentication blueprint route."""
    # Blueprint routes work just like app routes
    return "Login page (from auth blueprint)"

@auth_bp.route('/logout')
def logout():
    """Logout route in auth blueprint."""
    session.clear()
    return redirect(url_for('main.index'))


# Example API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users', methods=['GET'])
def get_users():
    """API endpoint in api blueprint."""
    return jsonify({'users': ['alice', 'bob']})


# ============================================================================
# SECTION 4: REQUEST/RESPONSE LIFECYCLE AND CONTEXT LOCALS
# ============================================================================
"""
REQUEST/RESPONSE LIFECYCLE

1. Client sends HTTP request
2. WSGI server receives request
3. Flask creates Request Context (request, session)
4. Flask creates Application Context (current_app, g)
5. before_request hooks execute (in order of registration)
6. Route handler processes request
7. after_request hooks execute (in reverse order)
8. Response sent to client
9. Contexts torn down

CONTEXT LOCALS:

1. REQUEST CONTEXT (per request):
   - request: Contains data about current HTTP request
   - session: User session (stored on server, sent as cookie)

2. APPLICATION CONTEXT (per app):
   - current_app: Current application instance
   - g: "Global" context for storing data during a single request
"""

# Main application using factory pattern
app = create_app()

@app.route('/')
def index():
    """
    Homepage demonstrating context locals.
    
    Shows how different context objects are used during request processing.
    """
    # ========================================================================
    # Using request object (Request Context)
    # ========================================================================
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    method = request.method
    
    # Accessing query parameters
    name = request.args.get('name', 'Guest')
    
    # Accessing form data (if POST request)
    if request.method == 'POST':
        form_data = request.form.get('data')
    
    # ========================================================================
    # Using session object (Request Context)
    # ========================================================================
    # Store data in session (persists across requests via cookie)
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['visit_count'] = 0
    
    session['visit_count'] = session.get('visit_count', 0) + 1
    session['last_visit'] = datetime.datetime.now().isoformat()
    
    # ========================================================================
    # Using g object (Application Context)
    # ========================================================================
    # g is for storing data during a single request only
    # Common use: database connections, user info, request start time
    g.request_start_time = datetime.datetime.now()
    g.current_user = {'id': session['user_id'], 'name': name}
    
    # ========================================================================
    # Using current_app (Application Context)
    # ========================================================================
    # Access app config and attributes
    debug_mode = current_app.config['DEBUG']
    app_name = current_app.name
    
    # ========================================================================
    # Prepare response data
    # ========================================================================
    response_data = {
        'message': f'Hello, {name}!',
        'client_info': {
            'ip': client_ip,
            'user_agent': user_agent,
            'method': method
        },
        'session_info': {
            'user_id': session['user_id'],
            'visits': session['visit_count'],
            'last_visit': session.get('last_visit')
        },
        'app_info': {
            'debug_mode': debug_mode,
            'app_name': app_name
        },
        'request_data': {
            'stored_in_g': {
                'user': g.current_user,
                'start_time': str(g.request_start_time)
            }
        }
    }
    
    return jsonify(response_data)


# ============================================================================
# SECTION 5: URL ROUTING WITH CONVERTERS AND CUSTOM ROUTES
# ============================================================================
"""
URL ROUTING, CONVERTERS, AND CUSTOM ROUTES

Flask supports various URL parameter types via converters:
- string: (default) accepts any text without slashes
- int: positive integers
- float: positive floating point values
- path: like string but accepts slashes
- uuid: UUID strings

Custom converters can be created for complex patterns.
"""

# ========================================================================
# Built-in converters
# ========================================================================
@app.route('/user/<string:username>')
def show_user_profile(username: str):
    """String converter (default)."""
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id: int):
    """Integer converter."""
    return f'Post #{post_id}'

@app.route('/price/<float:price>')
def show_price(price: float):
    """Float converter."""
    return f'Price: ${price:.2f}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath: str):
    """Path converter (accepts slashes)."""
    return f'Subpath: {subpath}'

@app.route('/object/<uuid:object_id>')
def show_object(object_id: uuid.UUID):
    """UUID converter."""
    return f'Object UUID: {object_id}'

# ========================================================================
# Custom converter example
# ========================================================================
from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
    """
    Custom converter for comma-separated lists in URLs.
    
    Example: /items/1,2,3,4
    """
    def to_python(self, value: str) -> list:
        """Convert URL string to Python list."""
        return value.split(',')
    
    def to_url(self, values: list) -> str:
        """Convert Python list to URL string."""
        return ','.join(str(v) for v in values)

# Register custom converter (already done in create_app)
# app.url_map.converters['list'] = ListConverter

@app.route('/items/<list:item_ids>')
def show_items(item_ids: list):
    """Using custom list converter."""
    return f'Items: {item_ids} (type: {type(item_ids)})'

# ========================================================================
# Complex routing with multiple methods
# ========================================================================
@app.route('/api/tasks', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_tasks():
    """
    Single endpoint handling multiple HTTP methods.
    
    Demonstrates RESTful API design pattern.
    """
    if request.method == 'GET':
        # Return all tasks
        return jsonify({'action': 'GET', 'tasks': ['task1', 'task2']})
    
    elif request.method == 'POST':
        # Create new task
        data = request.get_json()
        return jsonify({'action': 'POST', 'created': data}), 201
    
    elif request.method == 'PUT':
        # Update tasks
        return jsonify({'action': 'PUT', 'updated': True})
    
    elif request.method == 'DELETE':
        # Delete tasks
        return jsonify({'action': 'DELETE', 'deleted': True}), 204

# ========================================================================
# URL generation with url_for
# ========================================================================
@app.route('/dashboard')
def dashboard():
    """Dashboard page demonstrating url_for usage."""
    # Generate URLs for different endpoints
    user_url = url_for('show_user_profile', username='john')
    post_url = url_for('show_post', post_id=42)
    items_url = url_for('show_items', item_ids=['a', 'b', 'c'])
    
    links = {
        'user_profile': user_url,
        'post': post_url,
        'items': items_url
    }
    
    return jsonify({'links': links})


# ============================================================================
# SECTION 6: ERROR HANDLING
# ============================================================================
"""
ERROR HANDLING (@app.errorhandler)

Flask provides decorators to register custom error handlers.
These handlers can catch specific HTTP errors or all exceptions.
"""

def register_error_handlers(app: Flask):
    """Register custom error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request was malformed or invalid.',
            'status': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status': 404
        }), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 Forbidden errors."""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.',
            'status': 403
        }), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        # Log the error here (in production)
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'status': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_all_exceptions(error):
        """Catch-all exception handler."""
        # Check if it's an HTTPException (has a status code)
        if isinstance(error, HTTPException):
            response = {
                'error': error.name,
                'message': error.description,
                'status': error.code
            }
            return jsonify(response), error.code
        
        # Handle unexpected exceptions
        app.logger.exception(f'Unhandled Exception: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'status': 500
        }), 500

# ========================================================================
# Route demonstrating error handling
# ========================================================================
@app.route('/simulate-error/<error_code>')
def simulate_error(error_code: str):
    """
    Simulate different error conditions.
    
    Demonstrates abort() and automatic error handling.
    """
    try:
        code = int(error_code)
        
        if code == 400:
            abort(400, description="Custom bad request message")
        elif code == 404:
            abort(404)
        elif code == 403:
            abort(403, description="Access denied")
        elif code == 500:
            # Simulate an internal error
            raise ValueError("Simulated internal server error")
        elif code == 418:
            # I'm a teapot - for demonstration
            return jsonify({
                'message': "I'm a teapot",
                'status': 418
            }), 418
        else:
            return jsonify({
                'message': f'No error simulated for code {code}',
                'status': 200
            })
    
    except ValueError:
        # Handle non-integer error codes
        abort(400, description="Error code must be a number")


# ============================================================================
# SECTION 7: BEFORE/AFTER REQUEST HOOKS
# ============================================================================
"""
BEFORE/AFTER REQUEST HOOKS

These decorators allow you to execute code:
- before_request: Before each request
- after_request: After each request, before response is sent
- teardown_request: After response is sent (even if exception occurred)

Execution order for multiple hooks:
1. before_request hooks (in registration order)
2. Route handler
3. after_request hooks (in REVERSE registration order)
4. teardown_request hooks (in REVERSE registration order)
"""

def register_hooks(app: Flask):
    """Register before/after request hooks."""
    
    # ========================================================================
    # Before request hooks
    # ========================================================================
    @app.before_request
    def hook_before_request_1():
        """
        First before_request hook.
        
        Common uses:
        - Database connection setup
        - Authentication checks
        - Request logging
        - Setting request start time
        """
        # Store request start time in g
        g.request_start_time = datetime.datetime.now()
        g.request_id = str(uuid.uuid4())
        
        # Log request
        app.logger.debug(f'[{g.request_id}] Request started: {request.path}')
        
        # Example: Check authentication (simplified)
        if request.endpoint not in ['index', 'login', 'static']:
            if 'user_id' not in session:
                # Could redirect to login here
                pass
    
    @app.before_request
    def hook_before_request_2():
        """
        Second before_request hook.
        
        Hooks execute in registration order.
        """
        # Add custom header to request
        g.custom_header = 'X-Custom-Value'
    
    # ========================================================================
    # After request hooks
    # ========================================================================
    @app.after_request
    def hook_after_request_1(response: Response) -> Response:
        """
        First after_request hook.
        
        Note: after_request hooks run in REVERSE registration order.
        This means hook_after_request_2 runs BEFORE hook_after_request_1.
        
        Common uses:
        - Adding headers to response
        - Response logging
        - Setting CORS headers
        - Response modification
        """
        # Calculate request duration
        if hasattr(g, 'request_start_time'):
            duration = datetime.datetime.now() - g.request_start_time
            response.headers['X-Request-Duration'] = str(duration.total_seconds())
        
        # Add custom header
        response.headers['X-Custom-Header'] = 'Processed'
        
        # Log response
        request_id = getattr(g, 'request_id', 'unknown')
        app.logger.debug(f'[{request_id}] Request completed: {response.status}')
        
        return response
    
    @app.after_request
    def hook_after_request_2(response: Response) -> Response:
        """
        Second after_request hook.
        
        This runs BEFORE hook_after_request_1 because
        after_request hooks execute in reverse order.
        """
        # Add CORS headers (simplified example)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
    
    # ========================================================================
    # Teardown request hooks
    # ========================================================================
    @app.teardown_request
    def hook_teardown_request(exception: Optional[Exception]):
        """
        Teardown request hook.
        
        Runs after response is sent to client, even if exception occurred.
        Teardown hooks execute in REVERSE registration order.
        
        Common uses:
        - Database connection cleanup
        - Resource cleanup
        - Final logging
        """
        if exception:
            app.logger.error(f'Request teardown with exception: {exception}')
        
        # Cleanup example
        if hasattr(g, 'db_connection'):
            # g.db_connection.close() - hypothetical cleanup
            pass
        
        request_id = getattr(g, 'request_id', 'unknown')
        app.logger.debug(f'[{request_id}] Request teardown complete')

# ========================================================================
# Demonstration route for hooks
# ========================================================================
@app.route('/hooks-demo')
def hooks_demo():
    """
    Route to demonstrate before/after request hooks.
    
    Check response headers to see hooks in action.
    """
    response_data = {
        'message': 'Check response headers for hook modifications',
        'request_id': getattr(g, 'request_id', 'not set'),
        'custom_header': getattr(g, 'custom_header', 'not set'),
        'hooks_executed': [
            'before_request_1',
            'before_request_2', 
            'route_handler',
            'after_request_2',  # Note reverse order!
            'after_request_1'
        ]
    }
    
    response = jsonify(response_data)
    
    # You can also modify response in the route handler
    response.headers['X-Route-Handler'] = 'Modified in handler'
    
    return response


# ============================================================================
# SECTION 8: CONTEXT LOCALS DEEPER DIVE
# ============================================================================
"""
CONTEXT LOCALS: REQUEST CONTEXT VS APPLICATION CONTEXT

Understanding when contexts are created and destroyed:

1. REQUEST CONTEXT:
   - Created when: HTTP request starts
   - Destroyed when: Request ends (response sent)
   - Contains: request, session
   - Accessible via: flask.request, flask.session

2. APPLICATION CONTEXT:
   - Created when: First request comes in or manually via app.app_context()
   - Destroyed when: Request ends or app context popped
   - Contains: current_app, g
   - Accessible via: flask.current_app, flask.g

Key Points:
- g is NOT global across requests, only within a single request
- current_app is useful when you don't have direct access to app instance
- Contexts are automatically managed in web requests
- You can manually push/pop contexts for testing or CLI operations
"""

@app.route('/context-info')
def context_info():
    """
    Demonstrate context local objects and their behavior.
    """
    # ========================================================================
    # Demonstrate g object scope (request-bound)
    # ========================================================================
    if not hasattr(g, 'request_counter'):
        g.request_counter = 0
    g.request_counter += 1
    
    # ========================================================================
    # Access context information
    # ========================================================================
    context_data = {
        'request_context': {
            'request_method': request.method,
            'request_path': request.path,
            'session_keys': list(session.keys()),
            'session_id': session.get('user_id')
        },
        'application_context': {
            'app_name': current_app.name,
            'debug_mode': current_app.config['DEBUG'],
            'g_object': {
                'request_counter': g.request_counter,
                'request_id': getattr(g, 'request_id', 'not set')
            }
        },
        'note': 'g.request_counter resets to 0 on each new request'
    }
    
    return jsonify(context_data)


# ========================================================================
# Manual context manipulation example
# ========================================================================
def demonstrate_manual_contexts():
    """
    Demonstrate manual context creation and destruction.
    
    This is useful for:
    - Testing without running a server
    - CLI commands that need app context
    - Background tasks
    """
    print("\n=== MANUAL CONTEXT DEMONSTRATION ===")
    
    # Create an application context manually
    with app.app_context():
        # Now we can use current_app
        print(f"App name in context: {current_app.name}")
        print(f"Debug mode: {current_app.config['DEBUG']}")
        
        # We can also use g within this context
        g.demo_value = "Set in manual context"
        print(f"g.demo_value: {getattr(g, 'demo_value', 'not set')}")
    
    # Outside context, g is not accessible
    try:
        print(f"Outside context: {g.demo_value}")
    except Exception as e:
        print(f"Outside context (expected error): {type(e).__name__}")
    
    # Simulate a request context
    with app.test_request_context('/test-path?param=value'):
        print(f"\nIn test request context:")
        print(f"Request path: {request.path}")
        print(f"Query param: {request.args.get('param')}")
        
        # Set session in request context
        session['test'] = 'session value'
        print(f"Session value: {session.get('test')}")


# ============================================================================
# SECTION 9: ADVANCED ROUTING AND MIDDLEWARE PATTERNS
# ============================================================================
@app.route('/advanced/<regex("[a-z]{3}"):code>')
def regex_route(code: str):
    """
    Route with regex pattern (using custom converter pattern).
    
    Note: Flask doesn't have built-in regex converter,
    but you can create one or use this pattern.
    """
    return f'Three-letter code: {code}'

# ========================================================================
# Class-based views (using MethodView)
# ========================================================================
from flask.views import MethodView

class UserAPI(MethodView):
    """
    Class-based view for user operations.
    
    Demonstrates RESTful API pattern with different HTTP methods.
    """
    
    def get(self, user_id: Optional[int] = None):
        """GET /users or GET /users/<id>"""
        if user_id:
            return jsonify({'user': f'User {user_id}', 'method': 'GET'})
        return jsonify({'users': ['alice', 'bob'], 'method': 'GET'})
    
    def post(self):
        """POST /users"""
        data = request.get_json()
        return jsonify({'created': data, 'method': 'POST'}), 201
    
    def put(self, user_id: int):
        """PUT /users/<id>"""
        data = request.get_json()
        return jsonify({'updated': user_id, 'data': data, 'method': 'PUT'})
    
    def delete(self, user_id: int):
        """DELETE /users/<id>"""
        return jsonify({'deleted': user_id, 'method': 'DELETE'}), 204

# Register class-based view
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/users', defaults={'user_id': None}, 
                 view_func=user_view, methods=['GET'])
app.add_url_rule('/users', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, 
                 methods=['GET', 'PUT', 'DELETE'])


# ============================================================================
# SECTION 10: MAIN APPLICATION ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    """
    Main entry point when running this file directly.
    
    In production, you would use:
    - gunicorn: gunicorn app:app
    - waitress: waitress-serve --port=8000 app:app
    - uWSGI: uwsgi --http :8000 --module app:app
    """
    
    # Demonstrate manual contexts
    demonstrate_manual_contexts()
    
    # Run the Flask development server
    print("\n=== STARTING FLASK DEVELOPMENT SERVER ===")
    print(f"App name: {app.name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Available routes:")
    
    # List all registered routes
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} [{', '.join(rule.methods - {'OPTIONS', 'HEAD'})}]")
    
    print("\nAccess the following endpoints to see concepts in action:")
    print("  http://localhost:5000/")
    print("  http://localhost:5000/?name=YourName")
    print("  http://localhost:5000/context-info")
    print("  http://localhost:5000/hooks-demo")
    print("  http://localhost:5000/user/john")
    print("  http://localhost:5000/post/42")
    print("  http://localhost:5000/items/1,2,3,4")
    print("  http://localhost:5000/simulate-error/404")
    print("  http://localhost:5000/dashboard")
    print("  http://localhost:5000/users (GET, POST)")
    print("  http://localhost:5000/users/1 (GET, PUT, DELETE)")
    
    # Start the server
    app.run(host='0.0.0.0', port=5000, debug=True)


# ============================================================================
# SECTION 11: SUMMARY AND BEST PRACTICES
# ============================================================================
"""
FLASK CONCEPTS SUMMARY:

1. APPLICATION FACTORY (create_app):
   - Use for configurable, testable app creation
   - Essential for larger applications

2. BLUEPRINTS:
   - Organize large apps into modules
   - Use url_prefix for namespace separation
   - Each blueprint can have own templates/static files

3. REQUEST LIFECYCLE:
   - Contexts are created/destroyed automatically
   - Hooks execute in specific order
   - Response flows through hooks before returning

4. CONTEXT LOCALS:
   - request, session: Request Context (per HTTP request)
   - current_app, g: Application Context (per app instance)
   - g is NOT global, only per-request

5. ERROR HANDLING:
   - Use @app.errorhandler for custom error pages/responses
   - Can handle specific codes or all exceptions
   - Log exceptions appropriately

6. HOOKS:
   - before_request: Setup, authentication, logging
   - after_request: Modify responses, add headers
   - teardown_request: Cleanup resources
   - Note execution orders!

7. ROUTING:
   - Use converters for parameter validation
   - Create custom converters for complex patterns
   - Consider MethodView for RESTful APIs
   - Use url_for() for URL generation

BEST PRACTICES:
1. Always use application factory for production apps
2. Use blueprints for modularity
3. Keep route handlers focused and thin
4. Use hooks for cross-cutting concerns
5. Handle errors gracefully with appropriate responses
6. Use g for request-scoped data, not global variables
7. Test with different configurations
8. Use environment variables for sensitive config
"""