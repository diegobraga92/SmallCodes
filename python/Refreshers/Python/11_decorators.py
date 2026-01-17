"""
PYTHON DECORATORS: COMPREHENSIVE GUIDE
Covers function decorators, decorators with arguments, and common use cases.
"""

import time
import functools
from typing import Callable, Any, TypeVar, cast
import json
from datetime import datetime
import random
from functools import wraps

# Type variable for decorator typing
F = TypeVar('F', bound=Callable[..., Any])

print("=" * 60)
print("PYTHON DECORATORS")
print("=" * 60)
print("""
Decorators are functions that modify the behavior of other functions.
They are a powerful metaprogramming tool in Python.
""")

# ============================================================================
# PART 1: FUNDAMENTAL CONCEPTS
# ============================================================================

print("\n1. FUNCTION DECORATORS - BASIC CONCEPTS")
print("-" * 40)

# ============================================================================
# 1.1 What is a decorator?
# ============================================================================

print("\n1.1 What is a decorator?")
print("-" * 40)

def simple_decorator(func: F) -> F:
    """A basic decorator that adds behavior before and after function call."""
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After calling {func.__name__}")
        return result
    return cast(F, wrapper)

@simple_decorator
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

print("Basic decorator example:")
print(f"Result: {greet('Alice')}")

# What's really happening:
print("\nWhat @decorator syntax really does:")
print("""
@greet = simple_decorator(greet)

Is equivalent to:
greet = simple_decorator(greet)
""")

# ============================================================================
# 1.2 Decorator Chaining
# ============================================================================

print("\n1.2 Decorator Chaining")
print("-" * 40)

def uppercase_decorator(func: F) -> F:
    """Convert function result to uppercase."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return cast(F, wrapper)

def bold_decorator(func: F) -> F:
    """Wrap function result in bold tags."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"**{result}**"
    return cast(F, wrapper)

@bold_decorator
@uppercase_decorator
@simple_decorator
def get_message() -> str:
    """Get a message."""
    return "Python decorators are awesome!"

print("Chained decorators (applied bottom to top):")
print(f"Result: {get_message()}")

print("\nDecorator order matters!")
print("Applied as: bold(uppercase(simple(get_message)))")

# ============================================================================
# 1.3 Preserving Metadata with @wraps
# ============================================================================

print("\n1.3 Preserving Metadata with @wraps")
print("-" * 40)

def bad_decorator(func: F) -> F:
    """Decorator that loses function metadata."""
    def wrapper(*args, **kwargs):
        """Wrapper docstring."""
        return func(*args, **kwargs)
    return cast(F, wrapper)

def good_decorator(func: F) -> F:
    """Decorator that preserves function metadata using @wraps."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper docstring."""
        return func(*args, **kwargs)
    return cast(F, wrapper)

@bad_decorator
def function_with_metadata():
    """This function has important metadata."""
    return "Hello"

@good_decorator  
def better_function():
    """This function keeps its metadata."""
    return "World"

print("Without @wraps:")
print(f"  Name: {function_with_metadata.__name__}")
print(f"  Docstring: {function_with_metadata.__doc__}")

print("\nWith @wraps:")
print(f"  Name: {better_function.__name__}")
print(f"  Docstring: {better_function.__doc__}")

# ============================================================================
# PART 2: DECORATORS WITH ARGUMENTS
# ============================================================================

print("\n" + "=" * 60)
print("2. DECORATORS WITH ARGUMENTS")
print("=" * 60)

# ============================================================================
# 2.1 Decorator Factories
# ============================================================================

print("\n2.1 Decorator Factories")
print("-" * 40)

