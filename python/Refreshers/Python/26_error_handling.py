"""
COMPREHENSIVE ERROR HANDLING STRATEGIES IN PYTHON
==================================================
This code demonstrates different error handling approaches:
1. Where to catch exceptions (different layers)
2. Fail-fast strategy
3. Graceful degradation strategy
4. Error recovery patterns
"""

print("=" * 70)
print("ERROR HANDLING STRATEGIES DEMONSTRATION")
print("=" * 70)

# ============================================================================
# PART 1: WHERE TO CATCH EXCEPTIONS (ARCHITECTURAL LAYERS)
# ============================================================================

print("\n" + "=" * 30)
print("WHERE TO CATCH EXCEPTIONS")
print("=" * 30)

class DataAccessLayer:
    """
    LAYER 1: DATA ACCESS LAYER
    - Catches database/specific technical errors
    - Converts them to domain-specific exceptions
    - Never exposes raw database errors to business logic
    """
    
    def __init__(self):
        # Simulating database connection
        self.connected = True
        self.data = {
            "users": {
                1: {"id": 1, "name": "Alice", "balance": 1000},
                2: {"id": 2, "name": "Bob", "balance": 500}
            }
        }
    
    def get_user(self, user_id):
        """Database-level error handling"""
        print(f"\n[DataAccessLayer] Fetching user {user_id}")
        
        try:
            # Simulate database errors
            if not self.connected:
                raise ConnectionError("Database connection failed")
            
            if user_id <= 0:
                raise ValueError(f"Invalid user ID: {user_id}")
            
            user = self.data["users"].get(user_id)
            if not user:
                # Raise specific exception instead of returning None
                raise KeyError(f"User {user_id} not found in database")
            
            return user
            
        except ConnectionError as e:
            # Log technical error here
            print(f"  [DataAccessLayer] Database error: {e}")
            # Re-raise as domain-specific exception
            raise DataAccessError(f"Failed to access user data: {e}")
        except (ValueError, KeyError) as e:
            # These are also domain errors, but more specific
            print(f"  [DataAccessLayer] Data validation error: {e}")
            raise NotFoundError(f"User not found: {e}")


class BusinessLogicLayer:
    """
    LAYER 2: BUSINESS LOGIC LAYER
    - Handles business rule violations
    - Transforms technical errors into business errors
    - May catch specific exceptions for business logic
    """
    
    def __init__(self, data_access):
        self.data_access = data_access
    
    def transfer_money(self, from_user_id, to_user_id, amount):
        """Business logic with error handling"""
        print(f"\n[BusinessLogicLayer] Transferring ${amount} from {from_user_id} to {to_user_id}")
        
        try:
            # Get users with proper error handling
            from_user = self.data_access.get_user(from_user_id)
            to_user = self.data_access.get_user(to_user_id)
            
            # Business rule validation
            if amount <= 0:
                raise BusinessRuleError("Transfer amount must be positive")
            
            if from_user["balance"] < amount:
                raise BusinessRuleError(f"Insufficient funds: ${from_user['balance']} available")
            
            # Simulate transfer
            print(f"  [BusinessLogicLayer] Transfer successful")
            return {
                "from_balance": from_user["balance"] - amount,
                "to_balance": to_user["balance"] + amount
            }
            
        except NotFoundError as e:
            # Re-raise with business context
            raise BusinessRuleError(f"Cannot complete transfer: {e}")
        except DataAccessError as e:
            # Technical error becomes business error
            raise BusinessRuleError(f"Service temporarily unavailable. Please try again later.")


class PresentationLayer:
    """
    LAYER 3: PRESENTATION/API LAYER
    - Catches ALL unhandled exceptions
    - Returns user-friendly error messages
    - Logs errors for debugging
    - Never crashes the application
    """
    
    def __init__(self, business_logic):
        self.business_logic = business_logic
    
    def handle_transfer_request(self, from_id, to_id, amount):
        """Presentation layer - final error boundary"""
        print(f"\n[PresentationLayer] Handling transfer request")
        
        try:
            result = self.business_logic.transfer_money(from_id, to_id, amount)
            return {
                "success": True,
                "message": "Transfer completed successfully",
                "data": result
            }
            
        except BusinessRuleError as e:
            # User-friendly business error messages
            return {
                "success": False,
                "message": f"Transfer failed: {str(e)}",
                "error_type": "business_error"
            }
        except Exception as e:
            # Catch-all for unexpected errors
            # Log full error for debugging
            print(f"  [ERROR LOG] Unexpected error: {type(e).__name__}: {e}")
            
            return {
                "success": False,
                "message": "An unexpected error occurred. Our team has been notified.",
                "error_type": "system_error"
            }


