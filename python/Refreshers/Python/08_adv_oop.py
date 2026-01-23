"""
ADVANCED PYTHON OBJECT-ORIENTED PROGRAMMING
Covers advanced OOP concepts, encapsulation, design patterns, and special methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Any
import json

# ============================================================================
# PART 1: ADVANCED OOP CONCEPTS
# ============================================================================

print("=" * 60)
print("ADVANCED OOP CONCEPTS")
print("=" * 60)

# ============================================================================
# 1. COMPOSITION vs INHERITANCE
# ============================================================================
print("\n1. COMPOSITION vs INHERITANCE")
print("-" * 40)

"""
COMPOSITION: "Has-a" relationship - Building complex objects from simpler ones.
INHERITANCE: "Is-a" relationship - Creating specialized versions of existing classes.

Favor composition over inheritance when possible - it's more flexible.
"""

# Example demonstrating composition over inheritance
print("\nCOMPOSITION EXAMPLE: Building complex objects from components")

class Engine:
    """Engine component - designed for composition."""
    
    def __init__(self, horsepower: int, fuel_type: str = "gasoline"):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.is_running = False
    
    def start(self):
        self.is_running = True
        print(f"Engine ({self.horsepower} HP) started")
    
    def stop(self):
        self.is_running = False
        print(f"Engine stopped")

class Wheels:
    """Wheels component."""
    
    def __init__(self, count: int = 4, diameter: float = 16.0):
        self.count = count
        self.diameter = diameter
        self.pressure = 32.0  # PSI
    
    def inflate(self, pressure: float):
        self.pressure = pressure
        print(f"Wheels inflated to {pressure} PSI")

class Car:
    """Car using COMPOSITION - HAS-A Engine and Wheels."""
    
    def __init__(self, model: str, engine: Engine, wheels: Wheels):
        self.model = model
        self.engine = engine  # Composition: Car HAS-A Engine
        self.wheels = wheels  # Composition: Car HAS-A Wheels
        self.speed = 0
    
    def drive(self):
        """Uses composed objects' functionality."""
        if not self.engine.is_running:
            self.engine.start()
        self.speed = 30
        print(f"{self.model} is driving at {self.speed} mph")
    
    def maintenance(self):
        """Uses composed objects' functionality."""
        self.wheels.inflate(35.0)
        print(f"{self.model} maintenance complete")

print("\nINHERITANCE EXAMPLE: Creating specialized versions")

class Vehicle:
    """Base class for inheritance example."""
    
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
    
    def start(self):
        print(f"{self.make} {self.model} starting...")
    
    def stop(self):
        print(f"{self.make} {self.model} stopping...")

class ElectricCar(Vehicle):
    """INHERITANCE: ElectricCar IS-A Vehicle."""
    
    def __init__(self, make: str, model: str, year: int, battery_capacity: float):
        super().__init__(make, model, year)  # Initialize parent class
        self.battery_capacity = battery_capacity  # Child-specific attribute
        self.charge_level = 100.0
    
    # ============================================================================
    # 2. METHOD OVERRIDING
    # ============================================================================
    def start(self):
        """Override parent's start method for electric car behavior."""
        print(f"{self.make} {self.model} (Electric) starting silently...")
        print(f"Battery: {self.charge_level}% remaining")

# Demonstration
print("\nComposition Example:")
engine = Engine(horsepower=200)
wheels = Wheels(count=4, diameter=18.0)
car = Car("Sedan X", engine, wheels)
car.drive()
car.maintenance()

print("\nInheritance Example:")
tesla = ElectricCar("Tesla", "Model 3", 2023, 75.0)
tesla.start()
tesla.stop()

print("\nWHEN TO USE COMPOSITION vs INHERITANCE:")
print("-" * 40)
print("""
COMPOSITION (HAS-A) - Use when:
• You need functionality from multiple sources
• You want to change behavior at runtime
• You're modeling components/parts
• You want more flexibility

INHERITANCE (IS-A) - Use when:
• There's a clear hierarchical relationship
• You need polymorphism with base class
• Child truly is a specialization of parent
• You need to override most parent methods
""")

# ============================================================================
# 3. SUPER() FUNCTION
# ============================================================================
print("\n\n3. SUPER() FUNCTION")
print("-" * 40)
print("""
super() returns a proxy object that delegates method calls to a parent class.
Used to:
1. Call parent class constructor (__init__)
2. Call overridden parent methods
3. Work with multiple inheritance (cooperative multiple inheritance)
""")