def repeat(n_times: int):
    """Decorator factory that repeats function call n times."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(n_times):
                print(f"Call {i + 1}/{n_times}")
                result = func(*args, **kwargs)
                results.append(result)
            return results[-1]  # Return last result
        return cast(F, wrapper)
    return decorator

@repeat(n_times=3)
def say_hello(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

print("Decorator with arguments (repeat 3 times):")
print(f"Result: {say_hello('Bob')}")

# ============================================================================
# 2.2 Flexible Decorator with Optional Arguments
# ============================================================================

print("\n2.2 Flexible Decorator with Optional Arguments")
print("-" * 40)

def flexible_decorator(func=None, *, prefix="[INFO]"):
    """Decorator that can be used with or without arguments."""
    if func is None:
        # Called with arguments: @flexible_decorator(prefix="[DEBUG]")
        return lambda f: flexible_decorator(f, prefix=prefix)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"{prefix} Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{prefix} {func.__name__} completed")
        return result
    
    return wrapper

# Usage 1: Without arguments
@flexible_decorator
def function_one():
    """Function with default decorator."""
    print("Inside function_one")

# Usage 2: With arguments
@flexible_decorator(prefix="[DEBUG]")
def function_two():
    """Function with customized decorator."""
    print("Inside function_two")

print("Flexible decorator examples:")
print("\nFunction with default prefix:")
function_one()

print("\nFunction with custom prefix:")
function_two()

# ============================================================================
# 2.3 Decorator with Multiple Arguments
# ============================================================================

print("\n2.3 Decorator with Multiple Arguments")
print("-" * 40)

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """Decorator that retries function on specified exceptions."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1}/{max_attempts} failed: {e}")
                    
                    if attempt < max_attempts - 1:
                        print(f"  Waiting {delay} seconds before retry...")
                        time.sleep(delay)
                    else:
                        print("  All attempts exhausted")
            
            raise last_exception
        
        return cast(F, wrapper)
    return decorator

