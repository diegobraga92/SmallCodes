"""
PYTHON INTERVIEW-SPECIFIC KNOWLEDGE
=====================================
This comprehensive guide covers Python concepts often asked in interviews:
1. Difference between == and is
2. Mutable default arguments
3. Shallow vs deep copy
4. Late binding in closures
5. Python memory model (high level)
6. When not to optimize
"""

print("=" * 80)
print("PYTHON INTERVIEW-SPECIFIC KNOWLEDGE")
print("=" * 80)

import sys
import copy
import timeit
import tracemalloc
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
import weakref

# ============================================================================
# 1. DIFFERENCE BETWEEN == AND IS
# ============================================================================

print("\n" + "=" * 40)
print("1. DIFFERENCE BETWEEN == AND IS")
print("=" * 40)

"""
== (Equality Operator): Compares VALUES of objects
is (Identity Operator): Compares MEMORY ADDRESSES (whether they are the SAME object)
"""

class EqualityVsIdentity:
    """Demonstrates the difference between == and is operators"""
    
    @staticmethod
    def demonstrate_basic_difference():
        """Basic examples showing == vs is"""
        print("\nBasic Examples:")
        
        # Example 1: Same value, different objects
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        list3 = list1  # Reference to same object
        
        print(f"list1 = [1, 2, 3]")
        print(f"list2 = [1, 2, 3]")
        print(f"list3 = list1 (reference assignment)")
        
        print(f"\nlist1 == list2: {list1 == list2}  # Same VALUES")
        print(f"list1 is list2: {list1 is list2}  # Different OBJECTS")
        print(f"list1 is list3: {list1 is list3}  # Same OBJECT (reference)")
        
        # Example 2: Strings (interning)
        s1 = "hello"
        s2 = "hello"
        s3 = "".join(['h', 'e', 'l', 'l', 'o'])  # Dynamically created
        
        print(f"\nString interning example:")
        print(f"s1 = 'hello'")
        print(f"s2 = 'hello'")
        print(f"s3 = ''.join(['h', 'e', 'l', 'l', 'o'])")
        print(f"s1 == s2: {s1 == s2}  # Same value")
        print(f"s1 is s2: {s1 is s2}  # Python interns short strings (same object)")
        print(f"s1 == s3: {s1 == s3}  # Same value")
        print(f"s1 is s3: {s1 is s3}  # Different object (not interned)")
        
        # Example 3: Small integers caching (-5 to 256)
        a = 100
        b = 100
        c = 1000
        d = 1000
        
        print(f"\nSmall integer caching (-5 to 256):")
        print(f"a = 100, b = 100")
        print(f"c = 1000, d = 1000")
        print(f"a is b: {a is b}  # Small integer, cached")
        print(f"c is d: {c is d}  # Large integer, NOT cached (Python 3.8+)")
        
        # Example 4: None comparison (ALWAYS use 'is' for None)
        x = None
        y = None
        
        print(f"\nNone comparison (always use 'is'):")
        print(f"x = None, y = None")
        print(f"x == y: {x == y}")
        print(f"x is y: {x is y}  # Recommended way")
        print(f"x is None: {x is None}  # Best practice")
    
    @staticmethod
    def demonstrate_id_function():
        """Show memory addresses with id() function"""
        print("\n\nUsing id() to see memory addresses:")
        
        obj1 = [1, 2, 3]
        obj2 = [1, 2, 3]
        obj3 = obj1
        
        print(f"obj1 = [1, 2, 3]")
        print(f"obj2 = [1, 2, 3]")
        print(f"obj3 = obj1")
        
        print(f"\nid(obj1) = {id(obj1):#x}")
        print(f"id(obj2) = {id(obj2):#x}")
        print(f"id(obj3) = {id(obj3):#x}  # Same as obj1")
        
        print(f"\nobj1 is obj2: {obj1 is obj2}  # Different addresses")
        print(f"obj1 is obj3: {obj1 is obj3}  # Same address")
    
    @staticmethod
    def demonstrate_practical_use_cases():
        """Show when to use == vs is"""
        print("\n\nPractical Use Cases:")
        
        use_cases = [
            ("Checking for None", "if x is None:", "ALWAYS use 'is' for None"),
            ("Singleton objects", "if obj is True:", "True, False, None are singletons"),
            ("Object identity check", "if obj1 is obj2:", "Checking if same instance"),
            ("Value comparison", "if x == y:", "Comparing values/content"),
            ("String interning check", "if s1 is s2:", "Check if same interned string"),
            ("Small integer optimization", "if a is b:", "For -5 to 256 integers"),
        ]
        
        for use_case, code, explanation in use_cases:
            print(f"  {use_case:25} → {code:20} # {explanation}")
        
        print("\nCommon Interview Question:")
        print("  'Why should you use 'is' instead of '==' when checking for None?'")
        print("  Answer: 'is' is faster (memory address comparison vs value comparison)")
        print("          and more explicit about intent (checking identity, not value)")
    
    @staticmethod
    def demonstrate_custom_equality():
        """Show custom __eq__ implementation"""
        print("\n\nCustom Equality (__eq__ method):")
        
        @dataclass
        class Person:
            name: str
            age: int
            
            def __eq__(self, other):
                # Custom equality: same name and age
                if not isinstance(other, Person):
                    return False
                return self.name == other.name and self.age == other.age
        
        p1 = Person("Alice", 30)
        p2 = Person("Alice", 30)
        p3 = Person("Bob", 30)
        
        print(f"p1 = Person('Alice', 30)")
        print(f"p2 = Person('Alice', 30)")
        print(f"p3 = Person('Bob', 30)")
        
        print(f"\np1 == p2: {p1 == p2}  # Uses __eq__ method (value comparison)")
        print(f"p1 is p2: {p1 is p2}  # Different objects")
        print(f"p1 == p3: {p1 == p3}  # Different values")


