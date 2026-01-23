"""
PYTHON CONTEXT MANAGERS: COMPREHENSIVE GUIDE
Covers with statement, context manager protocol, custom managers, and contextlib utilities.
"""

import contextlib
import time
import os
import tempfile
import sqlite3
from typing import Any, Optional, Generator, List, Dict
from pathlib import Path
import threading
import sys

print("=" * 60)
print("PYTHON CONTEXT MANAGERS")
print("=" * 60)
print("""
Context managers provide a clean way to manage resources.
They ensure proper setup and teardown, even if exceptions occur.
""")

# ============================================================================
# PART 1: THE 'WITH' STATEMENT AND CONTEXT MANAGER PROTOCOL
# ============================================================================

print("\n1. THE 'WITH' STATEMENT AND CONTEXT MANAGER PROTOCOL")
print("-" * 40)

# ============================================================================
# 1.1 Basic 'with' Statement
# ============================================================================

print("\n1.1 Basic 'with' Statement")
print("-" * 40)

print("""
The 'with' statement ensures proper resource management:
• Resources are acquired before the block
• Resources are released after the block
• Resources are released even if exceptions occur
""")

# Most common example: file handling
print("\nFile handling with 'with' statement:")
with open('example.txt', 'w') as file:
    file.write("Hello, World!\n")
    file.write("This is a test file.\n")

# Read it back
with open('example.txt', 'r') as file:
    content = file.read()
    print("File content:")
    print(content)

# Clean up
os.remove('example.txt')

print("\nEquivalent without 'with' (more error-prone):")
file = None
try:
    file = open('example.txt', 'w')
    file.write("Without with statement\n")
except Exception as e:
    print(f"Error: {e}")
finally:
    if file:
        file.close()

# ============================================================================
# 1.2 Context Manager Protocol
# ============================================================================

print("\n1.2 Context Manager Protocol")
print("-" * 40)

print("""
Context managers implement two methods:
1. __enter__(self): 
   - Called when entering the 'with' block
   - Returns the resource to be managed
   
2. __exit__(self, exc_type, exc_value, traceback):
   - Called when exiting the 'with' block
   - Handles cleanup
   - Returns True to suppress exceptions, False to propagate them
""")

# ============================================================================
# PART 2: CREATING CUSTOM CONTEXT MANAGERS (CLASS-BASED)
# ============================================================================

print("\n" + "=" * 60)
print("2. CREATING CUSTOM CONTEXT MANAGERS (CLASS-BASED)")
print("=" * 60)

# ============================================================================
# 2.1 Simple Timer Context Manager
# ============================================================================

print("\n2.1 Simple Timer Context Manager")
print("-" * 40)