# Simulate an unreliable API call
@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def unreliable_api_call():
    """Simulate an unreliable API call."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("API temporarily unavailable")
    return "API call successful!"

print("Retry decorator example:")
try:
    result = unreliable_api_call()
    print(f"Result: {result}")
except Exception as e:
    print(f"Failed after all attempts: {e}")

# ============================================================================
# PART 3: COMMON USE CASES
# ============================================================================

print("\n" + "=" * 60)
print("3. COMMON DECORATOR USE CASES")
print("=" * 60)

# ============================================================================
# 3.1 Logging Decorator
# ============================================================================

print("\n3.1 Logging Decorator")
print("-" * 40)

def log_execution(log_file: str = "execution.log", log_level: str = "INFO"):
    """Decorator that logs function execution details."""
    
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Log entry
            log_entry = {
                "timestamp": timestamp,
                "level": log_level,
                "function": func.__name__,
                "args": str(args),
                "kwargs": str(kwargs),
                "status": "started"
            }
            
            # Write to log file
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            print(f"[{log_level}] {timestamp} - {func.__name__} started")
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Log success
                success_entry = log_entry.copy()
                success_entry.update({
                    "status": "completed",
                    "result": str(result)
                })
                
                with open(log_file, 'a') as f:
                    f.write(json.dumps(success_entry) + '\n')
                
                print(f"[{log_level}] {timestamp} - {func.__name__} completed")
                return result
                
            except Exception as e:
                # Log error
                error_entry = log_entry.copy()
                error_entry.update({
                    "status": "failed",
                    "error": str(e)
                })
                
                with open(log_file, 'a') as f:
                    f.write(json.dumps(error_entry) + '\n')
                
                print(f"[ERROR] {timestamp} - {func.__name__} failed: {e}")
                raise
        
        return cast(F, wrapper)
    return decorator

# Create a temporary log file
import tempfile
temp_log = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log').name

@log_execution(log_file=temp_log, log_level="DEBUG")
def calculate_total(items: list, tax_rate: float = 0.1) -> float:
    """Calculate total with tax."""
    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax

print("Logging decorator example:")
result = calculate_total([10.99, 24.99, 5.99], tax_rate=0.08)
print(f"Total: ${result:.2f}")

# Show log file content
print(f"\nLog file content ({temp_log}):")
with open(temp_log, 'r') as f:
    for line in f:
        log_data = json.loads(line.strip())
        print(f"  {log_data['timestamp']} - {log_data['function']}: {log_data['status']}")

# Clean up
import os
os.unlink(temp_log)

# ============================================================================
# 3.2 Timing/Performance Decorator
# ============================================================================

print("\n3.2 Timing/Performance Decorator")
print("-" * 40)

def timer(print_result: bool = True, unit: str = "seconds"):
    """Decorator that measures function execution time."""
    
    # Convert unit to appropriate divisor
    units = {
        "seconds": 1,
        "milliseconds": 1000,
        "microseconds": 1000000,
        "nanoseconds": 1000000000
    }
    
    if unit not in units:
        raise ValueError(f"Unit must be one of: {', '.join(units.keys())}")
    
    divisor = units[unit]
    
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            
            result = func(*args, **kwargs)
            
            end_time = time.perf_counter()
            elapsed = (end_time - start_time) * divisor
            
            if print_result:
                print(f"{func.__name__} took {elapsed:.4f} {unit}")
                print(f"  Args: {args}")
                print(f"  Kwargs: {kwargs}")
                if result is not None:
                    print(f"  Result: {result}")
            
            # You could also store timing data
            wrapper.execution_times = getattr(wrapper, 'execution_times', [])
            wrapper.execution_times.append(elapsed)
            
            return result
        
        return cast(F, wrapper)
    return decorator

@timer(print_result=True, unit="milliseconds")
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number (inefficient recursive version)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Timing decorator example:")
print("Calculating Fibonacci(10) with timing:")
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")

# ============================================================================
# 3.3 Caching/Memoization Decorator
# ============================================================================

print("\n3.3 Caching/Memoization Decorator")
print("-" * 40)

def cache(max_size: int = 128):
    """Custom caching decorator with LRU eviction."""
    
    def decorator(func: F) -> F:
        cache_store = {}
        cache_order = []  # For LRU tracking
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = (
                args,
                tuple(sorted(kwargs.items())) if kwargs else ()
            )
            
            # Check cache
            if key in cache_store:
                # Move to end (most recently used)
                cache_order.remove(key)
                cache_order.append(key)
                wrapper.cache_hits = getattr(wrapper, 'cache_hits', 0) + 1
                return cache_store[key]
            
            # Cache miss - compute result
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_store[key] = result
            cache_order.append(key)
            wrapper.cache_misses = getattr(wrapper, 'cache_misses', 0) + 1
            
            # Evict if cache is full (LRU)
            if len(cache_store) > max_size:
                lru_key = cache_order.pop(0)
                del cache_store[lru_key]
                wrapper.cache_evictions = getattr(wrapper, 'cache_evictions', 0) + 1
            
            return result
        
        # Add cache info method
        def cache_info():
            return {
                'hits': getattr(wrapper, 'cache_hits', 0),
                'misses': getattr(wrapper, 'cache_misses', 0),
                'evictions': getattr(wrapper, 'cache_evictions', 0),
                'size': len(cache_store),
                'max_size': max_size
            }
        
        wrapper.cache_info = cache_info
        wrapper.clear_cache = lambda: (cache_store.clear(), cache_order.clear())
        
        return cast(F, wrapper)
    return decorator

@cache(max_size=5)
def expensive_calculation(x: int, y: int) -> int:
    """Simulate expensive calculation."""
    print(f"  Calculating {x} * {y}...")
    time.sleep(0.1)  # Simulate computation time
    return x * y

print("Caching decorator example:")
print("First calls (cache misses):")
print(f"  expensive_calculation(2, 3) = {expensive_calculation(2, 3)}")
print(f"  expensive_calculation(3, 4) = {expensive_calculation(3, 4)}")
print(f"  expensive_calculation(4, 5) = {expensive_calculation(4, 5)}")

print("\nRepeat calls (cache hits):")
print(f"  expensive_calculation(2, 3) = {expensive_calculation(2, 3)}")
print(f"  expensive_calculation(3, 4) = {expensive_calculation(3, 4)}")

print("\nCache info:")
info = expensive_calculation.cache_info()
for key, value in info.items():
    print(f"  {key}: {value}")

# ============================================================================
# 3.4 Authorization/Authentication Decorator
# ============================================================================

print("\n3.4 Authorization/Authentication Decorator")
print("-" * 40)

class User:
    """Simple user class for demonstration."""
    
    def __init__(self, username: str, roles: list, is_authenticated: bool = True):
        self.username = username
        self.roles = roles
        self.is_authenticated = is_authenticated

def require_auth(required_roles: list = None):
    """Decorator that requires authentication and authorization."""
    
    if required_roles is None:
        required_roles = []
    
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(user: User, *args, **kwargs):
            # Check authentication
            if not user.is_authenticated:
                raise PermissionError(f"User {user.username} is not authenticated")
            
            # Check authorization
            if required_roles:
                user_roles = set(user.roles)
                required_set = set(required_roles)
                
                if not user_roles.intersection(required_set):
                    raise PermissionError(
                        f"User {user.username} lacks required roles: {required_roles}"
                    )
            
            # User is authorized, execute function
            return func(user, *args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

# Example usage
@require_auth(required_roles=["admin", "editor"])
def delete_post(user: User, post_id: str) -> str:
    """Delete a post (requires admin or editor role)."""
    return f"Post {post_id} deleted by {user.username}"

@require_auth()  # Only requires authentication, no specific roles
def view_profile(user: User) -> str:
    """View user profile."""
    return f"Profile of {user.username}"

print("Authorization decorator example:")

# Create users
admin_user = User("admin_user", ["admin", "user"], is_authenticated=True)
regular_user = User("regular_user", ["user"], is_authenticated=True)
guest_user = User("guest", [], is_authenticated=False)

print("\n1. Admin deleting post:")
try:
    result = delete_post(admin_user, "post_123")
    print(f"  Success: {result}")
except PermissionError as e:
    print(f"  Failed: {e}")

print("\n2. Regular user trying to delete post:")
try:
    result = delete_post(regular_user, "post_123")
    print(f"  Success: {result}")
except PermissionError as e:
    print(f"  Failed: {e}")

print("\n3. Guest viewing profile:")
try:
    result = view_profile(guest_user)
    print(f"  Success: {result}")
except PermissionError as e:
    print(f"  Failed: {e}")

print("\n4. Regular user viewing profile:")
try:
    result = view_profile(regular_user)
    print(f"  Success: {result}")
except PermissionError as e:
    print(f"  Failed: {e}")

# ============================================================================
# 3.5 Validation Decorator
# ============================================================================

print("\n3.5 Validation Decorator")
print("-" * 40)

def validate_input(**validators):
    """
    Decorator that validates function arguments.
    
    Usage:
    @validate_input(
        x=lambda v: v > 0,
        y=lambda v: isinstance(v, str) and len(v) > 0
    )
    """
    
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Combine args and kwargs into a dict
            from inspect import signature
            
            sig = signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            arg_dict = bound_args.arguments
            
            # Validate each argument
            for arg_name, validator in validators.items():
                if arg_name in arg_dict:
                    value = arg_dict[arg_name]
                    
                    if not validator(value):
                        raise ValueError(
                            f"Invalid value for {arg_name}: {value}. "
                            f"Validation: {validator.__doc__ or 'custom check'}"
                        )
            
            # All validations passed
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

# Define some validators
def is_positive(x):
    """Check if value is positive."""
    return x > 0

def is_non_empty_string(s):
    """Check if string is non-empty."""
    return isinstance(s, str) and len(s.strip()) > 0

def is_valid_email(email):
    """Check if string looks like a valid email."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return isinstance(email, str) and re.match(pattern, email) is not None

