/*
GOLANG MICROSERVICES & DISTRIBUTED SYSTEMS GUIDE
From Junior to Senior Developer Concepts
==========================================
*/

// ============================================================================
// 1. SERVICE BOUNDARIES - Domain-Driven Design (DDD) and Bounded Contexts
// ============================================================================

/*
Service boundaries define clear separation of concerns between microservices.
Key principles:
1. Single Responsibility - Each service handles one business capability
2. Loose Coupling - Services communicate via APIs, not shared databases
3. Independent Deployment - Services can be deployed separately
*/

package main

import (
	"fmt"
)

// Example: E-commerce system with clear service boundaries
type ServiceBoundaries struct{}

// Separate services instead of monolith
func (s *ServiceBoundaries) Demonstrate() {
	fmt.Println("=== Service Boundaries ===")
	
	// Instead of one monolithic service:
	// Monolith{}.HandleOrder() // Bad
	
	// Use separate services:
	orderService := &OrderService{}
	paymentService := &PaymentService{}
	inventoryService := &InventoryService{}
	
	// Each service manages its own domain
	order := orderService.CreateOrder("user123", []string{"item1", "item2"})
	paymentService.ProcessPayment(order.ID, 99.99)
	inventoryService.UpdateStock("item1", -1)
}

// Domain Services
type OrderService struct{}
func (o *OrderService) CreateOrder(userID string, items []string) Order {
	return Order{ID: "order_123", UserID: userID, Items: items}
}

type PaymentService struct{}
func (p *PaymentService) ProcessPayment(orderID string, amount float64) bool {
	fmt.Printf("Processing payment for order %s: $%.2f\n", orderID, amount)
	return true
}

type InventoryService struct{}
func (i *InventoryService) UpdateStock(itemID string, delta int) {
	fmt.Printf("Updating stock for %s: %d\n", itemID, delta)
}

type Order struct {
	ID     string
	UserID string
	Items  []string
}

// ============================================================================
// 2. gRPC BASICS - High-performance RPC framework
// ============================================================================

/*
gRPC uses HTTP/2, Protocol Buffers, and provides:
- Bi-directional streaming
- Authentication
- Load balancing
- Timeout/cancellation propagation
*/

// First, install protoc and protobuf tools:
// go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
// go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

// ============================================================================
// 3. PROTOBUF - Interface Definition Language (IDL) for gRPC
// ============================================================================

/*
// user_service.proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser(GetUserRequest) returns (UserResponse);
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
  rpc StreamUsers(StreamUsersRequest) returns (stream UserResponse);
}

message GetUserRequest {
  string user_id = 1;  // Field numbers, not values
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  UserRole role = 3;
}

enum UserRole {
  ROLE_USER = 0;
  ROLE_ADMIN = 1;
  ROLE_MODERATOR = 2;
}

message UserResponse {
  string id = 1;
  string name = 2;
  string email = 3;
  UserRole role = 4;
  google.protobuf.Timestamp created_at = 5;
}

// Generate Go code: protoc --go_out=. --go-grpc_out=. user_service.proto
*/

// ============================================================================
// 4. SERVICE DISCOVERY - Dynamic service location
// ============================================================================

package main

import (
	"context"
	"fmt"
	"log"
	"time"

	clientv3 "go.etcd.io/etcd/client/v3"
	"google.golang.org/grpc/resolver"
)

// Pattern 1: Client-side discovery with etcd
type ServiceDiscovery struct {
	etcdClient *clientv3.Client
}

func NewServiceDiscovery(endpoints []string) (*ServiceDiscovery, error) {
	client, err := clientv3.New(clientv3.Config{
		Endpoints:   endpoints,
		DialTimeout: 5 * time.Second,
	})
	if err != nil {
		return nil, err
	}
	return &ServiceDiscovery{etcdClient: client}, nil
}

