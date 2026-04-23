"""
OBSERVABILITY - LOGGING, MONITORING, AND TRACING
=================================================
Observability is the ability to understand the internal state of a system
based on its external outputs (logs, metrics, traces).

The Three Pillars:
1. LOGS: Discrete events
2. METRICS: Numerical measurements
3. TRACES: Request flow through system
"""

print("=" * 80)
print("OBSERVABILITY - LOGGING, MONITORING, AND TRACING")
print("=" * 80)

import logging
import structlog
import time
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
from contextlib import contextmanager
import json

# ============================================================================
# 1. STRUCTURED LOGGING WITH STRUCTLOG
# ============================================================================

"""
STRUCTURED LOGGING:
- JSON-formatted logs
- Easily parseable
- Better for log aggregation (ELK, Datadog)
- Context preservation
- Type-safe

INSTALLATION:
pip install structlog
"""

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# Create logger
log = structlog.get_logger()

def demo_structured_logging():
    """Demonstrate structured logging"""
    print("\n=== Structured Logging ===")
    
    # Basic logging with context
    log.info("user_login", user_id=123, username="alice", ip="192.168.1.1")
    
    # Error with exception
    try:
        result = 1 / 0
    except Exception as e:
        log.error("calculation_error", error=str(e), operation="division")
    
    # Bind context (persistent across logs)
    request_log = log.bind(request_id="abc-123", user_id=456)
    request_log.info("request_started", path="/api/users")
    request_log.info("database_query", table="users", duration_ms=45)
    request_log.info("request_completed", status_code=200)


# ============================================================================
# 2. LOGGING BEST PRACTICES
# ============================================================================

"""
LOGGING LEVELS:
- DEBUG: Detailed information for diagnosing problems
- INFO: General informational messages
- WARNING: Something unexpected but not an error
- ERROR: Error occurred but app continues
- CRITICAL: Serious error, app may not continue

WHAT TO LOG:
✓ User actions (login, logout, purchases)
✓ API requests/responses
✓ Database queries (in development)
✓ Errors and exceptions
✓ Performance metrics
✓ State changes

WHAT NOT TO LOG:
✗ Passwords, tokens, secrets
✗ PII (personally identifiable information) in production
✗ Too much (flooding logs)
✗ Inside tight loops
"""

