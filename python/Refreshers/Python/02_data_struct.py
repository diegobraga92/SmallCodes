"""
COMPREHENSIVE PYTHON DATA STRUCTURES DEMONSTRATION
This script demonstrates Python data structures with detailed examples.
"""

print("=" * 70)
print("PYTHON DATA STRUCTURES AND STRING MANIPULATION")
print("=" * 70)

# ============================================================================
# SECTION 1: LISTS - Mutable Ordered Sequences
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 1: LISTS - Mutable Ordered Sequences")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING AND ACCESSING LISTS
# ----------------------------------------------------------------------------
print("1.1 Creating and Accessing Lists:")

# Creating lists
empty_list = []
numbers = [1, 2, 3, 4, 5]
mixed_list = [1, "hello", 3.14, True]
nested_list = [[1, 2], [3, 4], [5, 6]]

print(f"   Empty list: {empty_list}")
print(f"   Numbers list: {numbers}")
print(f"   Mixed list: {mixed_list}")
print(f"   Nested list: {nested_list}")

# Accessing elements
print(f"\n   Accessing by index:")
print(f"   numbers[0]: {numbers[0]}")     # First element
print(f"   numbers[-1]: {numbers[-1]}")   # Last element
print(f"   numbers[1:4]: {numbers[1:4]}") # Slicing (index 1 to 3)
print(f"   numbers[::2]: {numbers[::2]}") # Every other element

# ----------------------------------------------------------------------------
# LIST OPERATIONS
# ----------------------------------------------------------------------------
print("\n1.2 List Operations:")

# Modifying lists
fruits = ["apple", "banana", "cherry"]
print(f"   Original: {fruits}")

fruits.append("date")  # Add to end
print(f"   After append('date'): {fruits}")

fruits.insert(1, "blueberry")  # Insert at specific position
print(f"   After insert(1, 'blueberry'): {fruits}")

fruits[2] = "blackberry"  # Modify element
print(f"   After fruits[2] = 'blackberry': {fruits}")

# Removing elements
removed = fruits.pop()  # Remove last element
print(f"   After pop(): {fruits} (removed: '{removed}')")

removed = fruits.pop(1)  # Remove at specific index
print(f"   After pop(1): {fruits} (removed: '{removed}')")

fruits.remove("blackberry")  # Remove specific value
print(f"   After remove('blackberry'): {fruits}")

# List concatenation and repetition
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2
print(f"\n   Concatenation: {list1} + {list2} = {combined}")
print(f"   Repetition: {list1} * 3 = {list1 * 3}")

# ----------------------------------------------------------------------------
# LIST METHODS
# ----------------------------------------------------------------------------
print("\n1.3 List Methods:")

numbers = [5, 2, 8, 1, 9, 3, 2, 5]

print(f"   Original list: {numbers}")
print(f"   Length: {len(numbers)}")
print(f"   Count of 5: {numbers.count(5)}")
print(f"   Index of 8: {numbers.index(8)}")

numbers.sort()
print(f"   After sort(): {numbers}")

numbers.reverse()
print(f"   After reverse(): {numbers}")

numbers_copy = numbers.copy()
print(f"   Copy: {numbers_copy}")

numbers.clear()
print(f"   After clear(): {numbers}")

# ----------------------------------------------------------------------------
# WHEN TO USE LISTS
# ----------------------------------------------------------------------------
print("\n1.4 When to Use Lists:")
print("   - Need ordered collection of items")
print("   - Need to modify the collection (add, remove, change items)")
print("   - Need to access elements by position/index")
print("   - Need to preserve duplicate elements")
print("   - Example: Shopping cart items, to-do list, history log")

# ============================================================================
# SECTION 2: TUPLES - Immutable Ordered Sequences
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: TUPLES - Immutable Ordered Sequences")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING AND ACCESSING TUPLES
# ----------------------------------------------------------------------------
print("2.1 Creating and Accessing Tuples:")