func (sd *ServiceDiscovery) RegisterService(serviceName, address string, ttl int64) error {
	// Register service with lease for automatic cleanup
	resp, err := sd.etcdClient.Grant(context.Background(), ttl)
	if err != nil {
		return err
	}
	
	key := fmt.Sprintf("/services/%s/%s", serviceName, address)
	_, err = sd.etcdClient.Put(context.Background(), key, address, clientv3.WithLease(resp.ID))
	
	// Keep lease alive
	keepAlive, err := sd.etcdClient.KeepAlive(context.Background(), resp.ID)
	if err != nil {
		return err
	}
	
	go func() {
		for range keepAlive {
			// Lease is being kept alive
		}
	}()
	
	return nil
}

func (sd *ServiceDiscovery) DiscoverService(serviceName string) ([]string, error) {
	key := fmt.Sprintf("/services/%s/", serviceName)
	resp, err := sd.etcdClient.Get(context.Background(), key, clientv3.WithPrefix())
	if err != nil {
		return nil, err
	}
	
	var addresses []string
	for _, kv := range resp.Kvs {
		addresses = append(addresses, string(kv.Value))
	}
	return addresses, nil
}

// Pattern 2: DNS-based discovery (simplified)
type DNSDiscovery struct {
	serviceMap map[string][]string
}

func (d *DNSDiscovery) Lookup(serviceName string) ([]string, error) {
	// In production: Implement SRV records lookup
	if addrs, ok := d.serviceMap[serviceName]; ok {
		return addrs, nil
	}
	return nil, fmt.Errorf("service %s not found", serviceName)
}

// ============================================================================
// 5. RATE LIMITING - Control request frequency
// ============================================================================

import (
	"golang.org/x/time/rate"
	"sync"
	"net/http"
)

// Token Bucket Algorithm - Most common rate limiting
type RateLimiter struct {
	limiters map[string]*rate.Limiter
	mu       sync.RWMutex
	rate     rate.Limit  // requests per second
	burst    int         // burst size
}

func NewRateLimiter(r rate.Limit, b int) *RateLimiter {
	return &RateLimiter{
		limiters: make(map[string]*rate.Limiter),
		rate:     r,
		burst:    b,
	}
}

func (rl *RateLimiter) getLimiter(key string) *rate.Limiter {
	rl.mu.RLock()
	limiter, exists := rl.limiters[key]
	rl.mu.RUnlock()
	
	if !exists {
		rl.mu.Lock()
		limiter = rate.NewLimiter(rl.rate, rl.burst)
		rl.limiters[key] = limiter
		rl.mu.Unlock()
	}
	return limiter
}

func (rl *RateLimiter) Allow(key string) bool {
	return rl.getLimiter(key).Allow()
}

// HTTP Middleware for rate limiting
func RateLimitMiddleware(rl *RateLimiter, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Use IP or API key as rate limit key
		key := r.RemoteAddr
		
		if !rl.Allow(key) {
			http.Error(w, "Rate limit exceeded", http.StatusTooManyRequests)
			return
		}
		next.ServeHTTP(w, r)
	})
}

// Distributed rate limiting using Redis (concept)
type DistributedRateLimiter struct {
	// Uses Redis with Lua scripting for atomic operations
	// Implements sliding window or token bucket across instances
}

// ============================================================================
// 6. CIRCUIT BREAKERS - Prevent cascade failures
// ============================================================================

import (
	"github.com/sony/gobreaker"
	"time"
)

// Circuit breaker states: Closed → Open → Half-Open → Closed
type CircuitBreakerDemo struct {
	cb *gobreaker.CircuitBreaker
}

func NewCircuitBreaker(name string) *CircuitBreakerDemo {
	settings := gobreaker.Settings{
		Name:        name,
		MaxRequests: 5,           // Half-open state max requests
		Interval:    10 * time.Second,
		Timeout:     30 * time.Second, // How long to stay open
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			// Trip when 50% of requests fail with at least 10 requests
			return counts.ConsecutiveFailures > 5 ||
				(counts.TotalFailures > 10 && 
					float64(counts.TotalFailures)/float64(counts.Requests) > 0.5)
		},
		OnStateChange: func(name string, from, to gobreaker.State) {
			log.Printf("Circuit breaker %s: %s → %s", name, from, to)
		},
	}
	
	return &CircuitBreakerDemo{
		cb: gobreaker.NewCircuitBreaker(settings),
	}
}