class Animal:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic animal sound"

class Dog(Animal):
    def __init__(self, name: str, breed: str):
        # Call parent's __init__ using super()
        super().__init__(name, species="Canine")
        self.breed = breed
    
    def make_sound(self):
        # Call parent method, then extend behavior
        base_sound = super().make_sound()
        return f"{base_sound}, but actually: Woof! Woof!"

# Demonstrating super()
print("\nDemonstrating super():")
dog = Dog("Buddy", "Golden Retriever")
print(f"Name: {dog.name}, Species: {dog.species}, Breed: {dog.breed}")
print(f"Sound: {dog.make_sound()}")

# ============================================================================
# 4. ABSTRACT BASE CLASSES (ABCs)
# ============================================================================
print("\n\n4. ABSTRACT BASE CLASSES (ABCs)")
print("-" * 40)
print("""
ABCs define interfaces that subclasses must implement.
Prevents instantiation of incomplete classes.
Use @abstractmethod decorator to mark abstract methods.
""")

class Shape(ABC):
    """Abstract base class for shapes."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def area(self) -> float:
        """Abstract method - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Another abstract method."""
        pass
    
    def describe(self) -> str:
        """Concrete method - inherited by all subclasses."""
        return f"{self.name} with area={self.area():.2f}, perimeter={self.perimeter():.2f}"

class Circle(Shape):
    """Concrete implementation of Shape."""
    
    def __init__(self, radius: float):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self) -> float:
        """Implement abstract method."""
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        """Implement abstract method."""
        return 2 * 3.14159 * self.radius

class Rectangle(Shape):
    """Another concrete implementation."""
    
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# Demonstrating ABCs
print("\nDemonstrating Abstract Base Classes:")
try:
    # shape = Shape("Generic")  # This would raise TypeError - cannot instantiate ABC
    # print("Created abstract shape")  # Won't reach here
    pass
except TypeError as e:
    print(f"Cannot instantiate abstract class: {e}")

circle = Circle(5.0)
rectangle = Rectangle(4.0, 6.0)

print(f"\n{circle.describe()}")
print(f"{rectangle.describe()}")

# ============================================================================
# 5. MIXINS AND MULTIPLE INHERITANCE
# ============================================================================
print("\n\n5. MIXINS AND MULTIPLE INHERITANCE")
print("-" * 40)
print("""
MIXIN: A class that provides specific functionality to be inherited by other classes.
• Not meant to stand alone
• Provides behavior, not identity
• Used with multiple inheritance

