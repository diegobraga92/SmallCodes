"""
COMPREHENSIVE PYTHON OBJECT-ORIENTED PROGRAMMING TUTORIAL
This script demonstrates fundamental OOP concepts in Python with detailed explanations.
"""

# ============================================================================
# 1. OBJECT-ORIENTED PROGRAMMING BASICS
# ============================================================================
"""
Object-Oriented Programming (OOP) is a programming paradigm that organizes code
around "objects" which contain both data (attributes) and behavior (methods).
Key principles: Encapsulation, Abstraction, Inheritance, Polymorphism
"""

# ============================================================================
# 2. CLASSES AND OBJECTS
# ============================================================================
"""
CLASS: A blueprint/template for creating objects. Defines attributes and methods.
OBJECT: An instance of a class. Has actual values for the attributes.
"""

class Vehicle:
    """
    This is a base class representing a generic vehicle.
    Classes are defined using the 'class' keyword followed by the class name.
    Class names in Python conventionally use CamelCase.
    """
    
    # ============================================================================
    # 3. CLASS ATTRIBUTES (vs INSTANCE ATTRIBUTES)
    # ============================================================================
    """
    CLASS ATTRIBUTE: Shared by all instances of the class.
    Defined directly under the class, outside any method.
    """
    vehicle_count = 0  # Class attribute - tracks total vehicles created
    manufacturer = "Generic Motors"  # Class attribute
    
    def __init__(self, make, model, year):
        """
        ============================================================================
        4. __INIT__ METHOD (Constructor/Magic/Dunder Method)
        ============================================================================
        __init__ is a special "magic" or "dunder" (double underscore) method.
        It's automatically called when a new object is created.
        Used to initialize instance attributes.
        
        'self' refers to the instance being created.
        It must be the first parameter of instance methods.
        """
        
        # ============================================================================
        # 5. INSTANCE ATTRIBUTES
        # ============================================================================
        """
        INSTANCE ATTRIBUTES: Specific to each object/instance.
        Defined inside __init__ using self.attribute_name
        Each object has its own copy of instance attributes.
        """
        self.make = make      # Instance attribute
        self.model = model    # Instance attribute  
        self.year = year      # Instance attribute
        self.mileage = 0      # Instance attribute with default value
        
        # Increment class attribute when new instance is created
        Vehicle.vehicle_count += 1
        
        # Instance attribute that's not from parameters
        self.vehicle_id = f"V{Vehicle.vehicle_count:04d}"
    
    # ============================================================================
    # 6. INSTANCE METHODS
    # ============================================================================
    """
    INSTANCE METHODS: Functions defined inside a class that operate on instances.
    First parameter must be 'self' (refers to the instance calling the method).
    """
    def drive(self, miles):
        """
        Instance method that updates the vehicle's mileage.
        Can access and modify instance attributes using self.
        """
        self.mileage += miles
        print(f"{self.make} {self.model} driven {miles} miles. Total: {self.mileage}")
    
    def get_info(self):
        """
        Instance method that returns formatted vehicle information.
        """
        return f"{self.year} {self.make} {self.model} (ID: {self.vehicle_id})"
    
    # ============================================================================
    # 7. CLASS METHODS
    # ============================================================================
    """
    CLASS METHODS: Methods that operate on the class itself, not instances.
    Decorated with @classmethod.
    First parameter is 'cls' (refers to the class, not instance).
    Can modify class attributes.
    """
    @classmethod
    def get_vehicle_count(cls):
        """
        Class method to get the total number of vehicles created.
        """
        return cls.vehicle_count
    
    @classmethod
    def create_from_string(cls, vehicle_string):
        """
        Alternative constructor - creates Vehicle from formatted string.
        This is a common use of class methods.
        """
        make, model, year = vehicle_string.split(",")
        return cls(make.strip(), model.strip(), int(year.strip()))
    
    # ============================================================================
    # 8. STATIC METHODS
    # ============================================================================
    """
    STATIC METHODS: Methods that don't operate on instance or class.
    Decorated with @staticmethod.
    No 'self' or 'cls' parameter.
    Used for utility functions related to the class.
    """
    @staticmethod
    def is_valid_year(year):
        """
        Static method to check if a year is valid for a vehicle.
        Doesn't need access to instance or class attributes.
        """
        current_year = 2024
        return 1886 <= year <= current_year  # First car was invented in 1886
    
    # ============================================================================
    # 9. PROPERTIES (GETTERS, SETTERS, DELETERS)
    # ============================================================================
    """
    PROPERTIES: Allow controlled access to attributes.
    Use @property decorator for getters, @attribute.setter for setters.
    Enables encapsulation and data validation.
    """
    
    @property
    def age(self):
        """
        Property (getter) - calculates vehicle age.
        Accessed like an attribute: vehicle.age (not vehicle.age())
        """
        current_year = 2024
        return current_year - self.year
    
    @property  
    def description(self):
        """
        Another property - returns formatted description.
        """
        return f"{self.make} {self.model} from {self.year}"
    
    @description.setter
    def description(self, desc_string):
        """
        Setter for description property.
        Allows setting multiple attributes from a single string.
        Called when: vehicle.description = "Toyota, Camry, 2020"
        """
        make, model, year = desc_string.split(",")
        self.make = make.strip()
        self.model = model.strip()
        self.year = int(year.strip())
    
    @description.deleter
    def description(self):
        """
        Deleter for description property.
        Called when: del vehicle.description
        """
        print(f"Description for {self.vehicle_id} reset")
        self.make = "Unknown"
        self.model = "Unknown"
        self.year = 1900
    
    # ============================================================================
    # 10. MAGIC/DUNDER METHODS (continued)
    # ============================================================================
    
    def __str__(self):
        """
        __str__: Returns human-readable string representation.
        Called by str(object), print(object), and f"{object}".
        """
        return f"{self.year} {self.make} {self.model} with {self.mileage} miles"
    
    def __repr__(self):
        """
        __repr__: Returns unambiguous string representation for debugging.
        Should look like a valid Python expression to recreate the object.
        Called by repr(object) and in interactive console.
        """
        return f"Vehicle('{self.make}', '{self.model}', {self.year})"
    
    def __len__(self):
        """
        __len__: Allows len(object) to work on Vehicle instances.
        Returns vehicle age in this implementation.
        """
        return self.age
    
    def __add__(self, other):
        """
        __add__: Defines behavior for + operator.
        Here, combining two vehicles creates a "fleet" tuple.
        """
        if isinstance(other, Vehicle):
            return (self, other)
        return NotImplemented