# Run equality vs identity demonstration
eq_demo = EqualityVsIdentity()
eq_demo.demonstrate_basic_difference()
eq_demo.demonstrate_id_function()
eq_demo.demonstrate_practical_use_cases()
eq_demo.demonstrate_custom_equality()

# ============================================================================
# 2. MUTABLE DEFAULT ARGUMENTS
# ============================================================================

print("\n\n" + "=" * 40)
print("2. MUTABLE DEFAULT ARGUMENTS")
print("=" * 40)

"""
Python's DEFAULT ARGUMENT VALUES are evaluated ONLY ONCE when the function
is defined, not each time the function is called. This causes issues with
mutable default arguments (lists, dicts, sets, etc.).
"""

class MutableDefaultArguments:
    """Demonstrates the mutable default argument pitfall"""
    
    @staticmethod
    def demonstrate_the_problem():
        """Show the classic mutable default argument problem"""
        print("\nThe Problem: Mutable Default Arguments")
        
        print("\nBAD Example (mutable default):")
        bad_code = """
def append_to_list(value, my_list=[]):  # Default list created ONCE
    my_list.append(value)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2]  <- OOPS! Unexpected!
print(append_to_list(3))  # [1, 2, 3]  <- Gets longer each call!
        """.strip()
        
        print(bad_code)
        
        # Execute the example
        def append_to_list_bad(value, my_list=[]):
            my_list.append(value)
            return my_list
        
        result1 = append_to_list_bad(1)
        result2 = append_to_list_bad(2)
        result3 = append_to_list_bad(3)
        
        print(f"\nActual output:")
        print(f"First call:  {result1}")
        print(f"Second call: {result2}")
        print(f"Third call:  {result3}")
        
        print("\nWhy this happens:")
        print("  • Default argument 'my_list=[]' is evaluated ONCE at function definition")
        print("  • Same list object is used for ALL calls that don't provide 'my_list'")
        print("  • All modifications persist across function calls")
    
    @staticmethod
    def demonstrate_solution():
        """Show solutions to mutable default argument problem"""
        print("\n\nSolutions:")
        
        print("\n1. Use None as default, create new list inside function:")
        solution1_code = """
def append_to_list_good(value, my_list=None):
    if my_list is None:  # Check for None
        my_list = []     # Create new list
    my_list.append(value)
    return my_list

print(append_to_list_good(1))  # [1]
print(append_to_list_good(2))  # [2]  <- Correct!
print(append_to_list_good(3))  # [3]  <- Fresh list each time
        """.strip()
        
        print(solution1_code)
        
        # Execute the solution
        def append_to_list_good(value, my_list=None):
            if my_list is None:
                my_list = []
            my_list.append(value)
            return my_list
        
        result1 = append_to_list_good(1)
        result2 = append_to_list_good(2)
        result3 = append_to_list_good(3)
        
        print(f"\nOutput:")
        print(f"First call:  {result1}")
        print(f"Second call: {result2}")
        print(f"Third call:  {result3}")
        
        print("\n2. Use immutable default values (tuples, strings, numbers):")
        solution2_code = """
def process_data(data, default_config=()):  # Tuple is immutable
    config = list(default_config)  # Convert to mutable if needed
    config.extend(data)
    return config
        """.strip()
        print(solution2_code)
        
        print("\n3. Use functools.partial for complex defaults:")
        import functools
        solution3_code = """
from functools import partial

def _create_list_with_item(item):
    return [item]

# Create function with default list containing one item
append_with_default = partial(_create_list_with_item, 'default')
        """.strip()
        print(solution3_code)
    
    @staticmethod
    def demonstrate_more_examples():
        """Show more examples with different mutable types"""
        print("\n\nMore Examples with Different Mutable Types:")
        
        # Dictionary example
        print("\nDictionary Example:")
        def add_to_dict_bad(key, value, my_dict={}):
            my_dict[key] = value
            return my_dict
        
        print("BAD (shared dictionary):")
        print(f"First call:  {add_to_dict_bad('a', 1)}")
        print(f"Second call: {add_to_dict_bad('b', 2)}")
        print(f"Third call:  {add_to_dict_bad('c', 3)}")
        
        def add_to_dict_good(key, value, my_dict=None):
            if my_dict is None:
                my_dict = {}
            my_dict[key] = value
            return my_dict
        
        print("\nGOOD (fresh dictionary each time):")
        print(f"First call:  {add_to_dict_good('a', 1)}")
        print(f"Second call: {add_to_dict_good('b', 2)}")
        print(f"Third call:  {add_to_dict_good('c', 3)}")
        
        # Set example
        print("\nSet Example:")
        def add_to_set_bad(value, my_set=set()):
            my_set.add(value)
            return my_set
        
        result1 = add_to_set_bad(1)
        result2 = add_to_set_bad(2)
        print(f"BAD: First call: {result1}, Second call: {result2}")
        
        def add_to_set_good(value, my_set=None):
            if my_set is None:
                my_set = set()
            my_set.add(value)
            return my_set
        
        result1 = add_to_set_good(1)
        result2 = add_to_set_good(2)
        print(f"GOOD: First call: {result1}, Second call: {result2}")
    
    @staticmethod
    def demonstrate_when_its_okay():
        """Show when mutable defaults are acceptable"""
        print("\n\nWhen Mutable Defaults Are Acceptable:")
        
        acceptable_cases = [
            ("Caching/Memoization", "Shared cache across calls"),
            ("Accumulator pattern", "When you WANT persistence"),
            ("Singleton pattern", "When object should be shared"),
            ("Function as factory", "Creating related objects"),
        ]
        
        for case, explanation in acceptable_cases:
            print(f"  • {case}: {explanation}")
        
        print("\nExample: Caching with mutable default:")
        cache_example = """
def expensive_computation(x, cache={}):
    if x not in cache:
        print(f"Computing for {x}...")
        result = x * x  # Expensive operation
        cache[x] = result
    return cache[x]

print(expensive_computation(5))  # Computes
print(expensive_computation(5))  # Returns cached
print(expensive_computation(10)) # Computes new
print(expensive_computation(10)) # Returns cached
        """.strip()
        print(cache_example)


