"""
COMPREHENSIVE PYTHON FUNCTIONS DEMONSTRATION
This script demonstrates Python functions with detailed examples.
"""

print("=" * 70)
print("PYTHON FUNCTIONS - DEFINITION, PARAMETERS, SCOPE, AND MORE")
print("=" * 70)

# ============================================================================
# SECTION 1: INTRODUCTION TO FUNCTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 1: INTRODUCTION TO FUNCTIONS")
print("=" * 60)

print("""
1.1 What are Functions?

Functions are reusable blocks of code that:
1. Perform specific tasks
2. Can accept input (parameters)
3. Can return output (return values)
4. Help organize code and avoid repetition
5. Make code more readable and maintainable

In Python, functions are first-class objects - they can be:
- Assigned to variables
- Passed as arguments
- Returned from other functions
- Stored in data structures
""")

# ============================================================================
# SECTION 2: DEFINING AND CALLING FUNCTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: DEFINING AND CALLING FUNCTIONS")
print("=" * 60)

# ----------------------------------------------------------------------------
# BASIC FUNCTION DEFINITION
# ----------------------------------------------------------------------------
print("\n2.1 Basic Function Definition:")

def greet():
    """Simple function without parameters."""
    print("   Hello, World!")

# Calling the function
print("   Calling greet():")
greet()

# ----------------------------------------------------------------------------
# FUNCTION WITH PARAMETERS
# ----------------------------------------------------------------------------
print("\n2.2 Function with Parameters:")

def greet_person(name):
    """Function with one parameter."""
    print(f"   Hello, {name}!")

print("   Calling greet_person('Alice'):")
greet_person("Alice")

# ----------------------------------------------------------------------------
# FUNCTION WITH MULTIPLE PARAMETERS
# ----------------------------------------------------------------------------
print("\n2.3 Function with Multiple Parameters:")

def introduce(name, age, city):
    """Function with multiple parameters."""
    print(f"   Hi, I'm {name}, {age} years old, from {city}.")

print("   Calling introduce('Bob', 30, 'New York'):")
introduce("Bob", 30, "New York")

# ----------------------------------------------------------------------------
# FUNCTION WITH RETURN VALUE
# ----------------------------------------------------------------------------
print("\n2.4 Function with Return Value:")

def add(a, b):
    """Function that returns a value."""
    result = a + b
    return result

sum_result = add(5, 3)
print(f"   add(5, 3) returns: {sum_result}")

# Functions without explicit return return None
def no_return_function():
    """Function without return statement."""
    print("   This function doesn't return anything")

result = no_return_function()
print(f"   no_return_function() returns: {result}")

# ============================================================================
# SECTION 3: PARAMETERS AND ARGUMENTS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: PARAMETERS AND ARGUMENTS")
print("=" * 60)

print("""
3.1 Parameters vs Arguments:
- PARAMETERS: Variables in function definition (a, b in def add(a, b))
- ARGUMENTS: Actual values passed to function (5, 3 in add(5, 3))
""")

# ----------------------------------------------------------------------------
# POSITIONAL ARGUMENTS
# ----------------------------------------------------------------------------
print("\n3.2 Positional Arguments:")

def describe_pet(animal_type, pet_name):
    """Demonstrate positional arguments."""
    print(f"   I have a {animal_type} named {pet_name}.")

print("   Positional arguments (order matters):")
describe_pet("dog", "Buddy")
describe_pet("Buddy", "dog")  # Order is wrong!

# ----------------------------------------------------------------------------
# KEYWORD ARGUMENTS (NAMED ARGUMENTS)
# ----------------------------------------------------------------------------
print("\n3.3 Keyword Arguments (Named Arguments):")

print("   Keyword arguments (order doesn't matter):")
describe_pet(animal_type="cat", pet_name="Whiskers")
describe_pet(pet_name="Whiskers", animal_type="cat")  # Same result

# Mixing positional and keyword arguments
print("\n   Mixing positional and keyword arguments:")
describe_pet("hamster", pet_name="Nibbles")  # Positional first, then keyword