# Creating tuples
empty_tuple = ()
single_tuple = (42,)  # Note the comma for single-element tuples
coordinates = (10.5, 20.3)
person = ("Alice", 30, "Engineer")
nested_tuple = ((1, 2), (3, 4))

print(f"   Empty tuple: {empty_tuple}")
print(f"   Single element tuple: {single_tuple}")
print(f"   Coordinates: {coordinates}")
print(f"   Person info: {person}")
print(f"   Nested tuple: {nested_tuple}")

# Tuple packing and unpacking
print("\n2.2 Tuple Packing and Unpacking:")

# Packing - creating a tuple without parentheses
packed = 1, 2, 3
print(f"   Packed tuple (without parentheses): {packed}")

# Unpacking - assigning tuple elements to variables
x, y, z = packed
print(f"   Unpacked: x={x}, y={y}, z={z}")

# Multiple assignment (tuple unpacking in disguise)
a, b = 10, 20
print(f"   Multiple assignment: a={a}, b={b}")

# Swapping values using tuple unpacking
a, b = b, a
print(f"   After swap: a={a}, b={b}")

# Extended unpacking (Python 3+)
values = (1, 2, 3, 4, 5)
first, *middle, last = values
print(f"\n   Extended unpacking: {values}")
print(f"   first={first}, middle={middle}, last={last}")

# ----------------------------------------------------------------------------
# TUPLE OPERATIONS
# ----------------------------------------------------------------------------
print("\n2.3 Tuple Operations:")

tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

print(f"   Concatenation: {tuple1} + {tuple2} = {tuple1 + tuple2}")
print(f"   Repetition: {tuple1} * 2 = {tuple1 * 2}")
print(f"   Membership: 2 in {tuple1} = {2 in tuple1}")
print(f"   Length of {tuple1}: {len(tuple1)}")

# Note: Tuples don't have methods like append(), remove(), sort()
# because they are immutable

# ----------------------------------------------------------------------------
# WHEN TO USE TUPLES
# ----------------------------------------------------------------------------
print("\n2.4 When to Use Tuples:")
print("   - Need immutable sequence (data shouldn't be changed)")
print("   - Using as dictionary keys (lists can't be used as keys)")
print("   - Multiple return values from functions")
print("   - Fixed collection of related items (coordinates, RGB colors)")
print("   - Performance - tuples are faster than lists for iteration")
print("   - Example: GPS coordinates, date (year, month, day), RGB values")

# ============================================================================
# SECTION 3: SETS - Unordered Unique Collections
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: SETS - Unordered Unique Collections")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING AND USING SETS
# ----------------------------------------------------------------------------
print("3.1 Creating and Using Sets:")

# Creating sets
empty_set = set()  # Note: {} creates an empty dictionary
numbers_set = {1, 2, 3, 4, 5}
duplicate_set = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4}
from_list = set([1, 2, 3, 2, 1])  # From list, duplicates removed
from_string = set("hello")  # From string, gets unique characters

print(f"   Empty set: {empty_set}")
print(f"   Numbers set: {numbers_set}")
print(f"   Set from list with duplicates: {from_list}")
print(f"   Set from string 'hello': {from_string}")

# Set operations
print("\n3.2 Set Operations:")

set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"   Set A: {set_a}")
print(f"   Set B: {set_b}")

# Basic set operations
print(f"   Union (A | B): {set_a | set_b}")
print(f"   Intersection (A & B): {set_a & set_b}")
print(f"   Difference (A - B): {set_a - set_b}")
print(f"   Symmetric Difference (A ^ B): {set_a ^ set_b}")

# Set comparisons
print(f"\n   Set comparisons:")
print(f"   Is subset (A <= B): {set_a <= set_b}")
print(f"   Is proper subset (A < B): {set_a < set_b}")
print(f"   Is superset (A >= B): {set_a >= set_b}")
print(f"   Disjoint (no common elements): {set_a.isdisjoint({6, 7, 8})}")

# ----------------------------------------------------------------------------
# SET METHODS
# ----------------------------------------------------------------------------
print("\n3.3 Set Methods:")

my_set = {1, 2, 3}

