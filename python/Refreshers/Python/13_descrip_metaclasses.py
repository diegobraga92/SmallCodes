"""
COMPREHENSIVE GUIDE TO PYTHON DESCRIPTORS AND METACLASSES
This script demonstrates and explains descriptors and metaclasses with practical examples.
"""

# ============================================================================
# PART 1: DESCRIPTORS
# ============================================================================

"""
WHAT ARE DESCRIPTORS?
---------------------
Descriptors are Python objects that implement the descriptor protocol (__get__, __set__, __delete__).
They control how attributes are accessed, modified, or deleted on other objects.

Three types of descriptors:
1. Non-data descriptors: Implement only __get__
2. Data descriptors: Implement __set__ and/or __delete__ in addition to __get__
   (Data descriptors have priority over instance dictionaries)

WHEN ARE THEY USED?
-------------------
- When you need attribute access control (validation, logging, type checking)
- Implementing computed/derived attributes
- ORM fields (Django, SQLAlchemy)
- Properties that depend on other properties
- Creating framework-level abstractions
"""

# ============================================================================
# Example 1: BASIC DESCRIPTOR IMPLEMENTATION
# ============================================================================

class PositiveNumber:
    """
    A data descriptor that ensures a value is always positive.
    Practical use: Validation in data models.
    """
    
    def __init__(self, default=0):
        # Store default value
        self.default = default
        # We'll use instance.__dict__ to store actual values
        self.storage_name = None  # Will be set by metaclass
    
    def __set_name__(self, owner, name):
        """
        Called when descriptor is assigned to a class attribute.
        Sets the storage key for instance values.
        """
        self.storage_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        """
        Retrieve the value. If accessed via class (not instance), return the descriptor.
        """
        if obj is None:
            # Accessed via class, e.g., MyClass.attribute
            return self
        
        # Return the stored value, or default if not set
        return getattr(obj, self.storage_name, self.default)
    
    def __set__(self, obj, value):
        """
        Set the value with validation.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Value must be a number, got {type(value).__name__}")
        
        if value < 0:
            raise ValueError(f"Value must be positive, got {value}")
        
        # Store in instance's dictionary
        setattr(obj, self.storage_name, value)
    
    def __delete__(self, obj):
        """
        Delete the stored value.
        """
        if hasattr(obj, self.storage_name):
            delattr(obj, self.storage_name)


class Account:
    """
    Example class using descriptors for validation.
    """
    balance = PositiveNumber(default=100.0)  # Minimum balance
    interest_rate = PositiveNumber(default=0.05)
    
    def __init__(self, initial_balance):
        self.balance = initial_balance  # Uses descriptor's __set__
    
    def apply_interest(self):
        """Demonstrates descriptor usage."""
        self.balance *= (1 + self.interest_rate)


# ============================================================================
# Example 2: COMPUTED ATTRIBUTE DESCRIPTOR
# ============================================================================

class CachedProperty:
    """
    Non-data descriptor that caches computed results.
    Practical use: Expensive computations, lazy evaluation.
    """
    
    def __init__(self, func):
        self.func = func
        self.cache_name = None
    
    def __set_name__(self, owner, name):
        self.cache_name = f"_cached_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Check if cached value exists
        if hasattr(obj, self.cache_name):
            return getattr(obj, self.cache_name)
        
        # Compute, cache, and return
        value = self.func(obj)
        setattr(obj, self.cache_name, value)
        return value


class Rectangle:
    """
    Example using cached property descriptor.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @CachedProperty
    def area(self):
        """Expensive computation (simulated)."""
        print("Computing area...")
        return self.width * self.height
    
    @CachedProperty
    def diagonal(self):
        """Another cached property."""
        print("Computing diagonal...")
        return (self.width**2 + self.height**2) ** 0.5


# ============================================================================
# Example 3: ORM-FIELD LIKE DESCRIPTOR
# ============================================================================

