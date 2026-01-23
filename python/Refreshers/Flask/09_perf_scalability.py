"""
FLASK PERFORMANCE, SCALABILITY, AND ARCHITECTURE DECISIONS
This comprehensive guide covers Flask's performance characteristics, scalability strategies,
and helps you decide when Flask is the right choice for your project.
"""

import time
import asyncio
import threading
import concurrent.futures
from datetime import datetime, timedelta
from functools import wraps
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
import memcache
from celery import Celery
import rq
from flask import Flask, request, jsonify, g, current_app
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
import queue
import multiprocessing
import os
import psutil

# ============================================================================
# 1. FLASK IS WSGI, NOT ASYNC-NATIVE: UNDERSTANDING THE IMPLICATIONS
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'performance-demo-key'

# Traditional synchronous Flask route
@app.route('/sync-endpoint')
def synchronous_endpoint():
    """
    Traditional Flask route - synchronous and blocking
    While this request is being processed, the worker thread/process cannot handle other requests
    """
    time.sleep(2)  # Simulate I/O bound operation (DB query, API call, etc.)
    return jsonify({'message': 'Synchronous response after 2 seconds'})

# ATTEMPTING ASYNC IN FLASK (Limited support)
@app.route('/fake-async')
def fake_async_route():
    """
    WARNING: This is NOT truly async in Flask/WSGI
    Even with async/await syntax, Flask/WSGI doesn't provide event loop integration
    The entire worker is still blocked during I/O
    """
    
    async def mock_async_operation():
        await asyncio.sleep(2)  # This doesn't actually free up the worker
        return "Async result"
    
    # This still blocks because Flask doesn't have an event loop
    result = asyncio.run(mock_async_operation())
    return jsonify({'message': result})

# Demonstration of Flask's synchronous nature
def demonstrate_wsgi_limitations():
    """
    WSGI (Web Server Gateway Interface) is synchronous by design
    Flask sits on top of WSGI, inheriting its synchronous nature
    
    Key Characteristics:
    1. One request per thread/process at a time
    2. I/O operations block the worker
    3. No built-in support for async/await
    4. Scale via adding more workers, not via async concurrency
    
    Contrast with ASGI (used by FastAPI, Quart):
    - Async-native
    - Handle thousands of concurrent connections
    - Non-blocking I/O
    """
    
    print("""
    ================================================
    FLASK IS WSGI - SYNCHRONOUS ARCHITECTURE
    ================================================
    
    Flask applications follow the WSGI specification which is:
    
    1. SYNCHRONOUS: Each request runs to completion before next starts
    2. BLOCKING: I/O operations (DB, API calls) block the worker
    3. PROCESS/THREAD BASED: Scale horizontally with multiple workers
    
    This is different from ASGI frameworks (FastAPI, Quart) which:
    
    1. ASYNCHRONOUS: Can handle multiple requests concurrently
    2. NON-BLOCKING: I/O doesn't block the event loop
    3. EVENT-DRIVEN: Scale vertically with single process
    
    Example: 100 concurrent requests with 2-second I/O:
    
    Flask (4 workers): ~50 seconds (100 requests / 4 workers * 2 seconds)
    FastAPI (async): ~2 seconds (all requests handled concurrently)
    
    Note: You CAN run async code in Flask, but it doesn't provide 
    the same concurrency benefits as async-native frameworks.
    """)

# ============================================================================
# 2. GUNICORN / UWSGI WORKER MODELS
# ============================================================================

def explain_gunicorn_worker_models():
    """
    Gunicorn (Green Unicorn) is a WSGI HTTP Server for Python
    It manages worker processes to handle concurrent requests
    
    Worker Types:
    """
    
    worker_configs = {
        'sync': {
            'description': 'Traditional synchronous worker',
            'use_case': 'CPU-bound tasks, safe but limited concurrency',
            'code': 'gunicorn --workers=4 app:app'
        },
        'gevent': {
            'description': 'Gevent worker using greenlets (coroutines)',
            'use_case': 'I/O-bound applications with many concurrent connections',
            'code': 'gunicorn --worker-class=gevent --worker-connections=1000 app:app'
        },
        'eventlet': {
            'description': 'Eventlet worker for async I/O',
            'use_case': 'Similar to gevent, alternative implementation',
            'code': 'gunicorn --worker-class=eventlet app:app'
        },
        'tornado': {
            'description': 'Tornado worker for async frameworks',
            'use_case': 'When using Tornado with Flask',
            'code': 'gunicorn --worker-class=tornado app:app'
        },
        'gthread': {
            'description': 'Thread-based worker',
            'use_case': 'I/O-bound with thread-safe code',
            'code': 'gunicorn --worker-class=gthread --threads=4 app:app'
        }
    }
    
    print("\n" + "="*60)
    print("GUNICORN WORKER MODELS")
    print("="*60)
    
    for worker, config in worker_configs.items():
        print(f"\n{worker.upper()}:")
        print(f"  Description: {config['description']}")
        print(f"  Use Case: {config['use_case']}")
        print(f"  Command: {config['code']}")

