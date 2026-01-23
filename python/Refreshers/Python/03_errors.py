"""
COMPREHENSIVE PYTHON ERRORS AND EXCEPTIONS DEMONSTRATION
This script demonstrates Python exception handling with detailed examples.
"""

print("=" * 70)
print("PYTHON ERRORS AND EXCEPTIONS")
print("=" * 70)

# ============================================================================
# SECTION 1: INTRODUCTION TO ERRORS AND EXCEPTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 1: INTRODUCTION TO ERRORS AND EXCEPTIONS")
print("=" * 60)

print("""
1.1 What are Errors and Exceptions?

In Python, errors can be categorized into two main types:

1. SYNTAX ERRORS: Occur when Python parser cannot understand the code.
   - Detected during parsing/compilation
   - Program won't even start executing
   - Example: Missing colon, unmatched parentheses

2. EXCEPTIONS: Occur during program execution (runtime errors).
   - Code syntax is correct, but something goes wrong during execution
   - Program starts but encounters an error condition
   - Example: Dividing by zero, accessing non-existent key

Python uses EXCEPTION HANDLING to gracefully deal with runtime errors
instead of crashing the program.
""")

# ============================================================================
# SECTION 2: COMMON BUILT-IN EXCEPTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: COMMON BUILT-IN EXCEPTIONS")
print("=" * 60)

print("2.1 Hierarchy of Common Exceptions (simplified):")
print("""
BaseException
├── KeyboardInterrupt
├── SystemExit
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── ConnectionError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── NameError
    ├── ImportError
    ├── RuntimeError
    ├── StopIteration
    └── AssertionError
""")

# ----------------------------------------------------------------------------
# DEMONSTRATING COMMON EXCEPTIONS
# ----------------------------------------------------------------------------
print("\n2.2 Demonstrating Common Exceptions:")

print("   ZeroDivisionError - Division by zero:")
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"     Caught ZeroDivisionError: {e}")

print("\n   TypeError - Operation on inappropriate type:")
try:
    result = "hello" + 5
except TypeError as e:
    print(f"     Caught TypeError: {e}")

print("\n   ValueError - Function receives argument of right type but inappropriate value:")
try:
    number = int("not_a_number")
except ValueError as e:
    print(f"     Caught ValueError: {e}")

print("\n   IndexError - Sequence subscript out of range:")
try:
    my_list = [1, 2, 3]
    item = my_list[10]
except IndexError as e:
    print(f"     Caught IndexError: {e}")

print("\n   KeyError - Dictionary key not found:")
try:
    my_dict = {"a": 1, "b": 2}
    value = my_dict["c"]
except KeyError as e:
    print(f"     Caught KeyError: {e}")

print("\n   FileNotFoundError - File doesn't exist:")
try:
    with open("non_existent_file.txt", "r") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"     Caught FileNotFoundError: {e}")

print("\n   AttributeError - Attribute reference or assignment fails:")
try:
    text = "hello"
    text.append("world")
except AttributeError as e:
    print(f"     Caught AttributeError: {e}")

print("\n   NameError - Local or global name not found:")
try:
    print(undefined_variable)
except NameError as e:
    print(f"     Caught NameError: {e}")

print("\n   ImportError - Import statement fails:")
try:
    import non_existent_module
except ImportError as e:
    print(f"     Caught ImportError: {e}")

print("\n   KeyboardInterrupt - User hits interrupt key (Ctrl+C):")
print("     (Simulated - try Ctrl+C during execution to see it)")
# Note: We won't actually trigger this to avoid stopping the script

# ============================================================================
# SECTION 3: BASIC TRY/EXCEPT BLOCKS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: BASIC TRY/EXCEPT BLOCKS")
print("=" * 60)

print("3.1 Basic try-except Structure:")
print("""
Syntax:
try:
    # Code that might raise an exception
    risky_operation()
except ExceptionType:
    # Code to handle the exception
    handle_error()
""")