# ----------------------------------------------------------------------------
# DEFAULT PARAMETER VALUES
# ----------------------------------------------------------------------------
print("\n3.4 Default Parameter Values:")

def describe_pet_with_default(pet_name, animal_type="dog"):
    """Function with default parameter value."""
    print(f"   I have a {animal_type} named {pet_name}.")

print("   Using default value:")
describe_pet_with_default("Rex")  # animal_type defaults to "dog"

print("\n   Overriding default value:")
describe_pet_with_default("Fluffy", "cat")

print("\n   Default parameters must come after non-default parameters:")
print("   def func(a, b=5):     # OK")
print("   def func(a=5, b):     # SyntaxError")

# ----------------------------------------------------------------------------
# ARBITRARY ARGUMENTS (*args)
# ----------------------------------------------------------------------------
print("\n3.5 Arbitrary Arguments (*args):")

def sum_numbers(*args):
    """Function that accepts any number of positional arguments."""
    print(f"   args type: {type(args)}")  # It's a tuple!
    print(f"   args received: {args}")
    total = 0
    for num in args:
        total += num
    return total

print("   Calling with different number of arguments:")
print(f"   sum_numbers(1, 2) = {sum_numbers(1, 2)}")
print(f"   sum_numbers(1, 2, 3, 4, 5) = {sum_numbers(1, 2, 3, 4, 5)}")

# Using *args with regular parameters
def make_pizza(size, *toppings):
    """Function with regular parameter and *args."""
    print(f"   Making a {size} pizza with:")
    for topping in toppings:
        print(f"     - {topping}")

print("\n   make_pizza('large', 'pepperoni', 'mushrooms', 'cheese'):")
make_pizza("large", "pepperoni", "mushrooms", "cheese")

# ----------------------------------------------------------------------------
# ARBITRARY KEYWORD ARGUMENTS (**kwargs)
# ----------------------------------------------------------------------------
print("\n3.6 Arbitrary Keyword Arguments (**kwargs):")

def build_profile(**kwargs):
    """Function that accepts any number of keyword arguments."""
    print(f"   kwargs type: {type(kwargs)}")  # It's a dictionary!
    print(f"   kwargs received: {kwargs}")
    
    profile = {}
    for key, value in kwargs.items():
        profile[key] = value
    return profile

print("   Creating user profiles with **kwargs:")
user1 = build_profile(first_name="Alice", last_name="Smith", age=30)
print(f"   User 1: {user1}")

user2 = build_profile(name="Bob", occupation="Engineer", city="NYC", salary=75000)
print(f"   User 2: {user2}")

# Using **kwargs with regular parameters
def create_car(brand, model, **car_info):
    """Function with regular parameters and **kwargs."""
    car = {"brand": brand, "model": model}
    car.update(car_info)
    return car

print("\n   Creating cars with **kwargs:")
my_car = create_car("Toyota", "Camry", year=2020, color="blue", mileage=15000)
print(f"   My car: {my_car}")

# ----------------------------------------------------------------------------
# COMBINING ALL PARAMETER TYPES
# ----------------------------------------------------------------------------
print("\n3.7 Combining All Parameter Types:")

def complex_function(a, b=10, *args, c=20, **kwargs):
    """
    Function demonstrating all parameter types.
    Order must be: positional, *args, keyword-only, **kwargs
    """
    print(f"   a: {a}, b: {b}, c: {c}")
    print(f"   args: {args}")
    print(f"   kwargs: {kwargs}")
    return "Done"

print("   Complex function call:")
complex_function(1, 2, 3, 4, 5, c=30, x=100, y=200)

# ----------------------------------------------------------------------------
# PARAMETER ORDER RULES
# ----------------------------------------------------------------------------
print("\n3.8 Parameter Order Rules:")
print("""
When defining functions, parameters must be in this order:

1. Positional parameters
2. *args (arbitrary positional arguments)
3. Keyword-only parameters (after * or *args)
4. **kwargs (arbitrary keyword arguments)

Example:
def func(pos1, pos2, *args, kw1=default, kw2=default, **kwargs)
""")