# Run mutable default arguments demonstration
mutable_demo = MutableDefaultArguments()
mutable_demo.demonstrate_the_problem()
mutable_demo.demonstrate_solution()
mutable_demo.demonstrate_more_examples()
mutable_demo.demonstrate_when_its_okay()

# ============================================================================
# 3. SHALLOW VS DEEP COPY
# ============================================================================

print("\n\n" + "=" * 40)
print("3. SHALLOW VS DEEP COPY")
print("=" * 40)

"""
Shallow Copy: Copies the object, but NOT the nested objects
Deep Copy: Copies the object AND all nested objects recursively
"""

class ShallowDeepCopy:
    """Demonstrates shallow vs deep copy"""
    
    @staticmethod
    def demonstrate_basic_difference():
        """Basic demonstration of shallow vs deep copy"""
        print("\nBasic Concept:")
        print("  • Shallow Copy: New container, SAME nested objects")
        print("  • Deep Copy: New container, NEW nested objects")
        
        # Create nested data structure
        original = {
            'name': 'Alice',
            'scores': [85, 92, 78],
            'info': {'age': 30, 'city': 'NYC'}
        }
        
        print(f"\nOriginal data: {original}")
        print(f"Original id: {id(original)}")
        print(f"Original['scores'] id: {id(original['scores'])}")
        
        # Shallow copy
        import copy
        shallow = copy.copy(original)
        deep = copy.deepcopy(original)
        
        print("\n" + "-" * 50)
        print("SHALLOW COPY (copy.copy()):")
        print("-" * 50)
        print(f"Shallow copy id: {id(shallow)}  # NEW dict object")
        print(f"Shallow['scores'] id: {id(shallow['scores'])}  # SAME list object")
        
        # Modify nested list in shallow copy
        shallow['scores'].append(95)
        print(f"\nAfter modifying shallow['scores'].append(95):")
        print(f"Original['scores']: {original['scores']}  # CHANGED! (unintended)")
        print(f"Shallow['scores']:  {shallow['scores']}")
        
        # Modify top-level in shallow copy
        shallow['name'] = 'Bob'
        print(f"\nAfter modifying shallow['name'] = 'Bob':")
        print(f"Original['name']: {original['name']}  # Unchanged (as expected)")
        print(f"Shallow['name']:  {shallow['name']}")
        
        print("\n" + "-" * 50)
        print("DEEP COPY (copy.deepcopy()):")
        print("-" * 50)
        print(f"Deep copy id: {id(deep)}  # NEW dict object")
        print(f"Deep['scores'] id: {id(deep['scores'])}  # NEW list object")
        
        # Modify nested list in deep copy
        deep['scores'].append(100)
        print(f"\nAfter modifying deep['scores'].append(100):")
        print(f"Original['scores']: {original['scores']}  # Unchanged (correct)")
        print(f"Deep['scores']:     {deep['scores']}")
    
    @staticmethod
    def demonstrate_different_copy_methods():
        """Show different ways to create copies"""
        print("\n\nDifferent Copy Methods in Python:")
        
        original_list = [[1, 2], [3, 4]]
        
        methods = [
            ("Slice copy", "list_copy = original[:]", "Shallow copy for lists"),
            ("list() constructor", "list_copy = list(original)", "Shallow copy for lists"),
            ("dict() constructor", "dict_copy = dict(original)", "Shallow copy for dicts"),
            ("set() constructor", "set_copy = set(original)", "Shallow copy for sets"),
            ("copy.copy()", "import copy; copy.copy(obj)", "Shallow copy (general)"),
            ("copy.deepcopy()", "import copy; copy.deepcopy(obj)", "Deep copy"),
            ("Object.copy()", "dict_copy = original.copy()", "Shallow copy (dict method)"),
        ]
        
        for method_name, code, description in methods:
            print(f"  • {method_name:20} → {code:45} # {description}")
        
        # Demonstrate each method
        print("\nDemonstrating copy methods:")
        original = [[1, 2], [3, 4]]
        
        # Slice copy (lists only)
        slice_copy = original[:]
        slice_copy[0].append(99)  # Modify nested list
        print(f"\nSlice copy: original[0] = {original[0]}  # CHANGED (shallow)")
        
        # Reset
        original = [[1, 2], [3, 4]]
        
        # Deep copy
        import copy
        deep_copy = copy.deepcopy(original)
        deep_copy[0].append(99)
        print(f"Deep copy: original[0] = {original[0]}  # UNCHANGED (deep)")
    
    @staticmethod
    def demonstrate_when_to_use_each():
        """Show when to use shallow vs deep copy"""
        print("\n\nWhen to Use Each:")
        
        scenarios = [
            ("Shallow Copy", [
                "Simple/flat data structures",
                "When you only need new container",
                "Performance-critical code (faster)",
                "When nested objects are immutable",
                "When you WANT to share nested objects"
            ]),
            ("Deep Copy", [
                "Complex nested data structures",
                "When you need complete independence",
                "Before passing data to untrusted code",
                "When modifying nested objects independently",
                "For thread-safe operations on nested data"
            ]),
            ("No Copy (Reference)", [
                "When you want to modify the original",
                "Large objects where copy is expensive",
                "When sharing data between components",
                "Read-only access is sufficient"
            ])
        ]
        
        for copy_type, situations in scenarios:
            print(f"\n{copy_type}:")
            for situation in situations:
                print(f"  • {situation}")
    
    @staticmethod
    def demonstrate_custom_copy_methods():
        """Show custom __copy__ and __deepcopy__ methods"""
        print("\n\nCustom Copy Methods (__copy__ and __deepcopy__):")
        
        class TreeNode:
            def __init__(self, value, children=None):
                self.value = value
                self.children = children if children is not None else []
            
            def __copy__(self):
                # Shallow copy: new node, same children references
                new_node = TreeNode(self.value)
                new_node.children = self.children[:]  # Shallow copy of list
                return new_node
            
            def __deepcopy__(self, memo):
                # Deep copy: new node, new children
                import copy
                new_node = TreeNode(copy.deepcopy(self.value, memo))
                # Add self to memo dict to handle cycles
                memo[id(self)] = new_node
                new_node.children = [copy.deepcopy(child, memo) 
                                   for child in self.children]
                return new_node
            
            def __repr__(self):
                return f"TreeNode({self.value}, {len(self.children)} children)"
        
        # Create tree
        root = TreeNode("root")
        child1 = TreeNode("child1")
        child2 = TreeNode("child2")
        root.children = [child1, child2]
        
        print(f"Original: {root}")
        print(f"Original children ids: {[id(c) for c in root.children]}")
        
        # Shallow copy
        shallow_root = copy.copy(root)
        print(f"\nShallow copy: {shallow_root}")
        print(f"Shallow children ids: {[id(c) for c in shallow_root.children]}")
        print(f"Same children? {root.children is shallow_root.children}")
        
        # Deep copy
        deep_root = copy.deepcopy(root)
        print(f"\nDeep copy: {deep_root}")
        print(f"Deep children ids: {[id(c) for c in deep_root.children]}")
        print(f"Same children? {root.children is deep_root.children}")