@validate_input(
    amount=is_positive,
    recipient=is_non_empty_string,
    email=is_valid_email
)
def send_payment(amount: float, recipient: str, email: str, currency: str = "USD") -> str:
    """Send payment to recipient."""
    return f"Sent {amount} {currency} to {recipient} ({email})"

print("Validation decorator example:")

print("\n1. Valid input:")
try:
    result = send_payment(100.0, "Alice", "alice@example.com")
    print(f"  Success: {result}")
except ValueError as e:
    print(f"  Failed: {e}")

print("\n2. Invalid amount:")
try:
    result = send_payment(-50.0, "Bob", "bob@example.com")
    print(f"  Success: {result}")
except ValueError as e:
    print(f"  Failed: {e}")

print("\n3. Invalid email:")
try:
    result = send_payment(50.0, "Charlie", "invalid-email")
    print(f"  Success: {result}")
except ValueError as e:
    print(f"  Failed: {e}")

# ============================================================================
# 3.6 Rate Limiting Decorator
# ============================================================================

print("\n3.6 Rate Limiting Decorator")
print("-" * 40)

def rate_limit(max_calls: int, period: float):
    """
    Decorator that limits function calls to max_calls per period (in seconds).
    
    Args:
        max_calls: Maximum number of calls allowed in the period
        period: Time period in seconds
    """
    
    def decorator(func: F) -> F:
        call_times = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_times
            
            current_time = time.time()
            
            # Remove calls older than the period
            call_times = [t for t in call_times if current_time - t < period]
            
            # Check if we've exceeded the rate limit
            if len(call_times) >= max_calls:
                oldest_call = call_times[0]
                wait_time = period - (current_time - oldest_call)
                raise RuntimeError(
                    f"Rate limit exceeded. Try again in {wait_time:.2f} seconds. "
                    f"Limit: {max_calls} calls per {period} seconds"
                )
            
            # Record this call
            call_times.append(current_time)
            
            # Execute the function
            return func(*args, **kwargs)
        
        return cast(F, wrapper)
    return decorator

@rate_limit(max_calls=3, period=2.0)
def api_request(endpoint: str) -> str:
    """Simulate API request."""
    return f"Response from {endpoint}"

print("Rate limiting decorator example:")