# ============================================================================
# SECTION 4: RETURN VALUES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: RETURN VALUES")
print("=" * 60)

# ----------------------------------------------------------------------------
# SINGLE RETURN VALUE
# ----------------------------------------------------------------------------
print("\n4.1 Single Return Value:")

def square(number):
    """Return the square of a number."""
    return number ** 2

result = square(5)
print(f"   square(5) = {result}")

# ----------------------------------------------------------------------------
# MULTIPLE RETURN VALUES (TUPLES)
# ----------------------------------------------------------------------------
print("\n4.2 Multiple Return Values (as Tuple):")

def min_max(numbers):
    """Return both minimum and maximum from a list."""
    if not numbers:
        return None, None  # Return two None values
    return min(numbers), max(numbers)

nums = [5, 2, 8, 1, 9, 3]
minimum, maximum = min_max(nums)
print(f"   List: {nums}")
print(f"   Minimum: {minimum}, Maximum: {maximum}")

# What's actually returned?
result = min_max(nums)
print(f"   Type of return value: {type(result)}")  # It's a tuple!
print(f"   Unpacked return value: {result}")

# ----------------------------------------------------------------------------
# RETURNING DIFFERENT TYPES
# ----------------------------------------------------------------------------
print("\n4.3 Returning Different Types:")

def process_data(data):
    """Return different types based on input."""
    if isinstance(data, list):
        return sorted(data)  # Return list
    elif isinstance(data, dict):
        return list(data.keys())  # Return list
    elif isinstance(data, str):
        return data.upper()  # Return string
    else:
        return None  # Return None

print("   process_data([3, 1, 2]):", process_data([3, 1, 2]))
print("   process_data({'a': 1, 'b': 2}):", process_data({'a': 1, 'b': 2}))
print("   process_data('hello'):", process_data('hello'))

# ----------------------------------------------------------------------------
# EARLY RETURNS
# ----------------------------------------------------------------------------
print("\n4.4 Early Returns (Guard Clauses):")

def validate_user(username, age):
    """Demonstrate early returns with guard clauses."""
    # Guard clause 1
    if not username:
        return "Error: Username cannot be empty"
    
    # Guard clause 2
    if age < 0:
        return "Error: Age cannot be negative"
    
    # Guard clause 3
    if age < 13:
        return "Error: User must be at least 13 years old"
    
    # Main logic (only reached if all checks pass)
    return f"User '{username}' (age {age}) validated successfully"

print("   Validation results:")
print(f"   {validate_user('', 20)}")
print(f"   {validate_user('Alice', -5)}")
print(f"   {validate_user('Bob', 10)}")
print(f"   {validate_user('Charlie', 25)}")

# ----------------------------------------------------------------------------
# RETURNING FUNCTIONS (HIGHER-ORDER FUNCTIONS)
# ----------------------------------------------------------------------------
print("\n4.5 Returning Functions:")

def create_multiplier(factor):
    """Return a function that multiplies by the given factor."""
    def multiplier(x):
        return x * factor
    return multiplier

# Create specialized functions
double = create_multiplier(2)
triple = create_multiplier(3)

print(f"   double(5) = {double(5)}")
print(f"   triple(5) = {triple(5)}")

# ============================================================================
# SECTION 5: SCOPE - LOCAL vs GLOBAL
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: SCOPE - LOCAL vs GLOBAL")
print("=" * 60)

print("""
5.1 Understanding Scope:

Scope determines where variables can be accessed:
- LOCAL SCOPE: Variables defined inside a function
- GLOBAL SCOPE: Variables defined at module level
- BUILT-IN SCOPE: Python's built-in names

Python uses LEGB rule for name resolution:
L: Local
E: Enclosing (for nested functions)
G: Global
B: Built-in
""")