class Timer:
    """Context manager for timing code execution."""
    
    def __init__(self, name: str = "Code block"):
        self.name = name
        self.start_time = None
        self.elapsed_time = None
    
    def __enter__(self) -> 'Timer':
        """Start the timer."""
        print(f"Starting timer for: {self.name}")
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Stop the timer and print results."""
        self.elapsed_time = time.perf_counter() - self.start_time
        print(f"Finished {self.name} in {self.elapsed_time:.4f} seconds")
        
        # Don't suppress exceptions
        return False
    
    def get_elapsed(self) -> float:
        """Get elapsed time."""
        if self.elapsed_time is None:
            raise RuntimeError("Timer hasn't finished yet")
        return self.elapsed_time

print("Using Timer context manager:")
with Timer("Fibonacci calculation"):
    # Simulate some work
    def fib(n):
        return n if n <= 1 else fib(n-1) + fib(n-2)
    result = fib(15)  # Small number to avoid long computation
    print(f"  Fibonacci(15) = {result}")

# ============================================================================
# 2.2 Database Connection Manager
# ============================================================================

print("\n2.2 Database Connection Manager")
print("-" * 40)

class DatabaseConnection:
    """Context manager for database connections with automatic commit/rollback."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self) -> 'DatabaseConnection':
        """Establish database connection."""
        print(f"Connecting to database: {self.db_path}")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Close connection, commit on success or rollback on failure."""
        try:
            if exc_type is None:
                # No exception occurred
                print("Committing transaction...")
                self.connection.commit()
                print("Transaction committed successfully")
            else:
                # Exception occurred
                print(f"Exception occurred: {exc_value}")
                print("Rolling back transaction...")
                self.connection.rollback()
                print("Transaction rolled back")
        finally:
            # Always close the connection
            print("Closing database connection...")
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        
        # Don't suppress exceptions
        return False
    
    def execute(self, query: str, params: tuple = ()) -> Any:
        """Execute a SQL query."""
        if not self.cursor:
            raise RuntimeError("Database not connected")
        return self.cursor.execute(query, params)

# Create a temporary database
temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name

print("Using DatabaseConnection context manager:")

# Successful transaction
with DatabaseConnection(temp_db) as db:
    print("\nCreating table...")
    db.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    
    print("Inserting data...")
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("Alice", "alice@example.com"))
    db.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("Bob", "bob@example.com"))
    
    print("Querying data...")
    db.execute("SELECT * FROM users")
    users = db.cursor.fetchall()
    for user in users:
        print(f"  User: {user}")

# Failed transaction (simulated)
print("\n\nSimulating failed transaction:")
try:
    with DatabaseConnection(temp_db) as db:
        print("Inserting data with duplicate email (should fail)...")
        db.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                   ("Charlie", "alice@example.com"))  # Duplicate email
except sqlite3.IntegrityError as e:
    print(f"  Expected error: {e}")

# Verify data wasn't inserted
with DatabaseConnection(temp_db) as db:
    db.execute("SELECT * FROM users")
    users = db.cursor.fetchall()
    print(f"\nUsers in database: {len(users)} (Charlie shouldn't be there)")

# Clean up
os.remove(temp_db)

# ============================================================================
# 2.3 Thread Lock Manager
# ============================================================================

print("\n2.3 Thread Lock Manager")
print("-" * 40)

class ThreadSafeCounter:
    """Thread-safe counter using context manager for locks."""
    
    def __init__(self, initial_value: int = 0):
        self.value = initial_value
        self.lock = threading.Lock()
    
    def increment(self, amount: int = 1):
        """Increment counter in a thread-safe manner."""
        with self.lock:
            old_value = self.value
            time.sleep(0.001)  # Simulate some work
            self.value = old_value + amount
            return self.value
    
    def get_value(self) -> int:
        """Get current value."""
        with self.lock:
            return self.value

class LockContext:
    """Context manager for acquiring and releasing locks."""
    
    def __init__(self, lock: threading.Lock):
        self.lock = lock
    
    def __enter__(self):
        """Acquire the lock."""
        print("  Acquiring lock...")
        self.lock.acquire()
        print("  Lock acquired")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Release the lock."""
        print("  Releasing lock...")
        self.lock.release()
        print("  Lock released")
        return False

print("Using lock context manager for thread safety:")

counter = ThreadSafeCounter()

def worker(worker_id: int, iterations: int):
    """Worker function that increments counter."""
    for i in range(iterations):
        # Using lock context manager
        with LockContext(counter.lock):
            old_value = counter.value
            time.sleep(0.001)
            counter.value = old_value + 1
        print(f"  Worker {worker_id}: Incremented to {counter.value}")

# Create and start threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i, 3))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print(f"\nFinal counter value: {counter.value} (should be 9)")

# ============================================================================
# 2.4 Directory Change Manager
# ============================================================================

print("\n2.4 Directory Change Manager")
print("-" * 40)

class ChangeDirectory:
    """Context manager for temporarily changing directories."""
    
    def __init__(self, new_path: str):
        self.new_path = Path(new_path).resolve()
        self.old_path = None
    
    def __enter__(self) -> 'ChangeDirectory':
        """Change to new directory."""
        self.old_path = Path.cwd()
        print(f"Changing directory: {self.old_path} -> {self.new_path}")
        
        if not self.new_path.exists():
            self.new_path.mkdir(parents=True, exist_ok=True)
        
        os.chdir(self.new_path)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Change back to original directory."""
        print(f"Changing back to: {self.old_path}")
        os.chdir(self.old_path)
        
        # Don't suppress exceptions
        return False

print("Using ChangeDirectory context manager:")

# Create a temporary directory
temp_dir = tempfile.mkdtemp()
sub_dir = os.path.join(temp_dir, "subfolder")

original_dir = os.getcwd()
print(f"Original directory: {original_dir}")

with ChangeDirectory(sub_dir):
    print(f"Current directory: {os.getcwd()}")
    
    # Create a file in the temporary directory
    with open("temp_file.txt", "w") as f:
        f.write("Created in temporary directory\n")
    
    print(f"Created file: {os.listdir('.')}")

print(f"Back in original directory: {os.getcwd()}")
print(f"Original directory preserved: {os.getcwd() == original_dir}")

# Clean up
import shutil
shutil.rmtree(temp_dir)

# ============================================================================
# PART 3: CREATING CONTEXT MANAGERS WITH @contextmanager
# ============================================================================

print("\n" + "=" * 60)
print("3. CREATING CONTEXT MANAGERS WITH @contextmanager")
print("=" * 60)

print("""
The @contextmanager decorator from contextlib allows creating
context managers using generator functions instead of classes.

Structure:
@contextlib.contextmanager
def context_manager():
    # Setup code (before yield)
    yield resource
    # Cleanup code (after yield)
