"""
COMPREHENSIVE GUIDE TO PYTHON STANDARD LIBRARY AND OS/SYSTEM OPERATIONS

This script demonstrates and explains key Python standard library modules
and OS/system operations with practical examples.
"""

# ============================================================================
# PART 1: DATETIME MODULE - Date and Time Operations
# ============================================================================

import datetime
from datetime import date, time, datetime, timedelta, timezone

def datetime_demo():
    """
    The datetime module provides classes for manipulating dates and times.
    
    Key Classes:
    - date: Year, month, day (no timezone)
    - time: Hour, minute, second, microsecond (no date)
    - datetime: Combines date and time
    - timedelta: Difference between two dates/times
    - timezone: Timezone information
    """
    
    print("\n" + "="*60)
    print("DATETIME MODULE DEMONSTRATION")
    print("="*60)
    
    # Current date and time
    now = datetime.now()
    print(f"1. Current datetime: {now}")
    print(f"   Date part: {now.date()}")
    print(f"   Time part: {now.time()}")
    
    # Creating specific dates
    birthday = date(1990, 5, 15)
    print(f"\n2. Specific date (birthday): {birthday}")
    
    # Creating datetime objects
    meeting = datetime(2024, 10, 15, 14, 30, 0)  # Oct 15, 2024 at 2:30 PM
    print(f"3. Meeting datetime: {meeting}")
    
    # Accessing components
    print(f"\n4. Date components:")
    print(f"   Year: {meeting.year}, Month: {meeting.month}, Day: {meeting.day}")
    print(f"   Hour: {meeting.hour}, Minute: {meeting.minute}, Second: {meeting.second}")
    
    # Formatting dates (strftime - string format time)
    print(f"\n5. Date formatting:")
    print(f"   ISO format: {meeting.isoformat()}")
    print(f"   Custom format: {meeting.strftime('%A, %B %d, %Y at %I:%M %p')}")
    print(f"   Short date: {meeting.strftime('%m/%d/%Y')}")
    
    # Parsing dates (strptime - string parse time)
    date_string = "2024-12-25 20:30:00"
    parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print(f"\n6. Parsed date: {parsed_date}")
    
    # Time delta operations
    print(f"\n7. Time delta operations:")
    
    # Add 5 days to current date
    future_date = now + timedelta(days=5, hours=3)
    print(f"   5 days and 3 hours from now: {future_date}")
    
    # Calculate difference between dates
    time_until_meeting = meeting - now
    print(f"   Days until meeting: {time_until_meeting.days} days")
    
    # Working with timezones
    print(f"\n8. Timezone operations:")
    utc_now = datetime.now(timezone.utc)
    print(f"   Current UTC time: {utc_now}")
    
    # Convert to different timezone (example: US/Eastern)
    from datetime import datetime, timezone, timedelta
    eastern = timezone(timedelta(hours=-5))  # UTC-5
    eastern_time = utc_now.astimezone(eastern)
    print(f"   Eastern Time: {eastern_time}")
    
    # Date comparisons
    print(f"\n9. Date comparisons:")
    date1 = date(2024, 1, 15)
    date2 = date(2024, 1, 20)
    print(f"   {date1} > {date2}: {date1 > date2}")
    print(f"   {date1} <= {date2}: {date1 <= date2}")
    
    # Working with just time
    print(f"\n10. Time operations:")
    start_time = time(9, 0, 0)  # 9:00 AM
    end_time = time(17, 30, 0)  # 5:30 PM
    print(f"   Work day: {start_time} to {end_time}")
    print(f"   Is 10:00 AM after start? {time(10, 0, 0) > start_time}")


# ============================================================================
# PART 2: COLLECTIONS MODULE - Advanced Data Structures
# ============================================================================

import collections
from collections import defaultdict, Counter, deque, namedtuple, OrderedDict