# ----------------------------------------------------------------------------
# CATCHING SPECIFIC EXCEPTIONS
# ----------------------------------------------------------------------------
print("\n3.2 Catching Specific Exceptions:")

def divide_numbers(a, b):
    """Demonstrate catching specific exceptions."""
    try:
        result = a / b
        print(f"   {a} / {b} = {result}")
    except ZeroDivisionError:
        print(f"   Error: Cannot divide {a} by zero!")
    except TypeError:
        print(f"   Error: Both arguments must be numbers!")

print("   Testing divide_numbers function:")
divide_numbers(10, 2)      # Normal division
divide_numbers(10, 0)      # Zero division
divide_numbers(10, "two")  # Type error

# ----------------------------------------------------------------------------
# CATCHING MULTIPLE EXCEPTIONS
# ----------------------------------------------------------------------------
print("\n3.3 Catching Multiple Exceptions:")

def process_user_input(user_input):
    """Demonstrate catching multiple exceptions."""
    try:
        # Try to convert to number and calculate square
        number = float(user_input)
        square = number ** 2
        print(f"   Square of {number} is {square}")
    except (ValueError, TypeError):
        print(f"   Error: '{user_input}' is not a valid number!")
    except OverflowError:
        print(f"   Error: Result is too large to compute!")

print("   Testing process_user_input function:")
process_user_input("25")        # Valid input
process_user_input("hello")     # ValueError
process_user_input("1e1000")    # Might cause OverflowError

# ----------------------------------------------------------------------------
# CATCHING ALL EXCEPTIONS (GENERALLY NOT RECOMMENDED)
# ----------------------------------------------------------------------------
print("\n3.4 Catching All Exceptions (with caution):")

print("""   
WARNING: Catching all exceptions with bare 'except:' or 'except Exception:'
can hide bugs and make debugging difficult. Use specific exceptions when possible.
""")

def risky_operation():
    """Demonstrate catching all exceptions (with caution)."""
    try:
        # Some risky operation
        result = 10 / 0
    except:  # Bare except - catches EVERYTHING (even KeyboardInterrupt!)
        print("   Caught some exception (bare except)")
    
    try:
        result = 10 / 0
    except Exception:  # Better than bare except, but still broad
        print("   Caught Exception (still quite broad)")
    
    # Best practice: Catch specific exceptions
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("   Caught ZeroDivisionError (specific and preferred)")

risky_operation()

# ============================================================================
# SECTION 4: TRY/EXCEPT/ELSE/FINALLY
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: TRY/EXCEPT/ELSE/FINALLY - Complete Structure")
print("=" * 60)

print("4.1 Complete try-except-else-finally Structure:")
print("""
Syntax:
try:
    # Code that might raise an exception
    risky_operation()
except ExceptionType:
    # Handle specific exception
    handle_error()
else:
    # Execute if NO exception was raised
    on_success()
finally:
    # ALWAYS execute, whether exception occurred or not
    cleanup()
""")

# ----------------------------------------------------------------------------
# ELSE CLAUSE - Executes when NO exception occurs
# ----------------------------------------------------------------------------
print("\n4.2 The else Clause:")

def read_file_safely(filename):
    """Demonstrate try-except-else."""
    try:
        print(f"   Attempting to read '{filename}'...")
        # Simulating file reading
        if filename == "valid.txt":
            content = "File content here"
        else:
            raise FileNotFoundError(f"File '{filename}' not found")
    except FileNotFoundError as e:
        print(f"   Error: {e}")
    else:
        # This runs ONLY if no exception occurred
        print(f"   Success! File content: {content}")
        print("   Processing file content...")
        return content

print("   Testing read_file_safely:")
read_file_safely("valid.txt")
print()
read_file_safely("invalid.txt")

# ----------------------------------------------------------------------------
# FINALLY CLAUSE - ALWAYS executes
# ----------------------------------------------------------------------------
print("\n4.3 The finally Clause:")