""")

# ============================================================================
# 3.1 Timer with @contextmanager
# ============================================================================

print("\n3.1 Timer with @contextmanager")
print("-" * 40)

@contextlib.contextmanager
def timer(name: str = "Code block") -> Generator[None, None, None]:
    """Context manager for timing code execution."""
    print(f"Starting timer for: {name}")
    start_time = time.perf_counter()
    
    try:
        yield  # Code block executes here
    finally:
        elapsed_time = time.perf_counter() - start_time
        print(f"Finished {name} in {elapsed_time:.4f} seconds")

print("Using @contextmanager timer:")
with timer("Slow operation"):
    time.sleep(0.1)
    print("  Operation completed")

# ============================================================================
# 3.2 Temporary File with @contextmanager
# ============================================================================

print("\n3.2 Temporary File with @contextmanager")
print("-" * 40)

@contextlib.contextmanager
def temporary_file(content: str = "", suffix: str = ".tmp") -> Generator[Path, None, None]:
    """Create a temporary file with content, delete it afterwards."""
    import tempfile
    
    # Create temporary file
    temp_fd, temp_path = tempfile.mkstemp(suffix=suffix, text=True)
    
    try:
        # Write content if provided
        if content:
            with os.fdopen(temp_fd, 'w') as f:
                f.write(content)
        else:
            os.close(temp_fd)
        
        print(f"Created temporary file: {temp_path}")
        yield Path(temp_path)
        
    finally:
        # Always clean up
        print(f"Deleting temporary file: {temp_path}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

print("Using @contextmanager for temporary files:")

with temporary_file("Hello, temporary world!\n", suffix=".txt") as temp_file:
    print(f"  Temporary file path: {temp_file}")
    
    # Read the content back
    with open(temp_file, 'r') as f:
        content = f.read()
        print(f"  File content: {content.strip()}")
    
    # Do some processing
    print(f"  File exists: {temp_file.exists()}")
    print(f"  File size: {temp_file.stat().st_size} bytes")

print(f"  File deleted: {not temp_file.exists()}")

# ============================================================================
# 3.3 Database Transaction with @contextmanager
# ============================================================================

print("\n3.3 Database Transaction with @contextmanager")
print("-" * 40)

@contextlib.contextmanager
def database_transaction(db_path: str) -> Generator[sqlite3.Cursor, None, None]:
    """Context manager for database transactions with auto-commit/rollback."""
    print(f"Opening database: {db_path}")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    try:
        yield cursor
        # If we get here, no exception occurred
        print("Committing transaction...")
        connection.commit()
        print("Transaction committed successfully")
    except Exception as e:
        # Exception occurred
        print(f"Exception occurred: {e}")
        print("Rolling back transaction...")
        connection.rollback()
        print("Transaction rolled back")
        raise  # Re-raise the exception
    finally:
        # Always close the connection
        print("Closing database connection...")
        cursor.close()
        connection.close()

# Create a temporary database
temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name

print("Using @contextmanager for database transactions:")

# Successful transaction
try:
    with database_transaction(temp_db) as cursor:
        print("\nCreating table...")
        cursor.execute("""
            CREATE IF NOT EXISTS TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        
        print("Inserting products...")
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", 
                       ("Laptop", 999.99))
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", 
                       ("Mouse", 49.99))
        
        print("Querying products...")
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            print(f"  Product: {row}")
except Exception as e:
    print(f"Error: {e}")

# Clean up
os.remove(temp_db)

# ============================================================================
# 3.4 Suppressing Exceptions with @contextmanager
# ============================================================================

print("\n3.4 Suppressing Exceptions with @contextmanager")
print("-" * 40)

@contextlib.contextmanager
def suppress_exceptions(*exception_types):
    """Context manager that suppresses specified exceptions."""
    try:
        yield
    except exception_types as e:
        print(f"Suppressed exception: {type(e).__name__}: {e}")
    except Exception as e:
        # Don't suppress other exceptions
        raise

print("Using @contextmanager to suppress exceptions:")

with suppress_exceptions(ValueError, ZeroDivisionError):
    print("  This will work fine")
    result = 10 / 2
    print(f"  Result: {result}")

print("\nTrying division by zero (suppressed):")
with suppress_exceptions(ZeroDivisionError):
    result = 10 / 0  # This would normally raise ZeroDivisionError
    print(f"  Result: {result}")  # Never reached

print("\nTrying invalid conversion (suppressed):")
with suppress_exceptions(ValueError):
    number = int("not a number")  # This would raise ValueError
    print(f"  Number: {number}")  # Never reached

print("\nDifferent exception type (not suppressed):")
try:
    with suppress_exceptions(ValueError):
        raise TypeError("This is a TypeError")