def explain_uwsgi_configuration():
    """
    uWSGI is another popular application server for Python
    
    Key configuration options for performance:
    """
    
    config = """
    [uwsgi]
    # Process Management
    master = true                    # Master process manages workers
    processes = 4                    # Number of worker processes
    threads = 2                      # Threads per worker (if using threads)
    
    # Socket Configuration
    socket = :8000                   # Listen on port 8000
    protocol = http                  # HTTP protocol
    
    # Performance Tuning
    harakiri = 30                    # Kill workers after 30 seconds of hanging
    max-requests = 1000              # Restart worker after 1000 requests
    buffer-size = 32768              # Buffer size for requests
    
    # Advanced Features
    lazy-apps = true                 # Load app in each worker (memory efficient)
    enable-threads = true            # Enable Python thread support
    single-interpreter = true        # Single Python interpreter per worker
    
    # Static Files (for better performance)
    static-map = /static=./static
    static-expires = 86400           # 1 day cache for static files
    """
    
    print("\n" + "="*60)
    print("UWSGI CONFIGURATION FOR PERFORMANCE")
    print("="*60)
    print(config)

# ============================================================================
# 3. THREAD VS PROCESS WORKERS: UNDERSTANDING THE TRADEOFFS
# ============================================================================

class WorkerStrategyDemonstrator:
    """
    Demonstrates different worker strategies and their tradeoffs
    """
    
    @staticmethod
    def thread_based_concurrency():
        """
        Thread-based workers share memory but have GIL limitations
        
        Advantages:
        - Memory efficient (shared memory space)
        - Fast context switching
        - Good for I/O-bound tasks
        
        Disadvantages:
        - Global Interpreter Lock (GIL) limits CPU parallelism
        - Thread-safety concerns
        - Debugging complexity
        """
        
        def io_bound_task(task_id):
            """Simulate I/O bound operation"""
            time.sleep(1)
            return f"Task {task_id} completed"
        
        print("\n" + "="*60)
        print("THREAD-BASED CONCURRENCY")
        print("="*60)
        
        start = time.time()
        
        # Using ThreadPoolExecutor for thread-based concurrency
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(io_bound_task, i) for i in range(8)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        duration = time.time() - start
        print(f"8 I/O-bound tasks with 4 threads: {duration:.2f} seconds")
        print("Expected: ~2 seconds (8 tasks / 4 threads * 1 second)")
    
    @staticmethod
    def process_based_concurrency():
        """
        Process-based workers avoid GIL but use more memory
        
        Advantages:
        - True CPU parallelism (no GIL limitation)
        - Memory isolation (crash in one doesn't affect others)
        - Better for CPU-bound tasks
        
        Disadvantages:
        - Higher memory usage
        - Slower inter-process communication
        - Process startup overhead
        """
        
        def cpu_bound_task(n):
            """Simulate CPU-bound operation"""
            return sum(i * i for i in range(n))
        
        print("\n" + "="*60)
        print("PROCESS-BASED CONCURRENCY")
        print("="*60)
        
        start = time.time()
        
        # Using ProcessPoolExecutor for process-based concurrency
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(cpu_bound_task, 1000000) for _ in range(8)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        duration = time.time() - start
        print(f"8 CPU-bound tasks with 4 processes: {duration:.2f} seconds")
        print("Note: Processes better for CPU work, threads better for I/O")
    
    @staticmethod
    def hybrid_approach():
        """
        Hybrid approach: Multiple processes, each with multiple threads
        
        Recommended for Flask:
        - Use process workers for GIL avoidance
        - Add threads within each process for I/O concurrency
        - Balance based on workload characteristics
        """
        
        print("\n" + "="*60)
        print("HYBRID APPROACH (PROCESSES + THREADS)")
        print("="*60)
        print("""
        Gunicorn example with hybrid approach:
        
        gunicorn --workers=2 --threads=4 --worker-class=gthread app:app
        
        This creates:
        - 2 worker processes (avoid GIL, memory isolation)
        - Each with 4 threads (I/O concurrency within process)
        - Total concurrent capacity: 2 × 4 = 8 requests
        
        Choose based on your workload:
        
        I/O-BOUND (APIs, DB calls):
        - More threads per process
        - Example: 2 workers × 8 threads = 16 concurrency
        
        CPU-BOUND (Data processing, ML inference):
        - More processes, fewer threads
        - Example: 8 workers × 2 threads = 16 concurrency
        
        MIXED WORKLOAD:
        - Balance based on profiling
        - Example: 4 workers × 4 threads = 16 concurrency
        """)

# ============================================================================
# 4. WHEN FLASK BECOMES A BOTTLENECK: IDENTIFICATION AND SOLUTIONS
# ============================================================================