# Run shallow vs deep copy demonstration
copy_demo = ShallowDeepCopy()
copy_demo.demonstrate_basic_difference()
copy_demo.demonstrate_different_copy_methods()
copy_demo.demonstrate_when_to_use_each()
copy_demo.demonstrate_custom_copy_methods()

# ============================================================================
# 4. LATE BINDING IN CLOSURES
# ============================================================================

print("\n\n" + "=" * 40)
print("4. LATE BINDING IN CLOSURES")
print("=" * 40)

"""
Late Binding: In Python, closures capture VARIABLES (not values) from 
enclosing scope. The variable's value is looked up WHEN the inner function 
is CALLED, not when it's defined.
"""

class LateBindingClosures:
    """Demonstrates late binding in closures"""
    
    @staticmethod
    def demonstrate_the_problem():
        """Show the classic late binding problem"""
        print("\nThe Late Binding Problem:")
        
        print("\nBAD Example (common pitfall):")
        bad_code = """
def create_multipliers():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)
    return multipliers

for multiplier in create_multipliers():
    print(multiplier(2))  # What will this print?
        """.strip()
        
        print(bad_code)
        
        # Execute the example
        def create_multipliers_bad():
            multipliers = []
            for i in range(5):
                multipliers.append(lambda x: x * i)
            return multipliers
        
        print("\nActual output:")
        results = []
        for idx, multiplier in enumerate(create_multipliers_bad()):
            result = multiplier(2)
            results.append(result)
            print(f"  multiplier[{idx}](2) = {result}")
        
        print(f"\nAll results: {results}")
        print("ALL are 8! Because 'i' is 4 (last value) when functions are called")
        
        print("\nWhy this happens (Late Binding):")
        print("  • The lambda captures the VARIABLE 'i', not its VALUE")
        print("  • When lambda is called, it looks up current value of 'i'")
        print("  • At call time, loop has finished, so 'i' = 4")
    
    @staticmethod
    def demonstrate_solutions():
        """Show solutions to late binding problem"""
        print("\n\nSolutions to Late Binding:")
        
        print("\n1. Use default arguments (eager binding):")
        solution1_code = """
def create_multipliers_good():
    multipliers = []
    for i in range(5):
        # 'i' value captured in default argument
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

for multiplier in create_multipliers_good():
    print(multiplier(2))  # Correct: 0, 2, 4, 6, 8
        """.strip()
        
        print(solution1_code)
        
        def create_multipliers_good():
            multipliers = []
            for i in range(5):
                multipliers.append(lambda x, i=i: x * i)
            return multipliers
        
        print("\nOutput:")
        for idx, multiplier in enumerate(create_multipliers_good()):
            print(f"  multiplier[{idx}](2) = {multiplier(2)}")
        
        print("\n2. Use functools.partial:")
        import functools
        solution2_code = """
from functools import partial

def create_multipliers_partial():
    multipliers = []
    for i in range(5):
        def multiply(x, factor):
            return x * factor
        multipliers.append(partial(multiply, factor=i))
    return multipliers
        """.strip()
        print(solution2_code)
        
        print("\n3. Use a factory function:")
        solution3_code = """
def create_multiplier(factor):
    # 'factor' is captured when factory is called
    return lambda x: x * factor

def create_multipliers_factory():
    multipliers = []
    for i in range(5):
        multipliers.append(create_multiplier(i))
    return multipliers
        """.strip()
        print(solution3_code)
        
        print("\n4. Use a list comprehension with immediate execution:")
        solution4_code = """
multipliers = [(lambda factor: lambda x: x * factor)(i) for i in range(5)]
        """.strip()
        print(solution4_code)
    
    @staticmethod
    def demonstrate_more_examples():
        """Show more late binding examples"""
        print("\n\nMore Late Binding Examples:")
        
        # Example 1: Event handlers
        print("\nExample 1: Event handlers in loop")
        def create_event_handlers_bad():
            handlers = []
            for event_type in ['click', 'hover', 'keypress']:
                handlers.append(lambda: print(f"Handling {event_type}"))
            return handlers
        
        print("BAD (all print 'keypress'):")
        for handler in create_event_handlers_bad():
            handler()  # All print 'keypress'
        
        def create_event_handlers_good():
            handlers = []
            for event_type in ['click', 'hover', 'keypress']:
                handlers.append(lambda et=event_type: print(f"Handling {et}"))
            return handlers
        
        print("\nGOOD (correct event types):")
        for handler in create_event_handlers_good():
            handler()
        
        # Example 2: Callback with index
        print("\nExample 2: Callbacks with indices")
        callbacks = []
        for i in range(3):
            callbacks.append(lambda: print(f"Callback {i}"))
        
        print("Calling callbacks:")
        for callback in callbacks:
            callback()  # All print 'Callback 2'
        
        # Fix with default argument
        callbacks_fixed = []
        for i in range(3):
            callbacks_fixed.append(lambda idx=i: print(f"Callback {idx}"))
        
        print("\nFixed callbacks:")
        for callback in callbacks_fixed:
            callback()
    
    @staticmethod
    def demonstrate_when_late_binding_is_useful():
        """Show when late binding is actually desirable"""
        print("\n\nWhen Late Binding is Useful:")
        
        useful_cases = [
            ("Dynamic configuration", "Function uses current config value"),
            ("Mutable state", "Function responds to changing state"),
            ("Callbacks to changing objects", "Always reference latest object"),
            ("Lazy evaluation", "Value computed when needed, not when defined"),
        ]
        
        for case, explanation in useful_cases:
            print(f"  • {case}: {explanation}")
        
        print("\nExample: Counter with late binding")
        counter_example = """
def create_counter():
    count = 0
    
    def increment():
        nonlocal count  # Late binding to mutable count
        count += 1
        return count
    
    return increment

counter = create_counter()
print(counter())  # 1
print(counter())  # 2  # Late binding allows this to work!
        """.strip()
        print(counter_example)


