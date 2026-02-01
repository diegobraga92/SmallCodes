/*
CONTEXT-DRIVEN BACKEND DESIGN COMPREHENSIVE GUIDE
This file demonstrates context patterns for building robust backend services.
*/

package context_design

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"testing"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/trace"
	"gorm.io/gorm"
)

// ============================================================================
// 1. REQUEST-SCOPED CONTEXT FOUNDATIONS
// ============================================================================

// Custom context keys for type safety
type contextKey string

const (
	// Core request identifiers
	requestIDKey     contextKey = "request_id"
	correlationIDKey contextKey = "correlation_id"

	// Authentication & authorization
	userKey        contextKey = "user"
	rolesKey       contextKey = "roles"
	permissionsKey contextKey = "permissions"

	// Request metadata
	clientIPKey  contextKey = "client_ip"
	userAgentKey contextKey = "user_agent"

	// Business context
	tenantIDKey     contextKey = "tenant_id"
	organizationKey contextKey = "organization"

	// Performance tracking
	requestStartKey contextKey = "request_start_time"

	// Tracing
	traceIDKey contextKey = "trace_id"
	spanIDKey  contextKey = "span_id"
)

// RequestScope holds all request-scoped data
type RequestScope struct {
	RequestID      string
	CorrelationID  string
	User           *User
	ClientIP       string
	UserAgent      string
	TenantID       string
	OrganizationID string
	RequestStart   time.Time
	TraceID        string
	SpanID         string
	CustomData     map[string]interface{}
}

// User represents an authenticated user
type User struct {
	ID           string
	Email        string
	Roles        []string
	Permissions  []string
	TenantID     string
	SessionToken string
}

// ============================================================================
// 2. CONTEXT CREATION & PROPAGATION
// ============================================================================

// Middleware to create request context
func RequestContextMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Create base context with timeout
		ctx, cancel := context.WithTimeout(r.Context(), 30*time.Second)
		defer cancel()

		// Generate request identifiers
		requestID := generateRequestID()
		correlationID := r.Header.Get("X-Correlation-ID")
		if correlationID == "" {
			correlationID = generateCorrelationID()
		}

		// Extract request metadata
		clientIP := r.RemoteAddr
		if forwarded := r.Header.Get("X-Forwarded-For"); forwarded != "" {
			clientIP = forwarded
		}

		userAgent := r.Header.Get("User-Agent")

		// Inject values into context
		ctx = context.WithValue(ctx, requestIDKey, requestID)
		ctx = context.WithValue(ctx, correlationIDKey, correlationID)
		ctx = context.WithValue(ctx, clientIPKey, clientIP)
		ctx = context.WithValue(ctx, userAgentKey, userAgent)
		ctx = context.WithValue(ctx, requestStartKey, time.Now())

		// Add to response headers for client correlation
		w.Header().Set("X-Request-ID", requestID)
		w.Header().Set("X-Correlation-ID", correlationID)

		// Create structured scope for logging/monitoring
		scope := &RequestScope{
			RequestID:     requestID,
			CorrelationID: correlationID,
			ClientIP:      clientIP,
			UserAgent:     userAgent,
			RequestStart:  time.Now(),
			CustomData:    make(map[string]interface{}),
		}
		ctx = context.WithValue(ctx, contextKey("request_scope"), scope)

		// Log request start with context
		log.Printf("[%s] %s %s - Request started",
			requestID, r.Method, r.URL.Path)

		// Pass context to next handler
		next.ServeHTTP(w, r.WithContext(ctx))

		// Log request completion
		duration := time.Since(scope.RequestStart)
		log.Printf("[%s] Request completed in %v", requestID, duration)
	})
}

