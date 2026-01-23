"""
COMPREHENSIVE PYTHON DESIGN PRINCIPLES & PATTERNS
==================================================
This single, comprehensive code block demonstrates:
1. Design Principles: Separation of Concerns, SOLID, Dependency Injection
2. Common Patterns: Factory, Strategy, Adapter, Repository, Singleton, Observer
"""

print("=" * 70)
print("PYTHON DESIGN PRINCIPLES & PATTERNS DEMONSTRATION")
print("=" * 70)

# ============================================================================
# PART 1: DESIGN PRINCIPLES
# ============================================================================

print("\n" + "=" * 30)
print("DESIGN PRINCIPLES")
print("=" * 30)

# ----------------------------------------------------------------------------
# 1. SEPARATION OF CONCERNS (SoC)
# ----------------------------------------------------------------------------
print("\n--- SEPARATION OF CONCERNS ---")

class DataStorage:
    """Concern: ONLY handles data persistence"""
    def __init__(self):
        self._data = {}
    
    def save(self, key, value):
        print(f"  [DataStorage] Saving {key}: {value}")
        self._data[key] = value
        return True
    
    def load(self, key):
        print(f"  [DataStorage] Loading {key}")
        return self._data.get(key)

class BusinessLogic:
    """Concern: ONLY handles business rules"""
    def __init__(self, storage):
        # Dependency for data handling (loose coupling)
        self.storage = storage
    
    def apply_discount(self, order_id, amount):
        print(f"  [BusinessLogic] Processing order {order_id}")
        # Business rule: 10% discount for orders > $100
        if amount > 100:
            discount = amount * 0.1
            amount -= discount
            print(f"  [BusinessLogic] Applied 10% discount: ${discount:.2f}")
        return amount

class UserInterface:
    """Concern: ONLY handles presentation"""
    def __init__(self, logic):
        self.logic = logic
    
    def display_order(self, order_id, amount):
        print(f"  [UserInterface] Displaying order {order_id}")
        final_amount = self.logic.apply_discount(order_id, amount)
        print(f"  [UserInterface] Final amount: ${final_amount:.2f}")

# Demonstrate Separation of Concerns
storage = DataStorage()
logic = BusinessLogic(storage)
ui = UserInterface(logic)
ui.display_order("ORD123", 150.00)

# ----------------------------------------------------------------------------
# 2. SOLID PRINCIPLES (Practical Examples)
# ----------------------------------------------------------------------------
print("\n--- SOLID PRINCIPLES ---")

# S: SINGLE RESPONSIBILITY PRINCIPLE
class InvoiceCalculator:
    """SRP Example: Only calculates invoice totals"""
    def calculate_total(self, items):
        return sum(item['price'] * item['quantity'] for item in items)

class InvoicePrinter:
    """SRP Example: Only prints invoices"""
    def print_invoice(self, customer, total):
        print(f"  [InvoicePrinter] Invoice for {customer}: ${total:.2f}")

# O: OPEN/CLOSED PRINCIPLE
print("\n  Open/Closed Principle:")
class PaymentProcessor:
    """Open for extension, closed for modification"""
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"    Processing ${amount:.2f} via Credit Card")
        return True

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"    Processing ${amount:.2f} via PayPal")
        return True

# L: LISKOV SUBSTITUTION PRINCIPLE
print("\n  Liskov Substitution Principle:")
class Bird:
    def make_sound(self):
        return "Chirp"

class FlyingBird(Bird):
    def fly(self):
        return "Flying"

class Sparrow(FlyingBird):
    pass  # Can substitute FlyingBird anywhere

class Penguin(Bird):
    pass  # Can substitute Bird but not FlyingBird

# I: INTERFACE SEGREGATION PRINCIPLE
print("\n  Interface Segregation Principle:")
class Printer:
    def print_doc(self, document):
        pass

class Scanner:
    def scan_doc(self):
        pass

