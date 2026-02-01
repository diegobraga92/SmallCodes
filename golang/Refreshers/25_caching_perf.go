/*
GOLANG CACHING & PERFORMANCE OPTIMIZATION
============================================
Comprehensive examples covering concepts from junior to senior level.
Includes real-world patterns, strategies, and benchmarks.
*/

package main

import (
	"context"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"sync"
	"sync/atomic"
	"time"

	"github.com/allegro/bigcache"  // Fast in-memory cache
	"github.com/coocood/freecache" // Zero GC cache
	// Memcached client
	"github.com/go-redis/redis/v8"  // Redis client
	"github.com/patrickmn/go-cache" // In-memory caching
	"go.uber.org/zap"               // Structured logging
)

// ============================================================================
// 1. IN-MEMORY CACHING (Junior to Mid Level)
// ============================================================================
type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
	LastLogin time.Time `json:"last_login"`
}

type Product struct {
	ID       string  `json:"id"`
	Name     string  `json:"name"`
	Price    float64 `json:"price"`
	Category string  `json:"category"`
	Stock    int     `json:"stock"`
}

func demonstrateInMemoryCaching() {
	fmt.Println("\n=== 1. IN-MEMORY CACHING ===")

	// Option 1: Simple sync.Map (built-in, concurrent-safe)
	var syncMapCache sync.Map

	// Store value
	syncMapCache.Store("user:123", User{
		ID:    "123",
		Name:  "John Doe",
		Email: "john@example.com",
	})

	// Load value
	if val, ok := syncMapCache.Load("user:123"); ok {
		user := val.(User)
		fmt.Printf("sync.Map Cache - User: %s, Email: %s\n", user.Name, user.Email)
	}

	// Option 2: go-cache (TTL support, automatic cleanup)
	gc := cache.New(5*time.Minute, 10*time.Minute) // Default expiration 5min, cleanup every 10min

	// Set with expiration
	gc.Set("product:456", Product{
		ID:    "456",
		Name:  "Laptop",
		Price: 1299.99,
	}, cache.DefaultExpiration)

	// Get with type assertion
	if x, found := gc.Get("product:456"); found {
		product := x.(Product)
		fmt.Printf("go-cache - Product: %s, Price: $%.2f\n", product.Name, product.Price)
	}

	// Option 3: bigcache (optimized for millions of entries)
	bigCacheConfig := bigcache.DefaultConfig(10 * time.Minute)
	bigCacheConfig.Shards = 1024
	bigCacheConfig.HardMaxCacheSize = 256 // 256MB
	bigCacheConfig.MaxEntrySize = 5000    // 5KB per entry

	bigCache, err := bigcache.NewBigCache(bigCacheConfig)
	if err != nil {
		log.Fatal(err)
	}

	// Store in bigcache
	userData, _ := json.Marshal(User{ID: "789", Name: "Alice", Email: "alice@example.com"})
	bigCache.Set("user:789", userData)

	// Retrieve from bigcache
	if entry, err := bigCache.Get("user:789"); err == nil {
		var user User
		json.Unmarshal(entry, &user)
		fmt.Printf("bigcache - User: %s\n", user.Name)
	}

	// Option 4: freecache (zero GC pressure, high performance)
	freeCache := freecache.NewCache(100 * 1024 * 1024) // 100MB cache

	key := []byte("product:999")
	productData, _ := json.Marshal(Product{ID: "999", Name: "Phone", Price: 899.99})
	freeCache.Set(key, productData, 300) // TTL 300 seconds

	if got, err := freeCache.Get(key); err == nil {
		var product Product
		json.Unmarshal(got, &product)
		fmt.Printf("freecache - Product: %s, Price: $%.2f\n", product.Name, product.Price)
	}
}

// ============================================================================
// 2. REDIS USAGE PATTERNS (Mid to Senior Level)
// ============================================================================
type RedisCache struct {
	client *redis.Client
	ctx    context.Context
	logger *zap.Logger
}

func NewRedisCache(addr string) *RedisCache {
	rdb := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: "",  // no password set
		DB:       0,   // use default DB
		PoolSize: 100, // connection pool size
	})

	logger, _ := zap.NewProduction()

	return &RedisCache{
		client: rdb,
		ctx:    context.Background(),
		logger: logger,
	}
}