def process_data(data):
    """Demonstrate try-except-finally for resource cleanup."""
    print(f"   Processing data: {data}")
    
    try:
        if data == "invalid":
            raise ValueError("Invalid data format")
        result = int(data) * 2
        print(f"   Result: {result}")
        return result
    except ValueError as e:
        print(f"   Error: {e}")
        return None
    finally:
        # This ALWAYS runs, whether successful or not
        print("   Cleanup: Closing resources, releasing memory...")

print("\n   Testing process_data:")
result1 = process_data("10")
print(f"   Function returned: {result1}")
print()
result2 = process_data("invalid")
print(f"   Function returned: {result2}")

# ----------------------------------------------------------------------------
# PRACTICAL EXAMPLE: FILE PROCESSING WITH FINALLY
# ----------------------------------------------------------------------------
print("\n4.4 Practical Example: File Processing with finally:")

def process_file(filename):
    """Demonstrate proper resource cleanup with finally."""
    file = None  # Initialize to None
    try:
        print(f"   Opening file: {filename}")
        # Simulate opening a file
        if filename == "data.txt":
            file = "file_handle_simulation"
            print("   Reading file content...")
            # Simulate reading
            content = "Sample data"
            # Simulate an error during processing
            if "error" in content:
                raise RuntimeError("Error in file content!")
            print(f"   Content: {content}")
        else:
            raise FileNotFoundError(f"File '{filename}' not found")
    except FileNotFoundError as e:
        print(f"   File error: {e}")
    except RuntimeError as e:
        print(f"   Processing error: {e}")
    finally:
        # This ALWAYS executes for cleanup
        if file:
            print("   Closing file...")
            # Actually close the file here
            file = None
        print("   Cleanup complete.")

print("\n   Testing process_file:")
process_file("data.txt")
print()
process_file("missing.txt")

# ============================================================================
# SECTION 5: RAISING EXCEPTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: RAISING EXCEPTIONS")
print("=" * 60)

print("5.1 Raising Exceptions with 'raise':")
print("""
Use the 'raise' statement to explicitly trigger an exception.
This is useful for:
1. Validating input parameters
2. Indicating error conditions
3. Re-raising caught exceptions
""")

# ----------------------------------------------------------------------------
# RAISING BUILT-IN EXCEPTIONS
# ----------------------------------------------------------------------------
print("\n5.2 Raising Built-in Exceptions:")

def calculate_square_root(number):
    """Calculate square root with validation."""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number ** 0.5

print("   Testing calculate_square_root:")
try:
    result = calculate_square_root(16)
    print(f"   Square root of 16 is {result}")
    
    result = calculate_square_root(-4)
    print(f"   Square root of -4 is {result}")
except ValueError as e:
    print(f"   Error: {e}")

# ----------------------------------------------------------------------------
# RAISING WITH ADDITIONAL INFORMATION
# ----------------------------------------------------------------------------
print("\n5.3 Raising Exceptions with Additional Information:")

def process_age(age):
    """Validate age with detailed error messages."""
    if not isinstance(age, (int, float)):
        raise TypeError(f"Age must be a number, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")
    if age > 150:
        raise ValueError(f"Age {age} is not realistic")
    
    print(f"   Age {age} is valid.")
    return age

print("\n   Testing process_age:")
test_cases = [25, -5, 200, "twenty-five"]

for test in test_cases:
    try:
        process_age(test)
    except (ValueError, TypeError) as e:
        print(f"   Error for input {test}: {e}")

# ----------------------------------------------------------------------------
# RE-RAISING EXCEPTIONS
# ----------------------------------------------------------------------------
print("\n5.4 Re-raising Exceptions:")

def process_with_logging(operation, *args):
    """Process operation with logging and re-raise exceptions."""
    print(f"   Starting operation: {operation.__name__}")
    
    try:
        result = operation(*args)
        print(f"   Operation completed successfully")
        return result
    except Exception as e:
        print(f"   ERROR in {operation.__name__}: {type(e).__name__} - {e}")
        print("   Logging error...")
        # Log the error, then re-raise it
        raise  # Re-raise the same exception

