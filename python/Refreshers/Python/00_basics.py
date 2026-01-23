"""
COMPREHENSIVE PYTHON CONCEPTS EXPLANATION
This script demonstrates fundamental Python concepts with detailed explanations.
Run this script to see examples of how Python handles various operations.
"""

# ============================================================================
# SECTION 1: VARIABLES AND DYNAMIC TYPING
# ============================================================================

print("=" * 60)
print("SECTION 1: VARIABLES AND DYNAMIC TYPING")
print("=" * 60)

# ----------------------------------------------------------------------------
# VARIABLES
# ----------------------------------------------------------------------------
# Variables are names that refer to values stored in memory.
# In Python, you create a variable by assigning a value to a name using =

# Simple variable assignment
my_variable = 10  # 'my_variable' now refers to the integer value 10
print(f"1.1 my_variable = {my_variable}")

# Variables can be reassigned to different values
my_variable = "Now I'm a string"  # Python allows this due to dynamic typing
print(f"1.2 my_variable reassigned = '{my_variable}'")

# ----------------------------------------------------------------------------
# DYNAMIC TYPING
# ----------------------------------------------------------------------------
# Python uses dynamic typing, meaning variable types are determined at runtime
# and can change during program execution.

# The same variable can hold different data types at different times
dynamic_var = 42
print(f"1.3 Type of dynamic_var (int): {type(dynamic_var)}")

dynamic_var = 3.14
print(f"1.4 Type of dynamic_var (float): {type(dynamic_var)}")

dynamic_var = "Hello"
print(f"1.5 Type of dynamic_var (str): {type(dynamic_var)}")

dynamic_var = True
print(f"1.6 Type of dynamic_var (bool): {type(dynamic_var)}")

# ============================================================================
# SECTION 2: BASIC DATA TYPES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: BASIC DATA TYPES")
print("=" * 60)

# ----------------------------------------------------------------------------
# INTEGER (int)
# ----------------------------------------------------------------------------
# Whole numbers, positive or negative, without decimals
integer_example = 42
negative_int = -15
large_int = 10_000_000  # Underscores improve readability (Python 3.6+)

print(f"2.1 Integer examples: {integer_example}, {negative_int}, {large_int}")
print(f"2.2 Type of integer_example: {type(integer_example)}")

# ----------------------------------------------------------------------------
# FLOAT (float)
# ----------------------------------------------------------------------------
# Real numbers with decimal points or in scientific notation
float_example = 3.14159
scientific_float = 6.022e23  # Scientific notation: 6.022 × 10^23
negative_float = -2.5

print(f"2.3 Float examples: {float_example}, {scientific_float}, {negative_float}")
print(f"2.4 Type of float_example: {type(float_example)}")

# Note: Float arithmetic can have precision issues due to binary representation
precision_issue = 0.1 + 0.2
print(f"2.5 Float precision issue: 0.1 + 0.2 = {precision_issue}")
print(f"2.6 Expected: 0.3, Actual: {precision_issue}")

# ----------------------------------------------------------------------------
# STRING (str)
# ----------------------------------------------------------------------------
# Sequence of characters, defined with single, double, or triple quotes
single_quote_str = 'Hello'
double_quote_str = "World"
triple_quote_str = """This is a
multi-line
string"""

# String concatenation
concatenated = single_quote_str + " " + double_quote_str
print(f"2.7 String examples: '{single_quote_str}', '{double_quote_str}'")
print(f"2.8 Concatenated: '{concatenated}'")
print(f"2.9 Multi-line string:\n{triple_quote_str}")
print(f"2.10 Type of single_quote_str: {type(single_quote_str)}")

# String methods (strings are immutable - more on that later)
lowercase_str = "HELLO".lower()
print(f"2.11 'HELLO'.lower() = '{lowercase_str}'")

# ----------------------------------------------------------------------------
# BOOLEAN (bool)
# ----------------------------------------------------------------------------
# Represents truth values: True or False (note capitalization)
true_value = True
false_value = False

print(f"2.12 Boolean examples: {true_value}, {false_value}")
print(f"2.13 Type of true_value: {type(true_value)}")

