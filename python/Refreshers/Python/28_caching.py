"""
COMPREHENSIVE CACHING STRATEGIES GUIDE
========================================
This comprehensive guide covers:
1. When and what to cache
2. Cache invalidation patterns
3. Practical implementations with Redis/memcached basics
4. Real-world caching strategies
"""

print("=" * 70)
print("CACHING STRATEGIES & IMPLEMENTATIONS")
print("=" * 70)

import time
import hashlib
import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List, Union, Callable
from enum import Enum
import threading
import json

# ============================================================================
# PART 1: WHEN AND WHAT TO CACHE
# ============================================================================

print("\n" + "=" * 30)
print("WHEN AND WHAT TO CACHE")
print("=" * 30)

class CacheCandidateType(Enum):
    """Types of data that are good candidates for caching"""
    STATIC_CONTENT = "static_content"          # CSS, JS, images
    READ_HEAVY_DATA = "read_heavy_data"        # Frequently read, rarely written
    COMPUTATIONALLY_EXPENSIVE = "expensive_computation"  # Complex calculations
    EXTERNAL_API_RESPONSES = "api_responses"   # Slow external API calls
    SESSION_DATA = "session_data"              # User session information
    DATABASE_QUERY_RESULTS = "query_results"   # Repeated database queries

@dataclass
class CacheDecisionMatrix:
    """
    Decision matrix for determining when to cache
    Based on: Read/write ratio, data volatility, computation cost, size
    """
    data_id: str
    read_frequency: int          # Reads per minute
    write_frequency: int         # Writes per minute
    computation_cost_ms: int     # Time to compute/fetch
    data_size_kb: int           # Size in KB
    volatility_score: float     # 0-1, how often data changes
    
    def should_cache(self) -> bool:
        """Determine if this data should be cached"""
        # Rule 1: Read-heavy (reads > writes * 10)
        if self.read_frequency > self.write_frequency * 10:
            return True
        
        # Rule 2: Computationally expensive (> 100ms)
        if self.computation_cost_ms > 100:
            return True
        
        # Rule 3: Large but stable data
        if self.data_size_kb > 100 and self.volatility_score < 0.1:
            return True
        
        # Rule 4: Moderate read frequency with low volatility
        if (self.read_frequency > 10 and 
            self.write_frequency < 1 and 
            self.volatility_score < 0.2):
            return True
        
        return False
    
    def recommended_ttl(self) -> int:
        """Recommended Time-To-Live in seconds based on volatility"""
        if self.volatility_score < 0.1:
            return 3600  # 1 hour for stable data
        elif self.volatility_score < 0.3:
            return 300   # 5 minutes for moderately volatile
        elif self.volatility_score < 0.6:
            return 60    # 1 minute for volatile data
        else:
            return 10    # 10 seconds for highly volatile


class CacheAnalyzer:
    """Analyzes application patterns to recommend caching strategies"""
    
    def __init__(self):
        self.data_patterns: Dict[str, CacheDecisionMatrix] = {}
    
    def track_data_access(self, data_id: str, is_read: bool, 
                         duration_ms: int, size_bytes: int):
        """Track data access patterns"""
        if data_id not in self.data_patterns:
            self.data_patterns[data_id] = CacheDecisionMatrix(
                data_id=data_id,
                read_frequency=0,
                write_frequency=0,
                computation_cost_ms=0,
                data_size_kb=size_bytes // 1024,
                volatility_score=0.5  # Default medium volatility
            )
        
        matrix = self.data_patterns[data_id]
        if is_read:
            matrix.read_frequency += 1
            matrix.computation_cost_ms = max(matrix.computation_cost_ms, duration_ms)
        else:
            matrix.write_frequency += 1
            # Increase volatility on writes
            matrix.volatility_score = min(1.0, matrix.volatility_score + 0.1)
    
    def get_cache_recommendations(self) -> List[Dict]:
        """Generate caching recommendations based on tracked patterns"""
        recommendations = []
        
        for data_id, matrix in self.data_patterns.items():
            if matrix.should_cache():
                recommendations.append({
                    "data_id": data_id,
                    "should_cache": True,
                    "recommended_ttl": matrix.recommended_ttl(),
                    "cache_reason": self._get_cache_reason(matrix),
                    "estimated_savings": self._calculate_savings(matrix),
                    "pattern": {
                        "read_per_min": matrix.read_frequency,
                        "write_per_min": matrix.write_frequency,
                        "read_write_ratio": matrix.read_frequency / max(1, matrix.write_frequency),
                        "computation_ms": matrix.computation_cost_ms
                    }
                })
            else:
                recommendations.append({
                    "data_id": data_id,
                    "should_cache": False,
                    "reason": "Not read-heavy enough or too volatile"
                })
        
        return recommendations
    
    def _get_cache_reason(self, matrix: CacheDecisionMatrix) -> str:
        """Determine primary reason for caching"""
        if matrix.read_frequency > matrix.write_frequency * 10:
            return "Read-heavy workload"
        elif matrix.computation_cost_ms > 100:
            return "Computationally expensive"
        elif matrix.data_size_kb > 100 and matrix.volatility_score < 0.1:
            return "Large stable data"
        else:
            return "Moderate read frequency with low volatility"
    
    def _calculate_savings(self, matrix: CacheDecisionMatrix) -> float:
        """Calculate estimated time savings from caching"""
        # Estimated calls per hour that would hit cache
        cache_hit_rate = 0.95  # Conservative estimate
        reads_per_hour = matrix.read_frequency * 60
        estimated_savings_ms = reads_per_hour * cache_hit_rate * matrix.computation_cost_ms
        return estimated_savings_ms / 1000  # Convert to seconds