def collections_demo():
    """
    The collections module provides specialized container datatypes.
    
    Key Data Structures:
    - defaultdict: Dict with default values for missing keys
    - Counter: Count hashable objects
    - deque: Double-ended queue (fast appends/pops from both ends)
    - namedtuple: Tuple with named fields
    - OrderedDict: Dict that remembers insertion order (less needed in Python 3.7+)
    """
    
    print("\n" + "="*60)
    print("COLLECTIONS MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. defaultdict - Dictionary with default values
    print("\n1. defaultdict Examples:")
    
    # Example 1: Grouping items
    fruits = ['apple', 'banana', 'cherry', 'apple', 'banana', 'apple']
    fruit_count = defaultdict(int)  # default factory is int (returns 0)
    
    for fruit in fruits:
        fruit_count[fruit] += 1
    
    print(f"   Fruit counts: {dict(fruit_count)}")
    
    # Example 2: Grouping by length
    words = ['apple', 'bat', 'car', 'dog', 'elephant']
    words_by_length = defaultdict(list)  # default factory is list (returns [])
    
    for word in words:
        words_by_length[len(word)].append(word)
    
    print(f"   Words by length: {dict(words_by_length)}")
    
    # Example 3: Nested defaultdict (tree structure)
    tree = lambda: defaultdict(tree)  # Factory for nested dicts
    nested_data = tree()
    nested_data['level1']['level2']['level3'] = 'value'
    print(f"   Nested defaultdict: {nested_data['level1']['level2']['level3']}")
    
    # 2. Counter - Counting hashable objects
    print("\n2. Counter Examples:")
    
    # Counting from list
    colors = ['red', 'blue', 'red', 'green', 'blue', 'blue', 'red']
    color_counter = Counter(colors)
    print(f"   Color counts: {color_counter}")
    print(f"   Most common: {color_counter.most_common(2)}")
    print(f"   Blue appears {color_counter['blue']} times")
    
    # Counting from string
    sentence = "the quick brown fox jumps over the lazy dog"
    letter_counter = Counter(sentence.replace(" ", ""))
    print(f"   Top 5 letters: {letter_counter.most_common(5)}")
    
    # Counter arithmetic
    counter1 = Counter(a=3, b=2, c=1)
    counter2 = Counter(a=1, b=2, c=3)
    print(f"\n   Counter1: {counter1}")
    print(f"   Counter2: {counter2}")
    print(f"   Addition: {counter1 + counter2}")
    print(f"   Subtraction: {counter1 - counter2}")
    
    # 3. deque - Double-ended queue
    print("\n3. deque Examples:")
    
    d = deque([1, 2, 3])
    print(f"   Initial deque: {d}")
    
    # Add to both ends
    d.append(4)        # Add to right end
    d.appendleft(0)    # Add to left end
    print(f"   After appends: {d}")
    
    # Remove from both ends
    right_item = d.pop()
    left_item = d.popleft()
    print(f"   Popped right: {right_item}, left: {left_item}")
    print(f"   After pops: {d}")
    
    # Rotate deque
    d.rotate(1)        # Rotate right by 1
    print(f"   After rotate(1): {d}")
    d.rotate(-2)       # Rotate left by 2
    print(f"   After rotate(-2): {d}")
    
    # Max length (bounded deque)
    bounded_d = deque(maxlen=3)
    for i in range(5):
        bounded_d.append(i)
        print(f"   Bounded deque (maxlen=3) after adding {i}: {bounded_d}")
    
    # 4. namedtuple - Tuple with named fields
    print("\n4. namedtuple Examples:")
    
    # Define a Point namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    
    # Create instances
    p1 = Point(10, 20)
    p2 = Point(x=5, y=15)
    
    print(f"   Point 1: x={p1.x}, y={p1.y}")
    print(f"   Point 2: {p2}")
    
    # Access like tuple
    print(f"   Point 1 as tuple: {p1[0]}, {p1[1]}")
    
    # Unpacking
    x, y = p1
    print(f"   Unpacked: x={x}, y={y}")
    
    # _replace creates a new instance
    p3 = p1._replace(x=30)
    print(f"   Modified point: {p3}")
    
    # _asdict converts to OrderedDict
    print(f"   As dict: {p1._asdict()}")
    
    # 5. OrderedDict - Dict that maintains insertion order
    print("\n5. OrderedDict Examples:")
    
    # Python 3.7+ regular dicts maintain order, but OrderedDict has extra features
    od = OrderedDict()
    od['z'] = 1
    od['y'] = 2
    od['x'] = 3
    
    print(f"   OrderedDict: {od}")
    print(f"   Keys in insertion order: {list(od.keys())}")
    
    # Move to end/beginning
    od.move_to_end('z')  # Move 'z' to end
    print(f"   After moving 'z' to end: {list(od.keys())}")
    
    od.move_to_end('y', last=False)  # Move 'y' to beginning
    print(f"   After moving 'y' to beginning: {list(od.keys())}")


# ============================================================================
# PART 3: ITERTOOLS MODULE - Iterator Tools
# ============================================================================

import itertools

def itertools_demo():
    """
    The itertools module provides functions for efficient looping.
    
    Categories:
    1. Infinite iterators: count(), cycle(), repeat()
    2. Finite iterators: chain(), compress(), dropwhile(), takewhile(), etc.
    3. Combinatoric generators: product(), permutations(), combinations()
    """
    
    print("\n" + "="*60)
    print("ITERTOOLS MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. Infinite iterators
    print("\n1. Infinite Iterators:")
    
    # count(start, step)
    print("   count(10, 2):", end=" ")
    for i in itertools.islice(itertools.count(10, 2), 5):  # First 5 elements
        print(i, end=" ")
    print()
    
    # cycle(iterable)
    print("   cycle('ABC'):", end=" ")
    for i, char in enumerate(itertools.cycle('ABC')):
        if i >= 9:  # Stop after 9 iterations
            break
        print(char, end=" ")
    print()
    
    # repeat(object, times)
    print("   repeat(5, 3):", list(itertools.repeat(5, 3)))
    
    # 2. Finite iterators
    print("\n2. Finite Iterators:")
    
    # chain(*iterables) - chain multiple iterables
    chain_result = list(itertools.chain('ABC', 'DEF', 'GHI'))
    print(f"   chain('ABC', 'DEF', 'GHI'): {chain_result}")
    
    # compress(data, selectors) - filter using boolean mask
    data = ['A', 'B', 'C', 'D', 'E']
    selectors = [1, 0, 1, 0, 1]  # True, False, True, False, True
    compress_result = list(itertools.compress(data, selectors))
    print(f"   compress(['A','B','C','D','E'], [1,0,1,0,1]): {compress_result}")
    
    # takewhile(predicate, iterable) - take while predicate is true
    takewhile_result = list(itertools.takewhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7]))
    print(f"   takewhile(x<5, [1..7]): {takewhile_result}")
    
    # dropwhile(predicate, iterable) - drop while predicate is true
    dropwhile_result = list(itertools.dropwhile(lambda x: x < 5, [1, 2, 3, 4, 5, 6, 7]))
    print(f"   dropwhile(x<5, [1..7]): {dropwhile_result}")
    
    # 3. Combinatoric generators
    print("\n3. Combinatoric Generators:")
    
    # product(*iterables, repeat) - Cartesian product
    print("   product('AB', '12'):")
    for a, b in itertools.product('AB', '12'):
        print(f"     {a}{b}", end=" ")
    print()
    
    # permutations(iterable, r) - r-length permutations
    print("   permutations('ABC', 2):")
    for perm in itertools.permutations('ABC', 2):
        print(f"     {''.join(perm)}", end=" ")
    print()
    
    # combinations(iterable, r) - r-length combinations
    print("   combinations('ABC', 2):")
    for comb in itertools.combinations('ABC', 2):
        print(f"     {''.join(comb)}", end=" ")
    print()
    
    # combinations_with_replacement
    print("   combinations_with_replacement('AB', 2):")
    for comb in itertools.combinations_with_replacement('AB', 2):
        print(f"     {''.join(comb)}", end=" ")
    print()
    
    # 4. Practical examples
    print("\n4. Practical Examples:")
    
    # Flatten a list of lists
    lists = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    flattened = list(itertools.chain.from_iterable(lists))
    print(f"   Flatten {lists}: {flattened}")
    
    # Group consecutive items
    data = [1, 1, 1, 2, 2, 3, 1, 1, 2, 2, 2, 3]
    grouped = [(key, list(group)) for key, group in itertools.groupby(data)]
    print(f"   Group consecutive: {grouped}")
    
    # Sliding window (n-grams)
    def sliding_window(iterable, n=2):
        """Yield sliding window of size n."""
        iterators = itertools.tee(iterable, n)
        for i, it in enumerate(iterators):
            # Advance each iterator by i steps
            for _ in range(i):
                next(it, None)
        return zip(*iterators)
    
    text = "python"
    print(f"   Bigrams of '{text}': {list(sliding_window(text, 2))}")
    print(f"   Trigrams of '{text}': {list(sliding_window(text, 3))}")