# Custom exception hierarchy
class ApplicationError(Exception):
    """Base exception for all application errors"""
    pass

class DataAccessError(ApplicationError):
    """Errors related to data access"""
    pass

class NotFoundError(DataAccessError):
    """Resource not found"""
    pass

class BusinessRuleError(ApplicationError):
    """Business rule violations"""
    pass


# Demonstration of layered error handling
print("\n--- Layered Error Handling Example ---")

# Setup layers
data_layer = DataAccessLayer()
business_layer = BusinessLogicLayer(data_layer)
presentation = PresentationLayer(business_layer)

# Test scenarios
print("\n1. Normal successful transfer:")
response = presentation.handle_transfer_request(1, 2, 100)
print(f"   Response: {response}")

print("\n2. Business rule violation (insufficient funds):")
response = presentation.handle_transfer_request(2, 1, 1000)
print(f"   Response: {response}")

print("\n3. User not found:")
response = presentation.handle_transfer_request(99, 1, 100)
print(f"   Response: {response}")


# ============================================================================
# PART 2: FAIL-FAST STRATEGY
# ============================================================================

print("\n" + "=" * 30)
print("FAIL-FAST STRATEGY")
print("=" * 30)
print("""
Fail-Fast Philosophy:
- Detect errors as early as possible
- Fail immediately when invalid state detected
- Don't continue with potentially corrupt data
- Makes debugging easier
""")

class PaymentProcessorFailFast:
    """Fail-fast implementation"""
    
    def __init__(self, config):
        # Validate configuration immediately
        if not config.get("api_key"):
            raise ValueError("API key is required")  # Fail fast!
        
        if config.get("timeout", 0) <= 0:
            raise ValueError("Timeout must be positive")
        
        self.config = config
        print(f"[PaymentProcessor] Initialized with timeout: {config['timeout']}s")
    
    def validate_payment(self, payment_data):
        """Validate all inputs before processing"""
        print(f"\n[FailFast] Validating payment: {payment_data.get('id')}")
        
        # Check all conditions first
        errors = []
        
        # 1. Validate payment ID
        if not payment_data.get("id"):
            errors.append("Payment ID is required")
        
        # 2. Validate amount
        amount = payment_data.get("amount", 0)
        if amount <= 0:
            errors.append("Amount must be positive")
        
        # 3. Validate currency
        if payment_data.get("currency") not in ["USD", "EUR", "GBP"]:
            errors.append(f"Invalid currency: {payment_data.get('currency')}")
        
        # 4. Validate card number (simplified)
        card = payment_data.get("card_number", "")
        if not card or len(card) < 16:
            errors.append("Invalid card number")
        
        # FAIL FAST: If any errors, stop immediately
        if errors:
            error_msg = "; ".join(errors)
            raise ValueError(f"Payment validation failed: {error_msg}")
        
        # Only proceed if everything is valid
        print("  [FailFast] All validations passed, processing payment...")
        return self._process_payment(payment_data)
    
    def _process_payment(self, payment_data):
        """Internal processing (only called if validation passes)"""
        # Simulate processing
        return {
            "success": True,
            "transaction_id": f"TXN{payment_data['id']}",
            "amount": payment_data["amount"]
        }


print("\n--- Fail-Fast Examples ---")

# Example 1: Valid configuration
try:
    config = {"api_key": "secret123", "timeout": 30}
    processor = PaymentProcessorFailFast(config)
    
    valid_payment = {
        "id": "PAY001",
        "amount": 99.99,
        "currency": "USD",
        "card_number": "4111111111111111"
    }
    result = processor.validate_payment(valid_payment)
    print(f"Success: {result}")
    
except ValueError as e:
    print(f"Failed fast: {e}")

# Example 2: Invalid payment (fail fast)
print("\nTrying invalid payment:")
try:
    invalid_payment = {
        "id": "",
        "amount": -10,
        "currency": "XYZ",
        "card_number": "123"
    }
    result = processor.validate_payment(invalid_payment)
    print(f"Success: {result}")
