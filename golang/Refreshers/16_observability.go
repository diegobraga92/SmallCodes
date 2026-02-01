package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"runtime/debug"
	"time"

	// Importing packages for advanced observability
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/stdout/stdoutmetric"
	"go.opentelemetry.io/otel/metric"
	"go.opentelemetry.io/otel/metric/noop"
	"go.opentelemetry.io/otel/sdk/metric"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/trace"
)

// =============================================
// 1. ERROR WRAPPING STRATEGIES
// =============================================

// In Go 1.13+, errors can be wrapped with additional context
// using fmt.Errorf with %w verb

func ErrorWrappingExample() error {
	// Basic error wrapping
	err := errors.New("database connection failed")

	// Wrap with additional context
	wrappedErr := fmt.Errorf("failed to fetch user: %w", err)

	// Multiple layers of wrapping
	finalErr := fmt.Errorf("API request failed: %w", wrappedErr)

	// Check for specific error in chain
	if errors.Is(finalErr, err) {
		fmt.Println("Original error found in chain")
	}

	return finalErr
}

// =============================================
// 2. CUSTOM ERROR TYPES
// =============================================

// Define custom error types for domain-specific errors

// DomainError - Base custom error with additional context
type DomainError struct {
	Code    string
	Message string
	Op      string // Operation
	Err     error  // Underlying error
	Time    time.Time
}

// Implement error interface
func (e *DomainError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s [%s]: %s: %v", e.Op, e.Code, e.Message, e.Err)
	}
	return fmt.Sprintf("%s [%s]: %s", e.Op, e.Code, e.Message)
}

// Unwrap method for error wrapping compatibility
func (e *DomainError) Unwrap() error {
	return e.Err
}

// Business-specific error types
type ValidationError struct {
	Field  string
	Value  interface{}
	Reason string
}

func (e *ValidationError) Error() string {
	return fmt.Sprintf("validation failed for %s: %v - %s", e.Field, e.Value, e.Reason)
}

// Sentinel errors (errors that are expected and handled)
var (
	ErrUserNotFound = errors.New("user not found")
	ErrInvalidToken = errors.New("invalid token")
	ErrRateLimited  = errors.New("rate limited")
)

// =============================================
// 3. STACK TRACES
// =============================================

// ErrorWithStackTrace - Custom error with stack trace
type ErrorWithStackTrace struct {
	Message   string
	Timestamp time.Time
	Stack     []byte
	Cause     error
}

func NewErrorWithStackTrace(msg string, cause error) *ErrorWithStackTrace {
	return &ErrorWithStackTrace{
		Message:   msg,
		Timestamp: time.Now(),
		Stack:     debug.Stack(),
		Cause:     cause,
	}
}

func (e *ErrorWithStackTrace) Error() string {
	if e.Cause != nil {
		return fmt.Sprintf("%s: %v\nStack Trace:\n%s", e.Message, e.Cause, e.Stack)
	}
	return fmt.Sprintf("%s\nStack Trace:\n%s", e.Message, e.Stack)
}

func (e *ErrorWithStackTrace) Unwrap() error {
	return e.Cause
}

// =============================================
// 4. LOGGING BEST PRACTICES
// =============================================

// StructuredLogger - Custom logger for structured logging
type StructuredLogger struct {
	*log.Logger
	Service string
	Version string
}

func NewStructuredLogger(service, version string) *StructuredLogger {
	return &StructuredLogger{
		Logger:  log.New(os.Stdout, "", 0), // No prefix, we'll handle formatting
		Service: service,
		Version: version,
	}
}

// Log with context and structured fields
func (l *StructuredLogger) Log(level, message string, fields map[string]interface{}) {
	// Structured log entry
	entry := map[string]interface{}{
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"service":   l.Service,
		"version":   l.Version,
		"level":     level,
		"message":   message,
	}

	// Add custom fields
	for k, v := range fields {
		entry[k] = v
	}

	// Convert to JSON (in production, use proper JSON encoder)
	l.Printf("%+v", entry)
}

