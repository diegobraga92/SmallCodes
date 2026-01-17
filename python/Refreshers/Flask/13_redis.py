"""
COMPREHENSIVE REDIS GUIDE FOR FLASK APPLICATIONS
This guide covers Redis fundamentals, integration with Flask, and practical examples.
"""

import os
import json
import time
import pickle
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional, List, Dict, Union, Tuple
import logging
from enum import Enum
import asyncio
import threading
from contextlib import contextmanager

# ============================================================================
# 1. REDIS OVERVIEW - FUNDAMENTALS
# ============================================================================

class RedisOverview:
    """
    Comprehensive overview of Redis - the in-memory data structure store
    """
    
    @staticmethod
    def redis_fundamentals():
        """
        Redis: RE mote DI ctionary S erver
        In-memory data structure store used as database, cache, and message broker
        """
        
        print("\n" + "="*80)
        print("REDIS OVERVIEW - COMPREHENSIVE GUIDE")
        print("="*80)
        
        fundamentals = """
        WHAT IS REDIS?
        --------------
        Redis (Remote Dictionary Server) is an open-source, in-memory data 
        structure store used as:
        1. Database
        2. Cache 
        3. Message broker
        4. Queue
        
        KEY CHARACTERISTICS:
        --------------------
        1. IN-MEMORY: Extremely fast (microsecond operations)
        2. DATA STRUCTURES: Strings, Lists, Sets, Hashes, Sorted Sets, Streams
        3. PERSISTENCE: Optional disk persistence (RDB snapshots, AOF logs)
        4. REPLICATION: Master-slave replication
        5. CLUSTERING: Automatic partitioning across multiple nodes
        6. PUB/SUB: Publish-subscribe messaging
        7. TRANSACTIONS: Multi-command atomic operations
        8. LUA SCRIPTING: Server-side scripts
        
        WHY USE REDIS WITH FLASK?
        -------------------------
        1. CACHE API responses → Reduce database load
        2. SESSION STORE → Fast, distributed sessions
        3. RATE LIMITING → Track request counts
        4. BACKGROUND JOBS → Task queues (Celery/RQ)
        5. REAL-TIME FEATURES → Pub/Sub, WebSockets
        6. LEADERBOARDS → Sorted sets for rankings
        7. DISTRIBUTED LOCKING → Coordinating across workers
        
        PERFORMANCE NUMBERS:
        --------------------
        Operations/second: 100,000+ (single node)
        Latency: <1ms for most operations
        Concurrent connections: 50,000+ per instance
        
        DATA SIZE LIMITS:
        -----------------
        Maximum key size: 512 MB
        Maximum value size: 512 MB
        Maximum database size: Memory limit (configurable)
        
        PERSISTENCE OPTIONS:
        --------------------
        1. RDB (Redis Database Backup)
           - Point-in-time snapshots
           - Good for backups
           - Faster restart
        
        2. AOF (Append Only File)
           - Logs every write operation
           - More durable
           - Slower restart
        
        3. RDB + AOF (Recommended for production)
           - Combines both approaches
           - Best durability with good performance
        """
        
        print(fundamentals)
    
    @staticmethod
    def data_structures_detailed():
        """
        Detailed explanation of Redis data structures
        """
        
        print("\n" + "="*80)
        print("REDIS DATA STRUCTURES")
        print("="*80)
        
        data_structures = {
            'STRING': {
                'description': 'Basic key-value pair, binary safe',
                'max_size': '512 MB',
                'operations': ['GET', 'SET', 'INCR', 'DECR', 'APPEND', 'GETRANGE'],
                'use_cases': [
                    'Caching HTML fragments',
                    'Counter values',
                    'JSON strings',
                    'Simple key-value storage'
                ],
                'flask_example': 'cache.set("user:1:profile", json.dumps(user_data))'
            },
            
            'HASH': {
                'description': 'Field-value maps, perfect for objects',
                'max_fields': '4 billion',
                'operations': ['HSET', 'HGET', 'HGETALL', 'HDEL', 'HINCRBY'],
                'use_cases': [
                    'User profiles (fields: name, email, age)',
                    'Product information',
                    'Configuration objects',
                    'Shopping cart items'
                ],
                'flask_example': 'redis.hset("user:1", mapping={"name": "John", "email": "john@example.com"})'
            },
            
            'LIST': {
                'description': 'Ordered collection of strings',
                'max_elements': '4 billion',
                'operations': ['LPUSH', 'RPUSH', 'LPOP', 'RPOP', 'LRANGE', 'LTRIM'],
                'use_cases': [
                    'Message queues',
                    'Activity feeds',
                    'Task queues',
                    'Recent items'
                ],
                'flask_example': 'redis.lpush("recent:users", user_id)'
            },
            
            'SET': {
                'description': 'Unordered collection of unique strings',
                'max_members': '4 billion',
                'operations': ['SADD', 'SREM', 'SISMEMBER', 'SMEMBERS', 'SINTER', 'SUNION'],
                'use_cases': [
                    'Unique visitors tracking',
                    'Tags/categories',
                    'Friends/followers',
                    'User roles/permissions'
                ],
                'flask_example': 'redis.sadd("article:123:tags", "python", "redis", "flask")'
            },
            
            'SORTED SET': {
                'description': 'Set with score-based ordering',
                'max_members': '4 billion',
                'operations': ['ZADD', 'ZRANGE', 'ZREVRANGE', 'ZSCORE', 'ZRANK'],
                'use_cases': [
                    'Leaderboards',
                    'Priority queues',
                    'Time-series data',
                    'Ranked listings'
                ],
                'flask_example': 'redis.zadd("leaderboard", {"player:1": 1000, "player:2": 850})'
            },
            
            'STREAM': {
                'description': 'Append-only log (Redis 5.0+)',
                'operations': ['XADD', 'XREAD', 'XRANGE', 'XGROUP'],
                'use_cases': [
                    'Event sourcing',
                    'Message streaming',
                    'Activity logs',
                    'Real-time notifications'
                ],
                'flask_example': 'redis.xadd("user:activity", {"user_id": "1", "action": "login"})'
            },
            
            'BITMAP': {
                'description': 'Bit array operations',
                'operations': ['SETBIT', 'GETBIT', 'BITCOUNT', 'BITOP'],
                'use_cases': [
                    'Real-time analytics',
                    'Feature flags',
                    'User presence',
                    'Bloom filters'
                ],
                'flask_example': 'redis.setbit("daily_active:2024-01-15", user_id, 1)'
            },
            
            'HYPERLOGLOG': {
                'description': 'Probabilistic cardinality estimator',
                'error_rate': '0.81%',
                'operations': ['PFADD', 'PFCOUNT', 'PFMERGE'],
                'use_cases': [
                    'Unique visitors (approximate)',
                    'Distinct elements counting',
                    'Analytics with huge datasets'
                ],
                'flask_example': 'redis.pfadd("daily_visitors:2024-01-15", user_ip)'
            },
            
            'GEO': {
                'description': 'Geospatial indexing',
                'operations': ['GEOADD', 'GEODIST', 'GEORADIUS', 'GEOHASH'],
                'use_cases': [
                    'Location-based services',
                    'Find nearby points',
                    'Delivery tracking',
                    'Ride-sharing apps'
                ],
                'flask_example': 'redis.geoadd("stores", longitude, latitude, "store:123")'
            }
        }
        
        for ds_name, ds_info in data_structures.items():
            print(f"\n{ds_name}:")
            print(f"  Description: {ds_info['description']}")
            print(f"  Use Cases: {', '.join(ds_info['use_cases'][:2])}...")
            if 'flask_example' in ds_info:
                print(f"  Flask Example: {ds_info['flask_example']}")
    
    @staticmethod
    def redis_vs_alternatives():
        """
        Comparison with other caching/storage solutions
        """
        
        print("\n" + "="*80)
        print("REDIS VS ALTERNATIVES")
        print("="*80)
        
        comparison = {
            'Memcached': {
                'type': 'Simple key-value cache',
                'data_structures': 'Only strings',
                'persistence': 'No',
                'replication': 'Limited',
                'clustering': 'No built-in',
                'use_case': 'Simple caching only',
                'flask_suitability': 'Good for simple caching'
            },
            
            'MongoDB': {
                'type': 'Document database',
                'data_structures': 'Documents (JSON-like)',
                'persistence': 'Disk-based',
                'replication': 'Yes',
                'clustering': 'Yes (sharding)',
                'use_case': 'Document storage, complex queries',
                'flask_suitability': 'Primary database, not cache'
            },
            
            'PostgreSQL': {
                'type': 'Relational database',
                'data_structures': 'Tables, rows',
                'persistence': 'Disk-based',
                'replication': 'Yes',
                'clustering': 'Limited',
                'use_case': 'Transactional data, complex queries',
                'flask_suitability': 'Primary database, ACID compliance'
            },
            
            'RabbitMQ': {
                'type': 'Message broker',
                'data_structures': 'Queues, exchanges',
                'persistence': 'Optional',
                'replication': 'Yes',
                'clustering': 'Yes',
                'use_case': 'Message queuing, enterprise messaging',
                'flask_suitability': 'Background jobs, complex routing'
            },
            
            'Redis': {
                'type': 'In-memory data structure store',
                'data_structures': 'Rich: strings, hashes, lists, sets, sorted sets, streams',
                'persistence': 'Optional (RDB/AOF)',
                'replication': 'Yes (master-slave)',
                'clustering': 'Yes (Redis Cluster)',
                'use_case': 'Cache, session store, real-time features',
                'flask_suitability': 'Excellent: versatile, fast, easy integration'
            }
        }
        
        for system, info in comparison.items():
            print(f"\n{system.upper()}:")
            print(f"  Type: {info['type']}")
            print(f"  Data Structures: {info['data_structures']}")
            print(f"  Flask Use: {info['flask_suitability']}")

# ============================================================================
# 2. REDIS USAGES WITH FLASK - COMPREHENSIVE INTEGRATION
# ============================================================================

from flask import Flask, request, jsonify, session, g, current_app
import redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'redis-demo-secret')