print(f"   Original set: {my_set}")
my_set.add(4)
print(f"   After add(4): {my_set}")
my_set.update([5, 6, 7])
print(f"   After update([5,6,7]): {my_set}")
my_set.remove(2)  # Raises KeyError if element doesn't exist
print(f"   After remove(2): {my_set}")
my_set.discard(10)  # Doesn't raise error if element doesn't exist
print(f"   After discard(10): {my_set}")
popped = my_set.pop()  # Removes and returns arbitrary element
print(f"   After pop(): {my_set} (popped: {popped})")
my_set.clear()
print(f"   After clear(): {my_set}")

# ----------------------------------------------------------------------------
# WHEN TO USE SETS
# ----------------------------------------------------------------------------
print("\n3.4 When to Use Sets:")
print("   - Need to remove duplicates from a collection")
print("   - Need fast membership testing (O(1) average case)")
print("   - Need mathematical set operations (union, intersection, etc.)")
print("   - Order doesn't matter")
print("   - Example: Unique tags, removing duplicates, finding common elements")

# ============================================================================
# SECTION 4: DICTIONARIES - Key-Value Mappings
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: DICTIONARIES - Key-Value Mappings")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING AND ACCESSING DICTIONARIES
# ----------------------------------------------------------------------------
print("4.1 Creating and Accessing Dictionaries:")

# Creating dictionaries
empty_dict = {}
person = {"name": "Alice", "age": 30, "city": "New York"}
using_dict = dict(name="Bob", age=25, city="London")
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])

print(f"   Empty dict: {empty_dict}")
print(f"   Person dict: {person}")
print(f"   Using dict(): {using_dict}")
print(f"   From pairs: {from_pairs}")

# Accessing values
print(f"\n   Accessing values:")
print(f"   person['name']: {person['name']}")
print(f"   person.get('age'): {person.get('age')}")
print(f"   person.get('country', 'USA'): {person.get('country', 'USA')}")  # Default value

# Checking for keys
print(f"\n   Checking for keys:")
print(f"   'name' in person: {'name' in person}")
print(f"   'country' in person: {'country' in person}")

# ----------------------------------------------------------------------------
# DICTIONARY OPERATIONS
# ----------------------------------------------------------------------------
print("\n4.2 Dictionary Operations:")

# Modifying dictionaries
print(f"   Original: {person}")

person["age"] = 31  # Update existing key
print(f"   After person['age'] = 31: {person}")

person["country"] = "USA"  # Add new key-value pair
print(f"   After adding country: {person}")

# Dictionary methods
print(f"\n   Dictionary methods:")
print(f"   Keys: {list(person.keys())}")
print(f"   Values: {list(person.values())}")
print(f"   Items: {list(person.items())}")

# Remove elements
removed_value = person.pop("city")
print(f"   After pop('city'): {person} (removed: '{removed_value}')")

last_item = person.popitem()  # Remove and return last inserted item
print(f"   After popitem(): {person} (removed: {last_item})")

person.clear()
print(f"   After clear(): {person}")

# ----------------------------------------------------------------------------
# DICTIONARY COMPREHENSIONS
# ----------------------------------------------------------------------------
print("\n4.3 Dictionary Comprehensions:")

# Create dictionary from two lists
keys = ["a", "b", "c", "d"]
values = [1, 2, 3, 4]

dict_from_lists = {k: v for k, v in zip(keys, values)}
print(f"   From lists: {dict_from_lists}")

# Create dictionary with conditional
squares = {x: x**2 for x in range(1, 6)}
print(f"   Squares: {squares}")

even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(f"   Even squares: {even_squares}")

# Transform existing dictionary
original = {"a": 1, "b": 2, "c": 3}
doubled = {k: v*2 for k, v in original.items()}
print(f"   Doubled values: {doubled}")

# ----------------------------------------------------------------------------
# WHEN TO USE DICTIONARIES
# ----------------------------------------------------------------------------
print("\n4.4 When to Use Dictionaries:")
print("   - Need to map keys to values")
print("   - Need fast lookup by key (O(1) average case)")
print("   - Data has natural key-value relationship")
print("   - Need flexible, dynamic structure")
print("   - Example: Phone book, configuration settings, JSON-like data")