// Context-aware logging
func (l *StructuredLogger) LogWithContext(ctx context.Context, level, msg string, fields map[string]interface{}) {
	// Extract trace/span IDs from context (if using tracing)
	if span := trace.SpanFromContext(ctx); span != nil {
		if fields == nil {
			fields = make(map[string]interface{})
		}
		spanCtx := span.SpanContext()
		fields["trace_id"] = spanCtx.TraceID().String()
		fields["span_id"] = spanCtx.SpanID().String()
	}

	l.Log(level, msg, fields)
}

// =============================================
// 5. STRUCTURED LOGGING
// =============================================

// Structured logging ensures logs are machine-readable (usually JSON)

func StructuredLoggingExample() {
	logger := NewStructuredLogger("user-service", "1.0.0")

	// Different log levels with structured data
	logger.Log("INFO", "User login successful", map[string]interface{}{
		"user_id":    "12345",
		"ip_address": "192.168.1.1",
		"user_agent": "Mozilla/5.0",
	})

	logger.Log("ERROR", "Database query failed", map[string]interface{}{
		"operation": "get_user",
		"error":     "connection timeout",
		"duration":  2.5, // seconds
		"attempt":   3,
	})

	// Logging with error wrapping
	err := fmt.Errorf("failed to process: %w", errors.New("underlying issue"))
	logger.Log("WARN", "Processing issue", map[string]interface{}{
		"error": err.Error(),
	})
}

// =============================================
// 6. METRICS BASICS
// =============================================

// Metrics types: counters, gauges, histograms

type MetricsCollector struct {
	meter             metric.Meter
	requestCounter    metric.Int64Counter
	errorCounter      metric.Int64Counter
	responseHistogram metric.Int64Histogram
	activeConnections metric.Int64ObservableGauge
}

func NewMetricsCollector(meter metric.Meter) (*MetricsCollector, error) {
	// Counter - monotonically increasing value
	requestCounter, err := meter.Int64Counter(
		"http_requests_total",
		metric.WithDescription("Total HTTP requests"),
		metric.WithUnit("1"),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create request counter: %w", err)
	}

	// Histogram - for measuring distributions (latency, size, etc.)
	responseHistogram, err := meter.Int64Histogram(
		"http_response_duration_ms",
		metric.WithDescription("HTTP response duration in milliseconds"),
		metric.WithUnit("ms"),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create histogram: %w", err)
	}

	// Error counter with specific labels
	errorCounter, err := meter.Int64Counter(
		"errors_total",
		metric.WithDescription("Total errors by type"),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create error counter: %w", err)
	}

	return &MetricsCollector{
		meter:             meter,
		requestCounter:    requestCounter,
		errorCounter:      errorCounter,
		responseHistogram: responseHistogram,
	}, nil
}

func (m *MetricsCollector) RecordRequest(method, path string, statusCode int, duration time.Duration) {
	// Increment request counter with labels/attributes
	m.requestCounter.Add(context.Background(), 1,
		metric.WithAttributes(
			attribute.String("method", method),
			attribute.String("path", path),
			attribute.Int("status", statusCode),
		))

	// Record duration in histogram
	m.responseHistogram.Record(context.Background(), duration.Milliseconds(),
		metric.WithAttributes(
			attribute.String("method", method),
			attribute.String("path", path),
		))
}

func (m *MetricsCollector) RecordError(errType string) {
	m.errorCounter.Add(context.Background(), 1,
		metric.WithAttributes(attribute.String("type", errType)))
}

// =============================================
// 7. TRACING FUNDAMENTALS
// =============================================

// Tracing helps track requests across service boundaries

type TracingMiddleware struct {
	tracer trace.Tracer
}

func NewTracingMiddleware(serviceName string) *TracingMiddleware {
	// In production, use proper exporter (Jaeger, Zipkin, etc.)
	// For demo, using no-op tracer
	tracer := otel.Tracer(serviceName)

	return &TracingMiddleware{
		tracer: tracer,
	}
}

func (t *TracingMiddleware) HandleRequest(ctx context.Context, req *http.Request) (context.Context, trace.Span) {
	// Start a new span for the request
	ctx, span := t.tracer.Start(ctx, "HTTP "+req.Method,
		trace.WithAttributes(
			attribute.String("http.method", req.Method),
			attribute.String("http.url", req.URL.Path),
			attribute.String("http.user_agent", req.UserAgent()),
		))

	return ctx, span
}