class Field:
    """
    Base class for ORM-like field descriptors.
    Inspired by Django models and SQLAlchemy.
    """
    
    def __init__(self, field_type, default=None, nullable=False):
        self.field_type = field_type
        self.default = default
        self.nullable = nullable
        self.name = None  # Set by metaclass
        self.private_name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # Return value or default
        if hasattr(obj, self.private_name):
            return getattr(obj, self.private_name)
        
        if self.default is not None:
            return self.default() if callable(self.default) else self.default
        
        return None
    
    def __set__(self, obj, value):
        # Handle nullable fields
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be None")
        
        # Type checking
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be of type {self.field_type.__name__}, "
                f"got {type(value).__name__}"
            )
        
        # Custom validation hook
        self.validate(value)
        
        setattr(obj, self.private_name, value)
    
    def validate(self, value):
        """Override in subclasses for custom validation."""
        pass


class CharField(Field):
    """String field with length validation."""
    
    def __init__(self, max_length=255, **kwargs):
        super().__init__(str, **kwargs)
        self.max_length = max_length
    
    def validate(self, value):
        if value is not None and len(value) > self.max_length:
            raise ValueError(
                f"Value exceeds max_length of {self.max_length}"
            )


class IntegerField(Field):
    """Integer field with range validation."""
    
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(int, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value):
        if value is not None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f"Value must be >= {self.min_value}")
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f"Value must be <= {self.max_value}")


# ============================================================================
# PART 2: METACLASSES
# ============================================================================

"""
WHAT ARE METACLASSES?
---------------------
Metaclasses are classes that create classes. While classes create instances,
metaclasses create classes.

Analogy:
- Class : Instance = Factory : Product
- Metaclass : Class = Factory : Factory

Every class in Python has a metaclass (default is 'type').
Metaclasses control class creation and can modify class attributes.

WHEN ARE THEY USED?
-------------------
- Framework development (Django models, SQLAlchemy)
- API creation (enforcing patterns/interfaces)
- Class registration (plugin systems)
- Automatic method/property generation
- ORM model definitions
"""

# ============================================================================
# Example 4: BASIC METACLASS
# ============================================================================

class ModelMeta(type):
    """
    Metaclass for creating ORM-like models.
    
    Responsibilities:
    1. Collect all Field descriptors
    2. Create a 'fields' dictionary
    3. Set a table name based on class name
    4. Add automatic methods
    """
    
    def __new__(mcs, name, bases, namespace):
        """
        Create a new class. Called before __init__.
        
        Args:
            mcs: Metaclass instance (ModelMeta)
            name: Name of the class being created
            bases: Tuple of parent classes
            namespace: Dict of class attributes
        
        Returns:
            New class object
        """
        
        # Skip if this is the base Model class itself
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)
        
        # Collect fields from namespace
        fields = {}
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        
        # Add fields to class namespace
        namespace['_fields'] = fields
        
        # Generate table name (lowercase, plural)
        namespace['_table_name'] = f"{name.lower()}s"
        
        # Add a method to get field names
        def get_field_names(self):
            return list(fields.keys())
        
        namespace['get_field_names'] = get_field_names
        
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Register class (simulating ORM registry)
        if hasattr(cls, '_registry'):
            cls._registry.append(cls)
        else:
            cls._registry = [cls]
        
        return cls
    
    def __init__(cls, name, bases, namespace):
        """
        Initialize the newly created class.
        """
        super().__init__(name, bases, namespace)
        
        # Additional initialization logic
        if hasattr(cls, '_fields'):
            print(f"Model '{name}' created with fields: {list(cls._fields.keys())}")


# ============================================================================
# Example 5: USING METACLASS FOR MODEL CREATION
# ============================================================================

class Model(metaclass=ModelMeta):
    """
    Base model class using ModelMeta metaclass.
    All subclasses will have metaclass behavior applied.
    """
    
    def __init__(self, **kwargs):
        # Set field values from kwargs
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, None)
            setattr(self, field_name, value)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            field_name: getattr(self, field_name)
            for field_name in self._fields
        }
    
    @classmethod
    def get_table_name(cls):
        return cls._table_name


class User(Model):
    """Example ORM-like model using descriptors and metaclass."""
    id = IntegerField()
    username = CharField(max_length=50)
    email = CharField(max_length=255, nullable=True)
    age = IntegerField(min_value=0, max_value=150, default=0)
    
    def greet(self):
        return f"Hello, {self.username}!"


