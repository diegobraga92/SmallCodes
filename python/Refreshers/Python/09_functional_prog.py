"""
FUNCTIONAL PROGRAMMING IN PYTHON
Covers lambda functions, map/filter/reduce, functools, and decorators.
"""

from functools import reduce, partial, lru_cache, wraps
from typing import List, Callable, Any, Dict, Tuple
import time
import math

# ============================================================================
# PART 1: LAMBDA FUNCTIONS
# ============================================================================

print("=" * 60)
print("LAMBDA FUNCTIONS")
print("=" * 60)
print("""
Lambda functions are anonymous, single-expression functions.
Syntax: lambda arguments: expression
Use when you need a simple function for a short period.
""")

# ============================================================================
# 1. BASIC LAMBDA FUNCTIONS
# ============================================================================

print("\n1. BASIC LAMBDA FUNCTIONS")
print("-" * 40)

# Regular function
def add_regular(x, y):
    return x + y

# Equivalent lambda function
add_lambda = lambda x, y: x + y

print(f"Regular function add(3, 5): {add_regular(3, 5)}")
print(f"Lambda function add(3, 5): {add_lambda(3, 5)}")

# Lambda functions are anonymous - they don't have a name
# But we can assign them to variables (like above)

# ============================================================================
# 2. COMMON USE CASES FOR LAMBDA
# ============================================================================

print("\n2. COMMON USE CASES FOR LAMBDA")
print("-" * 40)

# Example 1: Simple mathematical operations
square = lambda x: x ** 2
is_even = lambda x: x % 2 == 0
get_length = lambda s: len(s)

print(f"square(5): {square(5)}")
print(f"is_even(4): {is_even(4)}")
print(f"is_even(7): {is_even(7)}")
print(f"get_length('hello'): {get_length('hello')}")

# Example 2: Sorting with custom keys
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Sort by age using lambda
sorted_by_age = sorted(people, key=lambda person: person["age"])
print(f"\nPeople sorted by age: {sorted_by_age}")

# Sort by name length
sorted_by_name_length = sorted(people, key=lambda p: len(p["name"]))
print(f"People sorted by name length: {sorted_by_name_length}")

# Example 3: Inline operations
numbers = [1, 2, 3, 4, 5]
# Immediately invoked lambda
result = (lambda x, y: x * y)(10, 20)
print(f"\nImmediately invoked lambda: (lambda x, y: x * y)(10, 20) = {result}")

# ============================================================================
# 3. LAMBDA WITH DEFAULT ARGUMENTS AND *args, **kwargs
# ============================================================================

print("\n3. LAMBDA WITH DEFAULT ARGUMENTS")
print("-" * 40)

# Lambda with default argument
greet = lambda name, greeting="Hello": f"{greeting}, {name}!"
print(f"greet('Alice'): {greet('Alice')}")
print(f"greet('Bob', 'Hi'): {greet('Bob', 'Hi')}")

# Lambda with *args (variable number of arguments)
sum_all = lambda *args: sum(args)
print(f"sum_all(1, 2, 3, 4, 5): {sum_all(1, 2, 3, 4, 5)}")

# Lambda with **kwargs (keyword arguments)
build_dict = lambda **kwargs: kwargs
print(f"build_dict(name='Alice', age=30): {build_dict(name='Alice', age=30)}")

# ============================================================================
# 4. LAMBDA LIMITATIONS
# ============================================================================

print("\n4. LAMBDA LIMITATIONS")
print("-" * 40)
print("""
Lambda functions have limitations:
1. Only one expression (no multiple statements)
2. No type annotations in Python < 3.6
3. Harder to debug (no function name in tracebacks)
4. Can't have docstrings

When to use regular functions instead:
1. Complex logic with multiple steps
2. Need docstrings for documentation
3. Function will be reused frequently
4. Need to debug with meaningful names
""")

# Example showing limitation
try:
    # This won't work - lambda can't have multiple expressions
    complex_logic = lambda x: (
        print(f"Processing {x}"),  # This is a statement
        x * 2                     # This would be the return, but comma creates tuple
    )
    print("Trying complex lambda...")
    result = complex_logic(5)
    print(f"Result: {result}")
except Exception as e:
    print(f"Cannot create complex lambda: {type(e).__name__}")

# ============================================================================
# PART 2: MAP, FILTER, REDUCE
# ============================================================================

print("\n" + "=" * 60)
print("MAP, FILTER, REDUCE")
print("=" * 60)
print("""
These are higher-order functions that operate on iterables.
They are fundamental to functional programming.
""")