// Span example for database operation
func (t *TracingMiddleware) DatabaseQuery(ctx context.Context, query string) (context.Context, trace.Span) {
	ctx, span := t.tracer.Start(ctx, "Database.Query",
		trace.WithAttributes(
			attribute.String("db.query", query),
			attribute.String("db.system", "postgresql"),
		))

	// Simulate work
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)

	return ctx, span
}

// =============================================
// 8. COMPREHENSIVE EXAMPLE
// =============================================

// UserService demonstrates error design and observability patterns
type UserService struct {
	logger  *StructuredLogger
	metrics *MetricsCollector
	tracer  *TracingMiddleware
}

func NewUserService() *UserService {
	logger := NewStructuredLogger("user-service", "1.0.0")

	// In production, use proper meter provider
	meter := noop.NewMeterProvider().Meter("user-service")
	metrics, _ := NewMetricsCollector(meter)

	tracer := NewTracingMiddleware("user-service")

	return &UserService{
		logger:  logger,
		metrics: metrics,
		tracer:  tracer,
	}
}

func (s *UserService) GetUser(ctx context.Context, userID string) (*User, error) {
	startTime := time.Now()

	// Start tracing span
	ctx, span := s.tracer.HandleRequest(ctx, &http.Request{
		Method: "GET",
		URL:    &url.URL{Path: "/users/" + userID},
	})
	defer span.End()

	// Record metrics
	defer func() {
		s.metrics.RecordRequest("GET", "/users/"+userID, 200, time.Since(startTime))
	}()

	// Log entry
	s.logger.LogWithContext(ctx, "INFO", "Fetching user", map[string]interface{}{
		"user_id": userID,
		"action":  "get_user",
	})

	// Simulate database operation with tracing
	_, dbSpan := s.tracer.DatabaseQuery(ctx, "SELECT * FROM users WHERE id = $1")
	defer dbSpan.End()

	// Simulate error scenario
	if userID == "0" {
		// Record error metric
		s.metrics.RecordError("user_not_found")

		// Log error with context
		s.logger.LogWithContext(ctx, "ERROR", "User not found", map[string]interface{}{
			"user_id": userID,
			"error":   ErrUserNotFound.Error(),
		})

		// Return custom error with wrapping
		return nil, &DomainError{
			Code:    "USER_NOT_FOUND",
			Message: "Requested user does not exist",
			Op:      "UserService.GetUser",
			Err:     ErrUserNotFound,
			Time:    time.Now(),
		}
	}

	// Simulate validation error
	if userID == "invalid" {
		dbSpan.RecordError(errors.New("invalid user format"))

		// Structured logging with error details
		validationErr := &ValidationError{
			Field:  "user_id",
			Value:  userID,
			Reason: "Invalid format",
		}

		s.logger.LogWithContext(ctx, "WARN", "Validation failed", map[string]interface{}{
			"error": validationErr.Error(),
			"field": "user_id",
		})

		// Return error with stack trace for debugging
		return nil, NewErrorWithStackTrace("validation failed", validationErr)
	}

	// Success case
	user := &User{
		ID:   userID,
		Name: "John Doe",
	}

	// Log success
	s.logger.LogWithContext(ctx, "INFO", "User fetched successfully", map[string]interface{}{
		"user_id": userID,
		"elapsed": time.Since(startTime).String(),
	})

	// Add attribute to span
	span.SetAttributes(attribute.String("user.name", user.Name))

	return user, nil
}

type User struct {
	ID   string
	Name string
}

// =============================================
// 9. ERROR HANDLING MIDDLEWARE EXAMPLE
// =============================================