class PerformanceBottleneckAnalyzer:
    """
    Identifies when Flask becomes a bottleneck and suggests solutions
    """
    
    @staticmethod
    def identify_bottlenecks():
        """
        Common bottlenecks in Flask applications
        """
        
        bottlenecks = {
            'database_queries': {
                'symptoms': ['Slow response times', 'High DB CPU usage', 'Connection timeouts'],
                'detection': 'Use query profiling, monitor slow query logs',
                'solution': 'Add indexes, optimize queries, implement caching'
            },
            'external_api_calls': {
                'symptoms': ['Waiting for external services', 'Cascading timeouts'],
                'detection': 'Monitor external service response times',
                'solution': 'Implement timeouts, circuit breakers, async processing'
            },
            'cpu_bound_operations': {
                'symptoms': ['High CPU usage', 'Slow response even with few users'],
                'detection': 'Profile CPU usage per request',
                'solution': 'Offload to background jobs, use process workers'
            },
            'memory_issues': {
                'symptoms': ['Memory leaks', 'Frequent worker restarts'],
                'detection': 'Monitor memory usage over time',
                'solution': 'Fix memory leaks, implement connection pooling'
            },
            'global_interpreter_lock': {
                'symptoms': ['CPU underutilization', 'Poor multi-core scaling'],
                'detection': 'High CPU on single core, others idle',
                'solution': 'Use process-based workers, offload to services'
            }
        }
        
        print("\n" + "="*60)
        print("IDENTIFYING FLASK BOTTLENECKS")
        print("="*60)
        
        for bottleneck, info in bottlenecks.items():
            print(f"\n{bottleneck.replace('_', ' ').title()}:")
            print(f"  Symptoms: {', '.join(info['symptoms'])}")
            print(f"  Detection: {info['detection']}")
            print(f"  Solution: {info['solution']}")
    
    @staticmethod
    def performance_monitoring_decorator():
        """
        Decorator to monitor endpoint performance
        Helps identify slow endpoints
        """
        
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                start_time = time.time()
                result = f(*args, **kwargs)
                end_time = time.time()
                
                duration = end_time - start_time
                
                # Log slow requests (threshold: 1 second)
                if duration > 1.0:
                    print(f"⚠️  SLOW ENDPOINT: {f.__name__} took {duration:.2f} seconds")
                
                # Add timing header to response
                if isinstance(result, tuple) and len(result) == 2:
                    response, status = result
                    response.headers['X-Response-Time'] = f"{duration:.3f}s"
                    return response, status
                
                return result
            
            return decorated_function
        return decorator
    
    @app.route('/monitored-endpoint')
    @performance_monitoring_decorator()
    def monitored_endpoint():
        """Endpoint with performance monitoring"""
        time.sleep(1.5)  # Simulate slow operation
        return jsonify({'status': 'ok', 'message': 'This endpoint is monitored'})

# ============================================================================
# 5. CACHING STRATEGIES FOR FLASK
# ============================================================================

# Configure Flask-Caching
cache_config = {
    'CACHE_TYPE': 'redis',  # Options: redis, memcached, simple, filesystem
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
    'CACHE_KEY_PREFIX': 'flask_demo_'
}

cache = Cache(config=cache_config)
cache.init_app(app)

class CachingStrategies:
    """
    Different caching strategies for Flask applications
    """
    
    @staticmethod
    @app.route('/cache-simple')
    @cache.cached(timeout=60)  # Cache for 60 seconds
    def simple_caching():
        """
        Simple view caching - entire response cached
        Good for: Static or infrequently changing data
        """
        print("Cache MISS - generating fresh response")
        time.sleep(2)  # Simulate expensive operation
        return jsonify({
            'data': 'Expensive to compute data',
            'generated_at': datetime.utcnow().isoformat()
        })
    
    @staticmethod
    @app.route('/cache-memoize/<int:user_id>')
    @cache.memoize(timeout=120)  # Memoize with arguments
    def memoized_caching(user_id):
        """
        Memoization - caches based on function arguments
        Good for: User-specific data that doesn't change often
        """
        print(f"Cache MISS for user {user_id}")
        time.sleep(1)
        return jsonify({
            'user_id': user_id,
            'profile': f'Profile data for user {user_id}',
            'cached_at': datetime.utcnow().isoformat()
        })
    
    @staticmethod
    @app.route('/cache-database')
    def database_caching_example():
        """
        Manual caching strategy for database queries
        """
        cache_key = 'expensive_query_results'
        
        # Try to get from cache first
        cached_result = cache.get(cache_key)
        
        if cached_result:
            print("Cache HIT - using cached data")
            return jsonify({
                'source': 'cache',
                'data': cached_result,
                'retrieved_at': datetime.utcnow().isoformat()
            })
        
        # Cache miss - compute and store
        print("Cache MISS - computing fresh data")
        time.sleep(3)  # Simulate expensive database query
        
        result = {
            'users': 1000,
            'orders': 5000,
            'revenue': 100000
        }
        
        # Store in cache for future requests
        cache.set(cache_key, result, timeout=300)  # 5 minutes
        
        return jsonify({
            'source': 'database',
            'data': result,
            'cached_at': datetime.utcnow().isoformat()
        })
    
    @staticmethod
    def cache_invalidation_pattern():
        """
        Cache invalidation strategies
        """
        
        print("\n" + "="*60)
        print("CACHE INVALIDATION STRATEGIES")
        print("="*60)
        
        strategies = [
            ("Time-based expiration", "Set appropriate TTL based on data freshness needs"),
            ("Write-through cache", "Update cache when data is updated"),
            ("Write-behind cache", "Update cache asynchronously after DB update"),
            ("Cache-aside pattern", "App manages cache manually, invalidates on updates"),
            ("Tag-based invalidation", "Group cached items by tags, invalidate by tag")
        ]
        
        for strategy, description in strategies:
            print(f"\n{strategy}:")
            print(f"  {description}")
    
    @staticmethod
    @app.route('/cache-delete/<key>')
    def delete_cache(key):
        """
        Manual cache deletion endpoint
        Useful for cache invalidation
        """
        cache.delete(key)
        return jsonify({'status': 'deleted', 'key': key})