class MultiFunctionDevice(Printer, Scanner):
    """Segregated interfaces instead of one large interface"""
    def print_doc(self, document):
        print(f"    Printing: {document}")
    
    def scan_doc(self):
        print("    Scanning document")
        return "Scanned content"

# D: DEPENDENCY INVERSION PRINCIPLE
print("\n  Dependency Inversion Principle:")
class Database:
    """High-level module"""
    def __init__(self, connection):
        # Depends on abstraction (connection interface)
        self.connection = connection
    
    def query(self, sql):
        return self.connection.execute(sql)

class PostgreSQLConnection:
    """Low-level module implementing abstraction"""
    def execute(self, sql):
        print(f"    PostgreSQL executing: {sql}")
        return [{"id": 1, "name": "John"}]

# ----------------------------------------------------------------------------
# 3. DEPENDENCY INJECTION (Conceptual)
# ----------------------------------------------------------------------------
print("\n--- DEPENDENCY INJECTION ---")

class EmailService:
    def send_email(self, to, message):
        print(f"  [EmailService] Sending email to {to}: {message}")

class NotificationService:
    def __init__(self, email_service):
        # Dependency INJECTED via constructor
        self.email_service = email_service
    
    def notify(self, user, message):
        print(f"  [NotificationService] Notifying {user}")
        # Use injected dependency
        self.email_service.send_email(user, message)

# Manual Dependency Injection
email_service = EmailService()
notification = NotificationService(email_service)  # Dependency injected
notification.notify("user@example.com", "Your order shipped!")

# ============================================================================
# PART 2: COMMON PATTERNS
# ============================================================================

print("\n" + "=" * 30)
print("DESIGN PATTERNS")
print("=" * 30)

# ----------------------------------------------------------------------------
# 1. FACTORY PATTERN
# ----------------------------------------------------------------------------
print("\n--- FACTORY PATTERN ---")

class Vehicle:
    def drive(self):
        pass

class Car(Vehicle):
    def drive(self):
        return "Driving a car"

class Truck(Vehicle):
    def drive(self):
        return "Driving a truck"