except TypeError as e:
    print(f"  Caught exception: {e}")

# ============================================================================
# PART 4: CONTEXTLIB UTILITIES
# ============================================================================

print("\n" + "=" * 60)
print("4. CONTEXTLIB UTILITIES")
print("=" * 60)

print("""
contextlib provides several utilities for working with context managers:
1. closing() - Ensures an object's close() method is called
2. suppress() - Suppresses specified exceptions
3. redirect_stdout/stderr - Redirects output
4. nullcontext() - Does nothing (placeholder)
5. ExitStack - Manages multiple context managers dynamically
""")

# ============================================================================
# 4.1 closing() - Ensuring Cleanup
# ============================================================================

print("\n4.1 closing() - Ensuring Cleanup")
print("-" * 40)

class NetworkConnection:
    """Simulated network connection."""
    
    def __init__(self, address: str):
        self.address = address
        self.connected = False
    
    def connect(self):
        """Simulate connecting."""
        print(f"Connecting to {self.address}...")
        self.connected = True
        return self
    
    def send(self, data: str):
        """Simulate sending data."""
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"Sending data: {data}")
        return f"Sent: {data}"
    
    def close(self):
        """Simulate closing connection."""
        if self.connected:
            print(f"Closing connection to {self.address}")
            self.connected = False

print("Using closing() to ensure cleanup:")

# Without closing() - might forget to call close()
print("\nWithout closing():")
conn = NetworkConnection("example.com").connect()
try:
    print(conn.send("Hello"))
finally:
    conn.close()  # Easy to forget!

# With closing() - automatically calls close()
print("\nWith closing():")
with contextlib.closing(NetworkConnection("example.com").connect()) as conn:
    print(conn.send("Hello"))
# Connection automatically closed here

# ============================================================================
# 4.2 suppress() - Exception Suppression
# ============================================================================

print("\n4.2 suppress() - Exception Suppression")
print("-" * 40)

print("""
suppress() is a built-in context manager that suppresses specified exceptions.
It's cleaner than try-except-pass blocks.
""")

print("Using suppress() to handle expected exceptions:")

# Cleaning up files that may or may not exist
files_to_delete = ["file1.txt", "file2.txt", "file3.txt"]

print(f"\nAttempting to delete files: {files_to_delete}")
for filename in files_to_delete:
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)
        print(f"  Deleted: {filename}")

print("\nMathematical operations with potential errors:")
with contextlib.suppress(ZeroDivisionError, ValueError):
    result = 10 / 0
    print(f"Division result: {result}")  # Never reached

with contextlib.suppress(ValueError):
    number = int("invalid")
    print(f"Parsed number: {number}")  # Never reached

print("  Operations completed (exceptions suppressed)")

# ============================================================================
# 4.3 redirect_stdout/stderr - Output Redirection
# ============================================================================

print("\n4.3 redirect_stdout/stderr - Output Redirection")
print("-" * 40)

print("Using redirect_stdout to capture output:")

# Capture print output
output_buffer = []

class StringBuffer:
    """Custom writeable object to capture output."""
    def write(self, text):
        output_buffer.append(text)
    
    def get_value(self):
        return ''.join(output_buffer).strip()

buffer = StringBuffer()

print("Original output:")
print("This goes to the console")

print("\nRedirected output:")
with contextlib.redirect_stdout(buffer):
    print("This is captured")
    print("Not shown in console")
    
    # Function that prints
    def greet(name):
        print(f"Hello, {name}!")
    
    greet("Alice")

print("Back to console output")
print(f"\nCaptured output: '{buffer.get_value()}'")

# Redirect stderr example
print("\nUsing redirect_stderr:")

import warnings

with contextlib.redirect_stderr(buffer):
    warnings.warn("This is a warning message")
    print("Error output captured", file=sys.stderr)

print(f"Captured stderr: '{buffer.get_value()}'")

# ============================================================================
# 4.4 nullcontext() - Placeholder Context Manager
# ============================================================================

print("\n4.4 nullcontext() - Placeholder Context Manager")
print("-" * 40)

print("""
nullcontext() is useful when you need a context manager but don't 
actually need to manage any resources. It's often used in conditional 
contexts or API compatibility.
""")

def process_file(filepath: str, use_lock: bool = False):
    """Process a file, optionally with a lock."""
    
    # Choose context manager based on condition
    if use_lock:
        lock = threading.Lock()
        cm = LockContext(lock)  # Real lock context
    else:
        cm = contextlib.nullcontext()  # Do-nothing context
    
    with cm:
        print(f"Processing file: {filepath}")
        # Simulate file processing
        time.sleep(0.01)
        print(f"Finished processing: {filepath}")

print("Using nullcontext() for optional locking:")
process_file("data.txt", use_lock=False)
print()
process_file("data.txt", use_lock=True)