# ============================================================================
# 6. BACKGROUND JOBS (CELERY / RQ)
# ============================================================================

# Celery Configuration
celery_app = Celery(
    'flask_demo',
    broker='redis://localhost:6379/1',  # Message broker
    backend='redis://localhost:6379/2'   # Result backend
)

# RQ (Redis Queue) Configuration
redis_conn = redis.Redis(host='localhost', port=6379, db=3)
rq_queue = rq.Queue('default', connection=redis_conn)

class BackgroundJobStrategies:
    """
    Background job processing strategies for Flask
    """
    
    # ============== CELERY TASKS ==============
    
    @celery_app.task(bind=True, max_retries=3)
    def process_large_file(self, file_path):
        """
        Celery task for processing large files
        Runs asynchronously, can be retried
        """
        try:
            print(f"Processing file: {file_path}")
            time.sleep(10)  # Simulate long processing
            return f"Processed {file_path}"
        except Exception as exc:
            # Auto-retry with exponential backoff
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
    
    @celery_app.task
    def send_bulk_emails(self, email_list):
        """Send emails in background"""
        for email in email_list:
            print(f"Sending email to {email}")
            time.sleep(0.5)  # Simulate email sending
        return f"Sent {len(email_list)} emails"
    
    @app.route('/trigger-celery-task')
    def trigger_celery():
        """Trigger a Celery background task"""
        task = BackgroundJobStrategies.process_large_file.delay('/path/to/large/file.csv')
        return jsonify({
            'task_id': task.id,
            'status': 'started',
            'check_status': f'/task-status/{task.id}'
        })
    
    # ============== RQ (REDIS QUEUE) TASKS ==============
    
    def process_image_rq(self, image_path):
        """RQ job function"""
        print(f"Processing image: {image_path}")
        time.sleep(5)
        return f"Processed image {image_path}"
    
    @app.route('/trigger-rq-job')
    def trigger_rq():
        """Trigger an RQ background job"""
        job = rq_queue.enqueue(
            BackgroundJobStrategies().process_image_rq,
            '/path/to/image.jpg',
            job_timeout=30  # 30 second timeout
        )
        return jsonify({
            'job_id': job.id,
            'status': 'queued',
            'queue_size': len(rq_queue)
        })
    
    @staticmethod
    def compare_celery_vs_rq():
        """
        Comparison between Celery and RQ for background jobs
        """
        
        comparison = {
            'celery': {
                'pros': [
                    'Full-featured, production-ready',
                    'Supports multiple brokers (Redis, RabbitMQ, etc.)',
                    'Complex workflows (chains, groups, chords)',
                    'Monitoring and administration tools (Flower)',
                    'Rate limiting, retries, error handling'
                ],
                'cons': [
                    'More complex setup',
                    'Heavier resource usage',
                    'Steeper learning curve'
                ],
                'use_cases': 'Enterprise applications, complex workflows, large scale'
            },
            'rq': {
                'pros': [
                    'Simple and easy to use',
                    'Lightweight',
                    'Redis-only (simpler architecture)',
                    'Easier to debug'
                ],
                'cons': [
                    'Limited features compared to Celery',
                    'Redis as only broker option',
                    'Limited monitoring tools'
                ],
                'use_cases': 'Simple background tasks, smaller applications, quick setup'
            }
        }
        
        print("\n" + "="*60)
        print("CELERY VS RQ: CHOOSING BACKGROUND JOB PROCESSING")
        print("="*60)
        
        for system, info in comparison.items():
            print(f"\n{system.upper()}:")
            print(f"  Pros: {', '.join(info['pros'][:2])}...")
            print(f"  Use Cases: {info['use_cases']}")

# ============================================================================
# 7. CONNECTION POOLING
# ============================================================================