# Run late binding demonstration
late_binding_demo = LateBindingClosures()
late_binding_demo.demonstrate_the_problem()
late_binding_demo.demonstrate_solutions()
late_binding_demo.demonstrate_more_examples()
late_binding_demo.demonstrate_when_late_binding_is_useful()

# ============================================================================
# 5. PYTHON MEMORY MODEL (HIGH LEVEL)
# ============================================================================

print("\n\n" + "=" * 40)
print("5. PYTHON MEMORY MODEL (HIGH LEVEL)")
print("=" * 40)

"""
Python Memory Model:
• Reference counting for garbage collection
• Generational garbage collector for cycle detection
• Memory is managed automatically
• Objects have identity, type, and value
"""

class PythonMemoryModel:
    """Demonstrates Python's memory management"""
    
    @staticmethod
    def demonstrate_reference_counting():
        """Show reference counting basics"""
        print("\nReference Counting:")
        
        import sys
        
        # Create object
        a = [1, 2, 3]
        print(f"a = [1, 2, 3]")
        print(f"Reference count of a: {sys.getrefcount(a)}")
        
        # Create another reference
        b = a
        print(f"\nb = a  # Create another reference")
        print(f"Reference count of a: {sys.getrefcount(a)}")
        
        # Create more references
        c = a
        d = a
        print(f"\nc = a, d = a  # More references")
        print(f"Reference count of a: {sys.getrefcount(a)}")
        
        # Delete references
        del b, c, d
        print(f"\ndel b, c, d  # Delete references")
        print(f"Reference count of a: {sys.getrefcount(a)}")
        
        print("\nNote: sys.getrefcount() adds one reference itself!")
        print("Actual count = getrefcount() - 1")
    
    @staticmethod
    def demonstrate_garbage_collection():
        """Show garbage collection concepts"""
        print("\n\nGarbage Collection:")
        
        import gc
        
        # Enable GC debugging
        gc.set_debug(gc.DEBUG_SAVEALL)
        
        print("Garbage Collector info:")
        print(f"  Enabled: {gc.isenabled()}")
        print(f"  Thresholds: {gc.get_threshold()}")
        print(f"  Count: {gc.get_count()}")
        
        # Create reference cycle
        class Node:
            def __init__(self, name):
                self.name = name
                self.next = None
            
            def __del__(self):
                print(f"  Node {self.name} deleted")
        
        print("\nCreating reference cycle:")
        node1 = Node("A")
        node2 = Node("B")
        node1.next = node2
        node2.next = node1  # Cycle!
        
        print(f"  node1 -> node2 -> node1 (cycle)")
        print(f"  Reference counts increased")
        
        # Delete references
        print("\nDeleting references to cycle:")
        del node1
        del node2
        print("  Objects still exist (cycle prevents refcount from reaching 0)")
        
        # Force garbage collection
        print("\nRunning garbage collection:")
        collected = gc.collect()
        print(f"  Collected {collected} objects")
        print(f"  Garbage: {gc.garbage}")
        
        # Disable debug mode
        gc.set_debug(0)
    
    @staticmethod
    def demonstrate_memory_management_concepts():
        """Explain key memory management concepts"""
        print("\n\nMemory Management Concepts:")
        
        concepts = [
            ("Heap", "Where objects are stored"),
            ("Stack", "Function calls and local variables"),
            ("Reference", "Pointer to an object"),
            ("Reference Counting", "Primary garbage collection method"),
            ("Generational GC", "Handles reference cycles"),
            ("Memory Pool", "Python's memory allocator (pymalloc)"),
            ("Interning", "Reusing immutable objects (small ints, strings)"),
            ("Object Identity", "Unique identifier (id()) for each object"),
        ]
        
        for concept, description in concepts:
            print(f"  • {concept:25} → {description}")
    
    @staticmethod
    def demonstrate_memory_optimizations():
        """Show Python memory optimizations"""
        print("\n\nMemory Optimizations in Python:")
        
        # Small integer caching
        print("1. Small Integer Caching (-5 to 256):")
        a = 100
        b = 100
        c = 1000
        d = 1000
        print(f"  a = 100, b = 100 → a is b: {a is b}")
        print(f"  c = 1000, d = 1000 → c is d: {c is d} (Python 3.8+)")
        
        # String interning
        print("\n2. String Interning:")
        s1 = "hello"
        s2 = "hello"
        s3 = "".join(['h', 'e', 'l', 'l', 'o'])
        print(f"  s1 = 'hello', s2 = 'hello' → s1 is s2: {s1 is s2}")
        print(f"  s3 = ''.join(['h','e','l','l','o']) → s1 is s3: {s1 is s3}")
        
        # Intern manually
        import sys
        s4 = sys.intern("a_long_string_that_would_not_normally_be_interned")
        s5 = sys.intern("a_long_string_that_would_not_normally_be_interned")
        print(f"  Manual interning → s4 is s5: {s4 is s5}")
        
        # __slots__ memory optimization
        print("\n3. __slots__ Memory Optimization:")
        
        class RegularClass:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        class SlotsClass:
            __slots__ = ['x', 'y']
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        import tracemalloc
        tracemalloc.start()
        
        # Memory usage comparison
        regular_objects = [RegularClass(i, i*2) for i in range(1000)]
        slots_objects = [SlotsClass(i, i*2) for i in range(1000)]
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"  Memory after creating objects: {current / 1024:.1f} KB")
        
        # Estimate memory (simplified)
        print(f"  Regular class size estimate: ~{sys.getsizeof(RegularClass(1, 2))} bytes per instance")
        print(f"  Slots class size estimate: ~{sys.getsizeof(SlotsClass(1, 2))} bytes per instance")
        
        tracemalloc.stop()
    
    @staticmethod
    def demonstrate_memory_profiling():
        """Show basic memory profiling"""
        print("\n\nMemory Profiling Basics:")
        
        print("Using tracemalloc:")
        tracemalloc.start()
        
        # Allocate some memory
        big_list = [i for i in range(100000)]
        big_dict = {i: str(i) for i in range(10000)}
        
        # Get memory snapshot
        snapshot = tracemalloc.take_snapshot()
        
        # Show statistics
        stats = snapshot.statistics('lineno')
        
        print(f"Top 3 memory allocations:")
        for stat in stats[:3]:
            print(f"  {stat}")
        
        tracemalloc.stop()