// Authentication middleware
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		// Extract token from header
		token := r.Header.Get("Authorization")
		if token == "" {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}

		// Validate token and get user info
		user, err := validateToken(ctx, token)
		if err != nil {
			logContextError(ctx, "Token validation failed", err)
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}

		// Inject user into context
		ctx = context.WithValue(ctx, userKey, user)
		ctx = context.WithValue(ctx, rolesKey, user.Roles)
		ctx = context.WithValue(ctx, permissionsKey, user.Permissions)
		ctx = context.WithValue(ctx, tenantIDKey, user.TenantID)

		// Update scope if exists
		if scope, ok := ctx.Value(contextKey("request_scope")).(*RequestScope); ok {
			scope.User = user
			scope.TenantID = user.TenantID
		}

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Business context middleware (multi-tenancy)
func TenantMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		// Extract tenant from subdomain, header, or JWT claim
		tenantID := extractTenantID(r)
		if tenantID == "" {
			// Try to get from authenticated user
			if user, ok := ctx.Value(userKey).(*User); ok {
				tenantID = user.TenantID
			}
		}

		if tenantID != "" {
			ctx = context.WithValue(ctx, tenantIDKey, tenantID)

			// Update scope
			if scope, ok := ctx.Value(contextKey("request_scope")).(*RequestScope); ok {
				scope.TenantID = tenantID
			}
		}

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// ============================================================================
// 3. CONTEXT UTILITIES & HELPER FUNCTIONS
// ============================================================================

// Getter functions with type safety
func GetRequestID(ctx context.Context) string {
	if id, ok := ctx.Value(requestIDKey).(string); ok {
		return id
	}
	return "unknown"
}

func GetCorrelationID(ctx context.Context) string {
	if id, ok := ctx.Value(correlationIDKey).(string); ok {
		return id
	}
	return ""
}

func GetUser(ctx context.Context) *User {
	if user, ok := ctx.Value(userKey).(*User); ok {
		return user
	}
	return nil
}

func GetUserID(ctx context.Context) string {
	if user := GetUser(ctx); user != nil {
		return user.ID
	}
	return ""
}

func GetTenantID(ctx context.Context) string {
	if id, ok := ctx.Value(tenantIDKey).(string); ok {
		return id
	}
	// Fallback to user tenant
	if user := GetUser(ctx); user != nil {
		return user.TenantID
	}
	return ""
}

func GetRequestScope(ctx context.Context) *RequestScope {
	if scope, ok := ctx.Value(contextKey("request_scope")).(*RequestScope); ok {
		return scope
	}
	return nil
}

// Context-aware logging
func logWithContext(ctx context.Context, format string, args ...interface{}) {
	requestID := GetRequestID(ctx)
	msg := fmt.Sprintf(format, args...)
	log.Printf("[%s] %s", requestID, msg)
}

func logContextError(ctx context.Context, msg string, err error) {
	requestID := GetRequestID(ctx)
	log.Printf("[%s] ERROR: %s: %v", requestID, msg, err)
}

// Context-aware metrics
type MetricsCollector struct{}

func (m *MetricsCollector) RecordDuration(ctx context.Context, operation string, duration time.Duration) {
	tenantID := GetTenantID(ctx)
	// Record to metrics system with tenant context
	log.Printf("[%s] %s took %v for tenant %s",
		GetRequestID(ctx), operation, duration, tenantID)
}

// ============================================================================
// 4. DEADLINES & CANCELLATIONS IN PRACTICE
// ============================================================================

// Service with proper deadline propagation
type OrderService struct {
	db       *gorm.DB
	cache    *RedisClient
	payment  *PaymentService
	shipping *ShippingService
}

func (s *OrderService) CreateOrder(ctx context.Context, order *Order) (*Order, error) {
	// Check if context is still valid
	if err := ctx.Err(); err != nil {
		return nil, fmt.Errorf("context cancelled before processing: %w", err)
	}

	// Set operation-specific timeout (shorter than parent context)
	opCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	// Start transaction with context
	tx := s.db.WithContext(opCtx).Begin()
	if tx.Error != nil {
		return nil, tx.Error
	}

	// Process with context propagation
	order, err := s.processOrder(opCtx, tx, order)
	if err != nil {
		tx.Rollback()
		return nil, err
	}

	// Commit transaction
	if err := tx.Commit().Error; err != nil {
		return nil, err
	}

	return order, nil
}