func (c *CircuitBreakerDemo) Execute(fn func() (interface{}, error)) (interface{}, error) {
	// Wraps any function with circuit breaker protection
	return c.cb.Execute(func() (interface{}, error) {
		return fn()
	})
}

// Example usage
func ExternalAPICall() (interface{}, error) {
	// Simulate external service call
	// If this fails repeatedly, circuit will open
	return nil, nil
}

// ============================================================================
// 7. RETRIES & BACKOFF STRATEGIES - Handle transient failures
// ============================================================================

import (
	"math"
	"math/rand"
	"time"
	
	"github.com/cenkalti/backoff/v4"
)

// Exponential Backoff with Jitter (most common)
type RetryStrategy struct {
	MaxRetries int
	BaseDelay  time.Duration
	MaxDelay   time.Duration
}

func NewRetryStrategy(maxRetries int, baseDelay, maxDelay time.Duration) *RetryStrategy {
	return &RetryStrategy{
		MaxRetries: maxRetries,
		BaseDelay:  baseDelay,
		MaxDelay:   maxDelay,
	}
}

func (rs *RetryStrategy) ExponentialBackoff(retry int) time.Duration {
	// Exponential backoff: base * 2^retry
	delay := float64(rs.BaseDelay) * math.Pow(2, float64(retry))
	
	// Add jitter (±15%) to prevent thundering herd
	jitter := 0.15 * delay * (rand.Float64()*2 - 1) // -15% to +15%
	delay += jitter
	
	// Cap at max delay
	if delay > float64(rs.MaxDelay) {
		delay = float64(rs.MaxDelay)
	}
	
	return time.Duration(delay)
}

// Using backoff library (recommended for production)
func RetryWithBackoff(fn func() error, operationName string) error {
	expBackoff := backoff.NewExponentialBackOff()
	expBackoff.InitialInterval = 100 * time.Millisecond
	expBackoff.MaxInterval = 10 * time.Second
	expBackoff.MaxElapsedTime = 30 * time.Second
	expBackoff.RandomizationFactor = 0.5 // Jitter
	
	// With context for cancellation
	ctx := context.Background()
	
	b := backoff.WithContext(expBackoff, ctx)
	
	return backoff.Retry(func() error {
		err := fn()
		if err != nil {
			log.Printf("Operation %s failed: %v, retrying...", operationName, err)
		}
		return err
	}, b)
}

// Retry with specific status codes (HTTP example)
func RetryOnStatusCodes(fn func() (*http.Response, error), retryCodes []int) (*http.Response, error) {
	maxRetries := 3
	for i := 0; i <= maxRetries; i++ {
		resp, err := fn()
		if err != nil {
			if i == maxRetries {
				return nil, err
			}
			time.Sleep(time.Duration(math.Pow(2, float64(i))) * 100 * time.Millisecond)
			continue
		}
		
		// Check if status code warrants retry
		shouldRetry := false
		for _, code := range retryCodes {
			if resp.StatusCode == code {
				shouldRetry = true
				break
			}
		}
		
		if !shouldRetry || i == maxRetries {
			return resp, nil
		}
		
		time.Sleep(time.Duration(math.Pow(2, float64(i))) * 100 * time.Millisecond)
	}
	return nil, fmt.Errorf("max retries exceeded")
}

// ============================================================================
// 8. IDEMPOTENCY - Safe retry of operations
// ============================================================================

/*
Idempotency: Performing the same operation multiple times has the same effect as doing it once.
Critical for: POST requests, payment processing, order creation.
*/

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
)

// Idempotency Key Pattern (most common)
type IdempotencyService struct {
	store map[string]*IdempotencyRecord // Use Redis/DB in production
	mu    sync.RWMutex
}

type IdempotencyRecord struct {
	Response   []byte
	StatusCode int
	CreatedAt  time.Time
}

func NewIdempotencyService() *IdempotencyService {
	return &IdempotencyService{
		store: make(map[string]*IdempotencyRecord),
	}
}

