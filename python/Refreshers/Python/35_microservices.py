"""
MICROSERVICES ARCHITECTURE PATTERNS
====================================
Microservices are small, independent services that work together
to form a complete application.

Benefits:
- Independent deployment
- Technology diversity
- Fault isolation
- Scalability
- Team autonomy

Challenges:
- Distributed complexity
- Data consistency
- Testing
- Monitoring
"""

print("=" * 80)
print("MICROSERVICES ARCHITECTURE PATTERNS")
print("=" * 80)

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import hashlib

# ============================================================================
# 1. MICROSERVICES PRINCIPLES
# ============================================================================

"""
MICROSERVICES PRINCIPLES:

1. SINGLE RESPONSIBILITY:
   - Each service does one thing well
   - Clear boundaries
   - Independent data store

2. LOOSE COUPLING:
   - Services independent
   - Communicate via APIs
   - No shared databases

3. HIGH COHESION:
   - Related functionality grouped
   - Minimal cross-service dependencies

4. AUTONOMOUS:
   - Deploy independently
   - Own lifecycle
   - Own data

5. RESILIENT:
   - Handle failures gracefully
   - Circuit breakers
   - Timeouts and retries

6. OBSERVABLE:
   - Logging and monitoring
   - Distributed tracing
   - Health checks

7. DECENTRALIZED:
   - No single point of failure
   - Distributed data management
   - Service discovery
"""


# ============================================================================
# 2. SERVICE COMMUNICATION PATTERNS
# ============================================================================

"""
COMMUNICATION PATTERNS:

1. SYNCHRONOUS (HTTP/gRPC):
   - Request-response
   - Direct coupling
   - Use for: Queries, real-time needs
   
   Pros: Simple, immediate response
   Cons: Coupling, cascading failures

2. ASYNCHRONOUS (Message Queue):
   - Event-driven
   - Loose coupling
   - Use for: Commands, events
   
   Pros: Resilient, scalable
   Cons: Complexity, eventual consistency

3. HYBRID:
   - Synchronous for queries
   - Asynchronous for commands
   - Best of both worlds
"""

# ============================================================================
# HTTP Service Communication
# ============================================================================

class ServiceClient:
    """
    HTTP client for inter-service communication
    """
    
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """GET request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.get(url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        
        except aiohttp.ClientError as e:
            log.error("service_request_failed", url=url, error=str(e))
            raise
    
    async def post(self, endpoint: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.post(url, json=data, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        
        except aiohttp.ClientError as e:
            log.error("service_request_failed", url=url, error=str(e))
            raise


# ============================================================================
# 3. CIRCUIT BREAKER PATTERN
# ============================================================================

"""
CIRCUIT BREAKER:
Prevents cascading failures by stopping requests to failing services

STATES:
- CLOSED: Normal operation
- OPEN: Too many failures, reject requests
- HALF_OPEN: Test if service recovered

PARAMETERS:
- Failure threshold: Number of failures to open circuit
- Timeout: How long to stay open
- Success threshold: Successes needed to close
"""

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """
    Circuit breaker for service calls
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: float = 60.0,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker
        """
        if self.state == CircuitState.OPEN:
            # Check if timeout expired
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                print("Circuit HALF_OPEN: Testing service")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            # Execute function
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Success
            self.on_success()
            return result
        
        except Exception as e:
            # Failure
            self.on_failure()
            raise
    
    def on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                print("Circuit CLOSED: Service recovered")
    
    def on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"Circuit OPEN: Too many failures ({self.failure_count})")


async def demo_circuit_breaker():
    """Demonstrate circuit breaker"""
    print("\n=== Circuit Breaker ===")
    
    breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=2)
    
    attempts = 0
    
    async def flaky_service():
        nonlocal attempts
        attempts += 1
        
        # Fail first 3 times
        if attempts <= 3:
            raise Exception(f"Service failed (attempt {attempts})")
        
        return "Success!"
    
    # Try calling service multiple times
    for i in range(6):
        try:
            result = await breaker.call(flaky_service)
            print(f"Call {i + 1}: {result}")
        except Exception as e:
            print(f"Call {i + 1} failed: {e}")
        
        await asyncio.sleep(0.5)


# ============================================================================
# 4. SERVICE DISCOVERY
# ============================================================================

"""
SERVICE DISCOVERY:
Services need to find each other dynamically

PATTERNS:

1. CLIENT-SIDE DISCOVERY:
   - Client queries service registry
   - Client selects instance (load balancing)
   - Example: Consul, Eureka

2. SERVER-SIDE DISCOVERY:
   - Load balancer queries registry
   - Client calls load balancer
   - Example: Kubernetes Service, AWS ELB

3. DNS-BASED:
   - Services registered in DNS
   - Simple but limited
   - Example: Kubernetes DNS
"""

class ServiceRegistry:
    """
    Simple in-memory service registry
    (Production: Use Consul, etcd, or Kubernetes)
    """
    
    def __init__(self):
        self.services: Dict[str, List[Dict[str, Any]]] = {}
    
    def register(
        self,
        service_name: str,
        host: str,
        port: int,
        metadata: Optional[Dict] = None
    ):
        """Register service instance"""
        instance = {
            "host": host,
            "port": port,
            "registered_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        if service_name not in self.services:
            self.services[service_name] = []
        
        self.services[service_name].append(instance)
        
        print(f"Registered {service_name} at {host}:{port}")
    
    def deregister(self, service_name: str, host: str, port: int):
        """Deregister service instance"""
        if service_name in self.services:
            self.services[service_name] = [
                instance for instance in self.services[service_name]
                if not (instance["host"] == host and instance["port"] == port)
            ]
    
    def discover(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Discover service instance (simple round-robin)
        """
        if service_name not in self.services or not self.services[service_name]:
            return None
        
        # Simple: return first instance
        # Production: Load balancing algorithm
        return self.services[service_name][0]
    
    def get_all(self, service_name: str) -> List[Dict[str, Any]]:
        """Get all instances of a service"""
        return self.services.get(service_name, [])


# ============================================================================
# 5. API GATEWAY PATTERN
# ============================================================================

"""
API GATEWAY:
- Single entry point for clients
- Routes requests to microservices
- Cross-cutting concerns:
  - Authentication
  - Rate limiting
  - Request/response transformation
  - Caching
  - Logging

BENEFITS:
✓ Simplified client interface
✓ Reduced round trips
✓ Security layer
✓ Protocol translation

CHALLENGES:
✗ Single point of failure
✗ Bottleneck risk
✗ Complexity

TOOLS:
- Kong
- Nginx
- Traefik
- AWS API Gateway
- Azure API Management
"""


# ============================================================================
# 6. SAGA PATTERN (DISTRIBUTED TRANSACTIONS)
# ============================================================================

"""
SAGA PATTERN:
Manages distributed transactions without two-phase commit

TWO APPROACHES:

1. CHOREOGRAPHY:
   - Each service produces and listens to events
   - No central coordinator
   - Decentralized
   
   Example:
   Order Service → OrderCreated event
   Payment Service → PaymentProcessed event
   Inventory Service → InventoryReserved event

2. ORCHESTRATION:
   - Central coordinator (saga orchestrator)
   - Explicit control flow
   - Easier to understand
   
   Example:
   Orchestrator → Order Service (create order)
   Orchestrator → Payment Service (process payment)
   Orchestrator → Inventory Service (reserve inventory)

COMPENSATING TRANSACTIONS:
If a step fails, undo previous steps:
- CreateOrder → CancelOrder
- ProcessPayment → RefundPayment
- ReserveInventory → ReleaseInventory
"""

class SagaOrchestrator:
    """
    Simple saga orchestrator
    """
    
    def __init__(self):
        self.steps: List[Dict[str, Any]] = []
        self.completed_steps: List[int] = []
    
    def add_step(self, name: str, action: callable, compensate: callable):
        """Add saga step with compensation"""
        self.steps.append({
            "name": name,
            "action": action,
            "compensate": compensate
        })
    
    async def execute(self) -> bool:
        """
        Execute saga
        Returns True if successful, False if compensated
        """
        try:
            # Execute all steps
            for i, step in enumerate(self.steps):
                print(f"Executing: {step['name']}")
                await step["action"]()
                self.completed_steps.append(i)
            
            print("Saga completed successfully")
            return True
        
        except Exception as e:
            print(f"Saga failed: {e}")
            
            # Compensate completed steps in reverse order
            for i in reversed(self.completed_steps):
                step = self.steps[i]
                print(f"Compensating: {step['name']}")
                try:
                    await step["compensate"]()
                except Exception as comp_error:
                    print(f"Compensation failed: {comp_error}")
            
            return False