# Run memory model demonstration
memory_demo = PythonMemoryModel()
memory_demo.demonstrate_reference_counting()
memory_demo.demonstrate_garbage_collection()
memory_demo.demonstrate_memory_management_concepts()
memory_demo.demonstrate_memory_optimizations()
memory_demo.demonstrate_memory_profiling()

# ============================================================================
# 6. WHEN NOT TO OPTIMIZE
# ============================================================================

print("\n\n" + "=" * 40)
print("6. WHEN NOT TO OPTIMIZE")
print("=" * 40)

"""
Premature optimization is the root of all evil - Donald Knuth
Optimize only when you have identified a real performance problem.
"""

class WhenNotToOptimize:
    """Demonstrates when NOT to optimize Python code"""
    
    @staticmethod
    def demonstrate_knuth_quote():
        """Explain the famous quote"""
        print("\nDonald Knuth's Famous Quote:")
        print('  "We should forget about small efficiencies, say about 97% of the time:')
        print('   premature optimization is the root of all evil."')
        print('\n  - Donald Knuth, "Structured Programming with go to Statements"')
        
        print("\nWhat it means:")
        print("  1. Most code doesn't need optimization")
        print("  2. Optimizing too early makes code complex")
        print("  3. Optimize only proven bottlenecks")
        print("  4. Clarity and maintainability come first")
    
    @staticmethod
    def demonstrate_common_premature_optimizations():
        """Show common premature optimizations to avoid"""
        print("\n\nCommon Premature Optimizations to Avoid:")
        
        optimizations = [
            ("Micro-optimizing loops", 
             "for i in range(len(lst)): vs for item in lst:",
             "Readability matters more than tiny speed differences"),
            
            ("Using complex one-liners",
             "result = [x for x in lst if cond(x)] vs multi-line loop",
             "Comprehensions are fine, but don't make them unreadable"),
            
            ("Overusing generators",
             "Always using generators instead of lists",
             "Lists are often fine and more debuggable"),
            
            ("Premature caching",
             "Adding cache decorators everywhere",
             "Cache only when profiling shows benefit"),
            
            ("Avoiding function calls",
             "Inlining functions to avoid call overhead",
             "Function calls are cheap, abstraction is valuable"),
            
            ("Over-optimizing data structures",
             "Using array.array for tiny lists",
             "Python lists are optimized and flexible"),
            
            ("Writing C extensions prematurely",
             "Rewriting Python in C for small gains",
             "First optimize algorithms, then consider Cython/C"),
        ]
        
        for optimization, example, reason in optimizations:
            print(f"\n• {optimization}:")
            print(f"  Example: {example}")
            print(f"  Why avoid: {reason}")
    
    @staticmethod
    def demonstrate_when_to_optimize():
        """Show when optimization IS appropriate"""
        print("\n\nWhen Optimization IS Appropriate:")
        
        scenarios = [
            ("After profiling identifies bottleneck", "Use cProfile, line_profiler"),
            ("Hot loops executed millions of times", "Inner loops in numerical code"),
            ("Memory usage causing swapping", "Large datasets processing"),
            ("User-facing latency issues", "Web response times > 200ms"),
            ("Scaling to larger datasets", "Algorithm doesn't scale well"),
            ("Production performance requirements", "SLA violations"),
        ]
        
        for scenario, tools in scenarios:
            print(f"  • {scenario} → Tools: {tools}")
    
    @staticmethod
    def demonstrate_profiling_first():
        """Show the importance of profiling before optimizing"""
        print("\n\nProfile Before Optimizing:")
        
        import cProfile
        import pstats
        import io
        
        print("Example: Profiling a function")
        
        def slow_function():
            """Function with potential optimization opportunities"""
            result = []
            for i in range(10000):
                # Inefficient string concatenation
                s = ""
                for j in range(10):
                    s += str(j)
                result.append(s)
            return result
        
        def faster_function():
            """Optimized version"""
            result = []
            for i in range(10000):
                # Use join instead of +=
                result.append(''.join(str(j) for j in range(10)))
            return result
        
        # Profile both functions
        print("\nProfiling slow function:")
        pr = cProfile.Profile()
        pr.enable()
        slow_function()
        pr.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(5)  # Top 5 lines
        print(s.getvalue()[:500])  # Print first 500 chars
        
        print("\nKey insight: Profile shows where time is spent")
        print("Then optimize the hot spots, not random code")
    
    @staticmethod
    def demonstrate_big_o_optimization():
        """Show that algorithm complexity matters more than micro-optimizations"""
        print("\n\nAlgorithm Complexity Matters Most:")
        
        print("Compare O(n²) vs O(n log n) vs O(n):")
        
        # O(n²) algorithm
        def quadratic_algorithm(data):
            """Find pairs that sum to 100 - O(n²)"""
            results = []
            for i in range(len(data)):
                for j in range(i + 1, len(data)):
                    if data[i] + data[j] == 100:
                        results.append((data[i], data[j]))
            return results
        
        # O(n) algorithm with set
        def linear_algorithm(data):
            """Find pairs that sum to 100 - O(n)"""
            results = []
            seen = set()
            for num in data:
                complement = 100 - num
                if complement in seen:
                    results.append((num, complement))
                seen.add(num)
            return results
        
        # Test data
        test_data = list(range(1000))
        
        print(f"\nData size: {len(test_data)} elements")
        print("Micro-optimizing the O(n²) algorithm won't help much")
        print("Changing to O(n) algorithm gives 1000x speedup")
        
        # Simple timing comparison
        import time
        
        start = time.time()
        result1 = quadratic_algorithm(test_data[:100])  # Smaller for demo
        time1 = time.time() - start
        
        start = time.time()
        result2 = linear_algorithm(test_data)
        time2 = time.time() - start
        
        print(f"\nO(n²) on 100 elements: {time1:.4f}s")
        print(f"O(n) on 1000 elements: {time2:.4f}s")
        print(f"Algorithm matters more than micro-optimizations!")
    
    @staticmethod
    def demonstrate_readability_vs_performance():
        """Show trade-offs between readability and performance"""
        print("\n\nReadability vs Performance Trade-offs:")
        
        examples = [
            ("List comprehension vs loop",
             "[x*2 for x in range(10) if x % 2 == 0]",
             "result = []\nfor x in range(10):\n    if x % 2 == 0:\n        result.append(x*2)",
             "Comprehension is usually more readable and often faster"),
            
            ("Using built-in functions",
             "max(values)",
             "highest = values[0]\nfor v in values[1:]:\n    if v > highest:\n        highest = v",
             "Built-ins are optimized in C, use them"),
            
            ("Early return vs nested ifs",
             "if not valid:\n    return False\n# continue...",
             "if valid:\n    # lots of nested code",
             "Early returns reduce cognitive load"),
        ]
        
        for name, readable, less_readable, explanation in examples:
            print(f"\n{name}:")
            print(f"  Readable: {readable}")
            print(f"  Less readable: {less_readable}")
            print(f"  {explanation}")
    
    @staticmethod
    def demonstrate_practical_guidelines():
        """Show practical optimization guidelines"""
        print("\n\nPractical Optimization Guidelines:")
        
        guidelines = [
            ("1. Make it work", "First, write correct code"),
            ("2. Make it right", "Ensure it's well-structured, tested"),
            ("3. Make it fast", "Only then optimize if needed"),
            ("4. Profile first", "Don't guess where bottlenecks are"),
            ("5. Optimize algorithms", "Big O improvements > micro-optimizations"),
            ("6. Use appropriate data structures", "dict for lookups, set for membership"),
            ("7. Leverage Python's strengths", "Use built-ins, comprehensions"),
            ("8. Consider trade-offs", "Readability vs performance"),
            ("9. Document optimizations", "Explain why optimization was needed"),
            ("10. Test optimized code", "Ensure optimizations don't break correctness"),
        ]
        
        for guideline, explanation in guidelines:
            print(f"  {guideline:25} → {explanation}")