func (r *RedisCache) demonstrateRedisPatterns() {
	fmt.Println("\n=== 2. REDIS USAGE PATTERNS ===")

	// Pattern 1: Simple Key-Value with TTL
	err := r.client.Set(r.ctx, "session:user:123", "session_token_abc", 24*time.Hour).Err()
	if err != nil {
		r.logger.Error("Failed to set Redis key", zap.Error(err))
	}

	val, err := r.client.Get(r.ctx, "session:user:123").Result()
	if err == nil {
		fmt.Printf("Redis GET - Session token: %s\n", val)
	}

	// Pattern 2: Hash for objects
	userData := map[string]interface{}{
		"name":        "John Doe",
		"email":       "john@example.com",
		"last_login":  time.Now().Format(time.RFC3339),
		"login_count": 42,
	}

	r.client.HSet(r.ctx, "user:123", userData)

	// Get specific field
	email, _ := r.client.HGet(r.ctx, "user:123", "email").Result()
	fmt.Printf("Redis HGET - User email: %s\n", email)

	// Get all fields
	allFields, _ := r.client.HGetAll(r.ctx, "user:123").Result()
	fmt.Printf("Redis HGETALL - Fields: %d\n", len(allFields))

	// Pattern 3: Sorted Sets for leaderboards
	leaderboardKey := "game:leaderboard"
	r.client.ZAdd(r.ctx, leaderboardKey, &redis.Z{
		Score:  1500,
		Member: "player1",
	})
	r.client.ZAdd(r.ctx, leaderboardKey, &redis.Z{
		Score:  1800,
		Member: "player2",
	})
	r.client.ZAdd(r.ctx, leaderboardKey, &redis.Z{
		Score:  2200,
		Member: "player3",
	})

	// Get top 3 players
	topPlayers, _ := r.client.ZRevRangeWithScores(r.ctx, leaderboardKey, 0, 2).Result()
	fmt.Println("Redis Sorted Set - Top players:")
	for i, player := range topPlayers {
		fmt.Printf("  %d. %s: %.0f points\n", i+1, player.Member, player.Score)
	}

	// Pattern 4: Lists for recent activities
	activityKey := "user:123:activities"
	r.client.LPush(r.ctx, activityKey, "logged_in", "purchased_item", "updated_profile")

	// Trim list to last 100 items
	r.client.LTrim(r.ctx, activityKey, 0, 99)

	// Get recent activities
	activities, _ := r.client.LRange(r.ctx, activityKey, 0, 9).Result()
	fmt.Printf("Redis List - Recent activities: %v\n", activities)

	// Pattern 5: Sets for unique values
	followersKey := "user:123:followers"
	r.client.SAdd(r.ctx, followersKey, "user:456", "user:789", "user:101")

	// Check if user follows
	isFollower, _ := r.client.SIsMember(r.ctx, followersKey, "user:456").Result()
	fmt.Printf("Redis Set - Is follower: %v\n", isFollower)

	// Pattern 6: Pub/Sub for real-time updates
	pubsub := r.client.Subscribe(r.ctx, "notifications")
	defer pubsub.Close()

	// Goroutine to listen for messages
	go func() {
		for {
			msg, err := pubsub.ReceiveMessage(r.ctx)
			if err != nil {
				break
			}
			fmt.Printf("Redis Pub/Sub - Channel: %s, Message: %s\n", msg.Channel, msg.Payload)
		}
	}()

	// Publish a message
	r.client.Publish(r.ctx, "notifications", "New order received!")
	time.Sleep(100 * time.Millisecond)

	// Pattern 7: Bitmaps for feature flags
	featuresKey := "user:123:features"
	r.client.SetBit(r.ctx, featuresKey, 0, 1) // Enable feature 0
	r.client.SetBit(r.ctx, featuresKey, 3, 1) // Enable feature 3

	// Check if feature is enabled
	featureEnabled, _ := r.client.GetBit(r.ctx, featuresKey, 0).Result()
	fmt.Printf("Redis Bitmap - Feature 0 enabled: %d\n", featureEnabled)

	// Pattern 8: HyperLogLog for unique count estimation
	hllKey := "unique_visitors:daily"
	r.client.PFAdd(r.ctx, hllKey, "192.168.1.1", "192.168.1.2", "192.168.1.1")
	count, _ := r.client.PFCount(r.ctx, hllKey).Result()
	fmt.Printf("Redis HyperLogLog - Unique visitors: %d\n", count)
}

// ============================================================================
// 3. CACHE INVALIDATION STRATEGIES (Senior Level)
// ============================================================================
type CacheInvalidator struct {
	mu            sync.RWMutex
	cache         *cache.Cache
	redisClient   *redis.Client
	invalidation  map[string][]string // Key to dependent keys mapping
	versionPrefix string              // For cache versioning
}

func NewCacheInvalidator() *CacheInvalidator {
	return &CacheInvalidator{
		cache:         cache.New(10*time.Minute, 5*time.Minute),
		invalidation:  make(map[string][]string),
		versionPrefix: fmt.Sprintf("v%d:", time.Now().Unix()),
	}
}