# ============================================================================
# 1. MAP FUNCTION
# ============================================================================

print("\n1. MAP FUNCTION")
print("-" * 40)
print("""
map(function, iterable, ...)
Applies a function to every item in an iterable.
Returns a map object (iterator).
""")

# Example 1: Basic map with lambda
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print(f"Numbers: {numbers}")
print(f"Squared (map object): {squared}")
print(f"Squared (as list): {list(squared)}")

# Example 2: Map with multiple iterables
list1 = [1, 2, 3]
list2 = [10, 20, 30]
list3 = [100, 200, 300]

# Add corresponding elements
sums = map(lambda x, y, z: x + y + z, list1, list2, list3)
print(f"\nList1: {list1}, List2: {list2}, List3: {list3}")
print(f"Sum of corresponding elements: {list(sums)}")

# Example 3: Map with built-in functions
strings = ["hello", "world", "python"]
lengths = map(len, strings)
print(f"\nStrings: {strings}")
print(f"Lengths: {list(lengths)}")

# Example 4: Map vs List Comprehension (alternative)
numbers = [1, 2, 3, 4, 5]
print("\nMap vs List Comprehension:")
print(f"Using map: {list(map(lambda x: x * 2, numbers))}")
print(f"Using list comprehension: {[x * 2 for x in numbers]}")

# ============================================================================
# 2. FILTER FUNCTION
# ============================================================================

print("\n\n2. FILTER FUNCTION")
print("-" * 40)
print("""
filter(function or None, iterable)
Filters items where function returns True.
If function is None, filters out falsy values.
Returns a filter object (iterator).
""")

# Example 1: Basic filter with lambda
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(f"Numbers: {numbers}")
print(f"Even numbers: {list(even_numbers)}")

# Example 2: Filter with None (removes falsy values)
mixed_values = [0, 1, False, True, "", "hello", [], [1, 2], None, 42]
truthy_values = filter(None, mixed_values)
print(f"\nMixed values: {mixed_values}")
print(f"Truthy values: {list(truthy_values)}")

# Example 3: Filter with complex condition
words = ["apple", "banana", "cherry", "date", "elderberry", "fig"]
long_words = filter(lambda w: len(w) > 5 and 'a' in w, words)
print(f"\nWords: {words}")
print(f"Long words containing 'a': {list(long_words)}")

# Example 4: Filter vs List Comprehension
numbers = [1, 2, 3, 4, 5, 6]
print("\nFilter vs List Comprehension:")
print(f"Using filter: {list(filter(lambda x: x > 3, numbers))}")
print(f"Using list comprehension: {[x for x in numbers if x > 3]}")

# ============================================================================
# 3. REDUCE FUNCTION
# ============================================================================

print("\n\n3. REDUCE FUNCTION")
print("-" * 40)
print("""
reduce(function, iterable[, initial])
Applies function cumulatively to items of iterable.
function takes two arguments.
Returns a single value.
""")

# Example 1: Basic reduce - sum of numbers
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(f"Numbers: {numbers}")
print(f"Sum using reduce: {total}")

# Example 2: Reduce with initial value
product = reduce(lambda x, y: x * y, numbers, 1)
print(f"Product using reduce (with initial 1): {product}")

# Example 3: Complex reduce - find maximum
max_number = reduce(lambda x, y: x if x > y else y, numbers)
print(f"Maximum number: {max_number}")

# Example 4: Reduce for string concatenation
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda x, y: x + y, words)
print(f"\nWords: {words}")
print(f"Concatenated: '{sentence}'")

# Example 5: Reduce for custom aggregation
data = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

# Calculate average score
total_score = reduce(lambda acc, item: acc + item["score"], data, 0)
average_score = total_score / len(data)
print(f"\nStudent data: {data}")
print(f"Average score: {average_score:.2f}")

# ============================================================================
# 4. COMBINING MAP, FILTER, REDUCE
# ============================================================================

print("\n\n4. COMBINING MAP, FILTER, REDUCE")
print("-" * 40)

# Problem: Calculate sum of squares of even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Step-by-step approach
step1 = filter(lambda x: x % 2 == 0, numbers)  # Get even numbers
step2 = map(lambda x: x ** 2, step1)           # Square them
step3 = reduce(lambda x, y: x + y, step2, 0)   # Sum them

# All in one (harder to read)
result = reduce(
    lambda x, y: x + y,
    map(
        lambda x: x ** 2,
        filter(lambda x: x % 2 == 0, numbers)
    ),
    0
)