class ConnectionPoolingStrategies:
    """
    Connection pooling strategies for database and external services
    """
    
    @staticmethod
    def sqlalchemy_connection_pool():
        """
        SQLAlchemy connection pooling configuration
        """
        
        # Configure with optimized pool settings
        engine = create_engine(
            'postgresql://user:pass@localhost/dbname',
            poolclass=QueuePool,  # Default, thread-safe connection pool
            
            # Pool configuration
            pool_size=10,          # Number of connections to keep open
            max_overflow=20,       # Max connections above pool_size
            pool_timeout=30,       # Seconds to wait for connection
            pool_recycle=3600,     # Recycle connections after 1 hour
            pool_pre_ping=True,    # Verify connections before using
            
            # Performance tuning
            echo=False,            # Don't log SQL (for production)
            executemany_mode='values_plus_batch'  # Faster bulk inserts
        )
        
        print("\n" + "="*60)
        print("SQLALCHEMY CONNECTION POOLING")
        print("="*60)
        print(f"""
        Pool Configuration:
        - pool_size: {engine.pool.size()} (connections always ready)
        - max_overflow: {engine.pool._max_overflow} (extra connections when busy)
        - pool_timeout: {engine.pool.timeout()}s (wait time for connection)
        - pool_recycle: {engine.pool._recycle}s (reconnect interval)
        
        Monitoring:
        - Checked out connections: {engine.pool.checkedout()}
        - Connections in pool: {engine.pool.checkedin()}
        """)
        
        return engine
    
    @staticmethod
    def psycopg2_connection_pool():
        """
        Direct PostgreSQL connection pooling with psycopg2
        """
        
        # Create a threaded connection pool
        pool = ThreadedConnectionPool(
            minconn=5,      # Minimum connections in pool
            maxconn=20,     # Maximum connections in pool
            host='localhost',
            database='mydb',
            user='myuser',
            password='mypassword'
        )
        
        def get_connection():
            """Get connection from pool"""
            return pool.getconn()
        
        def return_connection(conn):
            """Return connection to pool"""
            pool.putconn(conn)
        
        print("\n" + "="*60)
        print("PSYCOPG2 THREADED CONNECTION POOL")
        print("="*60)
        print(f"""
        Pool Stats:
        - Min connections: 5 (always available)
        - Max connections: 20 (limit under load)
        
        Usage Pattern:
        
        def process_request():
            conn = get_connection()
            try:
                # Use connection
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                return cursor.fetchall()
            finally:
                # Always return connection to pool
                return_connection(conn)
        """)
        
        return pool
    
    @staticmethod
    def redis_connection_pool():
        """
        Redis connection pooling
        """
        
        # Redis connection pool
        redis_pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=0,
            max_connections=50,      # Maximum pool size
            socket_connect_timeout=5, # Connection timeout
            socket_keepalive=True,    # Keep connections alive
            retry_on_timeout=True     # Retry on timeout
        )
        
        # Create Redis client using connection pool
        redis_client = redis.Redis(connection_pool=redis_pool)
        
        print("\n" + "="*60)
        print("REDIS CONNECTION POOLING")
        print("="*60)
        print(f"""
        Configuration:
        - Max connections: 50
        - Connection reuse: Enabled
        - Timeout handling: Automatic retry
        
        Benefits:
        1. Reuse connections instead of creating new ones
        2. Limit total connections to prevent overload
        3. Better performance under load
        4. Resource management
        
        Without pooling (BAD):
        for i in range(1000):
            r = redis.Redis()  # Creates new connection each time!
            r.get('key')
        
        With pooling (GOOD):
        for i in range(1000):
            r = redis_client    # Reuses connections from pool
            r.get('key')
        """)
        
        return redis_client
    
    @staticmethod
    def http_connection_pool():
        """
        HTTP connection pooling for external API calls
        """
        import requests
        
        # Create a session with connection pooling
        session = requests.Session()
        
        # Configure adapter with connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,     # Number of connection pools
            pool_maxsize=100,        # Max connections per host
            max_retries=3,           # Retry failed requests
            pool_block=False         # Don't block when pool is full
        )
        
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        print("\n" + "="*60)
        print("HTTP CONNECTION POOLING WITH REQUESTS")
        print("="*60)
        print(f"""
        Configuration:
        - Connection pools: 10 (for different hosts)
        - Max connections per host: 100
        - Connection reuse: Enabled
        - Keep-alive: Automatic
        
        Benefits for Flask API calls:
        1. Reuse TCP connections to external APIs
        2. Avoid SSL handshake overhead
        3. Better performance for repeated calls
        4. Resource efficiency
        
        Example impact:
        
        Without pooling: 100 API calls = 100 TCP connections + SSL handshakes
        With pooling: 100 API calls = 1-10 TCP connections (reused)
        
        Performance improvement: 50-80% faster API calls
        """)
        
        return session

# ============================================================================
# 8. WHEN WOULD YOU NOT CHOOSE FLASK?
# ============================================================================

