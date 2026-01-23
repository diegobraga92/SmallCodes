"""
COMPREHENSIVE GUIDE TO PYTHON DEBUGGING AND PERFORMANCE OPTIMIZATION

This script demonstrates and explains debugging techniques and performance optimization
strategies in Python with practical examples.
"""

import sys
import logging
import pdb
import cProfile
import pstats
import io
import time
import timeit
import random
import functools
from typing import List, Dict, Any, Callable
from collections import defaultdict, Counter, deque
from dataclasses import dataclass
import tracemalloc
import line_profiler  # Note: Need to install: pip install line_profiler
import memory_profiler  # Note: Need to install: pip install memory_profiler

# ============================================================================
# PART 1: DEBUGGING - READING STACK TRACES
# ============================================================================

def stack_traces_demo():
    """
    READING STACK TRACES:
    --------------------
    Stack traces show the execution path when an error occurs.
    
    Anatomy of a stack trace:
    1. Error type and message
    2. Traceback (call stack)
    3. File name and line number for each frame
    4. Code snippet for the error line
    """
    
    print("\n" + "="*60)
    print("DEBUGGING: READING STACK TRACES")
    print("="*60)
    
    # 1. Simple Stack Trace Example
    print("\n1. SIMPLE STACK TRACE EXAMPLE:")
    
    def divide_numbers(a: float, b: float) -> float:
        """Function that can raise an error."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def calculate_average(numbers: List[float]) -> float:
        """Function that calls another function."""
        total = sum(numbers)
        count = len(numbers)
        return divide_numbers(total, count)
    
    def process_data() -> None:
        """Top-level function."""
        data = [10, 20, 30, 0]  # Oops, contains zero
        result = calculate_average(data)
        print(f"Result: {result}")
    
    print("   Simulating error in process_data() -> calculate_average() -> divide_numbers():")
    
    try:
        process_data()
    except Exception as e:
        print(f"\n   ERROR OCCURRED:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {e}")
        
        import traceback
        print(f"\n   FULL STACK TRACE:")
        traceback.print_exc()
    
    # 2. Understanding Stack Trace Components
    print("\n2. STACK TRACE COMPONENTS:")
    
    print("""
    Sample stack trace:
    
    Traceback (most recent call last):
      File "example.py", line 15, in <module>
        process_data()
      File "example.py", line 10, in process_data
        result = calculate_average(data)
      File "example.py", line 6, in calculate_average
        return divide_numbers(total, count)
      File "example.py", line 3, in divide_numbers
        raise ValueError("Cannot divide by zero")
    ValueError: Cannot divide by zero
    
    Components:
    1. "Traceback (most recent call last)": Header
    2. File paths and line numbers
    3. Function names and calling order
    4. Actual error line
    5. Error type and message
    """)
    
    # 3. Common Stack Trace Patterns
    print("\n3. COMMON STACK TRACE PATTERNS:")
    
    # AttributeError
    print("   a) AttributeError (missing attribute):")
    try:
        x = 10
        x.append(5)  # int has no append method
    except AttributeError as e:
        print(f"   Error: {e}")
    
    # TypeError
    print("\n   b) TypeError (wrong type):")
    try:
        result = "hello" + 5  # Can't concatenate str and int
    except TypeError as e:
        print(f"   Error: {e}")
    
    # IndexError
    print("\n   c) IndexError (out of bounds):")
    try:
        lst = [1, 2, 3]
        value = lst[10]  # Index doesn't exist
    except IndexError as e:
        print(f"   Error: {e}")
    
    # KeyError
    print("\n   d) KeyError (missing dict key):")
    try:
        d = {"a": 1, "b": 2}
        value = d["c"]  # Key doesn't exist
    except KeyError as e:
        print(f"   Error: {e}")
    
    # ImportError
    print("\n   e) ImportError (module not found):")
    try:
        import non_existent_module  # Module doesn't exist
    except ImportError as e:
        print(f"   Error: {type(e).__name__}: {e}")
    
    # 4. Custom Exception with Stack Trace
    print("\n4. CUSTOM EXCEPTIONS WITH STACK TRACE:")
    
    class ValidationError(Exception):
        """Custom exception for validation errors."""
        def __init__(self, message, field=None):
            self.message = message
            self.field = field
            super().__init__(self.message)
    
    def validate_user(user: Dict[str, Any]) -> None:
        """Validate user data."""
        if "name" not in user:
            raise ValidationError("Name is required", field="name")
        if "age" not in user:
            raise ValidationError("Age is required", field="age")
        if user["age"] < 0:
            raise ValidationError("Age must be positive", field="age")
    
    def register_user(user_data: Dict[str, Any]) -> None:
        """Register a new user."""
        validate_user(user_data)
        print(f"User {user_data['name']} registered successfully")
    
    print("   Testing custom exception with invalid data:")
    
    try:
        register_user({"age": -5})  # Missing name, negative age
    except ValidationError as e:
        print(f"\n   Custom Error: {e}")
        print(f"   Field: {e.field}")
        import traceback
        traceback.print_exc(limit=2)  # Limit stack trace depth
    
    # 5. Debugging with Traceback Module
    print("\n5. USING TRACEBACK MODULE FOR DEBUGGING:")
    
    def complex_calculation(x: int) -> int:
        """Function with potential error."""
        if x < 0:
            raise ValueError(f"Negative input: {x}")
        return x * 2
    
    def process_with_context() -> None:
        """Process with additional context."""
        for i in [-1, 0, 1, 2]:
            try:
                result = complex_calculation(i)
                print(f"   Processed {i}: {result}")
            except ValueError as e:
                # Get current traceback
                import traceback
                tb = traceback.format_exc()
                print(f"   Failed to process {i}: {e}")
                print(f"   Traceback:\n{tb[:200]}...")  # First 200 chars
    
    process_with_context()
    
    # 6. Tips for Reading Stack Traces
    print("\n6. TIPS FOR READING STACK TRACES:")
    
    print("""
    1. START FROM THE BOTTOM:
       - Read error message first
       - Then look at last call in trace
    
    2. IDENTIFY THE SOURCE:
       - Which file caused the error?
       - Which function?
       - What line number?
    
    3. UNDERSTAND THE FLOW:
       - How did execution get here?
       - What functions were called?
       - What were the inputs?
    
    4. LOOK FOR PATTERNS:
       - Common error types indicate specific issues
       - Recurring errors suggest design problems
       - Nested exceptions reveal root causes
    
    5. ADD CONTEXT:
       - Print variable values before error
       - Add logging to trace execution
       - Use debugger to step through
    """)

# ============================================================================
# PART 2: DEBUGGING - LOGGING MODULE
# ============================================================================

def logging_demo():
    """
    LOGGING MODULE:
    ---------------
    Python's built-in logging system for tracking application behavior.
    
    Log Levels (increasing severity):
    DEBUG < INFO < WARNING < ERROR < CRITICAL
    
    Components:
    - Logger: Entry point for logging
    - Handler: Where logs go (file, console, network)
    - Formatter: How logs are formatted
    - Filter: Optional filtering of logs
    """
    
    print("\n" + "="*60)
    print("DEBUGGING: LOGGING MODULE")
    print("="*60)
    
    # 1. Basic Logging Setup
    print("\n1. BASIC LOGGING SETUP:")
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get a logger
    logger = logging.getLogger(__name__)
    
    # Log at different levels
    logger.debug("This is a DEBUG message - detailed information")
    logger.info("This is an INFO message - general information")
    logger.warning("This is a WARNING message - something unexpected")
    logger.error("This is an ERROR message - something went wrong")
    logger.critical("This is a CRITICAL message - serious problem")
    
    # 2. Advanced Logging Configuration
    print("\n2. ADVANCED LOGGING CONFIGURATION:")
    
    # Reset logging
    logging.getLogger().handlers.clear()
    
    # Create custom logger
    app_logger = logging.getLogger("MyApp")
    app_logger.setLevel(logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler("app.log", mode='w')
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # Add formatters to handlers
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # Add handlers to logger
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)
    
    # Test logging
    print("   Logging to console and file...")
    app_logger.debug("Debug message (file only)")
    app_logger.info("Info message (console and file)")
    app_logger.warning("Warning message (console and file)")
    
    # 3. Logging in Different Modules
    print("\n3. LOGGING ACROSS MULTIPLE MODULES:")
    
    # Simulate module structure
    class DatabaseManager:
        def __init__(self):
            self.logger = logging.getLogger("MyApp.Database")
        
        def connect(self):
            self.logger.info("Connecting to database...")
            # Simulate error
            try:
                raise ConnectionError("Database unreachable")
            except ConnectionError as e:
                self.logger.error(f"Failed to connect: {e}")
                raise
    
    class UserService:
        def __init__(self):
            self.logger = logging.getLogger("MyApp.UserService")
            self.db = DatabaseManager()
        
        def get_user(self, user_id):
            self.logger.info(f"Getting user {user_id}")
            try:
                self.db.connect()
                return {"id": user_id, "name": "John"}
            except Exception as e:
                self.logger.error(f"Failed to get user {user_id}: {e}")
                return None
    
    # Test the modules
    user_service = UserService()
    user = user_service.get_user(123)
    
    # 4. Structured Logging (for production)
    print("\n4. STRUCTURED LOGGING (JSON FORMAT):")
    
    import json
    
    class JsonFormatter(logging.Formatter):
        """Formatter that outputs JSON."""
        
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            
            # Add exception info if present
            if record.exc_info:
                log_record["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_record)
    
    # Setup JSON logger
    json_logger = logging.getLogger("JsonApp")
    json_handler = logging.StreamHandler()
    json_handler.setFormatter(JsonFormatter())
    json_logger.addHandler(json_handler)
    json_logger.setLevel(logging.INFO)
    
    print("   JSON formatted log:")
    json_logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
    
    # 5. Logging Best Practices
    print("\n5. LOGGING BEST PRACTICES:")
    
    print("""
    1. USE APPROPRIATE LOG LEVELS:
       - DEBUG: Detailed information for debugging
       - INFO: Confirmation that things are working
       - WARNING: Something unexpected but recoverable
       - ERROR: Something failed but application continues
       - CRITICAL: Application cannot continue
    
    2. STRUCTURE LOGGERS HIERARCHICALLY:
       - Use dot notation: "app.module.submodule"
       - Inherit configuration from parent loggers
       - Set levels appropriately at each level
    
    3. INCLUDE CONTEXT IN LOG MESSAGES:
       - Use extra parameter for structured data
       - Include relevant identifiers (user_id, request_id)
       - Add timestamps for correlation
    
    4. SEPARATE CONCERNS:
       - Different handlers for different purposes
       - Console for development, file for production
       - Different formats for different consumers
    
    5. PERFORMANCE CONSIDERATIONS:
       - Guard expensive log computations
       - Use lazy evaluation with % formatting
       - Consider async logging for high volume
    """)
    
    # Clean up
    import os
    if os.path.exists("app.log"):
        os.remove("app.log")

# ============================================================================
# PART 3: DEBUGGING - DEBUGGERS (PDB & IDE TOOLS)
# ============================================================================

def debuggers_demo():
    """
    DEBUGGERS:
    ----------
    Tools for interactive debugging.
    
    PDB (Python Debugger):
    - Built-in command-line debugger
    - Basic but powerful
    
    IDE Debuggers:
    - VS Code, PyCharm, etc.
    - GUI interfaces
    - Advanced features
    
    Common Debugger Commands:
    - n(ext): Execute next line
    - s(tep): Step into function
    - c(ontinue): Continue execution
    - l(ist): Show source code
    - p(rint): Print expression
    - b(reak): Set breakpoint
    - q(uit): Quit debugger
    """
    
    print("\n" + "="*60)
    print("DEBUGGING: DEBUGGERS (PDB & IDE TOOLS)")
    print("="*60)
    
    # 1. Basic PDB Usage
    print("\n1. BASIC PDB USAGE:")
    
    print("""
    There are several ways to use PDB:
    
    1. POST-MORTEM DEBUGGING:
       python -m pdb script.py
       OR
       import pdb; pdb.pm()
    
    2. SET TRACEPOINT:
       import pdb; pdb.set_trace()
    
    3. BREAKPOINT() FUNCTION (Python 3.7+):
       breakpoint()  # Same as pdb.set_trace()
    """)
    
    # 2. Example Function for Debugging
    def calculate_statistics(data: List[float]) -> Dict[str, float]:
        """Calculate statistics with potential bugs."""
        # Let's intentionally add a bug
        total = 0
        for i in range(len(data) + 1):  # Bug: off-by-one error
            total += data[i]
        
        average = total / len(data)
        
        # Another potential issue
        variance = sum((x - average) ** 2 for x in data)
        std_dev = variance ** 0.5
        
        return {
            "average": average,
            "variance": variance,
            "std_dev": std_dev
        }
    
    # 3. Simulating PDB Session
    print("\n3. SIMULATED PDB SESSION:")
    
    print("""
    Let's simulate what happens in PDB:
    
    (Pdb) l
      1     def calculate_statistics(data):
      2         total = 0
      3         for i in range(len(data) + 1):  # Bug here!
      4             total += data[i]
      5         
      6         average = total / len(data)
      7         variance = sum((x - average) ** 2 for x in data)
      8         return {"average": average, "variance": variance}
    
    (Pdb) b 3
    Breakpoint 1 at line 3
    
    (Pdb) c
    > <stdin>(3)calculate_statistics()
    -> for i in range(len(data) + 1):
    
    (Pdb) p data
    [1.0, 2.0, 3.0, 4.0]
    
    (Pdb) p len(data)
    4
    
    (Pdb) p range(len(data) + 1)
    range(0, 5)  # Will cause IndexError!
    
    (Pdb) n  # Next line
    > <stdin>(4)calculate_statistics()
    -> total += data[i]
    
    (Pdb) p i
    0
    
    (Pdb) c  # Continue
    IndexError: list index out of range
    """)
    
    # 4. Practical PDB Example
    print("\n4. PRACTICAL PDB EXAMPLE:")
    
    def find_duplicates(items: List[Any]) -> List[Any]:
        """Find duplicate items (buggy version)."""
        seen = set()
        duplicates = []
        
        for item in items:
            if item in seen:
                duplicates.append(item)
            seen.add(item)  # Bug: should be after the check?
        
        return duplicates
    
    # Test the function
    test_data = [1, 2, 3, 2, 4, 3, 5]
    print(f"   Test data: {test_data}")
    
    try:
        result = find_duplicates(test_data)
        print(f"   Result: {result}")
        print(f"   Expected: [2, 3]")
        print(f"   Bug: First occurrence not detected properly")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 5. Advanced PDB Features
    print("\n5. ADVANCED PDB FEATURES:")
    
    print("""
    PDB COMMAND REFERENCE:
    
    BREAKPOINTS:
    - b lineno: Set breakpoint at line number
    - b function: Set breakpoint at function
    - b: List all breakpoints
    - clear bpnumber: Clear breakpoint
    - disable bpnumber: Disable breakpoint
    - enable bpnumber: Enable breakpoint
    
    EXECUTION CONTROL:
    - n(ext): Execute next line (don't step into functions)
    - s(tep): Step into function call
    - c(ontinue): Continue until next breakpoint
    - r(eturn): Continue until function returns
    - unt(il) lineno: Continue until line number
    
    INSPECTION:
    - l(ist): Show source code around current line
    - ll: Show current function source
    - p expression: Print expression value
    - pp expression: Pretty print expression
    - whatis expression: Show type of expression
    - w(here): Print stack trace
    
    VARIABLES:
    - a(rgs): Print function arguments
    - d(own): Move down stack frame
    - u(p): Move up stack frame
    
    MISCELLANEOUS:
    - !statement: Execute Python statement
    - q(uit): Quit debugger
    - h(elp): Show help
    """)
    
    # 6. IDE Debugging Features
    print("\n6. IDE DEBUGGING FEATURES:")
    
    print("""
    MODERN IDE DEBUGGERS (VS Code, PyCharm):
    
    1. VISUAL BREAKPOINTS:
       - Click gutter to set breakpoints
       - Conditional breakpoints
       - Hit count breakpoints
    
    2. WATCH EXPRESSIONS:
       - Monitor variable values
       - Evaluate expressions on the fly
       - View data structures visually
    
    3. CALL STACK NAVIGATION:
       - Click to jump between stack frames
       - View local variables at each level
       - Navigate to source code
    
    4. DEBUG CONSOLE:
       - Interactive Python console
       - Execute commands during debugging
       - Modify variables on the fly
    
    5. ADVANCED FEATURES:
       - Remote debugging
       - Multi-process debugging
       - Django/Flask debugging
       - Unit test debugging
    
    EXAMPLE VS CODE LAUNCH CONFIGURATION:
    
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "justMyCode": false
            }
        ]
    }
    """)
    
    # 7. Debugging Techniques
    print("\n7. DEBUGGING TECHNIQUES:")
    
    print("""
    1. REPRODUCE THE BUG:
       - Create minimal test case
       - Identify exact conditions
       - Remove unrelated code
    
    2. BINARY SEARCH:
       - Add debug statements at midpoint
       - Narrow down location
       - Repeat until found
    
    3. RUBBER DUCK DEBUGGING:
       - Explain code line by line
       - Often reveals the issue
       - Simple but effective
    
    4. TIME TRAVEL DEBUGGING:
       - Use version control
       - Bisect to find introducing commit
       - git bisect for complex issues
    
    5. INSTRUMENTATION:
       - Add logging at key points
       - Profile execution
       - Monitor memory usage
    
    6. VISUALIZATION:
       - Draw data structures
       - Create flow charts
       - Use debugging tools
    """)

# ============================================================================
# PART 4: PERFORMANCE OPTIMIZATION - PROFILING BASICS
# ============================================================================

def profiling_demo():
    """
    PROFILING:
    ----------
    Measuring where code spends time and memory.
    
    Types of Profiling:
    1. Time Profiling: cProfile, line_profiler
    2. Memory Profiling: memory_profiler, tracemalloc
    3. Statistical Profiling: Sampling profilers
    
    Rule: Profile before optimizing!
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE OPTIMIZATION: PROFILING BASICS")
    print("="*60)
    
    # 1. cProfile - Built-in Time Profiler
    print("\n1. CPROFILE - TIME PROFILING:")
    
    def slow_function(n: int) -> float:
        """Inefficient function for profiling."""
        result = 0
        for i in range(n):
            for j in range(n):
                result += i * j
        return result
    
    def fast_function(n: int) -> float:
        """More efficient version."""
        # Sum of arithmetic series
        total = 0
        for i in range(n):
            total += i * sum(range(n))
        return total
    
    def main_profile():
        """Main function to profile."""
        # Call slow function
        result1 = slow_function(100)
        
        # Call fast function
        result2 = fast_function(100)
        
        # Some I/O operation
        with open("temp_profile.txt", "w") as f:
            for i in range(1000):
                f.write(f"Line {i}\n")
        
        return result1 + result2
    
    print("   Running cProfile...")
    
    # Profile using cProfile
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = main_profile()
    
    profiler.disable()
    
    # Print profiling results
    print(f"   Result: {result}")
    
    # Create stats object
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    
    # Sort by different criteria
    print("\n   Statistics sorted by cumulative time:")
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(10)  # Top 10 functions
    
    print("\n   Statistics sorted by time per call:")
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(10)
    
    # Clean up
    import os
    if os.path.exists("temp_profile.txt"):
        os.remove("temp_profile.txt")
    
    # 2. Line Profiler (More Detailed)
    print("\n2. LINE PROFILER - LINE-BY-LINE ANALYSIS:")
    
    try:
        # Line profiler needs to be installed separately
        from line_profiler import LineProfiler
        
        def process_data_line_profiler(data_size: int) -> List[int]:
            """Function to profile line by line."""
            # Initialize
            result = []
            
            # Process data (inefficiently)
            for i in range(data_size):
                # Some computation
                value = i ** 2
                
                # Conditional check
                if value % 2 == 0:
                    result.append(value)
                else:
                    result.append(value * 2)
            
            # Sort (could be expensive)
            result.sort()
            
            return result[:10]  # Return only first 10
        
        # Create profiler
        lp = LineProfiler()
        
        # Add function to profile
        lp.add_function(process_data_line_profiler)
        
        # Run profiler
        print("   Running line_profiler...")
        lp.runctx("process_data_line_profiler(10000)", globals(), locals())
        
        # Print results
        print("   Line-by-line timing:")
        lp.print_stats()
        
    except ImportError:
        print("   line_profiler not installed. Install with: pip install line_profiler")
        print("   Simulated output would show time per line.")
    
    # 3. Memory Profiling
    print("\n3. MEMORY PROFILING:")
    
    try:
        from memory_profiler import profile
        
        @profile
        def memory_intensive_operation() -> List[List[int]]:
            """Function that uses lots of memory."""
            # Create large data structures
            matrix = []
            
            for i in range(1000):
                # Create row
                row = []
                for j in range(1000):
                    row.append(i * j)
                matrix.append(row)
            
            # Process matrix
            result = []
            for row in matrix:
                filtered = [x for x in row if x % 2 == 0]
                result.append(filtered)
            
            return result
        
        print("   Running memory_profiler...")
        memory_intensive_operation()
        
    except ImportError:
        print("   memory_profiler not installed. Install with: pip install memory_profiler")
        print("   Simulated output would show memory usage per line.")
    
    # 4. Built-in Time Measurement
    print("\n4. BUILT-IN TIME MEASUREMENT TOOLS:")
    
    # time.time() for wall clock time
    print("   Using time.time():")
    start = time.time()
    sum(range(1000000))
    end = time.time()
    print(f"   Elapsed: {end - start:.6f} seconds")
    
    # time.perf_counter() for high precision
    print("\n   Using time.perf_counter():")
    start = time.perf_counter()
    sum(range(1000000))
    end = time.perf_counter()
    print(f"   Elapsed: {end - start:.6f} seconds")
    
    # timeit for small code snippets
    print("\n   Using timeit module:")
    import timeit
    
    # Test string concatenation methods
    stmt1 = '"".join(str(i) for i in range(1000))'
    stmt2 = 'result = ""; [result + str(i) for i in range(1000)]'
    
    time1 = timeit.timeit(stmt1, number=1000)
    time2 = timeit.timeit(stmt2, number=1000)
    
    print(f"   join comprehension: {time1:.4f} seconds")
    print(f"   string concatenation: {time2:.4f} seconds")
    print(f"   Speedup: {time2/time1:.1f}x")
    
    # 5. Profiling Best Practices
    print("\n5. PROFILING BEST PRACTICES:")
    
    print("""
    1. PROFILE BEFORE OPTIMIZING:
       - Don't guess what's slow
       - Measure with realistic data
       - Focus on bottlenecks
    
    2. USE APPROPRIATE PROFILERS:
       - cProfile: Overall time analysis
       - line_profiler: Line-by-line timing
       - memory_profiler: Memory usage
       - tracemalloc: Allocation tracking
    
    3. PROFILE IN PRODUCTION-LIKE ENVIRONMENT:
       - Use realistic data sizes
       - Consider system load
       - Account for caching effects
    
    4. INTERPRET RESULTS CORRECTLY:
       - Distinguish between CPU and I/O time
       - Understand overhead of profiling
       - Look for patterns, not just numbers
    
    5. ITERATIVE PROFILING:
       - Profile after each optimization
       - Verify improvements
       - Watch for regressions
    
    6. COMMON BOTTLENECKS TO LOOK FOR:
       - Nested loops (O(n²) complexity)
       - Excessive function calls
       - Unnecessary object creation
       - Inefficient algorithms
       - I/O operations
    """)
    
    # 6. Profiling Example: Finding Bottlenecks
    print("\n6. REAL-WORLD PROFILING EXAMPLE:")
    
    def find_primes_inefficient(limit: int) -> List[int]:
        """Inefficient prime finder."""
        primes = []
        for num in range(2, limit + 1):
            is_prime = True
            for i in range(2, num):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes
    
    def find_primes_efficient(limit: int) -> List[int]:
        """Sieve of Eratosthenes."""
        sieve = [True] * (limit + 1)
        sieve[0:2] = [False, False]
        
        for i in range(2, int(limit ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        
        return [i for i, is_prime in enumerate(sieve) if is_prime]
    
    print("   Comparing prime finding algorithms:")
    
    limit = 10000
    
    # Profile inefficient version
    start = time.time()
    primes1 = find_primes_inefficient(limit)
    time1 = time.time() - start
    
    # Profile efficient version
    start = time.time()
    primes2 = find_primes_efficient(limit)
    time2 = time.time() - start
    
    print(f"   Inefficient: {time1:.4f} seconds, found {len(primes1)} primes")
    print(f"   Efficient:   {time2:.4f} seconds, found {len(primes2)} primes")
    print(f"   Speedup: {time1/time2:.1f}x")
    print(f"   Same results: {primes1 == primes2}")

# ============================================================================
# PART 5: PERFORMANCE OPTIMIZATION - WHEN PYTHON IS "SLOW"
# ============================================================================

def python_slow_demo():
    """
    WHEN PYTHON IS "SLOW" AND WHY:
    -----------------------------
    
    Python can be slower than compiled languages due to:
    1. Dynamic typing (runtime type checking)
    2. Interpreted nature (not compiled to machine code)
    3. GIL (limits multi-threading for CPU-bound tasks)
    4. Object overhead (everything is an object)
    5. Memory management (garbage collection)
    
    However, Python excels at:
    - Developer productivity
    - Readability and maintainability
    - Rich ecosystem
    - Integration capabilities
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE: WHEN PYTHON IS 'SLOW' AND WHY")
    print("="*60)
    
    # 1. Python vs C Performance Comparison
    print("\n1. PYTHON VS C PERFORMANCE COMPARISON:")
    
    def python_sum(n: int) -> int:
        """Python sum implementation."""
        total = 0
        for i in range(n):
            total += i
        return total
    
    # Time Python version
    n = 10_000_000
    print(f"   Summing {n:,} numbers in Python:")
    
    start = time.perf_counter()
    result = python_sum(n)
    python_time = time.perf_counter() - start
    
    print(f"   Result: {result}")
    print(f"   Time: {python_time:.4f} seconds")
    
    # Compare with theoretical C performance
    print("\n   Estimated C equivalent performance:")
    print("""
    // C code would be something like:
    // long long sum = 0;
    // for (long long i = 0; i < n; i++) {
    //     sum += i;
    // }
    // return sum;
    
    Python overhead factors:
    1. Dynamic dispatch (function lookups)
    2. Object creation for integers
    3. Bounds checking on loops
    4. Garbage collection pauses
    5. Interpreter bytecode execution
    """)
    
    # 2. Types of Python Overhead
    print("\n2. TYPES OF PYTHON OVERHEAD:")
    
    print("   a) OBJECT OVERHEAD:")
    
    import sys
    
    # Show object sizes
    print(f"   Empty tuple size: {sys.getsizeof(())} bytes")
    print(f"   Empty list size:  {sys.getsizeof([])} bytes")
    print(f"   Empty dict size:  {sys.getsizeof({{}})} bytes")
    print(f"   Integer size:     {sys.getsizeof(0)} bytes")
    print(f"   String 'a' size:  {sys.getsizeof('a')} bytes")
    
    print("\n   b) FUNCTION CALL OVERHEAD:")
    
    def simple_func(x):
        return x + 1
    
    def many_calls(n):
        total = 0
        for i in range(n):
            total += simple_func(i)
        return total
    
    n_calls = 1_000_000
    start = time.perf_counter()
    result = many_calls(n_calls)
    func_time = time.perf_counter() - start
    
    print(f"   {n_calls:,} function calls: {func_time:.4f} seconds")
    print(f"   ~{func_time/n_calls*1_000_000:.2f} microseconds per call")
    
    print("\n   c) ATTRIBUTE LOOKUP OVERHEAD:")
    
    class DataClass:
        def __init__(self, value):
            self.value = value
    
    def access_attribute(obj, n):
        total = 0
        for _ in range(n):
            total += obj.value  # Attribute lookup each time
        return total
    
    data = DataClass(42)
    start = time.perf_counter()
    result = access_attribute(data, 1_000_000)
    attr_time = time.perf_counter() - start
    
    print(f"   {1_000_000:,} attribute lookups: {attr_time:.4f} seconds")
    
    # 3. Where Python is Actually Fast
    print("\n3. WHERE PYTHON IS ACTUALLY FAST:")
    
    print("   a) BUILT-IN FUNCTIONS (C implementations):")
    
    # Python's built-in functions are written in C
    numbers = list(range(1_000_000))
    
    # Using Python loop
    start = time.perf_counter()
    total = 0
    for n in numbers:
        total += n
    loop_time = time.perf_counter() - start
    
    # Using built-in sum
    start = time.perf_counter()
    total = sum(numbers)
    builtin_time = time.perf_counter() - start
    
    print(f"   Manual loop: {loop_time:.4f} seconds")
    print(f"   Built-in sum: {builtin_time:.4f} seconds")
    print(f"   Built-in is {loop_time/builtin_time:.1f}x faster")
    
    print("\n   b) LIST COMPREHENSIONS:")
    
    # List comprehension vs manual loop
    start = time.perf_counter()
    squares = []
    for i in range(1_000_000):
        squares.append(i ** 2)
    loop_time = time.perf_counter() - start
    
    start = time.perf_counter()
    squares = [i ** 2 for i in range(1_000_000)]
    comp_time = time.perf_counter() - start
    
    print(f"   Manual loop: {loop_time:.4f} seconds")
    print(f"   List comprehension: {comp_time:.4f} seconds")
    print(f"   Comprehension is {loop_time/comp_time:.1f}x faster")
    
    # 4. Real-world Performance Considerations
    print("\n4. REAL-WORLD PERFORMANCE CONSIDERATIONS:")
    
    print("   a) I/O-BOUND VS CPU-BOUND TASKS:")
    
    def simulate_io_bound():
        """Simulate I/O-bound task (network, disk)."""
        time.sleep(0.1)  # Simulate I/O wait
        return "data"
    
    def simulate_cpu_bound(n):
        """Simulate CPU-bound task (computation)."""
        total = 0
        for i in range(n):
            total += i ** 2
        return total
    
    print("   Python is fine for I/O-bound tasks (async/threading)")
    print("   Python can be slow for CPU-bound tasks (use multiprocessing)")
    
    print("\n   b) LIBRARY PERFORMANCE:")
    
    print("""
    Many Python libraries are written in C:
    - NumPy: Numerical computing (C/Fortran)
    - Pandas: Data manipulation (C/Cython)
    - PIL/Pillow: Image processing (C)
    - Cryptography: Crypto operations (C/Rust)
    - lxml: XML processing (C)
    
    These can be as fast as native code!
    """)
    
    # 5. Performance Optimization Strategy
    print("\n5. PERFORMANCE OPTIMIZATION STRATEGY:")
    
    print("""
    APPROACH TO OPTIMIZATION:
    
    1. MEASURE FIRST:
       - Profile to find bottlenecks
       - Use realistic data sizes
       - Identify hot spots
    
    2. ALGORITHM OPTIMIZATION:
       - Choose better algorithms (O(n) vs O(n²))
       - Use appropriate data structures
       - Reduce complexity first
    
    3. PYTHON-SPECIFIC OPTIMIZATIONS:
       - Use built-in functions
       - Leverage list comprehensions
       - Minimize function calls
       - Avoid unnecessary object creation
    
    4. USE COMPILED CODE WHEN NEEDED:
       - NumPy for numerical work
       - Cython for custom C extensions
       - Numba for JIT compilation
       - PyPy for JIT optimization
    
    5. ARCHITECTURAL OPTIMIZATIONS:
       - Caching/memoization
       - Lazy evaluation
       - Asynchronous I/O
       - Parallel processing
    """)
    
    # 6. Case Study: Optimizing a Slow Function
    print("\n6. CASE STUDY: OPTIMIZING A SLOW FUNCTION:")
    
    # Original slow version
    def process_data_slow(data):
        """Original slow implementation."""
        result = []
        for item in data:
            # Multiple operations per item
            if isinstance(item, str):
                processed = item.upper()
            elif isinstance(item, int):
                processed = str(item)
            else:
                processed = str(item)
            
            # More operations
            if len(processed) > 10:
                processed = processed[:10]
            
            result.append(processed)
        return result
    
    # Optimized version
    def process_data_fast(data):
        """Optimized implementation."""
        # Pre-allocate list
        result = [None] * len(data)
        
        # Use local variables for speed
        upper = str.upper
        str_func = str
        
        for i, item in enumerate(data):
            # Simplified logic
            if isinstance(item, str):
                processed = upper(item)
            else:
                processed = str_func(item)
            
            # Conditional expression
            result[i] = processed[:10] if len(processed) > 10 else processed
        
        return result
    
    # Test both versions
    test_data = ["hello"] * 10000 + [123] * 10000
    
    print(f"   Testing with {len(test_data):,} items:")
    
    start = time.perf_counter()
    result1 = process_data_slow(test_data)
    time_slow = time.perf_counter() - start
    
    start = time.perf_counter()
    result2 = process_data_fast(test_data)
    time_fast = time.perf_counter() - start
    
    print(f"   Slow version: {time_slow:.4f} seconds")
    print(f"   Fast version: {time_fast:.4f} seconds")
    print(f"   Speedup: {time_slow/time_fast:.1f}x")
    print(f"   Same results: {result1 == result2}")

# ============================================================================
# PART 6: PERFORMANCE OPTIMIZATION - EFFICIENT DATA STRUCTURES
# ============================================================================

def efficient_data_structures_demo():
    """
    EFFICIENT DATA STRUCTURE CHOICES:
    ---------------------------------
    
    Choosing the right data structure can make orders of magnitude difference.
    
    Common Choices:
    1. Lists vs Tuples
    2. Sets vs Lists (for membership testing)
    3. Dictionaries vs Lists (for lookups)
    4. Collections module
    5. Arrays vs Lists
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE: EFFICIENT DATA STRUCTURE CHOICES")
    print("="*60)
    
    # 1. Lists vs Tuples
    print("\n1. LISTS VS TUPLES:")
    
    def test_list_tuple_access(n):
        """Test access speed for lists and tuples."""
        # Create list and tuple with same data
        lst = list(range(n))
        tpl = tuple(range(n))
        
        # Time list access
        start = time.perf_counter()
        total = 0
        for i in range(n):
            total += lst[i]
        list_time = time.perf_counter() - start
        
        # Time tuple access
        start = time.perf_counter()
        total = 0
        for i in range(n):
            total += tpl[i]
        tuple_time = time.perf_counter() - start
        
        return list_time, tuple_time
    
    n = 1_000_000
    list_time, tuple_time = test_list_tuple_access(n)
    
    print(f"   Accessing {n:,} elements:")
    print(f"   List time:  {list_time:.4f} seconds")
    print(f"   Tuple time: {tuple_time:.4f} seconds")
    print(f"   Tuple is {list_time/tuple_time:.1f}x faster for iteration")
    
    print("\n   When to use each:")
    print("   - Lists: When you need to modify the collection")
    print("   - Tuples: When data is immutable (faster, less memory)")
    print("   - Tuples as dictionary keys (hashable)")
    
    # 2. Sets vs Lists for Membership Testing
    print("\n2. SETS VS LISTS (MEMBERSHIP TESTING):")
    
    def test_membership(n, search_count):
        """Test membership testing performance."""
        # Create data
        data = list(range(n))
        
        # Convert to set
        data_set = set(data)
        
        # Search items (some present, some not)
        search_items = list(range(0, n * 2, 2))  # Every other item
        
        # Test list membership
        start = time.perf_counter()
        found_in_list = 0
        for item in search_items[:search_count]:
            if item in data:  # O(n) for lists
                found_in_list += 1
        list_time = time.perf_counter() - start
        
        # Test set membership
        start = time.perf_counter()
        found_in_set = 0
        for item in search_items[:search_count]:
            if item in data_set:  # O(1) for sets
                found_in_set += 1
        set_time = time.perf_counter() - start
        
        return list_time, set_time, found_in_list, found_in_set
    
    n = 10000
    search_count = 10000
    list_time, set_time, found_list, found_set = test_membership(n, search_count)
    
    print(f"   Testing {search_count:,} membership checks in {n:,} items:")
    print(f"   List (O(n)): {list_time:.4f} seconds")
    print(f"   Set (O(1)):  {set_time:.4f} seconds")
    print(f"   Set is {list_time/set_time:.1f}x faster")
    print(f"   Found: list={found_list}, set={found_set}")
    
    # 3. Dictionaries vs Lists for Lookups
    print("\n3. DICTIONARIES VS LISTS (KEY LOOKUPS):")
    
    def create_student_records(n):
        """Create student records with ID as key."""
        # List of tuples approach
        students_list = []
        for i in range(n):
            students_list.append((f"ID{i}", f"Student{i}", i * 10))
        
        # Dictionary approach
        students_dict = {}
        for i in range(n):
            students_dict[f"ID{i}"] = (f"Student{i}", i * 10)
        
        return students_list, students_dict
    
    def find_student_list(students, student_id):
        """Find student in list (linear search)."""
        for record in students:
            if record[0] == student_id:
                return record
        return None
    
    def find_student_dict(students, student_id):
        """Find student in dict (constant time)."""
        return students.get(student_id)
    
    n = 10000
    students_list, students_dict = create_student_records(n)
    
    # Test lookup performance
    search_ids = [f"ID{i}" for i in range(0, n * 2, 2)]
    
    # List lookup
    start = time.perf_counter()
    found_list = 0
    for student_id in search_ids[:1000]:
        if find_student_list(students_list, student_id):
            found_list += 1
    list_time = time.perf_counter() - start
    
    # Dict lookup
    start = time.perf_counter()
    found_dict = 0
    for student_id in search_ids[:1000]:
        if find_student_dict(students_dict, student_id):
            found_dict += 1
    dict_time = time.perf_counter() - start
    
    print(f"\n   Looking up 1,000 students in {n:,} records:")
    print(f"   List (linear search): {list_time:.4f} seconds")
    print(f"   Dict (hash table):   {dict_time:.4f} seconds")
    print(f"   Dict is {list_time/dict_time:.1f}x faster")
    print(f"   Found: list={found_list}, dict={found_dict}")
    
    # 4. Collections Module Specialized Containers
    print("\n4. COLLECTIONS MODULE SPECIALIZED CONTAINERS:")
    
    from collections import defaultdict, Counter, deque
    
    print("   a) defaultdict vs regular dict:")
    
    # Regular dict approach
    def count_items_regular(items):
        counts = {}
        for item in items:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        return counts
    
    # defaultdict approach
    def count_items_defaultdict(items):
        counts = defaultdict(int)
        for item in items:
            counts[item] += 1
        return counts
    
    # Generate test data
    items = [random.choice(['apple', 'banana', 'cherry', 'date']) 
             for _ in range(100000)]
    
    # Time regular dict
    start = time.perf_counter()
    counts1 = count_items_regular(items)
    regular_time = time.perf_counter() - start
    
    # Time defaultdict
    start = time.perf_counter()
    counts2 = count_items_defaultdict(items)
    default_time = time.perf_counter() - start
    
    print(f"   Counting 100,000 items:")
    print(f"   Regular dict:    {regular_time:.4f} seconds")
    print(f"   defaultdict:     {default_time:.4f} seconds")
    print(f"   defaultdict is {regular_time/default_time:.1f}x faster")
    
    print("\n   b) Counter for frequency counting:")
    
    # Even faster with Counter
    start = time.perf_counter()
    counts3 = Counter(items)
    counter_time = time.perf_counter() - start
    
    print(f"   Counter:         {counter_time:.4f} seconds")
    print(f"   Counter is {regular_time/counter_time:.1f}x faster than regular dict")
    
    print("\n   c) deque for queue operations:")
    
    # List vs deque for queue operations
    n = 10000
    
    # List as queue (pop from beginning is O(n))
    queue_list = list(range(n))
    start = time.perf_counter()
    while queue_list:
        queue_list.pop(0)  # Slow for large lists
    list_queue_time = time.perf_counter() - start
    
    # Deque as queue (pop from beginning is O(1))
    queue_deque = deque(range(n))
    start = time.perf_counter()
    while queue_deque:
        queue_deque.popleft()  # Fast for deques
    deque_queue_time = time.perf_counter() - start
    
    print(f"\n   Queue operations (pop from front):")
    print(f"   List (pop(0)):  {list_queue_time:.4f} seconds")
    print(f"   Deque (popleft): {deque_queue_time:.4f} seconds")
    print(f"   Deque is {list_queue_time/deque_queue_time:.1f}x faster")
    
    # 5. Arrays vs Lists for Numerical Data
    print("\n5. ARRAYS VS LISTS FOR NUMERICAL DATA:")
    
    import array
    
    n = 1_000_000
    
    # Create list of integers
    start = time.perf_counter()
    py_list = list(range(n))
    list_create_time = time.perf_counter() - start
    
    # Create array of integers
    start = time.perf_counter()
    py_array = array.array('i', range(n))
    array_create_time = time.perf_counter() - start
    
    # Memory usage
    list_memory = sys.getsizeof(py_list) + sum(sys.getsizeof(x) for x in py_list[:1000]) * (n / 1000)
    array_memory = sys.getsizeof(py_array)
    
    print(f"\n   Creating {n:,} integers:")
    print(f"   List creation:  {list_create_time:.4f} seconds")
    print(f"   Array creation: {array_create_time:.4f} seconds")
    print(f"   List memory:    ~{list_memory/1024/1024:.1f} MB")
    print(f"   Array memory:   {array_memory/1024/1024:.1f} MB")
    print(f"   Array uses ~{list_memory/array_memory:.1f}x less memory")
    
    # 6. Data Structure Selection Guide
    print("\n6. DATA STRUCTURE SELECTION GUIDE:")
    
    print("""
    WHEN TO USE EACH DATA STRUCTURE:
    
    LISTS:
    - When you need ordered collection
    - When you need to modify (append, insert, remove)
    - When you need indexing and slicing
    - When data is heterogeneous
    
    TUPLES:
    - When data is immutable
    - When using as dictionary keys
    - When you need fixed-size collections
    - For function return multiple values
    
    SETS:
    - For membership testing (x in set)
    - For removing duplicates
    - For mathematical set operations
    - When order doesn't matter
    
    DICTIONARIES:
    - For key-value lookups
    - For counting/frequency tracking
    - For sparse data storage
    - For fast lookups by key
    
    DEQUE:
    - For queues (FIFO) or stacks (LIFO)
    - When you need fast appends/pops from both ends
    - For sliding window algorithms
    
    ARRAYS:
    - For large collections of numbers
    - When memory efficiency is critical
    - When interfacing with C libraries
    
    DEFAULTDICT:
    - When you need default values for missing keys
    - For grouping/categorizing data
    - For building nested structures
    
    COUNTER:
    - For frequency counting
    - For finding most common elements
    - For multiset operations
    
    PERFORMANCE CHARACTERISTICS:
    
    Structure    Access    Search    Insert    Delete    Memory
    ---------    ------    ------    ------    ------    ------
    List         O(1)      O(n)      O(1)*     O(n)      Medium
    Tuple        O(1)      O(n)      N/A       N/A       Small
    Set          N/A       O(1)      O(1)      O(1)      Large
    Dict         O(1)      O(1)      O(1)      O(1)      Large
    Deque        O(1)      O(n)      O(1)      O(1)      Medium
    Array        O(1)      O(n)      O(n)      O(n)      Small
    
    * O(1) for append, O(n) for insert at beginning
    """)

# ============================================================================
# PART 7: PERFORMANCE OPTIMIZATION - BUILT-IN FUNCTIONS VS CUSTOM LOOPS
# ============================================================================

def builtin_vs_custom_demo():
    """
    BUILT-IN FUNCTIONS VS CUSTOM LOOPS:
    -----------------------------------
    
    Built-in functions are implemented in C and are often much faster.
    Python's "batteries included" philosophy provides optimized implementations.
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE: BUILT-IN FUNCTIONS VS CUSTOM LOOPS")
    print("="*60)
    
    # 1. Summation Example
    print("\n1. SUMMATION: BUILT-IN SUM() VS CUSTOM LOOP:")
    
    def sum_custom(numbers):
        """Custom sum implementation."""
        total = 0
        for n in numbers:
            total += n
        return total
    
    # Create test data
    numbers = list(range(1_000_000))
    
    # Time custom sum
    start = time.perf_counter()
    result_custom = sum_custom(numbers)
    custom_time = time.perf_counter() - start
    
    # Time built-in sum
    start = time.perf_counter()
    result_builtin = sum(numbers)
    builtin_time = time.perf_counter() - start
    
    print(f"   Summing {len(numbers):,} numbers:")
    print(f"   Custom loop:  {custom_time:.4f} seconds")
    print(f"   Built-in sum: {builtin_time:.4f} seconds")
    print(f"   Built-in is {custom_time/builtin_time:.1f}x faster")
    print(f"   Results match: {result_custom == result_builtin}")
    
    # 2. Minimum/Maximum Example
    print("\n2. MINIMUM/MAXIMUM: BUILT-IN MIN/MAX VS CUSTOM:")
    
    def min_max_custom(numbers):
        """Custom min/max implementation."""
        if not numbers:
            return None, None
        
        min_val = numbers[0]
        max_val = numbers[0]
        
        for n in numbers[1:]:
            if n < min_val:
                min_val = n
            if n > max_val:
                max_val = n
        
        return min_val, max_val
    
    # Time custom min/max
    start = time.perf_counter()
    min_custom, max_custom = min_max_custom(numbers)
    custom_time = time.perf_counter() - start
    
    # Time built-in min/max
    start = time.perf_counter()
    min_builtin = min(numbers)
    max_builtin = max(numbers)
    builtin_time = time.perf_counter() - start
    
    print(f"   Finding min/max of {len(numbers):,} numbers:")
    print(f"   Custom loop:  {custom_time:.4f} seconds")
    print(f"   Built-in:     {builtin_time:.4f} seconds")
    print(f"   Built-in is {custom_time/builtin_time:.1f}x faster")
    print(f"   Results match: {(min_custom, max_custom) == (min_builtin, max_builtin)}")
    
    # 3. Filtering Example
    print("\n3. FILTERING: BUILT-IN FILTER() VS LIST COMPREHENSION:")
    
    def filter_custom(numbers, threshold):
        """Custom filter implementation."""
        result = []
        for n in numbers:
            if n > threshold:
                result.append(n)
        return result
    
    # Test data
    numbers = list(range(1_000_000))
    threshold = 500_000
    
    # Time custom filter
    start = time.perf_counter()
    result_custom = filter_custom(numbers, threshold)
    custom_time = time.perf_counter() - start
    
    # Time built-in filter
    start = time.perf_counter()
    result_filter = list(filter(lambda x: x > threshold, numbers))
    filter_time = time.perf_counter() - start
    
    # Time list comprehension
    start = time.perf_counter()
    result_comprehension = [x for x in numbers if x > threshold]
    comprehension_time = time.perf_counter() - start
    
    print(f"   Filtering {len(numbers):,} numbers (> {threshold}):")
    print(f"   Custom loop:       {custom_time:.4f} seconds")
    print(f"   Built-in filter(): {filter_time:.4f} seconds")
    print(f"   List comprehension:{comprehension_time:.4f} seconds")
    print(f"   Comprehension is {custom_time/comprehension_time:.1f}x faster than custom")
    print(f"   Comprehension is {filter_time/comprehension_time:.1f}x faster than filter()")
    print(f"   Results match: {len(result_custom) == len(result_filter) == len(result_comprehension)}")
    
    # 4. String Joining Example
    print("\n4. STRING JOINING: BUILT-IN JOIN() VS CONCATENATION:")
    
    def concatenate_strings(strings):
        """String concatenation with + operator."""
        result = ""
        for s in strings:
            result += s
        return result
    
    # Test data
    strings = [str(i) for i in range(10000)]
    
    # Time concatenation
    start = time.perf_counter()
    result_concat = concatenate_strings(strings)
    concat_time = time.perf_counter() - start
    
    # Time join
    start = time.perf_counter()
    result_join = "".join(strings)
    join_time = time.perf_counter() - start
    
    print(f"   Joining {len(strings):,} strings:")
    print(f"   Concatenation (+): {concat_time:.4f} seconds")
    print(f"   Built-in join():   {join_time:.4f} seconds")
    print(f"   join() is {concat_time/join_time:.1f}x faster")
    print(f"   Results match: {result_concat == result_join}")
    print(f"   Memory note: Concatenation creates {len(strings)-1} intermediate strings!")
    
    # 5. Sorting Example
    print("\n5. SORTING: BUILT-IN SORTED() VS CUSTOM:")
    
    def bubble_sort(arr):
        """Bubble sort implementation (O(n²))."""
        n = len(arr)
        arr = arr.copy()  # Don't modify original
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    # Test data (smaller due to O(n²) complexity)
    numbers = [random.randint(1, 10000) for _ in range(1000)]
    
    # Time bubble sort
    start = time.perf_counter()
    result_bubble = bubble_sort(numbers)
    bubble_time = time.perf_counter() - start
    
    # Time built-in sort
    start = time.perf_counter()
    result_builtin = sorted(numbers)
    builtin_time = time.perf_counter() - start
    
    print(f"   Sorting {len(numbers):,} numbers:")
    print(f"   Bubble sort (O(n²)): {bubble_time:.4f} seconds")
    print(f"   Built-in sorted() (O(n log n)): {builtin_time:.4f} seconds")
    print(f"   Built-in is {bubble_time/builtin_time:.1f}x faster")
    print(f"   Results match: {result_bubble == result_builtin}")
    
    # 6. Why Built-in Functions are Faster
    print("\n6. WHY BUILT-IN FUNCTIONS ARE FASTER:")
    
    print("""
    REASONS FOR SPEED DIFFERENCE:
    
    1. IMPLEMENTED IN C:
       - Built-ins run as compiled C code
       - No Python interpreter overhead
       - Direct memory access
    
    2. OPTIMIZED ALGORITHMS:
       - Written by experts
       - Use best algorithms (Timsort for sorting)
       - Optimized for edge cases
    
    3. MEMORY EFFICIENCY:
       - Operate on C data structures
       - Minimize object creation
       - Use pre-allocated buffers
    
    4. VECTORIZED OPERATIONS:
       - Process multiple items at once
       - Use CPU vector instructions (SIMD)
       - Minimize Python loop overhead
    
    EXAMPLES OF OPTIMIZED BUILT-INS:
    
    1. sum(): Single pass, minimal type checking
    2. min()/max(): Single pass with early returns
    3. sorted(): Timsort (adaptive, stable)
    4. str.join(): Pre-calculates total size
    5. map()/filter(): Lazy evaluation
    6. any()/all(): Short-circuit evaluation
    """)
    
    # 7. When to Write Custom Code Anyway
    print("\n7. WHEN TO WRITE CUSTOM CODE:")
    
    print("""
    Despite built-in advantages, sometimes custom code is better:
    
    1. SPECIALIZED ALGORITHMS:
       - Built-ins are general purpose
       - Custom code can use domain knowledge
       - Specialized data structures
    
    2. MEMORY CONSTRAINTS:
       - Built-ins may create copies
       - Custom code can work in-place
       - Streaming/lazy processing
    
    3. UNUSUAL DATA FORMATS:
       - Built-ins expect standard types
       - Custom code handles edge cases
       - Non-standard comparisons
    
    4. PERFORMANCE TRADEOFFS:
       - Sometimes readability > performance
       - Maintainability considerations
       - Team skill level
    
    RULE OF THUMB:
    1. Always try built-in first
    2. Profile if performance is critical
    3. Write custom only when needed
    4. Document why custom code was needed
    """)
    
    # 8. Performance Comparison Table
    print("\n8. PERFORMANCE COMPARISON TABLE:")
    
    print("""
    Operation           Built-in           Custom Loop      Speedup
    ---------           --------           -----------      -------
    Summation           sum()              for loop         5-10x
    Min/Max             min()/max()        for loop         3-5x
    Filtering           list comprehension for+append       2-3x
    String joining      str.join()         += concatenation 10-100x
    Sorting             sorted()           bubble sort      100-1000x
    Mapping             list comprehension for+append       2-3x
    Any/All             any()/all()        for loop         2-3x*
    
    * any()/all() have short-circuit evaluation
    
    KEY TAKEAWAYS:
    1. Built-in functions are almost always faster
    2. List comprehensions are faster than map()/filter()
    3. Some built-ins have algorithmic advantages (sorting)
    4. Memory efficiency matters (string concatenation)
    5. Always measure with your specific data
    """)

# ============================================================================
# PART 8: PERFORMANCE OPTIMIZATION - CACHING STRATEGIES
# ============================================================================

def caching_demo():
    """
    CACHING STRATEGIES:
    -------------------
    
    Caching stores expensive computation results for reuse.
    
    Types of Caching:
    1. Memoization: Function-level caching
    2. LRU Cache: Least Recently Used cache
    3. TTL Cache: Time-To-Live cache
    4. Application-level caching
    5. Database query caching
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE: CACHING STRATEGIES")
    print("="*60)
    
    # 1. Simple Memoization
    print("\n1. SIMPLE MEMOIZATION:")
    
    def fibonacci_naive(n: int) -> int:
        """Naive recursive Fibonacci (exponential time)."""
        if n <= 1:
            return n
        return fibonacci_naive(n-1) + fibonacci_naive(n-2)
    
    # Memoized version
    fibonacci_cache = {}
    
    def fibonacci_memoized(n: int) -> int:
        """Memoized Fibonacci (linear time)."""
        if n in fibonacci_cache:
            return fibonacci_cache[n]
        
        if n <= 1:
            result = n
        else:
            result = fibonacci_memoized(n-1) + fibonacci_memoized(n-2)
        
        fibonacci_cache[n] = result
        return result
    
    print("   Testing Fibonacci(30):")
    
    # Naive version (very slow)
    start = time.perf_counter()
    result_naive = fibonacci_naive(30)
    time_naive = time.perf_counter() - start
    
    # Memoized version (fast)
    start = time.perf_counter()
    result_memoized = fibonacci_memoized(30)
    time_memoized = time.perf_counter() - start
    
    print(f"   Naive:     {time_naive:.4f} seconds")
    print(f"   Memoized:  {time_memoized:.4f} seconds")
    print(f"   Speedup:   {time_naive/time_memoized:.0f}x")
    print(f"   Result:    {result_naive} (both methods should match)")
    print(f"   Cache size: {len(fibonacci_cache)} entries")
    
    # 2. Using functools.lru_cache
    print("\n2. USING FUNCTOOLS.LRU_CACHE:")
    
    import functools
    
    @functools.lru_cache(maxsize=128)
    def expensive_computation(x: int, y: int) -> int:
        """Simulate expensive computation."""
        time.sleep(0.01)  # Simulate 10ms computation
        return x ** y
    
    print("   Testing with repeated calls:")
    
    # First call (computes)
    start = time.perf_counter()
    result1 = expensive_computation(2, 10)
    time1 = time.perf_counter() - start
    
    # Second call with same args (cached)
    start = time.perf_counter()
    result2 = expensive_computation(2, 10)
    time2 = time.perf_counter() - start
    
    # Third call with different args (computes)
    start = time.perf_counter()
    result3 = expensive_computation(3, 5)
    time3 = time.perf_counter() - start
    
    print(f"   First call (compute):  {time1:.4f} seconds")
    print(f"   Second call (cached):  {time2:.4f} seconds")
    print(f"   Third call (compute):  {time3:.4f} seconds")
    print(f"   Cache hit speedup: {time1/time2:.0f}x")
    
    # Show cache info
    cache_info = expensive_computation.cache_info()
    print(f"\n   Cache statistics:")
    print(f"   Hits: {cache_info.hits}")
    print(f"   Misses: {cache_info.misses}")
    print(f"   Maxsize: {cache_info.maxsize}")
    print(f"   Currsize: {cache_info.currsize}")
    
    # 3. Custom Cache Implementation
    print("\n3. CUSTOM CACHE IMPLEMENTATION:")
    
    class TTLCache:
        """Time-To-Live cache with expiration."""
        
        def __init__(self, ttl_seconds: int = 60):
            self.ttl = ttl_seconds
            self.cache = {}
        
        def get(self, key):
            """Get value from cache if not expired."""
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return value
                else:
                    # Expired, remove from cache
                    del self.cache[key]
            return None
        
        def set(self, key, value):
            """Set value in cache with current timestamp."""
            self.cache[key] = (value, time.time())
        
        def clear_expired(self):
            """Clear expired entries."""
            current_time = time.time()
            expired_keys = [
                key for key, (_, timestamp) in self.cache.items()
                if current_time - timestamp >= self.ttl
            ]
            for key in expired_keys:
                del self.cache[key]
    
    # Test TTL cache
    ttl_cache = TTLCache(ttl_seconds=1)  # 1 second TTL
    
    ttl_cache.set("key1", "value1")
    print(f"   Set key1 at time {time.time()}")
    
    # Immediate get (should work)
    value = ttl_cache.get("key1")
    print(f"   Immediate get: {value}")
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Get after expiration (should be None)
    value = ttl_cache.get("key1")
    print(f"   After 1.1 seconds: {value}")
    
    # Clear expired
    ttl_cache.clear_expired()
    print(f"   Cache size after clearing: {len(ttl_cache.cache)}")
    
    # 4. Application-Level Caching
    print("\n4. APPLICATION-LEVEL CACHING:")
    
    class DataService:
        """Service with application-level caching."""
        
        def __init__(self):
            self.cache = {}
            self.stats = {"hits": 0, "misses": 0}
        
        def get_user_data(self, user_id: int) -> Dict[str, Any]:
            """Get user data with caching."""
            cache_key = f"user:{user_id}"
            
            # Check cache
            if cache_key in self.cache:
                self.stats["hits"] += 1
                print(f"   Cache HIT for user {user_id}")
                return self.cache[cache_key]
            
            # Cache miss, fetch from "database"
            self.stats["misses"] += 1
            print(f"   Cache MISS for user {user_id}, fetching...")
            time.sleep(0.1)  # Simulate database query
            
            # Simulate database result
            user_data = {
                "id": user_id,
                "name": f"User{user_id}",
                "email": f"user{user_id}@example.com",
                "last_login": time.time()
            }
            
            # Store in cache
            self.cache[cache_key] = user_data
            
            return user_data
        
        def invalidate_user(self, user_id: int):
            """Remove user from cache."""
            cache_key = f"user:{user_id}"
            if cache_key in self.cache:
                del self.cache[cache_key]
                print(f"   Invalidated cache for user {user_id}")
    
    # Test application caching
    service = DataService()
    
    print("\n   Simulating user requests:")
    
    # First request (cache miss)
    user1 = service.get_user_data(1)
    
    # Second request for same user (cache hit)
    user1_cached = service.get_user_data(1)
    
    # Request different user (cache miss)
    user2 = service.get_user_data(2)
    
    # Request first user again (cache hit)
    user1_again = service.get_user_data(1)
    
    print(f"\n   Cache statistics:")
    print(f"   Hits: {service.stats['hits']}")
    print(f"   Misses: {service.stats['misses']}")
    print(f"   Hit rate: {service.stats['hits']/(service.stats['hits']+service.stats['misses'])*100:.1f}%")
    
    # 5. Database Query Caching
    print("\n5. DATABASE QUERY CACHING PATTERNS:")
    
    print("""
    COMMON DATABASE CACHING PATTERNS:
    
    1. QUERY RESULT CACHING:
       - Cache entire query results
       - Use query + parameters as cache key
       - Invalidate on data changes
    
    2. OBJECT CACHING:
       - Cache individual objects/rows
       - Invalidate when object changes
       - Use TTL for eventual consistency
    
    3. READ-THROUGH CACHE:
       - Check cache first
       - If miss, read from DB and cache
       - Transparent to application
    
    4. WRITE-THROUGH CACHE:
       - Write to cache and DB simultaneously
       - Ensures cache consistency
       - Higher write latency
    
    5. WRITE-BEHIND CACHE:
       - Write to cache immediately
       - Write to DB asynchronously
       - Risk of data loss
    
    PYTHON LIBRARIES FOR CACHING:
    
    1. Redis: In-memory data store
    2. Memcached: Distributed caching
    3. Django Cache Framework: Built-in
    4. Flask-Caching: Flask extension
    5. diskcache: Disk-based caching
    """)
    
    # 6. Cache Invalidation Strategies
    print("\n6. CACHE INVALIDATION STRATEGIES:")
    
    print("""
    CACHE INVALIDATION (Hard Problem):
    
    1. TIME-BASED (TTL):
       - Simple to implement
       - Eventual consistency
       - Stale data possible
    
    2. VERSION-BASED:
       - Each update increments version
       - Cache key includes version
       - Precise but requires coordination
    
    3. EVENT-BASED:
       - Invalidate on specific events
       - Requires event system
       - Complex but accurate
    
    4. MANUAL INVALIDATION:
       - Explicit cache clearing
       - Simple but error-prone
       - Developer responsibility
    
    5. COMPOSITE STRATEGIES:
       - TTL + event-based
       - Version + time-based
       - Multiple layers
    
    BEST PRACTICES:
    
    1. Start with TTL-based caching
    2. Add manual invalidation for critical data
    3. Monitor cache hit rates
    4. Implement cache warming
    5. Handle cache misses gracefully
    """)
    
    # 7. Performance Impact of Caching
    print("\n7. PERFORMANCE IMPACT OF CACHING:")
    
    print("""
    PERFORMANCE TRADEOFFS:
    
    BENEFITS:
    ✓ Faster response times
    ✓ Reduced database/API load
    ✓ Better scalability
    ✓ Lower latency
    
    COSTS:
    ✗ Memory usage
    ✗ Cache invalidation complexity
    ✗ Stale data risk
    ✗ Cache penetration (thundering herd)
    
    WHEN TO USE CACHING:
    
    1. READ-HEAVY WORKLOADS:
       - Cache can handle most reads
       - Database freed for writes
    
    2. EXPENSIVE COMPUTATIONS:
       - Results reused multiple times
       - Computation cost > cache cost
    
    3. EXTERNAL API CALLS:
       - Rate limits or latency issues
       - Reduce external dependencies
    
    4. SESSION DATA:
       - User-specific temporary data
       - Fast access needed
    
    WHEN TO AVOID CACHING:
    
    1. FREQUENTLY CHANGING DATA:
       - Cache invalidation overhead
       - Stale data issues
    
    2. LARGE DATASETS:
       - Cache memory requirements
       - Eviction overhead
    
    3. REAL-TIME DATA:
       - Freshness requirements
       - Cache lag unacceptable
    
    4. SIMPLE QUERIES:
       - Database already fast
       - Caching adds complexity
    """)

# ============================================================================
# PART 9: PERFORMANCE OPTIMIZATION - MEMORY VS SPEED TRADEOFFS
# ============================================================================

def memory_vs_speed_demo():
    """
    MEMORY VS SPEED TRADEOFFS:
    -------------------------
    
    Common performance tradeoffs in Python:
    1. Time vs Space complexity
    2. Precomputation vs On-demand computation
    3. Compression vs Decompression speed
    4. Caching vs Freshness
    """
    
    print("\n" + "="*60)
    print("PERFORMANCE: MEMORY VS SPEED TRADEOFFS")
    print("="*60)
    
    # 1. Time vs Space Complexity
    print("\n1. TIME VS SPACE COMPLEXITY:")
    
    def find_duplicates_space_efficient(items):
        """Find duplicates using O(n) time, O(1) space (destructive)."""
        duplicates = []
        items.sort()  # Sorts in-place, O(n log n) time, O(1) space
        
        for i in range(1, len(items)):
            if items[i] == items[i-1]:
                duplicates.append(items[i])
        
        return duplicates
    
    def find_duplicates_time_efficient(items):
        """Find duplicates using O(n) time, O(n) space."""
        seen = set()
        duplicates = set()
        
        for item in items:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
        
        return list(duplicates)
    
    # Test data
    items = [random.randint(1, 1000) for _ in range(10000)]
    
    # Time-efficient version
    start = time.perf_counter()
    result_time = find_duplicates_time_efficient(items)
    time_efficient = time.perf_counter() - start
    
    # Space-efficient version
    start = time.perf_counter()
    result_space = find_duplicates_space_efficient(items.copy())  # Copy to preserve original
    space_efficient = time.perf_counter() - start
    
    print(f"   Finding duplicates in {len(items):,} items:")
    print(f"   Time-efficient (hash set): {time_efficient:.4f} seconds")
    print(f"   Space-efficient (sorting): {space_efficient:.4f} seconds")
    print(f"   Time-efficient is {space_efficient/time_efficient:.1f}x faster")
    print(f"   Memory: hash set uses O(n) extra space")
    print(f"   Memory: sorting uses O(1) extra space")
    print(f"   Found {len(result_time)} duplicates")
    
    # 2. Precomputation vs On-demand
    print("\n2. PRECOMPUTATION VS ON-DEMAND COMPUTATION:")
    
    class PrimeCheckerPrecomputed:
        """Precomputes primes up to a limit."""
        
        def __init__(self, limit):
            self.limit = limit
            self.is_prime = [True] * (limit + 1)
            self.is_prime[0:2] = [False, False]
            
            # Precompute sieve
            for i in range(2, int(limit ** 0.5) + 1):
                if self.is_prime[i]:
                    for j in range(i * i, limit + 1, i):
                        self.is_prime[j] = False
        
        def check(self, n):
            """Check if number is prime (O(1) after precomputation)."""
            if n > self.limit:
                raise ValueError(f"Number {n} exceeds precomputed limit {self.limit}")
            return self.is_prime[n]
    
    class PrimeCheckerOnDemand:
        """Checks primes on-demand."""
        
        def check(self, n):
            """Check if number is prime (O(√n) each call)."""
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
    
    limit = 1_000_000
    
    # Create instances
    precomputed = PrimeCheckerPrecomputed(limit)
    on_demand = PrimeCheckerOnDemand()
    
    # Test numbers
    test_numbers = [random.randint(2, limit) for _ in range(1000)]
    
    # Time precomputed version
    start = time.perf_counter()
    results_pre = [precomputed.check(n) for n in test_numbers]
    time_pre = time.perf_counter() - start
    
    # Time on-demand version
    start = time.perf_counter()
    results_ondemand = [on_demand.check(n) for n in test_numbers]
    time_ondemand = time.perf_counter() - start
    
    print(f"\n   Checking 1,000 random numbers for primality:")
    print(f"   Precomputed (up to {limit:,}):")
    print(f"   - Initialization time: N/A (one-time cost)")
    print(f"   - Check time: {time_pre:.4f} seconds")
    print(f"   - Memory: ~{sys.getsizeof(precomputed.is_prime)/1024/1024:.1f} MB")
    
    print(f"\n   On-demand (per check):")
    print(f"   - Initialization time: 0")
    print(f"   - Check time: {time_ondemand:.4f} seconds")
    print(f"   - Memory: minimal")
    
    print(f"\n   Precomputed is {time_ondemand/time_pre:.1f}x faster for repeated checks")
    print(f"   Results match: {results_pre == results_ondemand}")
    
    # 3. Compression Tradeoffs
    print("\n3. COMPRESSION TRADEOFFS:")
    
    import zlib
    import pickle
    
    # Create some data to compress
    data = {
        "users": [
            {"id": i, "name": f"User{i}", "email": f"user{i}@example.com"}
            for i in range(1000)
        ]
    }
    
    # Serialize data
    serialized = pickle.dumps(data)
    
    # Test different compression levels
    compression_times = {}
    compression_sizes = {}
    
    for level in range(10):
        start = time.perf_counter()
        compressed = zlib.compress(serialized, level=level)
        compress_time = time.perf_counter() - start
        
        # Decompression time
        start = time.perf_counter()
        decompressed = zlib.decompress(compressed)
        decompress_time = time.perf_counter() - start
        
        compression_times[level] = (compress_time, decompress_time)
        compression_sizes[level] = len(compressed)
    
    print(f"   Original size: {len(serialized):,} bytes")
    print(f"   Compression results:")
    
    for level in [0, 1, 3, 6, 9]:
        compress_time, decompress_time = compression_times[level]
        compressed_size = compression_sizes[level]
        ratio = compressed_size / len(serialized) * 100
        
        print(f"   Level {level}:")
        print(f"     Size: {compressed_size:,} bytes ({ratio:.1f}%)")
        print(f"     Compression time: {compress_time:.4f}s")
        print(f"     Decompression time: {decompress_time:.4f}s")
    
    print("\n   Tradeoff: Higher compression = smaller size but slower")
    print("   Level 0: No compression (fastest)")
    print("   Level 6: Good balance (default)")
    print("   Level 9: Maximum compression (slowest)")
    
    # 4. Caching Tradeoffs
    print("\n4. CACHING TRADEOFFS:")
    
    def expensive_operation(x):
        """Simulate expensive operation."""
        time.sleep(0.01)  # 10ms
        return x * 2
    
    cache = {}
    
    def cached_operation(x):
        """Cached version."""
        if x not in cache:
            cache[x] = expensive_operation(x)
        return cache[x]
    
    # Simulate workload
    requests = [random.randint(1, 100) for _ in range(1000)]
    
    # Without cache
    start = time.perf_counter()
    results_no_cache = [expensive_operation(x) for x in requests]
    time_no_cache = time.perf_counter() - start
    
    # With cache
    start = time.perf_counter()
    results_cache = [cached_operation(x) for x in requests]
    time_cache = time.perf_counter() - start
    
    # Calculate hit rate
    unique_values = len(set(requests))
    hit_rate = (len(requests) - unique_values) / len(requests) * 100
    
    print(f"\n   Simulating 1,000 requests with 100 unique values:")
    print(f"   Without cache: {time_no_cache:.2f} seconds")
    print(f"   With cache:    {time_cache:.2f} seconds")
    print(f"   Speedup: {time_no_cache/time_cache:.1f}x")
    print(f"   Cache hit rate: {hit_rate:.1f}%")
    print(f"   Cache memory: {len(cache)} entries")
    print(f"   Memory per entry: ~{sys.getsizeof(cache)//len(cache)} bytes")
    
    # 5. Lazy Evaluation vs Eager Evaluation
    print("\n5. LAZY VS EAGER EVALUATION:")
    
    class DataProcessorEager:
        """Processes data eagerly (immediately)."""
        
        def __init__(self, data):
            self.data = data
            # Eager: process immediately
            self.processed = self._process_data(data)
        
        def _process_data(self, data):
            """Expensive processing."""
            time.sleep(0.1)  # Simulate processing
            return [x * 2 for x in data]
        
        def get_results(self):
            return self.processed
    
    class DataProcessorLazy:
        """Processes data lazily (on-demand)."""
        
        def __init__(self, data):
            self.data = data
            self._processed = None  # Not processed yet
        
        def _process_data(self, data):
            """Expensive processing."""
            time.sleep(0.1)  # Simulate processing
            return [x * 2 for x in data]
        
        def get_results(self):
            # Lazy: process only when needed
            if self._processed is None:
                self._processed = self._process_data(self.data)
            return self._processed
    
    # Test data
    data = list(range(100))
    
    print("   Creating data processors:")
    
    # Eager: pays cost immediately
    start = time.perf_counter()
    eager = DataProcessorEager(data)
    creation_time_eager = time.perf_counter() - start
    
    # Lazy: minimal creation cost
    start = time.perf_counter()
    lazy = DataProcessorLazy(data)
    creation_time_lazy = time.perf_counter() - start
    
    print(f"   Eager creation: {creation_time_eager:.4f} seconds")
    print(f"   Lazy creation:  {creation_time_lazy:.4f} seconds")
    
    # Access results
    print("\n   Accessing results:")
    
    start = time.perf_counter()
    results_eager = eager.get_results()
    access_time_eager = time.perf_counter() - start
    
    start = time.perf_counter()
    results_lazy = lazy.get_results()
    access_time_lazy = time.perf_counter() - start
    
    print(f"   Eager access: {access_time_eager:.4f} seconds")
    print(f"   Lazy access:  {access_time_lazy:.4f} seconds")
    
    print("\n   Tradeoffs:")
    print("   Eager: Pay cost upfront, fast access later")
    print("   Lazy: Fast creation, pay cost on first access")
    print("   Use eager if you'll always need the results")
    print("   Use lazy if you might not need the results")
    
    # 6. Decision Framework
    print("\n6. DECISION FRAMEWORK FOR TRADEOFFS:")
    
    print("""
    WHEN TO PRIORITIZE SPEED:
    
    1. REAL-TIME SYSTEMS:
       - Trading systems
       - Game engines
       - User interfaces
    
    2. HIGH-THROUGHPUT SYSTEMS:
       - Data processing pipelines
       - Web servers
       - Batch processing
    
    3. FREQUENTLY CALLED CODE:
       - Inner loops
       - Library functions
       - Core algorithms
    
    WHEN TO PRIORITIZE MEMORY:
    
    1. MEMORY-CONSTRAINED ENVIRONMENTS:
       - Embedded systems
       - Mobile devices
       - Cloud functions
    
    2. LARGE DATASETS:
       - Big data processing
       - Machine learning
       - Scientific computing
    
    3. SCALABILITY REQUIREMENTS:
       - Many concurrent users
       - Long-running processes
       - Cost optimization
    
    GENERAL GUIDELINES:
    
    1. PROFILE FIRST:
       - Don't guess what's important
       - Measure actual usage
    
    2. CONSIDER DATA ACCESS PATTERNS:
       - Read-heavy vs write-heavy
       - Sequential vs random access
       - Cache locality
    
    3. THINK ABOUT SCALABILITY:
       - How will requirements change?
       - What are the growth projections?
    
    4. BALANCE IS KEY:
       - Extreme optimization in one area often hurts another
       - Consider total cost of ownership
       - Maintainability matters
    """)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Run all debugging and performance optimization demonstrations."""
    
    print("PYTHON DEBUGGING & PERFORMANCE OPTIMIZATION COMPREHENSIVE GUIDE")
    print("="*60)
    
    # Run all demonstrations
    stack_traces_demo()
    logging_demo()
    debuggers_demo()
    profiling_demo()
    python_slow_demo()
    efficient_data_structures_demo()
    builtin_vs_custom_demo()
    caching_demo()
    memory_vs_speed_demo()
    
    print("\n" + "="*60)
    print("FINAL SUMMARY & RECOMMENDATIONS")
    print("="*60)
    
    print("""
    DEBUGGING KEY TAKEAWAYS:
    
    1. READING STACK TRACES:
       - Start from the bottom (error message)
       - Trace back through function calls
       - Look for line numbers and file names
       - Understand common error patterns
    
    2. EFFECTIVE LOGGING:
       - Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
       - Structure loggers hierarchically
       - Include context in log messages
       - Use JSON formatting for production
    
    3. USING DEBUGGERS:
       - PDB for command-line debugging
       - IDE debuggers for visual debugging
       - Set breakpoints strategically
       - Use watch expressions and step-through
    
    PERFORMANCE OPTIMIZATION KEY TAKEAWAYS:
    
    1. PROFILE BEFORE OPTIMIZING:
       - Use cProfile for time profiling
       - Use memory_profiler for memory analysis
       - Focus on bottlenecks (80/20 rule)
       - Measure with realistic data
    
    2. UNDERSTAND PYTHON'S CHARACTERISTICS:
       - Python is fast for I/O, slower for CPU
       - Built-in functions are optimized (C implementations)
       - Choose algorithms wisely
       - Consider PyPy for CPU-bound code
    
    3. CHOOSE DATA STRUCTURES WISELY:
       - Lists for ordered, modifiable collections
       - Sets for membership testing
       - Dicts for key-value lookups
       - Tuples for immutable sequences
       - Collections module for specialized needs
    
    4. LEVERAGE BUILT-IN FUNCTIONS:
       - Built-ins are 2-100x faster than Python loops
       - Use list comprehensions over map()/filter()
       - Use ''.join() for string concatenation
       - Let Python do the heavy lifting
    
    5. IMPLEMENT STRATEGIC CACHING:
       - Use @lru_cache for function memoization
       - Cache expensive computations
       - Consider TTL for time-sensitive data
       - Balance cache size vs hit rate
    
    6. BALANCE MEMORY VS SPEED:
       - Precompute for speed, compute on-demand for memory
       - Compress data for storage, decompress for speed
       - Cache for repeated access
       - Choose algorithms based on constraints
    
    PRACTICAL WORKFLOW:
    
    1. WRITE CORRECT CODE FIRST:
       - Make it work, make it right, make it fast
       - Don't optimize prematurely
    
    2. PROFILE TO FIND BOTTLENECKS:
       - Use profiling tools
       - Identify hot spots
       - Focus on impactful optimizations
    
    3. APPLY OPTIMIZATION TECHNIQUES:
       - Choose better algorithms
       - Use appropriate data structures
       - Leverage built-in functions
       - Implement caching where beneficial
    
    4. TEST AND MEASURE:
       - Verify optimizations don't break functionality
       - Measure performance improvements
       - Consider edge cases and scalability
    
    5. DOCUMENT DECISIONS:
       - Why optimizations were made
       - Tradeoffs considered
       - Performance characteristics
    
    FINAL REMINDERS:
    
    - "Premature optimization is the root of all evil" - Donald Knuth
    - Readability and maintainability are important
    - Python is often "fast enough" for business logic
    - Use the right tool for the job (consider C extensions, NumPy, etc.)
    - Always measure with your specific use case and data
    """)

if __name__ == "__main__":
    main()