class FlaskRedisIntegration:
    """
    Comprehensive Redis integration patterns for Flask
    """
    
    @staticmethod
    def setup_redis_connection():
        """
        Setup Redis connection with best practices
        """
        
        print("\n" + "="*80)
        print("REDIS CONNECTION SETUP FOR FLASK")
        print("="*80)
        
        connection_configs = {
            'basic': {
                'code': """
                import redis
                
                # Basic connection
                redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=True  # Return strings instead of bytes
                )
                """,
                'description': 'Simple local connection'
            },
            
            'production': {
                'code': """
                import redis
                
                # Production-ready connection with pooling
                redis_client = redis.Redis(
                    host=os.environ.get('REDIS_HOST', 'localhost'),
                    port=int(os.environ.get('REDIS_PORT', 6379)),
                    db=int(os.environ.get('REDIS_DB', 0)),
                    password=os.environ.get('REDIS_PASSWORD'),
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    max_connections=50,
                    health_check_interval=30
                )
                """,
                'description': 'Production with connection pooling and timeouts'
            },
            
            'connection_pool': {
                'code': """
                import redis
                
                # Connection pool for better performance
                redis_pool = redis.ConnectionPool(
                    host='localhost',
                    port=6379,
                    db=0,
                    max_connections=50,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True
                )
                
                # Create client using pool
                redis_client = redis.Redis(connection_pool=redis_pool)
                
                # Reuse the same pool across your application
                """,
                'description': 'Explicit connection pool management'
            },
            
            'ssl_tls': {
                'code': """
                import redis
                import ssl
                
                # SSL/TLS connection for secure Redis
                redis_client = redis.Redis(
                    host='redis.example.com',
                    port=6380,  # Redis SSL port
                    password=os.environ.get('REDIS_PASSWORD'),
                    ssl=True,
                    ssl_cert_reqs=ssl.CERT_REQUIRED,
                    ssl_ca_certs='/path/to/ca.pem',
                    decode_responses=True
                )
                """,
                'description': 'Secure Redis connection over SSL/TLS'
            },
            
            'sentinel': {
                'code': """
                import redis
                from redis.sentinel import Sentinel
                
                # Redis Sentinel for high availability
                sentinel = Sentinel([
                    ('sentinel1.example.com', 26379),
                    ('sentinel2.example.com', 26379),
                    ('sentinel3.example.com', 26379)
                ], socket_timeout=0.5)
                
                # Get master instance
                master = sentinel.master_for('mymaster', 
                    socket_timeout=0.5, 
                    password=os.environ.get('REDIS_PASSWORD'),
                    decode_responses=True
                )
                
                # Get slave instance for read operations
                slave = sentinel.slave_for('mymaster',
                    socket_timeout=0.5,
                    password=os.environ.get('REDIS_PASSWORD'),
                    decode_responses=True
                )
                """,
                'description': 'High availability with Redis Sentinel'
            },
            
            'cluster': {
                'code': """
                from redis.cluster import RedisCluster
                
                # Redis Cluster for horizontal scaling
                redis_client = RedisCluster(
                    startup_nodes=[
                        {'host': 'redis-cluster-node1', 'port': 6379},
                        {'host': 'redis-cluster-node2', 'port': 6379},
                        {'host': 'redis-cluster-node3', 'port': 6379}
                    ],
                    decode_responses=True,
                    socket_timeout=5,
                    retry_on_timeout=True,
                    password=os.environ.get('REDIS_PASSWORD')
                )
                """,
                'description': 'Redis Cluster for distributed data'
            }
        }
        
        for config_name, config in connection_configs.items():
            print(f"\n{config_name.upper()}:")
            print(f"Description: {config['description']}")
            print(f"Code:\n{config['code']}")
    
    @staticmethod
    def flask_redis_extensions():
        """
        Popular Flask-Redis extensions and their usage
        """
        
        print("\n" + "="*80)
        print("FLASK-REDIS EXTENSIONS")
        print("="*80)
        
        extensions = {
            'Flask-Redis': {
                'description': 'Simple Redis integration for Flask',
                'installation': 'pip install flask-redis',
                'usage': """
                from flask_redis import FlaskRedis
                
                redis_store = FlaskRedis()
                
                def create_app():
                    app = Flask(__name__)
                    redis_store.init_app(app)
                    return app
                
                # Usage
                redis_store.set('key', 'value')
                redis_store.get('key')
                """,
                'features': 'Simple, automatic configuration from app config'
            },
            
            'Flask-Caching': {
                'description': 'Caching support for Flask with multiple backends',
                'installation': 'pip install Flask-Caching',
                'usage': """
                from flask_caching import Cache
                
                cache = Cache(config={'CACHE_TYPE': 'redis'})
                
                def create_app():
                    app = Flask(__name__)
                    cache.init_app(app)
                    return app
                
                # Caching decorator
                @app.route('/expensive')
                @cache.cached(timeout=300)
                def expensive_operation():
                    return expensive_computation()
                """,
                'features': 'Built-in caching decorators, multiple backends'
            },
            
            'Flask-Session': {
                'description': 'Server-side session extension for Flask',
                'installation': 'pip install Flask-Session',
                'usage': """
                from flask_session import Session
                
                app.config['SESSION_TYPE'] = 'redis'
                app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
                
                sess = Session()
                sess.init_app(app)
                
                # Sessions automatically stored in Redis
                session['user_id'] = 123
                """,
                'features': 'Server-side sessions, multiple storage backends'
            },
            
            'Celery': {
                'description': 'Distributed task queue with Redis broker',
                'installation': 'pip install celery',
                'usage': """
                from celery import Celery
                
                celery = Celery(
                    'tasks',
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/1'
                )
                
                @celery.task
                def process_data(data):
                    # Long-running task
                    return process(data)
                
                # In Flask route
                process_data.delay(data)
                """,
                'features': 'Background jobs, scheduling, task routing'
            },
            
            'RQ (Redis Queue)': {
                'description': 'Simple job queues for Python',
                'installation': 'pip install rq',
                'usage': """
                import redis
                from rq import Queue
                
                redis_conn = redis.Redis()
                q = Queue(connection=redis_conn)
                
                def process_data(data):
                    return process(data)
                
                # Enqueue job
                job = q.enqueue(process_data, data)
                """,
                'features': 'Simpler than Celery, good for basic job queues'
            }
        }
        
        for ext_name, ext_info in extensions.items():
            print(f"\n{ext_name}:")
            print(f"Description: {ext_info['description']}")
            print(f"Features: {ext_info['features']}")

# ============================================================================
# 3. REDIS EXAMPLES WITH FLASK - PRACTICAL IMPLEMENTATIONS
# ============================================================================

# Initialize Redis connection for examples
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    db=int(os.environ.get('REDIS_DB', 0)),
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True
)

