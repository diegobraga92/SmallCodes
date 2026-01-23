"""
COMPREHENSIVE GUIDE TO PYTHON MEMORY MANAGEMENT

This script demonstrates and explains Python memory management concepts:
- Reference counting and garbage collection
- Mutable vs immutable objects
- Shallow vs deep copy
- Circular references and memory leaks
"""

import sys
import gc
import copy
import weakref
from typing import Any, List, Dict
import tracemalloc  # For memory allocation tracking
from pympler import asizeof  # For getting object sizes (install: pip install pympler)

# ============================================================================
# PART 1: REFERENCE COUNTING & GARBAGE COLLECTION
# ============================================================================

def reference_counting_demo():
    """
    REFERENCE COUNTING:
    -------------------
    Python's primary memory management mechanism.
    
    Each object has a reference count (number of references to it).
    When reference count reaches 0, object is immediately deallocated.
    
    GARBAGE COLLECTION:
    -------------------
    Python's secondary memory management for cyclic references.
    
    Generational GC (3 generations):
    - Generation 0: New objects
    - Generation 1: Objects that survived one collection
    - Generation 2: Long-lived objects
    
    GC runs automatically when thresholds are reached.
    """
    
    print("\n" + "="*60)
    print("REFERENCE COUNTING & GARBAGE COLLECTION")
    print("="*60)
    
    # 1. Basic Reference Counting
    print("\n1. BASIC REFERENCE COUNTING:")
    
    def show_ref_count(obj, name: str):
        """Helper to show reference count (sys.getrefcount returns +1 for the parameter)."""
        count = sys.getrefcount(obj) - 1  # Subtract the temporary reference
        print(f"   {name}: reference count = {count}")
        return count
    
    # Create an object
    my_list = [1, 2, 3]
    print(f"   Created list: {my_list}")
    rc1 = show_ref_count(my_list, "my_list")
    
    # Create another reference
    another_ref = my_list
    rc2 = show_ref_count(my_list, "my_list after another_ref")
    print(f"   Added reference: rc increased from {rc1} to {rc2}")
    
    # Delete a reference
    del another_ref
    rc3 = show_ref_count(my_list, "my_list after del another_ref")
    print(f"   Deleted reference: rc decreased from {rc2} to {rc3}")
    
    # References in containers
    container = [my_list, my_list]  # Two more references
    rc4 = show_ref_count(my_list, "my_list after adding to container")
    print(f"   Added to container: rc increased from {rc3} to {rc4}")
    
    # Clear container
    container.clear()
    rc5 = show_ref_count(my_list, "my_list after clearing container")
    print(f"   Cleared container: rc decreased from {rc4} to {rc5}")
    
    # Final cleanup
    del my_list
    print("   Deleted original reference: object can be freed")
    
    # 2. Garbage Collection Demonstration
    print("\n2. GARBAGE COLLECTION DEMONSTRATION:")
    
    # Enable GC debugging (optional)
    gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_SAVEALL)
    
    # Get current GC statistics
    print("   Current GC statistics:")
    print(f"   GC enabled: {gc.isenabled()}")
    print(f"   GC thresholds: {gc.get_threshold()}")
    print(f"   GC counts: {gc.get_count()}")
    
    # Manual GC control
    print("\n   Manual GC control example:")
    
    # Create some garbage
    for i in range(100):
        _ = [i] * 1000  # Create and discard lists
    
    print(f"   Created temporary objects")
    print(f"   GC count before collection: {gc.get_count()}")
    
    # Force garbage collection
    collected = gc.collect()
    print(f"   GC collected {collected} objects")
    print(f"   GC count after collection: {gc.get_count()}")
    
    # 3. Reference Cycles (GC's main job)
    print("\n3. REFERENCE CYCLES (Circular References):")
    
    class Node:
        """Simple class that can create reference cycles."""
        def __init__(self, name):
            self.name = name
            self.next = None
        
        def __repr__(self):
            return f"Node({self.name})"
    
    # Create a reference cycle
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    
    node1.next = node2
    node2.next = node3
    node3.next = node1  # Cycle created!
    
    print(f"   Created nodes: {node1} → {node2} → {node3} → {node1} (cycle)")
    
    # Show reference counts (will be 2 for each due to cycle)
    rc_node1 = sys.getrefcount(node1) - 1
    rc_node2 = sys.getrefcount(node2) - 1
    rc_node3 = sys.getrefcount(node3) - 1
    
    print(f"   Reference counts with cycle: node1={rc_node1}, node2={rc_node2}, node3={rc_node3}")
    
    # Delete external references
    del node1, node2, node3
    print("   Deleted external references (but cycle keeps objects alive)")
    
    # Force GC to collect cycles
    print("\n   Running GC to collect cycles...")
    unreachable = gc.collect()
    print(f"   GC collected {unreachable} unreachable objects in cycles")
    
    # Check what's in GC's unreachable list
    if gc.garbage:
        print(f"   Objects in gc.garbage: {len(gc.garbage)}")
        print("   Note: Objects with __del__ methods end up here")
    else:
        print("   No objects in gc.garbage (clean collection)")
    
    # 4. Weak References (avoid reference cycles)
    print("\n4. WEAK REFERENCES (Avoiding Cycles):")
    
    class Data:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Data({self.value})"
        
        def __del__(self):
            print(f"   Data({self.value}) is being destroyed")
    
    # Create object
    data = Data(42)
    print(f"   Created: {data}")
    
    # Create weak reference
    weak_ref = weakref.ref(data)
    print(f"   Created weak reference to data")
    
    # Access through weak reference
    retrieved = weak_ref()
    print(f"   Retrieved through weakref: {retrieved}")
    
    # Delete strong reference
    del data
    print("   Deleted strong reference")
    
    # Try to access through weak reference
    retrieved = weak_ref()
    if retrieved is None:
        print("   Weak reference is now None (object was garbage collected)")
    else:
        print(f"   Object still alive: {retrieved}")
    
    # 5. Generational GC in action
    print("\n5. GENERATIONAL GARBAGE COLLECTION:")
    
    # Reset GC debug
    gc.set_debug(0)
    
    def create_cycles(num_cycles):
        """Create many reference cycles."""
        cycles = []
        for i in range(num_cycles):
            a = []
            b = [a]
            a.append(b)  # Create cycle [a] ↔ [b]
            cycles.append((a, b))
        return cycles
    
    print("   Creating many reference cycles...")
    cycles = create_cycles(10000)
    print(f"   Created {len(cycles)} cycles")
    
    # Show generation counts
    print(f"\n   Generation counts before GC:")
    for gen in range(3):
        count = gc.get_count()[gen]
        print(f"   Generation {gen}: {count}")
    
    # Trigger GC at different levels
    print("\n   Triggering GC at different generations:")
    
    # Collect generation 0
    collected = gc.collect(0)
    print(f"   Collected generation 0: {collected} objects")
    
    # Collect generations 0 and 1
    collected = gc.collect(1)
    print(f"   Collected generation 0-1: {collected} objects")
    
    # Full collection
    collected = gc.collect(2)
    print(f"   Full collection (gen 0-2): {collected} objects")
    
    # Clean up
    del cycles
    gc.collect()
    
    print("\n" + "-"*40)
    print("REFERENCE COUNTING SUMMARY:")
    print("-"*40)
    print("""
    ADVANTAGES:
    ✓ Immediate cleanup (count = 0 → immediate deallocation)
    ✓ Predictable destruction timing
    ✓ Low overhead for non-cyclic references
    
    LIMITATIONS:
    ✗ Cannot handle circular references
    ✗ Reference count overhead (4-8 bytes per object)
    ✗ Atomic operations needed for thread safety
    
    GARBAGE COLLECTION ADVANTAGES:
    ✓ Handles circular references
    ✓ Reduces fragmentation
    ✓ Automatic and transparent
    
    BEST PRACTICES:
    1. Break cycles manually when possible
    2. Use weak references for caches/observers
    3. Avoid __del__ methods (can create gc.garbage)
    4. Manually trigger GC after large allocations
    """)