# ----------------------------------------------------------------------------
# NONE TYPE
# ----------------------------------------------------------------------------
# None represents the absence of a value, similar to null in other languages
none_value = None
print(f"2.14 None value: {none_value}")
print(f"2.15 Type of none_value: {type(none_value)}")

# None is often used as a default value or to indicate no return value
def function_that_returns_nothing():
    """This function implicitly returns None"""
    pass

result = function_that_returns_nothing()
print(f"2.16 Function that returns nothing: {result}")

# ============================================================================
# SECTION 3: OPERATORS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: OPERATORS")
print("=" * 60)

# ----------------------------------------------------------------------------
# ARITHMETIC OPERATORS
# ----------------------------------------------------------------------------
a, b = 10, 3

print("3.1 Arithmetic Operators:")
print(f"   {a} + {b} = {a + b}")      # Addition
print(f"   {a} - {b} = {a - b}")      # Subtraction
print(f"   {a} * {b} = {a * b}")      # Multiplication
print(f"   {a} / {b} = {a / b}")      # Division (always returns float)
print(f"   {a} // {b} = {a // b}")    # Floor division (integer division)
print(f"   {a} % {b} = {a % b}")      # Modulus (remainder)
print(f"   {a} ** {b} = {a ** b}")    # Exponentiation

# ----------------------------------------------------------------------------
# COMPARISON OPERATORS
# ----------------------------------------------------------------------------
x, y = 5, 10

print("\n3.2 Comparison Operators:")
print(f"   {x} == {y}: {x == y}")    # Equal to
print(f"   {x} != {y}: {x != y}")    # Not equal to
print(f"   {x} > {y}: {x > y}")      # Greater than
print(f"   {x} < {y}: {x < y}")      # Less than
print(f"   {x} >= {y}: {x >= y}")    # Greater than or equal to
print(f"   {x} <= {y}: {x <= y}")    # Less than or equal to

# ----------------------------------------------------------------------------
# LOGICAL OPERATORS
# ----------------------------------------------------------------------------
p, q = True, False

print("\n3.3 Logical Operators:")
print(f"   {p} and {q}: {p and q}")   # Logical AND
print(f"   {p} or {q}: {p or q}")     # Logical OR
print(f"   not {p}: {not p}")         # Logical NOT

# ----------------------------------------------------------------------------
# ASSIGNMENT OPERATORS
# ----------------------------------------------------------------------------
num = 5
print("\n3.4 Assignment Operators:")
num += 3  # Equivalent to num = num + 3
print(f"   num += 3: {num}")
num -= 2  # Equivalent to num = num - 2
print(f"   num -= 2: {num}")
num *= 2  # Equivalent to num = num * 2
print(f"   num *= 2: {num}")
num /= 4  # Equivalent to num = num / 4
print(f"   num /= 4: {num}")

# ----------------------------------------------------------------------------
# IDENTITY OPERATORS
# ----------------------------------------------------------------------------
# 'is' and 'is not' check if two variables refer to the same object
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = list1  # list3 refers to the same object as list1

print("\n3.5 Identity Operators:")
print(f"   list1 is list2: {list1 is list2}")  # False - different objects
print(f"   list1 is list3: {list1 is list3}")  # True - same object
print(f"   list1 is not list2: {list1 is not list2}")  # True

# ----------------------------------------------------------------------------
# MEMBERSHIP OPERATORS
# ----------------------------------------------------------------------------
# 'in' and 'not in' check if a value exists in a sequence
my_list = [1, 2, 3, 4, 5]
my_string = "Hello World"

print("\n3.6 Membership Operators:")
print(f"   3 in {my_list}: {3 in my_list}")
print(f"   10 in {my_list}: {10 in my_list}")
print(f"   'World' in '{my_string}': {'World' in my_string}")
print(f"   'Python' not in '{my_string}': {'Python' not in my_string}")

# ============================================================================
# SECTION 4: MUTABILITY VS IMMUTABILITY
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: MUTABILITY VS IMMUTABILITY")
print("=" * 60)