class FlaskAlternativesGuide:
    """
    Guide to when NOT to choose Flask and alternatives to consider
    """
    
    @staticmethod
    def when_not_to_choose_flask():
        """
        Scenarios where Flask might not be the best choice
        """
        
        scenarios = [
            {
                'scenario': 'REAL-TIME APPLICATIONS',
                'description': 'Chat apps, live dashboards, gaming',
                'why_not_flask': 'WSGI is synchronous, no native WebSocket support',
                'alternatives': ['Django Channels', 'FastAPI with WebSockets', 'Socket.IO', 'Tornado']
            },
            {
                'scenario': 'HIGH-CONCURRENCY APIs',
                'description': 'Thousands of concurrent connections, high throughput',
                'why_not_flask': 'Thread/process model doesn\'t scale as well as async',
                'alternatives': ['FastAPI', 'Quart', 'aiohttp', 'Sanic']
            },
            {
                'scenario': 'MICROSERVICES WITH ASYNC DEPENDENCIES',
                'description': 'Many external API calls, database connections',
                'why_not_flask': 'Async code runs but doesn\'t provide concurrency benefits',
                'alternatives': ['FastAPI', 'Quart', 'Starlette']
            },
            {
                'scenario': 'ENTERPRISE APPLICATIONS WITH BUILT-IN ADMIN',
                'description': 'Applications needing admin interface, auth, ORM out of the box',
                'why_not_flask': 'Flask is minimal, requires adding many extensions',
                'alternatives': ['Django', 'Ruby on Rails', 'Laravel']
            },
            {
                'scenario': 'GRAPHQL-FIRST APPLICATIONS',
                'description': 'Applications primarily serving GraphQL',
                'why_not_flask': 'No built-in GraphQL support, requires extensions',
                'alternatives': ['FastAPI with Strawberry', 'Graphene (Django)', 'Apollo Server']
            },
            {
                'scenario': 'CPU-INTENSIVE TASKS IN REQUEST CYCLE',
                'description': 'ML inference, video processing, complex calculations',
                'why_not_flask': 'Blocks workers, poor utilization of multiple cores',
                'alternatives': ['Offload to background workers', 'Use separate service', 'FastAPI with async']
            }
        ]
        
        print("\n" + "="*60)
        print("WHEN NOT TO CHOOSE FLASK")
        print("="*60)
        
        for scenario in scenarios:
            print(f"\n{scenario['scenario']}:")
            print(f"  Description: {scenario['description']}")
            print(f"  Flask Limitation: {scenario['why_not_flask']}")
            print(f"  Alternatives: {', '.join(scenario['alternatives'])}")
    
    @staticmethod
    def framework_comparison():
        """
        Detailed comparison with alternative frameworks
        """
        
        frameworks = {
            'flask': {
                'type': 'WSGI, Synchronous',
                'best_for': ['REST APIs', 'Microservices', 'Prototyping', 'Small to medium apps'],
                'performance': 'Good for typical web apps, scales with workers',
                'async': 'Limited support, not async-native',
                'learning_curve': 'Low to medium',
                'ecosystem': 'Large, many extensions'
            },
            'fastapi': {
                'type': 'ASGI, Async-native',
                'best_for': ['High-concurrency APIs', 'Real-time apps', 'Microservices'],
                'performance': 'Excellent for I/O bound, handles thousands of concurrent connections',
                'async': 'Full async/await support',
                'learning_curve': 'Medium (requires async understanding)',
                'ecosystem': 'Growing rapidly'
            },
            'django': {
                'type': 'WSGI, Synchronous (ASGI with Channels)',
                'best_for': ['Full-featured web apps', 'Admin interfaces', 'Enterprise apps'],
                'performance': 'Good, batteries-included approach has overhead',
                'async': 'Limited (Django 3.1+ has async views)',
                'learning_curve': 'High (many features to learn)',
                'ecosystem': 'Very large, mature'
            },
            'quart': {
                'type': 'ASGI, Async-native',
                'best_for': ['Async Flask-like apps', 'WebSocket applications'],
                'performance': 'Similar to FastAPI, async Flask alternative',
                'async': 'Full async/await, Flask-like API',
                'learning_curve': 'Low if you know Flask',
                'ecosystem': 'Uses Flask extensions where compatible'
            },
            'sanic': {
                'type': 'ASGI, Async-native',
                'best_for': ['High performance APIs', 'Async microservices'],
                'performance': 'Very fast, built for speed',
                'async': 'Full async/await support',
                'learning_curve': 'Medium',
                'ecosystem': 'Small but focused'
            }
        }
        
        print("\n" + "="*60)
        print("FRAMEWORK COMPARISON")
        print("="*60)
        
        for framework, info in frameworks.items():
            print(f"\n{framework.upper()}:")
            print(f"  Type: {info['type']}")
            print(f"  Best for: {', '.join(info['best_for'][:2])}...")
            print(f"  Async support: {info['async']}")
    
    @staticmethod
    def migration_path_from_flask():
        """
        How to migrate from Flask if you outgrow it
        """
        
        print("\n" + "="*60)
        print("MIGRATION PATHS FROM FLASK")
        print("="*60)
        
        migration_strategies = [
            ("GRADUAL MIGRATION TO QUART", """
            # 1. Install Quart (async Flask)
            pip install quart
            
            # 2. Change imports
            # FROM: from flask import Flask
            # TO:   from quart import Quart
            
            # 3. Add async/await to route handlers
            @app.route('/endpoint')
            async def endpoint():
                result = await async_operation()
                return jsonify(result)
            
            # 4. Update extensions to async versions
            # Many Flask extensions have Quart equivalents
            """),
            
            ("HYBRID APPROACH WITH FASTAPI", """
            # 1. Keep Flask for existing endpoints
            # 2. Add FastAPI for new async endpoints
            
            from fastapi import FastAPI
            from flask import Flask
            
            flask_app = Flask(__name__)
            fastapi_app = FastAPI()
            
            # Mount Flask app under FastAPI
            # or run them on different ports
            
            # Gradually migrate endpoints from Flask to FastAPI
            """),
            
            ("OFFLOAD WORK TO SEPARATE SERVICES", """
            # Instead of replacing Flask, augment it:
            
            1. Keep Flask for synchronous, request-response work
            2. Create separate async services for:
               - Real-time features (WebSockets)
               - High-concurrency endpoints
               - CPU-intensive tasks
            
            3. Use message queues (Redis, RabbitMQ) to communicate
            4. Implement API gateway to route requests
            """),
            
            ("OPTIMIZE EXISTING FLASK APP", """
            Before migrating, try optimizing:
            
            1. Add caching (Redis, Memcached)
            2. Implement connection pooling
            3. Use background jobs (Celery)
            4. Add more workers/threads
            5. Use gevent/eventlet workers
            6. Implement database optimizations
            
            Often, optimization can solve performance issues
            without needing framework migration
            """)
        ]
        
        for strategy, code in migration_strategies:
            print(f"\n{strategy}:")
            print(code)