# ============================================================================
# PART 2: MUTABLE vs IMMUTABLE OBJECTS
# ============================================================================

def mutable_vs_immutable_demo():
    """
    MUTABLE vs IMMUTABLE OBJECTS:
    ----------------------------
    
    IMMUTABLE: Cannot be changed after creation
    - int, float, complex
    - str, bytes
    - tuple, frozenset
    - bool, NoneType
    
    MUTABLE: Can be changed after creation
    - list, dict, set
    - bytearray
    - Custom classes (by default)
    """
    
    print("\n" + "="*60)
    print("MUTABLE vs IMMUTABLE OBJECTS")
    print("="*60)
    
    # 1. Identity and Equality
    print("\n1. IDENTITY (id()) vs EQUALITY (==):")
    
    # Immutable objects with same value often share memory
    a = 10
    b = 10
    print(f"   a = 10, b = 10")
    print(f"   a == b: {a == b} (same value)")
    print(f"   a is b: {a is b} (same object in memory)")
    print(f"   id(a): {id(a)}, id(b): {id(b)}")
    
    # Large integers may not be interned
    c = 1000
    d = 1000
    print(f"\n   c = 1000, d = 1000")
    print(f"   c == d: {c == d}")
    print(f"   c is d: {c is d} (implementation dependent)")
    
    # Strings are often interned
    s1 = "hello"
    s2 = "hello"
    print(f"\n   s1 = 'hello', s2 = 'hello'")
    print(f"   s1 == s2: {s1 == s2}")
    print(f"   s1 is s2: {s1 is s2} (strings are interned)")
    
    # 2. Immutable Objects Demonstration
    print("\n2. IMMUTABLE OBJECTS:")
    
    # Tuples are immutable
    t = (1, 2, 3)
    print(f"   Tuple: {t}")
    print(f"   Try to modify: t[0] = 99 will raise TypeError")
    
    try:
        t[0] = 99
    except TypeError as e:
        print(f"   Error: {type(e).__name__}: {e}")
    
    # But tuple can contain mutable objects!
    mutable_tuple = ([1, 2], [3, 4])
    print(f"\n   Tuple with lists: {mutable_tuple}")
    print(f"   The tuple is immutable, but the lists inside are mutable")
    
    mutable_tuple[0].append(99)
    print(f"   Modified list inside tuple: {mutable_tuple}")
    print(f"   Tuple id before/after: same = {id(mutable_tuple) == id(mutable_tuple)}")
    
    # 3. Mutable Objects Demonstration
    print("\n3. MUTABLE OBJECTS:")
    
    # Lists are mutable
    lst = [1, 2, 3]
    lst_id_initial = id(lst)
    print(f"   List: {lst}")
    print(f"   Initial id: {lst_id_initial}")
    
    # Modify in-place
    lst.append(4)
    lst[0] = 99
    print(f"   After modification: {lst}")
    print(f"   Same id? {id(lst) == lst_id_initial} (Yes, modified in-place)")
    
    # Reassignment creates new object
    lst = [1, 2, 3]  # New list object
    print(f"\n   After reassignment: id = {id(lst)}")
    print(f"   Different from initial? {id(lst) != lst_id_initial}")
    
    # 4. Memory Implications
    print("\n4. MEMORY IMPLICATIONS:")
    
    # Create large immutable object
    import sys
    large_string = "x" * 1000
    print(f"   Large string (1000 chars):")
    print(f"   Size: {sys.getsizeof(large_string)} bytes")
    
    # Try to modify (creates new object)
    new_string = large_string + "!"
    print(f"   After concatenation (+ '!'):")
    print(f"   Original id unchanged: {id(large_string)}")
    print(f"   New string id: {id(new_string)}")
    print(f"   Different objects? {large_string is not new_string}")
    
    # Mutable list comparison
    print(f"\n   Large list modification:")
    large_list = ["x"] * 1000
    initial_size = sys.getsizeof(large_list)
    print(f"   Initial size: {initial_size} bytes")
    
    # Modify in-place
    large_list.append("y")
    after_size = sys.getsizeof(large_list)
    print(f"   After append: {after_size} bytes")
    print(f"   Same object? {id(large_list) == id(large_list)} (Yes)")
    
    # 5. Performance Comparison
    print("\n5. PERFORMANCE COMPARISON:")
    
    import time
    
    # String concatenation (immutable)
    print("   String concatenation (creates new objects):")
    start = time.time()
    s = ""
    for i in range(10000):
        s += str(i)
    str_time = time.time() - start
    print(f"   Time: {str_time:.4f} seconds")
    
    # List append + join (mutable)
    print("\n   List append + join (more efficient):")
    start = time.time()
    parts = []
    for i in range(10000):
        parts.append(str(i))
    result = "".join(parts)
    list_time = time.time() - start
    print(f"   Time: {list_time:.4f} seconds")
    
    print(f"\n   Speedup: {str_time/list_time:.2f}x faster with mutable list")
    
    # 6. Implications for Function Arguments
    print("\n6. FUNCTION ARGUMENT BEHAVIOR:")
    
    def modify_immutable(x: int):
        """Immutable argument - creates local copy."""
        print(f"   Inside function, before: x = {x}, id = {id(x)}")
        x += 1  # Creates new int object
        print(f"   Inside function, after:  x = {x}, id = {id(x)}")
        return x
    
    def modify_mutable(lst: list):
        """Mutable argument - modifies original."""
        print(f"   Inside function, before: lst = {lst}, id = {id(lst)}")
        lst.append(99)  # Modifies original list
        print(f"   Inside function, after:  lst = {lst}, id = {id(lst)}")
    
    # Test with immutable
    num = 10
    print(f"\n   Calling modify_immutable({num}):")
    print(f"   Before call: num = {num}, id = {id(num)}")
    result = modify_immutable(num)
    print(f"   After call:  num = {num}, id = {id(num)}")
    print(f"   Returned:    result = {result}, id = {id(result)}")
    print("   Original unchanged (immutable)")
    
    # Test with mutable
    my_list = [1, 2, 3]
    print(f"\n   Calling modify_mutable({my_list}):")
    print(f"   Before call: my_list = {my_list}, id = {id(my_list)}")
    modify_mutable(my_list)
    print(f"   After call:  my_list = {my_list}, id = {id(my_list)}")
    print("   Original modified (mutable)!")
    
    # 7. Practical Use Cases
    print("\n7. PRACTICAL USE CASES:")
    
    print("   When to use IMMUTABLE:")
    print("   - Dictionary keys (must be hashable)")
    print("   - Thread-safe data sharing")
    print("   - Functional programming patterns")
    print("   - Caching/memoization")
    
    print("\n   When to use MUTABLE:")
    print("   - Building collections incrementally")
    print("   - In-place modifications for performance")
    print("   - Stateful objects")
    print("   - Buffers and caches")
    
    print("\n" + "-"*40)
    print("MUTABLE vs IMMUTABLE SUMMARY:")
    print("-"*40)
    print("""
    KEY DIFFERENCES:
    
    IMMUTABLE:
    ✓ Can be used as dict keys (hashable)
    ✓ Thread-safe (no concurrent modification)
    ✓ Predictable behavior
    ✗ Modifications create new objects (memory overhead)
    ✗ Can't modify in-place
    
    MUTABLE:
    ✓ Can modify in-place (memory efficient)
    ✓ Better for incremental construction
    ✓ More flexible
    ✗ Cannot be dict keys (unhashable)
    ✗ Thread-unsafe
    ✗ Unexpected side effects in functions
    
    PERFORMANCE TIPS:
    1. Use tuples instead of lists for constants
    2. Use ''.join() instead of string concatenation in loops
    3. Use list comprehensions for creating new lists
    4. Be careful with default mutable arguments in functions
    """)

