"""
COMPREHENSIVE PYTHON DATA STRUCTURES AND ALGORITHMS TUTORIAL
This script demonstrates built-in data structures, algorithms, and common patterns.
"""

# ============================================================================
# PART 1: BUILT-IN DATA STRUCTURES
# ============================================================================

"""
Python has four main built-in data structures:
1. Lists: Ordered, mutable, allows duplicates [ ]
2. Tuples: Ordered, immutable, allows duplicates ( )
3. Sets: Unordered, mutable, no duplicates { }
4. Dictionaries: Key-value pairs, unordered, mutable {key: value}
"""

def demonstrate_data_structures():
    """Demonstrate the four main data structures with examples."""
    
    print("=" * 60)
    print("BUILT-IN DATA STRUCTURES")
    print("=" * 60)
    
    # ============================================================================
    # 1. LISTS - Ordered, Mutable, Allows Duplicates
    # ============================================================================
    print("\n1. LISTS [ ]")
    print("-" * 40)
    print("Characteristics: Ordered, Mutable, Allows Duplicates, Indexed")
    
    # Creating lists
    fruits_list = ["apple", "banana", "cherry", "apple"]  # Allows duplicates
    numbers = [1, 2, 3, 4, 5]
    mixed = [1, "hello", 3.14, True]  # Can hold different types
    
    print(f"\nInitial lists:")
    print(f"fruits_list: {fruits_list}")
    print(f"numbers: {numbers}")
    print(f"mixed: {mixed}")
    
    # List operations
    fruits_list.append("orange")  # O(1) amortized
    fruits_list.insert(1, "blueberry")  # O(n) - shifts elements
    fruits_list.remove("banana")  # O(n) - searches then removes
    popped = fruits_list.pop()  # O(1) from end, O(n) from middle
    fruits_list[0] = "apricot"  # O(1) - direct index access
    
    print(f"\nAfter operations:")
    print(f"fruits_list: {fruits_list}")
    print(f"Popped element: {popped}")
    
    # List slicing (creates new list)
    first_two = fruits_list[:2]  # O(k) where k is slice size
    print(f"First two fruits: {first_two}")
    
    # List comprehension (Pythonic way to create lists)
    squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"\nList comprehensions:")
    print(f"squares: {squares}")
    print(f"even_squares: {even_squares}")
    
    # ============================================================================
    # 2. TUPLES - Ordered, Immutable, Allows Duplicates
    # ============================================================================
    print("\n\n2. TUPLES ( )")
    print("-" * 40)
    print("Characteristics: Ordered, Immutable, Allows Duplicates, Indexed")
    print("Use when: Data shouldn't change, need hashable collection")
    
    # Creating tuples
    coordinates = (10, 20)
    rgb = (255, 0, 128)
    single_element = (42,)  # Note comma for single element!
    not_a_tuple = (42)  # This is just an integer
    
    print(f"\nInitial tuples:")
    print(f"coordinates: {coordinates}")
    print(f"rgb: {rgb}")
    print(f"single_element: {single_element} (type: {type(single_element)})")
    print(f"not_a_tuple: {not_a_tuple} (type: {type(not_a_tuple)})")
    
    # Tuple operations (limited due to immutability)
    print(f"\nTuple operations:")
    print(f"coordinates[0]: {coordinates[0]}")  # O(1) access
    print(f"coordinates.count(10): {coordinates.count(10)}")  # O(n)
    print(f"coordinates.index(20): {coordinates.index(20)}")  # O(n)
    
    # Tuple unpacking
    x, y = coordinates  # Unpacking
    print(f"Unpacked: x={x}, y={y}")
    
    # Returning multiple values from functions (common tuple use)
    def get_stats(numbers):
        return min(numbers), max(numbers), sum(numbers)/len(numbers)
    
    min_val, max_val, avg_val = get_stats([1, 2, 3, 4, 5])
    print(f"\nMultiple return values: min={min_val}, max={max_val}, avg={avg_val:.2f}")
    
    # ============================================================================
    # 3. SETS - Unordered, Mutable, No Duplicates
    # ============================================================================
    print("\n\n3. SETS { } (or set())")
    print("-" * 40)
    print("Characteristics: Unordered, Mutable, No Duplicates, Not Indexed")
    print("Use when: Need uniqueness, membership testing, set operations")
    
    # Creating sets
    fruits_set = {"apple", "banana", "cherry"}
    empty_set = set()  # NOT {} - that creates dict!
    numbers_set = set([1, 2, 3, 2, 1])  # Removes duplicates
    print(f"\nInitial sets (notice duplicates removed):")
    print(f"fruits_set: {fruits_set}")
    print(f"numbers_set: {numbers_set}")
    
    # Set operations
    fruits_set.add("orange")  # O(1) average
    fruits_set.add("apple")  # No effect - already exists
    fruits_set.remove("banana")  # O(1) average, KeyError if not found
    fruits_set.discard("mango")  # O(1), no error if not found
    
    print(f"\nAfter operations:")
    print(f"fruits_set: {fruits_set}")
    
    # Set operations (mathematical)
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}
    
    print(f"\nSet A: {set_a}")
    print(f"Set B: {set_b}")
    print(f"Union (A | B): {set_a | set_b}")  # O(len(a) + len(b))
    print(f"Intersection (A & B): {set_a & set_b}")  # O(min(len(a), len(b)))
    print(f"Difference (A - B): {set_a - set_b}")  # O(len(a))
    print(f"Symmetric Difference (A ^ B): {set_a ^ set_b}")  # O(len(a) + len(b))
    
    # Membership testing is VERY fast in sets
    print(f"\nMembership testing (all O(1) average):")
    print(f"Is 3 in set_a? {3 in set_a}")
    print(f"Is 9 in set_a? {9 in set_a}")
    
    # ============================================================================
    # 4. DICTIONARIES - Key-Value Pairs, Unordered, Mutable
    # ============================================================================
    print("\n\n4. DICTIONARIES {key: value}")
    print("-" * 40)
    print("Characteristics: Key-Value pairs, Unordered (Python 3.7+: insertion order),")
    print("Mutable, Keys must be hashable (immutable), Values can be anything")
    
    # Creating dictionaries
    student = {
        "name": "Alice",
        "age": 22,
        "courses": ["Math", "Physics"],
        "graduated": False
    }
    
    empty_dict = {}
    dict_from_list = dict([("a", 1), ("b", 2), ("c", 3)])
    
    print(f"\nInitial dictionaries:")
    print(f"student: {student}")
    print(f"dict_from_list: {dict_from_list}")
    
    # Dictionary operations
    student["gpa"] = 3.8  # O(1) average - add/update
    age = student["age"]  # O(1) average - lookup
    student.get("phone", "Not provided")  # O(1) - safe get with default
    student.pop("graduated")  # O(1) average - remove key
    
    print(f"\nAfter operations:")
    print(f"student: {student}")
    print(f"Age: {age}")
    print(f"Phone: {student.get('phone', 'Not provided')}")
    
    # Dictionary iteration
    print("\nDictionary iteration:")
    for key, value in student.items():  # O(n) iteration
        print(f"  {key}: {value}")
    
    # Dictionary comprehension
    squares_dict = {x: x**2 for x in range(5)}
    print(f"\nDictionary comprehension: {squares_dict}")
    
    # ============================================================================
    # TIME COMPLEXITY SUMMARY (BIG-O NOTATION)
    # ============================================================================
    print("\n\n" + "=" * 60)
    print("TIME COMPLEXITY BASICS (BIG-O NOTATION)")
    print("=" * 60)
    print("""
    Big-O describes how runtime/memory grows with input size (n)
    
    Common Complexities:
    O(1)     - Constant time (best)
    O(log n) - Logarithmic (excellent)
    O(n)     - Linear (good)
    O(n log n) - Log-linear (decent)
    O(n²)    - Quadratic (poor)
    O(2ⁿ)    - Exponential (terrible)
    O(n!)    - Factorial (worst)
    """)
    
    print("\nDATA STRUCTURE OPERATION COMPLEXITIES:")
    print("-" * 40)
    
    complexities = {
        "Lists": {
            "Access by index (a[i])": "O(1)",
            "Append (a.append(x))": "O(1) amortized",
            "Insert (a.insert(i, x))": "O(n)",
            "Remove (a.remove(x))": "O(n)",
            "Search (x in a)": "O(n)",
            "Slice (a[i:j])": "O(k) where k=j-i",
        },
        "Tuples": {
            "Access by index": "O(1)",
            "Search (x in t)": "O(n)",
            "Count/Index": "O(n)",
        },
        "Sets": {
            "Add/Remove": "O(1) average",
            "Search (x in s)": "O(1) average",
            "Union/Intersection": "O(n+m)",
        },
        "Dictionaries": {
            "Get/Set item (d[key])": "O(1) average",
            "Delete (del d[key])": "O(1) average",
            "Search (key in d)": "O(1) average",
            "Iteration": "O(n)",
        }
    }
    
    for ds_name, ops in complexities.items():
        print(f"\n{ds_name}:")
        for op, complexity in ops.items():
            print(f"  {op:<25} {complexity}")
    
    # ============================================================================
    # WHEN TO USE EACH STRUCTURE
    # ============================================================================
    print("\n\n" + "=" * 60)
    print("WHEN TO USE EACH DATA STRUCTURE")
    print("=" * 60)
    
    guidelines = [
        ("Use LISTS when:", [
            "You need ordered collection",
            "You need to modify elements",
            "You allow duplicates",
            "You need indexed access",
            "Example: Shopping cart items, to-do list"
        ]),
        
        ("Use TUPLES when:", [
            "Data shouldn't change (immutable)",
            "You need hashable collection (for dict keys or set elements)",
            "Returning multiple values from function",
            "Example: Coordinates (x, y), RGB colors, database records"
        ]),
        
        ("Use SETS when:", [
            "You need uniqueness (no duplicates)",
            "Fast membership testing is crucial",
            "You need set operations (union, intersection, etc.)",
            "Order doesn't matter",
            "Example: Unique visitors, removing duplicates, tags"
        ]),
        
        ("Use DICTIONARIES when:", [
            "You need key-value mappings",
            "Fast lookups by key are important",
            "You need to associate data",
            "Example: User profiles, configurations, word frequency"
        ])
    ]
    
    for title, points in guidelines:
        print(f"\n{title}")
        for point in points:
            print(f"  • {point}")