// HTTP middleware for centralized error handling and observability
func ObservabilityMiddleware(next http.Handler, logger *StructuredLogger, metrics *MetricsCollector) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// Create context with request ID
		ctx := r.Context()
		requestID := fmt.Sprintf("%d", time.Now().UnixNano())
		ctx = context.WithValue(ctx, "request_id", requestID)

		// Wrap response writer to capture status code
		rw := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

		defer func() {
			// Handle panics
			if err := recover(); err != nil {
				// Log with stack trace
				logger.Log("ERROR", "Panic recovered", map[string]interface{}{
					"error":       err,
					"stack_trace": string(debug.Stack()),
					"request_id":  requestID,
					"duration":    time.Since(start).Seconds(),
				})

				// Record metric
				metrics.RecordError("panic")

				rw.WriteHeader(http.StatusInternalServerError)
				fmt.Fprintf(rw, "Internal Server Error")
			}

			// Record request metrics
			duration := time.Since(start)
			metrics.RecordRequest(r.Method, r.URL.Path, rw.statusCode, duration)

			// Log request completion
			logger.Log("INFO", "Request completed", map[string]interface{}{
				"method":      r.Method,
				"path":        r.URL.Path,
				"status_code": rw.statusCode,
				"duration":    duration.Seconds(),
				"request_id":  requestID,
			})
		}()

		next.ServeHTTP(rw, r.WithContext(ctx))
	})
}

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

// =============================================
// 10. SETUP AND INITIALIZATION
// =============================================

func setupObservability() (*StructuredLogger, *MetricsCollector, *TracingMiddleware, error) {
	// Setup structured logger
	logger := NewStructuredLogger("myapp", "1.0.0")

	// Setup metrics (simplified - in production use proper provider)
	meterProvider, err := setupMeterProvider()
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to setup metrics: %w", err)
	}

	meter := meterProvider.Meter("myapp")
	metrics, err := NewMetricsCollector(meter)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create metrics collector: %w", err)
	}

	// Setup tracing (simplified)
	tracer := NewTracingMiddleware("myapp")

	return logger, metrics, tracer, nil
}

func setupMeterProvider() (*metric.MeterProvider, error) {
	// Create a console exporter for demo purposes
	// In production, use Prometheus, OTLP, etc.
	exporter, err := stdoutmetric.New()
	if err != nil {
		return nil, err
	}

	provider := metric.NewMeterProvider(
		metric.WithReader(metric.NewPeriodicReader(exporter)),
	)

	return provider, nil
}

func setupTraceProvider() (*sdktrace.TracerProvider, error) {
	// In production, configure proper exporter (Jaeger, Zipkin, etc.)
	tp := sdktrace.NewTracerProvider()
	otel.SetTracerProvider(tp)

	return tp, nil
}

// =============================================
// MAIN FUNCTION - DEMO USAGE
// =============================================

func main() {
	fmt.Println("=== Go Error Design & Observability Demo ===\n")

	// 1. Demonstrate error wrapping
	fmt.Println("1. Error Wrapping Example:")
	if err := ErrorWrappingExample(); err != nil {
		fmt.Printf("Wrapped error: %v\n", err)
		fmt.Printf("Is original error in chain? %v\n\n", errors.Is(err, errors.New("database connection failed")))
	}

	// 2. Demonstrate custom error types
	fmt.Println("2. Custom Error Types Example:")
	customErr := &DomainError{
		Code:    "AUTH_FAILED",
		Message: "Authentication failed",
		Op:      "UserService.Authenticate",
		Err:     errors.New("invalid credentials"),
		Time:    time.Now(),
	}
	fmt.Printf("Custom error: %v\n\n", customErr)

	// 3. Demonstrate structured logging
	fmt.Println("3. Structured Logging Example:")
	StructuredLoggingExample()
	fmt.Println()

	// 4. Demonstrate comprehensive service
	fmt.Println("4. Comprehensive Service Example:")
	service := NewUserService()
	ctx := context.Background()

	// Success case
	user, err := service.GetUser(ctx, "123")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("User: %+v\n", user)
	}

	// Error case
	_, err = service.GetUser(ctx, "0")
	if err != nil {
		fmt.Printf("Expected error: %v\n", err)

		// Check error type
		var domainErr *DomainError
		if errors.As(err, &domainErr) {
			fmt.Printf("Domain error code: %s\n", domainErr.Code)
		}
	}

	fmt.Println("\n=== End of Demo ===")
}

// Helper function to demonstrate error unwrapping
func processErrorChain(err error) {
	fmt.Println("\nError Chain Analysis:")
	for err != nil {
		fmt.Printf("- %v\n", err)
		err = errors.Unwrap(err)
	}
}