# Another example: API compatibility
print("\nUsing nullcontext() for API compatibility:")

def api_call(use_compression: bool = True):
    """Make an API call with optional compression."""
    
    # Choose compression context based on parameter
    if use_compression:
        # Real compression context (simulated)
        @contextlib.contextmanager
        def compression_context():
            print("  Enabling compression...")
            yield
            print("  Disabling compression...")
        cm = compression_context()
    else:
        cm = contextlib.nullcontext()
    
    with cm:
        print("  Making API call...")
        # Simulate API call
        time.sleep(0.01)
        print("  API call completed")

api_call(use_compression=True)
print()
api_call(use_compression=False)

# ============================================================================
# 4.5 ExitStack - Managing Multiple Context Managers
# ============================================================================

print("\n4.5 ExitStack - Managing Multiple Context Managers")
print("-" * 40)

print("""
ExitStack allows managing multiple context managers dynamically.
Useful when you don't know in advance how many resources you'll need.
""")

def process_multiple_files(filepaths: List[str], output_dir: str):
    """
    Process multiple files, opening them all at once.
    All files are properly closed even if errors occur.
    """
    with contextlib.ExitStack() as stack:
        print(f"Processing {len(filepaths)} files...")
        
        # Open all files
        files = []
        for filepath in filepaths:
            print(f"  Opening: {filepath}")
            file = stack.enter_context(open(filepath, 'r'))
            files.append(file)
        
        # Create output directory if needed
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each file
        for i, file in enumerate(files):
            try:
                content = file.read()
                output_path = os.path.join(output_dir, f"processed_{i}.txt")
                
                # Open output file (also managed by ExitStack)
                output_file = stack.enter_context(open(output_path, 'w'))
                output_file.write(f"PROCESSED: {content.upper()}")
                
                print(f"  Processed: {filepaths[i]} -> {output_path}")
                
            except Exception as e:
                print(f"  Error processing {filepaths[i]}: {e}")
        
        print("All files processed and closed automatically")

# Create test files
test_dir = tempfile.mkdtemp()
file_paths = []
for i in range(3):
    filepath = os.path.join(test_dir, f"input_{i}.txt")
    with open(filepath, 'w') as f:
        f.write(f"Content of file {i}\nLine 2 of file {i}")
    file_paths.append(filepath)

output_dir = os.path.join(test_dir, "processed")

print("Using ExitStack to manage multiple files:")
process_multiple_files(file_paths, output_dir)

print(f"\nCreated files in: {test_dir}")
for root, dirs, files in os.walk(test_dir):
    for file in files:
        path = os.path.join(root, file)
        print(f"  {os.path.relpath(path, test_dir)}")

# Clean up
shutil.rmtree(test_dir)

# ============================================================================
# 4.6 Async Context Managers (Python 3.7+)
# ============================================================================

print("\n4.6 Async Context Managers (Python 3.7+)")
print("-" * 40)

print("""
Python 3.7+ supports asynchronous context managers for async/await code.
They use __aenter__() and __aexit__() methods.
""")

# Note: We'll simulate this since we're not in an async environment
class AsyncDatabaseConnection:
    """Simulated async database connection."""
    
    async def __aenter__(self):
        print("  (Async) Connecting to database...")
        # Simulate async connection
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        print("  (Async) Closing database connection...")
        # Simulate async cleanup
        return False
    
    async def query(self, sql: str):
        print(f"  (Async) Executing query: {sql}")
        # Simulate async query
        return "query results"

print("Async context manager pattern (conceptual):")
print("""
async with AsyncDatabaseConnection() as db:
    result = await db.query("SELECT * FROM users")
    print(result)
""")

# contextlib also provides @asynccontextmanager
print("\n@asynccontextmanager for async context managers:")
print("""
@contextlib.asynccontextmanager
async def async_timer(name):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name} took {time.time() - start:.2f}s")
""")

# ============================================================================
# PART 5: REAL-WORLD EXAMPLES AND PATTERNS
# ============================================================================

print("\n" + "=" * 60)
print("5. REAL-WORLD EXAMPLES AND PATTERNS")
print("=" * 60)

# ============================================================================
# 5.1 Configuration Management
# ============================================================================

print("\n5.1 Configuration Management")
print("-" * 40)