class RedisFlaskExamples:
    """
    Practical Redis examples for Flask applications
    """
    
    # ============================================================================
    # 3.1 CACHING PATTERNS
    # ============================================================================
    
    class CachingExamples:
        """
        Comprehensive caching strategies with Redis
        """
        
        @staticmethod
        def cache_decorator_factory():
            """
            Factory for creating cache decorators
            """
            
            def cache_it(ttl: int = 300, key_prefix: str = "cache"):
                """
                Generic caching decorator
                
                Args:
                    ttl: Time to live in seconds
                    key_prefix: Prefix for cache keys
                """
                
                def decorator(f):
                    @wraps(f)
                    def decorated_function(*args, **kwargs):
                        # Generate cache key from function name and arguments
                        cache_key = f"{key_prefix}:{f.__module__}:{f.__name__}"
                        
                        # Add args to cache key
                        if args:
                            args_hash = hashlib.md5(str(args).encode()).hexdigest()[:8]
                            cache_key += f":args:{args_hash}"
                        
                        # Add kwargs to cache key  
                        if kwargs:
                            kwargs_hash = hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()[:8]
                            cache_key += f":kwargs:{kwargs_hash}"
                        
                        # Try to get from cache
                        cached_data = redis_client.get(cache_key)
                        
                        if cached_data is not None:
                            # Cache hit
                            current_app.logger.debug(f"Cache HIT: {cache_key}")
                            return json.loads(cached_data)
                        
                        # Cache miss - execute function
                        current_app.logger.debug(f"Cache MISS: {cache_key}")
                        result = f(*args, **kwargs)
                        
                        # Store in cache
                        try:
                            redis_client.setex(
                                cache_key,
                                ttl,
                                json.dumps(result)
                            )
                        except RedisError as e:
                            current_app.logger.error(f"Redis cache error: {e}")
                            # Don't fail the request if cache fails
                        
                        return result
                    
                    return decorated_function
                
                return decorator
            
            return cache_it
        
        @staticmethod
        @app.route('/api/users/<int:user_id>')
        def get_user_cached(user_id):
            """
            Cached user endpoint example
            """
            # Check cache first
            cache_key = f"user:{user_id}:profile"
            cached_user = redis_client.get(cache_key)
            
            if cached_user:
                return jsonify({
                    'source': 'cache',
                    'data': json.loads(cached_user),
                    'cached_at': 'Now'
                })
            
            # Simulate database query
            time.sleep(1)  # Expensive operation
            
            user_data = {
                'id': user_id,
                'name': f'User {user_id}',
                'email': f'user{user_id}@example.com',
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Store in cache (5 minutes TTL)
            redis_client.setex(cache_key, 300, json.dumps(user_data))
            
            return jsonify({
                'source': 'database',
                'data': user_data,
                'cached': True
            })
        
        @staticmethod
        def fragment_caching():
            """
            Fragment caching for partial page content
            """
            
            @app.route('/dashboard')
            def user_dashboard():
                """
                Dashboard with multiple cacheable fragments
                """
                user_id = session.get('user_id', 1)
                
                # Cache key for each fragment
                recent_activity_key = f"user:{user_id}:recent_activity"
                stats_key = f"user:{user_id}:stats"
                recommendations_key = f"user:{user_id}:recommendations"
                
                # Try to get fragments from cache
                recent_activity = redis_client.get(recent_activity_key)
                stats = redis_client.get(stats_key)
                recommendations = redis_client.get(recommendations_key)
                
                # If any fragment is missing, compute it
                if not recent_activity:
                    recent_activity = compute_recent_activity(user_id)
                    redis_client.setex(recent_activity_key, 60, recent_activity)
                
                if not stats:
                    stats = compute_user_stats(user_id)
                    redis_client.setex(stats_key, 300, stats)
                
                if not recommendations:
                    recommendations = compute_recommendations(user_id)
                    redis_client.setex(recommendations_key, 3600, recommendations)
                
                return jsonify({
                    'recent_activity': recent_activity,
                    'stats': stats,
                    'recommendations': recommendations
                })
        
        @staticmethod
        def cache_invalidation_patterns():
            """
            Different cache invalidation strategies
            """
            
            class CacheInvalidator:
                """Handles cache invalidation strategies"""
                
                @staticmethod
                def time_based_invalidation():
                    """
                    Simple TTL-based invalidation
                    """
                    # Set with expiration
                    redis_client.setex("user:1:profile", 300, "user_data")
                    # Automatically expires after 5 minutes
                
                @staticmethod
                def tag_based_invalidation():
                    """
                    Tag-based cache invalidation
                    """
                    user_id = 1
                    cache_key = f"user:{user_id}:profile"
                    tag_key = f"cache_tag:user:{user_id}"
                    
                    # Store data with tag reference
                    redis_client.set(cache_key, "user_data")
                    redis_client.sadd(tag_key, cache_key)
                    
                    # Invalidate all cache entries for user
                    def invalidate_user_cache(user_id):
                        tag_key = f"cache_tag:user:{user_id}"
                        cache_keys = redis_client.smembers(tag_key)
                        
                        for key in cache_keys:
                            redis_client.delete(key)
                        
                        redis_client.delete(tag_key)
                
                @staticmethod
                def version_based_invalidation():
                    """
                    Version-based cache invalidation
                    """
                    cache_version = "v2"  # Change when data format changes
                    cache_key = f"user:1:profile:{cache_version}"
                    
                    # Store with version
                    redis_client.set(cache_key, "user_data")
                    
                    # Old versions automatically become stale
                
                @staticmethod
                def write_through_cache():
                    """
                    Update cache when data is updated
                    """
                    def update_user_profile(user_id, data):
                        # Update database
                        update_database(user_id, data)
                        
                        # Update cache
                        cache_key = f"user:{user_id}:profile"
                        redis_client.setex(cache_key, 300, json.dumps(data))
                
                @staticmethod
                def cache_aside_pattern():
                    """
                    Application-managed cache (most common)
                    """
                    def get_user_profile(user_id):
                        cache_key = f"user:{user_id}:profile"
                        
                        # 1. Check cache
                        cached = redis_client.get(cache_key)
                        if cached:
                            return json.loads(cached)
                        
                        # 2. Load from database
                        data = load_from_database(user_id)
                        
                        # 3. Update cache
                        redis_client.setex(cache_key, 300, json.dumps(data))
                        
                        return data
            
            return CacheInvalidator
        
        @staticmethod
        def advanced_caching_patterns():
            """
            Advanced caching patterns
            """
            
            patterns = {
                'Cache Stampede Prevention': """
                # Prevent multiple requests from recomputing same data
                
                import redis
                import time
                
                def get_with_stampede_prevention(key, ttl, compute_func):
                    # Try normal cache get
                    data = redis_client.get(key)
                    if data:
                        return json.loads(data)
                    
                    # Try to acquire lock
                    lock_key = f"{key}:lock"
                    lock_acquired = redis_client.setnx(lock_key, "1")
                    
                    if lock_acquired:
                        redis_client.expire(lock_key, 10)  # Lock timeout
                        try:
                            # Compute fresh data
                            data = compute_func()
                            redis_client.setex(key, ttl, json.dumps(data))
                            return data
                        finally:
                            # Release lock
                            redis_client.delete(lock_key)
                    else:
                        # Wait for other process to compute
                        for _ in range(10):  # Wait up to 1 second
                            time.sleep(0.1)
                            data = redis_client.get(key)
                            if data:
                                return json.loads(data)
                        
                        # Fallback to computation
                        return compute_func()
                """,
                
                'Two-Level Caching': """
                # Local memory cache + Redis cache
                
                from cachetools import TTLCache
                import redis
                
                # Local in-memory cache (fast, limited size)
                local_cache = TTLCache(maxsize=1000, ttl=60)
                
                def get_with_two_level_cache(key, ttl, compute_func):
                    # 1. Check local cache
                    if key in local_cache:
                        return local_cache[key]
                    
                    # 2. Check Redis cache
                    data = redis_client.get(key)
                    if data:
                        data = json.loads(data)
                        local_cache[key] = data  # Populate local cache
                        return data
                    
                    # 3. Compute and cache at both levels
                    data = compute_func()
                    redis_client.setex(key, ttl, json.dumps(data))
                    local_cache[key] = data
                    return data
                """,
                
                'Cache Warming': """
                # Pre-populate cache before peak loads
                
                def warm_user_cache(user_ids):
                    for user_id in user_ids:
                        cache_key = f"user:{user_id}:profile"
                        if not redis_client.exists(cache_key):
                            user_data = load_user_from_db(user_id)
                            redis_client.setex(
                                cache_key, 
                                3600,  # 1 hour
                                json.dumps(user_data)
                            )
                
                # Run before expected traffic spikes
                # Example: Before product launch, before marketing campaign
                """
            }
            
            print("\n" + "="*80)
            print("ADVANCED CACHING PATTERNS")
            print("="*80)
            
            for pattern_name, pattern_code in patterns.items():
                print(f"\n{pattern_name}:")
                print(pattern_code)
    
    # ============================================================================
    # 3.2 SESSION STORAGE WITH REDIS
    # ============================================================================
    
    class SessionExamples:
        """
        Redis-based session management
        """
        
        @staticmethod
        def custom_redis_session():
            """
            Custom Redis session implementation
            """
            
            def generate_session_id():
                """Generate secure session ID"""
                return secrets.token_urlsafe(32)
            
            class RedisSession:
                """Custom Redis-based session store"""
                
                def __init__(self, redis_client, ttl=3600):
                    self.redis = redis_client
                    self.ttl = ttl  # Session timeout in seconds
                
                def create_session(self, user_data):
                    """Create new session"""
                    session_id = generate_session_id()
                    session_key = f"session:{session_id}"
                    
                    session_data = {
                        'user_id': user_data['id'],
                        'created_at': datetime.utcnow().isoformat(),
                        'last_activity': datetime.utcnow().isoformat(),
                        'user_agent': request.headers.get('User-Agent', ''),
                        'ip_address': request.remote_addr,
                        **user_data
                    }
                    
                    # Store session in Redis
                    self.redis.hset(session_key, mapping=session_data)
                    self.redis.expire(session_key, self.ttl)
                    
                    return session_id
                
                def get_session(self, session_id):
                    """Retrieve session data"""
                    session_key = f"session:{session_id}"
                    
                    # Check if session exists
                    if not self.redis.exists(session_key):
                        return None
                    
                    # Get session data
                    session_data = self.redis.hgetall(session_key)
                    
                    # Update last activity
                    session_data['last_activity'] = datetime.utcnow().isoformat()
                    self.redis.hset(session_key, 'last_activity', session_data['last_activity'])
                    self.redis.expire(session_key, self.ttl)  # Reset TTL
                    
                    return session_data
                
                def destroy_session(self, session_id):
                    """Destroy session"""
                    session_key = f"session:{session_id}"
                    self.redis.delete(session_key)
                
                def update_session(self, session_id, updates):
                    """Update session data"""
                    session_key = f"session:{session_id}"
                    
                    if self.redis.exists(session_key):
                        self.redis.hset(session_key, mapping=updates)
                        self.redis.expire(session_key, self.ttl)
                        return True
                    return False
                
                def find_sessions_by_user(self, user_id):
                    """Find all sessions for a user (for admin purposes)"""
                    # Note: This is inefficient for large datasets
                    # Better to maintain a separate index
                    pattern = f"session:*"
                    sessions = []
                    
                    for key in self.redis.scan_iter(match=pattern):
                        session_data = self.redis.hgetall(key)
                        if session_data.get('user_id') == str(user_id):
                            sessions.append({
                                'session_id': key.split(':')[1],
                                **session_data
                            })
                    
                    return sessions
            
            return RedisSession
        
        @staticmethod
        @app.route('/api/login', methods=['POST'])
        def login_with_redis_session():
            """Login endpoint with Redis sessions"""
            data = request.json
            
            # Authentication logic
            username = data.get('username')
            password = data.get('password')
            
            # Validate credentials (simplified)
            if username == 'test' and password == 'password':
                user_data = {
                    'id': 1,
                    'username': username,
                    'email': 'test@example.com',
                    'role': 'user'
                }
                
                # Create session store instance
                session_store = RedisFlaskExamples.SessionExamples.custom_redis_session()(
                    redis_client, 
                    ttl=7200  # 2 hour sessions
                )
                
                # Create session
                session_id = session_store.create_session(user_data)
                
                response = jsonify({
                    'message': 'Login successful',
                    'user': user_data
                })
                
                # Set session cookie
                response.set_cookie(
                    'session_id',
                    session_id,
                    httponly=True,
                    secure=True,  # Only over HTTPS
                    samesite='Lax',
                    max_age=7200
                )
                
                return response
            
            return jsonify({'error': 'Invalid credentials'}), 401
        
        @staticmethod
        def session_middleware():
            """
            Session middleware using Redis
            """
            
            def session_middleware_decorator(f):
                @wraps(f)
                def decorated_function(*args, **kwargs):
                    # Get session ID from cookie
                    session_id = request.cookies.get('session_id')
                    
                    if session_id:
                        # Create session store
                        session_store = RedisFlaskExamples.SessionExamples.custom_redis_session()(
                            redis_client,
                            ttl=7200
                        )
                        
                        # Get session data
                        session_data = session_store.get_session(session_id)
                        
                        if session_data:
                            # Add session to Flask's g object
                            g.session = session_data
                            g.session_id = session_id
                        else:
                            # Invalid session
                            g.session = None
                            g.session_id = None
                    else:
                        g.session = None
                        g.session_id = None
                    
                    return f(*args, **kwargs)
                
                return decorated_function
            
            return session_middleware_decorator
        
        @staticmethod
        @app.route('/api/profile')
        @session_middleware()
        def protected_profile():
            """Protected endpoint requiring session"""
            if not g.session:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Access session data
            user_id = g.session.get('user_id')
            username = g.session.get('username')
            
            return jsonify({
                'user_id': user_id,
                'username': username,
                'authenticated': True
            })
    
    # ============================================================================
    # 3.3 RATE LIMITING WITH REDIS
    # ============================================================================
    
    class RateLimitingExamples:
        """
        Redis-based rate limiting implementations
        """
        
        @staticmethod
        def sliding_window_rate_limiter():
            """
            Sliding window rate limiter using Redis
            More accurate than fixed window
            """
            
            class SlidingWindowRateLimiter:
                """Sliding window rate limiter implementation"""
                
                def __init__(self, redis_client, limit, window):
                    """
                    Args:
                        redis_client: Redis connection
                        limit: Maximum requests allowed
                        window: Time window in seconds
                    """
                    self.redis = redis_client
                    self.limit = limit
                    self.window = window
                
                def is_allowed(self, key):
                    """
                    Check if request is allowed
                    
                    Args:
                        key: Rate limit key (e.g., "ip:127.0.0.1" or "user:1")
                    
                    Returns:
                        tuple: (allowed, remaining, reset_time)
                    """
                    current_time = time.time()
                    window_start = current_time - self.window
                    
                    # Redis key for this rate limit window
                    redis_key = f"ratelimit:{key}"
                    
                    # Remove old timestamps
                    self.redis.zremrangebyscore(redis_key, 0, window_start)
                    
                    # Count requests in current window
                    current_count = self.redis.zcard(redis_key)
                    
                    if current_count < self.limit:
                        # Add current request timestamp
                        self.redis.zadd(redis_key, {current_time: current_time})
                        self.redis.expire(redis_key, self.window)
                        
                        remaining = self.limit - current_count - 1
                        reset_time = window_start + self.window
                        
                        return True, remaining, reset_time
                    else:
                        # Get oldest request to calculate reset time
                        oldest = self.redis.zrange(redis_key, 0, 0, withscores=True)
                        if oldest:
                            reset_time = oldest[0][1] + self.window
                        else:
                            reset_time = current_time + self.window
                        
                        remaining = 0
                        return False, remaining, reset_time
            
            return SlidingWindowRateLimiter
        
        @staticmethod
        def token_bucket_rate_limiter():
            """
            Token bucket rate limiter using Redis
            Allows bursts but controls average rate
            """
            
            class TokenBucketRateLimiter:
                """Token bucket rate limiter implementation"""
                
                def __init__(self, redis_client, capacity, refill_rate):
                    """
                    Args:
                        redis_client: Redis connection
                        capacity: Maximum tokens in bucket
                        refill_rate: Tokens added per second
                    """
                    self.redis = redis_client
                    self.capacity = capacity
                    self.refill_rate = refill_rate
                
                def is_allowed(self, key, tokens=1):
                    """
                    Check if request is allowed
                    
                    Args:
                        key: Rate limit key
                        tokens: Tokens required for this request
                    
                    Returns:
                        tuple: (allowed, remaining, wait_time)
                    """
                    current_time = time.time()
                    
                    # Redis keys
                    tokens_key = f"tokenbucket:{key}:tokens"
                    timestamp_key = f"tokenbucket:{key}:timestamp"
                    
                    # Use Lua script for atomic operations
                    lua_script = """
                    local tokens_key = KEYS[1]
                    local timestamp_key = KEYS[2]
                    local current_time = tonumber(ARGV[1])
                    local capacity = tonumber(ARGV[2])
                    local refill_rate = tonumber(ARGV[3])
                    local tokens_requested = tonumber(ARGV[4])
                    
                    local last_time = redis.call('GET', timestamp_key)
                    local current_tokens = redis.call('GET', tokens_key)
                    
                    if not last_time then
                        last_time = current_time
                        current_tokens = capacity
                    else
                        last_time = tonumber(last_time)
                        current_tokens = tonumber(current_tokens)
                        
                        -- Calculate refilled tokens
                        local time_passed = current_time - last_time
                        local refill_amount = time_passed * refill_rate
                        current_tokens = math.min(capacity, current_tokens + refill_amount)
                    end
                    
                    -- Check if enough tokens
                    if current_tokens >= tokens_requested then
                        current_tokens = current_tokens - tokens_requested
                        redis.call('SET', tokens_key, current_tokens)
                        redis.call('SET', timestamp_key, current_time)
                        return {1, current_tokens, 0}
                    else
                        -- Calculate wait time
                        local tokens_needed = tokens_requested - current_tokens
                        local wait_time = tokens_needed / refill_rate
                        return {0, current_tokens, wait_time}
                    end
                    """
                    
                    # Execute Lua script
                    result = self.redis.eval(
                        lua_script,
                        2,  # Number of keys
                        tokens_key,
                        timestamp_key,
                        current_time,
                        self.capacity,
                        self.refill_rate,
                        tokens
                    )
                    
                    allowed = bool(result[0])
                    remaining = result[1]
                    wait_time = result[2]
                    
                    return allowed, remaining, wait_time
            
            return TokenBucketRateLimiter
        
        @staticmethod
        @app.route('/api/limited')
        def rate_limited_endpoint():
            """
            Endpoint with rate limiting
            """
            # Get client identifier
            client_id = request.remote_addr  # Use IP address
            # Or for authenticated users: client_id = f"user:{user_id}"
            
            # Create rate limiter
            limiter = RedisFlaskExamples.RateLimitingExamples.sliding_window_rate_limiter()(
                redis_client,
                limit=10,    # 10 requests
                window=60    # per 60 seconds
            )
            
            # Check rate limit
            allowed, remaining, reset_time = limiter.is_allowed(f"ip:{client_id}")
            
            if not allowed:
                retry_after = int(reset_time - time.time())
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': 'Too many requests',
                    'retry_after': retry_after,
                    'limit': 10,
                    'window': 60
                }), 429
            
            # Process request
            return jsonify({
                'message': 'Request successful',
                'rate_limit': {
                    'remaining': remaining,
                    'reset_time': datetime.fromtimestamp(reset_time).isoformat()
                }
            })
        
        @staticmethod
        def rate_limit_decorator():
            """
            Rate limit decorator for Flask routes
            """
            
            def rate_limit(limit=100, window=3600, key_func=None):
                """
                Decorator to rate limit Flask routes
                
                Args:
                    limit: Maximum requests allowed
                    window: Time window in seconds
                    key_func: Function to generate rate limit key
                """
                
                if key_func is None:
                    key_func = lambda: f"ip:{request.remote_addr}"
                
                def decorator(f):
                    @wraps(f)
                    def decorated_function(*args, **kwargs):
                        # Create rate limiter
                        limiter = RedisFlaskExamples.RateLimitingExamples.sliding_window_rate_limiter()(
                            redis_client,
                            limit=limit,
                            window=window
                        )
                        
                        # Get rate limit key
                        rate_limit_key = key_func()
                        
                        # Check rate limit
                        allowed, remaining, reset_time = limiter.is_allowed(
                            f"ratelimit:{f.__module__}:{f.__name__}:{rate_limit_key}"
                        )
                        
                        if not allowed:
                            retry_after = int(reset_time - time.time())
                            response = jsonify({
                                'error': 'Rate limit exceeded',
                                'message': f'Too many requests to {f.__name__}',
                                'retry_after': retry_after
                            })
                            response.headers['X-RateLimit-Limit'] = str(limit)
                            response.headers['X-RateLimit-Remaining'] = str(remaining)
                            response.headers['X-RateLimit-Reset'] = str(int(reset_time))
                            response.headers['Retry-After'] = str(retry_after)
                            return response, 429
                        
                        # Add rate limit headers
                        response = f(*args, **kwargs)
                        
                        if isinstance(response, tuple):
                            response_obj = response[0]
                        else:
                            response_obj = response
                        
                        response_obj.headers['X-RateLimit-Limit'] = str(limit)
                        response_obj.headers['X-RateLimit-Remaining'] = str(remaining)
                        response_obj.headers['X-RateLimit-Reset'] = str(int(reset_time))
                        
                        return response
                    
                    return decorated_function
                
                return decorator
            
            return rate_limit
        
        @staticmethod
        @app.route('/api/limited/decorated')
        @rate_limit(limit=5, window=60)
        def decorated_rate_limited_endpoint():
            """Endpoint with decorator-based rate limiting"""
            return jsonify({
                'message': 'This endpoint is rate limited to 5 requests per minute'
            })
    
    # ============================================================================
    # 3.4 TASK QUEUES WITH REDIS
    # ============================================================================
    
    class TaskQueueExamples:
        """
        Redis-based task queue implementations
        """
        
        @staticmethod
        def simple_task_queue():
            """
            Simple task queue using Redis lists
            """
            
            class SimpleTaskQueue:
                """Simple Redis-based task queue"""
                
                def __init__(self, redis_client, queue_name='tasks'):
                    self.redis = redis_client
                    self.queue_name = queue_name
                
                def enqueue(self, task_type, data):
                    """Add task to queue"""
                    task = {
                        'id': str(uuid.uuid4()),
                        'type': task_type,
                        'data': data,
                        'created_at': datetime.utcnow().isoformat(),
                        'status': 'queued'
                    }
                    
                    # Store task details
                    task_key = f"task:{task['id']}"
                    self.redis.hset(task_key, mapping=task)
                    self.redis.expire(task_key, 86400)  # 24 hours
                    
                    # Add to queue (left push)
                    self.redis.lpush(self.queue_name, task['id'])
                    
                    return task['id']
                
                def dequeue(self, timeout=0):
                    """Get next task from queue"""
                    # Blocking right pop
                    task_id = self.redis.brpop(self.queue_name, timeout=timeout)
                    
                    if task_id:
                        task_id = task_id[1]  # brpop returns (key, value)
                        task_key = f"task:{task_id}"
                        
                        # Get task details
                        task = self.redis.hgetall(task_key)
                        if task:
                            # Update status
                            task['status'] = 'processing'
                            task['started_at'] = datetime.utcnow().isoformat()
                            self.redis.hset(task_key, mapping=task)
                            
                            return task
                    
                    return None
                
                def complete(self, task_id, result=None, error=None):
                    """Mark task as completed"""
                    task_key = f"task:{task_id}"
                    
                    updates = {
                        'status': 'completed' if not error else 'failed',
                        'completed_at': datetime.utcnow().isoformat()
                    }
                    
                    if result:
                        updates['result'] = json.dumps(result)
                    
                    if error:
                        updates['error'] = str(error)
                    
                    self.redis.hset(task_key, mapping=updates)
                
                def get_status(self, task_id):
                    """Get task status"""
                    task_key = f"task:{task_id}"
                    return self.redis.hgetall(task_key)
            
            return SimpleTaskQueue
        
        @staticmethod
        def background_worker():
            """
            Background worker processing tasks
            """
            
            def start_background_worker():
                """Start background worker in separate thread"""
                
                def worker_process():
                    """Worker process function"""
                    queue = RedisFlaskExamples.TaskQueueExamples.simple_task_queue()(
                        redis_client,
                        queue_name='background_tasks'
                    )
                    
                    while True:
                        try:
                            # Get next task (blocking)
                            task = queue.dequeue(timeout=30)
                            
                            if task:
                                task_id = task['id']
                                task_type = task['type']
                                data = task['data']
                                
                                try:
                                    # Process task based on type
                                    if task_type == 'send_email':
                                        result = send_email_task(data)
                                        queue.complete(task_id, result=result)
                                    
                                    elif task_type == 'process_image':
                                        result = process_image_task(data)
                                        queue.complete(task_id, result=result)
                                    
                                    elif task_type == 'generate_report':
                                        result = generate_report_task(data)
                                        queue.complete(task_id, result=result)
                                    
                                    else:
                                        queue.complete(task_id, error=f"Unknown task type: {task_type}")
                                
                                except Exception as e:
                                    # Task failed
                                    queue.complete(task_id, error=str(e))
                                    current_app.logger.error(f"Task {task_id} failed: {e}")
                        
                        except Exception as e:
                            current_app.logger.error(f"Worker error: {e}")
                            time.sleep(5)  # Wait before retry
                
                # Start worker thread
                worker_thread = threading.Thread(target=worker_process, daemon=True)
                worker_thread.start()
                return worker_thread
            
            return start_background_worker
        
        @staticmethod
        @app.route('/api/tasks/send-email', methods=['POST'])
        def enqueue_email_task():
            """Endpoint to enqueue email sending task"""
            data = request.json
            
            # Create task queue
            task_queue = RedisFlaskExamples.TaskQueueExamples.simple_task_queue()(
                redis_client,
                queue_name='background_tasks'
            )
            
            # Enqueue task
            task_id = task_queue.enqueue(
                task_type='send_email',
                data={
                    'to': data.get('to'),
                    'subject': data.get('subject'),
                    'body': data.get('body'),
                    'requested_at': datetime.utcnow().isoformat()
                }
            )
            
            return jsonify({
                'message': 'Email task queued',
                'task_id': task_id,
                'status_endpoint': f'/api/tasks/{task_id}/status'
            })
        
        @staticmethod
        @app.route('/api/tasks/<task_id>/status', methods=['GET'])
        def get_task_status(task_id):
            """Check task status"""
            task_queue = RedisFlaskExamples.TaskQueueExamples.simple_task_queue()(
                redis_client,
                queue_name='background_tasks'
            )
            
            status = task_queue.get_status(task_id)
            
            if not status:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify(status)
        
        @staticmethod
        def scheduled_tasks_with_redis():
            """
            Scheduled/delayed tasks using Redis sorted sets
            """
            
            class ScheduledTaskQueue:
                """Scheduled task queue using Redis sorted sets"""
                
                def __init__(self, redis_client):
                    self.redis = redis_client
                    self.scheduled_set = 'scheduled_tasks'
                    self.ready_queue = 'ready_tasks'
                
                def schedule(self, task_type, data, execute_at):
                    """
                    Schedule task for future execution
                    
                    Args:
                        task_type: Type of task
                        data: Task data
                        execute_at: datetime when task should execute
                    """
                    task = {
                        'id': str(uuid.uuid4()),
                        'type': task_type,
                        'data': data,
                        'created_at': datetime.utcnow().isoformat(),
                        'execute_at': execute_at.isoformat(),
                        'status': 'scheduled'
                    }
                    
                    # Store task
                    task_key = f"scheduled_task:{task['id']}"
                    self.redis.hset(task_key, mapping=task)
                    
                    # Add to sorted set with score = execution timestamp
                    score = execute_at.timestamp()
                    self.redis.zadd(self.scheduled_set, {task['id']: score})
                    
                    return task['id']
                
                def check_scheduled_tasks(self):
                    """Move ready tasks to processing queue"""
                    current_time = time.time()
                    
                    # Get tasks whose execution time has passed
                    ready_tasks = self.redis.zrangebyscore(
                        self.scheduled_set,
                        0,
                        current_time
                    )
                    
                    for task_id in ready_tasks:
                        # Remove from scheduled set
                        self.redis.zrem(self.scheduled_set, task_id)
                        
                        # Add to ready queue
                        self.redis.lpush(self.ready_queue, task_id)
                        
                        # Update status
                        task_key = f"scheduled_task:{task_id}"
                        self.redis.hset(task_key, 'status', 'ready')
                    
                    return len(ready_tasks)
            
            return ScheduledTaskQueue
    
    # ============================================================================
    # 3.5 REAL-TIME FEATURES WITH REDIS PUB/SUB
    # ============================================================================
    
    class RealTimeExamples:
        """
        Real-time features using Redis Pub/Sub
        """
        
        @staticmethod
        def redis_pubsub_basics():
            """
            Redis Pub/Sub fundamentals
            """
            
            print("\n" + "="*80)
            print("REDIS PUB/SUB FOR REAL-TIME FEATURES")
            print("="*80)
            
            pubsub_info = """
            PUB/SUB CONCEPTS:
            -----------------
            Channels: Named message streams
            Publishers: Send messages to channels
            Subscribers: Receive messages from channels
            Pattern Subscriptions: Subscribe to multiple channels with patterns
            
            USE CASES:
            ----------
            1. Real-time notifications
            2. Live chat applications
            3. Live dashboards
            4. Event-driven architectures
            5. Cache invalidation notifications
            
            FLASK INTEGRATION PATTERNS:
            ---------------------------
            1. WebSocket + Redis Pub/Sub
               - Flask-SocketIO for WebSockets
               - Redis Pub/Sub for cross-process communication
            
            2. Server-Sent Events (SSE)
               - HTTP streaming for real-time updates
               - Redis Pub/Sub for event distribution
            
            3. Long Polling
               - Simple but less efficient
               - Redis for storing/polling messages
            
            PERFORMANCE:
            ------------
            - Low latency (sub-millisecond)
            - High throughput (10,000+ messages/second)
            - Suitable for high-frequency updates
            
            LIMITATIONS:
            ------------
            - No message persistence (use Redis Streams for persistence)
            - No guaranteed delivery
            - Fire-and-forget model
            """
            
            print(pubsub_info)
        
        @staticmethod
        def notification_system():
            """
            Real-time notification system using Redis Pub/Sub
            """
            
            class NotificationSystem:
                """Redis-based notification system"""
                
                def __init__(self, redis_client):
                    self.redis = redis_client
                    self.user_channel_prefix = "user:notifications:"
                
                def publish_user_notification(self, user_id, notification):
                    """
                    Publish notification to user's channel
                    
                    Args:
                        user_id: Recipient user ID
                        notification: Notification data dict
                    """
                    channel = f"{self.user_channel_prefix}{user_id}"
                    
                    notification_data = {
                        'id': str(uuid.uuid4()),
                        'user_id': user_id,
                        'type': notification.get('type', 'info'),
                        'title': notification.get('title', ''),
                        'message': notification.get('message', ''),
                        'data': notification.get('data', {}),
                        'timestamp': datetime.utcnow().isoformat(),
                        'read': False
                    }
                    
                    # Store notification in Redis for persistence
                    notification_key = f"notification:{notification_data['id']}"
                    self.redis.hset(notification_key, mapping=notification_data)
                    self.redis.expire(notification_key, 86400 * 7)  # 7 days
                    
                    # Add to user's notification list
                    user_notifications_key = f"user:{user_id}:notifications"
                    self.redis.lpush(user_notifications_key, notification_data['id'])
                    self.redis.ltrim(user_notifications_key, 0, 99)  # Keep last 100
                    
                    # Publish to user's channel
                    self.redis.publish(channel, json.dumps(notification_data))
                    
                    return notification_data['id']
                
                def publish_global_notification(self, notification):
                    """Publish notification to all users"""
                    channel = "notifications:global"
                    notification_data = {
                        'id': str(uuid.uuid4()),
                        'type': 'global',
                        'title': notification.get('title', 'Announcement'),
                        'message': notification.get('message', ''),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    
                    self.redis.publish(channel, json.dumps(notification_data))
                
                def get_user_notifications(self, user_id, limit=20):
                    """Get recent notifications for user"""
                    user_notifications_key = f"user:{user_id}:notifications"
                    notification_ids = self.redis.lrange(
                        user_notifications_key, 
                        0, 
                        limit - 1
                    )
                    
                    notifications = []
                    for notif_id in notification_ids:
                        notification_key = f"notification:{notif_id}"
                        notification = self.redis.hgetall(notification_key)
                        if notification:
                            notifications.append(notification)
                    
                    return notifications
            
            return NotificationSystem
        
        @staticmethod
        def websocket_integration():
            """
            WebSocket integration with Redis Pub/Sub
            """
            
            try:
                from flask_socketio import SocketIO, emit, join_room, leave_room
                
                # Initialize SocketIO with Redis message queue
                socketio = SocketIO(
                    app,
                    message_queue='redis://localhost:6379/0',
                    cors_allowed_origins="*",
                    async_mode='threading'
                )
                
                class WebSocketManager:
                    """Manage WebSocket connections with Redis Pub/Sub"""
                    
                    def __init__(self, socketio_app, redis_client):
                        self.socketio = socketio_app
                        self.redis = redis_client
                        self.pubsub = self.redis.pubsub()
                        
                        # Start Redis subscription in background thread
                        self.start_background_subscription()
                    
                    def start_background_subscription(self):
                        """Start Redis Pub/Sub subscription in background"""
                        
                        def redis_subscriber():
                            """Subscribe to Redis channels and forward to WebSockets"""
                            # Subscribe to channels
                            self.pubsub.subscribe(
                                'websocket:broadcast',
                                'websocket:user:*',
                                'websocket:room:*'
                            )
                            
                            for message in self.pubsub.listen():
                                if message['type'] == 'message':
                                    channel = message['channel']
                                    data = json.loads(message['data'])
                                    
                                    # Route message based on channel
                                    if channel == 'websocket:broadcast':
                                        self.socketio.emit('broadcast', data)
                                    
                                    elif channel.startswith('websocket:user:'):
                                        user_id = channel.split(':')[-1]
                                        self.socketio.emit(
                                            'private_message', 
                                            data, 
                                            room=f"user_{user_id}"
                                        )
                                    
                                    elif channel.startswith('websocket:room:'):
                                        room_id = channel.split(':')[-1]
                                        self.socketio.emit(
                                            'room_message',
                                            data,
                                            room=f"room_{room_id}"
                                        )
                        
                        # Start subscription thread
                        thread = threading.Thread(target=redis_subscriber, daemon=True)
                        thread.start()
                    
                    def send_to_user(self, user_id, event, data):
                        """Send WebSocket message to specific user"""
                        channel = f'websocket:user:{user_id}'
                        message = {'event': event, 'data': data}
                        self.redis.publish(channel, json.dumps(message))
                    
                    def send_to_room(self, room_id, event, data):
                        """Send WebSocket message to room"""
                        channel = f'websocket:room:{room_id}'
                        message = {'event': event, 'data': data}
                        self.redis.publish(channel, json.dumps(message))
                    
                    def broadcast(self, event, data):
                        """Broadcast WebSocket message to all clients"""
                        channel = 'websocket:broadcast'
                        message = {'event': event, 'data': data}
                        self.redis.publish(channel, json.dumps(message))
                
                # WebSocket event handlers
                @socketio.on('connect')
                def handle_connect():
                    """Handle WebSocket connection"""
                    user_id = request.args.get('user_id')
                    if user_id:
                        join_room(f"user_{user_id}")
                    emit('connected', {'message': 'Connected to WebSocket'})
                
                @socketio.on('join_room')
                def handle_join_room(data):
                    """Join a room"""
                    room_id = data.get('room_id')
                    if room_id:
                        join_room(f"room_{room_id}")
                        emit('room_joined', {'room_id': room_id})
                
                @socketio.on('send_message')
                def handle_send_message(data):
                    """Send message via Redis Pub/Sub"""
                    room_id = data.get('room_id')
                    message = data.get('message')
                    
                    if room_id and message:
                        # Publish to Redis
                        redis_client.publish(
                            f'websocket:room:{room_id}',
                            json.dumps({
                                'sender': request.sid,
                                'message': message,
                                'timestamp': datetime.utcnow().isoformat()
                            })
                        )
                
                return WebSocketManager(socketio, redis_client)
            
            except ImportError:
                print("Note: flask-socketio not installed. WebSocket examples disabled.")
                return None
        
        @staticmethod
        def server_sent_events():
            """
            Server-Sent Events (SSE) with Redis Pub/Sub
            """
            
            @app.route('/api/events/stream')
            def sse_stream():
                """
                Server-Sent Events stream endpoint
                Returns real-time events as a stream
                """
                
                def event_stream():
                    """
                    Generator function for SSE
                    """
                    # Create Redis Pub/Sub connection
                    pubsub = redis_client.pubsub()
                    
                    # Subscribe to events
                    user_id = request.args.get('user_id')
                    if user_id:
                        # Subscribe to user-specific channel
                        pubsub.subscribe(f'events:user:{user_id}')
                    else:
                        # Subscribe to global events
                        pubsub.subscribe('events:global')
                    
                    # Stream messages
                    for message in pubsub.listen():
                        if message['type'] == 'message':
                            data = message['data']
                            if isinstance(data, bytes):
                                data = data.decode('utf-8')
                            
                            yield f"data: {data}\n\n"
                
                return app.response_class(
                    event_stream(),
                    mimetype='text/event-stream',
                    headers={
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'X-Accel-Buffering': 'no'  # Disable nginx buffering
                    }
                )
            
            @app.route('/api/events/publish', methods=['POST'])
            def publish_event():
                """Publish event to Redis"""
                data = request.json
                channel = data.get('channel', 'events:global')
                event_data = data.get('data', {})
                
                # Add metadata
                event_data.update({
                    'published_at': datetime.utcnow().isoformat(),
                    'source': request.remote_addr
                })
                
                # Publish to Redis
                redis_client.publish(channel, json.dumps(event_data))
                
                return jsonify({
                    'message': 'Event published',
                    'channel': channel
                })

# ============================================================================
# 4. ADVANCED REDIS PATTERNS FOR FLASK
# ============================================================================

class AdvancedRedisPatterns:
    """
    Advanced Redis patterns and use cases for Flask
    """
    
    @staticmethod
    def leaderboard_implementation():
        """
        Leaderboard implementation using Redis Sorted Sets
        """
        
        class Leaderboard:
            """Redis-based leaderboard"""
            
            def __init__(self, redis_client, leaderboard_name='leaderboard'):
                self.redis = redis_client
                self.leaderboard_name = leaderboard_name
            
            def add_score(self, user_id, score):
                """Add or update user score"""
                # Use ZADD with NX option to only add if doesn't exist
                # Or XX to only update existing
                return self.redis.zadd(
                    self.leaderboard_name,
                    {str(user_id): score}
                )
            
            def increment_score(self, user_id, increment=1):
                """Increment user score"""
                return self.redis.zincrby(
                    self.leaderboard_name,
                    increment,
                    str(user_id)
                )
            
            def get_rank(self, user_id):
                """Get user's rank (0-indexed, highest score first)"""
                return self.redis.zrevrank(
                    self.leaderboard_name,
                    str(user_id)
                )
            
            def get_score(self, user_id):
                """Get user's score"""
                return self.redis.zscore(
                    self.leaderboard_name,
                    str(user_id)
                )
            
            def get_top_n(self, n=10, with_scores=True):
                """Get top N users"""
                return self.redis.zrevrange(
                    self.leaderboard_name,
                    0,
                    n - 1,
                    withscores=with_scores
                )
            
            def get_users_around(self, user_id, range_count=5):
                """Get users around a specific user"""
                rank = self.get_rank(user_id)
                if rank is None:
                    return []
                
                start = max(0, rank - range_count)
                end = rank + range_count
                
                return self.redis.zrevrange(
                    self.leaderboard_name,
                    start,
                    end,
                    withscores=True
                )
        
        return Leaderboard
    
    @staticmethod
    def real_time_analytics():
        """
        Real-time analytics with Redis
        """
        
        class RealTimeAnalytics:
            """Real-time analytics using Redis data structures"""
            
            def __init__(self, redis_client):
                self.redis = redis_client
            
            def track_page_view(self, page_path, user_id=None):
                """Track page view"""
                # Increment page counter
                self.redis.incr(f"page_views:{page_path}")
                
                # Track daily views
                today = datetime.utcnow().strftime("%Y-%m-%d")
                self.redis.incr(f"page_views:{page_path}:{today}")
                
                # Track unique visitors (HyperLogLog)
                if user_id:
                    self.redis.pfadd(f"unique_visitors:{page_path}:{today}", user_id)
                
                # Track real-time active users
                minute_key = f"active_users:{datetime.utcnow().strftime('%Y-%m-%d-%H-%M')}"
                if user_id:
                    self.redis.sadd(minute_key, user_id)
                    self.redis.expire(minute_key, 300)  # Expire after 5 minutes
            
            def get_page_stats(self, page_path, days=7):
                """Get page statistics"""
                today = datetime.utcnow()
                stats = {
                    'total_views': int(self.redis.get(f"page_views:{page_path}") or 0),
                    'daily_views': {},
                    'unique_visitors': {}
                }
                
                # Get daily views for last N days
                for i in range(days):
                    date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                    daily_views = self.redis.get(f"page_views:{page_path}:{date}")
                    stats['daily_views'][date] = int(daily_views or 0)
                    
                    # Get unique visitors
                    unique_count = self.redis.pfcount(f"unique_visitors:{page_path}:{date}")
                    stats['unique_visitors'][date] = unique_count
                
                return stats
            
            def get_realtime_active_users(self):
                """Get number of active users in last 5 minutes"""
                active_keys = []
                now = datetime.utcnow()
                
                # Check last 5 minutes
                for i in range(5):
                    minute_key = f"active_users:{(now - timedelta(minutes=i)).strftime('%Y-%m-%d-%H-%M')}"
                    active_keys.append(minute_key)
                
                # Count unique active users
                temp_key = f"temp_active_users:{int(time.time())}"
                self.redis.sunionstore(temp_key, *active_keys)
                count = self.redis.scard(temp_key)
                self.redis.delete(temp_key)
                
                return count
            
            def track_event(self, event_name, properties=None):
                """Track custom event"""
                event_id = str(uuid.uuid4())
                event_key = f"event:{event_id}"
                
                event_data = {
                    'name': event_name,
                    'timestamp': datetime.utcnow().isoformat(),
                    'properties': json.dumps(properties or {})
                }
                
                # Store event
                self.redis.hset(event_key, mapping=event_data)
                self.redis.expire(event_key, 86400 * 30)  # 30 days
                
                # Add to event stream
                self.redis.xadd(
                    'events_stream',
                    {'name': event_name, 'data': json.dumps(properties or {})}
                )
                
                return event_id
        
        return RealTimeAnalytics
    
    @staticmethod
    def distributed_locking():
        """
        Distributed locking with Redis
        """
        
        class DistributedLock:
            """Distributed lock using Redis"""
            
            def __init__(self, redis_client, lock_name, timeout=10):
                self.redis = redis_client
                self.lock_name = f"lock:{lock_name}"
                self.timeout = timeout
                self.identifier = str(uuid.uuid4())  # Unique lock identifier
            
            def acquire(self, blocking=True, block_timeout=None):
                """
                Acquire lock
                
                Args:
                    blocking: Wait for lock if not available
                    block_timeout: Maximum time to wait (seconds)
                
                Returns:
                    bool: True if lock acquired
                """
                if blocking:
                    # Wait for lock with timeout
                    end_time = time.time() + (block_timeout or self.timeout)
                    
                    while time.time() < end_time:
                        if self._try_acquire():
                            return True
                        time.sleep(0.1)  # Small sleep to avoid tight loop
                    
                    return False
                else:
                    # Try once
                    return self._try_acquire()
            
            def _try_acquire(self):
                """Try to acquire lock (non-blocking)"""
                # Use SET with NX and EX for atomic lock acquisition
                acquired = self.redis.set(
                    self.lock_name,
                    self.identifier,
                    ex=self.timeout,
                    nx=True  # Only set if doesn't exist
                )
                
                return acquired is not None
            
            def release(self):
                """Release lock"""
                # Use Lua script for atomic check-and-delete
                lua_script = """
                if redis.call("GET", KEYS[1]) == ARGV[1] then
                    return redis.call("DEL", KEYS[1])
                else
                    return 0
                end
                """
                
                result = self.redis.eval(
                    lua_script,
                    1,  # Number of keys
                    self.lock_name,
                    self.identifier
                )
                
                return result == 1
            
            def refresh(self):
                """Refresh lock timeout"""
                lua_script = """
                if redis.call("GET", KEYS[1]) == ARGV[1] then
                    return redis.call("EXPIRE", KEYS[1], ARGV[2])
                else
                    return 0
                end
                """
                
                result = self.redis.eval(
                    lua_script,
                    1,
                    self.lock_name,
                    self.identifier,
                    self.timeout
                )
                
                return result == 1
            
            @contextmanager
            def __call__(self):
                """Context manager support"""
                acquired = self.acquire(blocking=True)
                
                if not acquired:
                    raise Exception(f"Failed to acquire lock: {self.lock_name}")
                
                try:
                    yield self
                finally:
                    self.release()
        
        return DistributedLock
    
    @staticmethod
    def bloom_filter_implementation():
        """
        Bloom filter implementation using Redis Bitmaps
        """
        
        class BloomFilter:
            """Bloom filter for membership testing"""
            
            def __init__(self, redis_client, filter_name, capacity=1000000, error_rate=0.01):
                self.redis = redis_client
                self.filter_name = f"bloom:{filter_name}"
                
                # Calculate optimal parameters
                import math
                self.capacity = capacity
                self.error_rate = error_rate
                
                # Number of bits
                self.num_bits = int(-capacity * math.log(error_rate) / (math.log(2) ** 2))
                
                # Number of hash functions
                self.num_hashes = int(self.num_bits / capacity * math.log(2))
                
                # Ensure minimum values
                self.num_bits = max(self.num_bits, 1)
                self.num_hashes = max(self.num_hashes, 1)
            
            def _hash_positions(self, item):
                """Get bit positions for an item"""
                # Use multiple hash functions
                positions = []
                
                # Simple double-hashing technique
                hash1 = hashlib.md5(item.encode()).digest()
                hash2 = hashlib.sha256(item.encode()).digest()
                
                for i in range(self.num_hashes):
                    # Combine hashes
                    combined_hash = int.from_bytes(
                        hashlib.sha256(hash1 + hash2 + i.to_bytes(4, 'big')).digest(),
                        'big'
                    )
                    
                    position = combined_hash % self.num_bits
                    positions.append(position)
                
                return positions
            
            def add(self, item):
                """Add item to bloom filter"""
                positions = self._hash_positions(item)
                
                # Set bits
                for position in positions:
                    self.redis.setbit(self.filter_name, position, 1)
                
                return True
            
            def exists(self, item):
                """Check if item might exist in bloom filter"""
                positions = self._hash_positions(item)
                
                # Check all bits
                for position in positions:
                    if self.redis.getbit(self.filter_name, position) == 0:
                        return False  # Definitely not in set
                
                return True  # Probably in set (with error_rate probability)
            
            def clear(self):
                """Clear bloom filter"""
                self.redis.delete(self.filter_name)
        
        return BloomFilter

# ============================================================================
# 5. REDIS MONITORING, MAINTENANCE & BEST PRACTICES
# ============================================================================

class RedisOperations:
    """
    Redis monitoring, maintenance, and best practices
    """
    
    @staticmethod
    def monitoring_and_metrics():
        """
        Monitoring Redis performance and health
        """
        
        print("\n" + "="*80)
        print("REDIS MONITORING AND METRICS")
        print("="*80)
        
        monitoring_info = """
        KEY METRICS TO MONITOR:
        -----------------------
        
        1. MEMORY USAGE:
           - used_memory: Total memory used
           - used_memory_peak: Peak memory usage
           - mem_fragmentation_ratio: Fragmentation level (>1.5 needs attention)
           - maxmemory_policy: Eviction policy
        
        2. PERFORMANCE:
           - instantaneous_ops_per_sec: Current operations per second
           - total_connections_received: Total connections
           - total_commands_processed: Total commands
           - latency: Command latency
        
        3. PERSISTENCE:
           - rdb_last_save_time: Last RDB save
           - rdb_last_bgsave_status: Last RDB save status
           - aof_current_size: Current AOF file size
           - aof_last_write_status: Last AOF write status
        
        4. REPLICATION:
           - connected_slaves: Number of connected slaves
           - master_repl_offset: Replication offset
           - repl_backlog_size: Replication backlog size
        
        5. CLUSTER (if using Redis Cluster):
           - cluster_size: Number of nodes
           - cluster_slots_assigned: Slots assigned
           - cluster_state: Cluster state
        
        MONITORING TOOLS:
        -----------------
        
        1. redis-cli INFO: Get comprehensive Redis info
           $ redis-cli INFO
        
        2. redis-cli MONITOR: Monitor all commands in real-time
           $ redis-cli MONITOR
        
        3. redis-cli --latency: Check latency
           $ redis-cli --latency
        
        4. redis-cli --bigkeys: Find largest keys
           $ redis-cli --bigkeys
        
        5. redis-cli --scan: Scan keys with pattern
           $ redis-cli --scan --pattern "user:*"
        
        FLASK INTEGRATION MONITORING:
        -----------------------------
        
        def check_redis_health():
            try:
                # Check connection
                redis_client.ping()
                
                # Get info
                info = redis_client.info()
                
                return {
                    'status': 'healthy',
                    'memory_used': info['used_memory_human'],
                    'connected_clients': info['connected_clients'],
                    'ops_per_sec': info['instantaneous_ops_per_sec']
                }
            except RedisError as e:
                return {'status': 'unhealthy', 'error': str(e)}
        
        @app.route('/health/redis')
        def redis_health():
            return jsonify(check_redis_health())
        """
        
        print(monitoring_info)
    
    @staticmethod
    def redis_cli_commands():
        """
        Essential Redis CLI commands for development and debugging
        """
        
        commands = {
            'BASIC COMMANDS': {
                'SET key value': 'Set key to hold string value',
                'GET key': 'Get value of key',
                'DEL key': 'Delete key',
                'EXISTS key': 'Check if key exists',
                'EXPIRE key seconds': 'Set key expiration',
                'TTL key': 'Get time to live for key',
                'KEYS pattern': 'Find keys matching pattern',
                'SCAN cursor': 'Incrementally iterate keys',
                'FLUSHDB': 'Delete all keys in current database',
                'INFO': 'Get information and statistics'
            },
            
            'DATA STRUCTURE COMMANDS': {
                'HSET key field value': 'Set field in hash',
                'HGET key field': 'Get field from hash',
                'HGETALL key': 'Get all fields from hash',
                'LPUSH key value': 'Prepend to list',
                'RPUSH key value': 'Append to list',
                'LRANGE key start stop': 'Get range from list',
                'SADD key member': 'Add to set',
                'SMEMBERS key': 'Get all members of set',
                'ZADD key score member': 'Add to sorted set',
                'ZRANGE key start stop': 'Get range from sorted set'
            },
            
            'ADMINISTRATION COMMANDS': {
                'CONFIG GET parameter': 'Get configuration parameter',
                'CONFIG SET parameter value': 'Set configuration parameter',
                'CLIENT LIST': 'Get list of connected clients',
                'CLIENT KILL ip:port': 'Kill specific client',
                'MONITOR': 'Monitor all commands in real-time',
                'SLOWLOG GET': 'Get slow queries',
                'BGSAVE': 'Save database in background',
                'LASTSAVE': 'Get timestamp of last save'
            },
            
            'CLUSTER COMMANDS': {
                'CLUSTER INFO': 'Get cluster information',
                'CLUSTER NODES': 'Get cluster nodes',
                'CLUSTER SLOTS': 'Get cluster slot distribution',
                'CLUSTER KEYSLOT key': 'Get slot for key'
            }
        }
        
        print("\n" + "="*80)
        print("ESSENTIAL REDIS CLI COMMANDS")
        print("="*80)
        
        for category, cmds in commands.items():
            print(f"\n{category}:")
            for cmd, desc in cmds.items():
                print(f"  {cmd:<30} - {desc}")
    
    @staticmethod
    def best_practices():
        """
        Redis best practices for Flask applications
        """
        
        print("\n" + "="*80)
        print("REDIS BEST PRACTICES FOR FLASK")
        print("="*80)
        
        practices = [
            ("1. KEY NAMING CONVENTIONS", """
            Use consistent, descriptive key names:
            
            GOOD:
              user:123:profile
              session:abc123def456
              cache:article:456:views
              queue:email_tasks
            
            BAD:
              u123
              sess_abc
              cache_art456
              q_email
            
            Use colons (:) for hierarchy - they're conventional in Redis
            """),
            
            ("2. CONNECTION MANAGEMENT", """
            Always use connection pooling:
            
            redis_pool = redis.ConnectionPool(max_connections=50)
            redis_client = redis.Redis(connection_pool=redis_pool)
            
            Benefits:
            - Reuse connections
            - Limit total connections
            - Better performance under load
            
            Set appropriate timeouts:
            socket_timeout=5
            socket_connect_timeout=5
            retry_on_timeout=True
            """),
            
            ("3. MEMORY MANAGEMENT", """
            Monitor memory usage:
            
            # Get memory info
            info = redis_client.info()
            memory_used = info['used_memory_human']
            
            Set maxmemory policy:
            
            # In redis.conf or via CONFIG SET
            maxmemory 2gb
            maxmemory-policy allkeys-lru  # Or volatile-lru, allkeys-random
            
            Use appropriate data structures:
            - Hashes for objects
            - Sorted sets for rankings
            - Sets for unique items
            - Lists for queues
            """),
            
            ("4. ERROR HANDLING", """
            Always handle Redis errors gracefully:
            
            try:
                value = redis_client.get('key')
            except redis.ConnectionError:
                # Handle connection error
                value = None
            except redis.TimeoutError:
                # Handle timeout
                value = None
            except redis.RedisError as e:
                # Handle other Redis errors
                current_app.logger.error(f"Redis error: {e}")
                value = None
            
            Don't let Redis failures break your application
            """),
            
            ("5. PERFORMANCE OPTIMIZATION", """
            Use pipelines for multiple commands:
            
            pipe = redis_client.pipeline()
            pipe.set('key1', 'value1')
            pipe.set('key2', 'value2')
            pipe.execute()  # Single round trip
            
            Use appropriate data sizes:
            - Compress large values
            - Split huge hashes/lists
            - Use bitmaps for boolean arrays
            
            Enable Redis persistence appropriately:
            - RDB for backups
            - AOF for durability
            - RDB + AOF for production
            """),
            
            ("6. SECURITY", """
            Enable authentication:
            requirepass your_secure_password
            
            Use SSL/TLS for network encryption:
            redis_client = redis.Redis(ssl=True, ssl_cert_reqs='required')
            
            Restrict network access:
            bind 127.0.0.1  # Only local connections
            Or use firewall rules
            
            Regular updates:
            Keep Redis updated for security patches
            """),
            
            ("7. SCALING STRATEGIES", """
            For read-heavy applications:
            - Use Redis replication (master-slave)
            - Distribute reads to slaves
            
            For write-heavy applications:
            - Use Redis Cluster
            - Shard data across multiple masters
            
            For very large datasets:
            - Use Redis Cluster
            - Consider Redis Enterprise for larger scale
            
            Monitor and adjust based on metrics
            """)
        ]
        
        for title, content in practices:
            print(f"\n{title}")
            print(content)

# ============================================================================
# 6. COMPLETE FLASK-REDIS APPLICATION EXAMPLE
# ============================================================================

def create_complete_redis_flask_app():
    """
    Complete Flask application with Redis integration
    """
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # ============== REDIS CONFIGURATION ==============
    
    # Configure Redis connection
    redis_client = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'localhost'),
        port=int(os.environ.get('REDIS_PORT', 6379)),
        db=int(os.environ.get('REDIS_DB', 0)),
        decode_responses=True,
        socket_timeout=5,
        retry_on_timeout=True,
        max_connections=50
    )
    
    # ============== CACHE DECORATOR ==============
    
    def cache_view(ttl=300):
        """Cache view decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                cache_key = f"view:{request.path}"
                
                # Check cache
                cached = redis_client.get(cache_key)
                if cached:
                    return jsonify({'source': 'cache', 'data': json.loads(cached)})
                
                # Execute view
                result = f(*args, **kwargs)
                
                # Cache result
                if isinstance(result, tuple):
                    response_data, status = result
                    if status == 200:
                        redis_client.setex(cache_key, ttl, json.dumps(response_data.get_json()))
                else:
                    redis_client.setex(cache_key, ttl, json.dumps(result.get_json()))
                
                return result
            return decorated_function
        return decorator
    
    # ============== RATE LIMIT DECORATOR ==============
    
    def rate_limit(limit=100, window=3600):
        """Rate limit decorator"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                client_id = request.remote_addr
                key = f"ratelimit:{f.__name__}:{client_id}"
                
                # Get current count
                current = redis_client.get(key)
                if current is None:
                    redis_client.setex(key, window, 1)
                    current = 1
                else:
                    current = int(current) + 1
                    redis_client.incr(key)
                
                # Check limit
                if current > limit:
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'limit': limit,
                        'window': window
                    }), 429
                
                # Add headers
                response = f(*args, **kwargs)
                if isinstance(response, tuple):
                    response_obj = response[0]
                else:
                    response_obj = response
                
                response_obj.headers['X-RateLimit-Limit'] = str(limit)
                response_obj.headers['X-RateLimit-Remaining'] = str(limit - current)
                response_obj.headers['X-RateLimit-Reset'] = str(int(time.time()) + window)
                
                return response
            return decorated_function
        return decorator
    
    # ============== APPLICATION ROUTES ==============
    
    @app.route('/')
    def home():
        """Home page"""
        return jsonify({
            'name': 'Flask Redis Demo',
            'endpoints': {
                '/api/products': 'GET - Get products (cached)',
                '/api/products/<id>': 'GET - Get single product (cached)',
                '/api/search': 'GET - Search (rate limited)',
                '/api/leaderboard': 'GET - Leaderboard',
                '/api/analytics': 'GET - Analytics',
                '/api/session': 'GET/POST - Session demo',
                '/health': 'GET - Health check'
            }
        })
    
    @app.route('/api/products')
    @cache_view(ttl=60)
    def get_products():
        """Get products with caching"""
        # Simulate database query
        time.sleep(1)
        
        products = [
            {'id': 1, 'name': 'Product 1', 'price': 99.99},
            {'id': 2, 'name': 'Product 2', 'price': 149.99},
            {'id': 3, 'name': 'Product 3', 'price': 199.99}
        ]
        
        return jsonify({'products': products})
    
    @app.route('/api/search')
    @rate_limit(limit=10, window=60)
    def search():
        """Search endpoint with rate limiting"""
        query = request.args.get('q', '')
        
        # Track search analytics
        redis_client.incr(f"search:{query}")
        redis_client.zincrby('popular_searches', 1, query)
        
        # Simulate search
        time.sleep(0.5)
        
        return jsonify({
            'query': query,
            'results': [
                {'id': 1, 'name': f'Result for {query} 1'},
                {'id': 2, 'name': f'Result for {query} 2'}
            ]
        })
    
    @app.route('/api/leaderboard')
    def leaderboard():
        """Redis leaderboard example"""
        leaderboard = AdvancedRedisPatterns.leaderboard_implementation()(redis_client)
        
        # Get top 10
        top_users = leaderboard.get_top_n(10, with_scores=True)
        
        return jsonify({
            'leaderboard': [
                {'user_id': user_id, 'score': score}
                for user_id, score in top_users
            ]
        })
    
    @app.route('/api/analytics')
    def analytics():
        """Redis analytics example"""
        analytics = AdvancedRedisPatterns.real_time_analytics()(redis_client)
        
        # Track this page view
        user_id = request.args.get('user_id')
        analytics.track_page_view('/api/analytics', user_id)
        
        # Get stats
        stats = analytics.get_page_stats('/api/analytics', days=7)
        
        return jsonify(stats)
    
    @app.route('/api/session', methods=['GET', 'POST'])
    def session_demo():
        """Redis session demo"""
        if request.method == 'POST':
            # Set session data
            data = request.json
            session_id = secrets.token_urlsafe(32)
            
            session_data = {
                'user_id': data.get('user_id', 1),
                'username': data.get('username', 'guest'),
                'created_at': datetime.utcnow().isoformat(),
                'last_activity': datetime.utcnow().isoformat()
            }
            
            # Store in Redis
            redis_client.hset(f"session:{session_id}", mapping=session_data)
            redis_client.expire(f"session:{session_id}", 3600)
            
            response = jsonify({'session_id': session_id})
            response.set_cookie('session_id', session_id, httponly=True)
            return response
        
        else:
            # Get session data
            session_id = request.cookies.get('session_id')
            if not session_id:
                return jsonify({'error': 'No session'}), 401
            
            session_data = redis_client.hgetall(f"session:{session_id}")
            if not session_data:
                return jsonify({'error': 'Invalid session'}), 401
            
            # Update last activity
            session_data['last_activity'] = datetime.utcnow().isoformat()
            redis_client.hset(f"session:{session_id}", 'last_activity', session_data['last_activity'])
            redis_client.expire(f"session:{session_id}", 3600)
            
            return jsonify(session_data)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Check Redis
            redis_client.ping()
            redis_info = redis_client.info()
            
            return jsonify({
                'status': 'healthy',
                'redis': {
                    'connected': True,
                    'memory': redis_info.get('used_memory_human'),
                    'clients': redis_info.get('connected_clients')
                },
                'timestamp': datetime.utcnow().isoformat()
            })
        except RedisError as e:
            return jsonify({
                'status': 'unhealthy',
                'redis': {'connected': False, 'error': str(e)},
                'timestamp': datetime.utcnow().isoformat()
            }), 503
    
    # ============== ERROR HANDLERS ==============
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Please try again later'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f'Server error: {e}')
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# ============================================================================
# MAIN DEMONSTRATION FUNCTION
# ============================================================================