func (ci *CacheInvalidator) demonstrateInvalidationStrategies() {
	fmt.Println("\n=== 3. CACHE INVALIDATION STRATEGIES ===")

	// Strategy 1: Time-based expiration (TTL)
	ci.cache.Set("product:123", Product{ID: "123", Name: "Product A"}, 5*time.Minute)
	fmt.Println("Strategy 1: TTL-based expiration set (5 minutes)")

	// Strategy 2: Explicit invalidation
	ci.cache.Set("user:456", User{ID: "456", Name: "Bob"}, cache.NoExpiration)
	ci.cache.Delete("user:456")
	fmt.Println("Strategy 2: Explicit cache deletion")

	// Strategy 3: Write-through invalidation
	ci.registerDependency("order:789", []string{"user:789:orders", "user:789:stats"})
	ci.invalidateDependencies("order:789")
	fmt.Println("Strategy 3: Dependency-based invalidation")

	// Strategy 4: Version-based caching (cache busting)
	versionedKey := ci.getVersionedKey("product:999")
	ci.cache.Set(versionedKey, Product{ID: "999", Name: "Versioned Product"}, cache.NoExpiration)
	fmt.Printf("Strategy 4: Versioned key: %s\n", versionedKey)

	// Strategy 5: Event-driven invalidation
	ci.setupEventDrivenInvalidation()

	// Strategy 6: Probabilistic early expiration (to prevent thundering herd)
	ci.cache.Set("hot:key", "hot value", 10*time.Minute)

	// Add jitter to expiration
	go ci.refreshWithJitter("hot:key", func() interface{} {
		return "refreshed value"
	}, 10*time.Minute, 30*time.Second)

	fmt.Println("Strategy 6: Jitter added to prevent thundering herd")

	// Strategy 7: Namespace invalidation
	ci.invalidateNamespace("user:123:")
	fmt.Println("Strategy 7: Namespace-based invalidation")
}

func (ci *CacheInvalidator) registerDependency(key string, dependencies []string) {
	ci.mu.Lock()
	defer ci.mu.Unlock()
	ci.invalidation[key] = dependencies
}

func (ci *CacheInvalidator) invalidateDependencies(key string) {
	ci.mu.RLock()
	deps, exists := ci.invalidation[key]
	ci.mu.RUnlock()

	if exists {
		for _, dep := range deps {
			ci.cache.Delete(dep)
		}
	}
}

func (ci *CacheInvalidator) getVersionedKey(key string) string {
	return ci.versionPrefix + key
}

func (ci *CacheInvalidator) invalidateAll() {
	// Invalidate by changing version prefix
	ci.versionPrefix = fmt.Sprintf("v%d:", time.Now().Unix())
	fmt.Println("Cache version changed, all versioned keys invalidated")
}

func (ci *CacheInvalidator) invalidateNamespace(namespace string) {
	// In a real implementation, you would iterate through keys with the namespace prefix
	// For Redis: Use SCAN command with MATCH pattern
	fmt.Printf("Invalidated all keys starting with: %s\n", namespace)
}

func (ci *CacheInvalidator) refreshWithJitter(key string, fetchFunc func() interface{}, ttl, jitter time.Duration) {
	// Calculate jitter
	jitterTime := time.Duration(rand.Int63n(int64(jitter)))
	adjustedTTL := ttl - jitterTime

	time.Sleep(adjustedTTL)

	// Refresh the cache
	newValue := fetchFunc()
	ci.cache.Set(key, newValue, ttl)
	fmt.Printf("Cache key %s refreshed with jitter\n", key)
}

func (ci *CacheInvalidator) setupEventDrivenInvalidation() {
	// Simulate event-driven invalidation
	go func() {
		// In real application, this would listen to a message queue
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()

		for range ticker.C {
			// Check for invalidation events
			ci.checkAndInvalidate()
		}
	}()
}

func (ci *CacheInvalidator) checkAndInvalidate() {
	// Check for database changes or external events
	// This is a simplified example
	fmt.Println("Event-driven invalidation check performed")
}

// ============================================================================
// 4. READ-THROUGH VS WRITE-THROUGH CACHE (Mid to Senior Level)
// ============================================================================
type Database interface {
	GetUser(id string) (*User, error)
	SaveUser(user *User) error
	UpdateUser(user *User) error
}

type MockDB struct {
	mu    sync.RWMutex
	users map[string]*User
}

func NewMockDB() *MockDB {
	return &MockDB{
		users: make(map[string]*User),
	}
}