print("\n--- When to Cache Analysis ---")
analyzer = CacheAnalyzer()

# Simulate different data access patterns
patterns = [
    # (data_id, is_read, duration_ms, size_bytes)
    ("user_profile_123", True, 50, 2048),    # Frequently read profile
    ("user_profile_123", True, 50, 2048),
    ("user_profile_123", True, 50, 2048),
    ("user_profile_123", False, 100, 2048),  # One write
    
    ("product_list", True, 200, 51200),      # Large, expensive query
    ("product_list", True, 200, 51200),
    
    ("api_weather", True, 300, 1024),        # Slow external API
    ("api_weather", True, 300, 1024),
    
    ("shopping_cart_456", True, 20, 512),    # Volatile data
    ("shopping_cart_456", False, 30, 512),
    ("shopping_cart_456", False, 30, 512),
]

for pattern in patterns:
    analyzer.track_data_access(*pattern)

recommendations = analyzer.get_cache_recommendations()
print("\nCache Recommendations:")
for rec in recommendations:
    if rec["should_cache"]:
        print(f"\n  {rec['data_id']}:")
        print(f"    Reason: {rec['cache_reason']}")
        print(f"    Recommended TTL: {rec['recommended_ttl']}s")
        print(f"    Estimated savings: {rec['estimated_savings']:.1f}s/hour")
        print(f"    Read/Write ratio: {rec['pattern']['read_write_ratio']:.1f}x")


# ============================================================================
# PART 2: CACHE INVALIDATION PATTERNS
# ============================================================================

print("\n" + "=" * 30)
print("CACHE INVALIDATION PATTERNS")
print("=" * 30)

class CacheInvalidationStrategy(Enum):
    """Different cache invalidation strategies"""
    TIME_BASED = "time_based"              # TTL expiration
    WRITE_THROUGH = "write_through"        # Update cache on write
    WRITE_BEHIND = "write_behind"          # Async cache update
    INVALIDATE_ON_WRITE = "invalidate_on_write"  # Delete on write
    VERSION_BASED = "version_based"        # Version tags
    EVENT_BASED = "event_based"            # Listen for change events


class CacheInvalidator:
    """Implements various cache invalidation patterns"""
    
    def __init__(self):
        self.cache_store = {}
        self.version_store = {}
        self.event_listeners = {}
    
    # Pattern 1: Time-based invalidation (TTL)
    def set_with_ttl(self, key: str, value: Any, ttl_seconds: int):
        """Set value with Time-To-Live"""
        expiration = time.time() + ttl_seconds
        self.cache_store[key] = {
            "value": value,
            "expires_at": expiration,
            "strategy": CacheInvalidationStrategy.TIME_BASED
        }
        print(f"  [TTL] Set {key} with TTL {ttl_seconds}s")
    
    def get_with_ttl(self, key: str) -> Optional[Any]:
        """Get value, checking TTL"""
        if key not in self.cache_store:
            return None
        
        entry = self.cache_store[key]
        if time.time() > entry["expires_at"]:
            del self.cache_store[key]
            print(f"  [TTL] {key} expired and removed")
            return None
        
        return entry["value"]
    
    # Pattern 2: Write-through caching
    def write_through_update(self, key: str, new_value: Any, 
                            update_database: Callable[[str, Any], bool]):
        """
        Update both cache and database synchronously
        Ensures cache and source are always consistent
        """
        # Update database first
        success = update_database(key, new_value)
        if success:
            # Then update cache
            self.cache_store[key] = {
                "value": new_value,
                "updated_at": time.time(),
                "strategy": CacheInvalidationStrategy.WRITE_THROUGH
            }
            print(f"  [Write-Through] Updated {key} in cache and database")
        return success
    
    # Pattern 3: Write-behind (async) caching
    def write_behind_update(self, key: str, new_value: Any,
                          update_database: Callable[[str, Any], bool]):
        """
        Update cache immediately, update database asynchronously
        Better performance but risk of data loss
        """
        # Update cache immediately
        self.cache_store[key] = {
            "value": new_value,
            "pending_sync": True,
            "strategy": CacheInvalidationStrategy.WRITE_BEHIND
        }
        print(f"  [Write-Behind] Updated {key} in cache immediately")
        
        # Async database update (simulated)
        def async_update():
            time.sleep(0.1)  # Simulate delay
            success = update_database(key, new_value)
            if success:
                self.cache_store[key]["pending_sync"] = False
                print(f"  [Write-Behind] Async database update for {key}")
        
        threading.Thread(target=async_update, daemon=True).start()
    
    # Pattern 4: Invalidate on write
    def invalidate_on_write(self, key: str):
        """Remove from cache when data is written/updated"""
        if key in self.cache_store:
            del self.cache_store[key]
            print(f"  [Invalidate-On-Write] Removed {key} from cache")
    
    # Pattern 5: Version-based invalidation
    def set_with_version(self, key: str, value: Any, version: str):
        """Set value with version tag"""
        self.version_store[key] = version
        self.cache_store[key] = {
            "value": value,
            "version": version,
            "strategy": CacheInvalidationStrategy.VERSION_BASED
        }
        print(f"  [Version-Based] Set {key} with version {version}")
    
    def get_with_version_check(self, key: str, current_version: str) -> Optional[Any]:
        """Get value if version matches"""
        if key not in self.cache_store:
            return None
        
        cached_version = self.version_store.get(key)
        if cached_version != current_version:
            # Version mismatch - invalidate
            del self.cache_store[key]
            print(f"  [Version-Based] {key} version mismatch, invalidated")
            return None
        
        return self.cache_store[key]["value"]
    
    # Pattern 6: Event-based invalidation
    def subscribe_to_invalidation(self, key_pattern: str, 
                                callback: Callable[[str], None]):
        """Subscribe to invalidation events"""
        if key_pattern not in self.event_listeners:
            self.event_listeners[key_pattern] = []
        self.event_listeners[key_pattern].append(callback)
    
    def publish_invalidation(self, key: str):
        """Publish invalidation event for matching keys"""
        for pattern, callbacks in self.event_listeners.items():
            if self._key_matches_pattern(key, pattern):
                for callback in callbacks:
                    callback(key)
        print(f"  [Event-Based] Published invalidation for {key}")
    
    def _key_matches_pattern(self, key: str, pattern: str) -> bool:
        """Simple pattern matching (supports * wildcard)"""
        if "*" in pattern:
            # Convert pattern to regex-like matching
            regex_pattern = pattern.replace("*", ".*")
            import re
            return bool(re.match(regex_pattern, key))
        return key == pattern