class Product(Model):
    """Another model demonstrating reusability."""
    name = CharField(max_length=100)
    price = IntegerField(min_value=0)
    stock = IntegerField(default=0)


# ============================================================================
# Example 6: METACLASS FOR SINGLETON PATTERN
# ============================================================================

class SingletonMeta(type):
    """
    Metaclass implementing the Singleton pattern.
    Ensures only one instance of a class exists.
    
    Practical use: Database connections, configuration managers.
    """
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Called when class is instantiated.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """Singleton class using metaclass."""
    
    def __init__(self, connection_string="default://localhost"):
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self):
        if not self.connected:
            print(f"Connecting to {self.connection_string}")
            self.connected = True
        return self


# ============================================================================
# Example 7: METACLASS FOR METHOD REGISTRATION
# ============================================================================

class CommandMeta(type):
    """
    Metaclass that automatically registers command classes.
    
    Practical use: CLI frameworks, plugin systems, web routers.
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Skip base class
        if name != 'Command' and hasattr(cls, 'command_name'):
            # Register command
            if not hasattr(cls, '_command_registry'):
                cls._command_registry = {}
            
            cls._command_registry[cls.command_name] = cls
        
        return cls


class Command(metaclass=CommandMeta):
    """Base command class."""
    
    @classmethod
    def get_command(cls, name):
        """Get command by name."""
        return cls._command_registry.get(name)
    
    @classmethod
    def list_commands(cls):
        """List all registered commands."""
        return list(cls._command_registry.keys())
    
    def execute(self):
        raise NotImplementedError


class GreetCommand(Command):
    """Automatically registered command."""
    command_name = "greet"
    
    def execute(self, name="World"):
        print(f"Hello, {name}!")


class ExitCommand(Command):
    """Another registered command."""
    command_name = "exit"
    
    def execute(self):
        print("Goodbye!")
        exit(0)


# ============================================================================
# PART 3: PRACTICAL INTEGRATION EXAMPLE
# ============================================================================

def demo_descriptors():
    """Demonstrate descriptor functionality."""
    print("\n" + "="*60)
    print("DESCRIPTOR DEMONSTRATION")
    print("="*60)
    
    # Example 1: PositiveNumber descriptor
    print("\n1. PositiveNumber Descriptor (Validation):")
    acc = Account(500)
    print(f"Initial balance: {acc.balance}")
    
    try:
        acc.balance = -100  # Should raise ValueError
    except ValueError as e:
        print(f"Validation error: {e}")
    
    acc.balance = 1000
    print(f"Updated balance: {acc.balance}")
    
    # Example 2: CachedProperty descriptor
    print("\n2. CachedProperty Descriptor (Performance):")
    rect = Rectangle(10, 20)
    
    print(f"First access (computes): {rect.area}")
    print(f"Second access (cached): {rect.area}")
    print(f"Diagonal: {rect.diagonal}")
    print(f"Cached diagonal: {rect.diagonal}")
    
    # Example 3: ORM-like fields
    print("\n3. ORM-like Field Descriptors:")


def demo_metaclasses():
    """Demonstrate metaclass functionality."""
    print("\n" + "="*60)
    print("METACLASS DEMONSTRATION")
    print("="*60)
    
    # Example 4 & 5: Model metaclass
    print("\n1. Model Metaclass (ORM-like):")
    
    # Create a user instance
    user = User(id=1, username="alice", email="alice@example.com", age=25)
    
    print(f"User table: {User.get_table_name()}")
    print(f"User fields: {user.get_field_names()}")
    print(f"User as dict: {user.to_dict()}")
    print(f"User greeting: {user.greet()}")
    
    # Try validation
    try:
        user.age = -5  # Should fail
    except ValueError as e:
        print(f"Validation error: {e}")
    
    # Check registered models
    print(f"\nRegistered models: {[m.__name__ for m in Model._registry]}")
    
    # Example 6: Singleton metaclass
    print("\n2. Singleton Metaclass:")
    
    db1 = DatabaseConnection("postgres://localhost")
    db2 = DatabaseConnection("mysql://localhost")  # Same instance!
    
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 connection string: {db1.connection_string}")
    
    # Example 7: Command registration metaclass
    print("\n3. Command Registration Metaclass:")
    
    print(f"Available commands: {Command.list_commands()}")
    
    greet_cmd_class = Command.get_command("greet")
    if greet_cmd_class:
        cmd = greet_cmd_class()
        cmd.execute("Python Developer")


def advanced_example():
    """
    Advanced example combining descriptors and metaclasses
    to create a complete mini-ORM.
    """
    print("\n" + "="*60)
    print("ADVANCED EXAMPLE: MINI ORM")
    print("="*60)
    
    class QueryBuilder:
        """Simple query builder for demonstration."""
        
        @staticmethod
        def build_insert(model_class, data):
            fields = ', '.join(data.keys())
            values = ', '.join(str(v) for v in data.values())
            return f"INSERT INTO {model_class._table_name} ({fields}) VALUES ({values})"
        
        @staticmethod
        def build_select(model_class, where=None):
            query = f"SELECT * FROM {model_class._table_name}"
            if where:
                query += f" WHERE {where}"
            return query
    
    # Add query methods to Model using metaclass modification
    class ORMMeta(ModelMeta):
        """Extended metaclass with query capabilities."""
        
        def __new__(mcs, name, bases, namespace):
            cls = super().__new__(mcs, name, bases, namespace)
            
            if name != 'Model':
                # Add save method
                def save(self):
                    data = self.to_dict()
                    query = QueryBuilder.build_insert(self.__class__, data)
                    print(f"[ORM] Executing: {query}")
                    return True
                
                cls.save = save
                
                # Add classmethod for querying
                @classmethod
                def filter(cls, **conditions):
                    where_clause = ' AND '.join(
                        f"{k} = {v}" for k, v in conditions.items()
                    )
                    query = QueryBuilder.build_select(cls, where_clause)
                    print(f"[ORM] Query: {query}")
                    # In real ORM, this would execute and return instances
                    return []
                
                cls.filter = filter
            
            return cls
    
    # Redefine Model with enhanced metaclass
    class ORMModel(metaclass=ORMMeta):
        """Enhanced base model."""
        
        def __init__(self, **kwargs):
            for field_name in self._fields:
                value = kwargs.get(field_name)
                setattr(self, field_name, value)
    
    # Create models
    class Customer(ORMModel):
        id = IntegerField()
        name = CharField(max_length=100)
        status = CharField(max_length=20, default="active")
    
    class Order(ORMModel):
        id = IntegerField()
        customer_id = IntegerField()
        amount = IntegerField(min_value=0)
    
    # Demo
    cust = Customer(id=1, name="Bob")
    print(f"Customer: {cust.to_dict()}")
    cust.save()
    
    orders = Order.filter(customer_id=1, amount__gt=100)
    print(f"Found {len(orders)} orders")


def main():
    """
    Main demonstration function.
    """
    print("PYTHON DESCRIPTORS AND METACLASSES DEMONSTRATION")
    print("="*60)
    
    demo_descriptors()
    demo_metaclasses()
    advanced_example()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
    Key Takeaways:
    
    1. DESCRIPTORS:
       - Control attribute access (__get__, __set__, __delete__)
       - Used for validation, computed properties, ORM fields
       - Data descriptors > instance dictionary
       - Non-data descriptors < instance dictionary
    
    2. METACLASSES:
       - Classes that create classes
       - Control class creation and modification
       - Used in frameworks, ORMs, APIs
       - Can register, modify, or enhance classes automatically
    
    3. PRACTICAL APPLICATIONS:
       - Django models (Field descriptors + ModelBase metaclass)
       - SQLAlchemy (Column descriptors + DeclarativeMeta)
       - Validation frameworks
       - API schema generation
       - Plugin/command registration systems
    
    4. WHEN TO USE:
       - Descriptors: When you need fine-grained attribute control
       - Metaclasses: When you need to modify class creation behavior
       - Often used together in frameworks
    """)


if __name__ == "__main__":
    main()