func (db *MockDB) GetUser(id string) (*User, error) {
	db.mu.RLock()
	defer db.mu.RUnlock()

	user, exists := db.users[id]
	if !exists {
		return nil, fmt.Errorf("user not found")
	}
	return user, nil
}

func (db *MockDB) SaveUser(user *User) error {
	db.mu.Lock()
	defer db.mu.Unlock()

	db.users[user.ID] = user
	fmt.Printf("Database: Saved user %s\n", user.ID)
	return nil
}

func (db *MockDB) UpdateUser(user *User) error {
	db.mu.Lock()
	defer db.mu.Unlock()

	db.users[user.ID] = user
	fmt.Printf("Database: Updated user %s\n", user.ID)
	return nil
}

type CacheStrategy interface {
	GetUser(id string) (*User, error)
	SaveUser(user *User) error
}

// READ-THROUGH CACHE: Cache loads data on miss
type ReadThroughCache struct {
	cache  *cache.Cache
	db     Database
	mu     sync.RWMutex
	misses int64
	hits   int64
}

func NewReadThroughCache(db Database) *ReadThroughCache {
	return &ReadThroughCache{
		cache: cache.New(5*time.Minute, 10*time.Minute),
		db:    db,
	}
}

func (rt *ReadThroughCache) GetUser(id string) (*User, error) {
	key := "user:" + id

	// Try cache first
	if cached, found := rt.cache.Get(key); found {
		atomic.AddInt64(&rt.hits, 1)
		return cached.(*User), nil
	}

	// Cache miss - read from DB
	atomic.AddInt64(&rt.misses, 1)
	user, err := rt.db.GetUser(id)
	if err != nil {
		return nil, err
	}

	// Populate cache for future reads
	rt.cache.Set(key, user, cache.DefaultExpiration)
	fmt.Printf("Read-Through: Cache miss for user %s, loaded from DB\n", id)

	return user, nil
}

func (rt *ReadThroughCache) SaveUser(user *User) error {
	// Direct write to DB
	err := rt.db.SaveUser(user)
	if err != nil {
		return err
	}

	// Invalidate cache (or could update cache - write-around)
	rt.cache.Delete("user:" + user.ID)
	fmt.Printf("Read-Through: Invalidated cache for user %s after save\n", user.ID)

	return nil
}

func (rt *ReadThroughCache) Stats() (int64, int64) {
	return atomic.LoadInt64(&rt.hits), atomic.LoadInt64(&rt.misses)
}

// WRITE-THROUGH CACHE: Cache is updated on write
type WriteThroughCache struct {
	cache  *cache.Cache
	db     Database
	mu     sync.RWMutex
	writes int64
}

func NewWriteThroughCache(db Database) *WriteThroughCache {
	return &WriteThroughCache{
		cache: cache.New(5*time.Minute, 10*time.Minute),
		db:    db,
	}
}

func (wt *WriteThroughCache) GetUser(id string) (*User, error) {
	key := "user:" + id

	// Try cache first
	if cached, found := wt.cache.Get(key); found {
		return cached.(*User), nil
	}

	// Cache miss - read from DB
	user, err := wt.db.GetUser(id)
	if err != nil {
		return nil, err
	}

	// Update cache
	wt.cache.Set(key, user, cache.DefaultExpiration)

	return user, nil
}

func (wt *WriteThroughCache) SaveUser(user *User) error {
	key := "user:" + user.ID

	// Update cache first
	wt.cache.Set(key, user, cache.DefaultExpiration)
	fmt.Printf("Write-Through: Updated cache for user %s\n", user.ID)

	// Then write to DB (could be async in real implementation)
	err := wt.db.SaveUser(user)
	if err != nil {
		// Rollback cache on DB failure
		wt.cache.Delete(key)
		return err
	}

	atomic.AddInt64(&wt.writes, 1)
	return nil
}

// WRITE-BEHIND CACHE (Async write-through)
type WriteBehindCache struct {
	cache     *cache.Cache
	db        Database
	writeChan chan *User
	batchSize int
	mu        sync.RWMutex
}

func NewWriteBehindCache(db Database, batchSize int) *WriteBehindCache {
	wbc := &WriteBehindCache{
		cache:     cache.New(5*time.Minute, 10*time.Minute),
		db:        db,
		writeChan: make(chan *User, 1000),
		batchSize: batchSize,
	}

	// Start background writer
	go wbc.batchWriter()

	return wbc
}

func (wb *WriteBehindCache) GetUser(id string) (*User, error) {
	key := "user:" + id

	if cached, found := wb.cache.Get(key); found {
		return cached.(*User), nil
	}

	user, err := wb.db.GetUser(id)
	if err != nil {
		return nil, err
	}

	wb.cache.Set(key, user, cache.DefaultExpiration)
	return user, nil
}