def divide(a, b):
    """Simple division function."""
    return a / b

print("\n   Testing process_with_logging with divide:")
try:
    result = process_with_logging(divide, 10, 0)
except ZeroDivisionError as e:
    print(f"   Caught re-raised exception: {e}")

# ============================================================================
# SECTION 6: CUSTOM EXCEPTIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: CUSTOM EXCEPTIONS")
print("=" * 60)

print("6.1 Creating Custom Exceptions:")
print("""
Why create custom exceptions?
1. More specific error types for your application
2. Better error messages
3. Easier to catch specific errors
4. Better code organization

Custom exceptions should inherit from Exception (or its subclasses).
""")

# ----------------------------------------------------------------------------
# BASIC CUSTOM EXCEPTION
# ----------------------------------------------------------------------------
print("\n6.2 Basic Custom Exception:")

class InvalidEmailError(Exception):
    """Exception raised for invalid email addresses."""
    pass

def validate_email(email):
    """Validate email address."""
    if "@" not in email:
        raise InvalidEmailError(f"Invalid email: '{email}' doesn't contain '@'")
    if "." not in email.split("@")[-1]:
        raise InvalidEmailError(f"Invalid email: '{email}' doesn't have domain extension")
    
    print(f"   Email '{email}' is valid.")
    return True

print("   Testing validate_email with custom exception:")
emails = ["user@example.com", "invalid-email", "user@domain"]

for email in emails:
    try:
        validate_email(email)
    except InvalidEmailError as e:
        print(f"   {e}")

# ----------------------------------------------------------------------------
# CUSTOM EXCEPTION WITH ADDITIONAL ATTRIBUTES
# ----------------------------------------------------------------------------
print("\n6.3 Custom Exception with Additional Attributes:")

class InsufficientFundsError(Exception):
    """Exception raised when account has insufficient funds."""
    
    def __init__(self, balance, amount, message="Insufficient funds"):
        self.balance = balance
        self.amount = amount
        self.shortage = amount - balance
        self.message = f"{message}: Balance ${balance:.2f}, tried to withdraw ${amount:.2f}"
        super().__init__(self.message)