# Example: Order saga
async def demo_saga():
    """Demonstrate saga pattern"""
    print("\n=== Saga Pattern ===")
    
    # Simulated service calls
    async def create_order():
        await asyncio.sleep(0.1)
        print("  Order created")
    
    async def cancel_order():
        await asyncio.sleep(0.1)
        print("  Order cancelled")
    
    async def process_payment():
        await asyncio.sleep(0.1)
        # Simulate failure
        raise Exception("Payment declined")
    
    async def refund_payment():
        await asyncio.sleep(0.1)
        print("  Payment refunded")
    
    async def reserve_inventory():
        await asyncio.sleep(0.1)
        print("  Inventory reserved")
    
    async def release_inventory():
        await asyncio.sleep(0.1)
        print("  Inventory released")
    
    # Create saga
    saga = SagaOrchestrator()
    saga.add_step("create_order", create_order, cancel_order)
    saga.add_step("process_payment", process_payment, refund_payment)
    saga.add_step("reserve_inventory", reserve_inventory, release_inventory)
    
    # Execute (will fail and compensate)
    success = await saga.execute()
    print(f"Saga result: {'Success' if success else 'Failed and compensated'}")


# ============================================================================
# 7. BEST PRACTICES
# ============================================================================

"""
MICROSERVICES BEST PRACTICES:

DESIGN:
✓ Domain-driven design (DDD)
✓ Bounded contexts
✓ API-first design
✓ Version APIs from start
✓ Keep services small
✗ Don't create nano-services

COMMUNICATION:
✓ Async for commands/events
✓ Sync for queries
✓ Use message queues
✓ Implement timeouts
✓ Retry with backoff
✓ Circuit breakers

DATA:
✓ Each service owns its data
✓ No shared databases
✓ Event sourcing for consistency
✓ CQRS when appropriate
✗ Don't use distributed transactions

DEPLOYMENT:
✓ Containerize (Docker)
✓ Orchestrate (Kubernetes)
✓ CI/CD pipelines
✓ Blue-green deployments
✓ Canary releases
✓ Infrastructure as code

OBSERVABILITY:
✓ Centralized logging
✓ Distributed tracing
✓ Service mesh (Istio, Linkerd)
✓ Health checks
✓ Monitoring dashboards

TESTING:
✓ Unit tests per service
✓ Integration tests
✓ Contract testing (Pact)
✓ End-to-end tests (minimal)
✓ Chaos engineering

SECURITY:
✓ Service-to-service auth (mTLS)
✓ API gateway for external auth
✓ Secret management (Vault)
✓ Network policies
✓ Input validation
"""

# ============================================================================
# 8. MICROSERVICES ANTI-PATTERNS
# ============================================================================

"""
ANTI-PATTERNS TO AVOID:

1. DISTRIBUTED MONOLITH:
   ✗ Services tightly coupled
   ✗ Shared database
   ✗ Synchronous chains
   Solution: Loose coupling, async communication

2. NANO-SERVICES:
   ✗ Too many tiny services
   ✗ Excessive network overhead
   Solution: Right-size services

3. DATA COUPLING:
   ✗ Services sharing database tables
   ✗ Services directly accessing other service data
   Solution: API-based communication

4. LACK OF GOVERNANCE:
   ✗ No standards
   ✗ Technology chaos
   ✗ Inconsistent practices
   Solution: Governance, standards, patterns

5. IGNORING FALLACIES OF DISTRIBUTED COMPUTING:
   ✗ Network is reliable
   ✗ Latency is zero
   ✗ Bandwidth is infinite
   Solution: Design for failure

6. BIG BANG MIGRATION:
   ✗ Rewrite everything at once
   Solution: Strangler fig pattern, incremental migration
"""

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

async def main():
    """Run demonstrations"""
    
    # Circuit breaker
    await demo_circuit_breaker()
    
    # Saga pattern
    await demo_saga()
    
    print("\n=== Microservices Patterns Complete ===")

if __name__ == "__main__":
    asyncio.run(main())

"""
KEY TAKEAWAYS:

1. Microservices = small, independent, autonomous
2. Communication: Sync (HTTP) vs Async (messages)
3. Circuit breaker prevents cascading failures
4. Saga pattern for distributed transactions
5. Service discovery for dynamic routing
6. API gateway for unified entry point
7. Each service owns its data
8. Design for failure and resilience
9. Observability is critical
10. Start with monolith, extract services gradually
11. Use patterns: Circuit breaker, Saga, Event sourcing
12. Test thoroughly at all levels
"""