print("Making 3 quick API calls (should succeed):")
for i in range(3):
    try:
        result = api_request(f"/api/data/{i}")
        print(f"  Call {i+1}: {result}")
    except RuntimeError as e:
        print(f"  Call {i+1}: {e}")

print("\nMaking 4th call immediately (should fail):")
try:
    result = api_request("/api/data/3")
    print(f"  Call 4: {result}")
except RuntimeError as e:
    print(f"  Call 4: {e}")

print("\nWaiting 2 seconds...")
time.sleep(2.1)

print("Trying again after wait (should succeed):")
try:
    result = api_request("/api/data/4")
    print(f"  After wait: {result}")
except RuntimeError as e:
    print(f"  After wait: {e}")

# ============================================================================
# PART 4: ADVANCED DECORATOR PATTERNS
# ============================================================================

print("\n" + "=" * 60)
print("4. ADVANCED DECORATOR PATTERNS")
print("=" * 60)

# ============================================================================
# 4.1 Class Decorators
# ============================================================================

print("\n4.1 Class Decorators")
print("-" * 40)

def singleton(cls):
    """Decorator that makes a class a singleton."""
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class DatabaseConnection:
    """Singleton database connection."""
    
    def __init__(self):
        print("  Creating new database connection...")
        self.connection_id = id(self)
    
    def query(self, sql: str) -> str:
        return f"Executing on connection {self.connection_id}: {sql}"

print("Singleton class decorator example:")
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"  db1 is db2: {db1 is db2}")
print(f"  db1.connection_id: {db1.connection_id}")
print(f"  db2.connection_id: {db2.connection_id}")
print(f"  db1.query('SELECT * FROM users'): {db1.query('SELECT * FROM users')}")

# ============================================================================
# 4.2 Method Decorators in Classes
# ============================================================================

print("\n4.2 Method Decorators in Classes")
print("-" * 40)

def class_method_decorator(func):
    """Decorator for class methods."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"  Calling {self.__class__.__name__}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class ShoppingCart:
    """Shopping cart with decorated methods."""
    
    def __init__(self):
        self.items = []
    
    @class_method_decorator
    def add_item(self, item: str, price: float):
        self.items.append((item, price))
        return f"Added {item} for ${price:.2f}"
    
    @class_method_decorator
    def get_total(self) -> float:
        return sum(price for _, price in self.items)
    
    @property
    @class_method_decorator
    def item_count(self):
        return len(self.items)

print("Method decorators in classes:")
cart = ShoppingCart()
print(f"  {cart.add_item('Laptop', 999.99)}")
print(f"  {cart.add_item('Mouse', 49.99)}")
print(f"  Total: ${cart.get_total():.2f}")
print(f"  Item count: {cart.item_count}")

# ============================================================================
# 4.3 Decorator with State
# ============================================================================

print("\n4.3 Decorator with State")
print("-" * 40)

def counter_decorator(func):
    """Decorator that counts function calls."""
    
    # Use function attributes to store state
    func.call_count = 0
    func.last_called = None
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func.call_count += 1
        func.last_called = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"  Call #{func.call_count} at {func.last_called}")
        return func(*args, **kwargs)
    
    # Add methods to access state
    def get_stats():
        return {
            'call_count': func.call_count,
            'last_called': func.last_called
        }
    
    wrapper.get_stats = get_stats
    wrapper.reset_counter = lambda: (setattr(func, 'call_count', 0), 
                                     setattr(func, 'last_called', None))
    
    return wrapper

@counter_decorator
def process_order(order_id: str) -> str:
    """Process an order."""
    return f"Order {order_id} processed"

print("Stateful decorator example:")
print(f"  First call: {process_order('123')}")
print(f"  Second call: {process_order('456')}")
print(f"  Third call: {process_order('789')}")

stats = process_order.get_stats()
print(f"\n  Statistics: {stats}")

process_order.reset_counter()
print("  Counter reset")

print(f"  After reset: {process_order('999')}")
print(f"  New stats: {process_order.get_stats()}")

# ============================================================================
# 4.4 Stackable Decorators with Dependencies
# ============================================================================

print("\n4.4 Stackable Decorators with Dependencies")
print("-" * 40)

def debug_decorator(func):
    """Add debug information."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] Entering {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[DEBUG] Exiting {func.__name__}")
        return result
    return wrapper

def timing_decorator(func):
    """Add timing information."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMING] {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

def logging_decorator(log_level="INFO"):
    """Add logging."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{log_level}] Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            print(f"[{log_level}] {func.__name__} returned: {result}")
            return result
        return wrapper
    return decorator