MRO (Method Resolution Order): Order in which Python looks for methods in inheritance hierarchy.
Use ClassName.__mro__ to see the order.
""")

class JSONSerializableMixin:
    """Mixin to add JSON serialization capability."""
    
    def to_json(self) -> str:
        """Convert object to JSON string."""
        import json
        return json.dumps(self.__dict__, indent=2)
    
    @classmethod
    def from_json(cls, json_string: str):
        """Create object from JSON string."""
        data = json.loads(json_string)
        return cls(**data)

class LoggableMixin:
    """Mixin to add logging capability."""
    
    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.__class__.__name__}: {message}")

class Product(JSONSerializableMixin, LoggableMixin):
    """Class using multiple inheritance with mixins."""
    
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category
    
    def apply_discount(self, percent: float):
        """Apply discount to product price."""
        old_price = self.price
        self.price *= (1 - percent / 100)
        self.log(f"Discount applied: {old_price} -> {self.price}")

# Demonstrating mixins and multiple inheritance
print("\nDemonstrating Mixins and Multiple Inheritance:")
product = Product("Laptop", 999.99, "Electronics")
product.log("Product created")
product.apply_discount(10.0)

print(f"\nProduct as JSON:\n{product.to_json()}")

# Demonstrating MRO (Method Resolution Order)
print("\nMethod Resolution Order (MRO) for Product class:")
for i, cls in enumerate(Product.__mro__):
    print(f"{i}: {cls.__name__}")

print("\nKey points about MRO:")
print("1. Python uses C3 Linearization algorithm")
print("2. Order: Current class -> Parents (left to right) -> Object")
print("3. No class appears more than once")
print("4. Child classes come before parent classes")

# ============================================================================
# 6. CLASS METHODS vs STATIC METHODS
# ============================================================================
print("\n\n6. CLASS METHODS vs STATIC METHODS")
print("-" * 40)

class Employee:
    """Demonstrating class and static methods."""
    
    # Class attribute
    company = "Tech Corp"
    total_employees = 0
    
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
        Employee.total_employees += 1
    
    # ============================================================================
    # INSTANCE METHOD
    # ============================================================================
    def get_info(self) -> str:
        """Instance method - operates on instance (self)."""
        return f"{self.name} earns ${self.salary:.2f}"
    
    # ============================================================================
    # CLASS METHOD
    # ============================================================================
    @classmethod
    def create_from_string(cls, employee_string: str):
        """
        Class method - operates on class (cls).
        Often used as alternative constructors.
        """
        name, salary_str = employee_string.split(",")
        salary = float(salary_str.strip())
        return cls(name.strip(), salary)
    
    @classmethod
    def get_company_info(cls) -> str:
        """Class method accessing class attributes."""
        return f"{cls.company} has {cls.total_employees} employees"
    
    # ============================================================================
    # STATIC METHOD
    # ============================================================================
    @staticmethod
    def calculate_bonus(salary: float, performance_rating: float) -> float:
        """
        Static method - doesn't need instance or class.
        Pure utility function related to Employee domain.
        """
        if performance_rating >= 0.9:
            return salary * 0.2
        elif performance_rating >= 0.7:
            return salary * 0.1
        else:
            return salary * 0.05

# Demonstration
print("\nDemonstrating Method Types:")
emp1 = Employee("Alice", 75000)
print(f"Instance method: {emp1.get_info()}")
print(f"Class method: {Employee.get_company_info()}")

# Using class method as alternative constructor
emp2 = Employee.create_from_string("Bob, 80000")
print(f"Created via class method: {emp2.get_info()}")

# Using static method
bonus = Employee.calculate_bonus(75000, 0.85)
print(f"Static method (bonus): ${bonus:.2f}")

print("\nSUMMARY:")
print("-" * 40)
print("""
INSTANCE METHODS:
• First parameter: self
• Operates on instance data
• Can modify instance attributes

CLASS METHODS:
• First parameter: cls
• Decorated with @classmethod
• Operates on class data
• Can modify class attributes
• Often used as alternative constructors

STATIC METHODS:
• No self or cls parameter
• Decorated with @staticmethod
• Utility functions related to class
• Cannot modify instance or class state
""")

# ============================================================================
# 7. PROPERTY DECORATORS
# ============================================================================
print("\n\n7. PROPERTY DECORATORS (@property, @setter, @deleter)")
print("-" * 40)
print("""
Properties allow controlled access to attributes.
They look like attributes but behave like methods.