class TemporaryConfiguration:
    """Temporarily modify configuration settings."""
    
    def __init__(self, **settings):
        self.settings = settings
        self.original_values = {}
    
    def __enter__(self):
        """Save original values and apply new settings."""
        import configparser
        
        # Simulate configuration
        self.config = {
            'debug': False,
            'timeout': 30,
            'retries': 3,
            'log_level': 'INFO'
        }
        
        # Save original values
        for key in self.settings:
            if key in self.config:
                self.original_values[key] = self.config[key]
        
        # Apply new settings
        self.config.update(self.settings)
        
        print("Configuration updated:")
        for key, value in self.settings.items():
            print(f"  {key}: {self.original_values.get(key)} -> {value}")
        
        return self.config
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Restore original configuration."""
        # Restore original values
        self.config.update(self.original_values)
        
        print("\nConfiguration restored:")
        for key in self.original_values:
            print(f"  {key}: {self.config[key]}")
        
        return False

print("Temporarily modifying configuration:")
with TemporaryConfiguration(debug=True, timeout=60, log_level='DEBUG'):
    print("\n  Running with temporary configuration...")
    # Code that uses the temporary configuration
    print("  Debug mode enabled")
    print("  Timeout set to 60 seconds")
    print("  Log level: DEBUG")

print("\nBack to original configuration")

# ============================================================================
# 5.2 Resource Pooling
# ============================================================================

print("\n5.2 Resource Pooling")
print("-" * 40)

class ConnectionPool:
    """Simple connection pool using context managers."""
    
    def __init__(self, max_connections: int = 5):
        self.max_connections = max_connections
        self.active_connections = 0
        self.waiting_queue = []
        self.lock = threading.Lock()
    
    @contextlib.contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        with self.lock:
            if self.active_connections >= self.max_connections:
                # Pool is full, wait for a connection
                print(f"  Pool full ({self.active_connections}/{self.max_connections}), waiting...")
                event = threading.Event()
                self.waiting_queue.append(event)
        
        # Wait if necessary
        if 'event' in locals():
            event.wait()
        
        with self.lock:
            self.active_connections += 1
        
        print(f"  Connection acquired ({self.active_connections}/{self.max_connections} active)")
        
        try:
            # Simulate a connection
            connection = {"id": id(self), "active": True}
            yield connection
        finally:
            # Return connection to pool
            with self.lock:
                self.active_connections -= 1
                
                # Notify waiting threads if any
                if self.waiting_queue:
                    event = self.waiting_queue.pop(0)
                    event.set()
                
                print(f"  Connection released ({self.active_connections}/{self.max_connections} active)")

print("Connection pool with context managers:")

pool = ConnectionPool(max_connections=2)

def worker(worker_id: int, duration: float):
    """Worker function that uses connections."""
    with pool.get_connection() as conn:
        print(f"  Worker {worker_id}: Using connection {conn['id']}")
        time.sleep(duration)
        print(f"  Worker {worker_id}: Finished")

# Create workers that will contend for connections
threads = []
for i in range(4):
    t = threading.Thread(target=worker, args=(i, 0.5))
    threads.append(t)
    t.start()

# Wait for all workers to complete
for t in threads:
    t.join()

# ============================================================================
# 5.3 Nested Context Managers
# ============================================================================

print("\n5.3 Nested Context Managers")
print("-" * 40)

print("Nesting multiple context managers for complex operations:")

@contextlib.contextmanager
def log_operation(operation_name: str):
    """Log the start and end of an operation."""
    print(f"[START] {operation_name}")
    start_time = time.perf_counter()
    
    try:
        yield
    finally:
        elapsed_time = time.perf_counter() - start_time
        print(f"[END] {operation_name} - took {elapsed_time:.4f}s")

@contextlib.contextmanager  
def indent_output(indent_level: int = 1):
    """Indent output within a context."""
    import sys
    original_write = sys.stdout.write
    
    def indented_write(text):
        if text.strip():  # Only indent non-empty lines
            original_write("  " * indent_level + text)
        else:
            original_write(text)
    
    sys.stdout.write = indented_write
    try:
        yield
    finally:
        sys.stdout.write = original_write

print("Complex operation with nested context managers:")
with log_operation("Data Processing Pipeline"):
    with indent_output():
        print("Starting pipeline...")
        
        with log_operation("Step 1: Data Extraction"):
            with indent_output(2):
                print("Connecting to source...")
                time.sleep(0.05)
                print("Extracting data...")
                time.sleep(0.1)
                print("Data extracted")
        
        with log_operation("Step 2: Data Transformation"):
            with indent_output(2):
                print("Cleaning data...")
                time.sleep(0.05)
                print("Transforming data...")
                time.sleep(0.1)
                print("Data transformed")
        
        with log_operation("Step 3: Data Loading"):
            with indent_output(2):
                print("Connecting to destination...")
                time.sleep(0.05)
                print("Loading data...")
                time.sleep(0.1)
                print("Data loaded")
        
        print("Pipeline completed")

# ============================================================================
# 5.4 Context Manager for Testing
# ============================================================================

print("\n5.4 Context Manager for Testing")
print("-" * 40)

class TemporaryEnvironment:
    """Temporarily modify environment variables for testing."""
    
    def __init__(self, **env_vars):
        self.env_vars = env_vars
        self.original_values = {}
    
    def __enter__(self):
        """Set environment variables."""
        import os
        
        for key, value in self.env_vars.items():
            # Save original value if it exists
            if key in os.environ:
                self.original_values[key] = os.environ[key]
            else:
                self.original_values[key] = None
            
            # Set new value
            os.environ[key] = str(value)
        
        print("Environment variables set:")
        for key, value in self.env_vars.items():
            print(f"  {key}={value}")
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Restore original environment variables."""
        import os
        
        for key, original_value in self.original_values.items():
            if original_value is None:
                # Variable didn't exist before
                if key in os.environ:
                    del os.environ[key]
            else:
                # Restore original value
                os.environ[key] = original_value
        
        print("\nEnvironment variables restored")
        return False