# ============================================================================
# SECTION 5: COMPREHENSIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: COMPREHENSIONS")
print("=" * 60)

# ----------------------------------------------------------------------------
# LIST COMPREHENSIONS
# ----------------------------------------------------------------------------
print("5.1 List Comprehensions:")

# Basic list comprehension
squares = [x**2 for x in range(1, 6)]
print(f"   Squares: {squares}")

# With condition
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"   Even squares: {even_squares}")

# Multiple loops
pairs = [(x, y) for x in range(1, 4) for y in range(1, 4)]
print(f"   All pairs (x,y) for x,y in 1..3: {pairs}")

# Nested comprehensions
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"   Flattened matrix: {flattened}")

# With if-else (conditional expression)
numbers = [1, 2, 3, 4, 5, 6]
parity = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(f"   Parity: {parity}")

# ----------------------------------------------------------------------------
# DICTIONARY COMPREHENSIONS
# ----------------------------------------------------------------------------
print("\n5.2 Dictionary Comprehensions:")

# Basic dictionary comprehension
square_dict = {x: x**2 for x in range(1, 6)}
print(f"   Square dictionary: {square_dict}")

# From two lists
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
name_age_dict = {name: age for name, age in zip(names, ages)}
print(f"   Name-age dictionary: {name_age_dict}")

# With condition
even_square_dict = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(f"   Even square dictionary: {even_square_dict}")

# Swapping keys and values (if values are unique)
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"   Swapped dictionary: {swapped}")

# ----------------------------------------------------------------------------
# SET COMPREHENSIONS
# ----------------------------------------------------------------------------
print("\n5.3 Set Comprehensions:")

# Basic set comprehension
unique_squares = {x**2 for x in range(-5, 6)}
print(f"   Unique squares from -5 to 5: {unique_squares}")

# With condition
vowels_in_word = {char for char in "hello world" if char in "aeiou"}
print(f"   Vowels in 'hello world': {vowels_in_word}")

# From list with duplicates
numbers_with_duplicates = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_numbers = {x for x in numbers_with_duplicates}
print(f"   Unique numbers from list: {unique_numbers}")

# ----------------------------------------------------------------------------
# GENERATOR EXPRESSIONS
# ----------------------------------------------------------------------------
print("\n5.4 Generator Expressions (similar syntax):")

# Generator expression - memory efficient
squares_gen = (x**2 for x in range(1, 6))
print(f"   Generator expression: {squares_gen}")
print(f"   Converted to list: {list(squares_gen)}")

# Useful for large datasets
large_gen = (x * 2 for x in range(1000000))  # Doesn't create list in memory
print(f"   Large generator (first 5 values): {[next(large_gen) for _ in range(5)]}")

# ============================================================================
# SECTION 6: TIME COMPLEXITIES OF COMMON OPERATIONS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: TIME COMPLEXITIES (Big O Notation)")
print("=" * 60)

print("""
6.1 Time Complexities of Common Operations:

LIST OPERATIONS:
  Access/Update by index: O(1)
  Append to end: O(1) average, O(n) worst (when resizing)
  Insert/Delete at beginning: O(n) (all elements shift)
  Insert/Delete in middle: O(n)
  Search (in operator): O(n)
  Sort: O(n log n)
  Slice: O(k) where k is slice size

TUPLE OPERATIONS:
  Access by index: O(1)
  Search: O(n)
  Same as list except no modification operations

SET OPERATIONS:
  Add/Remove: O(1) average, O(n) worst
  Search (in operator): O(1) average, O(n) worst
  Union/Intersection/Difference: O(len(s) + len(t))

DICTIONARY OPERATIONS:
  Get/Set item by key: O(1) average, O(n) worst
  Delete item: O(1) average, O(n) worst
  Search for key (in operator): O(1) average, O(n) worst
  Iteration: O(n)

STRING OPERATIONS:
  Access by index: O(1)
  Concatenation: O(n + m) where n, m are string lengths
  Search (in operator): O(n)
  Slicing: O(k) where k is slice size

Note: 'Average' assumes good hash distribution
      'Worst' occurs with hash collisions
""")