# ----------------------------------------------------------------------------
# IMMUTABLE TYPES
# ----------------------------------------------------------------------------
# Immutable objects cannot be changed after creation
# Basic immutable types: int, float, str, bool, tuple

print("4.1 Immutable Types (int, float, str, bool, tuple):")

# Example with integers
immutable_int = 10
print(f"   Before: immutable_int = {immutable_int}, id = {id(immutable_int)}")
immutable_int += 5  # This creates a NEW integer object
print(f"   After immutable_int += 5: {immutable_int}, id = {id(immutable_int)}")
print("   Note: The id changed! A new object was created.")

# Example with strings
immutable_str = "Hello"
print(f"\n   Before: immutable_str = '{immutable_str}', id = {id(immutable_str)}")
immutable_str += " World"  # This creates a NEW string object
print(f"   After immutable_str += ' World': '{immutable_str}'")
print(f"   New id = {id(immutable_str)}")

# Example with tuples (immutable sequences)
immutable_tuple = (1, 2, 3)
print(f"\n   Tuple: {immutable_tuple}")
print(f"   Trying to modify: immutable_tuple[0] = 5 will raise TypeError")

# ----------------------------------------------------------------------------
# MUTABLE TYPES
# ----------------------------------------------------------------------------
# Mutable objects can be changed after creation
# Common mutable types: list, dict, set

print("\n4.2 Mutable Types (list, dict, set):")

# Example with lists
mutable_list = [1, 2, 3]
print(f"   Before: mutable_list = {mutable_list}, id = {id(mutable_list)}")
mutable_list.append(4)  # Modifies the existing object
print(f"   After append: mutable_list = {mutable_list}, id = {id(mutable_list)}")
print("   Note: The id stayed the same! Same object was modified.")

mutable_list[0] = 100  # We can modify elements
print(f"   After mutable_list[0] = 100: {mutable_list}")

# Example with dictionaries
mutable_dict = {"name": "Alice", "age": 30}
print(f"\n   Dict before: {mutable_dict}")
mutable_dict["age"] = 31  # Modify existing key
mutable_dict["city"] = "New York"  # Add new key-value pair
print(f"   Dict after modifications: {mutable_dict}")

# ----------------------------------------------------------------------------
# IMPORTANT CONSEQUENCES OF MUTABILITY
# ----------------------------------------------------------------------------
print("\n4.3 Important Consequences:")

# When you assign a mutable object to a new variable,
# both variables reference the SAME object
original_list = [1, 2, 3]
copied_reference = original_list  # Not a copy, just another reference

print(f"   original_list: {original_list}, id: {id(original_list)}")
print(f"   copied_reference: {copied_reference}, id: {id(copied_reference)}")

copied_reference.append(4)  # Modifies the shared object
print(f"\n   After copied_reference.append(4):")
print(f"   original_list: {original_list}")  # Also modified!
print(f"   copied_reference: {copied_reference}")

# To create an actual copy, use .copy() method or slicing
true_copy = original_list.copy()
true_copy.append(5)
print(f"\n   After creating true copy and appending 5:")
print(f"   original_list: {original_list}")  # Unchanged
print(f"   true_copy: {true_copy}")  # Has the new element

# ============================================================================
# SECTION 5: TRUTHY AND FALSY VALUES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: TRUTHY AND FALSY VALUES")
print("=" * 60)

# In Python, values evaluate to True or False in boolean contexts
# Falsy values: False, None, 0, 0.0, empty sequences/collections
# Truthy values: Everything else

print("5.1 Falsy Values (evaluate to False in boolean contexts):")
falsy_values = [False, None, 0, 0.0, "", [], {}, set(), ()]

for value in falsy_values:
    if not value:  # This condition will be True for falsy values
        print(f"   {repr(value)} is falsy")

print("\n5.2 Truthy Values (evaluate to True in boolean contexts):")
truthy_values = [True, 1, -1, 3.14, "hello", [1, 2], {"a": 1}, {1, 2}, (1, 2)]

for value in truthy_values:
    if value:  # This condition will be True for truthy values
        print(f"   {repr(value)} is truthy")