print("Using context manager for testing environment variables:")

# Save original value
original_home = os.environ.get('HOME', 'not set')

with TemporaryEnvironment(HOME="/tmp/test_home", DEBUG="1", TEST_MODE="true"):
    print(f"\n  Inside context:")
    print(f"  HOME: {os.environ.get('HOME')}")
    print(f"  DEBUG: {os.environ.get('DEBUG')}")
    print(f"  TEST_MODE: {os.environ.get('TEST_MODE')}")
    
    # Simulate test code that uses these variables
    if os.environ.get('TEST_MODE') == 'true':
        print("  Running in test mode")

print(f"\nOutside context:")
print(f"  HOME restored to: {os.environ.get('HOME')}")
print(f"  (Original was: {original_home})")

# ============================================================================
# 5.5 Context Manager for Benchmarking
# ============================================================================

print("\n5.5 Context Manager for Benchmarking")
print("-" * 40)

class Benchmark:
    """Context manager for benchmarking code with multiple runs."""
    
    def __init__(self, name: str, num_runs: int = 100):
        self.name = name
        self.num_runs = num_runs
        self.times = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if not self.times:
            return False
        
        import statistics
        
        avg = statistics.mean(self.times)
        std = statistics.stdev(self.times) if len(self.times) > 1 else 0
        min_time = min(self.times)
        max_time = max(self.times)
        
        print(f"\nBenchmark: {self.name}")
        print(f"  Runs: {self.num_runs}")
        print(f"  Average: {avg:.6f}s")
        print(f"  Std Dev: {std:.6f}s")
        print(f"  Min: {min_time:.6f}s")
        print(f"  Max: {max_time:.6f}s")
        
        return False
    
    def run(self, func, *args, **kwargs):
        """Run a function multiple times and record times."""
        for i in range(self.num_runs):
            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()
            self.times.append(end_time - start_time)
        
        return self

print("Benchmarking with context manager:")

def fast_function():
    """A fast function."""
    return sum(range(1000))

def slow_function():
    """A slower function."""
    total = 0
    for i in range(10000):
        total += i
    return total

with Benchmark("Fast Function", num_runs=1000) as bench:
    bench.run(fast_function)

with Benchmark("Slow Function", num_runs=100) as bench:
    bench.run(slow_function)

# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("CONTEXT MANAGERS: KEY TAKEAWAYS")
print("=" * 60)

summary = """
1. CORE CONCEPTS:
   • Context managers ensure proper resource management
   • They implement __enter__() and __exit__() methods
   • The 'with' statement automatically calls these methods
   • Resources are cleaned up even if exceptions occur

2. CREATING CONTEXT MANAGERS:
   • Class-based: Implement __enter__() and __exit__()
   • Function-based: Use @contextmanager decorator with yield
   • Choose based on complexity and preference

3. CONTEXTLIB UTILITIES:
   • closing(): Ensure close() is called
   • suppress(): Suppress specific exceptions
   • redirect_stdout/stderr: Redirect output
   • nullcontext(): Do-nothing placeholder
   • ExitStack: Manage multiple contexts dynamically

4. COMMON USE CASES:
   • File I/O: Automatic closing
   • Database connections: Auto commit/rollback
   • Locks: Automatic acquisition/release
   • Timing/Profiling: Measure execution time
   • Temporary changes: Config, environment, directories

5. BEST PRACTICES:
   • Always handle exceptions properly in __exit__()
   • Use @contextmanager for simple cases
   • Use class-based for complex state management
   • Consider using contextlib utilities before reinventing
   • Document what resources your context manager manages

6. ADVANCED PATTERNS:
   • Nested context managers for complex operations
   • Resource pooling with context managers
   • Configuration management
   • Testing utilities
   • Benchmarking tools

7. WHEN TO USE:
   • Whenever you acquire and release resources
   • For setup/teardown operations
   • When you need to ensure cleanup happens
   • For improving code readability and safety

8. WHEN TO AVOID:
   • For very simple one-time operations
   • When the overhead isn't justified
   • When it makes code less readable (rare)

REMEMBER: Context managers make your code cleaner, safer, and more 
Pythonic. They're one of Python's most elegant features for resource 
management.
"""