func (s *OrderService) processOrder(ctx context.Context, tx *gorm.DB, order *Order) (*Order, error) {
	// Check deadline
	if deadline, ok := ctx.Deadline(); ok {
		logWithContext(ctx, "Must complete by %v", deadline)
	}

	// 1. Validate order with context
	if err := s.validateOrder(ctx, order); err != nil {
		return nil, err
	}

	// 2. Process payment with timeout
	paymentCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()

	if err := s.payment.Process(paymentCtx, order); err != nil {
		return nil, fmt.Errorf("payment failed: %w", err)
	}

	// 3. Reserve inventory
	if err := s.reserveInventory(ctx, order); err != nil {
		return nil, fmt.Errorf("inventory reservation failed: %w", err)
	}

	// 4. Create shipping label with cancellation
	shippingCtx, cancel := context.WithCancel(ctx)
	defer cancel()

	// Setup cancellation on error
	go func() {
		if <-ctx.Done(); ctx.Err() == context.Canceled {
			logWithContext(ctx, "Shipping processing cancelled")
		}
	}()

	if err := s.shipping.CreateLabel(shippingCtx, order); err != nil {
		return nil, fmt.Errorf("shipping failed: %w", err)
	}

	// 5. Save order to database
	if err := tx.Create(order).Error; err != nil {
		return nil, err
	}

	return order, nil
}

// Database operations with context
type UserRepository struct {
	db *gorm.DB
}

func (r *UserRepository) GetUserByID(ctx context.Context, id string) (*User, error) {
	// Use context for query cancellation
	var user User
	result := r.db.WithContext(ctx).Where("id = ?", id).First(&user)

	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			return nil, fmt.Errorf("user not found: %w", result.Error)
		}
		return nil, result.Error
	}

	return &user, nil
}

func (r *UserRepository) ListUsers(ctx context.Context, filter UserFilter) ([]User, error) {
	// Apply tenant isolation from context
	tenantID := GetTenantID(ctx)
	if tenantID == "" {
		return nil, errors.New("tenant context required")
	}

	query := r.db.WithContext(ctx).Where("tenant_id = ?", tenantID)

	// Apply filters
	if filter.Email != "" {
		query = query.Where("email LIKE ?", "%"+filter.Email+"%")
	}

	if filter.Role != "" {
		query = query.Where("role = ?", filter.Role)
	}

	// Set timeout for complex queries
	if filter.Limit > 100 {
		ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
		defer cancel()
		query = query.WithContext(ctx)
	}

	var users []User
	if err := query.Limit(filter.Limit).Offset(filter.Offset).Find(&users).Error; err != nil {
		return nil, err
	}

	return users, nil
}

// ============================================================================
// 5. GRACEFUL SHUTDOWN PATTERNS
// ============================================================================

func GracefulShutdownExample() {
	// Create main context for shutdown signal
	ctx, stop := signal.NotifyContext(context.Background(),
		os.Interrupt, syscall.SIGTERM, syscall.SIGQUIT)
	defer stop()

	// Initialize services
	server := &HTTPServer{}
	db := &Database{}
	cache := &RedisClient{}

	// Start services
	var wg sync.WaitGroup

	// HTTP Server
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.Start(ctx)
	}()

	// Background workers
	wg.Add(1)
	go func() {
		defer wg.Done()
		startBackgroundWorkers(ctx)
	}()

	// Wait for shutdown signal
	<-ctx.Done()
	log.Println("Shutdown signal received, initiating graceful shutdown...")

	// Give services time to complete
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	// Shutdown services in dependency order
	log.Println("Stopping HTTP server...")
	if err := server.Stop(shutdownCtx); err != nil {
		log.Printf("HTTP server shutdown error: %v", err)
	}

	log.Println("Closing database connections...")
	if err := db.Close(shutdownCtx); err != nil {
		log.Printf("Database shutdown error: %v", err)
	}

	log.Println("Closing cache connections...")
	if err := cache.Close(shutdownCtx); err != nil {
		log.Printf("Cache shutdown error: %v", err)
	}

	// Wait for all goroutines
	wg.Wait()
	log.Println("Graceful shutdown completed")
}

func startBackgroundWorkers(ctx context.Context) {
	// Worker pool with context
	workerCount := 5
	var wg sync.WaitGroup

	for i := 0; i < workerCount; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			worker(ctx, workerID)
		}(i)
	}

	wg.Wait()
}

func worker(ctx context.Context, id int) {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// Do periodic work
			log.Printf("Worker %d: doing work", id)
			doWork(ctx)

		case <-ctx.Done():
			log.Printf("Worker %d: stopping due to shutdown", id)
			// Cleanup work
			cleanupWork(id)
			return
		}
	}
}

// ============================================================================
// 6. DISTRIBUTED TRACING WITH CONTEXT
// ============================================================================

