"""
ITERATORS, GENERATORS, AND COMPREHENSIONS IN PYTHON
Covers iterator protocol, generators, itertools, and comprehensions.
"""

import itertools
import time
import sys
from typing import Iterator, Generator, List, Dict, Set, Tuple, Any

# ============================================================================
# PART 1: ITERATORS
# ============================================================================

print("=" * 60)
print("ITERATORS")
print("=" * 60)
print("""
Iterators are objects that implement:
1. __iter__() method that returns self
2. __next__() method that returns the next value
   or raises StopIteration when done

All iterators are iterables, but not all iterables are iterators.
""")

# ============================================================================
# 1. ITERATOR PROTOCOL
# ============================================================================

print("\n1. ITERATOR PROTOCOL")
print("-" * 40)

class CountdownIterator:
    """Custom iterator that counts down from n to 1."""
    
    def __init__(self, start: int):
        self.current = start
    
    def __iter__(self) -> 'CountdownIterator':
        """Return self - iterator objects return themselves."""
        return self
    
    def __next__(self) -> int:
        """Return next value or raise StopIteration."""
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print("Custom CountdownIterator from 5:")
countdown = CountdownIterator(5)

# Manual iteration using next()
print("Manual iteration with next():")
try:
    print(f"  next(countdown): {next(countdown)}")
    print(f"  next(countdown): {next(countdown)}")
    print(f"  next(countdown): {next(countdown)}")
    print(f"  next(countdown): {next(countdown)}")
    print(f"  next(countdown): {next(countdown)}")
    print(f"  next(countdown): {next(countdown)}")  # This raises StopIteration
except StopIteration:
    print("  StopIteration raised - iterator exhausted")

# Using in for loop (automatically handles StopIteration)
print("\nUsing in for loop:")
for number in CountdownIterator(3):
    print(f"  {number}")

# ============================================================================
# 2. ITERABLE vs ITERATOR
# ============================================================================

print("\n2. ITERABLE vs ITERATOR")
print("-" * 40)

class FibonacciIterable:
    """An iterable that creates new iterators each time."""
    
    def __init__(self, limit: int):
        self.limit = limit
    
    def __iter__(self) -> Iterator[int]:
        """Return a NEW iterator each time called."""
        return FibonacciIterator(self.limit)

class FibonacciIterator:
    """Iterator for Fibonacci sequence."""
    
    def __init__(self, limit: int):
        self.limit = limit
        self.a, self.b = 0, 1
        self.count = 0
    
    def __iter__(self) -> 'FibonacciIterator':
        return self
    
    def __next__(self) -> int:
        if self.count >= self.limit:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return value

print("Demonstrating iterable (creates new iterators):")
fib_iterable = FibonacciIterable(5)

# First iteration
print("First iteration:")
for num in fib_iterable:
    print(f"  {num}")

# Second iteration (works because __iter__ creates new iterator)
print("\nSecond iteration (new iterator):")
for num in fib_iterable:
    print(f"  {num}")

# Contrast with iterator (can't restart)
print("\nDirect iterator (can't restart):")
fib_iterator = FibonacciIterator(3)
for num in fib_iterator:
    print(f"  {num}")

print("Trying to iterate exhausted iterator:")
try:
    for num in fib_iterator:  # Won't execute - iterator is exhausted
        print(f"  {num}")
except Exception as e:
    print(f"  No output - iterator is exhausted")

# ============================================================================
# 3. BUILT-IN ITERATOR FUNCTIONS
# ============================================================================

print("\n3. BUILT-IN ITERATOR FUNCTIONS")
print("-" * 40)

# iter() creates an iterator from an iterable
print("Using iter() function:")
numbers = [1, 2, 3, 4, 5]
numbers_iterator = iter(numbers)

print(f"numbers: {numbers}")
print(f"type(numbers_iterator): {type(numbers_iterator)}")
print(f"next(numbers_iterator): {next(numbers_iterator)}")
print(f"next(numbers_iterator): {next(numbers_iterator)}")

# enumerate() creates iterator of (index, value) pairs
print("\nUsing enumerate():")
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")

# zip() combines multiple iterables
print("\nUsing zip():")
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"  {name} is {age} years old")