print(summary)

# ============================================================================
# COMPREHENSIVE EXAMPLE: WEB SCRAPER WITH CONTEXT MANAGERS
# ============================================================================

print("\n" + "=" * 60)
print("COMPREHENSIVE EXAMPLE: WEB SCRAPER")
print("=" * 60)

def web_scraper_example():
    """Example of a web scraper using multiple context managers."""
    
    print("""
This example demonstrates a web scraper that uses context managers for:
1. Rate limiting requests
2. Database transactions
3. File output
4. Error handling
5. Progress tracking
""")
    
    # Simulated scraper components
    class RateLimiter:
        """Context manager for rate limiting."""
        
        def __init__(self, requests_per_second: float = 1.0):
            self.delay = 1.0 / requests_per_second
            self.last_request = 0
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            return False
        
        def wait_if_needed(self):
            """Wait to respect rate limit."""
            current_time = time.time()
            time_since_last = current_time - self.last_request
            
            if time_since_last < self.delay:
                sleep_time = self.delay - time_since_last
                time.sleep(sleep_time)
            
            self.last_request = time.time()
    
    class ProgressTracker:
        """Context manager for tracking progress."""
        
        def __init__(self, total_items: int):
            self.total = total_items
            self.completed = 0
            self.start_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            print(f"Starting scrape of {self.total} pages...")
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            elapsed = time.time() - self.start_time
            print(f"\nScrape completed in {elapsed:.2f} seconds")
            print(f"Successfully scraped {self.completed}/{self.total} pages")
            return False
        
        def update(self, count: int = 1):
            """Update progress."""
            self.completed += count
            progress = (self.completed / self.total) * 100
            print(f"  Progress: {self.completed}/{self.total} ({progress:.1f}%)")
    
    # Simulate scraping
    def scrape_page(url: str):
        """Simulate scraping a web page."""
        # Simulate network delay
        time.sleep(0.05)
        
        # Simulate sometimes failing
        if "fail" in url:
            raise ConnectionError(f"Failed to scrape {url}")
        
        return f"Content from {url}"
    
    # Main scraping function
    def run_scraper(urls: List[str], output_file: str):
        """Run the web scraper with multiple context managers."""
        
        # Create a temporary database
        temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False).name
        
        try:
            with ExitStack() as stack:
                # 1. Progress tracking
                progress = stack.enter_context(ProgressTracker(len(urls)))
                
                # 2. Rate limiter
                rate_limiter = stack.enter_context(RateLimiter(requests_per_second=10))
                
                # 3. Database for storing results
                db_conn = stack.enter_context(sqlite3.connect(temp_db))
                db_cursor = db_conn.cursor()
                db_cursor.execute("""
                    CREATE TABLE scraped_data (
                        url TEXT PRIMARY KEY,
                        content TEXT,
                        timestamp REAL
                    )
                """)
                
                # 4. Output file
                output = stack.enter_context(open(output_file, 'w'))
                
                print("Scraping started with all context managers active")
                
                # Process each URL
                for url in urls:
                    try:
                        # Apply rate limiting
                        rate_limiter.wait_if_needed()
                        
                        # Scrape the page
                        content = scrape_page(url)
                        
                        # Store in database
                        db_cursor.execute(
                            "INSERT INTO scraped_data VALUES (?, ?, ?)",
                            (url, content, time.time())
                        )
                        
                        # Write to output file
                        output.write(f"{url}: {content[:50]}...\n")
                        
                        # Update progress
                        progress.update()
                        
                    except Exception as e:
                        print(f"  Error scraping {url}: {e}")
                        # Continue with next URL
                
                # Commit database changes
                db_conn.commit()
                
                print("\nScraping completed successfully!")
                
        finally:
            # Clean up temporary database
            if os.path.exists(temp_db):
                os.remove(temp_db)
    
    # Run the example
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/fail-page",  # This will fail
        "https://example.com/page3",
        "https://example.com/page4",
    ]
    
    output_file = "scraped_output.txt"
    
    print("Running web scraper example...")
    run_scraper(urls, output_file)
    
    # Show results
    print(f"\nOutput written to: {output_file}")
    with open(output_file, 'r') as f:
        print("First few lines of output:")
        for i, line in enumerate(f):
            if i < 3:
                print(f"  {line.strip()}")
    
    # Clean up
    os.remove(output_file)

# Note: Using ExitStack from contextlib
from contextlib import ExitStack

web_scraper_example()