# ----------------------------------------------------------------------------
# PRACTICAL USE OF TRUTHY/FALSY VALUES
# ----------------------------------------------------------------------------
print("\n5.3 Practical Examples:")

# Check if a string is non-empty
user_input = ""
if user_input:
    print(f"   User entered: {user_input}")
else:
    print("   User entered an empty string")

# Check if a list has elements
shopping_cart = []
if shopping_cart:
    print("   Your cart has items")
else:
    print("   Your cart is empty")

# Default value assignment using 'or' operator
name = None
display_name = name or "Guest"  # If name is falsy (None), use "Guest"
print(f"\n   name = {name}, display_name = '{display_name}'")

count = 0
result = count or "No items"  # 0 is falsy, so result becomes "No items"
print(f"   count = {count}, result = '{result}'")

# ============================================================================
# SECTION 6: TYPE CASTING AND COERCION
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: TYPE CASTING AND COERCION")
print("=" * 60)

# ----------------------------------------------------------------------------
# EXPLICIT TYPE CASTING
# ----------------------------------------------------------------------------
# Converting between types using constructor functions

print("6.1 Explicit Type Casting:")

# str() - convert to string
num = 42
num_as_str = str(num)
print(f"   str({num}) = '{num_as_str}', type: {type(num_as_str)}")

# int() - convert to integer (truncates decimal part)
float_num = 3.99
float_as_int = int(float_num)  # Note: truncates, doesn't round
print(f"   int({float_num}) = {float_as_int}, type: {type(float_as_int)}")

# int() can also convert strings
numeric_string = "123"
string_as_int = int(numeric_string)
print(f"   int('{numeric_string}') = {string_as_int}, type: {type(string_as_int)}")

# float() - convert to float
int_num = 7
int_as_float = float(int_num)
print(f"   float({int_num}) = {int_as_float}, type: {type(int_as_float)}")

# bool() - convert to boolean
print(f"\n   bool(0) = {bool(0)}")
print(f"   bool(42) = {bool(42)}")
print(f"   bool('') = {bool('')}")
print(f"   bool('hello') = {bool('hello')}")
print(f"   bool([]) = {bool([])}")
print(f"   bool([1, 2]) = {bool([1, 2])}")

# ----------------------------------------------------------------------------
# IMPLICIT TYPE COERCION
# ----------------------------------------------------------------------------
# Python automatically converts types in some operations

print("\n6.2 Implicit Type Coercion:")

# Numeric types in arithmetic
int_num = 5
float_num = 2.5
result = int_num + float_num  # int is promoted to float
print(f"   {int_num} (int) + {float_num} (float) = {result} (type: {type(result)})")

# Boolean in arithmetic
true_as_int = True + 5  # True is treated as 1
false_as_int = False + 5  # False is treated as 0
print(f"   True + 5 = {true_as_int}")
print(f"   False + 5 = {false_as_int}")

# String and numeric concatenation requires explicit conversion
# This would cause TypeError: str_num = "The number is " + 42
str_num = "The number is " + str(42)  # Explicit conversion needed
print(f"\n   String concatenation: '{str_num}'")

# ============================================================================
# SECTION 7: BASIC INPUT/OUTPUT OPERATIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: BASIC INPUT/OUTPUT OPERATIONS")
print("=" * 60)

# ----------------------------------------------------------------------------
# OUTPUT: print() FUNCTION
# ----------------------------------------------------------------------------
print("7.1 Output with print():")

# Basic print
print("   Hello, World!")

# Printing multiple values
name = "Alice"
age = 30
print(f"   Name: {name}, Age: {age}")  # f-string (formatted string literal)

# Using sep and end parameters
print("   Apple", "Banana", "Cherry", sep=", ", end="!\n")

# ----------------------------------------------------------------------------
# INPUT: input() FUNCTION
# ----------------------------------------------------------------------------
print("\n7.2 Input with input():")
print("   The following sections demonstrate input, but are commented out")
print("   to avoid blocking script execution.")