# Run when not to optimize demonstration
optimize_demo = WhenNotToOptimize()
optimize_demo.demonstrate_knuth_quote()
optimize_demo.demonstrate_common_premature_optimizations()
optimize_demo.demonstrate_when_to_optimize()
optimize_demo.demonstrate_profiling_first()
optimize_demo.demonstrate_big_o_optimization()
optimize_demo.demonstrate_readability_vs_performance()
optimize_demo.demonstrate_practical_guidelines()

# ============================================================================
# SUMMARY & INTERVIEW TIPS
# ============================================================================

print("\n" + "=" * 80)
print("INTERVIEW TIPS & SUMMARY")
print("=" * 80)

interview_tips = """
INTERVIEW TIPS FOR EACH TOPIC:
==============================

1. == vs is:
   • Explain: "== compares values, 'is' compares object identity (memory addresses)"
   • Mention: "Always use 'is' for None, True, False comparisons"
   • Example: "Small integers (-5 to 256) and short strings are interned/cached"
   • Gotcha: "Two lists with same values: == True, is False"

2. Mutable Default Arguments:
   • Explain: "Default arguments are evaluated once at function definition"
   • Problem: "Mutable defaults (list, dict) are shared across function calls"
   • Solution: "Use None as default, create new mutable inside function"
   • Example: "def func(arg=None): arg = [] if arg is None else arg"

3. Shallow vs Deep Copy:
   • Explain: "Shallow copy: new container, same nested objects. Deep copy: new container, new nested objects"
   • Methods: "copy.copy() for shallow, copy.deepcopy() for deep"
   • When to use: "Shallow for simple structures, deep for nested mutable structures"
   • Gotcha: "Slicing lists creates shallow copy: new_list = old_list[:]"

4. Late Binding in Closures:
   • Explain: "Closures capture variables, not values. Value looked up when called"
   • Problem: "In loops, all closures see final loop variable value"
   • Solution: "Use default arguments: lambda x, i=i: x * i"
   • Alternative: "functools.partial or factory function"

5. Python Memory Model:
   • Key points: "Reference counting + generational GC for cycles"
   • Optimizations: "Small integer cache, string interning"
   • Memory: "Objects on heap, references on stack"
   • Management: "Automatic via GC, manual with del and gc.collect()"

6. When Not to Optimize:
   • Quote: "Premature optimization is root of all evil - Knuth"
   • Strategy: "First make it work, then make it right, then make it fast"
   • Process: "Profile before optimizing, optimize algorithms first"
   • Balance: "Readability and maintainability over micro-optimizations"

COMMON INTERVIEW QUESTIONS:
===========================
1. "What's the difference between == and is?"
2. "Why shouldn't you use mutable default arguments?"
3. "When would you use deep copy vs shallow copy?"
4. "What will this closure output? (show loop with lambdas)"
5. "How does Python manage memory?"
6. "When should you optimize Python code?"

PRACTICE PROBLEMS:
==================
1. Write a function that demonstrates the mutable default argument issue
2. Fix a closure that has late binding problems
3. Explain when to use copy.copy() vs copy.deepcopy()
4. Write code that creates a memory leak and explain how to fix it
5. Identify premature optimization in given code
"""