# ============================================================================
# PART 2: ALGORITHMS (CONCEPTUAL)
# ============================================================================

def demonstrate_algorithms():
    """Demonstrate searching, sorting, and recursion algorithms."""
    
    print("\n" + "=" * 60)
    print("ALGORITHMS")
    print("=" * 60)
    
    # ============================================================================
    # 1. SEARCHING ALGORITHMS
    # ============================================================================
    print("\n1. SEARCHING ALGORITHMS")
    print("-" * 40)
    
    def linear_search(arr, target):
        """
        LINEAR SEARCH: O(n) time, O(1) space
        Checks each element sequentially.
        Works on any list (sorted or unsorted).
        """
        for i, value in enumerate(arr):
            if value == target:
                return i
        return -1
    
    def binary_search(arr, target):
        """
        BINARY SEARCH: O(log n) time, O(1) space
        Requires SORTED list.
        Repeatedly divides search interval in half.
        """
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    # Test searching algorithms
    unsorted_list = [42, 15, 7, 30, 22, 10]
    sorted_list = [7, 10, 15, 22, 30, 42]
    target = 22
    
    print(f"Unsorted list: {unsorted_list}")
    print(f"Sorted list:   {sorted_list}")
    print(f"Target: {target}")
    
    lin_result = linear_search(unsorted_list, target)
    bin_result = binary_search(sorted_list, target)
    
    print(f"\nLinear search (unsorted): Found at index {lin_result}")
    print(f"Binary search (sorted):   Found at index {bin_result}")
    
    print("\n" + "=" * 60)
    print("SEARCHING COMPARISON")
    print("=" * 60)
    print("""
    LINEAR SEARCH:
    • Time: O(n) - checks each element
    • Space: O(1) - no extra memory
    • Pros: Works on unsorted data, simple to implement
    • Cons: Slow for large lists
    
    BINARY SEARCH:
    • Time: O(log n) - halves search space each time
    • Space: O(1) for iterative, O(log n) for recursive
    • Pros: Extremely fast for large sorted lists
    • Cons: Requires sorted data, more complex
    """)
    
    # ============================================================================
    # 2. SORTING ALGORITHMS
    # ============================================================================
    print("\n\n2. SORTING ALGORITHMS")
    print("-" * 40)
    
    numbers_to_sort = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Original list: {numbers_to_sort}")
    
    # Python's built-in sorted() - returns new sorted list
    sorted_numbers = sorted(numbers_to_sort)  # O(n log n) average
    print(f"sorted(): {sorted_numbers} (new list)")
    print(f"Original unchanged: {numbers_to_sort}")
    
    # List's sort() method - sorts in place
    numbers_to_sort.sort()  # O(n log n) average
    print(f"list.sort(): {numbers_to_sort} (original modified)")
    
    # Sorting with custom keys
    words = ["banana", "apple", "cherry", "date"]
    words_sorted = sorted(words)  # Alphabetical
    words_by_length = sorted(words, key=len)  # By length
    words_desc = sorted(words, reverse=True)  # Reverse alphabetical
    
    print(f"\nSorting examples:")
    print(f"Alphabetical: {words_sorted}")
    print(f"By length:    {words_by_length}")
    print(f"Descending:   {words_desc}")
    
    # ============================================================================
    # 3. RECURSION
    # ============================================================================
    print("\n\n3. RECURSION")
    print("-" * 40)
    
    def factorial_iterative(n):
        """Iterative factorial: O(n) time, O(1) space"""
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
    def factorial_recursive(n):
        """
        Recursive factorial: O(n) time, O(n) space (call stack)
        Base case: factorial(0) = 1
        Recursive case: factorial(n) = n * factorial(n-1)
        """
        if n <= 1:  # Base case
            return 1
        return n * factorial_recursive(n - 1)  # Recursive case
    
    def fibonacci_recursive(n):
        """
        Fibonacci sequence (recursive): O(2ⁿ) time, O(n) space
        Warning: Extremely inefficient! Demonstrates exponential growth.
        """
        if n <= 1:
            return n
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
    
    def fibonacci_iterative(n):
        """
        Fibonacci sequence (iterative): O(n) time, O(1) space
        Much more efficient than recursive version.
        """
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    # Test recursion examples
    n = 5
    print(f"Factorial of {n}:")
    print(f"  Iterative: {factorial_iterative(n)}")
    print(f"  Recursive: {factorial_recursive(n)}")
    
    print(f"\nFibonacci({n}):")
    print(f"  Recursive: {fibonacci_recursive(n)} (inefficient)")
    print(f"  Iterative: {fibonacci_iterative(n)} (efficient)")
    
    # ============================================================================
    # RECURSION vs ITERATION TRADE-OFFS
    # ============================================================================
    print("\n" + "=" * 60)
    print("RECURSION vs ITERATION TRADE-OFFS")
    print("=" * 60)
    
    print("""
    RECURSION:
    • Pros:
      - More elegant/readable for certain problems (trees, divide-and-conquer)
      - Mathematical definition closely
      - Can be more intuitive for recursive data structures
    
    • Cons:
      - Overhead of function calls
      - Risk of stack overflow for deep recursion
      - Often less efficient than iteration
      - Can be harder to debug
    
    ITERATION:
    • Pros:
      - Generally faster (no function call overhead)
      - No risk of stack overflow
      - More memory efficient
      - Easier to understand for simple cases
    
    • Cons:
      - Can be less elegant for recursive problems
      - May require manual state management
      - Can be harder for certain algorithms (DFS, backtracking)
    
    WHEN TO USE RECURSION:
    • Problems with recursive structure (trees, graphs)
    • Divide and conquer algorithms
    • When readability is more important than performance
    • When recursion depth is limited (e.g., balanced trees)
    
    WHEN TO USE ITERATION:
    • Performance-critical code
    • Deep recursion would cause stack overflow
    • Simple linear processing
    • When you need to convert to/from generators
    """)