@property - Getter method
@attribute.setter - Setter method  
@attribute.deleter - Deleter method
""")

class BankAccount:
    """Demonstrating property decorators."""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner  # Protected attribute (convention)
        self._balance = initial_balance  # Protected attribute
        self._transaction_history = []
    
    # ============================================================================
    # GETTER (PROPERTY)
    # ============================================================================
    @property
    def balance(self) -> float:
        """Getter for balance - read-only from outside."""
        return self._balance
    
    @property
    def owner(self) -> str:
        """Getter for owner."""
        return self._owner
    
    # ============================================================================
    # SETTER
    # ============================================================================
    @owner.setter
    def owner(self, new_owner: str):
        """Setter for owner with validation."""
        if not new_owner or not isinstance(new_owner, str):
            raise ValueError("Owner name must be a non-empty string")
        self._owner = new_owner
    
    # ============================================================================
    # COMPUTED PROPERTY
    # ============================================================================
    @property
    def is_overdrawn(self) -> bool:
        """Computed property - no storage, calculated on demand."""
        return self._balance < 0
    
    @property
    def summary(self) -> str:
        """Another computed property."""
        status = "Overdrawn" if self.is_overdrawn else "OK"
        return f"{self._owner}: ${self._balance:.2f} ({status})"
    
    @summary.setter
    def summary(self, value: str):
        """
        Example of a setter that parses a string to set multiple attributes.
        Not typical, but shows flexibility.
        """
        try:
            name, balance_str = value.split(":")
            self._owner = name.strip()
            self._balance = float(balance_str.strip())
        except ValueError:
            raise ValueError("Summary must be 'Name: balance'")
    
    @summary.deleter
    def summary(self):
        """Deleter example - resets account."""
        print(f"Resetting account for {self._owner}")
        self._balance = 0
        self._transaction_history.clear()
    
    # Regular methods
    def deposit(self, amount: float):
        """Deposit money with validation."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transaction_history.append(f"Deposit: +${amount:.2f}")
    
    def withdraw(self, amount: float):
        """Withdraw money with validation."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transaction_history.append(f"Withdrawal: -${amount:.2f}")

# Demonstration
print("\nDemonstrating Properties:")
account = BankAccount("John Doe", 1000.0)

print(f"Using getters (look like attributes):")
print(f"  account.balance = ${account.balance:.2f}")
print(f"  account.owner = {account.owner}")
print(f"  account.is_overdrawn = {account.is_overdrawn}")
print(f"  account.summary = {account.summary}")

print("\nUsing setter:")
account.owner = "Jane Smith"  # Uses @owner.setter
print(f"  New owner: {account.owner}")

print("\nTrying to set balance directly (won't work - no setter):")
try:
    account.balance = 5000  # This will fail - no setter defined
except AttributeError as e:
    print(f"  Error: {e}")

print("\nUsing computed property setter:")
account.summary = "Robert Johnson: 2500.00"
print(f"  New summary: {account.summary}")

print("\nUsing deleter:")
del account.summary  # Calls @summary.deleter
print(f"  After deletion - balance: ${account.balance:.2f}")

# ============================================================================
# PART 2: ENCAPSULATION & DESIGN
# ============================================================================

print("\n" + "=" * 60)
print("ENCAPSULATION & DESIGN")
print("=" * 60)

# ============================================================================
# 1. PUBLIC vs PROTECTED vs PRIVATE CONVENTIONS
# ============================================================================
print("\n1. PUBLIC vs PROTECTED vs PRIVATE CONVENTIONS")
print("-" * 40)
print("""
Python doesn't have true private/protected - it's based on conventions:

PUBLIC:        attribute_name        - Accessible anywhere
PROTECTED:     _attribute_name       - "Shouldn't" be accessed outside class (convention)
PRIVATE:       __attribute_name      - Name mangled to _ClassName__attribute_name

Note: All are technically accessible, but private attributes are name-mangled.
""")

class AccessExample:
    """Demonstrating access level conventions."""
    
    def __init__(self):
        self.public = "I'm public"           # Public attribute
        self._protected = "I'm protected"    # Protected attribute (convention)
        self.__private = "I'm private"       # Private attribute (name-mangled)
    
    def show_access(self):
        """Method showing all attributes are accessible within class."""
        print(f"Inside class:")
        print(f"  public: {self.public}")
        print(f"  _protected: {self._protected}")
        print(f"  __private: {self.__private}")
    
    def get_private(self):
        """Public getter for private attribute."""
        return self.__private

# Demonstration
print("\nDemonstrating Access Levels:")
obj = AccessExample()

print("From outside class:")
print(f"  obj.public: {obj.public}")
print(f"  obj._protected: {obj._protected}")  # Works but convention says don't

try:
    print(f"  obj.__private: {obj.__private}")  # This will fail
except AttributeError as e:
    print(f"  obj.__private: AttributeError - {e}")

# Name mangling demonstration
print(f"\nName mangling in action:")
print(f"  Actual attribute name: {obj._AccessExample__private}")  # Access via mangled name

print("\nUsing class method to access all:")
obj.show_access()

print("\nBest Practice - Use getters/setters:")
print(f"  obj.get_private(): {obj.get_private()}")

# ============================================================================
# 2. WHEN NOT TO USE OOP
# ============================================================================
print("\n\n2. WHEN NOT TO USE OOP")
print("-" * 40)

# Example 1: Simple data transformation (functional approach is cleaner)
print("\nExample 1: Data Transformation")

# Functional approach (often better for simple transformations)
def process_data_functional(data):
    """Pure function - no state, no side effects."""
    return [x * 2 for x in data if x > 0]

# OOP approach (overkill for simple operations)
class DataProcessor:
    """OOP version - unnecessary complexity."""
    def __init__(self, data):
        self.data = data
    
    def process(self):
        return [x * 2 for x in self.data if x > 0]

# Comparison
data = [1, -2, 3, -4, 5]
print(f"Functional: {process_data_functional(data)}")
print(f"OOP: {DataProcessor(data).process()}")

print("\nExample 2: Utility functions")

# Collection of related utility functions (better as module functions)
def math_utils():
    """Module functions - no need for OOP here."""
    
    def add(a, b):
        return a + b
    
    def multiply(a, b):
        return a * b
    
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    
    return add, multiply, factorial

add_func, multiply_func, factorial_func = math_utils()
print(f"Utility functions: add(2,3)={add_func(2,3)}, factorial(5)={factorial_func(5)}")

print("\nWHEN TO AVOID OOP:")
print("-" * 40)
print("""
1. SIMPLE SCRIPTS: When you just need to get something done quickly
2. PURE FUNCTIONS: When operations are stateless and side-effect free
3. PERFORMANCE: OOP has overhead; use data-oriented design for performance-critical code
4. DATA PROCESSING: Pandas/NumPy style operations are often better procedural
5. WHEN IT ADD COMPLEXITY WITHOUT BENEFIT: Don't create classes just because