# reversed() creates reverse iterator
print("\nUsing reversed():")
for num in reversed(range(5)):
    print(f"  {num}")

# ============================================================================
# PART 2: GENERATORS
# ============================================================================

print("\n" + "=" * 60)
print("GENERATORS")
print("=" * 60)
print("""
Generators are a simpler way to create iterators.
They use yield instead of return.
When yield is called, the function's state is saved.
Generators are iterators (they implement __iter__ and __next__).
""")

# ============================================================================
# 1. GENERATOR FUNCTIONS
# ============================================================================

print("\n1. GENERATOR FUNCTIONS")
print("-" * 40)

def countdown_generator(start: int) -> Generator[int, None, None]:
    """Generator version of countdown."""
    current = start
    while current > 0:
        yield current  # Pauses here, returns value
        current -= 1

print("Generator countdown from 5:")
for number in countdown_generator(5):
    print(f"  {number}")

# Generator for infinite sequence
def fibonacci_generator() -> Generator[int, None, None]:
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print("\nFibonacci generator (first 10 numbers):")
fib = fibonacci_generator()
for _ in range(10):
    print(f"  {next(fib)}")

# ============================================================================
# 2. GENERATOR EXPRESSIONS
# ============================================================================

print("\n2. GENERATOR EXPRESSIONS")
print("-" * 40)
print("""
Generator expressions are like list comprehensions but:
• Use parentheses instead of brackets
• Create generators (lazy evaluation)
• Memory efficient
""")

# List comprehension (eager, creates list)
numbers = [1, 2, 3, 4, 5]
squares_list = [x**2 for x in numbers]
print(f"List comprehension (eager): {squares_list}")
print(f"Type: {type(squares_list)}")

# Generator expression (lazy, creates generator)
squares_gen = (x**2 for x in numbers)
print(f"\nGenerator expression (lazy): {squares_gen}")
print(f"Type: {type(squares_gen)}")
print(f"Converted to list: {list(squares_gen)}")

# Using generator expression directly
print("\nUsing generator expression in functions:")
total = sum(x**2 for x in range(10))
print(f"Sum of squares 0-9: {total}")

# Compare memory usage
print("\nMemory comparison:")
import sys

# List comprehension stores all values
list_comp = [x for x in range(1000000)]
print(f"List comprehension memory: {sys.getsizeof(list_comp):,} bytes")

# Generator expression stores algorithm
gen_exp = (x for x in range(1000000))
print(f"Generator expression memory: {sys.getsizeof(gen_exp):,} bytes")

# ============================================================================
# 3. YIELD FROM (DELEGATING TO SUBGENERATORS)
# ============================================================================

print("\n3. YIELD FROM (SUB-GENERATOR DELEGATION)")
print("-" * 40)

def first_n_numbers(n: int) -> Generator[int, None, None]:
    """Yield numbers from 0 to n-1."""
    for i in range(n):
        yield i

def first_n_evens(n: int) -> Generator[int, None, None]:
    """Yield even numbers from 0 to 2n-2."""
    for i in range(n):
        yield i * 2

def combined_generator() -> Generator[int, None, None]:
    """Combine multiple generators using yield from."""
    print("Starting first generator...")
    yield from first_n_numbers(3)
    print("Starting second generator...")
    yield from first_n_evens(3)
    print("All done!")

print("Combined generator output:")
for value in combined_generator():
    print(f"  {value}")

# ============================================================================
# 4. GENERATOR STATE AND COMMUNICATION
# ============================================================================

print("\n4. GENERATOR STATE AND COMMUNICATION")
print("-" * 40)

def interactive_generator() -> Generator[str, str, str]:
    """Generator that can receive values via send()."""
    print("Generator started")
    received = None
    
    while True:
        # Receive value via send(), or None via next()
        value = yield f"Received: {received}"
        
        if value == "STOP":
            return "Generator stopped gracefully"
        
        received = value
        print(f"Generator processing: {value}")

print("Interactive generator example:")
gen = interactive_generator()

# Start generator (must send None first, or use next())
print(f"Initial: {next(gen)}")

# Send values to generator
print(f"Send 'Hello': {gen.send('Hello')}")
print(f"Send 'World': {gen.send('World')}")

# Stop generator
try:
    gen.send("STOP")