# ============================================================================
# 9. PERFORMANCE OPTIMIZATION CHECKLIST
# ============================================================================

class PerformanceOptimizationChecklist:
    """
    Comprehensive checklist for optimizing Flask applications
    """
    
    @staticmethod
    def generate_checklist():
        """
        Performance optimization checklist
        """
        
        checklist = {
            'Architecture': [
                'Use application factory pattern',
                'Implement blueprints for modularity',
                'Separate concerns (models, views, services)',
                'Use environment-specific configurations'
            ],
            'Deployment & Scaling': [
                'Use Gunicorn/uWSGI in production',
                'Configure appropriate worker count (2-4 × CPU cores)',
                'Use gevent/eventlet workers for I/O bound apps',
                'Implement load balancing',
                'Use process supervisor (Supervisor, systemd)'
            ],
            'Database Optimization': [
                'Implement connection pooling',
                'Use database indexes',
                'Optimize queries (avoid N+1 problem)',
                'Use read replicas for heavy read workloads',
                'Implement database migrations properly'
            ],
            'Caching Strategy': [
                'Implement Redis/Memcached for frequent queries',
                'Cache static content',
                'Use HTTP caching headers',
                'Implement cache invalidation strategy',
                'Consider CDN for static assets'
            ],
            'Background Processing': [
                'Offload long-running tasks to Celery/RQ',
                'Use message queues for decoupling',
                'Implement retry mechanisms',
                'Monitor background job queues'
            ],
            'Monitoring & Profiling': [
                'Implement application logging',
                'Use APM tools (New Relic, DataDog)',
                'Monitor database query performance',
                'Track memory usage and leaks',
                'Set up alerts for error rates'
            ],
            'Security & Performance': [
                'Implement rate limiting',
                'Use secure, performant session storage',
                'Enable CORS appropriately',
                'Use HTTPS with modern ciphers',
                'Implement request size limits'
            ],
            'Frontend Performance': [
                'Minify and bundle static assets',
                'Implement lazy loading',
                'Use efficient JavaScript frameworks',
                'Optimize images and media',
                'Implement server-side rendering where needed'
            ]
        }
        
        print("\n" + "="*60)
        print("FLASK PERFORMANCE OPTIMIZATION CHECKLIST")
        print("="*60)
        
        for category, items in checklist.items():
            print(f"\n{category}:")
            for item in items:
                print(f"  [ ] {item}")

# ============================================================================
# 10. DEMONSTRATION AND BENCHMARKING
# ============================================================================

class PerformanceDemonstrator:
    """
    Demonstrates performance characteristics with benchmarks
    """
    
    @staticmethod
    def benchmark_sync_vs_async_pattern():
        """
        Benchmark to show performance characteristics
        """
        
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK: SYNC VS ASYNC PATTERNS")
        print("="*60)
        
        # Simulate 100 concurrent requests with 100ms I/O each
        
        def synchronous_processing():
            """Simulate synchronous Flask processing"""
            start = time.time()
            for i in range(100):
                time.sleep(0.1)  # 100ms I/O operation
            return time.time() - start
        
        async def asynchronous_processing():
            """Simulate async framework processing"""
            start = time.time()
            tasks = []
            for i in range(100):
                tasks.append(asyncio.sleep(0.1))
            await asyncio.gather(*tasks)
            return time.time() - start
        
        # Run benchmarks
        sync_time = synchronous_processing()
        
        # For async, we need to run in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_time = loop.run_until_complete(asynchronous_processing())
        
        print(f"\nSynchronous (Flask-like):")
        print(f"  100 requests × 100ms I/O = {sync_time:.2f} seconds")
        print(f"  Throughput: {100/sync_time:.1f} requests/second")
        
        print(f"\nAsynchronous (FastAPI-like):")
        print(f"  100 requests × 100ms I/O = {async_time:.2f} seconds")
        print(f"  Throughput: {100/async_time:.1f} requests/second")
        
        print(f"\nPerformance improvement: {sync_time/async_time:.1f}x faster")
        
        print("\n" + "="*60)
        print("KEY INSIGHT:")
        print("="*60)
        print("""
        Flask's performance depends on:
        1. Number of workers/threads
        2. I/O vs CPU bound workload
        3. Efficiency of blocking operations
        
        For I/O-bound workloads with many concurrent users,
        async frameworks can handle more requests with fewer resources.
        
        For Flask to achieve similar throughput, you need:
        - More workers (more memory)
        - Efficient connection pooling
        - Background job processing
        - Caching strategy
        """)

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def run_comprehensive_demo():
    """
    Run all demonstrations
    """
    
    print("\n" + "="*80)
    print("FLASK PERFORMANCE & SCALABILITY COMPREHENSIVE GUIDE")
    print("="*80)
    
    # 1. Flask is WSGI, not async-native
    demonstrate_wsgi_limitations()
    
    # 2. Gunicorn/uWSGI worker models
    explain_gunicorn_worker_models()
    explain_uwsgi_configuration()
    
    # 3. Thread vs Process workers
    WorkerStrategyDemonstrator.thread_based_concurrency()
    WorkerStrategyDemonstrator.process_based_concurrency()
    WorkerStrategyDemonstrator.hybrid_approach()
    
    # 4. When Flask becomes a bottleneck
    PerformanceBottleneckAnalyzer.identify_bottlenecks()
    
    # 5. Caching strategies
    CachingStrategies.cache_invalidation_pattern()
    
    # 6. Background jobs
    BackgroundJobStrategies.compare_celery_vs_rq()
    
    # 7. Connection pooling
    ConnectionPoolingStrategies.sqlalchemy_connection_pool()
    ConnectionPoolingStrategies.redis_connection_pool()
    ConnectionPoolingStrategies.http_connection_pool()
    
    # 8. When not to choose Flask
    FlaskAlternativesGuide.when_not_to_choose_flask()
    FlaskAlternativesGuide.framework_comparison()
    FlaskAlternativesGuide.migration_path_from_flask()
    
    # 9. Performance optimization checklist
    PerformanceOptimizationChecklist.generate_checklist()
    
    # 10. Performance demonstration
    PerformanceDemonstrator.benchmark_sync_vs_async_pattern()
    
    print("\n" + "="*80)
    print("SUMMARY: FLASK PERFORMANCE & SCALABILITY")
    print("="*80)
    print("""
    Flask is an excellent choice for:
    ✅ Traditional web applications
    ✅ REST APIs with moderate concurrency
    ✅ Prototyping and MVPs
    ✅ Microservices with sync dependencies
    
    Flask requires careful planning for:
    ⚠️  High-concurrency applications (>1000 concurrent users)
    ⚠️  Real-time features (WebSockets)
    ⚠️  CPU-intensive request processing
    ⚠️  Applications with many external API calls
    
    Key strategies for Flask performance:
    1. Use appropriate worker configuration (Gunicorn/uWSGI)
    2. Implement connection pooling (DB, Redis, HTTP)
    3. Add caching layers (Redis, Memcached)
    4. Offload background work (Celery, RQ)
    5. Monitor and profile continuously
    
    Consider alternatives when:
    1. You need native async/WebSocket support → FastAPI, Quart
    2. You need built-in admin/auth → Django
    3. Extreme performance is critical → Sanic, aiohttp
    
    Remember: Many performance issues can be solved with proper
    architecture and optimization, regardless of framework!
    """)