GOOD CANDIDATES FOR OOP:
1. Complex systems with clear entities
2. When you need to maintain state
3. GUI applications
4. Frameworks and libraries
5. When polymorphism is needed
""")

# ============================================================================
# 3. DATA CLASSES (@dataclass)
# ============================================================================
print("\n\n3. DATA CLASSES (@dataclass)")
print("-" * 40)
print("""
Data classes automatically generate common methods:
• __init__()
• __repr__()
• __eq__()
• And more...

Use when you need a class mainly to store data.
Less boilerplate code.
""")

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar

# Basic data class
@dataclass
class Point:
    """Simple data class for 2D points."""
    x: float
    y: float
    
    # Class variable (not in __init__)
    description: ClassVar[str] = "A point in 2D space"
    
    def distance_from_origin(self) -> float:
        """Custom method - data classes can have methods too."""
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Data class with default values and field options
@dataclass(order=True)  # order=True generates comparison methods
class ProductItem:
    """Data class for product items with various field options."""
    name: str
    price: float
    quantity: int = 1  # Default value
    tags: List[str] = field(default_factory=list)  # Mutable default using field()
    discount: Optional[float] = None  # Optional field
    
    # Post-init processing
    def __post_init__(self):
        """Called after __init__ to calculate derived values."""
        self.total_price = self.price * self.quantity
        if self.discount:
            self.total_price *= (1 - self.discount / 100)

# Demonstration
print("\nBasic Data Class:")
point = Point(3.0, 4.0)
print(f"point = {point}")  # Automatic __repr__
print(f"point.x = {point.x}, point.y = {point.y}")
print(f"Distance from origin: {point.distance_from_origin():.2f}")
print(f"Description: {Point.description}")

print("\nData Class with Defaults and Ordering:")
item1 = ProductItem("Laptop", 999.99, 2, ["electronics", "sale"], 10.0)
item2 = ProductItem("Mouse", 49.99)
item3 = ProductItem("Keyboard", 89.99, tags=["electronics"])

print(f"item1: {item1}")
print(f"item2: {item2}")
print(f"item3: {item3}")

print(f"\nAutomatic comparison (because order=True):")
print(f"item1.total_price > item2.total_price: {item1.total_price > item2.total_price}")

print(f"\nitem1 fields:")
for field_name, field_value in item1.__dict__.items():
    print(f"  {field_name}: {field_value}")

# ============================================================================
# PART 3: SPECIAL METHODS (DUNDER METHODS)
# ============================================================================

print("\n" + "=" * 60)
print("SPECIAL METHODS (DUNDER METHODS)")
print("=" * 60)

class Vector:
    """Class demonstrating various dunder methods."""
    
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
    
    # ============================================================================
    # 1. __str__ vs __repr__
    # ============================================================================
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"
    
    # ============================================================================
    # 2. COMPARISON METHODS
    # ============================================================================
    def __eq__(self, other: Any) -> bool:
        """Equality comparison."""
        if not isinstance(other, Vector):
            return False
        return (self.x == other.x and 
                self.y == other.y and 
                self.z == other.z)
    
    def __lt__(self, other: Any) -> bool:
        """Less than comparison (based on magnitude)."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.magnitude() < other.magnitude()
    
    def __le__(self, other: Any) -> bool:
        """Less than or equal."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.magnitude() <= other.magnitude()
    
    # ============================================================================
    # 3. MATHEMATICAL OPERATIONS
    # ============================================================================
    def __add__(self, other: Any) -> 'Vector':
        """Vector addition."""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Any) -> 'Vector':
        """Vector subtraction."""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: Any) -> 'Vector':
        """Scalar multiplication."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar: Any) -> 'Vector':
        """Reverse multiplication (scalar * vector)."""
        return self.__mul__(scalar)
    
    # ============================================================================
    # 4. __len__ AND __iter__
    # ============================================================================
    def __len__(self) -> int:
        """Length returns number of dimensions (always 3 for 3D vector)."""
        return 3
    
    def __iter__(self):
        """Make vector iterable over its components."""
        yield self.x
        yield self.y
        yield self.z
    
    def __getitem__(self, index: int) -> float:
        """Allow indexing: vector[0] gets x, vector[1] gets y, etc."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        raise IndexError("Vector index out of range")
    
    # ============================================================================
    # 5. __call__ METHOD
    # ============================================================================
    def __call__(self, *scalars: float) -> 'Vector':
        """
        Make vector callable.
        When called with arguments, scales the vector.
        """
        if len(scalars) == 1:
            return self * scalars[0]
        elif len(scalars) == 3:
            return Vector(self.x * scalars[0], 
                         self.y * scalars[1], 
                         self.z * scalars[2])
        else:
            raise ValueError("Call with 1 or 3 arguments")
    
    # ============================================================================
    # 6. OTHER USEFUL METHODS
    # ============================================================================
    def __bool__(self) -> bool:
        """Truth value testing - vector is False if zero vector."""
        return not (self.x == 0 and self.y == 0 and self.z == 0)
    
    def __abs__(self) -> float:
        """Absolute value returns magnitude."""
        return self.magnitude()
    
    # Helper methods
    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def dot(self, other: 'Vector') -> float:
        """Dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