except StopIteration as e:
    print(f"Generator stopped with value: {e.value}")

# Generator with throw() for exception handling
def resilient_generator() -> Generator[int, None, None]:
    """Generator that handles exceptions."""
    for i in range(5):
        try:
            yield i
        except ValueError as e:
            print(f"Caught ValueError: {e}")
            yield -1  # Return error indicator
        except GeneratorExit:
            print("Generator closing...")
            raise  # Re-raise to allow cleanup

print("\nResilient generator with throw():")
gen = resilient_generator()
for value in gen:
    print(f"  Yielded: {value}")
    if value == 2:
        print("  Throwing ValueError...")
        gen.throw(ValueError("Test error"))

# ============================================================================
# PART 3: ITERTOOLS MODULE
# ============================================================================

print("\n" + "=" * 60)
print("ITERTOOLS MODULE")
print("=" * 60)
print("""
itertools provides building blocks for efficient iteration.
All functions return iterators (memory efficient).
""")

# ============================================================================
# 1. INFINITE ITERATORS
# ============================================================================

print("\n1. INFINITE ITERATORS")
print("-" * 40)

print("count(start=10, step=2):")
counter = itertools.count(start=10, step=2)
for _ in range(5):
    print(f"  {next(counter)}")

print("\ncycle('ABC'):")
cycler = itertools.cycle('ABC')
for _ in range(7):
    print(f"  {next(cycler)}", end=" ")
print()

print("\nrepeat(7, times=4):")
repeater = itertools.repeat(7, times=4)
print(f"  {list(repeater)}")

# ============================================================================
# 2. COMBINATORIC ITERATORS
# ============================================================================

print("\n2. COMBINATORIC ITERATORS")
print("-" * 40)

print("product('AB', '12'):")
print(f"  {list(itertools.product('AB', '12'))}")

print("\npermutations('ABC', 2):")
print(f"  {list(itertools.permutations('ABC', 2))}")

print("\ncombinations('ABCD', 2):")
print(f"  {list(itertools.combinations('ABCD', 2))}")

print("\ncombinations_with_replacement('ABC', 2):")
print(f"  {list(itertools.combinations_with_replacement('ABC', 2))}")

# ============================================================================
# 3. TERMINATING ITERATORS
# ============================================================================

print("\n3. TERMINATING ITERATORS")
print("-" * 40)

print("accumulate([1, 2, 3, 4, 5]):")
print(f"  {list(itertools.accumulate([1, 2, 3, 4, 5]))}")

print("\naccumulate([1, 2, 3, 4, 5], lambda x, y: x * y):")
print(f"  {list(itertools.accumulate([1, 2, 3, 4, 5], lambda x, y: x * y))}")

print("\nchain('ABC', 'DEF'):")
print(f"  {list(itertools.chain('ABC', 'DEF'))}")

print("\nchain.from_iterable(['ABC', 'DEF']):")
print(f"  {list(itertools.chain.from_iterable(['ABC', 'DEF']))}")

print("\ncompress('ABCDEF', [1, 0, 1, 0, 1, 1]):")
print(f"  {list(itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1]))}")

print("\ndropwhile(lambda x: x < 5, [1, 4, 6, 4, 1]):")
print(f"  {list(itertools.dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1]))}")

print("\ntakewhile(lambda x: x < 5, [1, 4, 6, 4, 1]):")
print(f"  {list(itertools.takewhile(lambda x: x < 5, [1, 4, 6, 4, 1]))}")

# ============================================================================
# 4. GROUPING AND MORE
# ============================================================================

print("\n4. GROUPING AND MORE")
print("-" * 40)

print("groupby('AAAABBBCCD'):")
for key, group in itertools.groupby('AAAABBBCCD'):
    print(f"  {key}: {list(group)}")