print(interview_tips)

print("\n" + "=" * 80)
print("QUICK REFERENCE CHEAT SHEET")
print("=" * 80)

cheat_sheet = """
== vs is:
  • == : Value equality (uses __eq__)
  • is : Object identity (memory address)
  • Use 'is' for: None, True, False, singletons

Mutable Default Args:
  • BAD:  def f(items=[]):
  • GOOD: def f(items=None):
            items = [] if items is None else items

Copy:
  • Shallow: copy.copy() or obj.copy() or obj[:]
  • Deep: copy.deepcopy()
  • Shallow = new container, same nested objects
  • Deep = new container, new nested objects

Late Binding:
  • Problem: for i in range(3): funcs.append(lambda: print(i))
  • Fix: for i in range(3): funcs.append(lambda i=i: print(i))

Memory:
  • GC: Reference counting + cycle detector
  • Optimizations: Integer cache (-5 to 256), string interning
  • __slots__: Reduces memory for many instances

Optimization:
  • Don't optimize prematurely
  • Profile first (cProfile, line_profiler)
  • Optimize algorithms before micro-optimizations
  • Readability > minor performance gains
"""

print(cheat_sheet)

print("\n" + "=" * 80)
print("DEMONSTRATION COMPLETE")
print("=" * 80)
print("\nKey concepts demonstrated:")
print("  1. == vs is operators")
print("  2. Mutable default arguments pitfall")
print("  3. Shallow vs deep copy differences")
print("  4. Late binding in closures")
print("  5. Python memory model (high level)")
print("  6. When not to optimize (Knuth's principle)")