# Demonstration
print("\nDemonstrating Special Methods:")

v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
v3 = Vector(1, 2, 3)

# 1. __str__ and __repr__
print(f"\n1. String Representations:")
print(f"  str(v1): {str(v1)}")
print(f"  repr(v1): {repr(v1)}")

# 2. Comparison methods
print(f"\n2. Comparisons:")
print(f"  v1 == v2: {v1 == v2}")
print(f"  v1 == v3: {v1 == v3}")
print(f"  v1 < v2: {v1 < v2}")  # Based on magnitude

# 3. Mathematical operations
print(f"\n3. Mathematical Operations:")
print(f"  v1 + v2: {v1 + v2}")
print(f"  v2 - v1: {v2 - v1}")
print(f"  v1 * 2: {v1 * 2}")
print(f"  3 * v1: {3 * v1}")  # Uses __rmul__

# 4. __len__, __iter__, and __getitem__
print(f"\n4. Iteration and Indexing:")
print(f"  len(v1): {len(v1)}")
print(f"  Iteration: {[coord for coord in v1]}")
print(f"  v1[0]: {v1[0]}, v1[1]: {v1[1]}, v1[2]: {v1[2]}")

# 5. __call__ method
print(f"\n5. Callable Objects:")
v4 = v1(2)  # Scale by 2
print(f"  v1(2): {v4}")
v5 = v1(2, 3, 4)  # Scale each component differently
print(f"  v1(2, 3, 4): {v5}")

# 6. Other methods
print(f"\n6. Other Special Methods:")
print(f"  bool(v1): {bool(v1)}")
print(f"  bool(Vector(0,0,0)): {bool(Vector(0,0,0))}")
print(f"  abs(v1): {abs(v1):.2f}")
print(f"  v1.dot(v2): {v1.dot(v2)}")

# ============================================================================
# COMPREHENSIVE EXAMPLE: USING ALL CONCEPTS TOGETHER
# ============================================================================

print("\n" + "=" * 60)
print("COMPREHENSIVE EXAMPLE")
print("=" * 60)

@dataclass
class OrderItem:
    """Data class for order items."""
    product_id: str
    name: str
    price: float
    quantity: int = 1
    
    @property
    def total(self) -> float:
        return self.price * self.quantity