print("\ngroupby with sorting:")
data = sorted(['cat', 'dog', 'cow', 'duck', 'chicken'], key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")

print("\npairwise('ABCDEFG'):")
print(f"  {list(itertools.pairwise('ABCDEFG'))}")

print("\nislice('ABCDEFG', 2, None, 2):")
print(f"  {list(itertools.islice('ABCDEFG', 2, None, 2))}")

# ============================================================================
# PART 4: MEMORY EFFICIENCY USE CASES
# ============================================================================

print("\n" + "=" * 60)
print("MEMORY EFFICIENCY USE CASES")
print("=" * 60)

# ============================================================================
# 1. PROCESSING LARGE FILES
# ============================================================================

print("\n1. PROCESSING LARGE FILES")
print("-" * 40)

def read_large_file_generator(filename: str) -> Generator[str, None, None]:
    """Read large file line by line using generator."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

print("Simulating large file processing:")
# Create a temporary file for demonstration
import tempfile

with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    for i in range(10000):
        f.write(f"Line {i}: Some data here\n")
    temp_filename = f.name

# Process with generator (memory efficient)
print("Processing with generator (memory efficient):")
line_count = 0
for line in read_large_file_generator(temp_filename):
    if line_count < 3:
        print(f"  {line[:50]}...")
    line_count += 1
    # Simulate processing
    _ = line.upper()

print(f"  Total lines processed: {line_count}")
print(f"  Memory used: ~constant")

# Clean up
import os
os.unlink(temp_filename)

# ============================================================================
# 2. PROCESSING LARGE DATASETS
# ============================================================================

print("\n2. PROCESSING LARGE DATASETS")
print("-" * 40)

def process_dataset() -> None:
    """Compare memory usage for large dataset processing."""
    
    # Simulate large dataset
    print("Creating large dataset...")
    
    # Method 1: List comprehension (memory intensive)
    print("\nMethod 1: List comprehension")
    start_time = time.time()
    data = [i for i in range(1000000)]  # Creates list in memory
    processed = [x * 2 for x in data]   # Creates another list
    end_time = time.time()
    print(f"  Memory for data list: {sys.getsizeof(data):,} bytes")
    print(f"  Memory for processed list: {sys.getsizeof(processed):,} bytes")
    print(f"  Time: {end_time - start_time:.4f} seconds")
    
    # Method 2: Generator expression (memory efficient)
    print("\nMethod 2: Generator expression")
    start_time = time.time()
    # No list created - just generator expressions
    total = sum(x * 2 for x in range(1000000))
    end_time = time.time()
    print(f"  Total: {total}")
    print(f"  Time: {end_time - start_time:.4f} seconds")
    print(f"  Memory: ~constant (no large lists created)")

process_dataset()

# ============================================================================
# 3. PIPELINE PROCESSING
# ============================================================================

print("\n3. PIPELINE PROCESSING")
print("-" * 40)

def data_pipeline_example() -> None:
    """Example of memory-efficient data pipeline."""
    
    def read_data() -> Generator[int, None, None]:
        """Simulate reading data from source."""
        print("  Reading data...")
        for i in range(10):  # In real case, could be millions
            yield i
    
    def filter_data(data: Generator[int, None, None]) -> Generator[int, None, None]:
        """Filter even numbers."""
        print("  Filtering even numbers...")
        for item in data:
            if item % 2 == 0:
                yield item
    
    def transform_data(data: Generator[int, None, None]) -> Generator[int, None, None]:
        """Transform data (square it)."""
        print("  Transforming data (squaring)...")
        for item in data:
            yield item ** 2
    
    def process_data(data: Generator[int, None, None]) -> int:
        """Process data (sum it)."""
        print("  Processing data (summing)...")
        total = 0
        for item in data:
            total += item
        return total
    
    # Build pipeline (each step processes items one by one)
    print("Building data pipeline:")
    data_stream = read_data()
    filtered_stream = filter_data(data_stream)
    transformed_stream = transform_data(filtered_stream)
    result = process_data(transformed_stream)
    
    print(f"\nResult: {result}")
    print("Note: Only one item in memory at each pipeline stage!")

data_pipeline_example()

# ============================================================================
# 4. INFINITE SEQUENCES
# ============================================================================

print("\n4. INFINITE SEQUENCES")
print("-" * 40)

def prime_generator() -> Generator[int, None, None]:
    """Generate prime numbers infinitely."""
    primes = []
    candidate = 2
    
    while True:
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        
        if is_prime:
            primes.append(candidate)
            yield candidate
        
        candidate += 1

print("First 10 prime numbers:")
prime_gen = prime_generator()
for i in range(10):
    print(f"  {next(prime_gen)}")

# ============================================================================
# PART 5: COMPREHENSIONS
# ============================================================================

print("\n" + "=" * 60)
print("COMPREHENSIONS")
print("=" * 60)
print("""
Comprehensions provide a concise way to create collections.
Types: List, Dict, Set (no tuple comprehension, but generator expression).
""")

# ============================================================================
# 1. LIST COMPREHENSIONS
# ============================================================================

print("\n1. LIST COMPREHENSIONS")
print("-" * 40)

# Basic list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Basic: {squares}")

# With condition
evens = [x for x in numbers if x % 2 == 0]
print(f"With condition (evens): {evens}")

# With if-else (ternary in comprehension)
parity = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(f"With if-else: {parity}")

# Multiple loops
pairs = [(x, y) for x in range(3) for y in range(3)]
print(f"Multiple loops: {pairs}")

# Real-world example: Processing strings
words = ["hello", "world", "python", "programming"]
lengths = [(word, len(word)) for word in words]
print(f"Word lengths: {lengths}")

# ============================================================================
# 2. DICTIONARY COMPREHENSIONS
# ============================================================================

print("\n2. DICTIONARY COMPREHENSIONS")
print("-" * 40)

# Basic dict comprehension
numbers = [1, 2, 3, 4, 5]
square_dict = {x: x**2 for x in numbers}
print(f"Basic: {square_dict}")

# From list of tuples
pairs = [("a", 1), ("b", 2), ("c", 3)]
dict_from_pairs = {k: v for k, v in pairs}
print(f"From tuples: {dict_from_pairs}")

# With condition
even_squares = {x: x**2 for x in numbers if x % 2 == 0}
print(f"With condition: {even_squares}")

# Transforming keys and values
words = ["apple", "banana", "cherry"]
word_lengths = {word.upper(): len(word) for word in words}
print(f"Transformed keys: {word_lengths}")

# Swapping keys and values (if values are hashable)
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"Swapped keys/values: {swapped}")

# ============================================================================
# 3. SET COMPREHENSIONS
# ============================================================================

print("\n3. SET COMPREHENSIONS")
print("-" * 40)

# Basic set comprehension
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in numbers}
print(f"Basic (duplicates removed): {unique_squares}")

# From string (unique characters)
text = "hello world"
unique_chars = {char for char in text if char != ' '}
print(f"Unique characters: {sorted(unique_chars)}")

# With condition
words = ["apple", "banana", "cherry", "date", "elderberry"]
long_words = {word for word in words if len(word) > 5}
print(f"Long words: {long_words}")

# Set operations in comprehension
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}
intersection_comp = {x for x in set_a if x in set_b}
print(f"Intersection via comprehension: {intersection_comp}")
print(f"Using set operator: {set_a & set_b}")

# ============================================================================
# 4. NESTED COMPREHENSIONS
# ============================================================================

print("\n4. NESTED COMPREHENSIONS")
print("-" * 40)

# Simple nested list comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")

# Transpose matrix
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(f"Transposed matrix: {transposed}")

# Nested dictionary comprehension
students = {
    "Alice": {"math": 90, "science": 85},
    "Bob": {"math": 78, "science": 92},
    "Charlie": {"math": 88, "science": 79}
}

# Get all math scores
math_scores = {name: scores["math"] for name, scores in students.items()}
print(f"Math scores: {math_scores}")

# Complex nested example: Cartesian product with filtering
list_a = [1, 2, 3]
list_b = ['a', 'b', 'c']
filtered_pairs = [(x, y) for x in list_a if x % 2 != 0 for y in list_b if y != 'b']
print(f"Filtered Cartesian product: {filtered_pairs}")

# ============================================================================
# 5. READABILITY TRADE-OFFS
# ============================================================================

print("\n5. READABILITY TRADE-OFFS")
print("-" * 40)

print("Example 1: Simple vs Complex Comprehension")

# Simple comprehension (easy to read)
simple = [x*2 for x in range(10) if x % 2 == 0]
print(f"Simple: {simple}")

# Complex comprehension (harder to read)
complex_comp = [
    (x, y, z) 
    for x in range(3) 
    for y in range(3) 
    for z in range(3) 
    if x + y + z > 3 and x != y
]
print(f"Complex (hard to read): {complex_comp}")

print("\nExample 2: Equivalent For Loop")
print("Complex comprehension above is equivalent to:")

result = []
for x in range(3):
    for y in range(3):
        for z in range(3):
            if x + y + z > 3 and x != y:
                result.append((x, y, z))
print(f"For loop version: {result}")

print("\nWhen to use comprehensions vs loops:")
print("-" * 40)
print("""
USE COMPREHENSIONS WHEN:
1. The logic is simple and fits on one line
2. You're creating a new collection
3. The transformation/filtering is straightforward
4. Readability is improved (not worsened)

USE FOR LOOPS WHEN:
1. The logic is complex with multiple conditions
2. You need to modify existing data structures
3. You need side effects (printing, logging, etc.)
4. The comprehension becomes hard to read
5. You need exception handling within the loop

GUIDELINES:
1. Keep comprehensions to 2 levels of nesting max
2. Avoid complex if-else logic in comprehensions
3. If it doesn't fit on one line comfortably, use a loop
4. Consider using helper functions for complex transformations
""")

# ============================================================================
# 6. PERFORMANCE COMPARISON
# ============================================================================

print("\n6. PERFORMANCE COMPARISON")
print("-" * 40)

def performance_comparison():
    """Compare performance of comprehensions vs loops."""
    
    import timeit
    
    setup = """
numbers = list(range(10000))
"""
    
    # List comprehension
    list_comp_time = timeit.timeit(
        "[x**2 for x in numbers]",
        setup=setup,
        number=1000
    )
    
    # For loop equivalent
    for_loop_time = timeit.timeit(
        """
result = []
for x in numbers:
    result.append(x**2)
        """,
        setup=setup,
        number=1000
    )
    
    # Generator expression
    gen_exp_time = timeit.timeit(
        "sum(x**2 for x in numbers)",
        setup=setup,
        number=1000
    )
    
    print(f"List comprehension: {list_comp_time:.4f} seconds")
    print(f"For loop: {for_loop_time:.4f} seconds")
    print(f"Generator expression (sum): {gen_exp_time:.4f} seconds")
    
    print("\nNote: Comprehensions are often faster due to:")
    print("1. Optimized C implementation in Python")
    print("2. No function call overhead for append()")
    print("3. Less Python bytecode to execute")

performance_comparison()

# ============================================================================
# COMPREHENSIVE EXAMPLE: REAL-WORD DATA PROCESSING
# ============================================================================

print("\n" + "=" * 60)
print("COMPREHENSIVE EXAMPLE: DATA ANALYSIS PIPELINE")
print("=" * 60)

def data_analysis_pipeline():
    """Complete example combining all concepts."""
    
    # Simulate sales data
    sales_data = [
        {"product": "Laptop", "price": 999.99, "quantity": 3, "category": "Electronics"},
        {"product": "Mouse", "price": 49.99, "quantity": 10, "category": "Electronics"},
        {"product": "Notebook", "price": 12.99, "quantity": 25, "category": "Stationery"},
        {"product": "Pen", "price": 1.99, "quantity": 100, "category": "Stationery"},
        {"product": "Monitor", "price": 299.99, "quantity": 2, "category": "Electronics"},
        {"product": "Keyboard", "price": 89.99, "quantity": 5, "category": "Electronics"},
        {"product": "Highlighter", "price": 2.49, "quantity": 50, "category": "Stationery"},
    ]
    
    print("Original sales data:")
    for item in sales_data:
        print(f"  {item}")
    
    # 1. Using generator for memory-efficient filtering
    print("\n1. Filtering Electronics (using generator):")
    
    def filter_electronics(data):
        """Generator to filter electronics items."""
        for item in data:
            if item["category"] == "Electronics":
                yield item
    
    electronics_gen = filter_electronics(sales_data)
    electronics_list = list(electronics_gen)
    for item in electronics_list:
        print(f"  {item['product']}: ${item['price']}")
    
    # 2. List comprehension for transformation
    print("\n2. Calculating revenue per product:")
    
    revenue_data = [
        {
            "product": item["product"],
            "revenue": item["price"] * item["quantity"],
            "category": item["category"]
        }
        for item in sales_data
    ]
    
    for item in revenue_data:
        print(f"  {item['product']}: ${item['revenue']:.2f}")
    
    # 3. Dictionary comprehension for aggregation
    print("\n3. Revenue by category (using dict comprehension):")
    
    revenue_by_category = {}
    for item in revenue_data:
        category = item["category"]
        revenue_by_category[category] = revenue_by_category.get(category, 0) + item["revenue"]
    
    print(f"  {revenue_by_category}")
    
    # Alternative using itertools.groupby
    print("\n4. Using itertools.groupby for same analysis:")
    
    # Sort by category first (required for groupby)
    sorted_data = sorted(revenue_data, key=lambda x: x["category"])
    
    for category, items in itertools.groupby(sorted_data, key=lambda x: x["category"]):
        total = sum(item["revenue"] for item in items)
        print(f"  {category}: ${total:.2f}")
    
    # 5. Set comprehension for unique analysis
    print("\n5. Unique product categories:")
    categories = {item["category"] for item in sales_data}
    print(f"  {categories}")
    
    # 6. Nested comprehension for complex query
    print("\n6. High-value transactions (> $500):")
    high_value = [
        (item["product"], item["price"] * item["quantity"])
        for item in sales_data
        if item["price"] * item["quantity"] > 500
    ]
    print(f"  {high_value}")
    
    # 7. Using generator expression for memory efficiency
    print("\n7. Total revenue (using generator expression):")
    total_revenue = sum(
        item["price"] * item["quantity"]
        for item in sales_data
    )
    print(f"  Total revenue: ${total_revenue:.2f}")
    
    # Demonstrate memory difference
    print("\nMemory usage demonstration:")
    print("  Using list comprehension (stores all in memory):")
    all_revenues = [item["price"] * item["quantity"] for item in sales_data]
    print(f"    Memory: {sys.getsizeof(all_revenues)} bytes")
    
    print("  Using generator expression (processes one at a time):")
    gen_revenues = (item["price"] * item["quantity"] for item in sales_data)
    print(f"    Memory: {sys.getsizeof(gen_revenues)} bytes")

data_analysis_pipeline()

# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY AND BEST PRACTICES")
print("=" * 60)

summary = """
KEY CONCEPTS:

1. ITERATORS:
   • Implement __iter__() and __next__() methods
   • Can only be iterated once (exhausted after use)
   • Use iter() to get iterator from iterable

2. GENERATORS:
   • Simplified way to create iterators using yield
   • Generator functions: def with yield
   • Generator expressions: (x for x in iterable)
   • Memory efficient (lazy evaluation)

3. ITERTOOLS:
   • Powerful tools for efficient iteration
   • Infinite iterators: count(), cycle(), repeat()
   • Combinatoric: product(), permutations(), combinations()
   • Terminating: accumulate(), chain(), groupby()

4. COMPREHENSIONS:
   • List: [expr for item in iterable]
   • Dict: {key: value for item in iterable}
   • Set: {expr for item in iterable}
   • No tuple comprehension (use generator expression)

BEST PRACTICES:

1. MEMORY EFFICIENCY:
   • Use generators for large datasets
   • Use itertools for efficient iteration patterns
   • Process data in pipelines, not all at once

2. READABILITY:
   • Keep comprehensions simple (max 2 levels nesting)
   • Use helper functions for complex logic
   • Prefer for loops when comprehensions become unreadable

3. PERFORMANCE:
   • Comprehensions are often faster than equivalent loops
   • Generator expressions save memory for large data
   • Profile before optimizing

4. CHOOSING THE RIGHT TOOL:
   • Small data, simple transformation → List comprehension
   • Large data, memory concerns → Generator expression
   • Complex iteration patterns → itertools
   • Need to resume iteration → Custom iterator
   • Infinite sequences → Generator function

5. COMMON PATTERNS:
   • Data pipelines with generators
   • Lazy loading with generator expressions
   • Memory-efficient file processing
   • Complex aggregations with itertools.groupby
   • Set operations with set comprehensions

REMEMBER:
Python is designed to be readable. Choose the approach that makes
your code easiest to understand while meeting performance requirements.
Often, a combination of these techniques yields the best results!
"""

print(summary)