func (wb *WriteBehindCache) SaveUser(user *User) error {
	key := "user:" + user.ID

	// Update cache synchronously
	wb.cache.Set(key, user, cache.DefaultExpiration)

	// Queue for async DB write
	select {
	case wb.writeChan <- user:
		fmt.Printf("Write-Behind: Queued user %s for async write\n", user.ID)
	default:
		// Channel full - could use fallback strategy
		fmt.Printf("Write-Behind: Channel full for user %s\n", user.ID)
	}

	return nil
}

func (wb *WriteBehindCache) batchWriter() {
	batch := make([]*User, 0, wb.batchSize)
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case user := <-wb.writeChan:
			batch = append(batch, user)

			if len(batch) >= wb.batchSize {
				wb.flushBatch(batch)
				batch = batch[:0]
			}

		case <-ticker.C:
			if len(batch) > 0 {
				wb.flushBatch(batch)
				batch = batch[:0]
			}
		}
	}
}

func (wb *WriteBehindCache) flushBatch(batch []*User) {
	fmt.Printf("Write-Behind: Flushing batch of %d users to DB\n", len(batch))

	// In real implementation, use bulk insert or transaction
	for _, user := range batch {
		wb.db.SaveUser(user)
	}
}

func demonstrateCacheStrategies() {
	fmt.Println("\n=== 4. READ-THROUGH VS WRITE-THROUGH CACHE ===")

	db := NewMockDB()

	// Test Read-Through
	fmt.Println("\n--- Read-Through Cache ---")
	rtCache := NewReadThroughCache(db)

	// Save user first (invalidates cache)
	rtCache.SaveUser(&User{ID: "rt1", Name: "ReadThrough User", Email: "rt@example.com"})

	// First read will miss cache
	user1, _ := rtCache.GetUser("rt1")
	fmt.Printf("First read: %s\n", user1.Name)

	// Second read will hit cache
	user2, _ := rtCache.GetUser("rt1")
	fmt.Printf("Second read: %s\n", user2.Name)

	hits, misses := rtCache.Stats()
	fmt.Printf("Stats - Hits: %d, Misses: %d\n", hits, misses)

	// Test Write-Through
	fmt.Println("\n--- Write-Through Cache ---")
	wtCache := NewWriteThroughCache(db)

	wtCache.SaveUser(&User{ID: "wt1", Name: "WriteThrough User", Email: "wt@example.com"})

	// Read should hit cache since it was updated on write
	user3, _ := wtCache.GetUser("wt1")
	fmt.Printf("Read after write-through: %s\n", user3.Name)

	// Test Write-Behind
	fmt.Println("\n--- Write-Behind Cache ---")
	wbCache := NewWriteBehindCache(db, 5)

	// Save multiple users
	for i := 1; i <= 7; i++ {
		wbCache.SaveUser(&User{
			ID:    fmt.Sprintf("wb%d", i),
			Name:  fmt.Sprintf("WriteBehind User %d", i),
			Email: fmt.Sprintf("wb%d@example.com", i),
		})
	}

	// Wait for batch flush
	time.Sleep(2 * time.Second)

	fmt.Println("\nCache Strategy Summary:")
	fmt.Println("- Read-Through: Load on miss, invalidate on write")
	fmt.Println("- Write-Through: Update cache and DB synchronously")
	fmt.Println("- Write-Behind: Update cache immediately, write to DB async")
}

// ============================================================================
// 5. LOAD TESTING & PERFORMANCE OPTIMIZATION (Senior Level)
// ============================================================================
type LoadTester struct {
	concurrentUsers int
	requestsPerUser int
	latencies       []time.Duration
	mu              sync.RWMutex
	errors          int64
	cache           *cache.Cache
}

func NewLoadTester(users, requests int) *LoadTester {
	return &LoadTester{
		concurrentUsers: users,
		requestsPerUser: requests,
		latencies:       make([]time.Duration, 0, users*requests),
		cache:           cache.New(5*time.Minute, 10*time.Minute),
	}
}