# Uncomment the following lines to test input functionality:
"""
# Basic input
user_name = input("Enter your name: ")
print(f"Hello, {user_name}!")

# Input always returns a string, so conversion is often needed
age_str = input("Enter your age: ")
age = int(age_str)  # Convert to integer
print(f"In 10 years, you'll be {age + 10} years old.")

# Handle potential conversion errors
while True:
    try:
        number = float(input("Enter a number: "))
        print(f"You entered: {number}")
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
"""

# ----------------------------------------------------------------------------
# FORMATTED OUTPUT EXAMPLES
# ----------------------------------------------------------------------------
print("\n7.3 Formatted Output Examples:")

# Using f-strings (Python 3.6+)
price = 19.99
quantity = 3
total = price * quantity
print(f"   Price: ${price:.2f}, Quantity: {quantity}, Total: ${total:.2f}")

# Using format() method
template = "   Item: {}, Price: ${:.2f}"
print(template.format("Book", 15.99))

# Old style (not recommended for new code)
print("   %s is %d years old" % ("Bob", 25))

# ============================================================================
# SECTION 8: PRACTICAL EXAMPLE PUTTING IT ALL TOGETHER
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 8: PRACTICAL EXAMPLE")
print("=" * 60)

def simple_calculator():
    """
    A simple calculator demonstrating multiple Python concepts.
    This shows variables, types, operators, type conversion, and I/O.
    """
    
    # Get user input (normally we'd use input(), but for demo we'll use fixed values)
    print("\n8.1 Simple Calculator Example:")
    
    # Simulating user input for demonstration
    num1_str = "10"  # Simulated: input("Enter first number: ")
    num2_str = "3"   # Simulated: input("Enter second number: ")
    
    # Type conversion from string to float
    num1 = float(num1_str)
    num2 = float(num2_str)
    
    print(f"   Numbers: {num1} and {num2}")
    print(f"   Types: {type(num1)} and {type(num2)}")
    
    # Perform calculations
    addition = num1 + num2
    subtraction = num1 - num2
    multiplication = num1 * num2
    
    # Handle division by zero (using truthy/falsy check)
    if num2:  # Truthy if num2 is not 0
        division = num1 / num2
    else:
        division = "undefined (division by zero)"
    
    # Create a results dictionary (mutable type)
    results = {
        "Addition": addition,
        "Subtraction": subtraction,
        "Multiplication": multiplication,
        "Division": division
    }
    
    # Display results
    print("\n   Results:")
    for operation, result in results.items():
        print(f"     {operation}: {result}")
    
    # Check if results are integers or floats
    print("\n   Result types:")
    for operation, result in results.items():
        if isinstance(result, (int, float)):
            # Check if result is a whole number
            if result == int(result):
                print(f"     {operation}: {int(result)} (integer)")
            else:
                print(f"     {operation}: {result} (float)")
    
    # Demonstrate mutability
    results_copy = results  # This is a reference, not a copy
    results["Modulus"] = num1 % num2  # Modifies the original dict too
    
    print(f"\n   Original dict has new key: {'Modulus' in results}")
    print(f"   Copy also has new key: {'Modulus' in results_copy}")
    
    return results

# Run the practical example
calculator_results = simple_calculator()

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
This comprehensive example has demonstrated:

1. VARIABLES: Named references to values in memory
2. DATA TYPES: int, float, str, bool, and None
3. OPERATORS: Arithmetic, comparison, logical, assignment, identity, membership
4. DYNAMIC TYPING: Variables can change type during execution
5. MUTABILITY: 
   - Immutable: int, float, str, bool, tuple (cannot be changed)
   - Mutable: list, dict, set (can be modified in-place)
6. TRUTHY/FALSY: Values that evaluate to True or False in boolean contexts
7. TYPE CASTING: 
   - Explicit: Using constructor functions (int(), str(), etc.)
   - Implicit: Automatic conversion in some operations
8. BASIC I/O:
   - Output: print() function with formatting options
   - Input: input() function (gets user input as string)

Python's flexibility with dynamic typing makes it easy to write code quickly,
but requires careful attention to type-related issues in complex programs.
""")

print("End of Python concepts demonstration.")