func (is *IdempotencyService) ProcessRequest(
	idempotencyKey string,
	operation func() ([]byte, int, error),
	ttl time.Duration,
) ([]byte, int, error) {
	
	// Check if we've seen this key before
	is.mu.RLock()
	record, exists := is.store[idempotencyKey]
	is.mu.RUnlock()
	
	if exists {
		// Check if record is expired
		if time.Since(record.CreatedAt) > ttl {
			// Expired, remove and continue
			is.mu.Lock()
			delete(is.store, idempotencyKey)
			is.mu.Unlock()
		} else {
			// Return cached response
			return record.Response, record.StatusCode, nil
		}
	}
	
	// Execute operation
	response, statusCode, err := operation()
	
	// Store result for future idempotent calls (only on success)
	if err == nil && statusCode < 400 {
		is.mu.Lock()
		is.store[idempotencyKey] = &IdempotencyRecord{
			Response:   response,
			StatusCode: statusCode,
			CreatedAt:  time.Now(),
		}
		is.mu.Unlock()
	}
	
	return response, statusCode, err
}

// Deterministic ID Generation for idempotency
func GenerateIdempotencyKey(operation string, params map[string]string) string {
	// Create deterministic hash of operation and parameters
	h := sha256.New()
	h.Write([]byte(operation))
	
	// Sort keys for consistency (important!)
	keys := make([]string, 0, len(params))
	for k := range params {
		keys = append(keys, k)
	}
	// sort.Strings(keys) // Uncomment for production
	
	for _, k := range keys {
		h.Write([]byte(k))
		h.Write([]byte(params[k]))
	}
	
	return hex.EncodeToString(h.Sum(nil))
}

// Idempotent HTTP Handler
func IdempotentHandler(w http.ResponseWriter, r *http.Request) {
	// Client should send X-Idempotency-Key header
	idempotencyKey := r.Header.Get("X-Idempotency-Key")
	if idempotencyKey == "" {
		http.Error(w, "Idempotency key required", http.StatusBadRequest)
		return
	}
	
	// Check Redis/database for existing response
	// If found, return cached response
	// If not, process and store result
	
	// Example flow:
	// 1. Start transaction
	// 2. Check idempotency key in database
	// 3. If exists and not expired, return stored response
	// 4. If not exists, process request
	// 5. Store response with idempotency key
	// 6. Commit transaction
}

// Idempotent Database Operations
type OrderServiceWithIdempotency struct {
	db *sql.DB // Assume sql.DB for example
}

func (os *OrderServiceWithIdempotency) CreateOrder(
	ctx context.Context, 
	userID string, 
	items []string, 
	idempotencyKey string,
) (*Order, error) {
	
	// Using database transaction with unique constraint
	tx, err := os.db.BeginTx(ctx, nil)
	if err != nil {
		return nil, err
	}
	defer tx.Rollback()
	
	// Check if order with this idempotency key already exists
	var existingOrderID string
	err = tx.QueryRowContext(ctx,
		"SELECT order_id FROM idempotency_keys WHERE key = $1",
		idempotencyKey,
	).Scan(&existingOrderID)
	
	if err == nil {
		// Key exists, fetch and return existing order
		return os.getOrder(ctx, existingOrderID)
	}
	
	// Create new order
	orderID := generateOrderID()
	_, err = tx.ExecContext(ctx,
		"INSERT INTO orders (id, user_id, status) VALUES ($1, $2, 'pending')",
		orderID, userID,
	)
	if err != nil {
		return nil, err
	}
	
	// Store idempotency key mapping
	_, err = tx.ExecContext(ctx,
		"INSERT INTO idempotency_keys (key, order_id) VALUES ($1, $2)",
		idempotencyKey, orderID,
	)
	if err != nil {
		return nil, err
	}
	
	if err := tx.Commit(); err != nil {
		return nil, err
	}
	
	return os.getOrder(ctx, orderID)
}

// ============================================================================
// PRACTICAL INTEGRATION EXAMPLE
// ============================================================================

type ResilientServiceClient struct {
	serviceURL     string
	circuitBreaker *CircuitBreakerDemo
	retryStrategy  *RetryStrategy
	rateLimiter    *RateLimiter
}

func NewResilientServiceClient(url string) *ResilientServiceClient {
	return &ResilientServiceClient{
		serviceURL:     url,
		circuitBreaker: NewCircuitBreaker("external-api"),
		retryStrategy:  NewRetryStrategy(3, 100*time.Millisecond, 5*time.Second),
		rateLimiter:    NewRateLimiter(10, 5), // 10 req/sec, burst 5
	}
}