func (lt *LoadTester) runLoadTest(cacheStrategy func() error) LoadTestResult {
	var wg sync.WaitGroup
	startTime := time.Now()

	for i := 0; i < lt.concurrentUsers; i++ {
		wg.Add(1)
		go func(userID int) {
			defer wg.Done()

			for j := 0; j < lt.requestsPerUser; j++ {
				requestStart := time.Now()

				// Simulate cache/database operation
				err := cacheStrategy()

				latency := time.Since(requestStart)

				lt.mu.Lock()
				lt.latencies = append(lt.latencies, latency)
				lt.mu.Unlock()

				if err != nil {
					atomic.AddInt64(&lt.errors, 1)
				}

				// Simulate think time
				time.Sleep(time.Duration(rand.Intn(50)) * time.Millisecond)
			}
		}(i)
	}

	wg.Wait()

	duration := time.Since(startTime)

	// Calculate statistics
	lt.mu.RLock()
	defer lt.mu.RUnlock()

	var totalLatency time.Duration
	minLatency := time.Hour
	maxLatency := time.Duration(0)

	for _, latency := range lt.latencies {
		totalLatency += latency
		if latency < minLatency {
			minLatency = latency
		}
		if latency > maxLatency {
			maxLatency = latency
		}
	}

	avgLatency := totalLatency / time.Duration(len(lt.latencies))

	// Calculate percentiles
	sortedLatencies := make([]time.Duration, len(lt.latencies))
	copy(sortedLatencies, lt.latencies)

	// Simple sort for percentiles
	for i := range sortedLatencies {
		for j := i + 1; j < len(sortedLatencies); j++ {
			if sortedLatencies[i] > sortedLatencies[j] {
				sortedLatencies[i], sortedLatencies[j] = sortedLatencies[j], sortedLatencies[i]
			}
		}
	}

	p50 := sortedLatencies[int(float64(len(sortedLatencies))*0.5)]
	p95 := sortedLatencies[int(float64(len(sortedLatencies))*0.95)]
	p99 := sortedLatencies[int(float64(len(sortedLatencies))*0.99)]

	return LoadTestResult{
		TotalRequests:     len(lt.latencies),
		Duration:          duration,
		RequestsPerSecond: float64(len(lt.latencies)) / duration.Seconds(),
		AvgLatency:        avgLatency,
		MinLatency:        minLatency,
		MaxLatency:        maxLatency,
		P50Latency:        p50,
		P95Latency:        p95,
		P99Latency:        p99,
		ErrorCount:        int(atomic.LoadInt64(&lt.errors)),
		ErrorRate:         float64(atomic.LoadInt64(&lt.errors)) / float64(len(lt.latencies)),
	}
}

type LoadTestResult struct {
	TotalRequests     int
	Duration          time.Duration
	RequestsPerSecond float64
	AvgLatency        time.Duration
	MinLatency        time.Duration
	MaxLatency        time.Duration
	P50Latency        time.Duration
	P95Latency        time.Duration
	P99Latency        time.Duration
	ErrorCount        int
	ErrorRate         float64
}

func (r LoadTestResult) String() string {
	return fmt.Sprintf(`Load Test Results:
  Total Requests: %d
  Duration: %v
  RPS: %.2f
  Latency:
    Avg: %v
    Min: %v
    Max: %v
    P50: %v
    P95: %v
    P99: %v
  Errors: %d (%.2f%%)`,
		r.TotalRequests,
		r.Duration,
		r.RequestsPerSecond,
		r.AvgLatency,
		r.MinLatency,
		r.MaxLatency,
		r.P50Latency,
		r.P95Latency,
		r.P99Latency,
		r.ErrorCount,
		r.ErrorRate*100)
}

func simulateCacheHit() error {
	// Simulate cache hit (fast)
	time.Sleep(time.Duration(1+rand.Intn(5)) * time.Millisecond)
	return nil
}

func simulateCacheMiss() error {
	// Simulate cache miss + DB read (slower)
	time.Sleep(time.Duration(10+rand.Intn(20)) * time.Millisecond)
	return nil
}

func simulateDatabaseWrite() error {
	// Simulate database write (slowest)
	time.Sleep(time.Duration(20+rand.Intn(30)) * time.Millisecond)
	return nil
}

func demonstrateLoadTesting() {
	fmt.Println("\n=== 5. LOAD TESTING & PERFORMANCE OPTIMIZATION ===")

	// Warm up
	fmt.Println("Warming up...")
	time.Sleep(100 * time.Millisecond)

	// Test 1: Cache hits (best case)
	fmt.Println("\n--- Test 1: Cache Hits (95% hit rate) ---")
	tester1 := NewLoadTester(50, 100)

	result1 := tester1.runLoadTest(func() error {
		if rand.Float32() < 0.95 {
			return simulateCacheHit()
		}
		return simulateCacheMiss()
	})

	fmt.Println(result1.String())

	// Test 2: Cache misses (worst case)
	fmt.Println("\n--- Test 2: Cache Misses (5% hit rate) ---")
	tester2 := NewLoadTester(50, 100)

	result2 := tester2.runLoadTest(func() error {
		if rand.Float32() < 0.05 {
			return simulateCacheHit()
		}
		return simulateCacheMiss()
	})

	fmt.Println(result2.String())

	// Test 3: Mixed workload
	fmt.Println("\n--- Test 3: Mixed Workload (70% reads, 30% writes) ---")
	tester3 := NewLoadTester(50, 100)

	result3 := tester3.runLoadTest(func() error {
		if rand.Float32() < 0.7 {
			// Read operation
			if rand.Float32() < 0.8 {
				return simulateCacheHit()
			}
			return simulateCacheMiss()
		} else {
			// Write operation
			return simulateDatabaseWrite()
		}
	})

	fmt.Println(result3.String())

	// Performance optimization techniques
	fmt.Println("\n=== PERFORMANCE OPTIMIZATION TECHNIQUES ===")

	// 1. Connection pooling demonstration
	demonstrateConnectionPooling()

	// 2. Memory optimization
	demonstrateMemoryOptimization()

	// 3. Concurrent patterns
	demonstrateConcurrentPatterns()
}