class VehicleFactory:
    """Factory creates objects without exposing instantiation logic"""
    @staticmethod
    def create_vehicle(vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "truck":
            return Truck()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# Use Factory
factory = VehicleFactory()
car = factory.create_vehicle("car")
print(f"  Factory created: {car.drive()}")

# ----------------------------------------------------------------------------
# 2. STRATEGY PATTERN
# ----------------------------------------------------------------------------
print("\n--- STRATEGY PATTERN ---")

class CompressionStrategy:
    """Strategy interface"""
    def compress(self, data):
        pass

class ZIPStrategy(CompressionStrategy):
    def compress(self, data):
        print(f"  Compressing {data} using ZIP")
        return f"{data}.zip"

class RARStrategy(CompressionStrategy):
    def compress(self, data):
        print(f"  Compressing {data} using RAR")
        return f"{data}.rar"

class Compressor:
    """Context class using strategy"""
    def __init__(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def execute_compression(self, data):
        return self.strategy.compress(data)

# Use Strategy Pattern
compressor = Compressor(ZIPStrategy())
result1 = compressor.execute_compression("datafile")
compressor.set_strategy(RARStrategy())
result2 = compressor.execute_compression("datafile")

# ----------------------------------------------------------------------------
# 3. ADAPTER PATTERN
# ----------------------------------------------------------------------------
print("\n--- ADAPTER PATTERN ---")

class LegacyPaymentSystem:
    """Legacy system with incompatible interface"""
    def make_payment(self, dollars):
        print(f"  [Legacy] Processing payment of ${dollars}")
        return True

class ModernPaymentSystem:
    """Modern system expecting different interface"""
    def process_payment(self, amount, currency="USD"):
        print(f"  [Modern] Processing {currency} {amount}")
        return True

class PaymentAdapter:
    """Adapter makes legacy system compatible with modern interface"""
    def __init__(self, legacy_system):
        self.legacy_system = legacy_system
    
    def process_payment(self, amount, currency="USD"):
        # Convert and adapt the interface
        if currency != "USD":
            # Simple conversion for demo
            amount = amount * 0.85  # USD to EUR approx
        return self.legacy_system.make_payment(amount)

# Use Adapter
legacy = LegacyPaymentSystem()
adapter = PaymentAdapter(legacy)
adapter.process_payment(100, "EUR")

# ----------------------------------------------------------------------------
# 4. REPOSITORY PATTERN
# ----------------------------------------------------------------------------
print("\n--- REPOSITORY PATTERN ---")

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserRepository:
    """Repository abstracts data access logic"""
    def __init__(self):
        self._users = {}
        self._next_id = 1
    
    def add(self, user):
        user.id = self._next_id
        self._users[user.id] = user
        self._next_id += 1
        print(f"  [Repository] Added user: {user.name}")
        return user.id
    
    def get(self, user_id):
        user = self._users.get(user_id)
        print(f"  [Repository] Retrieved user ID {user_id}")
        return user
    
    def get_all(self):
        return list(self._users.values())
    
    def delete(self, user_id):
        if user_id in self._users:
            del self._users[user_id]
            print(f"  [Repository] Deleted user ID {user_id}")
            return True
        return False

# Use Repository
repo = UserRepository()
user1 = User(None, "Alice", "alice@example.com")
user2 = User(None, "Bob", "bob@example.com")
repo.add(user1)
repo.add(user2)
retrieved = repo.get(1)

# ----------------------------------------------------------------------------
# 5. SINGLETON PATTERN
# ----------------------------------------------------------------------------
print("\n--- SINGLETON PATTERN ---")

class AppConfig:
    """Singleton ensuring single configuration instance"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("  Creating new AppConfig instance")
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.settings = {}
            self._initialized = True
    
    def set_setting(self, key, value):
        self.settings[key] = value
    
    def get_setting(self, key):
        return self.settings.get(key)

# Demonstrate Singleton
config1 = AppConfig()
config1.set_setting("theme", "dark")
config2 = AppConfig()
print(f"  Same instance? {config1 is config2}")
print(f"  Config2 theme: {config2.get_setting('theme')}")

# ----------------------------------------------------------------------------
# 6. OBSERVER PATTERN
# ----------------------------------------------------------------------------
print("\n--- OBSERVER PATTERN ---")

class NewsPublisher:
    """Subject being observed"""
    def __init__(self):
        self._subscribers = []
        self._latest_news = None
    
    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)
    
    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)
    
    def publish_news(self, news):
        print(f"\n  [Publisher] Publishing: {news}")
        self._latest_news = news
        self._notify_subscribers()
    
    def _notify_subscribers(self):
        for subscriber in self._subscribers:
            subscriber.update(self._latest_news)

class NewsSubscriber:
    """Observer"""
    def __init__(self, name):
        self.name = name
    
    def update(self, news):
        print(f"  [{self.name}] Received news: {news}")

# Use Observer Pattern
publisher = NewsPublisher()
subscriber1 = NewsSubscriber("Subscriber A")
subscriber2 = NewsSubscriber("Subscriber B")

publisher.subscribe(subscriber1)
publisher.subscribe(subscriber2)
publisher.publish_news("Python 3.12 released!")
publisher.unsubscribe(subscriber1)
publisher.publish_news("New AI framework announced")

# ----------------------------------------------------------------------------
# 7. COMBINED EXAMPLE: Strategy + Factory + Dependency Injection
# ----------------------------------------------------------------------------
print("\n--- COMBINED PATTERN EXAMPLE ---")

# Strategy Interface
class ShippingStrategy:
    def calculate_cost(self, weight, distance):
        pass

# Concrete Strategies
class StandardShipping(ShippingStrategy):
    def calculate_cost(self, weight, distance):
        return weight * 0.5 + distance * 0.1

class ExpressShipping(ShippingStrategy):
    def calculate_cost(self, weight, distance):
        return weight * 1.0 + distance * 0.3

class OvernightShipping(ShippingStrategy):
    def calculate_cost(self, weight, distance):
        return weight * 2.0 + distance * 0.5

# Strategy Factory
class ShippingStrategyFactory:
    @staticmethod
    def create_strategy(shipping_type):
        strategies = {
            "standard": StandardShipping,
            "express": ExpressShipping,
            "overnight": OvernightShipping
        }
        strategy_class = strategies.get(shipping_type.lower())
        if not strategy_class:
            raise ValueError(f"Unknown shipping type: {shipping_type}")
        return strategy_class()

# Context using Dependency Injection
class ShippingCalculator:
    def __init__(self, strategy_factory):
        # Dependency injection of factory
        self.strategy_factory = strategy_factory
        self.current_strategy = None
    
    def calculate_shipping(self, shipping_type, weight, distance):
        # Use factory to create strategy
        self.current_strategy = self.strategy_factory.create_strategy(shipping_type)
        cost = self.current_strategy.calculate_cost(weight, distance)
        print(f"  {shipping_type.capitalize()} shipping cost for {weight}kg, {distance}km: ${cost:.2f}")
        return cost

# Usage
factory = ShippingStrategyFactory()
calculator = ShippingCalculator(factory)  # Dependency injection
calculator.calculate_shipping("standard", 5, 100)
calculator.calculate_shipping("express", 5, 100)

# ============================================================================
# SUMMARY & USAGE EXAMPLE
# ============================================================================

print("\n" + "=" * 70)
print("SUMMARY: COMPLETE E-COMMERCE EXAMPLE USING MULTIPLE PATTERNS")
print("=" * 70)

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class ProductRepository:
    """Repository Pattern"""
    def __init__(self):
        self.products = {}
    
    def add(self, product):
        self.products[product.id] = product
    
    def find(self, product_id):
        return self.products.get(product_id)

class PricingStrategy:
    """Strategy Pattern"""
    def calculate_price(self, base_price):
        pass

class RegularPricing(PricingStrategy):
    def calculate_price(self, base_price):
        return base_price

class SalePricing(PricingStrategy):
    def calculate_price(self, base_price):
        return base_price * 0.8  # 20% off

class Cart:
    """Uses multiple patterns"""
    def __init__(self, product_repo, pricing_strategy):
        # Dependency Injection
        self.product_repo = product_repo
        self.pricing_strategy = pricing_strategy
        self.items = []
    
    def add_item(self, product_id):
        product = self.product_repo.find(product_id)
        if product:
            self.items.append(product)
            print(f"Added {product.name} to cart")
    
    def calculate_total(self):
        total = sum(self.pricing_strategy.calculate_price(p.price) 
                   for p in self.items)
        return total

# Setup and use
product_repo = ProductRepository()
product_repo.add(Product(1, "Laptop", 999.99))
product_repo.add(Product(2, "Mouse", 29.99))

# Factory method for pricing strategy
def get_pricing_strategy(strategy_type):
    """Factory Pattern"""
    if strategy_type == "sale":
        return SalePricing()
    return RegularPricing()

# Create cart with injected dependencies
cart = Cart(product_repo, get_pricing_strategy("sale"))
cart.add_item(1)
cart.add_item(2)
print(f"\nTotal with sale pricing: ${cart.calculate_total():.2f}")

print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
print("\nKey Concepts Demonstrated:")
print("1. Separation of Concerns: Different classes handle different concerns")
print("2. SOLID Principles: Five principles with practical examples")
print("3. Dependency Injection: Passing dependencies externally")
print("4. Factory Pattern: Object creation abstraction")
print("5. Strategy Pattern: Interchangeable algorithms")
print("6. Adapter Pattern: Interface compatibility")
print("7. Repository Pattern: Data access abstraction")
print("8. Singleton Pattern: Single instance guarantee")
print("9. Observer Pattern: Publish-subscribe mechanism")
print("10. Combined Patterns: Real-world integration")
print("=" * 70)