# ============================================================================
# CONFIGURATION EXAMPLES
# ============================================================================

def generate_configuration_files():
    """
    Generate example configuration files
    """
    
    # Gunicorn config
    gunicorn_conf = """
# gunicorn_config.py
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Process naming
proc_name = "flask_app"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process management
graceful_timeout = 30
"""
    
    # Dockerfile for optimized Flask deployment
    dockerfile = """
# Dockerfile for Flask with performance optimizations
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Create virtual environment
RUN python -m venv venv
ENV PATH="/home/appuser/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Gunicorn configuration
ENV GUNICORN_CMD_ARGS="--workers=4 --threads=2 --worker-class=gthread --bind=0.0.0.0:8000"

# Run application
CMD ["gunicorn", "app:app"]
"""
    
    # Supervisor config
    supervisor_conf = """
[program:flask_app]
command=/path/to/venv/bin/gunicorn --workers=4 --threads=2 --worker-class=gthread --bind=unix:/tmp/flask_app.sock app:app
directory=/path/to/your/app
user=www-data
group=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/flask_app.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
"""
    
    print("\n" + "="*60)
    print("SAMPLE CONFIGURATION FILES")
    print("="*60)
    print("\nGunicorn Configuration (gunicorn_config.py):")
    print(gunicorn_conf[:500] + "...")
    
    print("\nDockerfile:")
    print(dockerfile[:500] + "...")
    
    print("\nSupervisor Configuration:")
    print(supervisor_conf)

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask Performance & Scalability Demo')
    parser.add_argument('--demo', action='store_true', help='Run comprehensive demo')
    parser.add_argument('--configs', action='store_true', help='Show configuration examples')
    parser.add_argument('--run', action='store_true', help='Run Flask app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run app on')
    
    args = parser.parse_args()
    
    if args.demo:
        run_comprehensive_demo()
    elif args.configs:
        generate_configuration_files()
    elif args.run:
        # Run the Flask application
        print(f"\nStarting Flask performance demo on http://localhost:{args.port}")
        print("\nAvailable endpoints:")
        print("  GET  /sync-endpoint          - Synchronous endpoint (blocks for 2s)")
        print("  GET  /monitored-endpoint     - Performance monitored endpoint")
        print("  GET  /cache-simple           - Simple caching example")
        print("  GET  /cache-memoize/<id>     - Memoized caching by user ID")
        print("  GET  /cache-database         - Database query caching")
        print("  GET  /trigger-celery-task    - Start Celery background task")
        print("  GET  /trigger-rq-job         - Start RQ background job")
        print("\nUse --demo flag to see comprehensive performance guide")
        
        app.run(debug=True, port=args.port)
    else:
        print("Usage: python flask_performance.py [--demo|--configs|--run]")
        print("\nOptions:")
        print("  --demo      Run comprehensive performance demo")
        print("  --configs   Show configuration examples")
        print("  --run       Run Flask application")