func demonstrateConnectionPooling() {
	fmt.Println("\n1. Connection Pooling:")
	fmt.Println("   - Reuse database/Redis connections")
	fmt.Println("   - Set appropriate pool size based on workload")
	fmt.Println("   - Monitor connection usage metrics")
}

func demonstrateMemoryOptimization() {
	fmt.Println("\n2. Memory Optimization:")
	fmt.Println("   - Use structs with appropriate field types")
	fmt.Println("   - Consider using []byte instead of strings for large data")
	fmt.Println("   - Implement object pooling for frequently allocated objects")
	fmt.Println("   - Monitor GC pauses and heap usage")

	// Example: Memory-efficient struct
	type OptimizedUser struct {
		ID        [16]byte // Fixed size array instead of string
		Name      string   `json:"name,omitempty"`
		Email     string   `json:"email,omitempty"`
		CreatedAt int64    // Unix timestamp instead of time.Time
		Flags     uint32   // Bit flags for boolean fields
	}

	// Calculate memory usage
	var regularUser User
	var optimizedUser OptimizedUser

	fmt.Printf("   Regular User size: ~%d bytes\n", estimateSize(regularUser))
	fmt.Printf("   Optimized User size: ~%d bytes\n", estimateSize(optimizedUser))
}

func estimateSize(v interface{}) int {
	// Simplified size estimation
	data, _ := json.Marshal(v)
	return len(data)
}

func demonstrateConcurrentPatterns() {
	fmt.Println("\n3. Concurrent Patterns:")
	fmt.Println("   - Use worker pools for concurrent processing")
	fmt.Println("   - Implement backpressure mechanisms")
	fmt.Println("   - Use sync.Pool for temporary objects")
	fmt.Println("   - Consider lock-free data structures for high contention")

	// Worker pool example
	workerPool := NewWorkerPool(10, 100)

	// Submit tasks
	for i := 0; i < 100; i++ {
		taskID := i
		workerPool.Submit(func() {
			// Process task
			time.Sleep(10 * time.Millisecond)
			fmt.Printf("   Worker processed task %d\n", taskID)
		})
	}

	workerPool.Stop()
}

type WorkerPool struct {
	workers   int
	taskQueue chan func()
	wg        sync.WaitGroup
}

func NewWorkerPool(workers, queueSize int) *WorkerPool {
	pool := &WorkerPool{
		workers:   workers,
		taskQueue: make(chan func(), queueSize),
	}

	pool.wg.Add(workers)
	for i := 0; i < workers; i++ {
		go pool.worker()
	}

	return pool
}

func (p *WorkerPool) Submit(task func()) {
	select {
	case p.taskQueue <- task:
		// Task submitted
	default:
		// Queue full - implement backpressure strategy
		fmt.Println("   Worker pool queue full - implementing backpressure")
		// Could: drop task, block, or execute synchronously
		task()
	}
}

func (p *WorkerPool) worker() {
	defer p.wg.Done()

	for task := range p.taskQueue {
		task()
	}
}

func (p *WorkerPool) Stop() {
	close(p.taskQueue)
	p.wg.Wait()
}

// ============================================================================
// ADVANCED CACHING PATTERNS (Senior/Architect Level)
// ============================================================================
type CacheWarmer struct {
	cache     *cache.Cache
	db        Database
	warmKeys  []string
	mu        sync.RWMutex
	isWarming bool
}

func NewCacheWarmer(cache *cache.Cache, db Database) *CacheWarmer {
	return &CacheWarmer{
		cache:    cache,
		db:       db,
		warmKeys: make([]string, 0),
	}
}