print(f"Numbers: {numbers}")
print(f"Sum of squares of even numbers (step-by-step): {step3}")
print(f"Sum of squares of even numbers (one-liner): {result}")

# ============================================================================
# 5. PERFORMANCE CONSIDERATIONS
# ============================================================================

print("\n\n5. PERFORMANCE CONSIDERATIONS")
print("-" * 40)
print("""
Map/Filter vs List Comprehensions:
• Map/Filter: Return iterators (lazy evaluation, memory efficient)
• List Comprehensions: Create lists immediately (eager evaluation)

Generator Expressions: Best of both worlds - lazy like map/filter, 
syntax like list comprehensions.
""")

import time

# Performance comparison
large_list = list(range(1000000))

print("\nTiming different approaches (sum of squares):")

# Method 1: For loop
start = time.time()
total = 0
for x in large_list:
    total += x ** 2
end = time.time()
print(f"For loop: {end - start:.4f} seconds")

# Method 2: List comprehension
start = time.time()
total = sum([x ** 2 for x in large_list])
end = time.time()
print(f"List comprehension: {end - start:.4f} seconds")

# Method 3: Generator expression
start = time.time()
total = sum(x ** 2 for x in large_list)
end = time.time()
print(f"Generator expression: {end - start:.4f} seconds")

# Method 4: Map
start = time.time()
total = sum(map(lambda x: x ** 2, large_list))
end = time.time()
print(f"Map with lambda: {end - start:.4f} seconds")

print("\nKey Insight: Generator expressions are often the most efficient!")

# ============================================================================
# PART 3: FUNCTOOLS MODULE
# ============================================================================

print("\n" + "=" * 60)
print("FUNCTOOLS MODULE")
print("=" * 60)
print("""
The functools module provides higher-order functions and operations 
on callable objects.
""")

# ============================================================================
# 1. PARTIAL FUNCTIONS
# ============================================================================

print("\n1. PARTIAL FUNCTIONS")
print("-" * 40)
print("""
partial(func, *args, **kwargs)
Creates a new function with some arguments pre-filled.
Useful for creating specialized versions of general functions.
""")

# Example 1: Basic partial function
def power(base, exponent):
    """Return base raised to exponent."""
    return base ** exponent

# Create specialized functions using partial
square = partial(power, exponent=2)      # Always square
cube = partial(power, exponent=3)        # Always cube
root = partial(power, exponent=0.5)      # Always square root

print(f"Original function: power(2, 3) = {power(2, 3)}")
print(f"Partial square(5): {square(5)}")      # 5² = 25
print(f"Partial cube(3): {cube(3)}")          # 3³ = 27
print(f"Partial root(16): {root(16):.2f}")    # √16 = 4