# ============================================================================
# PART 3: SHALLOW vs DEEP COPY
# ============================================================================

def copy_demo():
    """
    SHALLOW COPY vs DEEP COPY:
    -------------------------
    
    SHALLOW COPY:
    - Creates new container object
    - Copies references to nested objects
    - Nested objects are shared between original and copy
    
    DEEP COPY:
    - Creates new container object
    - Recursively copies all nested objects
    - Complete independence from original
    """
    
    print("\n" + "="*60)
    print("SHALLOW COPY vs DEEP COPY")
    print("="*60)
    
    # 1. Assignment (not a copy)
    print("\n1. ASSIGNMENT (Reference, not Copy):")
    
    original = [1, 2, [3, 4]]
    assigned = original  # Just another reference
    
    print(f"   original = {original}")
    print(f"   assigned = original (assignment)")
    print(f"   original is assigned: {original is assigned}")
    
    # Modify through either reference
    assigned[0] = 99
    print(f"\n   After assigned[0] = 99:")
    print(f"   original = {original}")
    print(f"   assigned = {assigned}")
    print("   Both changed (same object)")
    
    # 2. Shallow Copy Demonstration
    print("\n2. SHALLOW COPY:")
    
    original = [1, 2, [3, 4]]
    shallow_copy = copy.copy(original)  # or original.copy() for lists
    # shallow_copy = original[:]  # Also creates shallow copy for lists
    
    print(f"   original = {original}")
    print(f"   shallow_copy = copy.copy(original)")
    print(f"   original is shallow_copy: {original is shallow_copy}")
    print(f"   But nested list is same? {original[2] is shallow_copy[2]}")
    
    # Modify top level (independent)
    shallow_copy[0] = 99
    print(f"\n   After shallow_copy[0] = 99:")
    print(f"   original = {original}")
    print(f"   shallow_copy = {shallow_copy}")
    print("   Top level independent")
    
    # Modify nested level (shared!)
    shallow_copy[2][0] = 999
    print(f"\n   After shallow_copy[2][0] = 999:")
    print(f"   original = {original}")
    print(f"   shallow_copy = {shallow_copy}")
    print("   Nested objects still shared!")
    
    # 3. Deep Copy Demonstration
    print("\n3. DEEP COPY:")
    
    original = [1, 2, [3, 4]]
    deep_copy = copy.deepcopy(original)
    
    print(f"   original = {original}")
    print(f"   deep_copy = copy.deepcopy(original)")
    print(f"   original is deep_copy: {original is deep_copy}")
    print(f"   Nested list is same? {original[2] is deep_copy[2]}")
    
    # Modify at any level (completely independent)
    deep_copy[0] = 99
    deep_copy[2][0] = 999
    
    print(f"\n   After modifying both levels in deep_copy:")
    print(f"   original = {original}")
    print(f"   deep_copy = {deep_copy}")
    print("   Completely independent!")
    
    # 4. Complex Object Example
    print("\n4. COMPLEX OBJECT EXAMPLE:")
    
    class Employee:
        def __init__(self, name, skills):
            self.name = name
            self.skills = skills  # List of skills
        
        def __repr__(self):
            return f"Employee({self.name}, skills={self.skills})"
    
    # Create original employee
    alice = Employee("Alice", ["Python", "JavaScript", ["Django", "Flask"]])
    print(f"   Original: {alice}")
    
    # Shallow copy
    shallow_alice = copy.copy(alice)
    shallow_alice.name = "Alice_Shallow"
    shallow_alice.skills[0] = "Java"
    shallow_alice.skills[2][0] = "FastAPI"
    
    print(f"\n   After shallow copy modifications:")
    print(f"   Original: {alice}")
    print(f"   Shallow:  {shallow_alice}")
    print("   Nested list still shared!")
    
    # Deep copy
    bob = Employee("Bob", ["Python", "JavaScript", ["Django", "Flask"]])
    deep_bob = copy.deepcopy(bob)
    deep_bob.name = "Bob_Deep"
    deep_bob.skills[0] = "C++"
    deep_bob.skills[2][0] = "Pyramid"
    
    print(f"\n   After deep copy modifications:")
    print(f"   Original: {bob}")
    print(f"   Deep:     {deep_bob}")
    print("   Completely independent!")
    
    # 5. Performance Comparison
    print("\n5. PERFORMANCE COMPARISON:")
    
    import time
    
    # Create complex nested structure
    def create_nested_structure(depth, width):
        """Create deeply nested structure."""
        if depth == 0:
            return list(range(width))
        return [create_nested_structure(depth-1, width) for _ in range(width)]
    
    # Test structure
    test_data = create_nested_structure(4, 3)
    print(f"   Created nested structure depth=4, width=3")
    
    # Time shallow copy
    start = time.time()
    for _ in range(1000):
        copy.copy(test_data)
    shallow_time = time.time() - start
    
    # Time deep copy
    start = time.time()
    for _ in range(1000):
        copy.deepcopy(test_data)
    deep_time = time.time() - start
    
    print(f"   Shallow copy 1000x: {shallow_time:.4f} seconds")
    print(f"   Deep copy 1000x:    {deep_time:.4f} seconds")
    print(f"   Deep copy is {deep_time/shallow_time:.1f}x slower")
    
    # 6. When to Use Each
    print("\n6. WHEN TO USE EACH:")
    
    print("   Use SHALLOW COPY when:")
    print("   - Nested objects are immutable")
    print("   - You want to share nested objects")
    print("   - Performance is critical")
    print("   - Objects are flat (no nesting)")
    
    print("\n   Use DEEP COPY when:")
    print("   - Nested objects are mutable and should be independent")
    print("   - Working with recursive data structures")
    print("   - Need complete isolation")
    print("   - Passing data to untrusted code")
    
    # 7. Custom Copy Methods
    print("\n7. CUSTOM COPY METHODS:")
    
    class Config:
        """Class with custom copy behavior."""
        
        def __init__(self, settings, cache):
            self.settings = settings  # Dict, should be deep copied
            self.cache = cache        # Dict, should be shallow copied
            self.timestamp = time.time()  # Should be new for each copy
        
        def __copy__(self):
            """Shallow copy implementation."""
            print("   Custom __copy__ called")
            new_instance = self.__class__.__new__(self.__class__)
            new_instance.__dict__.update(self.__dict__)
            # But we want cache to be shared
            return new_instance
        
        def __deepcopy__(self, memo):
            """Deep copy implementation."""
            print("   Custom __deepcopy__ called")
            import copy
            new_instance = self.__class__.__new__(self.__class__)
            memo[id(self)] = new_instance
            
            # Deep copy settings
            new_instance.settings = copy.deepcopy(self.settings, memo)
            # Shallow copy cache (intentional)
            new_instance.cache = self.cache
            # New timestamp
            new_instance.timestamp = time.time()
            
            return new_instance
        
        def __repr__(self):
            return f"Config(settings={self.settings}, cache={self.cache}, timestamp={self.timestamp})"
    
    # Test custom copy
    config = Config({"theme": "dark", "language": "en"}, {"user": "admin"})
    print(f"   Original: {config}")
    
    config_shallow = copy.copy(config)
    print(f"   Shallow:  {config_shallow}")
    
    config_deep = copy.deepcopy(config)
    print(f"   Deep:     {config_deep}")
    
    print("\n" + "-"*40)
    print("COPY SUMMARY:")
    print("-"*40)
    print("""
    KEY CONCEPTS:
    
    ASSIGNMENT (=):
    - Creates new reference to same object
    - Modifications affect all references
    - Use when you want to share the object
    
    SHALLOW COPY:
    - Creates new container object
    - Copies references to contained objects
    - Contained objects are shared
    - Use copy.copy() or obj.copy()
    
    DEEP COPY:
    - Creates new container object
    - Recursively copies all contained objects
    - Complete independence
    - Use copy.deepcopy()
    
    PERFORMANCE:
    - Shallow copy: O(n) where n = container size
    - Deep copy: O(n × m) where m = nesting depth
    - Deep copy can be 10-100x slower for nested structures
    
    COMMON PITFALLS:
    1. Modifying shared nested objects accidentally
    2. Using copy when you need deepcopy
    3. Creating unnecessary copies (waste memory)
    4. Forgetting to copy when you need independence
    """)