# ============================================================================
# PART 4: FUNCTOOLS MODULE - Higher-order Functions
# ============================================================================

import functools
from functools import lru_cache, partial, reduce, wraps

def functools_demo():
    """
    The functools module provides tools for functional programming.
    
    Key Functions:
    - lru_cache: Memoization decorator (Least Recently Used cache)
    - partial: Partial function application (fix some arguments)
    - reduce: Apply function cumulatively to items
    - wraps: Decorator to preserve metadata
    """
    
    print("\n" + "="*60)
    print("FUNCTOOLS MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. lru_cache - Memoization decorator
    print("\n1. lru_cache (Memoization):")
    
    @lru_cache(maxsize=32)  # Cache up to 32 most recent calls
    def fibonacci(n):
        """Recursive Fibonacci with caching."""
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print("   Without cache (naive recursive): O(2^n)")
    print("   With @lru_cache: O(n)")
    
    import time
    start = time.time()
    result = fibonacci(30)
    elapsed = time.time() - start
    print(f"   fibonacci(30) = {result} (took {elapsed:.6f} seconds)")
    
    # Cache info
    print(f"   Cache info: {fibonacci.cache_info()}")
    
    # Clear cache
    fibonacci.cache_clear()
    print(f"   After clear: {fibonacci.cache_info()}")
    
    # 2. partial - Partial function application
    print("\n2. partial (Partial Application):")
    
    # Original function
    def power(base, exponent):
        return base ** exponent
    
    # Create specialized versions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"   square(5) = {square(5)}")
    print(f"   cube(3) = {cube(3)}")
    print(f"   power(2, 3) = {power(2, 3)}")
    
    # Another example: fixing arguments
    def greet(greeting, name):
        return f"{greeting}, {name}!"
    
    say_hello = partial(greet, "Hello")
    say_hi = partial(greet, "Hi")
    
    print(f"   say_hello('Alice'): {say_hello('Alice')}")
    print(f"   say_hi('Bob'): {say_hi('Bob')}")
    
    # 3. reduce - Functional reduction
    print("\n3. reduce (Functional Reduction):")
    
    # Sum of list
    numbers = [1, 2, 3, 4, 5]
    sum_result = reduce(lambda x, y: x + y, numbers)
    print(f"   reduce(lambda x,y: x+y, {numbers}) = {sum_result}")
    
    # Product of list
    product_result = reduce(lambda x, y: x * y, numbers)
    print(f"   reduce(lambda x,y: x*y, {numbers}) = {product_result}")
    
    # Maximum with initial value
    max_result = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"   max of {numbers} = {max_result}")
    
    # 4. wraps - Preserve metadata in decorators
    print("\n4. wraps (Preserve Metadata):")
    
    def simple_decorator(func):
        """Decorator without @wraps."""
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    def proper_decorator(func):
        """Decorator with @wraps."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    @simple_decorator
    def example1():
        """This is example1 function."""
        pass
    
    @proper_decorator
    def example2():
        """This is example2 function."""
        pass
    
    print("   Without @wraps:")
    print(f"     Name: {example1.__name__}")
    print(f"     Docstring: {example1.__doc__}")
    
    print("   With @wraps:")
    print(f"     Name: {example2.__name__}")
    print(f"     Docstring: {example2.__doc__}")
    
    # 5. total_ordering - Reduce boilerplate in rich comparison classes
    print("\n5. total_ordering (Rich Comparisons):")
    
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
            return f"Student({self.name}, {self.grade})"
    
    alice = Student("Alice", 85)
    bob = Student("Bob", 92)
    charlie = Student("Charlie", 85)
    
    print(f"   {alice} == {charlie}: {alice == charlie}")
    print(f"   {alice} != {bob}: {alice != bob}")
    print(f"   {alice} < {bob}: {alice < bob}")
    print(f"   {bob} >= {charlie}: {bob >= charlie}")


# ============================================================================
# PART 5: PATHLIB MODULE - Modern Path Handling
# ============================================================================

from pathlib import Path
import os
import tempfile

def pathlib_demo():
    """
    The pathlib module provides object-oriented filesystem paths.
    
    Key Features:
    - Object-oriented API (vs os.path string operations)
    - Platform-independent path handling
    - Easy path manipulation and joining
    - Convenient file operations
    """
    
    print("\n" + "="*60)
    print("PATHLIB MODULE DEMONSTRATION")
    print("="*60)
    
    # 1. Creating Path objects
    print("\n1. Creating Path Objects:")
    
    # Current directory
    current = Path.cwd()
    print(f"   Current directory: {current}")
    
    # Home directory
    home = Path.home()
    print(f"   Home directory: {home}")
    
    # Constructing paths
    path1 = Path('/usr/local/bin')
    path2 = Path('documents') / 'reports' / 'summary.pdf'
    path3 = Path.cwd() / 'data' / 'input.txt'
    
    print(f"   Absolute path: {path1}")
    print(f"   Relative path: {path2}")
    print(f"   Combined path: {path3}")
    
    # 2. Path properties and methods
    print("\n2. Path Properties and Methods:")
    
    # Using a temporary file for demonstration
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(b"Sample content")
    
    print(f"   Temporary file: {tmp_path}")
    print(f"   Parent: {tmp_path.parent}")
    print(f"   Name: {tmp_path.name}")
    print(f"   Stem: {tmp_path.stem}")
    print(f"   Suffix: {tmp_path.suffix}")
    print(f"   Is absolute: {tmp_path.is_absolute()}")
    print(f"   Exists: {tmp_path.exists()}")
    
    # 3. Path operations
    print("\n3. Path Operations:")
    
    # Joining paths
    base = Path('/base/path')
    full_path = base / 'subdir' / 'file.txt'
    print(f"   Joined path: {full_path}")
    
    # Resolving paths (absolute, with symlinks resolved)
    try:
        resolved = full_path.resolve()
        print(f"   Resolved: {resolved}")
    except Exception as e:
        print(f"   Could not resolve (expected): {type(e).__name__}")
    
    # Relative paths
    p1 = Path('/usr/local/bin')
    p2 = Path('/usr/local/share')
    relative = p2.relative_to(p1.parent.parent)
    print(f"   {p2} relative to {p1.parent.parent}: {relative}")
    
    # 4. File and directory operations
    print("\n4. File and Directory Operations:")
    
    # Create a temporary directory for demo
    temp_dir = Path(tempfile.mkdtemp())
    print(f"   Working in temp directory: {temp_dir}")
    
    # Create files and directories
    (temp_dir / 'subdir').mkdir(exist_ok=True)
    file_path = temp_dir / 'test.txt'
    file_path.write_text("Hello, World!")
    
    print(f"   Created: {file_path}")
    print(f"   File content: {file_path.read_text()}")
    
    # List directory contents
    print(f"\n   Directory listing:")
    for item in temp_dir.iterdir():
        indicator = "📁" if item.is_dir() else "📄"
        print(f"     {indicator} {item.name}")
    
    # Glob patterns
    print(f"\n   Using glob patterns:")
    
    # Create some test files
    (temp_dir / 'data1.json').write_text('{}')
    (temp_dir / 'data2.json').write_text('{}')
    (temp_dir / 'notes.md').write_text('# Notes')
    
    for json_file in temp_dir.glob('*.json'):
        print(f"     Found JSON: {json_file.name}")
    
    for all_files in temp_dir.rglob('*'):  # Recursive
        print(f"     Found: {all_files.relative_to(temp_dir)}")
    
    # 5. Comparison with os.path (legacy approach)
    print("\n5. pathlib vs os.path comparison:")
    
    # Legacy (os.path)
    import os
    legacy_path = os.path.join('/usr', 'local', 'bin')
    legacy_dir = os.path.dirname(legacy_path)
    legacy_base = os.path.basename(legacy_path)
    
    print(f"   os.path.join('/usr', 'local', 'bin'): {legacy_path}")
    print(f"   os.path.dirname(): {legacy_dir}")
    print(f"   os.path.basename(): {legacy_base}")
    
    # Modern (pathlib)
    modern_path = Path('/usr') / 'local' / 'bin'
    modern_dir = modern_path.parent
    modern_base = modern_path.name
    
    print(f"\n   Path('/usr') / 'local' / 'bin': {modern_path}")
    print(f"   .parent: {modern_dir}")
    print(f"   .name: {modern_base}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    os.unlink(tmp_path)


# ============================================================================
# PART 6: JSON, CSV, PICKLE - Data Serialization
# ============================================================================

import json
import csv
import pickle
import io

def serialization_demo():
    """
    Data serialization modules for different formats.
    
    JSON: Human-readable, web-friendly, limited to basic types
    CSV: Tabular data, spreadsheet compatible
    Pickle: Python-specific, can serialize almost anything
    """
    
    print("\n" + "="*60)
    print("DATA SERIALIZATION DEMONSTRATION")
    print("="*60)
    
    # Sample data
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "skills": ["Python", "JavaScript", "SQL"],
        "employed": True,
        "salary": 75000.50
    }
    
    sample_list = [
        {"name": "Alice", "age": 25, "department": "Engineering"},
        {"name": "Bob", "age": 32, "department": "Marketing"},
        {"name": "Charlie", "age": 28, "department": "Sales"}
    ]
    
    # 1. JSON - JavaScript Object Notation
    print("\n1. JSON Serialization:")
    
    # Convert Python object to JSON string
    json_string = json.dumps(sample_data, indent=2)
    print(f"   JSON string:\n{json_string}")
    
    # Convert JSON string back to Python object
    python_obj = json.loads(json_string)
    print(f"\n   Python object from JSON: {type(python_obj)}")
    print(f"   Name: {python_obj['name']}")
    
    # Read/write JSON files
    print(f"\n   Writing/reading JSON file:")
    
    with open('temp_data.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    with open('temp_data.json', 'r') as f:
        loaded_data = json.load(f)
    
    print(f"   Loaded name: {loaded_data['name']}")
    
    # Custom JSON encoding/decoding
    print(f"\n   Custom JSON encoder (datetime):")
    
    from datetime import datetime
    
    class CustomEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)
    
    complex_data = {"event": "meeting", "time": datetime.now()}
    custom_json = json.dumps(complex_data, cls=CustomEncoder)
    print(f"   Custom encoded: {custom_json}")
    
    # 2. CSV - Comma Separated Values
    print("\n2. CSV Serialization:")
    
    # Writing CSV
    print(f"   Writing CSV file:")
    
    with open('temp_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'age', 'department']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in sample_list:
            writer.writerow(row)
    
    # Reading CSV
    print(f"   Reading CSV file:")
    
    with open('temp_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, 1):
            print(f"     Row {i}: {row}")
    
    # CSV with different delimiters
    print(f"\n   CSV with custom delimiter (tab):")
    
    csv_data = "name\tage\tcity\nAlice\t25\tNYC\nBob\t30\tBoston"
    
    # Parse tab-separated data
    reader = csv.DictReader(io.StringIO(csv_data), delimiter='\t')
    for row in reader:
        print(f"     {row['name']} - {row['city']}")
    
    # 3. Pickle - Python object serialization
    print("\n3. Pickle Serialization:")
    
    # Complex Python object
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
            self.secret = "This is secret"
        
        def __repr__(self):
            return f"Person({self.name}, {self.age})"
        
        def greet(self):
            return f"Hello, I'm {self.name}"
    
    person = Person("Alice", 30)
    
    # Pickle to bytes
    print(f"   Pickling object: {person}")
    pickled_bytes = pickle.dumps(person)
    print(f"   Pickled size: {len(pickled_bytes)} bytes")
    
    # Unpickle
    unpickled_person = pickle.loads(pickled_bytes)
    print(f"   Unpickled: {unpickled_person}")
    print(f"   Method still works: {unpickled_person.greet()}")
    print(f"   Attributes preserved: {unpickled_person.secret}")
    
    # Pickle to file
    with open('temp_data.pkl', 'wb') as f:  # Note 'wb' for binary write
        pickle.dump(person, f)
    
    with open('temp_data.pkl', 'rb') as f:  # Note 'rb' for binary read
        loaded_person = pickle.load(f)
    
    print(f"\n   Loaded from file: {loaded_person}")
    
    # 4. Comparison and recommendations
    print("\n4. Format Comparison:")
    print("""
   JSON:
     ✓ Human readable
     ✓ Language independent
     ✓ Web standard
     ✗ Limited to basic types
     ✗ No comments
    
   CSV:
     ✓ Simple tabular data
     ✓ Spreadsheet compatible
     ✓ Human readable
     ✗ No complex structures
     ✗ No standard schema
    
   Pickle:
     ✓ Can serialize any Python object
     ✓ Preserves object types and methods
     ✗ Python-specific
     ✗ Security risk (unpickle untrusted data)
     ✗ Not human readable
    """)
    
    # Cleanup temporary files
    import os
    for f in ['temp_data.json', 'temp_data.csv', 'temp_data.pkl']:
        if os.path.exists(f):
            os.remove(f)


# ============================================================================
# PART 7: OS MODULE & SYSTEM OPERATIONS
# ============================================================================

import os
import sys
import platform
import shutil

def os_system_demo():
    """
    OS and System operations for file handling, environment, and system info.
    
    Key Areas:
    1. os module: Operating system interfaces
    2. Environment variables
    3. File I/O (text vs binary)
    4. System information
    """
    
    print("\n" + "="*60)
    print("OS & SYSTEM OPERATIONS DEMONSTRATION")
    print("="*60)
    
    # 1. OS Module - Core operations
    print("\n1. OS Module Operations:")
    
    # System information
    print(f"   Platform: {platform.system()} {platform.release()}")
    print(f"   Python version: {platform.python_version()}")
    print(f"   Current PID: {os.getpid()}")
    print(f"   CPU count: {os.cpu_count()}")
    
    # Working directory
    print(f"\n   Directory operations:")
    cwd = os.getcwd()
    print(f"   Current directory: {cwd}")
    
    # List directory contents
    print(f"   Contents of current directory (first 5):")
    for i, item in enumerate(os.listdir('.'), 1):
        if i > 5:
            print(f"     ... and {len(os.listdir('.')) - 5} more")
            break
        full_path = os.path.join('.', item)
        size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
        print(f"     {item} ({size} bytes)")
    
    # Create and remove directories
    print(f"\n   Directory creation/deletion:")
    
    # Create temporary directory for demo
    temp_dir = "temp_demo_dir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
        print(f"   Created directory: {temp_dir}")
    
    # Create a file inside
    temp_file = os.path.join(temp_dir, "test.txt")
    with open(temp_file, 'w') as f:
        f.write("Test content")
    
    print(f"   Created file: {temp_file}")
    print(f"   File exists: {os.path.exists(temp_file)}")
    print(f"   File size: {os.path.getsize(temp_file)} bytes")
    print(f"   Is file: {os.path.isfile(temp_file)}")
    print(f"   Is directory: {os.path.isdir(temp_file)}")
    
    # 2. Environment Variables
    print("\n2. Environment Variables:")
    
    # Get environment variables
    print(f"   Current user: {os.environ.get('USER') or os.environ.get('USERNAME')}")
    print(f"   Home directory: {os.environ.get('HOME') or os.environ.get('USERPROFILE')}")
    print(f"   PATH variable (first 3 entries):")
    
    path_var = os.environ.get('PATH', '')
    for i, path in enumerate(path_var.split(os.pathsep)[:3], 1):
        print(f"     {i}. {path}")
    
    # Set environment variable (temporary, for current process)
    os.environ['DEMO_VAR'] = 'demo_value'
    print(f"\n   Set DEMO_VAR: {os.environ.get('DEMO_VAR')}")
    
    # 3. File I/O - Text vs Binary
    print("\n3. File I/O - Text vs Binary:")
    
    # Text file operations
    print(f"   Text file operations:")
    
    text_content = """Hello, World!