func (cw *CacheWarmer) WarmCache(keys []string) {
	cw.mu.Lock()
	cw.isWarming = true
	cw.mu.Unlock()

	fmt.Printf("Cache warmer: Warming %d keys\n", len(keys))

	for _, key := range keys {
		// In real implementation, fetch data and cache it
		cw.cache.Set(key, "warmed_value", 10*time.Minute)
	}

	cw.mu.Lock()
	cw.warmKeys = keys
	cw.isWarming = false
	cw.mu.Unlock()

	fmt.Println("Cache warmer: Warming completed")
}

func (cw *CacheWarmer) GetWarmKeys() []string {
	cw.mu.RLock()
	defer cw.mu.RUnlock()
	return cw.warmKeys
}

// Bloom filter for cache existence checking (memory-efficient)
type BloomFilter struct {
	bitset []byte
	size   uint32
	hashes []func([]byte) uint32
}

func NewBloomFilter(size uint32) *BloomFilter {
	bf := &BloomFilter{
		bitset: make([]byte, (size+7)/8),
		size:   size,
		hashes: []func([]byte) uint32{
			func(data []byte) uint32 {
				h := sha256.New()
				h.Write(data)
				return uint32(h.Sum(nil)[0]) % size
			},
			func(data []byte) uint32 {
				h := sha256.New()
				h.Write(data)
				return uint32(h.Sum(nil)[1]) % size
			},
		},
	}
	return bf
}

func (bf *BloomFilter) Add(key string) {
	data := []byte(key)
	for _, hash := range bf.hashes {
		pos := hash(data)
		byteIndex := pos / 8
		bitIndex := pos % 8
		bf.bitset[byteIndex] |= 1 << bitIndex
	}
}

func (bf *BloomFilter) Contains(key string) bool {
	data := []byte(key)
	for _, hash := range bf.hashes {
		pos := hash(data)
		byteIndex := pos / 8
		bitIndex := pos % 8
		if (bf.bitset[byteIndex] & (1 << bitIndex)) == 0 {
			return false
		}
	}
	return true
}

// ============================================================================
// MAIN FUNCTION - RUN ALL DEMONSTRATIONS
// ============================================================================
func main() {
	fmt.Println("GOLANG CACHING & PERFORMANCE OPTIMIZATION DEMO")
	fmt.Println("=================================================")

	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	// Run all demonstrations
	demonstrateInMemoryCaching()

	// Redis demonstration (commented out since it needs Redis server)
	// redisCache := NewRedisCache("localhost:6379")
	// redisCache.demonstrateRedisPatterns()

	invalidator := NewCacheInvalidator()
	invalidator.demonstrateInvalidationStrategies()

	demonstrateCacheStrategies()

	demonstrateLoadTesting()

	fmt.Println("\n=== SUMMARY ===")
	fmt.Println("1. In-Memory Caching: sync.Map, go-cache, bigcache, freecache")
	fmt.Println("2. Redis Patterns: Hashes, Sorted Sets, Lists, Pub/Sub, Bitmaps")
	fmt.Println("3. Cache Invalidation: TTL, explicit, versioning, event-driven")
	fmt.Println("4. Cache Strategies: Read-through, Write-through, Write-behind")
	fmt.Println("5. Load Testing: Simulate workloads, measure RPS, latency, errors")

	fmt.Println("\nBEST PRACTICES:")
	fmt.Println("- Use appropriate cache size and TTL for your workload")
	fmt.Println("- Implement circuit breakers for cache failures")
	fmt.Println("- Monitor cache hit rates and adjust strategies")
	fmt.Println("- Use connection pooling for external caches (Redis)")
	fmt.Println("- Consider cache warming for critical paths")
	fmt.Println("- Implement graceful degradation when cache is unavailable")
}

/*
INSTRUCTIONS TO RUN:
====================
1. Install dependencies:
   go get github.com/go-redis/redis/v8
   go get github.com/patrickmn/go-cache
   go get github.com/allegro/bigcache
   go get github.com/coocood/freecache
   go get github.com/bradfitz/gomemcache/memcache
   go get go.uber.org/zap

2. For Redis examples, ensure Redis server is running:
   docker run -p 6379:6379 redis

3. Run:
   go run main.go

4. For load testing with more realistic scenarios:
   - Use dedicated tools like vegeta, k6, or wrk
   - Implement distributed load testing for large-scale apps
   - Monitor system resources during tests

KEY TAKEAWAYS:
==============
- Choose cache implementation based on data size and access patterns
- Always set appropriate TTLs to prevent stale data
- Implement proper cache invalidation strategies
- Monitor cache performance metrics (hit rate, latency)
- Use connection pooling for external cache services
- Implement circuit breakers to handle cache failures gracefully
- Consider cache warming for predictable high-traffic periods
- Test cache performance under load with realistic scenarios
*/