# Example 2: Partial with multiple fixed arguments
def greet(greeting, name, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

hello_greet = partial(greet, "Hello")               # Fixed greeting
hello_excited = partial(greet, "Hello", punctuation="!!!")  # Fixed greeting and punctuation

print(f"\nOriginal: {greet('Hi', 'Alice', '?')}")
print(f"Partial 1: {hello_greet('Bob')}")
print(f"Partial 2: {hello_excited('Charlie')}")

# Example 3: Partial with keyword arguments
def connect_to_database(host, port, username, password, database):
    """Simulate database connection."""
    return f"Connected to {database} on {host}:{port} as {username}"

# Create pre-configured connection functions
connect_local = partial(
    connect_to_database,
    host="localhost",
    port=5432,
    username="admin"
)

connect_prod = partial(
    connect_to_database,
    host="prod-db.example.com",
    port=5432,
    username="readonly"
)

print(f"\nLocal connection: {connect_local(password='secret', database='mydb')}")
print(f"Prod connection: {connect_prod(password='readonly_pass', database='analytics')}")

# ============================================================================
# 2. LRU_CACHE (LEAST RECENTLY USED CACHE)
# ============================================================================

print("\n\n2. LRU_CACHE DECORATOR")
print("-" * 40)
print("""
@lru_cache(maxsize=None, typed=False)
Memoization decorator that caches function results.
Improves performance for expensive, pure functions.
maxsize: Maximum cache size (None = unlimited)
typed: Cache arguments of different types separately
""")

# Example 1: Fibonacci with and without cache
def fibonacci_naive(n):
    """Naive recursive Fibonacci - very slow!"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

@lru_cache(maxsize=None)
def fibonacci_cached(n):
    """Cached recursive Fibonacci - much faster!"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

print("Calculating Fibonacci(35):")
start = time.time()
result_naive = fibonacci_naive(35)
end = time.time()
print(f"Naive version: {result_naive} (took {end - start:.2f} seconds)")

start = time.time()
result_cached = fibonacci_cached(35)
end = time.time()
print(f"Cached version: {result_cached} (took {end - start:.4f} seconds)")

# Example 2: Expensive computation
@lru_cache(maxsize=128)
def expensive_computation(x, y):
    """Simulate expensive computation."""
    time.sleep(0.1)  # Simulate slow computation
    return x * y + x ** 2 + y ** 2

print("\nTesting expensive computation (first call is slow, subsequent are fast):")
print("Call 1...")
result1 = expensive_computation(5, 10)
print(f"Result: {result1}")

print("Call 2 (should be cached)...")
result2 = expensive_computation(5, 10)
print(f"Result: {result2}")

print("Call 3 (different arguments)...")
result3 = expensive_computation(10, 20)
print(f"Result: {result3}")

# Show cache info
print(f"\nCache info: {expensive_computation.cache_info()}")

# Example 3: Cache with typed=True
@lru_cache(maxsize=None, typed=True)
def process_value(value):
    """Process value - cache integers and floats separately."""
    return value * 2

print("\nWith typed=True, 1 and 1.0 are cached separately:")
print(f"process_value(1) = {process_value(1)}")
print(f"process_value(1.0) = {process_value(1.0)}")
print(f"Cache hits: {process_value.cache_info().hits}")
print(f"Cache misses: {process_value.cache_info().misses}")

# ============================================================================
# 3. OTHER FUNCTOOLS UTILITIES
# ============================================================================

print("\n\n3. OTHER FUNCTOOLS UTILITIES")
print("-" * 40)

# wraps - helps create better decorators (covered in decorators section)

# total_ordering - generates missing comparison methods
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        return self.grade == other.grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    
    def __repr__(self):
        return f"Student(name='{self.name}', grade={self.grade})"

print("total_ordering example:")
alice = Student("Alice", 85)
bob = Student("Bob", 92)
charlie = Student("Charlie", 85)

print(f"alice == charlie: {alice == charlie}")
print(f"alice < bob: {alice < bob}")
print(f"alice <= charlie: {alice <= charlie}")  # Generated by total_ordering
print(f"alice > bob: {alice > bob}")            # Generated by total_ordering

# ============================================================================
# PART 4: DECORATORS
# ============================================================================

print("\n" + "=" * 60)
print("DECORATORS")
print("=" * 60)
print("""
Decorators are functions that modify the behavior of other functions.
They are a form of metaprogramming.
Syntax: @decorator_name above function definition.
""")

# ============================================================================
# 1. BASIC DECORATOR CONCEPT
# ============================================================================

print("\n1. BASIC DECORATOR CONCEPT")
print("-" * 40)

# A decorator is just a function that takes a function and returns a function
def simple_decorator(func):
    """A simple decorator that prints before and after function call."""
    def wrapper():
        print("Before function call")
        result = func()
        print("After function call")
        return result
    return wrapper

# Using the decorator
@simple_decorator
def say_hello():
    print("Hello, World!")

print("Calling decorated function:")
say_hello()

# What's really happening (decorator syntax is just syntactic sugar):
print("\nWhat's happening behind the scenes:")
def say_hi():
    print("Hi!")

decorated_say_hi = simple_decorator(say_hi)
print("Manual decoration:")
decorated_say_hi()

# ============================================================================
# 2. DECORATORS WITH ARGUMENTS
# ============================================================================

print("\n\n2. DECORATORS WITH ARGUMENTS")
print("-" * 40)

# Decorator that accepts arguments
def repeat(n_times):
    """Decorator that repeats function call n_times."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n_times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(n_times=3)
def greet(name):
    return f"Hello, {name}!"

print(f"Repeated greeting: {greet('Alice')}")

# ============================================================================
# 3. DECORATORS FOR FUNCTIONS WITH ARGUMENTS
# ============================================================================

print("\n\n3. DECORATORS FOR FUNCTIONS WITH ARGUMENTS")
print("-" * 40)

def debug_decorator(func):
    """Decorator that prints function arguments and return value."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@debug_decorator
def add(a, b):
    return a + b

@debug_decorator
def multiply(x, y, z=1):
    return x * y * z

print("Debugging function calls:")
print(f"add(3, 5): {add(3, 5)}")
print(f"\nmultiply(2, 3, z=4): {multiply(2, 3, z=4)}")

# ============================================================================
# 4. USING @wraps TO PRESERVE FUNCTION METADATA
# ============================================================================

print("\n\n4. USING @wraps TO PRESERVE FUNCTION METADATA")
print("-" * 40)
print("""
Without @wraps, decorated functions lose their name, docstring, etc.
@wraps(func) copies metadata from original function to wrapper.
""")

def bad_decorator(func):
    """Decorator that doesn't preserve metadata."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def good_decorator(func):
    """Decorator that preserves metadata using @wraps."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def function_with_metadata():
    """This is a documented function."""
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
# 5. PRACTICAL DECORATOR EXAMPLES
# ============================================================================

print("\n\n5. PRACTICAL DECORATOR EXAMPLES")
print("-" * 40)

# Example 1: Timing decorator
def timer(func):
    """Decorator that measures function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    """Simulate a slow function."""
    time.sleep(0.5)
    return "Done"

print("Timing function execution:")
result = slow_function()
print(f"Result: {result}")

# Example 2: Retry decorator
def retry(max_attempts=3, delay=1):
    """Decorator that retries function on exception."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    """Function that fails 2 times before succeeding."""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ValueError("Temporary failure")
    return "Success!"

print("\nRetry decorator example:")
try:
    result = unreliable_function()
    print(f"Result: {result}")
except Exception as e:
    print(f"Failed after all attempts: {e}")

# Example 3: Validation decorator
def validate_input(validator):
    """Decorator that validates function input."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validator(*args, **kwargs):
                raise ValueError("Invalid input")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_positive(a, b):
    """Validator that checks if both arguments are positive."""
    return a > 0 and b > 0

@validate_input(is_positive)
def divide(a, b):
    """Divide a by b."""
    return a / b

print("\nValidation decorator example:")
try:
    print(f"divide(10, 2) = {divide(10, 2)}")
    print(f"divide(-5, 2) = {divide(-5, 2)}")  # This should fail
except ValueError as e:
    print(f"Error: {e}")

# Example 4: Memoization decorator (manual implementation)
def memoize(func):
    """Manual memoization decorator."""
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a key from arguments
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        
        return cache[key]
    
    # Add cache info to wrapper
    wrapper.cache_info = lambda: f"Cache size: {len(cache)}"
    wrapper.clear_cache = lambda: cache.clear()
    
    return wrapper

@memoize
def expensive_operation(x):
    """Simulate expensive operation."""
    print(f"Computing expensive_operation({x})...")
    time.sleep(0.1)
    return x * x

print("\nManual memoization decorator:")
print(f"First call: {expensive_operation(5)}")
print(f"Second call (cached): {expensive_operation(5)}")
print(f"Different argument: {expensive_operation(10)}")
print(f"Cache info: {expensive_operation.cache_info()}")

# ============================================================================
# 6. CLASS DECORATORS
# ============================================================================

print("\n\n6. CLASS DECORATORS")
print("-" * 40)

def singleton(cls):
    """Decorator that makes a class a singleton."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        print("Creating new database connection...")
        self.connected = True
    
    def query(self, sql):
        return f"Executing: {sql}"

print("Singleton decorator example:")
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"db1 is db2: {db1 is db2}")
print(f"db1.query('SELECT * FROM users'): {db1.query('SELECT * FROM users')}")

# ============================================================================
# 7. DECORATOR FACTORY PATTERN
# ============================================================================

print("\n\n7. DECORATOR FACTORY PATTERN")
print("-" * 40)

def decorator_factory(prefix="[LOG]"):
    """Factory that creates decorators with configurable prefix."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{prefix} Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"{prefix} {func.__name__} completed")
            return result
        return wrapper
    return decorator

@decorator_factory("[INFO]")
def process_data(data):
    """Process some data."""
    return [x * 2 for x in data]

@decorator_factory("[DEBUG]")
def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    return a + b

print("Decorator factory example:")
print(f"process_data([1, 2, 3]): {process_data([1, 2, 3])}")
print(f"\ncalculate_sum(10, 20): {calculate_sum(10, 20)}")

# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY AND BEST PRACTICES")
print("=" * 60)

summary = """
FUNCTIONAL PROGRAMMING IN PYTHON:

1. LAMBDA FUNCTIONS:
   • Use for simple, one-expression functions
   • Great for sorting keys and short callbacks
   • Avoid for complex logic - use regular functions instead

2. MAP, FILTER, REDUCE:
   • Map: Transform each element
   • Filter: Select elements that meet criteria
   • Reduce: Aggregate elements to single value
   • Consider generator expressions for memory efficiency

3. FUNCTOOLS MODULE:
   • partial: Create specialized functions
   • lru_cache: Memoization for performance
   • wraps: Preserve metadata in decorators
   • total_ordering: Generate comparison methods

4. DECORATORS:
   • Use @wraps to preserve function metadata
   • Decorators can accept arguments (decorator factories)
   • Useful for cross-cutting concerns:
     - Logging
     - Timing
     - Caching
     - Validation
     - Retry logic
     - Authorization

BEST PRACTICES:
1. Use list comprehensions/generator expressions when they're more readable
2. Use functools.lru_cache for expensive pure functions
3. Always use @wraps in decorators
4. Keep decorators simple and focused
5. Document what your decorators do
6. Consider performance implications of functional chains

WHEN TO USE FUNCTIONAL PROGRAMMING:
1. Data transformation pipelines
2. When you need immutability
3. Parallel processing (functional code is easier to parallelize)
4. When operations are mathematical or data-oriented

WHEN TO USE OBJECT-ORIENTED PROGRAMMING:
1. When you need to maintain state
2. For complex business logic with multiple behaviors
3. When you need polymorphism
4. For GUI applications and frameworks

PYTHON IS MULTI-PARADIGM:
The best approach often combines functional and object-oriented techniques!
"""

print(summary)

# ============================================================================
# FINAL COMPREHENSIVE EXAMPLE
# ============================================================================

print("\n" + "=" * 60)
print("FINAL COMPREHENSIVE EXAMPLE")
print("=" * 60)

def pipeline_example():
    """Demonstrate a complete functional pipeline."""
    
    # Data source
    transactions = [
        {"id": 1, "amount": 100.50, "currency": "USD", "status": "completed"},
        {"id": 2, "amount": 200.75, "currency": "EUR", "status": "pending"},
        {"id": 3, "amount": 50.25, "currency": "USD", "status": "completed"},
        {"id": 4, "amount": 300.00, "currency": "GBP", "status": "failed"},
        {"id": 5, "amount": 150.00, "currency": "USD", "status": "completed"},
        {"id": 6, "amount": 75.50, "currency": "EUR", "status": "completed"},
    ]
    
    # Exchange rates
    exchange_rates = {"USD": 1.0, "EUR": 1.1, "GBP": 1.3}
    
    # Decorator for logging pipeline steps
    def log_step(step_name):
        def decorator(func):
            @wraps(func)
            def wrapper(data):
                print(f"{step_name}: Processing {len(data)} items")
                result = func(data)
                print(f"{step_name}: Result has {len(result)} items")
                return result
            return wrapper
        return decorator
    
    # Pipeline steps using functional programming
    
    @log_step("1. Filter completed")
    @lru_cache(maxsize=1)  # Cache the filtering since it's called multiple times
    def filter_completed(transactions):
        return list(filter(lambda t: t["status"] == "completed", transactions))
    
    @log_step("2. Convert to USD")
    def convert_to_usd(transactions):
        return list(map(
            lambda t: {
                **t,
                "amount_usd": t["amount"] * exchange_rates[t["currency"]]
            },
            transactions
        ))
    
    @log_step("3. Get large transactions")
    def get_large_transactions(transactions):
        return list(filter(lambda t: t["amount_usd"] > 100, transactions))
    
    @log_step("4. Calculate statistics")
    def calculate_statistics(transactions):
        if not transactions:
            return {"count": 0, "total": 0, "average": 0}
        
        total = reduce(lambda acc, t: acc + t["amount_usd"], transactions, 0)
        count = len(transactions)
        
        return {
            "count": count,
            "total": total,
            "average": total / count
        }
    
    # Build and execute pipeline
    print("Building transaction processing pipeline...\n")
    
    # Functional pipeline
    result = calculate_statistics(
        get_large_transactions(
            convert_to_usd(
                filter_completed(transactions)
            )
        )
    )
    
    print("\nPipeline Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    # Alternative: Using a pipeline function
    def pipeline(data, *functions):
        """Apply a series of functions to data."""
        return reduce(lambda d, f: f(d), functions, data)
    
    print("\nAlternative using pipeline function:")
    final_result = pipeline(
        transactions,
        filter_completed,
        convert_to_usd,
        get_large_transactions,
        calculate_statistics
    )
    
    print(f"Final result: {final_result}")

# Run the comprehensive example
pipeline_example()