func (c *ResilientServiceClient) CallAPI(ctx context.Context, request interface{}) (interface{}, error) {
	// 1. Check rate limit
	if !c.rateLimiter.Allow(c.serviceURL) {
		return nil, fmt.Errorf("rate limit exceeded")
	}
	
	// 2. Use circuit breaker
	result, err := c.circuitBreaker.Execute(func() (interface{}, error) {
		var finalResult interface{}
		var finalErr error
		
		// 3. Implement retries with backoff
		for retry := 0; retry <= c.retryStrategy.MaxRetries; retry++ {
			if retry > 0 {
				delay := c.retryStrategy.ExponentialBackoff(retry - 1)
				select {
				case <-time.After(delay):
				case <-ctx.Done():
					return nil, ctx.Err()
				}
			}
			
			// Make the actual API call
			finalResult, finalErr = c.makeAPICall(ctx, request)
			
			// Check if error is retryable
			if finalErr == nil || !c.isRetryableError(finalErr) {
				break
			}
			
			log.Printf("Attempt %d failed: %v", retry+1, finalErr)
		}
		
		return finalResult, finalErr
	})
	
	return result, err
}

func (c *ResilientServiceClient) makeAPICall(ctx context.Context, request interface{}) (interface{}, error) {
	// Actual HTTP/gRPC call implementation
	// Include timeout context, tracing headers, etc.
	return nil, nil
}

func (c *ResilientServiceClient) isRetryableError(err error) bool {
	// Determine if error is transient (network, timeout, 5xx)
	// vs permanent (4xx, validation errors)
	return true // Simplified for example
}

// ============================================================================
// MAIN FUNCTION - DEMONSTRATION
// ============================================================================

func main() {
	fmt.Println("=== Microservices & Distributed Systems Patterns in Go ===")
	
	// Service Boundaries
	sb := &ServiceBoundaries{}
	sb.Demonstrate()
	
	// Rate Limiting
	rl := NewRateLimiter(10, 5) // 10 req/sec, burst 5
	fmt.Printf("Rate limit allowed: %v\n", rl.Allow("client1"))
	
	// Circuit Breaker
	cb := NewCircuitBreaker("demo-service")
	result, err := cb.Execute(ExternalAPICall)
	fmt.Printf("Circuit breaker result: %v, error: %v\n", result, err)
	
	// Retry Strategy
	rs := NewRetryStrategy(3, 100*time.Millisecond, 5*time.Second)
	fmt.Printf("Retry delay for attempt 2: %v\n", rs.ExponentialBackoff(2))
	
	// Idempotency
	is := NewIdempotencyService()
	key := GenerateIdempotencyKey("create_order", map[string]string{
		"user_id": "123",
		"amount":  "99.99",
	})
	fmt.Printf("Generated idempotency key: %s\n", key[:16])
	
	// Resilient Client
	client := NewResilientServiceClient("https://api.example.com")
	ctx := context.Background()
	_, _ = client.CallAPI(ctx, "test request")
	
	fmt.Println("\n=== Key Takeaways ===")
	fmt.Println("1. Define clear service boundaries around business capabilities")
	fmt.Println("2. Use gRPC/Protobuf for efficient service communication")
	fmt.Println("3. Implement service discovery for dynamic environments")
	fmt.Println("4. Always use rate limiting to protect your services")
	fmt.Println("5. Circuit breakers prevent cascade failures")
	fmt.Println("6. Implement retries with exponential backoff and jitter")
	fmt.Println("7. Design idempotent APIs for safe retries")
	fmt.Println("8. Combine patterns for resilient distributed systems")
}

// Additional notes for production:
// - Use structured logging (zap, logrus)
// - Implement comprehensive metrics and tracing (OpenTelemetry)
// - Use context for cancellation and deadlines
// - Implement health checks and readiness probes
// - Consider message queues for async communication
// - Use feature flags for gradual rollouts
// - Implement proper security (mTLS, JWT validation)
// - Follow 12-factor app principles

// Remember: Distributed systems are hard. Start simple, add complexity only when needed.
// Test failure modes extensively (chaos engineering).