# ----------------------------------------------------------------------------
# LOCAL VARIABLES
# ----------------------------------------------------------------------------
print("\n5.2 Local Variables:")

def demonstrate_local():
    """Function with local variables."""
    local_var = "I'm local"
    print(f"   Inside function: local_var = '{local_var}'")

demonstrate_local()

# Trying to access local_var outside the function
try:
    print(f"   Outside function: local_var = '{local_var}'")
except NameError as e:
    print(f"   Error: {e}")

# ----------------------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------------------
print("\n5.3 Global Variables:")

global_var = "I'm global"

def access_global():
    """Function accessing global variable."""
    print(f"   Inside function: global_var = '{global_var}'")

access_global()
print(f"   Outside function: global_var = '{global_var}'")

# ----------------------------------------------------------------------------
# LOCAL vs GLOBAL with SAME NAME
# ----------------------------------------------------------------------------
print("\n5.4 Local vs Global with Same Name:")

x = "global x"

def demonstrate_shadowing():
    """Function that creates a local variable with same name as global."""
    x = "local x"  # This creates a new local variable, doesn't modify global
    print(f"   Inside function: x = '{x}'")

demonstrate_shadowing()
print(f"   Outside function: x = '{x}'")  # Global x unchanged

# ----------------------------------------------------------------------------
# MODIFYING GLOBAL VARIABLES (global keyword)
# ----------------------------------------------------------------------------
print("\n5.5 Modifying Global Variables (global keyword):")

counter = 0

def increment_counter():
    """Function that modifies a global variable."""
    global counter  # Declare we're using the global variable
    counter += 1
    print(f"   Inside function: counter = {counter}")

print(f"   Before: counter = {counter}")
increment_counter()
print(f"   After: counter = {counter}")

# ----------------------------------------------------------------------------
# NESTED FUNCTIONS AND ENCLOSING SCOPE
# ----------------------------------------------------------------------------
print("\n5.6 Nested Functions and Enclosing Scope:")

def outer_function():
    """Outer function with nested inner function."""
    outer_var = "I'm in outer scope"
    
    def inner_function():
        """Inner function accessing enclosing scope."""
        print(f"   Inside inner function: outer_var = '{outer_var}'")
    
    inner_function()
    return inner_function

print("   Calling outer_function():")
outer_function()

# ----------------------------------------------------------------------------
# NONLOCAL KEYWORD
# ----------------------------------------------------------------------------
print("\n5.7 Modifying Enclosing Scope Variables (nonlocal):")

def outer():
    """Demonstrate nonlocal keyword."""
    count = 0
    
    def inner():
        nonlocal count  # Refers to count in the enclosing scope
        count += 1
        return count
    
    return inner

counter_func = outer()
print(f"   counter_func() = {counter_func()}")
print(f"   counter_func() = {counter_func()}")
print(f"   counter_func() = {counter_func()}")

# ----------------------------------------------------------------------------
# SCOPE EXAMPLE WITH DIFFERENT LEVELS
# ----------------------------------------------------------------------------
print("\n5.8 Scope Example with Different Levels:")

# Built-in scope (B)
print("   Built-in scope example:")
print(f"   len('hello') = {len('hello')}")  # len is in built-in scope

# Global scope (G)
global_value = "global"

def level_one():
    # Enclosing scope for level_two (E)
    enclosing_value = "enclosing"
    
    def level_two():
        # Local scope (L)
        local_value = "local"
        
        print("\n   Inside level_two():")
        print(f"     Local: {local_value}")
        print(f"     Enclosing: {enclosing_value}")
        print(f"     Global: {global_value}")
        print(f"     Built-in: {len([1,2,3])}")
    
    level_two()

print("\n   Calling level_one():")
level_one()

# ============================================================================
# SECTION 6: FUNCTION TYPES AND PATTERNS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: FUNCTION TYPES AND PATTERNS")
print("=" * 60)

# ----------------------------------------------------------------------------
# PURE FUNCTIONS
# ----------------------------------------------------------------------------
print("\n6.1 Pure Functions:")