print("\n--- Cache Invalidation Patterns Demonstration ---")
invalidator = CacheInvalidator()

# Mock database function
def mock_update_database(key: str, value: Any) -> bool:
    print(f"    [Database] Updating {key} = {value}")
    return True

print("\n1. Time-based (TTL) invalidation:")
invalidator.set_with_ttl("user_123", {"name": "John"}, ttl_seconds=2)
print(f"   Get immediately: {invalidator.get_with_ttl('user_123')}")
time.sleep(2.1)
print(f"   Get after 2.1s: {invalidator.get_with_ttl('user_123')}")

print("\n2. Write-through caching:")
invalidator.write_through_update(
    "product_456", 
    {"name": "Laptop", "price": 999},
    mock_update_database
)
print(f"   Cache after write-through: {invalidator.cache_store.get('product_456')}")

print("\n3. Write-behind caching:")
invalidator.write_behind_update(
    "cart_789",
    {"items": 3, "total": 150},
    mock_update_database
)
print(f"   Cache immediately after write-behind: {invalidator.cache_store.get('cart_789')}")
time.sleep(0.2)  # Allow async update to complete

print("\n4. Invalidate on write:")
invalidator.set_with_ttl("session_abc", {"user": "Alice"}, 60)
print(f"   Cache before invalidate: 'session_abc' in cache = {'session_abc' in invalidator.cache_store}")
invalidator.invalidate_on_write("session_abc")
print(f"   Cache after invalidate: 'session_abc' in cache = {'session_abc' in invalidator.cache_store}")

print("\n5. Version-based invalidation:")
invalidator.set_with_version("config_v1", {"theme": "dark"}, "v1.0")
print(f"   Get with matching version: {invalidator.get_with_version_check('config_v1', 'v1.0')}")
print(f"   Get with different version: {invalidator.get_with_version_check('config_v1', 'v2.0')}")

print("\n6. Event-based invalidation:")
def on_user_data_invalidated(key: str):
    print(f"    [Callback] User data {key} was invalidated!")

invalidator.subscribe_to_invalidation("user_*", on_user_data_invalidated)
invalidator.set_with_ttl("user_999", {"name": "Bob"}, 60)
invalidator.publish_invalidation("user_999")


# ============================================================================
# PART 3: CACHING TOOLS - REDIS & MEMCACHED BASICS
# ============================================================================

print("\n" + "=" * 30)
print("CACHING TOOLS: REDIS & MEMCACHED")
print("=" * 30)