// Tracing middleware
func TracingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		// Extract or create trace
		tracer := otel.Tracer("api")
		ctx, span := tracer.Start(ctx, r.URL.Path)
		defer span.End()

		// Inject trace IDs into context
		spanContext := span.SpanContext()
		ctx = context.WithValue(ctx, traceIDKey, spanContext.TraceID().String())
		ctx = context.WithValue(ctx, spanIDKey, spanContext.SpanID().String())

		// Update request scope
		if scope, ok := ctx.Value(contextKey("request_scope")).(*RequestScope); ok {
			scope.TraceID = spanContext.TraceID().String()
			scope.SpanID = spanContext.SpanID().String()
		}

		// Add trace headers to response
		w.Header().Set("X-Trace-ID", spanContext.TraceID().String())

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Database tracing wrapper
type TracedDB struct {
	db     *gorm.DB
	tracer trace.Tracer
}

func (t *TracedDB) QueryWithTrace(ctx context.Context, query string, args ...interface{}) ([]map[string]interface{}, error) {
	ctx, span := t.tracer.Start(ctx, "database.query")
	defer span.End()

	// Add query to span
	span.SetAttributes(
		trace.StringAttribute("db.query", query),
		trace.StringAttribute("db.system", "postgres"),
	)

	// Execute query with context
	rows, err := t.db.WithContext(ctx).Raw(query, args...).Rows()
	if err != nil {
		span.RecordError(err)
		return nil, err
	}
	defer rows.Close()

	// Process results
	var results []map[string]interface{}
	columns, _ := rows.Columns()

	for rows.Next() {
		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))
		for i := range columns {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			span.RecordError(err)
			return nil, err
		}

		result := make(map[string]interface{})
		for i, col := range columns {
			val := values[i]
			if b, ok := val.([]byte); ok {
				result[col] = string(b)
			} else {
				result[col] = val
			}
		}
		results = append(results, result)
	}

	span.SetAttributes(trace.IntAttribute("db.result_count", len(results)))
	return results, nil
}

// ============================================================================
// 7. ASYNC OPERATIONS WITH CONTEXT PROPAGATION
// ============================================================================

// Async job processor with context inheritance
type AsyncJobProcessor struct {
	queue    chan Job
	workers  int
	shutdown chan struct{}
}

type Job struct {
	ID        string
	Type      string
	Payload   []byte
	Context   map[string]string // For propagating context values
	CreatedAt time.Time
}

func (p *AsyncJobProcessor) Start(parentCtx context.Context) {
	for i := 0; i < p.workers; i++ {
		go p.worker(parentCtx, i)
	}
}

func (p *AsyncJobProcessor) worker(parentCtx context.Context, id int) {
	log.Printf("Worker %d started", id)

	for {
		select {
		case job := <-p.queue:
			// Restore context from job
			ctx := restoreContext(parentCtx, job.Context)

			// Process job with restored context
			if err := p.processJob(ctx, job); err != nil {
				logContextError(ctx, "Job processing failed", err)
			}

		case <-parentCtx.Done():
			log.Printf("Worker %d stopping", id)
			return

		case <-p.shutdown:
			log.Printf("Worker %d shutting down", id)
			return
		}
	}
}

func (p *AsyncJobProcessor) processJob(ctx context.Context, job Job) error {
	// Recreate request scope from job context
	scope := &RequestScope{
		RequestID:    job.ID,
		RequestStart: time.Now(),
		CustomData:   make(map[string]interface{}),
	}

	// Restore trace if available
	if traceID, ok := job.Context["trace_id"]; ok {
		scope.TraceID = traceID
	}

	ctx = context.WithValue(ctx, contextKey("request_scope"), scope)

	// Process based on job type
	switch job.Type {
	case "email":
		return p.sendEmail(ctx, job)
	case "report":
		return p.generateReport(ctx, job)
	default:
		return fmt.Errorf("unknown job type: %s", job.Type)
	}
}

func restoreContext(parent context.Context, values map[string]string) context.Context {
	ctx := parent

	// Restore important context values
	if requestID, ok := values["request_id"]; ok {
		ctx = context.WithValue(ctx, requestIDKey, requestID)
	}

	if correlationID, ok := values["correlation_id"]; ok {
		ctx = context.WithValue(ctx, correlationIDKey, correlationID)
	}

	if traceID, ok := values["trace_id"]; ok {
		ctx = context.WithValue(ctx, traceIDKey, traceID)
	}

	return ctx
}

// ============================================================================
// 8. CONTEXT IN MICROSERVICES COMMUNICATION
// ============================================================================