print("\n6.2 Practical Implications:")

print("   For frequent search operations:")
print("     Use sets or dictionaries (O(1)) instead of lists (O(n))")

print("\n   For frequent insertions at beginning:")
print("     Consider collections.deque (O(1)) instead of list (O(n))")

print("\n   For large datasets:")
print("     Use generator expressions instead of list comprehensions")

print("\n   Example performance comparison:")
import time

# Demonstrate difference in search time
print("\n   Searching for element in large collections:")

# Create large collections
size = 100000
large_list = list(range(size))
large_set = set(range(size))

# Time list search (linear time)
start = time.time()
99999 in large_list
list_time = time.time() - start

# Time set search (constant time)
start = time.time()
99999 in large_set
set_time = time.time() - start

print(f"   List search time: {list_time:.6f} seconds")
print(f"   Set search time: {set_time:.6f} seconds")
print(f"   Set is {list_time/set_time:.0f}x faster for this search!")

# ============================================================================
# SECTION 7: STRING MANIPULATION METHODS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: STRING MANIPULATION METHODS")
print("=" * 60)

# ----------------------------------------------------------------------------
# CREATING AND ACCESSING STRINGS
# ----------------------------------------------------------------------------
print("7.1 Creating and Accessing Strings:")

# Strings are immutable sequences of characters
single_quotes = 'Hello'
double_quotes = "World"
triple_quotes = """This is a
multi-line
string"""
raw_string = r"C:\Users\Name"  # Raw string - backslashes are literal

print(f"   Single quotes: {single_quotes}")
print(f"   Double quotes: {double_quotes}")
print(f"   Triple quotes:\n{triple_quotes}")
print(f"   Raw string: {raw_string}")

# Accessing characters
text = "Python"
print(f"\n   Accessing characters in '{text}':")
print(f"   text[0]: '{text[0]}'")
print(f"   text[-1]: '{text[-1]}'")
print(f"   text[2:5]: '{text[2:5]}'")

# ----------------------------------------------------------------------------
# COMMON STRING METHODS
# ----------------------------------------------------------------------------
print("\n7.2 Common String Methods:")

# Case conversion
text = "  Hello World!  "
print(f"   Original: '{text}'")
print(f"   upper(): '{text.upper()}'")
print(f"   lower(): '{text.lower()}'")
print(f"   title(): '{text.title()}'")
print(f"   capitalize(): '{text.capitalize()}'")
print(f"   swapcase(): '{text.swapcase()}'")

# Stripping whitespace
print(f"\n   Stripping whitespace:")
print(f"   strip(): '{text.strip()}'")
print(f"   lstrip(): '{text.lstrip()}'")
print(f"   rstrip(): '{text.rstrip()}'")

# Searching and checking
text = "Hello World"
print(f"\n   Searching in '{text}':")
print(f"   startswith('Hello'): {text.startswith('Hello')}")
print(f"   endswith('World'): {text.endswith('World')}")
print(f"   find('World'): {text.find('World')}")  # Returns index or -1
print(f"   index('World'): {text.index('World')}")  # Returns index or raises error
print(f"   count('l'): {text.count('l')}")
print(f"   isalpha(): {text.isalpha()}")  # False because of space
print(f"   isdigit(): {text.isdigit()}")

# Splitting and joining
text = "apple,banana,cherry"
print(f"\n   Splitting and joining:")
print(f"   Original: '{text}'")
print(f"   split(','): {text.split(',')}")
print(f"   split(',', maxsplit=1): {text.split(',', 1)}")

words = ["Hello", "World", "Python"]
print(f"   List to join: {words}")
print(f"   ' '.join(words): {' '.join(words)}")
print(f"   '-'.join(words): {'-'.join(words)}")