class LoggingBestPractices:
    """Examples of logging best practices"""
    
    def __init__(self):
        self.log = structlog.get_logger()
    
    def process_payment(self, user_id: int, amount: float, card_last4: str):
        """Example: Log important business operation"""
        
        # Start of operation
        self.log.info(
            "payment_started",
            user_id=user_id,
            amount=amount,
            card_last4=card_last4,  # Only last 4 digits!
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Process payment
            time.sleep(0.1)  # Simulate processing
            
            # Success
            self.log.info(
                "payment_successful",
                user_id=user_id,
                amount=amount,
                transaction_id="txn_123456"
            )
            
            return {"status": "success", "transaction_id": "txn_123456"}
        
        except Exception as e:
            # Error with context
            self.log.error(
                "payment_failed",
                user_id=user_id,
                amount=amount,
                error=str(e),
                error_type=type(e).__name__
            )
            raise


# ============================================================================
# 3. PERFORMANCE MONITORING
# ============================================================================

class PerformanceMonitor:
    """
    Monitor operation performance
    """
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
    
    @contextmanager
    def measure(self, operation: str):
        """Context manager to measure operation time"""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            
            if operation not in self.metrics:
                self.metrics[operation] = []
            
            self.metrics[operation].append(duration)
            
            log.info(
                "operation_completed",
                operation=operation,
                duration_ms=duration * 1000,
                timestamp=datetime.now().isoformat()
            )
    
    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for operation"""
        if operation not in self.metrics:
            return {}
        
        durations = self.metrics[operation]
        return {
            "count": len(durations),
            "avg_ms": sum(durations) / len(durations) * 1000,
            "min_ms": min(durations) * 1000,
            "max_ms": max(durations) * 1000
        }

monitor = PerformanceMonitor()

def demo_performance_monitoring():
    """Demonstrate performance monitoring"""
    print("\n=== Performance Monitoring ===")
    
    # Measure operations
    with monitor.measure("database_query"):
        time.sleep(0.05)  # Simulate DB query
    
    with monitor.measure("api_call"):
        time.sleep(0.1)  # Simulate API call
    
    with monitor.measure("database_query"):
        time.sleep(0.03)  # Another query
    
    # Get statistics
    stats = monitor.get_stats("database_query")
    print(f"Database query stats: {stats}")


# ============================================================================
# 4. DISTRIBUTED TRACING
# ============================================================================

"""
DISTRIBUTED TRACING:
- Track requests across multiple services
- Understand latency sources
- Identify bottlenecks

TOOLS:
- OpenTelemetry (standard)
- Jaeger (UI for traces)
- Zipkin (distributed tracing)
- Datadog APM
- New Relic

OPENTELEMETRY EXAMPLE:

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Use in code
@tracer.start_as_current_span("process_order")
def process_order(order_id: str):
    with tracer.start_as_current_span("validate_order"):
        # Validation logic
        pass
    
    with tracer.start_as_current_span("charge_payment"):
        # Payment logic
        pass
    
    with tracer.start_as_current_span("update_inventory"):
        # Inventory logic
        pass
    
    return {"order_id": order_id, "status": "completed"}
"""


# ============================================================================
# 5. METRICS COLLECTION
# ============================================================================

"""
METRICS:
- Numerical measurements over time
- Counters, gauges, histograms
- Aggregated and visualized

PROMETHEUS EXAMPLE:

from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Define metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

# Use in application
@app.middleware("http")
async def metrics_middleware(request, call_next):
    active_requests.inc()  # Increment gauge
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Record metrics
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        duration = time.time() - start_time
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    
    finally:
        active_requests.dec()

# Expose metrics endpoint
start_http_server(8001)  # Metrics at http://localhost:8001/metrics
"""


# ============================================================================
# 6. HEALTH CHECKS
# ============================================================================

class HealthCheck:
    """
    Health check implementation
    """
    
    def __init__(self):
        self.checks: Dict[str, callable] = {}
    
    def register(self, name: str, check_func: callable):
        """Register health check"""
        self.checks[name] = check_func
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        for name, check_func in self.checks.items():
            try:
                check_result = await check_func() if asyncio.iscoroutinefunction(check_func) else check_func()
                results["checks"][name] = {
                    "status": "healthy",
                    "details": check_result
                }
            except Exception as e:
                results["checks"][name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                results["status"] = "unhealthy"
        
        return results

# Example health checks
health = HealthCheck()

async def check_database():
    """Check database connection"""
    # Simulate DB check
    await asyncio.sleep(0.01)
    return {"connected": True, "latency_ms": 10}

def check_redis():
    """Check Redis connection"""
    # Simulate Redis check
    return {"connected": True, "memory_mb": 100}

async def check_api_dependency():
    """Check external API"""
    # Simulate API check
    await asyncio.sleep(0.02)
    return {"available": True, "latency_ms": 20}

health.register("database", check_database)
health.register("redis", check_redis)
health.register("external_api", check_api_dependency)

"""
HEALTH CHECK ENDPOINT (FastAPI):

@app.get("/health")
async def health_check():
    return await health.run_checks()

@app.get("/health/live")
async def liveness():
    # Quick check if app is running
    return {"status": "ok"}

@app.get("/health/ready")
async def readiness():
    # Check if app is ready to serve traffic
    results = await health.run_checks()
    status_code = 200 if results["status"] == "healthy" else 503
    return JSONResponse(content=results, status_code=status_code)
"""


# ============================================================================
# 7. BEST PRACTICES
# ============================================================================

"""
OBSERVABILITY BEST PRACTICES:

LOGGING:
✓ Use structured logging (JSON)
✓ Include correlation IDs
✓ Log at appropriate levels
✓ Include context (user_id, request_id)
✓ Never log sensitive data
✓ Use log aggregation (ELK, Datadog)
✓ Set up log rotation

METRICS:
✓ Expose /metrics endpoint (Prometheus format)
✓ Track request rate, duration, errors
✓ Monitor resource usage (CPU, memory)
✓ Business metrics (signups, orders)
✓ Use dashboards (Grafana)
✓ Set up alerts

TRACING:
✓ Use OpenTelemetry (standard)
✓ Trace cross-service requests
✓ Include span context
✓ Sample traces (don't trace everything)
✓ Visualize with Jaeger/Zipkin

HEALTH CHECKS:
✓ Implement /health endpoints
✓ Check dependencies (DB, Redis, APIs)
✓ Separate liveness vs readiness
✓ Fast checks (<1s)

ALERTING:
✓ Alert on critical errors
✓ Set meaningful thresholds
✓ Avoid alert fatigue
✓ Include context in alerts
✓ Test alert rules

MONITORING WHAT MATTERS:
- Latency (p50, p95, p99)
- Error rate
- Request rate
- Saturation (CPU, memory, disk)
- Business KPIs
"""

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

async def main():
    """Run demonstrations"""
    demo_structured_logging()
    demo_performance_monitoring()
    
    # Health checks
    results = await health.run_checks()
    print(f"\nHealth check results: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())

print("\n=== Observability Complete ===")

"""
KEY TAKEAWAYS:

1. Three pillars: Logs, Metrics, Traces
2. Use structured logging (JSON format)
3. Include correlation IDs for request tracking
4. Expose Prometheus metrics
5. Implement OpenTelemetry tracing
6. Health check endpoints (liveness, readiness)
7. Monitor The Four Golden Signals:
   - Latency
   - Traffic
   - Errors
   - Saturation
8. Use log aggregation tools
9. Set up dashboards (Grafana)
10. Alert on anomalies, not everything
11. Never log sensitive data
12. Test observability in development
"""