# ============================================================================
# PART 3: COMMON INTERVIEW PATTERNS
# ============================================================================

def demonstrate_interview_patterns():
    """Demonstrate common coding interview patterns."""
    
    print("\n" + "=" * 60)
    print("COMMON INTERVIEW PATTERNS")
    print("=" * 60)
    
    # ============================================================================
    # 1. COUNTING & FREQUENCY MAPS
    # ============================================================================
    print("\n1. COUNTING & FREQUENCY MAPS")
    print("-" * 40)
    print("Use dictionaries to count frequencies of elements.")
    
    def count_frequencies(items):
        """Count frequency of each item using dictionary."""
        freq = {}
        for item in items:
            freq[item] = freq.get(item, 0) + 1
        return freq
    
    def find_most_frequent(items):
        """Find most frequent item using frequency map."""
        freq = count_frequencies(items)
        return max(freq, key=freq.get)
    
    def group_anagrams(words):
        """Group anagrams using sorted word as key."""
        groups = {}
        for word in words:
            key = ''.join(sorted(word))  # Sort letters to create key
            groups.setdefault(key, []).append(word)
        return list(groups.values())
    
    # Examples
    numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    
    print(f"\nCounting frequencies of {numbers}:")
    print(f"Frequencies: {count_frequencies(numbers)}")
    print(f"Most frequent: {find_most_frequent(numbers)}")
    
    print(f"\nGrouping anagrams: {words}")
    anagram_groups = group_anagrams(words)
    for group in anagram_groups:
        print(f"  {group}")
    
    # ============================================================================
    # 2. TWO-POINTER TECHNIQUE
    # ============================================================================
    print("\n\n2. TWO-POINTER TECHNIQUE")
    print("-" * 40)
    print("Use two pointers to traverse array from different positions.")
    
    def two_sum_sorted(numbers, target):
        """
        Find two numbers that sum to target (sorted array).
        Time: O(n), Space: O(1)
        """
        left, right = 0, len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return (left, right)
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        
        return None
    
    def remove_duplicates_sorted(nums):
        """
        Remove duplicates in-place from sorted array.
        Returns new length.
        """
        if not nums:
            return 0
        
        write_index = 1
        for read_index in range(1, len(nums)):
            if nums[read_index] != nums[read_index - 1]:
                nums[write_index] = nums[read_index]
                write_index += 1
        
        return write_index
    
    # Examples
    sorted_nums = [2, 7, 11, 15]
    target = 9
    duplicates = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    
    print(f"\nTwo-sum in sorted array {sorted_nums}, target={target}:")
    result = two_sum_sorted(sorted_nums, target)
    print(f"Indices: {result}, Numbers: {sorted_nums[result[0]]}+{sorted_nums[result[1]]}")
    
    print(f"\nRemove duplicates from {duplicates}:")
    new_length = remove_duplicates_sorted(duplicates.copy())
    print(f"Array after: {duplicates[:new_length]}")
    print(f"New length: {new_length}")
    
    # ============================================================================
    # 3. SLIDING WINDOW BASICS
    # ============================================================================
    print("\n\n3. SLIDING WINDOW TECHNIQUE")
    print("-" * 40)
    print("Maintain a window that slides through the array.")
    
    def max_sum_subarray(nums, k):
        """
        Find maximum sum of any contiguous subarray of size k.
        Time: O(n), Space: O(1)
        """
        if len(nums) < k:
            return None
        
        # Calculate initial window sum
        window_sum = sum(nums[:k])
        max_sum = window_sum
        
        # Slide the window
        for i in range(k, len(nums)):
            window_sum = window_sum - nums[i - k] + nums[i]
            max_sum = max(max_sum, window_sum)
        
        return max_sum
    
    def longest_substring_without_repeats(s):
        """
        Find longest substring without repeating characters.
        Time: O(n), Space: O(min(n, alphabet_size))
        """
        char_index = {}  # Store last seen index of each character
        left = 0
        max_length = 0
        
        for right, char in enumerate(s):
            # If char seen before and within current window
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1  # Move left pointer
            
            char_index[char] = right  # Update last seen index
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    # Examples
    nums = [1, 4, 2, 10, 23, 3, 1, 0, 20]
    k = 4
    
    print(f"\nMaximum sum subarray of size {k} in {nums}:")
    print(f"Maximum sum: {max_sum_subarray(nums, k)}")
    
    test_strings = ["abcabcbb", "bbbbb", "pwwkew"]
    for s in test_strings:
        length = longest_substring_without_repeats(s)
        print(f"Longest unique substring in '{s}': {length}")
    
    # ============================================================================
    # 4. HASH-BASED LOOKUPS
    # ============================================================================
    print("\n\n4. HASH-BASED LOOKUPS")
    print("-" * 40)
    print("Use sets/dicts for O(1) lookups to optimize algorithms.")
    
    def find_pair_sum(nums, target):
        """
        Find if any pair sums to target using hash set.
        Time: O(n), Space: O(n)
        """
        seen = set()
        
        for num in nums:
            complement = target - num
            if complement in seen:
                return (complement, num)
            seen.add(num)
        
        return None
    
    def first_repeating_char(s):
        """
        Find first repeating character using hash set.
        """
        seen = set()
        for char in s:
            if char in seen:
                return char
            seen.add(char)
        return None
    
    def word_pattern(pattern, s):
        """
        Check if string follows pattern using two dictionaries.
        """
        words = s.split()
        if len(pattern) != len(words):
            return False
        
        char_to_word = {}
        word_to_char = {}
        
        for char, word in zip(pattern, words):
            if char in char_to_word:
                if char_to_word[char] != word:
                    return False
            else:
                char_to_word[char] = word
            
            if word in word_to_char:
                if word_to_char[word] != char:
                    return False
            else:
                word_to_char[word] = char
        
        return True
    
    # Examples
    nums = [10, 15, 3, 7]
    target = 17
    
    print(f"\nFind pair sum {target} in {nums}:")
    pair = find_pair_sum(nums, target)
    print(f"Pair: {pair}")
    
    strings = ["hello", "world", "python"]
    for s in strings:
        repeating = first_repeating_char(s)
        print(f"First repeating in '{s}': {repeating}")
    
    print("\nWord pattern matching:")
    pattern1, s1 = "abba", "dog cat cat dog"
    pattern2, s2 = "abba", "dog cat cat fish"
    
    print(f"'{s1}' matches '{pattern1}': {word_pattern(pattern1, s1)}")
    print(f"'{s2}' matches '{pattern2}': {word_pattern(pattern2, s2)}")
    
    # ============================================================================
    # PATTERN SUMMARY
    # ============================================================================
    print("\n" + "=" * 60)
    print("PATTERN SUMMARY")
    print("=" * 60)
    
    patterns = {
        "Frequency Maps": {
            "When to use": "Counting elements, finding duplicates/majority",
            "Data structure": "Dictionary",
            "Time complexity": "O(n)",
            "Example problems": "Anagram detection, character count"
        },
        "Two Pointers": {
            "When to use": "Sorted arrays, palindrome checks, pair sums",
            "Variants": "Opposite ends, fast-slow, sliding window",
            "Time complexity": "O(n)",
            "Example problems": "Two-sum (sorted), remove duplicates"
        },
        "Sliding Window": {
            "When to use": "Contiguous subarrays/substrings, fixed/variable size",
            "Key insight": "Reuse computation from previous window",
            "Time complexity": "O(n)",
            "Example problems": "Max sum subarray, longest unique substring"
        },
        "Hash Lookups": {
            "When to use": "Fast membership testing, complement finding",
            "Data structures": "Set, Dictionary",
            "Time complexity": "O(1) average for operations",
            "Example problems": "Pair sum, first duplicate, cache/memoization"
        }
    }
    
    for pattern_name, info in patterns.items():
        print(f"\n{pattern_name.upper()}:")
        for key, value in info.items():
            print(f"  {key}: {value}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Run all demonstrations in sequence.
    """
    
    # Part 1: Data Structures
    demonstrate_data_structures()
    
    # Part 2: Algorithms
    demonstrate_algorithms()
    
    # Part 3: Interview Patterns
    demonstrate_interview_patterns()
    
    print("\n" + "=" * 60)
    print("QUICK REFERENCE")
    print("=" * 60)
    
    print("""
    KEY TAKEAWAYS:
    
    1. DATA STRUCTURE SELECTION:
       • Lists: Ordered, modifiable sequences
       • Tuples: Immutable, hashable sequences  
       • Sets: Unique elements, fast membership
       • Dictionaries: Key-value mappings
    
    2. TIME COMPLEXITY RULES:
       • O(1): Best (constant)
       • O(log n): Excellent (logarithmic)
       • O(n): Good (linear)
       • O(n²): Poor (quadratic)
       • O(2ⁿ) or O(n!): Avoid (exponential/factorial)
    
    3. ALGORITHM CHOICES:
       • Search: Binary (sorted) vs Linear (unsorted)
       • Sort: Use built-in sorted() or list.sort() (O(n log n))
       • Recursion: Use for recursive problems, but watch depth
    
    4. INTERVIEW PATTERNS:
       • Frequency Maps: Count with dictionaries
       • Two Pointers: Process from both ends
       • Sliding Window: Maintain moving window
       • Hash Lookups: O(1) membership testing
    
    PRACTICE ADVICE:
    1. Understand time/space complexity trade-offs
    2. Choose data structure based on operations needed
    3. Recognize patterns in problems
    4. Always consider edge cases
    5. Practice explaining your thought process
    """)