# ============================================================================
# 11. INHERITANCE
# ============================================================================
"""
INHERITANCE: Creating a new class based on an existing class.
New class (child/subclass) inherits attributes and methods from parent class.
Allows code reuse and specialization.
"""

class Car(Vehicle):
    """
    Car class inherits from Vehicle class.
    Car is a subclass/child class of Vehicle.
    Vehicle is the superclass/parent class of Car.
    """
    
    def __init__(self, make, model, year, doors=4):
        """
        Child class constructor.
        First call parent constructor using super().__init__()
        Then initialize child-specific attributes.
        """
        super().__init__(make, model, year)  # Call parent constructor
        self.doors = doors  # Car-specific attribute
        self.windows_up = True
    
    # ============================================================================
    # 12. METHOD OVERRIDING (Simple Polymorphism)
    # ============================================================================
    """
    POLYMORPHISM: Objects of different classes can be used interchangeably.
    METHOD OVERRIDING: Child class provides its own implementation of a method
    defined in the parent class.
    """
    
    def drive(self, miles):
        """
        Override parent's drive method to add car-specific behavior.
        This demonstrates polymorphism - same method name, different behavior.
        """
        if not self.windows_up:
            print("Windows are down - enjoy the breeze!")
        
        # Call parent method using super()
        super().drive(miles)
        
        # Car-specific behavior
        if miles > 100:
            print("Long drive! Consider checking oil and tire pressure.")
    
    def toggle_windows(self):
        """
        Car-specific method not available in Vehicle class.
        """
        self.windows_up = not self.windows_up
        status = "up" if self.windows_up else "down"
        print(f"Windows are now {status}")
    
    def __str__(self):
        """
        Override __str__ to include car-specific information.
        """
        base_str = super().__str__()
        return f"{base_str}, {self.doors} doors"