This is a text file.
It contains multiple lines.
Special characters: Café 🍵"""
    
    # Write text file
    with open('text_demo.txt', 'w', encoding='utf-8') as f:
        f.write(text_content)
    
    # Read text file
    with open('text_demo.txt', 'r', encoding='utf-8') as f:
        read_text = f.read()
    
    print(f"   Written and read {len(read_text)} characters")
    print(f"   First line: {read_text.splitlines()[0]}")
    
    # Binary file operations
    print(f"\n   Binary file operations:")
    
    binary_data = bytes(range(256))  # 0-255 bytes
    
    # Write binary file
    with open('binary_demo.bin', 'wb') as f:
        f.write(binary_data)
    
    # Read binary file
    with open('binary_demo.bin', 'rb') as f:
        read_binary = f.read()
    
    print(f"   Written and read {len(read_binary)} bytes")
    print(f"   First 5 bytes: {list(read_binary[:5])}")
    print(f"   Last 5 bytes: {list(read_binary[-5:])}")
    
    # Binary vs Text mode demonstration
    print(f"\n   Text vs Binary mode difference:")
    
    test_string = "Line1\nLine2\r\nLine3"  # Mixed line endings
    
    # Write in text mode (platform-specific line endings)
    with open('text_mode.txt', 'w') as f:
        f.write(test_string)
    
    # Write in binary mode (exact bytes)
    with open('binary_mode.bin', 'wb') as f:
        f.write(test_string.encode('utf-8'))
    
    # Compare file sizes
    text_size = os.path.getsize('text_mode.txt')
    binary_size = os.path.getsize('binary_mode.bin')
    
    print(f"   Text mode file size: {text_size} bytes")
    print(f"   Binary mode file size: {binary_size} bytes")
    
    # 4. Advanced File Operations
    print("\n4. Advanced File Operations:")
    
    # File metadata
    print(f"   File metadata for 'text_demo.txt':")
    stats = os.stat('text_demo.txt')
    print(f"     Size: {stats.st_size} bytes")
    print(f"     Created: {datetime.fromtimestamp(stats.st_ctime)}")
    print(f"     Modified: {datetime.fromtimestamp(stats.st_mtime)}")
    print(f"     Accessed: {datetime.fromtimestamp(stats.st_atime)}")
    
    # File operations with shutil
    print(f"\n   Using shutil for file operations:")
    
    # Copy file
    shutil.copy('text_demo.txt', 'text_demo_copy.txt')
    print(f"   Copied to 'text_demo_copy.txt'")
    
    # Move/rename file
    if not os.path.exists('renamed_demo.txt'):
        shutil.move('text_demo_copy.txt', 'renamed_demo.txt')
        print(f"   Renamed to 'renamed_demo.txt'")
    
    # Walk directory tree
    print(f"\n   Directory tree walk (os.walk):")
    for root, dirs, files in os.walk('.', topdown=True):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files[:3]:  # Show first 3 files
            print(f"{subindent}{file}")
        if len(files) > 3:
            print(f"{subindent}... and {len(files) - 3} more")
        
        if level >= 1:  # Limit depth for demo
            dirs[:] = []  # Don't recurse deeper
    
    # 5. Cleanup
    print("\n5. Cleanup temporary files:")
    
    files_to_remove = [
        'text_demo.txt', 'binary_demo.bin',
        'text_mode.txt', 'binary_mode.bin',
        'renamed_demo.txt', temp_file
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"   Removed: {file}")
    
    # Remove temp directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"   Removed directory: {temp_dir}")


# ============================================================================
# MAIN DEMONSTRATION FUNCTION
# ============================================================================

def main():
    """
    Run all demonstrations.
    """
    print("PYTHON STANDARD LIBRARY & OS/SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Run all demos
    datetime_demo()
    collections_demo()
    itertools_demo()
    functools_demo()
    pathlib_demo()
    serialization_demo()
    os_system_demo()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
    Key Takeaways:
    
    1. DATETIME:
       - Use for all date/time operations
       - timezone-aware datetimes for applications
       - strftime/strptime for formatting/parsing
    
    2. COLLECTIONS:
       - defaultdict: When you need default values
       - Counter: Quick frequency counting
       - deque: Fast FIFO/LIFO operations
       - namedtuple: Simple data classes
    
    3. ITERTOOLS:
       - Efficient iteration and combination
       - chain, zip_longest for working with multiple iterables
       - product, permutations, combinations for combinatorics
    
    4. FUNCTOOLS:
       - @lru_cache: Optimize expensive function calls
       - partial: Create specialized functions
       - @wraps: Preserve metadata in decorators
    
    5. PATHLIB:
       - Modern replacement for os.path
       - Object-oriented path manipulation
       - Platform-independent paths
    
    6. SERIALIZATION:
       - JSON: Web APIs, configuration files
       - CSV: Tabular data, spreadsheets
       - Pickle: Python object persistence (trusted data only)
    
    7. OS & SYSTEM:
       - os module: System operations
       - Environment variables: Configuration
       - Text vs Binary files: Know when to use each
       - shutil: High-level file operations
    
    BEST PRACTICES:
    - Use pathlib over os.path for new code
    - Always specify encoding when opening text files
    - Use context managers (with statement) for file operations
    - Validate data when deserializing from untrusted sources
    - Use environment variables for configuration
    """)

if __name__ == "__main__":
    main()