except ValueError as e:
    print(f"Failed fast: {e}")

# Example 3: Defensive programming with assertions
print("\n--- Defensive Programming (Assertions) ---")

class ShoppingCart:
    """Using assertions for fail-fast during development"""
    
    def __init__(self):
        self.items = []
        self._total = 0.0
    
    def add_item(self, name, price, quantity=1):
        # Assertions for development/debugging (can be disabled in production)
        assert price >= 0, f"Price cannot be negative: {price}"
        assert quantity > 0, f"Quantity must be positive: {quantity}"
        assert isinstance(name, str) and name, "Item name must be a non-empty string"
        
        self.items.append({"name": name, "price": price, "quantity": quantity})
        self._recalculate_total()
    
    def _recalculate_total(self):
        # Internal consistency check
        calculated = sum(item["price"] * item["quantity"] for item in self.items)
        
        # Assert that our internal state is consistent
        assert calculated >= 0, f"Negative total calculated: {calculated}"
        
        self._total = calculated
    
    def get_total(self):
        # Another consistency check
        assert abs(self._total - sum(item["price"] * item["quantity"] for item in self.items)) < 0.01, \
            "Total calculation is inconsistent!"
        
        return self._total


# ============================================================================
# PART 3: GRACEFUL DEGRADATION STRATEGY
# ============================================================================

print("\n" + "=" * 30)
print("GRACEFUL DEGRADATION")
print("=" * 30)
print("""
Graceful Degradation Philosophy:
- Continue operating with reduced functionality
- Provide fallbacks when services fail
- Never show raw errors to users
- Maintain core functionality
""")

class PaymentProcessorGraceful:
    """Graceful degradation implementation"""
    
    def __init__(self, primary_gateway, fallback_gateway=None, cache_service=None):
        self.primary = primary_gateway
        self.fallback = fallback_gateway
        self.cache = cache_service
        self.use_fallback = False
    
    def process_payment(self, payment_data):
        """Try primary, fallback, then cached response"""
        print(f"\n[Graceful] Processing payment: {payment_data.get('id')}")
        
        # Strategy 1: Try primary service
        try:
            print("  Attempting primary payment gateway...")
            result = self.primary.process(payment_data)
            print("  Primary gateway succeeded!")
            return result
            
        except (ConnectionError, TimeoutError) as e:
            print(f"  Primary failed: {e}")
            
            # Strategy 2: Try fallback service
            if self.fallback:
                try:
                    print("  Attempting fallback payment gateway...")
                    result = self.fallback.process(payment_data)
                    print("  Fallback gateway succeeded!")
                    self.use_fallback = True
                    return result
                    
                except Exception as e:
                    print(f"  Fallback also failed: {e}")
            
            # Strategy 3: Use cached responses for known payments
            if self.cache:
                cached = self.cache.get_payment(payment_data["id"])
                if cached:
                    print("  Using cached payment result")
                    return {
                        "success": True,
                        "cached": True,
                        "message": "Payment was previously processed",
                        "data": cached
                    }
            
            # Strategy 4: Queue for later processing
            print("  Queueing payment for later processing...")
            return {
                "success": False,
                "recoverable": True,
                "message": "Payment system is temporarily unavailable. Your payment has been queued.",
                "queue_id": f"QUEUE_{payment_data['id']}"
            }


class PrimaryPaymentGateway:
    def process(self, payment_data):
        # Simulate random failures
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise ConnectionError("Primary gateway timeout")
        return {"transaction_id": "PRIMARY_123", "status": "completed"}

class FallbackPaymentGateway:
    def process(self, payment_data):
        # Simulate slower but more reliable service
        import time
        time.sleep(0.1)
        return {"transaction_id": "FALLBACK_456", "status": "completed"}

class PaymentCache:
    def __init__(self):
        self.cache = {}
    
    def save_payment(self, payment_id, result):
        self.cache[payment_id] = result
    
    def get_payment(self, payment_id):
        return self.cache.get(payment_id)


print("\n--- Graceful Degradation Examples ---")

# Setup services
primary = PrimaryPaymentGateway()
fallback = FallbackPaymentGateway()
cache = PaymentCache()

# Cache a previous payment
cache.save_payment("PAY001", {"amount": 99.99, "status": "processed"})

processor = PaymentProcessorGraceful(primary, fallback, cache)