# Apply multiple decorators
@debug_decorator
@timing_decorator
@logging_decorator(log_level="INFO")
def complex_operation(x: int, y: int) -> int:
    """Perform a complex operation."""
    time.sleep(0.1)  # Simulate work
    return x ** y

print("Stackable decorators with dependencies:")
result = complex_operation(2, 8)
print(f"Result: {result}")

print("\nOrder of execution (decorators applied bottom to top):")
print("1. logging_decorator - logs inputs/outputs")
print("2. timing_decorator - measures execution time")
print("3. debug_decorator - adds debug entry/exit messages")

# ============================================================================
# 4.5 Decorator for Dependency Injection
# ============================================================================

print("\n4.5 Decorator for Dependency Injection")
print("-" * 40)

def inject_dependencies(**dependencies):
    """Decorator for dependency injection."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Inject dependencies into kwargs
            injected_kwargs = kwargs.copy()
            
            # Get function signature
            from inspect import signature, Parameter
            
            sig = signature(func)
            params = sig.parameters
            
            # Inject only dependencies that the function accepts
            for dep_name, dep_value in dependencies.items():
                if dep_name in params:
                    # Check if parameter already provided
                    param = params[dep_name]
                    
                    # Only inject if not already in args/kwargs
                    if (param.kind in (Parameter.POSITIONAL_OR_KEYWORD, 
                                      Parameter.KEYWORD_ONLY) and
                        dep_name not in kwargs):
                        
                        # Also check if it's not in positional args
                        param_index = list(params.keys()).index(dep_name)
                        if param_index >= len(args):
                            injected_kwargs[dep_name] = dep_value
            
            return func(*args, **injected_kwargs)
        
        return wrapper
    return decorator

# Simulate some services
class DatabaseService:
    def query(self, sql):
        return f"Database result: {sql}"

class EmailService:
    def send(self, to, subject):
        return f"Email sent to {to}: {subject}"

# Create service instances
db_service = DatabaseService()
email_service = EmailService()

@inject_dependencies(
    db=db_service,
    email=email_service,
    config={"debug": True, "timeout": 30}
)
def process_user_request(user_id: int, db=None, email=None, config=None) -> dict:
    """Process user request with injected dependencies."""
    result = {}
    
    if db:
        result['user_data'] = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    
    if email:
        result['notification'] = email.send(
            to=f"user{user_id}@example.com",
            subject="Your request was processed"
        )
    
    if config:
        result['config'] = config
    
    return result

print("Dependency injection decorator example:")
result = process_user_request(123)
print(f"Result: {result}")

# ============================================================================
# PART 5: BEST PRACTICES AND GOTCHAS
# ============================================================================

print("\n" + "=" * 60)
print("5. BEST PRACTICES AND GOTCHAS")
print("=" * 60)

# ============================================================================
# 5.1 Common Pitfalls
# ============================================================================

print("\n5.1 Common Pitfalls")
print("-" * 40)

print("Pitfall 1: Forgetting @wraps")
print("Without @wraps, decorated functions lose their metadata:")

def bad_wrapper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_wrapper
def documented_function():
    """This docstring will be lost."""
    pass

print(f"  Name without @wraps: {documented_function.__name__}")
print(f"  Docstring without @wraps: {documented_function.__doc__}")

print("\nPitfall 2: Decorator execution time")
print("Decorators execute when the function is defined, not when it's called:")

def decorator_with_print(func):
    print(f"  Decorating {func.__name__} (executes at definition time)")
    
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__} (executes at call time)")
        return func(*args, **kwargs)
    
    return wrapper

@decorator_with_print
def example_function():
    return "Hello"

print("\n  (Notice the 'Decorating' message appears above)")
print(f"  Now calling function: {example_function()}")

print("\nPitfall 3: Decorating methods")
print("When decorating methods, the first argument is 'self', not the function:")

def method_decorator(func):
    def wrapper(self, *args, **kwargs):
        print(f"  Method {func.__name__} called on {self.__class__.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class ExampleClass:
    @method_decorator
    def example_method(self):
        return "Method result"

print("\n  Creating instance and calling method:")
obj = ExampleClass()
print(f"  Result: {obj.example_method()}")

# ============================================================================
# 5.2 Testing Decorated Functions
# ============================================================================

print("\n5.2 Testing Decorated Functions")
print("-" * 40)

# The undecorated function is accessible via __wrapped__
# if @wraps was used

def testable_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  Decorator logic")
        return func(*args, **kwargs)
    return wrapper

@testable_decorator
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

print("Testing decorated functions:")
print(f"  Decorated function: {add(2, 3)}")

# Access original function for testing
if hasattr(add, '__wrapped__'):
    original_add = add.__wrapped__
    print(f"  Original function (via __wrapped__): {original_add(2, 3)}")
    print(f"  Original docstring: {original_add.__doc__}")

# ============================================================================
# 5.3 When to Use Decorators
# ============================================================================

print("\n5.3 When to Use Decorators")
print("-" * 40)

print("""
GOOD USE CASES FOR DECORATORS:

1. CROSS-CUTTING CONCERNS:
   • Logging
   • Timing/Profiling
   • Caching/Memoization
   • Rate limiting
   • Authentication/Authorization

2. BEHAVIOR MODIFICATION:
   • Retry logic
   • Input validation
   • Output transformation
   • Error handling
   • Circuit breakers

3. METAPROGRAMMING:
   • Registering functions
   • Creating APIs
   • Dependency injection
   • Aspect-oriented programming

WHEN TO AVOID DECORATORS:

1. SIMPLE FUNCTIONS:
   • If the decorator logic is trivial
   • When a simple if-statement would suffice

2. PERFORMANCE-CRITICAL CODE:
   • Each decorator adds a function call overhead
   • For tight loops, consider inlining the logic

3. COMPLEX BUSINESS LOGIC:
   • Don't hide important business logic in decorators
   • Decorators should handle concerns, not core logic

4. WHEN IT REDUCES READABILITY:
   • If the decorator makes code harder to understand
   • When debugging becomes difficult
""")

# ============================================================================
# 5.4 Performance Considerations
# ============================================================================

print("\n5.4 Performance Considerations")
print("-" * 40)

def noop_decorator(func):
    """A decorator that does nothing (for benchmarking)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Apply multiple no-op decorators
@noop_decorator
@noop_decorator
@noop_decorator
@noop_decorator
@noop_decorator
def simple_function(x):
    return x * 2

print("Performance impact of multiple decorators:")

import timeit

# Test without decorators
def undecorated(x):
    return x * 2

# Benchmark
decorated_time = timeit.timeit(
    'simple_function(10)',
    globals=globals(),
    number=100000
)

undecorated_time = timeit.timeit(
    'undecorated(10)',
    globals=globals(),
    number=100000
)

print(f"  5 decorators: {decorated_time:.4f} seconds")
print(f"  No decorators: {undecorated_time:.4f} seconds")
print(f"  Overhead: {(decorated_time/undecorated_time - 1) * 100:.1f}%")

print("\nFor performance-critical code:")
print("1. Minimize number of decorators")
print("2. Keep decorator logic simple")
print("3. Consider using functools.lru_cache directly")
print("4. Profile before optimizing")

# ============================================================================
# COMPREHENSIVE REAL-WORLD EXAMPLE
# ============================================================================

print("\n" + "=" * 60)
print("COMPREHENSIVE REAL-WORLD EXAMPLE: API ENDPOINT")
print("=" * 60)