class CacheBackend(ABC):
    """Abstract base class for cache backends"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        pass


class InMemoryCache(CacheBackend):
    """Simple in-memory cache (for demonstration)"""
    
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            entry = self.store.get(key)
            if entry and entry["expires_at"] > time.time():
                return entry["value"]
            elif entry:
                del self.store[key]  # Cleanup expired
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        with self.lock:
            expires_at = time.time() + (ttl if ttl else 3600)
            self.store[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": time.time()
            }
            return True
    
    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self.store:
                del self.store[key]
                return True
            return False
    
    def clear(self) -> bool:
        with self.lock:
            self.store.clear()
            return True
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            total = len(self.store)
            expired = sum(1 for v in self.store.values() 
                         if v["expires_at"] <= time.time())
            return {
                "total_keys": total,
                "expired_keys": expired,
                "active_keys": total - expired,
                "memory_usage": f"{sum(len(str(v)) for v in self.store.values())} chars"
            }


class RedisCache(CacheBackend):
    """
    Redis-like cache implementation (simulated)
    Redis features demonstrated:
    - Data structures: Strings, Hashes, Lists, Sets, Sorted Sets
    - Pub/Sub for invalidation
    - Transactions (MULTI/EXEC)
    - Lua scripting
    """
    
    def __init__(self, host="localhost", port=6379, db=0):
        print(f"  [Redis] Connecting to {host}:{port} DB{db}")
        self.store = {}  # Simulating Redis store
        self.pubsub_channels = {}
        self.transaction_mode = False
        self.transaction_commands = []
    
    def get(self, key: str) -> Optional[Any]:
        """GET key - Retrieve string value"""
        entry = self.store.get(key)
        if entry and entry["type"] == "string":
            if entry["expires_at"] > time.time():
                return entry["value"]
            else:
                self.delete(key)
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """SET key value [EX seconds]"""
        expires_at = time.time() + (ttl if ttl else 0)  # 0 = no expiry
        
        if self.transaction_mode:
            self.transaction_commands.append(("SET", key, value, ttl))
            return True
        
        self.store[key] = {
            "type": "string",
            "value": value,
            "expires_at": expires_at if ttl else float('inf')
        }
        
        # Publish invalidation event for pub/sub
        self._publish(f"__keyspace@0__:{key}", "set")
        return True
    
    def hset(self, hash_key: str, field: str, value: Any) -> bool:
        """HSET hash_key field value - Set hash field"""
        if hash_key not in self.store:
            self.store[hash_key] = {
                "type": "hash",
                "value": {}
            }
        
        self.store[hash_key]["value"][field] = value
        return True
    
    def hget(self, hash_key: str, field: str) -> Optional[Any]:
        """HGET hash_key field - Get hash field"""
        hash_data = self.store.get(hash_key)
        if hash_data and hash_data["type"] == "hash":
            return hash_data["value"].get(field)
        return None
    
    def hgetall(self, hash_key: str) -> Dict:
        """HGETALL hash_key - Get all hash fields"""
        hash_data = self.store.get(hash_key)
        if hash_data and hash_data["type"] == "hash":
            return hash_data["value"].copy()
        return {}
    
    def sadd(self, set_key: str, *members) -> int:
        """SADD set_key member [member...] - Add to set"""
        if set_key not in self.store:
            self.store[set_key] = {
                "type": "set",
                "value": set()
            }
        
        added = 0
        for member in members:
            if member not in self.store[set_key]["value"]:
                self.store[set_key]["value"].add(member)
                added += 1
        
        return added
    
    def smembers(self, set_key: str) -> set:
        """SMEMBERS set_key - Get all set members"""
        set_data = self.store.get(set_key)
        if set_data and set_data["type"] == "set":
            return set_data["value"].copy()
        return set()
    
    def delete(self, key: str) -> bool:
        """DEL key - Delete key"""
        if key in self.store:
            del self.store[key]
            self._publish(f"__keyspace@0__:{key}", "del")
            return True
        return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """EXPIRE key seconds - Set key expiry"""
        if key in self.store:
            self.store[key]["expires_at"] = time.time() + seconds
            return True
        return False
    
    def multi(self):
        """MULTI - Start transaction"""
        self.transaction_mode = True
        self.transaction_commands = []
    
    def exec(self):
        """EXEC - Execute transaction"""
        results = []
        for cmd in self.transaction_commands:
            command = cmd[0]
            if command == "SET":
                _, key, value, ttl = cmd
                self.set(key, value, ttl)
                results.append(True)
        
        self.transaction_mode = False
        self.transaction_commands = []
        return results
    
    def publish(self, channel: str, message: str) -> int:
        """PUBLISH channel message - Publish to channel"""
        return self._publish(channel, message)
    
    def subscribe(self, channel: str, callback: Callable):
        """SUBSCRIBE channel - Subscribe to channel"""
        if channel not in self.pubsub_channels:
            self.pubsub_channels[channel] = []
        self.pubsub_channels[channel].append(callback)
    
    def _publish(self, channel: str, message: str) -> int:
        """Internal publish method"""
        subscribers = self.pubsub_channels.get(channel, [])
        for callback in subscribers:
            callback(message)
        return len(subscribers)
    
    def clear(self) -> bool:
        """FLUSHDB - Clear all keys"""
        self.store.clear()
        return True
    
    def info(self) -> Dict:
        """INFO - Get Redis-like information"""
        total_keys = len(self.store)
        expired_keys = sum(1 for v in self.store.values() 
                          if "expires_at" in v and v["expires_at"] < time.time())
        
        return {
            "redis_version": "6.2.6",
            "connected_clients": 1,
            "used_memory_human": f"{total_keys * 100} bytes",
            "total_keys": total_keys,
            "expired_keys": expired_keys,
            "uptime_in_seconds": 3600
        }


class MemcachedCache(CacheBackend):
    """
    Memcached-like cache implementation (simulated)
    Memcached features demonstrated:
    - Simple key-value store
    - Atomic increment/decrement
    - CAS (Check-And-Set) operations
    - Multi-get
    """
    
    def __init__(self, servers=["localhost:11211"]):
        print(f"  [Memcached] Connecting to servers: {servers}")
        self.store = {}
        self.cas_tokens = {}  # For CAS operations
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """get key - Retrieve value"""
        with self.lock:
            entry = self.store.get(key)
            if entry and entry["expires_at"] > time.time():
                return entry["value"]
            elif entry:
                del self.store[key]  # Cleanup expired
            return None
    
    def gets(self, key: str) -> tuple:
        """
        gets key - Retrieve value with CAS token
        Returns (value, cas_token) or (None, None)
        """
        with self.lock:
            entry = self.store.get(key)
            if entry and entry["expires_at"] > time.time():
                cas_token = self.cas_tokens.get(key, 1)
                return entry["value"], cas_token
            return None, None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """set key value [exptime] - Store value"""
        with self.lock:
            expires_at = time.time() + (ttl if ttl else 0)
            self.store[key] = {
                "value": value,
                "expires_at": expires_at,
                "flags": 0  # Memcached flags field
            }
            return True
    
    def cas(self, key: str, value: Any, cas_token: int, 
           ttl: Optional[int] = None) -> bool:
        """
        cas key value cas_token [exptime] - Check and set
        Only sets if CAS token matches
        """
        with self.lock:
            current_token = self.cas_tokens.get(key, 1)
            if current_token != cas_token:
                return False
            
            expires_at = time.time() + (ttl if ttl else 0)
            self.store[key] = {
                "value": value,
                "expires_at": expires_at,
                "flags": 0
            }
            self.cas_tokens[key] = cas_token + 1
            return True
    
    def add(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """add key value [exptime] - Only add if key doesn't exist"""
        with self.lock:
            if key in self.store and self.store[key]["expires_at"] > time.time():
                return False
            
            expires_at = time.time() + (ttl if ttl else 0)
            self.store[key] = {
                "value": value,
                "expires_at": expires_at,
                "flags": 0
            }
            return True
    
    def replace(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """replace key value [exptime] - Only replace if key exists"""
        with selflock:
            if key not in self.store or self.store[key]["expires_at"] <= time.time():
                return False
            
            expires_at = time.time() + (ttl if ttl else 0)
            self.store[key] = {
                "value": value,
                "expires_at": expires_at,
                "flags": 0
            }
            return True
    
    def incr(self, key: str, value: int = 1) -> Optional[int]:
        """incr key value - Increment numeric value"""
        with self.lock:
            entry = self.store.get(key)
            if not entry or entry["expires_at"] <= time.time():
                return None
            
            try:
                current = int(entry["value"])
                new_value = current + value
                entry["value"] = str(new_value)
                return new_value
            except (ValueError, TypeError):
                return None
    
    def decr(self, key: str, value: int = 1) -> Optional[int]:
        """decr key value - Decrement numeric value"""
        return self.incr(key, -value)
    
    def delete(self, key: str) -> bool:
        """delete key - Delete key"""
        with self.lock:
            if key in self.store:
                del self.store[key]
                if key in self.cas_tokens:
                    del self.cas_tokens[key]
                return True
            return False
    
    def get_multi(self, keys: List[str]) -> Dict[str, Any]:
        """get key1 key2 ... - Get multiple keys"""
        result = {}
        with self.lock:
            for key in keys:
                entry = self.store.get(key)
                if entry and entry["expires_at"] > time.time():
                    result[key] = entry["value"]
        return result
    
    def clear(self) -> bool:
        """flush_all - Clear all keys"""
        with self.lock:
            self.store.clear()
            self.cas_tokens.clear()
            return True
    
    def stats(self) -> Dict:
        """stats - Get statistics"""
        with self.lock:
            total = len(self.store)
            expired = sum(1 for v in self.store.values() 
                         if v["expires_at"] <= time.time())
            
            return {
                "curr_items": total - expired,
                "total_items": total,
                "bytes": sum(len(str(v["value"])) for v in self.store.values()),
                "cmd_get": 0,  # Would track in real implementation
                "cmd_set": 0,
                "get_hits": 0,
                "get_misses": 0
            }


print("\n--- Redis Implementation Demonstration ---")
redis = RedisCache()

print("\n1. Basic string operations:")
redis.set("user:1001", "Alice", ttl=60)
print(f"   GET user:1001 = {redis.get('user:1001')}")

print("\n2. Hash operations:")
redis.hset("user:profile:1001", "name", "Alice")
redis.hset("user:profile:1001", "email", "alice@example.com")
print(f"   HGET user:profile:1001 name = {redis.hget('user:profile:1001', 'name')}")
print(f"   HGETALL user:profile:1001 = {redis.hgetall('user:profile:1001')}")

print("\n3. Set operations:")
redis.sadd("user:1001:roles", "admin", "editor")
print(f"   SMEMBERS user:1001:roles = {redis.smembers('user:1001:roles')}")

print("\n4. Pub/Sub for cache invalidation:")
def on_invalidation(message):
    print(f"    [Pub/Sub] Received: {message}")

redis.subscribe("cache:invalidate", on_invalidation)
redis.publish("cache:invalidate", "user:1001 updated")

print("\n5. Transactions:")
redis.multi()
redis.set("temp:1", "value1")
redis.set("temp:2", "value2")
results = redis.exec()
print(f"   Transaction results: {results}")

print("\n--- Memcached Implementation Demonstration ---")
memcached = MemcachedCache()

print("\n1. Basic operations:")
memcached.set("counter", "10", ttl=60)
print(f"   GET counter = {memcached.get('counter')}")

print("\n2. CAS (Check-And-Set) operations:")
value, cas_token = memcached.gets("counter")
print(f"   GETS counter = ({value}, cas_token={cas_token})")
if cas_token:
    success = memcached.cas("counter", "11", cas_token)
    print(f"   CAS update success: {success}")

print("\n3. Atomic increment:")
memcached.set("page_views", "100", ttl=60)
new_value = memcached.incr("page_views", 5)
print(f"   INCR page_views by 5 = {new_value}")

print("\n4. Add only if doesn't exist:")
success1 = memcached.add("unique_key", "value1")
success2 = memcached.add("unique_key", "value2")  # Should fail
print(f"   ADD unique_key first time: {success1}")
print(f"   ADD unique_key second time: {success2}")

print("\n5. Multi-get:")
memcached.set("key1", "value1")
memcached.set("key2", "value2")
multi_result = memcached.get_multi(["key1", "key2", "nonexistent"])
print(f"   GET_MULTI result: {multi_result}")


# ============================================================================
# PART 4: ADVANCED CACHING STRATEGIES
# ============================================================================

print("\n" + "=" * 30)
print("ADVANCED CACHING STRATEGIES")
print("=" * 30)

class CacheLayer:
    """Multi-layer caching strategy"""
    
    def __init__(self):
        # L1: In-memory cache (fastest, smallest)
        self.l1_cache = InMemoryCache()
        
        # L2: Redis-like cache (distributed, medium speed)
        self.l2_cache = RedisCache()
        
        # L3: Memcached-like cache (distributed, good for large objects)
        self.l3_cache = MemcachedCache()
        
        # Database simulation
        self.database = {}
        
        # Statistics
        self.stats = {
            "l1_hits": 0,
            "l2_hits": 0,
            "l3_hits": 0,
            "db_hits": 0,
            "misses": 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """
        Multi-level cache lookup (L1 → L2 → L3 → Database)
        Implements cache-aside pattern
        """
        # Level 1: In-memory cache
        value = self.l1_cache.get(key)
        if value is not None:
            self.stats["l1_hits"] += 1
            print(f"  [L1 Hit] {key}")
            return value
        
        # Level 2: Redis cache
        value = self.l2_cache.get(key)
        if value is not None:
            self.stats["l2_hits"] += 1
            print(f"  [L2 Hit] {key}")
            # Populate L1 cache
            self.l1_cache.set(key, value, ttl=30)
            return value
        
        # Level 3: Memcached cache
        value = self.l3_cache.get(key)
        if value is not None:
            self.stats["l3_hits"] += 1
            print(f"  [L3 Hit] {key}")
            # Populate L1 and L2 caches
            self.l1_cache.set(key, value, ttl=30)
            self.l2_cache.set(key, value, ttl=300)
            return value
        
        # Database (cache miss)
        value = self.database.get(key)
        if value is not None:
            self.stats["db_hits"] += 1
            print(f"  [DB Hit] {key}")
            # Populate all cache levels
            self.l1_cache.set(key, value, ttl=30)
            self.l2_cache.set(key, value, ttl=300)
            self.l3_cache.set(key, value, ttl=3600)
            return value
        
        # Complete miss
        self.stats["misses"] += 1
        print(f"  [Miss] {key}")
        return None
    
    def set(self, key: str, value: Any, strategy: str = "write-through"):
        """
        Set value with different write strategies
        """
        # Update database
        self.database[key] = value
        
        if strategy == "write-through":
            # Update all cache levels synchronously
            self.l1_cache.set(key, value, ttl=30)
            self.l2_cache.set(key, value, ttl=300)
            self.l3_cache.set(key, value, ttl=3600)
            print(f"  [Write-Through] Updated all cache levels for {key}")
        
        elif strategy == "write-behind":
            # Update L1 immediately, others async
            self.l1_cache.set(key, value, ttl=30)
            
            def update_async():
                time.sleep(0.05)
                self.l2_cache.set(key, value, ttl=300)
                self.l3_cache.set(key, value, ttl=3600)
                print(f"  [Write-Behind] Async updated L2/L3 for {key}")
            
            threading.Thread(target=update_async, daemon=True).start()
        
        elif strategy == "invalidate":
            # Invalidate cache entries
            self.l1_cache.delete(key)
            self.l2_cache.delete(key)
            self.l3_cache.delete(key)
            print(f"  [Invalidate] Removed {key} from all cache levels")
        
        return True
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = sum(self.stats.values())
        if total == 0:
            hit_rate = 0
        else:
            hit_rate = (self.stats["l1_hits"] + self.stats["l2_hits"] + 
                       self.stats["l3_hits"]) / total * 100
        
        return {
            **self.stats,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "l1_hit_rate": round(self.stats["l1_hits"] / max(1, total) * 100, 2),
            "effective_latency_reduction": self._calculate_latency_reduction()
        }
    
    def _calculate_latency_reduction(self) -> Dict[str, float]:
        """Calculate estimated latency savings"""
        # Assumed latencies (in milliseconds)
        latencies = {
            "l1": 0.1,    # In-memory
            "l2": 1,      # Redis
            "l3": 2,      # Memcached
            "db": 10      # Database
        }
        
        total_requests = sum(self.stats.values())
        if total_requests == 0:
            return {"average_ms": 0, "total_savings_ms": 0}
        
        # Calculate weighted average latency
        avg_latency = (
            self.stats["l1_hits"] * latencies["l1"] +
            self.stats["l2_hits"] * latencies["l2"] +
            self.stats["l3_hits"] * latencies["l3"] +
            self.stats["db_hits"] * latencies["db"]
        ) / total_requests
        
        # Calculate savings compared to always hitting DB
        db_only_latency = latencies["db"]
        savings_per_request = db_only_latency - avg_latency
        
        return {
            "average_ms": round(avg_latency, 2),
            "savings_per_request_ms": round(savings_per_request, 2),
            "total_savings_ms": round(savings_per_request * total_requests, 2)
        }


print("\n--- Multi-layer Caching Strategy ---")
cache_layer = CacheLayer()

# Populate database
cache_layer.database = {
    "product:1": {"id": 1, "name": "Laptop", "price": 999},
    "product:2": {"id": 2, "name": "Mouse", "price": 25},
    "product:3": {"id": 3, "name": "Keyboard", "price": 75},
}

print("\nSimulating cache access patterns:")
# First access - should miss all caches, hit database
print("\n1. First access (cache miss → database):")
result1 = cache_layer.get("product:1")
print(f"   Result: {result1['name'] if result1 else 'None'}")

# Second access - should hit L1 cache
print("\n2. Second access (L1 cache hit):")
result2 = cache_layer.get("product:1")
print(f"   Result: {result2['name'] if result2 else 'None'}")

# Access different product - should hit database then populate caches
print("\n3. Access new product (database → populate caches):")
result3 = cache_layer.get("product:2")
print(f"   Result: {result3['name'] if result3 else 'None'}")

# Access third product
print("\n4. Access third product:")
result4 = cache_layer.get("product:3")
print(f"   Result: {result4['name'] if result4 else 'None'}")

# Access first product again (should hit L1)
print("\n5. Access first product again (L1 hit):")
result5 = cache_layer.get("product:1")

# Test write strategies
print("\n6. Testing write strategies:")
print("   a) Write-through:")
cache_layer.set("product:4", {"id": 4, "name": "Monitor", "price": 200}, 
               strategy="write-through")
print(f"   b) Get after write-through: {cache_layer.get('product:4')}")

print("\n   c) Write-behind:")
cache_layer.set("product:5", {"id": 5, "name": "Webcam", "price": 50},
               strategy="write-behind")
time.sleep(0.1)  # Allow async write to complete
print(f"   d) Get after write-behind: {cache_layer.get('product:5')}")

print("\n   e) Invalidate:")
cache_layer.set("product:1", {"id": 1, "name": "Laptop Pro", "price": 1299},
               strategy="invalidate")
print(f"   f) Get after invalidate (should hit database): {cache_layer.get('product:1')}")

# Show statistics
print("\nCache Statistics:")
stats = cache_layer.get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")


# ============================================================================
# PART 5: REAL-WORLD CACHING PATTERNS
# ============================================================================

print("\n" + "=" * 30)
print("REAL-WORLD CACHING PATTERNS")
print("=" * 30)

class CachePatterns:
    """Common caching patterns used in production systems"""
    
    @staticmethod
    def cache_aside_pattern(data_source: Callable[[str], Any], 
                           cache: CacheBackend,
                           key: str,
                           ttl: int = 300) -> Any:
        """
        Cache-Aside (Lazy Loading) Pattern:
        1. Check cache first
        2. If miss, load from data source
        3. Store in cache for future requests
        """
        # Try cache first
        cached_value = cache.get(key)
        if cached_value is not None:
            print(f"  [Cache-Aside] Cache hit for {key}")
            return cached_value
        
        # Cache miss - load from data source
        print(f"  [Cache-Aside] Cache miss for {key}, loading from source")
        value = data_source(key)
        
        # Store in cache for future requests
        if value is not None:
            cache.set(key, value, ttl=ttl)
            print(f"  [Cache-Aside] Stored {key} in cache with TTL {ttl}s")
        
        return value
    
    @staticmethod
    def write_through_pattern(data_source: Callable[[str, Any], bool],
                             cache: CacheBackend,
                             key: str,
                             value: Any,
                             ttl: int = 300) -> bool:
        """
        Write-Through Pattern:
        1. Write to data source first
        2. Then write to cache
        3. Ensures cache consistency
        """
        # Write to data source
        success = data_source(key, value)
        if not success:
            return False
        
        # Write to cache
        cache.set(key, value, ttl=ttl)
        print(f"  [Write-Through] Updated {key} in cache and data source")
        return True
    
    @staticmethod
    def write_behind_pattern(data_source: Callable[[str, Any], bool],
                            cache: CacheBackend,
                            key: str,
                            value: Any,
                            ttl: int = 300) -> bool:
        """
        Write-Behind (Write-Back) Pattern:
        1. Write to cache immediately
        2. Async write to data source
        3. Better performance, risk of data loss
        """
        # Write to cache immediately
        cache.set(key, value, ttl=ttl)
        print(f"  [Write-Behind] Updated {key} in cache immediately")
        
        # Async write to data source
        def async_write():
            try:
                data_source(key, value)
                print(f"  [Write-Behind] Async write completed for {key}")
            except Exception as e:
                print(f"  [Write-Behind] Async write failed: {e}")
        
        threading.Thread(target=async_write, daemon=True).start()
        return True
    
    @staticmethod
    def read_through_pattern(cache: CacheBackend,
                            data_loader: Callable[[str], Any],
                            key: str,
                            ttl: int = 300) -> Any:
        """
        Read-Through Pattern:
        1. Cache automatically loads from data source on miss
        2. Transparent to application
        """
        # This pattern requires cache to support loading callbacks
        # Simulated implementation
        value = cache.get(key)
        if value is None:
            # Cache would automatically call data_loader
            value = data_loader(key)
            if value is not None:
                cache.set(key, value, ttl=ttl)
                print(f"  [Read-Through] Cache loaded {key} from data source")
        
        return value
    
    @staticmethod
    def cache_stampede_prevention(cache: CacheBackend,
                                 data_source: Callable[[str], Any],
                                 key: str,
                                 ttl: int = 300,
                                 lock_timeout: int = 10) -> Any:
        """
        Prevent Cache Stampede (Thundering Herd):
        Multiple requests for expired key don't all hit data source
        """
        # Try to get from cache
        value = cache.get(key)
        if value is not None:
            return value
        
        # Try to acquire lock before loading
        lock_key = f"lock:{key}"
        lock_acquired = cache.add(lock_key, "locked", ttl=lock_timeout)
        
        if lock_acquired:
            try:
                # This request loads the data
                print(f"  [Stampede Prevention] {key} cache expired, loading...")
                value = data_source(key)
                if value is not None:
                    cache.set(key, value, ttl=ttl)
                return value
            finally:
                # Release lock
                cache.delete(lock_key)
        else:
            # Another request is loading, wait and retry
            print(f"  [Stampede Prevention] Waiting for {key} to be loaded...")
            for _ in range(50):  # Wait up to 5 seconds
                time.sleep(0.1)
                value = cache.get(key)
                if value is not None:
                    return value
            
            # Fallback to direct load
            return data_source(key)
    
    @staticmethod
    def cache_warming_strategy(cache: CacheBackend,
                              data_keys: List[str],
                              data_loader: Callable[[str], Any],
                              ttl: int = 3600):
        """
        Cache Warming: Pre-load cache before peak traffic
        """
        print(f"  [Cache Warming] Pre-loading {len(data_keys)} items...")
        
        for key in data_keys:
            try:
                value = data_loader(key)
                if value is not None:
                    cache.set(key, value, ttl=ttl)
            except Exception as e:
                print(f"  [Cache Warming] Failed to load {key}: {e}")
        
        print(f"  [Cache Warming] Completed")


# Mock data source functions
def mock_data_source(key: str) -> Any:
    """Simulate slow data source"""
    time.sleep(0.1)  # Simulate 100ms latency
    data = {
        "user:1001": {"id": 1001, "name": "Alice", "email": "alice@example.com"},
        "product:999": {"id": 999, "name": "Gaming PC", "price": 1499},
        "config:site": {"theme": "dark", "language": "en"}
    }
    print(f"    [Data Source] Loading {key}")
    return data.get(key)

def mock_update_source(key: str, value: Any) -> bool:
    """Simulate data source update"""
    print(f"    [Update Source] Updating {key} = {value}")
    time.sleep(0.05)  # Simulate write latency
    return True


print("\n--- Real-World Cache Pattern Examples ---")
cache = InMemoryCache()

print("\n1. Cache-Aside Pattern:")
result = CachePatterns.cache_aside_pattern(
    data_source=mock_data_source,
    cache=cache,
    key="user:1001",
    ttl=60
)
print(f"   Result: {result}")

print("\n2. Write-Through Pattern:")
success = CachePatterns.write_through_pattern(
    data_source=mock_update_source,
    cache=cache,
    key="user:1002",
    value={"id": 1002, "name": "Bob"},
    ttl=60
)
print(f"   Success: {success}")

print("\n3. Cache Stampede Prevention:")
# Simulate multiple concurrent requests for same expired key
def concurrent_request(key):
    result = CachePatterns.cache_stampede_prevention(
        cache=cache,
        data_source=mock_data_source,
        key=key,
        ttl=5
    )
    return result

print("\n   Simulating 5 concurrent requests for expired key:")
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(concurrent_request, "product:999") 
              for _ in range(5)]
    results = [f.result() for f in futures]

print(f"   All requests completed, got {len(results)} results")

print("\n4. Cache Warming:")
CachePatterns.cache_warming_strategy(
    cache=cache,
    data_keys=["config:site", "user:1001", "product:999"],
    data_loader=mock_data_source,
    ttl=3600
)

# ============================================================================
# SUMMARY & BEST PRACTICES
# ============================================================================

print("\n" + "=" * 70)
print("CACHING BEST PRACTICES SUMMARY")
print("=" * 70)

print("""
WHEN TO CACHE (Decision Matrix):
--------------------------------
1. READ-HEAVY DATA: Reads > Writes * 10
2. COMPUTATIONALLY EXPENSIVE: > 100ms to compute/fetch
3. STABLE DATA: Low volatility (< 10% change frequency)
4. LARGE STATIC ASSETS: Images, CSS, JS bundles
5. EXTERNAL API RESPONSES: With rate limits or high latency

WHEN NOT TO CACHE:
------------------
1. REAL-TIME DATA: Stock prices, live scores
2. FREQUENTLY UPDATED: Shopping cart contents
3. SENSITIVE DATA: Passwords, payment info
4. VERY SMALL DATASETS: < 1KB, faster to recompute
5. UNIQUE REQUESTS: Never repeated

CACHE INVALIDATION STRATEGIES:
------------------------------
1. TIME-BASED (TTL):
   - Simple, automatic cleanup
   - Risk of stale data before expiry
   
2. WRITE-THROUGH:
   - Cache and source always consistent
   - Higher write latency
   
3. WRITE-BEHIND:
   - Better write performance
   - Risk of data loss on crash
   
4. INVALIDATE-ON-WRITE:
   - Simple, ensures fresh reads
   - Causes cache misses after writes
   
5. VERSION-BASED:
   - Precise control over cache freshness
   - Requires version tracking

6. EVENT-BASED:
   - Real-time invalidation
   - Complex infrastructure needed

CHOOSING CACHE TOOLS:
---------------------
REDIS (Use when you need):
- Rich data structures (hashes, lists, sets, sorted sets)
- Pub/Sub messaging
- Persistence to disk
- Lua scripting
- Transactions
- Geospatial indexes

MEMCACHED (Use when you need):
- Simple key-value store
- Multi-threaded performance
- Very large object storage
- Simple horizontal scaling
- CAS operations for atomic updates

IN-MEMORY CACHE (Use when you need):
- Ultra-fast access (nanoseconds)
- Single process/application
- Small dataset fits in memory
- No network overhead

MULTI-LEVEL CACHING STRATEGY:
-----------------------------
L1: In-memory cache (per instance, ~MBs, nanoseconds)
  ↓ On miss
L2: Redis cache (distributed, ~GBs, milliseconds)
  ↓ On miss
L3: Memcached cache (distributed, ~TBs, milliseconds)
  ↓ On miss
Database/External API (seconds)

MONITORING & METRICS:
---------------------
1. Cache hit ratio: Target > 95%
2. Latency percentiles: P95, P99
3. Memory usage and eviction rate
4. Network bandwidth for distributed caches
5. Error rates and connection issues

COMMON PITFALLS TO AVOID:
--------------------------
1. CACHE STAMPEDE: Use locks or early refresh
2. CACHE POLLUTION: Validate data before caching
3. MEMORY LEAKS: Set appropriate TTLs
4. HOT KEYS: Shard frequently accessed keys
5. CACHE PENETRATION: Use Bloom filters for non-existent keys
6. CACHE AVALANCHE: Randomize TTLs across keys

SECURITY CONSIDERATIONS:
------------------------
1. Never cache sensitive data without encryption
2. Validate cache data on retrieval
3. Use separate cache instances for different security zones
4. Implement cache key namespacing
5. Regularly audit cache contents
""")

print("\n" + "=" * 70)
print("CACHING DEMONSTRATION COMPLETE")
print("=" * 70)