class Motorcycle(Vehicle):
    """
    Another child class demonstrating inheritance with different specialization.
    """
    
    def __init__(self, make, model, year, has_sidecar=False):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar
        self.helmet_included = True
    
    def drive(self, miles):
        """
        Different implementation of drive method for Motorcycle.
        Demonstrates polymorphism - same method name, different implementation.
        """
        if not self.helmet_included:
            print("Warning: No helmet! Drive safely.")
        
        super().drive(miles)
        
        if miles > 50 and not self.has_sidecar:
            print("Long ride on a motorcycle! Take breaks.")

# ============================================================================
# DEMONSTRATION AND TESTING
# ============================================================================

def demonstrate_oop_concepts():
    """Demonstrate all the OOP concepts with practical examples."""
    
    print("=" * 60)
    print("OBJECT-ORIENTED PROGRAMMING DEMONSTRATION")
    print("=" * 60)
    
    # ============================================================================
    # Creating objects (instances)
    # ============================================================================
    print("\n1. CREATING OBJECTS (INSTANCES)")
    print("-" * 40)
    
    # Create Vehicle instances
    vehicle1 = Vehicle("Toyota", "Camry", 2020)
    vehicle2 = Vehicle("Honda", "Civic", 2022)
    
    print(f"Vehicle 1 created: {vehicle1}")
    print(f"Vehicle 2 created: {vehicle2}")
    
    # ============================================================================
    # Accessing attributes
    # ============================================================================
    print("\n2. ACCESSING ATTRIBUTES")
    print("-" * 40)
    
    print(f"Vehicle 1 make (instance attribute): {vehicle1.make}")
    print(f"Vehicle 2 model (instance attribute): {vehicle2.model}")
    print(f"Manufacturer (class attribute): {Vehicle.manufacturer}")
    print(f"Same class attr via instance: {vehicle1.manufacturer}")
    
    # ============================================================================
    # Calling methods
    # ============================================================================
    print("\n3. CALLING METHODS")
    print("-" * 40)
    
    vehicle1.drive(150)
    vehicle1.drive(85)
    vehicle2.drive(50)
    
    print(f"\nVehicle 1 info: {vehicle1.get_info()}")
    print(f"Vehicle 2 info: {vehicle2.get_info()}")
    
    # ============================================================================
    # Class and Static methods
    # ============================================================================
    print("\n4. CLASS AND STATIC METHODS")
    print("-" * 40)
    
    print(f"Total vehicles created: {Vehicle.get_vehicle_count()}")
    print(f"Is 2025 a valid year? {Vehicle.is_valid_year(2025)}")
    print(f"Is 1995 a valid year? {Vehicle.is_valid_year(1995)}")
    
    # Alternative constructor using class method
    vehicle3 = Vehicle.create_from_string("Ford, Mustang, 2021")
    print(f"Vehicle 3 from string: {vehicle3}")
    
    # ============================================================================
    # Properties
    # ============================================================================
    print("\n5. PROPERTIES")
    print("-" * 40)
    
    print(f"Vehicle 1 age (property): {vehicle1.age} years")
    print(f"Vehicle 1 description: {vehicle1.description}")
    
    # Using setter
    vehicle1.description = "Toyota, Avalon, 2019"
    print(f"After setter - Vehicle 1: {vehicle1}")
    print(f"Updated age: {vehicle1.age} years")
    
    # Using deleter
    del vehicle1.description
    print(f"After deleter - Vehicle 1 make: {vehicle1.make}")
    
    # ============================================================================
    # Magic/Dunder methods
    # ============================================================================
    print("\n6. MAGIC/DUNDER METHODS")
    print("-" * 40)
    
    print(f"str(vehicle2): {str(vehicle2)}")
    print(f"repr(vehicle2): {repr(vehicle2)}")
    print(f"len(vehicle2): {len(vehicle2)}")  # Uses __len__
    
    # Using __add__ magic method
    fleet = vehicle2 + vehicle3
    print(f"Vehicle fleet (vehicle2 + vehicle3): {fleet}")
    
    # ============================================================================
    # Inheritance and Polymorphism
    # ============================================================================
    print("\n7. INHERITANCE AND POLYMORPHISM")
    print("-" * 40)
    
    # Create instances of child classes
    car = Car("Tesla", "Model 3", 2023, 4)
    motorcycle = Motorcycle("Harley", "Sportster", 2022)
    
    print(f"Car instance: {car}")
    print(f"Motorcycle instance: {motorcycle}")
    
    # Access inherited attributes
    print(f"Car manufacturer (inherited): {car.manufacturer}")
    print(f"Car mileage (inherited): {car.mileage}")
    
    # Call overridden methods (polymorphism in action)
    print("\nPolymorphism demonstration - same method, different behaviors:")
    
    vehicles = [vehicle1, car, motorcycle]
    
    for i, veh in enumerate(vehicles, 1):
        print(f"\nVehicle {i} ({type(veh).__name__}) driving:")
        veh.drive(75)
    
    # Child-specific methods
    print("\nChild-specific methods:")
    car.toggle_windows()
    car.drive(120)
    
    # ============================================================================
    # Type checking and isinstance
    # ============================================================================
    print("\n8. TYPE CHECKING")
    print("-" * 40)
    
    print(f"car is instance of Car: {isinstance(car, Car)}")
    print(f"car is instance of Vehicle: {isinstance(car, Vehicle)}")
    print(f"car is instance of Motorcycle: {isinstance(car, Motorcycle)}")
    print(f"Vehicle is subclass of Car: {issubclass(Vehicle, Car)}")
    print(f"Car is subclass of Vehicle: {issubclass(Car, Vehicle)}")
    
    # ============================================================================
    # Class attribute demonstration
    # ============================================================================
    print("\n9. CLASS VS INSTANCE ATTRIBUTES")
    print("-" * 40)
    
    print(f"Vehicle.vehicle_count (class): {Vehicle.vehicle_count}")
    print(f"car.vehicle_count (via instance): {car.vehicle_count}")
    
    # Modify class attribute through class
    Vehicle.manufacturer = "Global Motors"
    print(f"\nAfter changing Vehicle.manufacturer:")
    print(f"Vehicle.manufacturer: {Vehicle.manufacturer}")
    print(f"car.manufacturer: {car.manufacturer}")
    print(f"motorcycle.manufacturer: {motorcycle.manufacturer}")
    
    # Warning: Modifying class attribute through instance creates instance attribute!
    car.manufacturer = "Tesla Motors"
    print(f"\nAfter car.manufacturer = 'Tesla Motors':")
    print(f"car.manufacturer: {car.manufacturer}")
    print(f"Vehicle.manufacturer: {Vehicle.manufacturer}")
    print(f"motorcycle.manufacturer: {motorcycle.manufacturer}")
    
    # Check __dict__ to see instance namespace
    print(f"\ncar.__dict__: {car.__dict__}")
    
    # ============================================================================
    # Final summary
    # ============================================================================
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"Total vehicles of all types created: {Vehicle.vehicle_count}")
    print("\nAll vehicle descriptions:")
    all_vehicles = [vehicle1, vehicle2, vehicle3, car, motorcycle]
    for veh in all_vehicles:
        print(f"  - {veh}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    """
    This block runs when the script is executed directly.
    It demonstrates all OOP concepts with clear output.
    """
    demonstrate_oop_concepts()
    
    print("\n" + "=" * 60)
    print("QUICK REFERENCE OF CONCEPTS DEMONSTRATED:")
    print("=" * 60)
    print("""
    1. Classes and Objects
    2. __init__ method (constructor)
    3. Instance attributes (self.attribute)
    4. Class attributes (shared across instances)
    5. Instance methods (def method(self, ...))
    6. Class methods (@classmethod, cls parameter)
    7. Static methods (@staticmethod, no self/cls)
    8. Properties (@property, @attr.setter, @attr.deleter)
    9. Magic/Dunder methods (__str__, __repr__, __len__, __add__)
    10. Inheritance (class Child(Parent):)
    11. Method overriding and Polymorphism
    12. super() for calling parent methods
    13. isinstance() and issubclass() functions
    14. Instance vs class namespace (__dict__)
    """)