# Replacement
text = "I like cats. Cats are nice."
print(f"\n   Replacement:")
print(f"   Original: '{text}'")
print(f"   replace('cats', 'dogs'): {text.replace('cats', 'dogs')}")
print(f"   replace('cats', 'dogs', 1): {text.replace('cats', 'dogs', 1)}")

# Formatting
print(f"\n   String Formatting:")
name = "Alice"
age = 30
print(f"   f-string: {name} is {age} years old")
#print(f"   format(): {} is {} years old".format(name, age))
print(f"   % formatting: %s is %d years old" % (name, age))

# ----------------------------------------------------------------------------
# STRING VALIDATION METHODS
# ----------------------------------------------------------------------------
print("\n7.3 String Validation Methods:")

test_cases = [
    ("12345", "isdigit()"),
    ("Hello", "isalpha()"),
    ("Hello123", "isalnum()"),
    ("   ", "isspace()"),
    ("Hello World", "istitle()"),
    ("HELLO", "isupper()"),
    ("hello", "islower()"),
    ("\t\n", "isprintable()"),
    ("Hello", "isascii()"),
]

for text, method in test_cases:
    result = getattr(text, method.replace("()", ""))()
    print(f"   '{text}'.{method}: {result}")

# ----------------------------------------------------------------------------
# ADVANCED STRING OPERATIONS
# ----------------------------------------------------------------------------
print("\n7.4 Advanced String Operations:")

# Partitioning
text = "apple:banana:cherry"
print(f"   partition(':'): {text.partition(':')}")
print(f"   rpartition(':'): {text.rpartition(':')}")

# Removing prefixes/suffixes (Python 3.9+)
text = "HelloWorld"
print(f"\n   Removing prefixes/suffixes:")
print(f"   Original: '{text}'")
print(f"   removeprefix('Hello'): '{text.removeprefix('Hello')}'")
print(f"   removesuffix('World'): '{text.removesuffix('World')}'")

# String translation
text = "Hello World!"
translation_table = str.maketrans("Helo", "HELO", "!")
translated = text.translate(translation_table)
print(f"\n   Translation:")
print(f"   Original: '{text}'")
print(f"   Translated: '{translated}'")

# Center, ljust, rjust
text = "Hello"
print(f"\n   Alignment:")
print(f"   center(10, '*'): '{text.center(10, '*')}'")
print(f"   ljust(10, '-'): '{text.ljust(10, '-')}'")
print(f"   rjust(10, '+'): '{text.rjust(10, '+')}'")
print(f"   zfill(10): '{'42'.zfill(10)}'")

# ============================================================================
# SECTION 8: PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 8: PRACTICAL EXAMPLES")
print("=" * 60)

# ----------------------------------------------------------------------------
# EXAMPLE 1: DATA ANALYSIS PIPELINE
# ----------------------------------------------------------------------------
print("8.1 Data Analysis Pipeline:")

# Simulate processing student data
student_records = [
    {"name": "Alice", "scores": [85, 92, 78], "age": 20},
    {"name": "Bob", "scores": [72, 65, 80], "age": 22},
    {"name": "Charlie", "scores": [90, 95, 88], "age": 21},
    {"name": "Diana", "scores": [60, 55, 50], "age": 20},
]

print("   Student Statistics:")

# Using list comprehension to extract data
all_scores = [score for student in student_records for score in student["scores"]]
print(f"   All scores: {all_scores}")
print(f"   Average score: {sum(all_scores) / len(all_scores):.1f}")

# Using dictionary comprehension for averages
student_averages = {
    student["name"]: sum(student["scores"]) / len(student["scores"])
    for student in student_records
}
print(f"\n   Student averages: {student_averages}")

# Using set for unique ages
unique_ages = {student["age"] for student in student_records}
print(f"   Unique ages: {unique_ages}")

# Finding top student using max with key function
top_student = max(student_records, key=lambda s: sum(s["scores"]) / len(s["scores"]))
print(f"   Top student: {top_student['name']} with average {sum(top_student['scores'])/len(top_student['scores']):.1f}")