def create_api_endpoint():
    """Demonstrate a real-world API endpoint with multiple decorators."""
    
    # Simulated user database
    users_db = {
        "alice": {"password": "secret123", "roles": ["user", "admin"]},
        "bob": {"password": "password456", "roles": ["user"]},
        "charlie": {"password": "test789", "roles": ["user", "editor"]}
    }
    
    # Simulated rate limit store
    rate_limit_store = {}
    
    # 1. Authentication decorator
    def authenticate(func):
        @wraps(func)
        def wrapper(username, password, *args, **kwargs):
            if username not in users_db:
                raise PermissionError(f"User {username} not found")
            
            if users_db[username]["password"] != password:
                raise PermissionError("Invalid password")
            
            # Create user object
            user = type('User', (), {
                'username': username,
                'roles': users_db[username]["roles"],
                'is_authenticated': True
            })()
            
            return func(user, *args, **kwargs)
        return wrapper
    
    # 2. Rate limiting decorator
    def api_rate_limit(max_calls=10, period=60):
        def decorator(func):
            @wraps(func)
            def wrapper(user, *args, **kwargs):
                key = f"{func.__name__}:{user.username}"
                current_time = time.time()
                
                # Initialize or clean up old calls
                if key not in rate_limit_store:
                    rate_limit_store[key] = []
                
                rate_limit_store[key] = [
                    t for t in rate_limit_store[key] 
                    if current_time - t < period
                ]
                
                # Check limit
                if len(rate_limit_store[key]) >= max_calls:
                    raise RuntimeError(
                        f"Rate limit exceeded for {user.username}. "
                        f"Limit: {max_calls} calls per {period} seconds"
                    )
                
                # Record call
                rate_limit_store[key].append(current_time)
                
                return func(user, *args, **kwargs)
            return wrapper
        return decorator
    
    # 3. Logging decorator
    def api_logger(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[API] {timestamp} - {user.username} called {func.__name__}")
            
            try:
                result = func(user, *args, **kwargs)
                print(f"[API] {timestamp} - {func.__name__} succeeded")
                return result
            except Exception as e:
                print(f"[API] {timestamp} - {func.__name__} failed: {e}")
                raise
        return wrapper
    
    # 4. Authorization decorator
    def require_role(required_role):
        def decorator(func):
            @wraps(func)
            def wrapper(user, *args, **kwargs):
                if required_role not in user.roles:
                    raise PermissionError(
                        f"User {user.username} lacks required role: {required_role}"
                    )
                return func(user, *args, **kwargs)
            return wrapper
        return decorator
    
    # Apply all decorators to API endpoint
    @api_logger
    @api_rate_limit(max_calls=5, period=30)
    @authenticate
    @require_role("admin")
    def delete_user(admin_user, target_username):
        """Delete a user (admin only)."""
        if target_username not in users_db:
            raise ValueError(f"User {target_username} not found")
        
        # Simulate deletion
        del users_db[target_username]
        return f"User {target_username} deleted by {admin_user.username}"
    
    # Test the API endpoint
    print("Testing API endpoint with all decorators:")
    
    print("\n1. Valid admin request:")
    try:
        result = delete_user("alice", "secret123", "charlie")
        print(f"  Success: {result}")
    except Exception as e:
        print(f"  Failed: {e}")
    
    print("\n2. Non-admin user (should fail):")
    try:
        result = delete_user("bob", "password456", "charlie")
        print(f"  Success: {result}")
    except Exception as e:
        print(f"  Failed: {e}")
    
    print("\n3. Rate limit test (making multiple calls):")
    for i in range(6):  # Try 6 calls with limit of 5
        try:
            result = delete_user("alice", "secret123", "test_user")
            print(f"  Call {i+1}: Success")
        except Exception as e:
            print(f"  Call {i+1}: Failed - {e}")

create_api_endpoint()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("DECORATORS: KEY TAKEAWAYS")
print("=" * 60)

summary = """
1. CORE CONCEPTS:
   • Decorators are functions that modify other functions
   • @decorator syntax is syntactic sugar for func = decorator(func)
   • Always use @wraps to preserve function metadata
   • Decorators are applied from bottom to top

2. DECORATORS WITH ARGUMENTS:
   • Use decorator factories (function that returns decorator)
   • Can have optional arguments with flexible syntax
   • Can validate and transform inputs

3. COMMON USE CASES:
   • LOGGING: Track function calls and results
   • TIMING: Measure execution performance
   • CACHING: Store results for repeated calls
   • AUTHENTICATION: Verify user identity
   • AUTHORIZATION: Check user permissions
   • VALIDATION: Verify input parameters
   • RATE LIMITING: Control call frequency
   • RETRY LOGIC: Handle temporary failures

4. ADVANCED PATTERNS:
   • CLASS DECORATORS: Modify class behavior
   • METHOD DECORATORS: Decorate class methods
   • STATEFUL DECORATORS: Maintain state between calls
   • STACKABLE DECORATORS: Combine multiple concerns
   • DEPENDENCY INJECTION: Inject services automatically

5. BEST PRACTICES:
   • Keep decorators focused on a single concern
   • Document what your decorator does
   • Consider performance overhead
   • Make decorators testable
   • Use type hints for better IDE support
   • Handle exceptions appropriately

6. WHEN TO USE:
   • For cross-cutting concerns
   • When you need to apply the same logic to many functions
   • For aspect-oriented programming patterns
   • When building frameworks or libraries

7. WHEN TO AVOID:
   • When it makes code harder to understand
   • For simple, one-off logic
   • In performance-critical inner loops
   • When business logic should be explicit

REMEMBER: Decorators are a powerful tool, but with great power comes
great responsibility. Use them judiciously to make your code cleaner,
more maintainable, and more expressive.
"""

print(summary)