// HTTP client with context propagation
type ContextAwareHTTPClient struct {
	client *http.Client
}

func (c *ContextAwareHTTPClient) Do(ctx context.Context, req *http.Request) (*http.Response, error) {
	// Propagate context headers
	req.Header.Set("X-Request-ID", GetRequestID(ctx))
	req.Header.Set("X-Correlation-ID", GetCorrelationID(ctx))

	// Propagate trace headers
	if traceID, ok := ctx.Value(traceIDKey).(string); ok {
		req.Header.Set("X-Trace-ID", traceID)
	}

	// Propagate tenant context
	if tenantID := GetTenantID(ctx); tenantID != "" {
		req.Header.Set("X-Tenant-ID", tenantID)
	}

	// Add authorization if available
	if user := GetUser(ctx); user != nil {
		req.Header.Set("Authorization", "Bearer "+user.SessionToken)
	}

	// Execute request with timeout from context
	if deadline, ok := ctx.Deadline(); ok {
		timeout := time.Until(deadline)
		client := *c.client
		client.Timeout = timeout
		return client.Do(req)
	}

	return c.client.Do(req)
}

// GRPC interceptor for context propagation
func ContextPropagationInterceptor(ctx context.Context, method string, req, reply interface{},
	cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {

	// Extract metadata from context
	md := metadata.New(map[string]string{
		"x-request-id":     GetRequestID(ctx),
		"x-correlation-id": GetCorrelationID(ctx),
		"x-tenant-id":      GetTenantID(ctx),
	})

	// Add trace if available
	if traceID, ok := ctx.Value(traceIDKey).(string); ok {
		md.Set("x-trace-id", traceID)
	}

	// Add auth token if available
	if user := GetUser(ctx); user != nil {
		md.Set("authorization", "Bearer "+user.SessionToken)
	}

	// Create new context with metadata
	ctx = metadata.NewOutgoingContext(ctx, md)

	// Call with propagated context
	return invoker(ctx, method, req, reply, cc, opts...)
}

// ============================================================================
// 9. CACHE WITH CONTEXT-AWARE INVALIDATION
// ============================================================================

type ContextAwareCache struct {
	store        map[string]cacheEntry
	mu           sync.RWMutex
	tenantScoped bool
}

type cacheEntry struct {
	value     interface{}
	expiresAt time.Time
	tenantID  string
	userID    string
}

func (c *ContextAwareCache) Get(ctx context.Context, key string) (interface{}, bool) {
	c.mu.RLock()
	entry, found := c.store[key]
	c.mu.RUnlock()

	if !found {
		return nil, false
	}

	// Check expiration
	if time.Now().After(entry.expiresAt) {
		c.mu.Lock()
		delete(c.store, key)
		c.mu.Unlock()
		return nil, false
	}

	// Tenant isolation check
	if c.tenantScoped {
		tenantID := GetTenantID(ctx)
		if entry.tenantID != tenantID {
			return nil, false
		}
	}

	return entry.value, true
}

func (c *ContextAwareCache) Set(ctx context.Context, key string, value interface{}, ttl time.Duration) {
	entry := cacheEntry{
		value:     value,
		expiresAt: time.Now().Add(ttl),
	}

	// Add context metadata if tenant-scoped
	if c.tenantScoped {
		entry.tenantID = GetTenantID(ctx)
		entry.userID = GetUserID(ctx)
	}

	c.mu.Lock()
	c.store[key] = entry
	c.mu.Unlock()
}

func (c *ContextAwareCache) InvalidateByTenant(ctx context.Context, tenantID string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	for key, entry := range c.store {
		if entry.tenantID == tenantID {
			delete(c.store, key)
		}
	}
}

// ============================================================================
// 10. CONTEXT MISUSE PATTERNS TO AVOID
// ============================================================================

// MISUSE 1: Storing context in structs
type BadService struct {
	ctx context.Context // WRONG: Context shouldn't be stored
}

// CORRECT: Pass context as parameter
type GoodService struct {
	// No context stored
}

func (s *GoodService) Process(ctx context.Context, data interface{}) error {
	// Use ctx parameter
	return nil
}

// MISUSE 2: Using background context everywhere
func BadBackgroundContextUsage() {
	// WRONG: Using background context for user requests
	ctx := context.Background()

	// This loses all request context!
	processUserRequest(ctx)
}

// CORRECT: Pass request context through call chain
func HandleRequest(ctx context.Context, req *http.Request) error {
	return processUserRequest(ctx) // Preserve request context
}

// MISUSE 3: Ignoring context cancellation
func BadIgnoreCancellation(ctx context.Context) error {
	// WRONG: Not checking context
	result := make(chan error, 1)

	go func() {
		// Long operation that won't be cancelled
		time.Sleep(10 * time.Second)
		result <- nil
	}()

	select {
	case err := <-result:
		return err
		// MISSING: case <-ctx.Done():
		//     return ctx.Err()
	}
}

// CORRECT: Respect context cancellation
func GoodWithCancellation(ctx context.Context) error {
	result := make(chan error, 1)

	go func() {
		select {
		case <-time.After(10 * time.Second):
			result <- nil
		case <-ctx.Done():
			result <- ctx.Err()
		}
	}()

	return <-result
}

// MISUSE 4: Creating context without timeout
func BadNoTimeout(db *Database) error {
	// WRONG: No timeout - could hang forever
	ctx := context.Background()
	return db.Query(ctx, "SELECT * FROM large_table")
}

// CORRECT: Always use timeouts
func GoodWithTimeout(db *Database) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	return db.Query(ctx, "SELECT * FROM large_table")
}