# ============================================================================
# PART 4: CIRCULAR REFERENCES & MEMORY LEAKS
# ============================================================================

def circular_references_demo():
    """
    CIRCULAR REFERENCES:
    --------------------
    When objects reference each other, creating a cycle.
    
    PROBLEMS:
    - Reference counting cannot free them
    - Can cause memory leaks
    - GC must handle them (generational GC)
    
    SOLUTIONS:
    - Break cycles manually
    - Use weak references
    - Avoid __del__ methods
    """
    
    print("\n" + "="*60)
    print("CIRCULAR REFERENCES & MEMORY LEAKS")
    print("="*60)
    
    # Enable GC debugging for this demo
    gc.set_debug(gc.DEBUG_SAVEALL)
    
    # 1. Simple Circular Reference
    print("\n1. SIMPLE CIRCULAR REFERENCE:")
    
    def create_simple_cycle():
        """Create a simple reference cycle."""
        a = []
        b = [a]
        a.append(b)  # a contains b, b contains a
        return a, b
    
    print("   Creating list cycle: a = [], b = [a], a.append(b)")
    a, b = create_simple_cycle()
    
    print(f"   Reference counts:")
    print(f"   a: {sys.getrefcount(a) - 1}")
    print(f"   b: {sys.getrefcount(b) - 1}")
    
    # Delete external references
    del a, b
    print("   Deleted external references")
    
    # Force GC
    collected = gc.collect()
    print(f"   GC collected {collected} objects")
    print(f"   Objects in gc.garbage: {len(gc.garbage)}")
    
    # Clear garbage for next demo
    gc.garbage.clear()
    
    # 2. Complex Circular Reference
    print("\n2. COMPLEX CIRCULAR REFERENCE:")
    
    class TreeNode:
        """Tree node that can create cycles."""
        def __init__(self, name):
            self.name = name
            self.parent = None
            self.children = []
        
        def add_child(self, child):
            self.children.append(child)
            child.parent = self
        
        def __repr__(self):
            return f"TreeNode({self.name})"
        
        def __del__(self):
            print(f"   Deleting {self.name}")
    
    # Create tree with cycles
    root = TreeNode("root")
    child1 = TreeNode("child1")
    child2 = TreeNode("child2")
    
    root.add_child(child1)
    root.add_child(child2)
    
    # Create a cycle (child points back to parent through different path)
    child2.add_child(root)  # Cycle!
    
    print(f"   Created tree: root → child1, child2 → root (cycle)")
    print(f"   Reference counts:")
    print(f"   root: {sys.getrefcount(root) - 1}")
    print(f"   child1: {sys.getrefcount(child1) - 1}")
    print(f"   child2: {sys.getrefcount(child2) - 1}")
    
    # Delete references
    del root, child1, child2
    print("   Deleted all references")
    
    # GC with __del__ methods (problematic)
    print("\n   GC with __del__ methods (can cause issues):")
    collected = gc.collect()
    print(f"   GC collected {collected} objects")
    
    if gc.garbage:
        print(f"   Objects in gc.garbage (due to __del__): {len(gc.garbage)}")
        print("   These won't be collected automatically!")
        gc.garbage.clear()
    
    # 3. Weak References to Avoid Cycles
    print("\n3. WEAK REFERENCES (Breaking Cycles):")
    
    import weakref
    
    class WeakTreeNode:
        """Tree node using weak references to avoid cycles."""
        def __init__(self, name):
            self.name = name
            self._parent = None  # Will be weak reference
            self.children = []
        
        @property
        def parent(self):
            return self._parent() if self._parent else None
        
        @parent.setter
        def parent(self, value):
            self._parent = weakref.ref(value) if value else None
        
        def add_child(self, child):
            self.children.append(child)
            child.parent = self
        
        def __repr__(self):
            parent_name = self.parent.name if self.parent else "None"
            return f"WeakTreeNode({self.name}, parent={parent_name})"
    
    # Create tree without strong cycles
    root = WeakTreeNode("root")
    child1 = WeakTreeNode("child1")
    child2 = WeakTreeNode("child2")
    
    root.add_child(child1)
    root.add_child(child2)
    
    print(f"   Created weak reference tree:")
    print(f"   {root}")
    print(f"   {child1}")
    print(f"   {child2}")
    
    # Access parent through weak reference
    print(f"\n   child1.parent: {child1.parent}")
    print(f"   child2.parent: {child2.parent}")
    
    # Delete root
    del root
    print("\n   Deleted root (parent)")
    print(f"   child1.parent: {child1.parent}")
    print(f"   child2.parent: {child2.parent}")
    print("   Weak references become None automatically")
    
    # Clean up
    del child1, child2
    gc.collect()
    
    # 4. Memory Leak Detection
    print("\n4. MEMORY LEAK DETECTION:")
    
    # Start tracking memory allocations
    tracemalloc.start()
    
    def create_leak(iterations):
        """Function that leaks memory."""
        leaked = []
        
        for i in range(iterations):
            # Create data but keep reference in outer scope
            data = "x" * 1000
            leaked.append(data)  # Oops, never cleared!
            
            # Simulate some work
            _ = sum(range(1000))
        
        return f"Processed {iterations} items"
    
    def create_no_leak(iterations):
        """Function that doesn't leak memory."""
        for i in range(iterations):
            # Create and use data locally
            data = "x" * 1000
            
            # Simulate some work
            _ = sum(range(1000))
            
            # Data goes out of scope and can be garbage collected
        return f"Processed {iterations} items"
    
    print("   Testing with memory leak:")
    snapshot1 = tracemalloc.take_snapshot()
    result = create_leak(1000)
    snapshot2 = tracemalloc.take_snapshot()
    
    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print(f"   {result}")
    print(f"   Memory allocation changes:")
    for stat in top_stats[:3]:  # Top 3
        print(f"   {stat}")
    
    print("\n   Testing without memory leak:")
    snapshot1 = tracemalloc.take_snapshot()
    result = create_no_leak(1000)
    snapshot2 = tracemalloc.take_snapshot()
    
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print(f"   {result}")
    print(f"   Memory allocation changes (should be minimal):")
    for stat in top_stats[:3]:
        print(f"   {stat}")
    
    tracemalloc.stop()
    
    # 5. Common Memory Leak Patterns
    print("\n5. COMMON MEMORY LEAK PATTERNS:")
    
    print("   Pattern 1: Unbounded caches")
    
    class LeakyCache:
        """Cache that never removes items."""
        def __init__(self):
            self.cache = {}
        
        def get(self, key):
            return self.cache.get(key)
        
        def set(self, key, value):
            self.cache[key] = value  # Never removes old entries!
    
    print("   Solution: Use weakref.WeakValueDictionary or LRU cache")
    
    print("\n   Pattern 2: Event listeners not removed")
    
    class EventManager:
        """Manages event listeners."""
        def __init__(self):
            self.listeners = []
        
        def add_listener(self, listener):
            self.listeners.append(listener)
        
        # Missing: remove_listener method!
    
    print("   Solution: Always provide removal method or use weak references")
    
    print("\n   Pattern 3: Global or long-lived collections")
    
    global_data = []
    
    def process_data(data):
        """Accidentally stores data globally."""
        result = process(data)
        global_data.append(result)  # Oops!
        return result
    
    print("   Solution: Use local variables, clear collections periodically")
    
    # 6. Tools for Memory Analysis
    print("\n6. MEMORY ANALYSIS TOOLS:")
    
    print("   Built-in:")
    print("   - gc module: collect(), get_count(), get_objects()")
    print("   - sys.getsizeof(): Object size in bytes")
    print("   - tracemalloc: Allocation tracking")
    
    print("\n   Third-party:")
    print("   - objgraph: Visualize object references")
    print("   - memory_profiler: Line-by-line memory usage")
    print("   - pympler: Detailed object analysis")
    print("   - guppy3: Heap analysis")
    
    # 7. Best Practices to Avoid Leaks
    print("\n7. BEST PRACTICES TO AVOID MEMORY LEAKS:")
    
    print("   1. Use context managers (with statement)")
    print("      Automatically clean up resources")
    
    print("\n   2. Break circular references manually")
    print("      Set references to None when done")
    
    print("\n   3. Use weak references for caches/observers")
    print("      WeakValueDictionary, WeakKeyDictionary")
    
    print("\n   4. Avoid __del__ methods")
    print("      Can prevent GC from collecting cycles")
    
    print("\n   5. Clear large collections periodically")
    print("      Or use bounded collections")
    
    print("\n   6. Profile memory usage")
    print("      Use tracemalloc or memory_profiler")
    
    print("\n   7. Use generators for large datasets")
    print("      Process items one at a time")
    
    # Clean up for next demos
    gc.set_debug(0)
    gc.collect()
    
    print("\n" + "-"*40)
    print("CIRCULAR REFERENCES SUMMARY:")
    print("-"*40)
    print("""
    KEY POINTS:
    
    REFERENCE CYCLES:
    - Objects that reference each other
    - Reference counting cannot free them
    - GC handles them automatically (mostly)
    
    MEMORY LEAKS:
    - Unintended retention of objects
    - Often caused by cycles with __del__ methods
    - Can be caused by unclosed resources
    
    PREVENTION STRATEGIES:
    1. Use weak references for parent/child relationships
    2. Break cycles manually (set references to None)
    3. Avoid __del__ methods
    4. Use context managers
    
    DETECTION TOOLS:
    1. gc module: Track unreachable objects
    2. tracemalloc: Track allocations
    3. objgraph: Visualize object graphs
    4. memory_profiler: Profile memory usage
    
    PERFORMANCE IMPACT:
    - GC has overhead (pauses program execution)
    - Generational GC reduces this impact
    - Manual cycle breaking improves performance
    """)