def run_redis_demo():
    """
    Run comprehensive Redis with Flask demonstration
    """
    print("\n" + "="*100)
    print("COMPREHENSIVE REDIS WITH FLASK GUIDE")
    print("="*100)
    
    # 1. Redis Overview
    RedisOverview.redis_fundamentals()
    RedisOverview.data_structures_detailed()
    RedisOverview.redis_vs_alternatives()
    
    # 2. Redis Usages with Flask
    FlaskRedisIntegration.setup_redis_connection()
    FlaskRedisIntegration.flask_redis_extensions()
    
    # 3. Redis Examples with Flask
    print("\n" + "="*100)
    print("REDIS EXAMPLES WITH FLASK")
    print("="*100)
    
    # Caching Examples
    print("\nCACHING PATTERNS:")
    RedisFlaskExamples.CachingExamples.advanced_caching_patterns()
    
    # Session Examples
    print("\nSESSION MANAGEMENT:")
    session_store = RedisFlaskExamples.SessionExamples.custom_redis_session()(
        redis.Redis(decode_responses=True),
        ttl=3600
    )
    print("✓ Custom Redis session store implemented")
    
    # Rate Limiting Examples
    print("\nRATE LIMITING:")
    limiter = RedisFlaskExamples.RateLimitingExamples.sliding_window_rate_limiter()(
        redis.Redis(decode_responses=True),
        limit=10,
        window=60
    )
    print("✓ Sliding window rate limiter implemented")
    
    # Task Queue Examples
    print("\nTASK QUEUES:")
    task_queue = RedisFlaskExamples.TaskQueueExamples.simple_task_queue()(
        redis.Redis(decode_responses=True),
        queue_name='demo_tasks'
    )
    print("✓ Redis task queue implemented")
    
    # Real-time Examples
    print("\nREAL-TIME FEATURES:")
    RedisFlaskExamples.RealTimeExamples.redis_pubsub_basics()
    
    # 4. Advanced Redis Patterns
    print("\n" + "="*100)
    print("ADVANCED REDIS PATTERNS")
    print("="*100)
    
    print("\nLEADERBOARDS:")
    leaderboard = AdvancedRedisPatterns.leaderboard_implementation()(
        redis.Redis(decode_responses=True)
    )
    print("✓ Redis sorted set leaderboard implemented")
    
    print("\nREAL-TIME ANALYTICS:")
    analytics = AdvancedRedisPatterns.real_time_analytics()(
        redis.Redis(decode_responses=True)
    )
    print("✓ Real-time analytics with Redis implemented")
    
    print("\nDISTRIBUTED LOCKING:")
    distributed_lock = AdvancedRedisPatterns.distributed_locking()(
        redis.Redis(decode_responses=True),
        lock_name='resource_lock',
        timeout=30
    )
    print("✓ Distributed locking with Redis implemented")
    
    # 5. Redis Operations
    RedisOperations.monitoring_and_metrics()
    RedisOperations.redis_cli_commands()
    RedisOperations.best_practices()
    
    print("\n" + "="*100)
    print("SUMMARY: REDIS WITH FLASK")
    print("="*100)
    
    summary = """
    WHEN TO USE REDIS WITH FLASK:
    -----------------------------
    
    1. CACHING: 
       - API responses
       - Database query results
       - HTML fragments
       - Use with TTL for automatic expiration
    
    2. SESSION STORAGE:
       - Server-side sessions
       - Distributed sessions across workers
       - Fast session access
    
    3. RATE LIMITING:
       - API rate limiting
       - Login attempt limiting
       - DDoS protection
    
    4. BACKGROUND JOBS:
       - Task queues (Celery/RQ)
       - Scheduled tasks
       - Email sending
       - Report generation
    
    5. REAL-TIME FEATURES:
       - WebSocket backends
       - Live notifications
       - Chat applications
       - Real-time dashboards
    
    6. ADVANCED USE CASES:
       - Leaderboards (sorted sets)
       - Real-time analytics
       - Distributed locking
       - Bloom filters
       - Geospatial queries
    
    PERFORMANCE BENEFITS:
    ---------------------
    
    With Redis:
    - Microsecond response times
    - 100,000+ operations/second
    - Reduced database load
    - Horizontal scalability
    
    Without Redis:
    - Database becomes bottleneck
    - Slower response times
    - Limited scalability
    - No real-time capabilities
    
    GETTING STARTED:
    ----------------
    
    1. Install: pip install redis
    2. Connect: redis.Redis(host='localhost', port=6379)
    3. Use: redis_client.set('key', 'value')
    4. Cache: @cache.cached(timeout=300)
    5. Queue: celery = Celery(broker='redis://')
    
    PRODUCTION READY:
    -----------------
    
    1. Use connection pooling
    2. Set appropriate timeouts
    3. Enable Redis persistence (RDB/AOF)
    4. Use Redis Sentinel for HA
    5. Monitor memory usage
    6. Secure with authentication
    
    Redis transforms Flask from a simple web framework
    into a high-performance, scalable application platform!
    """
    
    print(summary)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Redis with Flask Demo')
    parser.add_argument('--demo', action='store_true', help='Run comprehensive demo')
    parser.add_argument('--run', action='store_true', help='Run Flask app with Redis')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    
    args = parser.parse_args()
    
    if args.demo:
        run_redis_demo()
    elif args.run:
        # Run the complete Flask-Redis application
        app = create_complete_redis_flask_app()
        
        print(f"\n🚀 Starting Flask Redis Demo on http://localhost:{args.port}")
        print("\nAvailable endpoints:")
        print("  GET  /                    - API documentation")
        print("  GET  /api/products        - Cached products (60s cache)")
        print("  GET  /api/search?q=query  - Rate limited search (10/min)")
        print("  GET  /api/leaderboard     - Redis leaderboard example")
        print("  GET  /api/analytics       - Real-time analytics")
        print("  GET  /api/session         - Get session")
        print("  POST /api/session         - Create session")
        print("  GET  /health              - Health check with Redis status")
        
        print("\nRedis features included:")
        print("  ✓ Caching with TTL")
        print("  ✓ Rate limiting")
        print("  ✓ Session storage")
        print("  ✓ Leaderboards")
        print("  ✓ Real-time analytics")
        print("  ✓ Health monitoring")
        
        app.run(debug=True, port=args.port)
    else:
        print("Usage: python redis_flask.py [--demo|--run]")
        print("\nOptions:")
        print("  --demo    Run comprehensive Redis-Flask demonstration")
        print("  --run     Run complete Flask application with Redis integration")