print("""
Pure functions have:
1. Same input always produces same output
2. No side effects (don't modify external state)
3. Don't depend on external state
""")

def pure_add(a, b):
    """Pure function example."""
    return a + b

def impure_add(a, b):
    """Impure function example (has side effect)."""
    result = a + b
    print(f"   Adding {a} + {b} = {result}")  # Side effect: printing
    return result

print("   Pure function: pure_add(2, 3) =", pure_add(2, 3))
print("   Impure function:")
impure_add(2, 3)

# ----------------------------------------------------------------------------
# HIGHER-ORDER FUNCTIONS
# ----------------------------------------------------------------------------
print("\n6.2 Higher-Order Functions:")

print("""
Higher-order functions either:
1. Take functions as arguments
2. Return functions as results
""")

def apply_operation(numbers, operation):
    """Apply operation to each number in list."""
    return [operation(num) for num in numbers]

numbers = [1, 2, 3, 4, 5]

# Passing functions as arguments
squared = apply_operation(numbers, lambda x: x ** 2)
cubed = apply_operation(numbers, lambda x: x ** 3)

print(f"   Numbers: {numbers}")
print(f"   Squared: {squared}")
print(f"   Cubed: {cubed}")

# ----------------------------------------------------------------------------
# LAMBDA FUNCTIONS (ANONYMOUS FUNCTIONS)
# ----------------------------------------------------------------------------
print("\n6.3 Lambda Functions (Anonymous Functions):")

# Regular function
def square(x):
    return x ** 2

# Equivalent lambda function
square_lambda = lambda x: x ** 2

print(f"   square(5) = {square(5)}")
print(f"   square_lambda(5) = {square_lambda(5)}")

# Lambda functions are often used for short operations
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"   Doubled numbers: {doubled}")

# Sorting with lambda
people = [("Alice", 25), ("Bob", 20), ("Charlie", 30)]
sorted_by_age = sorted(people, key=lambda person: person[1])
print(f"   People sorted by age: {sorted_by_age}")

# ----------------------------------------------------------------------------
# CLOSURES
# ----------------------------------------------------------------------------
print("\n6.4 Closures:")

def make_counter(start=0):
    """Create a counter function using closure."""
    count = start  # This variable is "closed over"
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

counter1 = make_counter(10)
counter2 = make_counter(100)

print(f"   Counter 1: {counter1()}, {counter1()}, {counter1()}")
print(f"   Counter 2: {counter2()}, {counter2()}")

# Each closure has its own state
print("   Each closure maintains its own 'count' variable")

# ----------------------------------------------------------------------------
# DECORATORS (ADVANCED TOPIC)
# ----------------------------------------------------------------------------
print("\n6.5 Decorators (Introduction):")