// MISUSE 5: Context value abuse
func BadContextValueAbuse(ctx context.Context) {
	// WRONG: Using context as data bag for everything
	ctx = context.WithValue(ctx, "large_data", []byte{})  // Large data in context
	ctx = context.WithValue(ctx, "connection", &DBConn{}) // Resources in context
}

// CORRECT: Only store request-scoped metadata
func GoodContextValues(ctx context.Context) {
	// Store only metadata
	ctx = context.WithValue(ctx, requestIDKey, "req-123")
	ctx = context.WithValue(ctx, tenantIDKey, "tenant-456")
}

// ============================================================================
// 11. TESTING CONTEXT-DRIVEN CODE
// ============================================================================

// Test utilities
func TestRequestContext() context.Context {
	ctx := context.Background()

	// Add test values
	ctx = context.WithValue(ctx, requestIDKey, "test-request-123")
	ctx = context.WithValue(ctx, correlationIDKey, "test-correlation-456")
	ctx = context.WithValue(ctx, tenantIDKey, "test-tenant")

	// Create test user
	user := &User{
		ID:       "test-user",
		Email:    "test@example.com",
		TenantID: "test-tenant",
		Roles:    []string{"admin"},
	}
	ctx = context.WithValue(ctx, userKey, user)

	// Add scope
	scope := &RequestScope{
		RequestID:     "test-request-123",
		CorrelationID: "test-correlation-456",
		TenantID:      "test-tenant",
		RequestStart:  time.Now(),
	}
	ctx = context.WithValue(ctx, contextKey("request_scope"), scope)

	return ctx
}

func TestWithTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(TestRequestContext(), 1*time.Second)
	defer cancel()

	// Test service with timeout
	svc := &OrderService{}
	_, err := svc.CreateOrder(ctx, &Order{})

	if err != nil && !errors.Is(err, context.DeadlineExceeded) {
		t.Errorf("Expected deadline exceeded, got %v", err)
	}
}

// Mock context for testing
type MockContext struct {
	context.Context
	values map[interface{}]interface{}
	err    error
}

func (m *MockContext) Value(key interface{}) interface{} {
	return m.values[key]
}

func (m *MockContext) Err() error {
	return m.err
}

func (m *MockContext) Done() <-chan struct{} {
	ch := make(chan struct{})
	close(ch)
	return ch
}

func (m *MockContext) Deadline() (time.Time, bool) {
	return time.Time{}, false
}

// ============================================================================
// 12. MONITORING & OBSERVABILITY WITH CONTEXT
// ============================================================================

// Structured logger with context
type ContextLogger struct{}

func (l *ContextLogger) Info(ctx context.Context, msg string, fields ...interface{}) {
	scope := GetRequestScope(ctx)
	logEntry := map[string]interface{}{
		"timestamp":      time.Now().UTC(),
		"level":          "INFO",
		"message":        msg,
		"request_id":     scope.RequestID,
		"correlation_id": scope.CorrelationID,
		"tenant_id":      scope.TenantID,
		"user_id":        GetUserID(ctx),
		"trace_id":       scope.TraceID,
	}

	// Add custom fields
	for i := 0; i < len(fields); i += 2 {
		if i+1 < len(fields) {
			key, ok := fields[i].(string)
			if ok {
				logEntry[key] = fields[i+1]
			}
		}
	}

	// Log as JSON for structured logging
	log.Printf("%+v", logEntry)
}