# ----------------------------------------------------------------------------
# EXAMPLE 2: TEXT PROCESSING
# ----------------------------------------------------------------------------
print("\n8.2 Text Processing Example:")

text = """
Python is an interpreted, high-level, general-purpose programming language.
Created by Guido van Rossum and first released in 1991, Python's design 
philosophy emphasizes code readability with its notable use of significant 
whitespace. Its language constructs and object-oriented approach aim to help 
programmers write clear, logical code for small and large-scale projects.
"""

print("   Text Analysis:")
print(f"   Original text length: {len(text)} characters")

# Clean and process text
clean_text = text.lower()
words = clean_text.split()

print(f"   Number of words: {len(words)}")
print(f"   Number of unique words: {len(set(words))}")

# Word frequency using dictionary
word_count = {}
for word in words:
    # Remove punctuation
    word = word.strip(".,!?;:\"\'()")
    if word:
        word_count[word] = word_count.get(word, 0) + 1

print(f"\n   Most common words:")
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
for word, count in sorted_words[:5]:
    print(f"     '{word}': {count} times")

# ----------------------------------------------------------------------------
# EXAMPLE 3: SET OPERATIONS FOR DATA PROCESSING
# ----------------------------------------------------------------------------
print("\n8.3 Set Operations for Data Processing:")

# Simulate customer data
all_customers = {"Alice", "Bob", "Charlie", "Diana", "Eve"}
jan_customers = {"Alice", "Bob", "Charlie"}
feb_customers = {"Bob", "Charlie", "Diana"}
mar_customers = {"Charlie", "Diana", "Eve"}

print("   Customer Analysis:")

# Customers who shopped every month
loyal_customers = jan_customers & feb_customers & mar_customers
print(f"   Loyal customers (all 3 months): {loyal_customers}")

# Customers who shopped in January but not February
jan_only = jan_customers - feb_customers
print(f"   January only customers: {jan_only}")

# All unique customers
all_unique = jan_customers | feb_customers | mar_customers
print(f"   All unique customers: {all_unique}")

# Customers who shopped in exactly one month
jan_only = jan_customers - (feb_customers | mar_customers)
feb_only = feb_customers - (jan_customers | mar_customers)
mar_only = mar_customers - (jan_customers | feb_customers)
one_time_customers = jan_only | feb_only | mar_only
print(f"   One-time customers: {one_time_customers}")

# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY AND BEST PRACTICES")
print("=" * 60)

print("""
DATA STRUCTURE SELECTION GUIDE:

Use LISTS when:
  - You need ordered collection
  - You need to modify the collection frequently
  - You need to access elements by position
  - Duplicates are allowed and important
  - Example: Shopping cart, to-do list, log entries

Use TUPLES when:
  - Data should not be changed (immutable)
  - Using as dictionary keys
  - Returning multiple values from functions
  - Fixed collection of related items
  - Example: Coordinates, date components, RGB values

Use SETS when:
  - You need unique elements
  - Order doesn't matter
  - Need fast membership testing
  - Need set operations (union, intersection, etc.)
  - Example: Tags, removing duplicates, finding common elements

Use DICTIONARIES when:
  - You need key-value pairs
  - Need fast lookup by key
  - Data has natural key-value relationship
  - Need flexible structure
  - Example: Configuration, phone book, JSON data

STRING MANIPULATION TIPS:
  - Strings are immutable - operations return new strings
  - Use f-strings for most formatting (Python 3.6+)
  - Use join() for concatenating many strings (more efficient than +)
  - Be aware of encoding issues with non-ASCII text

PERFORMANCE CONSIDERATIONS:
  - Choose data structure based on your most common operations
  - Sets and dicts offer O(1) average lookups
  - Lists are O(1) for end operations, O(n) for beginning operations
  - Use comprehensions for cleaner, often faster code
  - Use generators for memory efficiency with large data
""")

print("\n" + "=" * 70)
print("END OF DATA STRUCTURES DEMONSTRATION")
print("=" * 70)