# Simulate multiple payment attempts
test_payments = [
    {"id": "PAY001", "amount": 99.99},
    {"id": "PAY002", "amount": 49.99},
    {"id": "PAY003", "amount": 199.99}
]

for i, payment in enumerate(test_payments, 1):
    print(f"\nPayment attempt {i}:")
    result = processor.process_payment(payment)
    print(f"  Result: {result}")


# ============================================================================
# PART 4: HYBRID APPROACH & ERROR RECOVERY
# ============================================================================

print("\n" + "=" * 30)
print("HYBRID APPROACH & ERROR RECOVERY")
print("=" * 30)

class ResilientService:
    """
    Combines fail-fast validation with graceful degradation
    and automatic retry mechanisms
    """
    
    def __init__(self, max_retries=3, retry_delay=1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def execute_with_retry(self, operation, operation_name="Operation"):
        """Retry pattern with exponential backoff"""
        import time
        
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    print(f"  Retry {attempt}/{self.max_retries} for {operation_name}")
                    # Exponential backoff
                    delay = self.retry_delay * (2 ** (attempt - 1))
                    time.sleep(delay)
                
                return operation()
                
            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                print(f"  Attempt {attempt + 1} failed: {e}")
                continue
            except ValueError as e:
                # Don't retry validation errors (fail-fast)
                print(f"  Validation error (no retry): {e}")
                raise
            except Exception as e:
                last_exception = e
                print(f"  Unexpected error: {e}")
                # Don't retry unknown errors
                break
        
        # All retries failed
        raise OperationFailedError(
            f"{operation_name} failed after {self.max_retries} retries",
            last_exception
        )
    
    def validate_and_process(self, data, validator, processor):
        """
        Hybrid approach:
        1. Fail-fast validation
        2. Graceful processing with retries
        3. Fallback if all retries fail
        """
        print(f"\n[ResilientService] Processing with hybrid strategy")
        
        # STEP 1: Fail-fast validation
        print("  Step 1: Validating input (fail-fast)...")
        validator(data)  # Raises ValueError if invalid
        
        # STEP 2: Process with retries and graceful degradation
        print("  Step 2: Processing with retry logic...")
        
        def process_operation():
            return processor(data)
        
        try:
            result = self.execute_with_retry(process_operation, "Payment processing")
            return {"success": True, "data": result}
            
        except OperationFailedError:
            # STEP 3: Graceful degradation
            print("  Step 3: All retries failed, applying graceful degradation...")
            return {
                "success": False,
                "recoverable": True,
                "message": "Service temporarily degraded. Your request has been queued.",
                "queued": True
            }


class OperationFailedError(Exception):
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


print("\n--- Hybrid Strategy Example ---")

def validate_payment_data(data):
    """Fail-fast validator"""
    if not data.get("id"):
        raise ValueError("Payment ID required")
    if data.get("amount", 0) <= 0:
        raise ValueError("Amount must be positive")

def process_payment(data):
    """Processor that might fail"""
    import random
    # Simulate unreliable service
    if random.random() < 0.6:  # 60% failure rate
        raise ConnectionError("Payment service unavailable")
    return {"transaction_id": f"TXN_{data['id']}", "status": "completed"}

# Create resilient service
resilient = ResilientService(max_retries=2, retry_delay=0.5)

# Test with valid data
print("\nTest 1: Processing valid payment (may require retries):")
result = resilient.validate_and_process(
    {"id": "PAY123", "amount": 100},
    validate_payment_data,
    process_payment
)
print(f"  Final result: {result}")

# Test with invalid data (should fail fast)
print("\nTest 2: Processing invalid payment (should fail fast):")
try:
    result = resilient.validate_and_process(
        {"id": "", "amount": -10},
        validate_payment_data,
        process_payment
    )
    print(f"  Result: {result}")
except ValueError as e:
    print(f"  Failed fast as expected: {e}")


# ============================================================================
# PART 5: CONTEXT-BASED ERROR HANDLING
# ============================================================================

print("\n" + "=" * 30)
print("CONTEXT-BASED ERROR HANDLING")
print("=" * 30)
print("""
Choosing the right strategy based on context:
1. User Input: Fail-fast with clear messages
2. External Services: Graceful degradation with fallbacks
3. Critical Operations: Retry with exponential backoff
4. Data Processing: Continue with partial results
""")

class ContextAwareErrorHandler:
    """Applies different strategies based on context"""
    
    @staticmethod
    def handle_user_input(context, input_data, validator):
        """Fail-fast for user input with helpful messages"""
        try:
            validator(input_data)
            return {"valid": True, "data": input_data}
        except ValueError as e:
            # User-friendly error messages
            return {
                "valid": False,
                "error": str(e),
                "suggestion": "Please check your input and try again."
            }
    
    @staticmethod
    def handle_external_service(context, operation, fallback=None):
        """Graceful degradation for external services"""
        try:
            return operation()
        except (ConnectionError, TimeoutError) as e:
            print(f"  External service failed: {e}")
            
            if fallback:
                print("  Using fallback...")
                return fallback()
            
            # Degrade gracefully
            return {
                "status": "degraded",
                "message": "Service temporarily unavailable",
                "timestamp": context.get("timestamp")
            }
    
    @staticmethod
    def handle_batch_processing(context, items, processor):
        """Continue processing despite individual failures"""
        results = []
        errors = []
        
        for item in items:
            try:
                result = processor(item)
                results.append(result)
            except Exception as e:
                errors.append({
                    "item": item,
                    "error": str(e)
                })
                # Continue with next item
        
        return {
            "processed": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors
        }


print("\n--- Context-Based Examples ---")

handler = ContextAwareErrorHandler()

# Example 1: User input validation (fail-fast)
print("\n1. User Input Context:")
def validate_email(email):
    if "@" not in email:
        raise ValueError("Invalid email format")
    return email

result = handler.handle_user_input(
    context={"source": "registration_form"},
    input_data="invalid-email",
    validator=validate_email
)
print(f"   Result: {result}")

# Example 2: External service with fallback
print("\n2. External Service Context:")
def fetch_weather():
    # Simulate service failure
    raise ConnectionError("Weather API timeout")

def fallback_weather():
    return {"temperature": "N/A", "source": "cached"}

weather_result = handler.handle_external_service(
    context={"service": "weather", "timestamp": "2024-01-15"},
    operation=fetch_weather,
    fallback=fallback_weather
)
print(f"   Result: {weather_result}")

# Example 3: Batch processing (continue on error)
print("\n3. Batch Processing Context:")
def process_order(order):
    if order["amount"] > 1000:
        raise ValueError(f"Order amount too high: {order['amount']}")
    return {"order_id": order["id"], "processed": True}

orders = [
    {"id": 1, "amount": 100},
    {"id": 2, "amount": 1500},  # This will fail
    {"id": 3, "amount": 200},
    {"id": 4, "amount": 3000},  # This will fail
    {"id": 5, "amount": 50}
]

batch_result = handler.handle_batch_processing(
    context={"job": "order_processing"},
    items=orders,
    processor=process_order
)
print(f"   Processed: {batch_result['processed']}, Failed: {batch_result['failed']}")
print(f"   Errors: {batch_result['errors']}")


# ============================================================================
# SUMMARY & DECISION GUIDE
# ============================================================================

print("\n" + "=" * 70)
print("ERROR HANDLING STRATEGY DECISION GUIDE")
print("=" * 70)

print("""
WHEN TO USE EACH STRATEGY:
--------------------------
1. FAIL-FAST (Raise Early):
   - User input validation
   - Configuration errors
   - Programming errors (use assertions)
   - Invalid business rules
   - When continuing would cause data corruption

2. GRACEFUL DEGRADATION (Continue with Reduced Functionality):
   - External service failures
   - Network timeouts
   - Non-critical feature failures
   - When partial results are acceptable
   - User-facing applications where uptime is critical

3. RETRY PATTERNS:
   - Transient failures (network blips)
   - Load-related timeouts
   - When failure is likely temporary
   - With exponential backoff to avoid thundering herd

4. LAYERED HANDLING:
   - Data Layer: Catch technical errors, convert to domain exceptions
   - Business Layer: Handle business rules, transform errors
   - Presentation Layer: Catch all, show user-friendly messages, log details

BEST PRACTICES:
---------------
1. Never expose raw exceptions to users
2. Log detailed errors for debugging
3. Use custom exception hierarchies
4. Document what exceptions each function can raise
5. Consider context when choosing strategy
6. Monitor error rates and patterns
7. Implement circuit breakers for external services
8. Test error scenarios as part of your test suite
""")

print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)