class BankAccount:
    """Simple bank account with withdrawal validation."""
    
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    
    def withdraw(self, amount):
        """Withdraw money from account."""
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        
        self.balance -= amount
        print(f"   Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        return amount

print("\n   Testing BankAccount with custom exception:")
account = BankAccount(1000.00)

try:
    account.withdraw(500.00)
    account.withdraw(600.00)  # This should raise an exception
except InsufficientFundsError as e:
    print(f"   {e}")
    print(f"   Shortage: ${e.shortage:.2f}")

# ----------------------------------------------------------------------------
# EXCEPTION HIERARCHY FOR AN APPLICATION
# ----------------------------------------------------------------------------
print("\n6.4 Creating an Exception Hierarchy:")

# Base exception for our application
class ShoppingCartError(Exception):
    """Base exception for shopping cart errors."""
    pass

# Specific exceptions
class ProductNotFoundError(ShoppingCartError):
    """Exception raised when product is not found."""
    pass

class OutOfStockError(ShoppingCartError):
    """Exception raised when product is out of stock."""
    
    def __init__(self, product_name, available, requested):
        self.product_name = product_name
        self.available = available
        self.requested = requested
        message = f"'{product_name}' out of stock. Available: {available}, Requested: {requested}"
        super().__init__(message)

class InvalidQuantityError(ShoppingCartError):
    """Exception raised for invalid quantity."""
    pass

class ShoppingCart:
    """Simple shopping cart with exception handling."""
    
    def __init__(self):
        self.products = {
            "apple": {"price": 1.0, "stock": 10},
            "banana": {"price": 0.5, "stock": 5},
            "orange": {"price": 0.8, "stock": 0},  # Out of stock
        }
    
    def add_product(self, product_name, quantity=1):
        """Add product to cart with validation."""
        if quantity <= 0:
            raise InvalidQuantityError(f"Quantity must be positive: {quantity}")
        
        if product_name not in self.products:
            raise ProductNotFoundError(f"Product '{product_name}' not found")
        
        product = self.products[product_name]
        if quantity > product["stock"]:
            raise OutOfStockError(product_name, product["stock"], quantity)
        
        print(f"   Added {quantity} {product_name}(s) to cart. Price: ${product['price'] * quantity:.2f}")
        return True

print("\n   Testing ShoppingCart with exception hierarchy:")
cart = ShoppingCart()

test_cases = [
    ("apple", 3),      # Valid
    ("banana", -1),    # Invalid quantity
    ("grape", 2),      # Product not found
    ("orange", 1),     # Out of stock
    ("banana", 10),    # Insufficient stock
]

for product_name, quantity in test_cases:
    try:
        cart.add_product(product_name, quantity)
    except InvalidQuantityError as e:
        print(f"   InvalidQuantityError: {e}")
    except ProductNotFoundError as e:
        print(f"   ProductNotFoundError: {e}")
    except OutOfStockError as e:
        print(f"   OutOfStockError: {e}")
        print(f"     Available: {e.available}, Requested: {e.requested}")
    except ShoppingCartError as e:
        print(f"   Generic ShoppingCartError: {e}")

# ============================================================================
# SECTION 7: BEST PRACTICES AND COMMON PATTERNS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: BEST PRACTICES AND COMMON PATTERNS")
print("=" * 60)

print("7.1 Exception Handling Best Practices:")
print("""
1. BE SPECIFIC: Catch specific exceptions, not all exceptions
   Bad: except:  # Catches everything including KeyboardInterrupt
   Good: except ValueError:  # Only catches ValueError

2. DON'T SUPPRESS EXCEPTIONS SILENTLY:
   Bad: 
       try:
           do_something()
       except:
           pass  # Silent failure!
   
   Good:
       try:
           do_something()
       except SpecificError as e:
           log_error(e)
           handle_gracefully()

3. USE ELSE FOR SUCCESS PATHS:
   Use 'else' for code that should run only if no exception occurred

4. ALWAYS CLEAN UP WITH FINALLY:
   Use 'finally' for cleanup code (closing files, releasing resources)

5. PROVIDE MEANINGFUL ERROR MESSAGES:
   Include relevant information in error messages

6. CREATE CUSTOM EXCEPTIONS FOR YOUR DOMAIN:
   Makes your code more readable and maintainable
""")

# ----------------------------------------------------------------------------
# COMMON PATTERNS
# ----------------------------------------------------------------------------
print("\n7.2 Common Exception Handling Patterns:")

print("Pattern 1: Retry with exponential backoff")

import time

def retry_with_backoff(operation, max_retries=3, initial_delay=1):
    """Retry operation with exponential backoff on failure."""
    for attempt in range(max_retries + 1):  # +1 for initial attempt
        try:
            return operation()
        except Exception as e:
            if attempt == max_retries:
                print(f"   Failed after {max_retries} retries. Last error: {e}")
                raise
            delay = initial_delay * (2 ** attempt)  # Exponential backoff
            print(f"   Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)

def unreliable_operation():
    """Simulate an unreliable operation that fails randomly."""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise RuntimeError("Operation failed randomly")
    return "Success!"

print("\n   Testing retry_with_backoff:")
try:
    # Note: This might succeed or fail based on randomness
    result = retry_with_backoff(unreliable_operation, max_retries=3)
    print(f"   Result: {result}")
except RuntimeError as e:
    print(f"   Operation failed despite retries: {e}")

print("\nPattern 2: Context manager pattern")

class DatabaseConnection:
    """Simulate a database connection with context manager."""
    
    def __init__(self, database_name):
        self.database_name = database_name
        self.connected = False
    
    def __enter__(self):
        """Enter context - establish connection."""
        print(f"   Connecting to database: {self.database_name}")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - ensure cleanup."""
        print("   Closing database connection...")
        self.connected = False
        if exc_type is not None:
            print(f"   Error occurred: {exc_val}")
        # Return False to propagate exception, True to suppress it
        return False
    
    def query(self, sql):
        """Execute a query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"   Executing query: {sql}")
        # Simulate query execution
        return f"Results for: {sql}"

print("\n   Testing context manager pattern:")
try:
    with DatabaseConnection("my_database") as db:
        result = db.query("SELECT * FROM users")
        print(f"   {result}")
        # Simulate an error
        raise ValueError("Simulated query error")
except ValueError as e:
    print(f"   Caught error outside context manager: {e}")

print("\nPattern 3: Input validation with multiple attempts")

def get_valid_input(prompt, validation_func, max_attempts=3):
    """Get valid input from user with multiple attempts."""
    for attempt in range(max_attempts):
        try:
            # In real code: user_input = input(prompt)
            # For demo, we'll simulate inputs
            simulated_inputs = ["invalid", "-5", "25"]
            user_input = simulated_inputs[attempt]
            print(f"   Attempt {attempt + 1}: Input='{user_input}'")
            
            # Validate using provided function
            validated = validation_func(user_input)
            print(f"   Valid input received: {validated}")
            return validated
            
        except ValueError as e:
            print(f"   Invalid input: {e}")
            if attempt == max_attempts - 1:
                print(f"   Maximum attempts reached. Using default value.")
                return 0  # Default value
    
    return 0  # Fallback

def validate_positive_integer(value):
    """Validate that input is a positive integer."""
    num = int(value)
    if num <= 0:
        raise ValueError(f"Number must be positive: {num}")
    return num

print("\n   Testing input validation with multiple attempts:")
result = get_valid_input("Enter a positive number: ", validate_positive_integer)
print(f"   Final result: {result}")

# ============================================================================
# SECTION 8: REAL-WORLD EXAMPLE
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 8: REAL-WORLD EXAMPLE - FILE PROCESSING APPLICATION")
print("=" * 60)

# Define custom exceptions for our application
class FileProcessingError(Exception):
    """Base exception for file processing errors."""
    pass

class InvalidFileFormatError(FileProcessingError):
    """Invalid file format."""
    pass

class FileSizeExceededError(FileProcessingError):
    """File size exceeds limit."""
    
    def __init__(self, file_size, max_size):
        self.file_size = file_size
        self.max_size = max_size
        super().__init__(f"File size {file_size} exceeds maximum {max_size}")

class DataValidationError(FileProcessingError):
    """Data validation failed."""
    pass

def process_data_file(file_path, max_size=1024):
    """
    Process a data file with comprehensive error handling.
    
    Args:
        file_path: Path to the data file
        max_size: Maximum file size in bytes
    
    Returns:
        Processed data as list
    
    Raises:
        FileProcessingError: If any processing error occurs
    """
    file_handle = None
    processed_data = []
    
    try:
        print(f"   Starting to process file: {file_path}")
        
        # 1. Check file extension
        if not file_path.endswith('.txt'):
            raise InvalidFileFormatError("Only .txt files are supported")
        
        # 2. Check file size (simulated)
        import random
        file_size = random.randint(500, 1500)
        print(f"   File size: {file_size} bytes")
        
        if file_size > max_size:
            raise FileSizeExceededError(file_size, max_size)
        
        # 3. Open and read file (simulated)
        print("   Reading file content...")
        file_handle = "simulated_file_handle"
        
        # Simulate file content
        lines = [
            "Alice,25,Engineer",
            "Bob,30,Designer",
            "Charlie,invalid,Manager",  # Invalid age
            "Diana,35,Developer",
        ]
        
        # 4. Process each line
        for line_num, line in enumerate(lines, 1):
            try:
                # Parse CSV line
                parts = line.strip().split(',')
                if len(parts) != 3:
                    raise DataValidationError(f"Line {line_num}: Expected 3 columns, got {len(parts)}")
                
                name, age_str, occupation = parts
                
                # Validate age
                try:
                    age = int(age_str)
                    if age < 18 or age > 100:
                        raise DataValidationError(f"Line {line_num}: Age {age} out of valid range (18-100)")
                except ValueError:
                    raise DataValidationError(f"Line {line_num}: Invalid age '{age_str}'")
                
                # Validate occupation
                valid_occupations = {"Engineer", "Designer", "Manager", "Developer"}
                if occupation not in valid_occupations:
                    raise DataValidationError(f"Line {line_num}: Invalid occupation '{occupation}'")
                
                # Add to processed data
                processed_data.append({
                    "name": name,
                    "age": age,
                    "occupation": occupation,
                    "line_num": line_num
                })
                
                print(f"     Processed line {line_num}: {name}, {age}, {occupation}")
                
            except DataValidationError as e:
                print(f"     Skipping line {line_num}: {e}")
                # Continue processing other lines
                continue
        
        # 5. Validate we have some data
        if not processed_data:
            raise DataValidationError("No valid data found in file")
        
        print(f"   Successfully processed {len(processed_data)} records")
        return processed_data
        
    except (InvalidFileFormatError, FileSizeExceededError) as e:
        # These are fatal errors - we can't proceed
        print(f"   Fatal error: {e}")
        raise  # Re-raise for caller to handle
    
    except Exception as e:
        # Catch any other unexpected errors
        print(f"   Unexpected error: {type(e).__name__} - {e}")
        raise FileProcessingError(f"Failed to process file: {e}") from e
    
    finally:
        # Always clean up
        if file_handle:
            print("   Closing file handle...")
            # Actually close the file here
        print("   File processing cleanup complete.")

print("\n   Testing the file processing application:")

test_cases = [
    ("data.txt", 1024),      # Valid file (might randomly exceed size)
    ("data.csv", 1024),      # Invalid format
    ("large.txt", 500),      # Too large (simulated)
]

for file_path, max_size in test_cases:
    print(f"\n   Processing {file_path} with max size {max_size}:")
    try:
        result = process_data_file(file_path, max_size)
        print(f"   Success! Processed {len(result)} records.")
    except InvalidFileFormatError as e:
        print(f"   Format error: {e}")
    except FileSizeExceededError as e:
        print(f"   Size error: {e}")
    except FileProcessingError as e:
        print(f"   Processing error: {e}")
    except Exception as e:
        print(f"   Unexpected error: {type(e).__name__} - {e}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
KEY CONCEPTS COVERED:

1. ERROR TYPES:
   - Syntax errors: Caught during parsing, prevent execution
   - Exceptions: Runtime errors, can be caught and handled

2. COMMON BUILT-IN EXCEPTIONS:
   - ZeroDivisionError, TypeError, ValueError
   - IndexError, KeyError, FileNotFoundError
   - Know the exception hierarchy

3. EXCEPTION HANDLING:
   - try: Code that might raise exceptions
   - except: Handle specific exceptions
   - else: Execute if NO exception occurred
   - finally: ALWAYS execute (for cleanup)

4. RAISING EXCEPTIONS:
   - Use 'raise' to trigger exceptions
   - Can raise built-in or custom exceptions
   - Use 'raise' without arguments to re-raise

5. CUSTOM EXCEPTIONS:
   - Inherit from Exception or its subclasses
   - Add custom attributes for more context
   - Create exception hierarchies for complex applications

BEST PRACTICES:
1. Be specific in what exceptions you catch
2. Don't suppress exceptions silently
3. Use finally for cleanup operations
4. Provide meaningful error messages
5. Create custom exceptions for your domain
6. Use context managers for resource management

REMEMBER:
- Exception handling makes your code more robust
- It allows graceful degradation instead of crashes
- Well-designed error handling is a hallmark of professional code
- "It's easier to ask for forgiveness than permission" (EAFP) vs
  "Look before you leap" (LBYL) - Python favors EAFP
""")

print("\n" + "=" * 70)
print("END OF ERRORS AND EXCEPTIONS DEMONSTRATION")
print("=" * 70)