func (l *ContextLogger) Error(ctx context.Context, err error, msg string, fields ...interface{}) {
	scope := GetRequestScope(ctx)
	logEntry := map[string]interface{}{
		"timestamp":      time.Now().UTC(),
		"level":          "ERROR",
		"message":        msg,
		"error":          err.Error(),
		"request_id":     scope.RequestID,
		"correlation_id": scope.CorrelationID,
		"tenant_id":      scope.TenantID,
		"trace_id":       scope.TraceID,
	}

	log.Printf("%+v", logEntry)
}

// Metrics with context labels
type ContextMetrics struct {
	registry *MetricsRegistry
}

func (m *ContextMetrics) RecordHTTPRequest(ctx context.Context, method, path string, status int, duration time.Duration) {
	labels := map[string]string{
		"method":     method,
		"path":       path,
		"status":     fmt.Sprintf("%d", status),
		"tenant":     GetTenantID(ctx),
		"request_id": GetRequestID(ctx),
	}

	m.registry.RecordHistogram("http_requests_duration_seconds", duration.Seconds(), labels)
	m.registry.IncrementCounter("http_requests_total", labels)
}

// ============================================================================
// 13. SECURITY CONSIDERATIONS
// ============================================================================

// Context-based authorization
type RBACAuthorizer struct{}

func (a *RBACAuthorizer) Authorize(ctx context.Context, resource, action string) error {
	user := GetUser(ctx)
	if user == nil {
		return errors.New("user not authenticated")
	}

	// Check permissions in context
	permissions, _ := ctx.Value(permissionsKey).([]string)

	// Build permission string (e.g., "orders:read")
	requiredPermission := fmt.Sprintf("%s:%s", resource, action)

	for _, perm := range permissions {
		if perm == requiredPermission {
			return nil
		}
	}

	return fmt.Errorf("user lacks permission: %s", requiredPermission)
}

// Tenant isolation enforcement
func EnforceTenantIsolation(ctx context.Context, query *gorm.DB) *gorm.DB {
	tenantID := GetTenantID(ctx)
	if tenantID == "" {
		// No tenant context - might be system operation
		return query
	}

	// Add tenant filter to query
	return query.Where("tenant_id = ?", tenantID)
}

// Audit logging with context
func AuditLog(ctx context.Context, action, resource, resourceID string, details interface{}) {
	userID := GetUserID(ctx)
	tenantID := GetTenantID(ctx)
	requestID := GetRequestID(ctx)

	auditEntry := AuditEntry{
		Timestamp:  time.Now().UTC(),
		Action:     action,
		Resource:   resource,
		ResourceID: resourceID,
		UserID:     userID,
		TenantID:   tenantID,
		RequestID:  requestID,
		Details:    details,
		IPAddress:  GetClientIP(ctx),
		UserAgent:  GetUserAgent(ctx),
	}

	// Save to audit log
	saveAuditEntry(ctx, auditEntry)
}

// ============================================================================
// 14. BEST PRACTICES SUMMARY
// ============================================================================

/*
1. Always pass context as first parameter in functions
2. Use custom types for context keys to avoid collisions
3. Store only request-scoped data in context (not application state)
4. Always check ctx.Err() before starting expensive operations
5. Propagate context through all layers (HTTP handlers, database, cache, etc.)
6. Use context timeouts for all external calls
7. Implement graceful shutdown using context cancellation
8. Never store context in structs - pass it explicitly
9. Use context for distributed tracing correlation
10. Implement tenant isolation using context values
11. Add context to logging for better debugging
12. Test context cancellation and timeout scenarios
13. Use context.WithValue sparingly - prefer explicit parameters
14. Create context at the entry point (HTTP handler, CLI command)
15. Cancel contexts as soon as they're no longer needed
16. Use context for request-based rate limiting
17. Implement context-aware caching with proper invalidation
18. Propagate authentication/authorization through context
19. Use context deadlines to prevent resource leaks
20. Monitor context cancellation patterns for system health
*/