def simple_decorator(func):
    """A simple decorator that adds timing."""
    def wrapper(*args, **kwargs):
        print(f"   Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"   {func.__name__} finished")
        return result
    return wrapper

@simple_decorator
def say_hello(name):
    """Greet someone."""
    return f"Hello, {name}!"

print("   Using decorator:")
result = say_hello("Alice")
print(f"   Result: {result}")

# ============================================================================
# SECTION 7: DOCUMENTING FUNCTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: DOCUMENTING FUNCTIONS")
print("=" * 60)

print("\n7.1 Docstrings:")

def calculate_area(radius):
    """
    Calculate the area of a circle.
    
    Args:
        radius (float): The radius of the circle in units.
        
    Returns:
        float: The area of the circle in square units.
        
    Raises:
        ValueError: If radius is negative.
        
    Examples:
        >>> calculate_area(5)
        78.53981633974483
        
        >>> calculate_area(0)
        0.0
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    import math
    return math.pi * radius ** 2

print("   Function docstring:")
print(calculate_area.__doc__)

# Accessing function metadata
print(f"\n   Function name: {calculate_area.__name__}")
print(f"   Function module: {calculate_area.__module__}")

# ----------------------------------------------------------------------------
# TYPE HINTS (PYTHON 3.5+)
# ----------------------------------------------------------------------------
print("\n7.2 Type Hints (Python 3.5+):")

from typing import List, Tuple, Optional, Union

def process_items(items: List[str], 
                  count: int = 1,
                  optional_param: Optional[str] = None) -> Tuple[List[str], int]:
    """
    Process a list of items.
    
    Type hints help with:
    1. Code readability
    2. IDE autocomplete
    3. Static type checking (with tools like mypy)
    """
    # Type hints don't enforce types at runtime (unless using type-checking tools)
    processed = [item.upper() for item in items[:count]]
    return processed, len(processed)

# The function works the same way
result = process_items(["apple", "banana", "cherry"], 2)
print(f"   process_items(['apple', 'banana', 'cherry'], 2) = {result}")

# ============================================================================
# SECTION 8: COMMON FUNCTION PATTERNS AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 8: COMMON PATTERNS AND BEST PRACTICES")
print("=" * 60)

# ----------------------------------------------------------------------------
# THE SINGLE RESPONSIBILITY PRINCIPLE
# ----------------------------------------------------------------------------
print("\n8.1 Single Responsibility Principle:")

print("""
BAD: Function does too many things
def process_user_data(data):
    # Validates data
    # Saves to database
    # Sends email
    # Logs activity
    # etc.
    
GOOD: Each function does one thing
def validate_user_data(data):
    # Only validates

def save_to_database(data):
    # Only saves

def send_notification(user):
    # Only sends notification
""")

# ----------------------------------------------------------------------------
# DEFAULT ARGUMENT GOTCHA
# ----------------------------------------------------------------------------
print("\n8.2 Default Argument Gotcha:")

print("""
WARNING: Mutable default arguments are shared across function calls!
""")

def bad_append(item, items=[]):
    """BAD: Default list is shared across calls."""
    items.append(item)
    return items

def good_append(item, items=None):
    """GOOD: Create new list if None provided."""
    if items is None:
        items = []
    items.append(item)
    return items

print("   Testing bad_append:")
print(f"   bad_append(1) = {bad_append(1)}")
print(f"   bad_append(2) = {bad_append(2)}")  # Keeps previous items!

print("\n   Testing good_append:")
print(f"   good_append(1) = {good_append(1)}")
print(f"   good_append(2) = {good_append(2)}")  # Fresh list each time

# ----------------------------------------------------------------------------
# FUNCTION COMPOSITION
# ----------------------------------------------------------------------------
print("\n8.3 Function Composition:")

def add_one(x):
    return x + 1

def multiply_by_two(x):
    return x * 2

def square(x):
    return x ** 2

# Manual composition
result = square(multiply_by_two(add_one(5)))
print(f"   square(multiply_by_two(add_one(5))) = {result}")

# Composition function
def compose(*functions):
    """Compose multiple functions."""
    def composed(arg):
        result = arg
        for func in reversed(functions):
            result = func(result)
        return result
    return composed

composed_func = compose(square, multiply_by_two, add_one)
print(f"   composed_func(5) = {composed_func(5)}")

# ----------------------------------------------------------------------------
# FUNCTION CACHING/MEMOIZATION
# ----------------------------------------------------------------------------
print("\n8.4 Function Caching/Memoization:")

def fibonacci(n, cache={}):
    """
    Calculate Fibonacci number with memoization.
    cache dictionary persists across calls.
    """
    if n in cache:
        return cache[n]
    
    if n <= 1:
        result = n
    else:
        result = fibonacci(n-1) + fibonacci(n-2)
    
    cache[n] = result
    return result

print("   Fibonacci numbers (cached):")
for i in range(10):
    print(f"   fibonacci({i}) = {fibonacci(i)}")

# ----------------------------------------------------------------------------
# ARGUMENT UNPACKING
# ----------------------------------------------------------------------------
print("\n8.5 Argument Unpacking:")

def print_coordinates(x, y, z):
    print(f"   Coordinates: x={x}, y={y}, z={z}")

# Using * to unpack list/tuple
point = [10, 20, 30]
print_coordinates(*point)  # Unpacks list

# Using ** to unpack dictionary
point_dict = {"x": 100, "y": 200, "z": 300}
print_coordinates(**point_dict)  # Unpacks dictionary

# ----------------------------------------------------------------------------
# ERROR HANDLING IN FUNCTIONS
# ----------------------------------------------------------------------------
print("\n8.6 Error Handling in Functions:")

def safe_divide(a, b):
    """Function with error handling."""
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Division by zero"
    except TypeError:
        return "Error: Both arguments must be numbers"
    else:
        return result

print(f"   safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"   safe_divide(10, 0) = {safe_divide(10, 0)}")
print(f"   safe_divide(10, '2') = {safe_divide(10, '2')}")

# ============================================================================
# SECTION 9: PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 9: PRACTICAL EXAMPLES")
print("=" * 60)

# ----------------------------------------------------------------------------
# EXAMPLE 1: DATA VALIDATION FUNCTION
# ----------------------------------------------------------------------------
print("\n9.1 Data Validation Function:")

def validate_student_data(name, age, grades):
    """
    Validate student data with comprehensive checks.
    
    Demonstrates:
    - Multiple parameters
    - Type checking
    - Value validation
    - Early returns
    - Clear error messages
    """
    # Check name
    if not isinstance(name, str):
        return False, "Name must be a string"
    if not name.strip():
        return False, "Name cannot be empty"
    
    # Check age
    if not isinstance(age, (int, float)):
        return False, "Age must be a number"
    if age < 0 or age > 120:
        return False, "Age must be between 0 and 120"
    
    # Check grades
    if not isinstance(grades, list):
        return False, "Grades must be a list"
    if not grades:
        return False, "Grades list cannot be empty"
    for grade in grades:
        if not isinstance(grade, (int, float)):
            return False, "All grades must be numbers"
        if grade < 0 or grade > 100:
            return False, f"Grade {grade} must be between 0 and 100"
    
    return True, "Data is valid"

print("   Testing student data validation:")
test_cases = [
    ("Alice", 20, [85, 90, 78]),  # Valid
    ("", 20, [85, 90]),           # Empty name
    ("Bob", -5, [70, 80]),        # Invalid age
    ("Charlie", 25, []),          # Empty grades
    ("Diana", 30, [85, 105, 90]), # Invalid grade
]

for name, age, grades in test_cases:
    is_valid, message = validate_student_data(name, age, grades)
    status = "✓" if is_valid else "✗"
    print(f"   {status} {name}, {age}, {grades}: {message}")

# ----------------------------------------------------------------------------
# EXAMPLE 2: CONFIGURATION BUILDER
# ----------------------------------------------------------------------------
print("\n9.2 Configuration Builder Function:")

def build_config(*, env="development", debug=False, **settings):
    """
    Build configuration with sensible defaults.
    
    Demonstrates:
    - Keyword-only arguments (*)
    - Default parameter values
    - **kwargs for additional settings
    - Dictionary manipulation
    """
    # Base configuration
    config = {
        "environment": env,
        "debug": debug,
        "database": {
            "host": "localhost",
            "port": 5432,
        }
    }
    
    # Update with additional settings
    config.update(settings)
    
    # Environment-specific overrides
    if env == "production":
        config["debug"] = False
        config["database"]["host"] = "prod-db.example.com"
    elif env == "testing":
        config["debug"] = True
        config["database"]["port"] = 5433
    
    return config

print("   Building configurations:")

# Development config (defaults)
dev_config = build_config()
print(f"   Development: {dev_config['environment']}, Debug: {dev_config['debug']}")

# Production config
prod_config = build_config(env="production", cache_size=1000)
print(f"   Production: {prod_config['environment']}, Debug: {prod_config['debug']}")

# Custom config with extra settings
custom_config = build_config(
    env="staging", 
    debug=True, 
    api_key="abc123",
    database={"host": "staging-db", "port": 5434}
)
print(f"   Custom: {custom_config['environment']}, "
      f"API Key: {custom_config.get('api_key')}")

# ----------------------------------------------------------------------------
# EXAMPLE 3: FUNCTION FACTORY
# ----------------------------------------------------------------------------
print("\n9.3 Function Factory Pattern:")

def create_math_operation(operation):
    """
    Create math operation functions dynamically.
    
    Demonstrates:
    - Returning functions
    - Closures
    - Function factories
    """
    if operation == "add":
        def add_func(a, b):
            return a + b
        return add_func
    
    elif operation == "multiply":
        def multiply_func(a, b):
            return a * b
        return multiply_func
    
    elif operation == "power":
        def power_func(a, b):
            return a ** b
        return power_func
    
    else:
        def default_func(a, b):
            raise ValueError(f"Unknown operation: {operation}")
        return default_func

print("   Creating and using operation functions:")

# Create operation functions
add = create_math_operation("add")
multiply = create_math_operation("multiply")
power = create_math_operation("power")

# Use them
print(f"   add(5, 3) = {add(5, 3)}")
print(f"   multiply(5, 3) = {multiply(5, 3)}")
print(f"   power(2, 8) = {power(2, 8)}")

# ----------------------------------------------------------------------------
# EXAMPLE 4: DECORATOR WITH ARGUMENTS
# ----------------------------------------------------------------------------
print("\n9.4 Advanced Decorator Pattern:")

def retry(max_attempts=3, delay=1):
    """
    Decorator that retries a function on failure.
    
    Demonstrates:
    - Decorators with arguments
    - Nested functions
    - *args and **kwargs
    - Function metadata preservation
    """
    import time
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    print(f"   Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# Use the decorator
@retry(max_attempts=2, delay=0.5)
def unreliable_operation():
    """Simulate an unreliable operation."""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise RuntimeError("Operation failed!")
    return "Success!"

print("   Testing retry decorator:")
try:
    result = unreliable_operation()
    print(f"   Result: {result}")
except RuntimeError as e:
    print(f"   Failed after retries: {e}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
KEY CONCEPTS COVERED:

1. FUNCTION DEFINITION AND CALLING:
   - def keyword defines functions
   - Functions are called with ()
   - Can have parameters and return values

2. PARAMETER TYPES:
   - Positional arguments: func(a, b)
   - Keyword arguments: func(a=1, b=2)
   - Default values: def func(a=1)
   - *args: Arbitrary positional arguments (tuple)
   - **kwargs: Arbitrary keyword arguments (dict)

3. RETURN VALUES:
   - return statement sends value back to caller
   - Can return multiple values as tuple
   - Functions without return return None
   - Early returns for error handling

4. SCOPE:
   - Local scope: Inside function
   - Global scope: Module level
   - Enclosing scope: For nested functions
   - Built-in scope: Python's built-in names
   - global keyword: Modify global variables
   - nonlocal keyword: Modify enclosing scope variables

5. FUNCTION TYPES:
   - Pure functions: No side effects
   - Higher-order functions: Take/return functions
   - Lambda functions: Anonymous functions
   - Closures: Functions with "remembered" environment
   - Decorators: Modify function behavior

6. BEST PRACTICES:
   - Single responsibility principle
   - Avoid mutable default arguments
   - Use docstrings for documentation
   - Consider type hints (Python 3.5+)
   - Handle errors appropriately
   - Keep functions focused and small

7. COMMON PATTERNS:
   - Function composition
   - Function factories
   - Memoization/caching
   - Argument unpacking (* and **)
   - Guard clauses/early returns

REMEMBER:
- Functions make code reusable and organized
- Understand scope to avoid variable conflicts
- Use appropriate parameter types for flexibility
- Document your functions well
- Functions are first-class objects in Python
""")

print("\n" + "=" * 70)
print("END OF FUNCTIONS DEMONSTRATION")
print("=" * 70)