# ============================================================================
# PART 5: PRACTICAL EXAMPLES & INTEGRATION
# ============================================================================

def practical_examples():
    """
    PRACTICAL EXAMPLES SHOWING REAL-WORLD MEMORY MANAGEMENT.
    """
    
    print("\n" + "="*60)
    print("PRACTICAL EXAMPLES & INTEGRATION")
    print("="*60)
    
    # 1. Efficient Data Processing
    print("\n1. EFFICIENT DATA PROCESSING:")
    
    # Bad: Creating many intermediate lists
    def process_data_inefficient(data):
        """Inefficient processing with many copies."""
        # Each operation creates new list
        filtered = [x for x in data if x % 2 == 0]
        doubled = [x * 2 for x in filtered]
        result = [str(x) for x in doubled]
        return result
    
    # Good: Generator pipeline
    def process_data_efficient(data):
        """Efficient processing with generators."""
        return (str(x * 2) for x in data if x % 2 == 0)
    
    # Test with large dataset
    data = list(range(100000))
    
    print("   Testing with 100,000 items:")
    
    import time
    
    # Inefficient version
    start = time.time()
    result1 = process_data_inefficient(data)
    time1 = time.time() - start
    print(f"   Inefficient: {time1:.4f} seconds, memory: lists created")
    
    # Efficient version
    start = time.time()
    result2 = list(process_data_efficient(data))  # Convert to list at end
    time2 = time.time() - start
    print(f"   Efficient:   {time2:.4f} seconds, memory: generators")
    
    print(f"   Speedup: {time1/time2:.1f}x, same results: {result1[:3] == result2[:3]}")
    
    # 2. Caching Strategies
    print("\n2. CACHING STRATEGIES (Memory vs Performance):")
    
    import functools
    
    # Simple cache (can cause memory leak if unbounded)
    cache = {}
    
    def expensive_calculation(x):
        """Expensive calculation with caching."""
        if x not in cache:
            # Simulate expensive calculation
            result = sum(i * i for i in range(x * 1000))
            cache[x] = result
        return cache[x]
    
    print("   Simple cache (risk: unbounded growth)")
    
    # Better: LRU Cache (bounded)
    @functools.lru_cache(maxsize=128)
    def expensive_calculation_lru(x):
        """Expensive calculation with LRU cache."""
        return sum(i * i for i in range(x * 1000))
    
    print("   LRU cache (safe: bounded to 128 entries)")
    
    # Test
    print("\n   Testing cache performance:")
    start = time.time()
    for i in range(100):
        expensive_calculation(i % 50)  # Repeats values
    time_simple = time.time() - start
    
    start = time.time()
    for i in range(100):
        expensive_calculation_lru(i % 50)
    time_lru = time.time() - start
    
    print(f"   Simple cache: {time_simple:.4f} seconds")
    print(f"   LRU cache:    {time_lru:.4f} seconds")
    print(f"   Cache size: simple={len(cache)}, LRU={expensive_calculation_lru.cache_info().currsize}")
    
    # 3. Memory-efficient Data Structures
    print("\n3. MEMORY-EFFICIENT DATA STRUCTURES:")
    
    import array
    import numpy as np
    
    # List vs Array vs numpy array
    print("   Comparing memory usage for 1,000,000 integers:")
    
    # Python list (lots of overhead)
    py_list = list(range(1000000))
    
    # Array (more compact)
    py_array = array.array('i', range(1000000))
    
    # NumPy array (most compact)
    np_array = np.arange(1000000, dtype=np.int32)
    
    print(f"   Python list:   {sys.getsizeof(py_list):,} bytes")
    print(f"   Python array:  {sys.getsizeof(py_array):,} bytes")
    print(f"   NumPy array:   {np_array.nbytes:,} bytes")
    print(f"   NumPy is {sys.getsizeof(py_list)/np_array.nbytes:.1f}x more memory efficient")
    
    # 4. Real-world Example: Graph Processing
    print("\n4. GRAPH PROCESSING EXAMPLE:")
    
    class GraphNode:
        """Graph node with potential memory issues."""
        def __init__(self, id):
            self.id = id
            self.neighbors = []  # List of strong references
        
        def add_neighbor(self, node):
            self.neighbors.append(node)
        
        def __repr__(self):
            return f"Node({self.id})"
    
    class GraphNodeWeak:
        """Graph node using weak references."""
        def __init__(self, id):
            self.id = id
            self.neighbors = []  # List of weak references
        
        def add_neighbor(self, node):
            self.neighbors.append(weakref.ref(node))
        
        def get_neighbors(self):
            """Get live neighbors."""
            neighbors = []
            for ref in self.neighbors:
                node = ref()
                if node is not None:
                    neighbors.append(node)
            return neighbors
        
        def __repr__(self):
            return f"NodeWeak({self.id})"
    
    # Create graph with strong references (creates cycles)
    print("   Creating graph with strong references:")
    nodes = [GraphNode(i) for i in range(5)]
    for i in range(4):
        nodes[i].add_neighbor(nodes[i + 1])
        nodes[i + 1].add_neighbor(nodes[i])  # Bidirectional = cycles!
    
    print("   Graph created with cycles")
    print("   Deleting references...")
    del nodes
    
    # Check if GC collected them
    collected = gc.collect()
    print(f"   GC collected {collected} objects")
    
    # Create graph with weak references
    print("\n   Creating graph with weak references:")
    nodes = [GraphNodeWeak(i) for i in range(5)]
    for i in range(4):
        nodes[i].add_neighbor(nodes[i + 1])
        nodes[i + 1].add_neighbor(nodes[i])
    
    print("   Graph created without strong cycles")
    print("   Deleting some nodes...")
    
    # Delete some nodes
    del nodes[2]
    gc.collect()
    
    print("   Node 2 can be collected (only weak references to it)")
    
    # 5. Memory Profiling Example
    print("\n5. MEMORY PROFILING EXAMPLE:")
    
    def memory_intensive_operation():
        """Function that uses lots of memory."""
        # Create large data structures
        big_list = [i for i in range(1000000)]  # ~8MB
        big_dict = {i: str(i) for i in range(100000)}  # ~5MB
        big_string = "x" * 1000000  # ~1MB
        
        # Process
        result = sum(big_list)
        
        # Return only small result
        return result
    
    print("   Function creates ~14MB of data but returns only an int")
    print("   Memory is freed when function returns (locals go out of scope)")
    
    # Demonstrate with tracemalloc
    tracemalloc.start()
    
    snapshot1 = tracemalloc.take_snapshot()
    result = memory_intensive_operation()
    snapshot2 = tracemalloc.take_snapshot()
    
    print(f"   Result: {result}")
    print("   Memory should return to baseline after function")
    
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    if top_stats:
        print(f"   Memory change: {top_stats[0].size_diff:,} bytes")
    
    tracemalloc.stop()
    
    print("\n" + "-"*40)
    print("PRACTICAL ADVICE:")
    print("-"*40)
    print("""
    PERFORMANCE VS MEMORY TRADEOFFS:
    
    1. IMMUTABLE vs MUTABLE:
       - Immutable: Safer, cacheable, but more allocations
       - Mutable: Faster modifications, but risk of side effects
    
    2. SHALLOW vs DEEP COPY:
       - Shallow: Fast, shares nested objects
       - Deep: Safe, independent, but slower
    
    3. GENERATORS vs LISTS:
       - Generators: Memory efficient, lazy evaluation
       - Lists: Faster access, reusable
    
    4. CACHING STRATEGIES:
       - No cache: Uses less memory, slower
       - LRU cache: Balanced memory/performance
       - Unlimited cache: Best performance, risk of leaks
    
    REAL-WORLD RECOMMENDATIONS:
    1. Profile before optimizing
    2. Use appropriate data structures
    3. Consider memory early in design
    4. Test with realistic data sizes
    5. Monitor memory in production
    """)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Run all memory management demonstrations."""
    
    print("PYTHON MEMORY MANAGEMENT COMPREHENSIVE GUIDE")
    print("="*60)
    
    # Run all demonstrations
    reference_counting_demo()
    mutable_vs_immutable_demo()
    copy_demo()
    circular_references_demo()
    practical_examples()
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    print("""
    KEY CONCEPTS RECAP:
    
    1. REFERENCE COUNTING:
       - Primary memory management in Python
       - Immediate deallocation when count reaches 0
       - Cannot handle circular references
    
    2. GARBAGE COLLECTION:
       - Handles circular references
       - Generational (0, 1, 2)
       - Automatic but can be manually triggered
    
    3. MUTABLE vs IMMUTABLE:
       - Mutable: Can change after creation (list, dict, set)
       - Immutable: Cannot change (int, str, tuple)
       - Implications for memory, performance, and thread safety
    
    4. COPYING:
       - Assignment: Creates reference (shares object)
       - Shallow copy: New container, shares nested objects
       - Deep copy: New container, new nested objects
    
    5. CIRCULAR REFERENCES:
       - Objects that reference each other
       - Can cause memory leaks
       - Use weak references to avoid
    
    MEMORY OPTIMIZATION STRATEGIES:
    
    1. CHOOSE DATA STRUCTURES WISELY:
       - Use tuples for constant sequences
       - Use arrays for large numeric datasets
       - Use sets for membership testing
    
    2. MANAGE OBJECT LIFECYCLES:
       - Use context managers for resources
       - Clear large collections when done
       - Break circular references manually
    
    3. MONITOR MEMORY USAGE:
       - Use sys.getsizeof() for object sizes
       - Use tracemalloc for allocation tracking
       - Use gc module for garbage collection stats
    
    4. AVOID COMMON PITFALLS:
       - Don't use mutable default arguments
       - Don't create unnecessary copies
       - Don't hold references longer than needed
       - Avoid __del__ methods in classes with cycles
    
    PERFORMANCE vs MEMORY TRADEOFFS:
    
    ┌─────────────────┬──────────────────────┬─────────────────────┐
    │ STRATEGY        │ MEMORY EFFICIENT     │ PERFORMANCE EFFICIENT │
    ├─────────────────┼──────────────────────┼─────────────────────┤
    │ Strings         │ String interning     │ String concatenation │
    │ Collections     │ Generators           │ Lists                │
    │ Copying         │ Shallow copy         │ Deep copy           │
    │ Caching         │ No cache             │ Unlimited cache     │
    │ References      │ Weak references      │ Strong references   │
    └─────────────────┴──────────────────────┴─────────────────────┘
    
    REMEMBER:
    - "Premature optimization is the root of all evil"
    - Profile before optimizing
    - Consider readability and maintainability
    - Test with realistic data sizes
    - Memory errors often show up in production, not development
    """)

if __name__ == "__main__":
    main()