class ShoppingCart:
    """Shopping cart using composition, properties, and special methods."""
    
    def __init__(self, customer_id: str):
        self.customer_id = customer_id
        self._items: List[OrderItem] = []  # Composition: cart HAS items
        self._discount = 0.0
    
    def add_item(self, item: OrderItem):
        """Add item to cart."""
        self._items.append(item)
    
    def remove_item(self, product_id: str):
        """Remove item by product ID."""
        self._items = [item for item in self._items 
                      if item.product_id != product_id]
    
    @property
    def subtotal(self) -> float:
        """Calculate subtotal (computed property)."""
        return sum(item.total for item in self._items)
    
    @property
    def discount(self) -> float:
        return self._discount
    
    @discount.setter
    def discount(self, value: float):
        """Setter with validation."""
        if not 0 <= value <= 100:
            raise ValueError("Discount must be between 0 and 100")
        self._discount = value
    
    @property
    def total(self) -> float:
        """Calculate total after discount."""
        subtotal = self.subtotal
        return subtotal * (1 - self._discount / 100)
    
    # Special methods
    def __len__(self) -> int:
        """Number of unique items in cart."""
        return len(self._items)
    
    def __iter__(self):
        """Make cart iterable over items."""
        return iter(self._items)
    
    def __contains__(self, product_id: str) -> bool:
        """Check if product is in cart."""
        return any(item.product_id == product_id for item in self._items)
    
    def __str__(self) -> str:
        return f"ShoppingCart for customer {self.customer_id} with {len(self)} items"
    
    def __repr__(self) -> str:
        return f"ShoppingCart(customer_id='{self.customer_id}', items={len(self._items)})"

# Using the comprehensive example
print("\nRunning Comprehensive Example:")

# Create some order items
laptop = OrderItem("P001", "Laptop", 999.99, 1)
mouse = OrderItem("P002", "Mouse", 49.99, 2)
keyboard = OrderItem("P003", "Keyboard", 89.99, 1)

# Create shopping cart
cart = ShoppingCart("CUST123")
cart.add_item(laptop)
cart.add_item(mouse)
cart.add_item(keyboard)

# Apply discount
cart.discount = 10.0  # 10% discount

# Demonstrate functionality
print(f"\n{cart}")
print(f"Subtotal: ${cart.subtotal:.2f}")
print(f"Discount: {cart.discount}%")
print(f"Total: ${cart.total:.2f}")

print(f"\nNumber of items: {len(cart)}")
print(f"Is laptop in cart? {'P001' in cart}")
print(f"Is tablet in cart? {'P004' in cart}")

print("\nItems in cart:")
for item in cart:  # Uses __iter__
    print(f"  {item.name}: {item.quantity} × ${item.price:.2f} = ${item.total:.2f}")

print(f"\nCart representation: {repr(cart)}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY OF KEY CONCEPTS")
print("=" * 60)

summary = """
1. COMPOSITION vs INHERITANCE:
   • Composition (HAS-A): More flexible, uses components
   • Inheritance (IS-A): Hierarchical, for polymorphism

2. METHOD OVERRIDING:
   • Child classes can override parent methods
   • Use super() to call parent implementation

3. ABSTRACT BASE CLASSES:
   • Define interfaces with @abstractmethod
   • Cannot instantiate incomplete classes

4. MIXINS & MULTIPLE INHERITANCE:
   • Mixins add functionality without being standalone
   • MRO determines method lookup order

5. METHOD TYPES:
   • Instance: Operates on self
   • Class (@classmethod): Operates on cls, alternative constructors
   • Static (@staticmethod): Utility functions

6. PROPERTIES:
   • @property: Getter method
   • @attribute.setter: Setter with validation
   • @attribute.deleter: Cleanup actions

7. ENCAPSULATION:
   • Public: attribute_name
   • Protected: _attribute_name (convention)
   • Private: __attribute_name (name-mangled)

8. DATA CLASSES (@dataclass):
   • Automatically generate __init__, __repr__, __eq__
   • Less boilerplate for data-centric classes

9. SPECIAL METHODS:
   • __str__: User-friendly string
   • __repr__: Developer-friendly string
   • __eq__, __lt__: Comparisons
   • __len__, __iter__: Container behavior
   • __call__: Make objects callable

BEST PRACTICES:
1. Favor composition over inheritance
2. Use properties for controlled attribute access
3. Use data classes for simple data containers
4. Implement appropriate special methods
5. Keep classes focused and cohesive
"""

print(summary)