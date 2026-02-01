/*
GOLANG OBSERVABILITY & RELIABILITY GUIDE
From Junior to Senior Developer Concepts
==========================================
*/

// ============================================================================
// 1. LOGGING STRATEGIES - Structured, Contextual, and Production-Ready Logging
// ============================================================================

package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"
    
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
)

// Anti-pattern: Basic unstructured logging
func BasicLogging() {
    log.Printf("User %s logged in from IP %s", "john", "192.168.1.1")
    // Problems: Hard to parse, filter, or analyze programmatically
}

// Pattern 1: Structured Logging with zap (Uber's logging library)
type StructuredLogging struct {
    logger *zap.Logger
}

func NewStructuredLogging() (*StructuredLogging, error) {
    // Production configuration
    config := zap.NewProductionConfig()
    config.OutputPaths = []string{"stdout", "/var/log/service.log"}
    config.ErrorOutputPaths = []string{"stderr"}
    config.EncoderConfig.TimeKey = "timestamp"
    config.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
    
    logger, err := config.Build()
    if err != nil {
        return nil, err
    }
    
    // Don't forget to defer logger.Sync() in main()
    return &StructuredLogging{logger: logger}, nil
}

func (sl *StructuredLogging) LogUserAction(userID, action, resource string, duration time.Duration) {
    // Structured logging with fields
    sl.logger.Info("user_action_completed",
        zap.String("user_id", userID),
        zap.String("action", action),
        zap.String("resource", resource),
        zap.Duration("duration_ms", duration),
        zap.Int("status_code", 200),
    )
    
    // Outputs JSON:
    // {
    //   "level": "info",
    //   "timestamp": "2024-01-01T10:00:00Z",
    //   "msg": "user_action_completed",
    //   "user_id": "user123",
    //   "action": "delete",
    //   "resource": "document_456",
    //   "duration_ms": 150.5,
    //   "status_code": 200
    // }
}

// Pattern 2: Contextual Logging with Request ID/Trace ID
type ContextualLogger struct {
    baseLogger *zap.Logger
}

func NewContextualLogger() *ContextualLogger {
    logger, _ := zap.NewProduction()
    return &ContextualLogger{baseLogger: logger}
}

func (cl *ContextualLogger) WithContext(ctx context.Context) *zap.Logger {
    // Extract correlation IDs from context
    if requestID, ok := ctx.Value("request_id").(string); ok {
        return cl.baseLogger.With(zap.String("request_id", requestID))
    }
    if traceID, ok := ctx.Value("trace_id").(string); ok {
        return cl.baseLogger.With(zap.String("trace_id", traceID))
    }
    return cl.baseLogger
}

// HTTP Middleware for contextual logging
func LoggingMiddleware(next http.Handler) http.Handler {
    logger, _ := zap.NewProduction()
    
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        
        // Generate request ID
        requestID := generateRequestID()
        
        // Create context with request ID
        ctx := context.WithValue(r.Context(), "request_id", requestID)
        r = r.WithContext(ctx)
        
        // Add request ID to response headers
        w.Header().Set("X-Request-ID", requestID)
        
        // Create logger with request context
        requestLogger := logger.With(
            zap.String("request_id", requestID),
            zap.String("method", r.Method),
            zap.String("path", r.URL.Path),
            zap.String("remote_addr", r.RemoteAddr),
            zap.String("user_agent", r.UserAgent()),
        )
        
        // Log request start
        requestLogger.Info("request_started")
        
        // Wrap response writer to capture status code
        rw := &responseWriter{ResponseWriter: w, statusCode: 200}
        
        // Call next handler
        next.ServeHTTP(rw, r)
        
        // Log request completion
        duration := time.Since(start)
        requestLogger.Info("request_completed",
            zap.Int("status_code", rw.statusCode),
            zap.Duration("duration_ms", duration),
            zap.Int64("response_size", rw.responseSize),
        )
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode   int
    responseSize int64
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

func (rw *responseWriter) Write(b []byte) (int, error) {
    n, err := rw.ResponseWriter.Write(b)
    rw.responseSize += int64(n)
    return n, err
}

func generateRequestID() string {
    return fmt.Sprintf("req_%d", time.Now().UnixNano())
}

// Pattern 3: Log Levels and Sampling
type LogLevelStrategy struct {
    logger *zap.Logger
}

func (lls *LogLevelStrategy) DemonstrateLogLevels() {
    // Appropriate use of log levels:
    lls.logger.Debug("debug_details", zap.String("detail", "low-level info"))
    lls.logger.Info("user_action", zap.String("action", "login"))
    lls.logger.Warn("potential_issue", zap.String("issue", "cache miss"))
    lls.logger.Error("operation_failed", 
        zap.Error(fmt.Errorf("database connection failed")),
        zap.String("component", "database"),
    )
    // Fatal and Panic should be used sparingly
    
    // Dynamic log level adjustment
    if os.Getenv("ENVIRONMENT") == "production" {
        zap.NewAtomicLevelAt(zap.InfoLevel)
    } else {
        zap.NewAtomicLevelAt(zap.DebugLevel)
    }
}

// Pattern 4: Log Aggregation and Correlation
type LogCorrelation struct{}

func (lc *LogCorrelation) CorrelateLogs() {
    // All logs for a single request should share:
    // - Request ID
    // - Trace ID
    // - User ID
    // - Session ID
    
    // This enables:
    // 1. Finding all logs for a specific request
    // 2. Tracing a request through multiple services
    // 3. Debugging user-specific issues
}

// ============================================================================
// 2. METRICS WITH PROMETHEUS CONCEPTS - Monitoring and Alerting
// ============================================================================

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

// Four types of Prometheus metrics:
// 1. Counter: Monotonically increasing value (requests, errors)
// 2. Gauge: Value that can go up and down (memory usage, active connections)
// 3. Histogram: Samples observations into buckets (request duration, response size)
// 4. Summary: Similar to histogram but calculates quantiles

type MetricsCollector struct {
    // HTTP Request Metrics
    httpRequestsTotal *prometheus.CounterVec
    httpRequestDuration *prometheus.HistogramVec
    httpRequestSize *prometheus.SummaryVec
    
    // Business Metrics
    userRegistrations prometheus.Counter
    ordersProcessed *prometheus.CounterVec
    cartValue *prometheus.GaugeVec
    
    // System Metrics
    goroutineCount prometheus.Gauge
    memoryUsage    prometheus.Gauge
}

func NewMetricsCollector() *MetricsCollector {
    return &MetricsCollector{
        // Counter example: total HTTP requests
        httpRequestsTotal: promauto.NewCounterVec(
            prometheus.CounterOpts{
                Name: "http_requests_total",
                Help: "Total number of HTTP requests",
                ConstLabels: prometheus.Labels{
                    "service": "api-gateway",
                },
            },
            []string{"method", "path", "status_code"},
        ),
        
        // Histogram example: request duration
        httpRequestDuration: promauto.NewHistogramVec(
            prometheus.HistogramOpts{
                Name:    "http_request_duration_seconds",
                Help:    "Duration of HTTP requests in seconds",
                Buckets: prometheus.DefBuckets, // Default buckets: .005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10
            },
            []string{"method", "path"},
        ),
        
        // Summary example: request/response size
        httpRequestSize: promauto.NewSummaryVec(
            prometheus.SummaryOpts{
                Name:       "http_request_size_bytes",
                Help:       "Size of HTTP requests in bytes",
                Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
            },
            []string{"method", "path"},
        ),
        
        // Business metric: user registrations
        userRegistrations: promauto.NewCounter(
            prometheus.CounterOpts{
                Name: "user_registrations_total",
                Help: "Total number of user registrations",
            },
        ),
        
        // Business metric: orders by status
        ordersProcessed: promauto.NewCounterVec(
            prometheus.CounterOpts{
                Name: "orders_processed_total",
                Help: "Total number of processed orders",
            },
            []string{"status"}, // created, paid, shipped, cancelled
        ),
        
        // Gauge example: current cart value
        cartValue: promauto.NewGaugeVec(
            prometheus.GaugeOpts{
                Name: "cart_value_usd",
                Help: "Current value of shopping cart in USD",
            },
            []string{"user_id"},
        ),
        
        // System metric: goroutine count
        goroutineCount: promauto.NewGauge(
            prometheus.GaugeOpts{
                Name: "go_goroutines",
                Help: "Number of active goroutines",
            },
        ),
    }
}

func (mc *MetricsCollector) RecordHTTPRequest(method, path, statusCode string, duration time.Duration, size int64) {
    mc.httpRequestsTotal.WithLabelValues(method, path, statusCode).Inc()
    mc.httpRequestDuration.WithLabelValues(method, path).Observe(duration.Seconds())
    mc.httpRequestSize.WithLabelValues(method, path).Observe(float64(size))
}

func (mc *MetricsCollector) RecordBusinessEvent(event string, labels ...string) {
    switch event {
    case "user_registration":
        mc.userRegistrations.Inc()
    case "order_processed":
        if len(labels) > 0 {
            mc.ordersProcessed.WithLabelValues(labels[0]).Inc()
        }
    case "cart_updated":
        if len(labels) == 2 {
            value := parseFloat(labels[1])
            mc.cartValue.WithLabelValues(labels[0]).Set(value)
        }
    }
}

func parseFloat(s string) float64 {
    var f float64
    fmt.Sscanf(s, "%f", &f)
    return f
}

// HTTP Handler for Prometheus metrics
func (mc *MetricsCollector) MetricsHandler() http.Handler {
    return promhttp.Handler()
}

// Custom Collectors for application-specific metrics
type CustomCollector struct {
    activeSessions prometheus.Gauge
    cacheHitRatio  prometheus.Gauge
}

func (cc *CustomCollector) Describe(ch chan<- *prometheus.Desc) {
    ch <- cc.activeSessions.Desc()
    ch <- cc.cacheHitRatio.Desc()
}

func (cc *CustomCollector) Collect(ch chan<- prometheus.Metric) {
    // Update metrics with current values
    activeSessions := getActiveSessions()
    cacheHitRatio := getCacheHitRatio()
    
    cc.activeSessions.Set(float64(activeSessions))
    cc.cacheHitRatio.Set(cacheHitRatio)
    
    ch <- cc.activeSessions
    ch <- cc.cacheHitRatio
}

func getActiveSessions() int {
    // Implementation to get active sessions
    return 42
}

func getCacheHitRatio() float64 {
    // Implementation to calculate cache hit ratio
    return 0.95
}

// Metrics Middleware
func MetricsMiddleware(metrics *MetricsCollector, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        
        // Wrap response writer to capture status and size
        rw := &metricsResponseWriter{ResponseWriter: w}
        
        // Call next handler
        next.ServeHTTP(rw, r)
        
        // Record metrics
        duration := time.Since(start)
        metrics.RecordHTTPRequest(
            r.Method,
            r.URL.Path,
            fmt.Sprintf("%d", rw.statusCode),
            duration,
            rw.size,
        )
    })
}

type metricsResponseWriter struct {
    http.ResponseWriter
    statusCode int
    size       int64
}

func (mrw *metricsResponseWriter) WriteHeader(code int) {
    mrw.statusCode = code
    mrw.ResponseWriter.WriteHeader(code)
}

func (mrw *metricsResponseWriter) Write(b []byte) (int, error) {
    n, err := mrw.ResponseWriter.Write(b)
    mrw.size += int64(n)
    return n, err
}

// Alerting Rules Example (Prometheus YAML format)
/*
groups:
  - name: example
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High error rate on {{ $labels.instance }}"
        description: "Error rate is {{ $value }} for {{ $labels.service }}"
    
    - alert: HighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
      for: 10m
      labels:
        severity: warning
*/

// ============================================================================
// 3. DISTRIBUTED TRACING - Following Requests Across Services
// ============================================================================

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
    "go.opentelemetry.io/otel/trace"
)

type TracingManager struct {
    tracer trace.Tracer
}

func InitTracing(serviceName string) (*TracingManager, func(), error) {
    // Create Jaeger exporter
    exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(
        jaeger.WithEndpoint("http://jaeger:14268/api/traces"),
    ))
    if err != nil {
        return nil, nil, err
    }
    
    // Create resource with service name
    res := resource.NewWithAttributes(
        semconv.SchemaURL,
        semconv.ServiceNameKey.String(serviceName),
        attribute.String("environment", os.Getenv("ENVIRONMENT")),
        attribute.String("version", "1.0.0"),
    )
    
    // Create trace provider
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        sdktrace.WithSampler(sdktrace.ParentBased(
            sdktrace.TraceIDRatioBased(0.1), // Sample 10% of traces in production
        )),
    )
    
    // Set global tracer provider and propagator
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(
        propagation.NewCompositeTextMapPropagator(
            propagation.TraceContext{},
            propagation.Baggage{},
        ),
    )
    
    // Create tracer
    tracer := tp.Tracer(serviceName)
    
    // Return cleanup function
    cleanup := func() {
        tp.Shutdown(context.Background())
    }
    
    return &TracingManager{tracer: tracer}, cleanup, nil
}

func (tm *TracingManager) StartSpan(ctx context.Context, spanName string) (context.Context, trace.Span) {
    return tm.tracer.Start(ctx, spanName)
}

// HTTP Handler with distributed tracing
func TracingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Extract trace context from headers
        ctx := otel.GetTextMapPropagator().Extract(r.Context(), propagation.HeaderCarrier(r.Header))
        
        // Start span
        ctx, span := otel.Tracer("http-server").Start(ctx, r.URL.Path)
        defer span.End()
        
        // Add attributes to span
        span.SetAttributes(
            attribute.String("http.method", r.Method),
            attribute.String("http.path", r.URL.Path),
            attribute.String("http.user_agent", r.UserAgent()),
            attribute.String("http.client_ip", r.RemoteAddr),
        )
        
        // Add span to context
        r = r.WithContext(ctx)
        
        // Inject trace context into response headers
        w.Header().Set("X-Trace-ID", span.SpanContext().TraceID().String())
        
        // Create response writer that captures status
        rw := &tracingResponseWriter{ResponseWriter: w, statusCode: 200}
        
        // Call next handler
        next.ServeHTTP(rw, r)
        
        // Record final span attributes
        span.SetAttributes(attribute.Int("http.status_code", rw.statusCode))
        
        if rw.statusCode >= 400 {
            span.SetStatus(codes.Error, fmt.Sprintf("HTTP %d", rw.statusCode))
        }
    })
}

type tracingResponseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (trw *tracingResponseWriter) WriteHeader(code int) {
    trw.statusCode = code
    trw.ResponseWriter.WriteHeader(code)
}

// Database operation with tracing
func (tm *TracingManager) QueryWithTrace(ctx context.Context, query string, args ...interface{}) error {
    ctx, span := tm.tracer.Start(ctx, "database.query")
    defer span.End()
    
    span.SetAttributes(
        attribute.String("db.query", query),
        attribute.Int("db.args_count", len(args)),
        attribute.String("db.system", "postgresql"),
    )
    
    // Execute query
    // result, err := db.ExecContext(ctx, query, args...)
    
    // if err != nil {
    //     span.RecordError(err)
    //     span.SetStatus(codes.Error, err.Error())
    //     return err
    // }
    
    // span.SetAttributes(attribute.Int64("db.rows_affected", rowsAffected))
    return nil
}

// RPC/gRPC call with tracing
func (tm *TracingManager) CallServiceWithTrace(ctx context.Context, serviceName, method string, request interface{}) (interface{}, error) {
    ctx, span := tm.tracer.Start(ctx, fmt.Sprintf("%s.%s", serviceName, method))
    defer span.End()
    
    span.SetAttributes(
        attribute.String("rpc.service", serviceName),
        attribute.String("rpc.method", method),
    )
    
    // Make the actual RPC call with trace context propagated
    // The trace context will be automatically propagated if using
    // OpenTelemetry instrumented gRPC client
    
    return nil, nil
}

// ============================================================================
// 4. SLIs / SLOs / SLAs - Measuring and Managing Reliability
// ============================================================================

type ReliabilityMetrics struct {
    // Service Level Indicators (SLIs) - What we measure
    availability   prometheus.Gauge
    latency        prometheus.Histogram
    errorRate      prometheus.Gauge
    throughput     prometheus.Counter
    
    // Service Level Objectives (SLOs) - Our internal targets
    availabilityTarget   float64 // 0.9999 = 99.99%
    latencyTarget        float64 // 0.1 seconds
    errorRateTarget      float64 // 0.001 = 0.1%
    
    // Service Level Agreements (SLAs) - Contractual commitments to customers
    // Usually slightly lower than SLOs to allow for buffer
}

func NewReliabilityMetrics() *ReliabilityMetrics {
    return &ReliabilityMetrics{
        availability: promauto.NewGauge(prometheus.GaugeOpts{
            Name: "service_availability",
            Help: "Current service availability percentage",
        }),
        
        latency: promauto.NewHistogram(prometheus.HistogramOpts{
            Name:    "service_latency_seconds",
            Help:    "Service latency distribution",
            Buckets: []float64{0.01, 0.05, 0.1, 0.2, 0.5, 1, 2},
        }),
        
        errorRate: promauto.NewGauge(prometheus.GaugeOpts{
            Name: "service_error_rate",
            Help: "Current error rate percentage",
        }),
        
        throughput: promauto.NewCounter(prometheus.CounterOpts{
            Name: "service_requests_total",
            Help: "Total service requests",
        }),
        
        availabilityTarget: 0.9995,  // 99.95%
        latencyTarget:      0.2,     // 200ms
        errorRateTarget:    0.005,   // 0.5%
    }
}

// Common SLIs for web services:
func (rm *ReliabilityMetrics) CalculateSLIs() {
    // 1. Availability = Successful requests / Total requests
    // availability := successCount / totalCount
    
    // 2. Latency = Time to process requests
    // Usually measured as p95, p99, or average
    
    // 3. Throughput = Requests per second
    // throughput := requestCount / timeWindow
    
    // 4. Error Rate = Failed requests / Total requests
    // errorRate := errorCount / totalCount
}

// Error Budget Calculation
type ErrorBudget struct {
    budget          float64
    consumedBudget  float64
    timeWindow      time.Duration
}

func NewErrorBudget(availabilityTarget float64, timeWindow time.Duration) *ErrorBudget {
    // Error budget = 1 - availability target
    // For 99.95% availability, error budget = 0.05% downtime
    return &ErrorBudget{
        budget:     1 - availabilityTarget,
        timeWindow: timeWindow,
    }
}

func (eb *ErrorBudget) RecordError(duration time.Duration) {
    // Consume error budget based on error duration
    errorPercentage := duration.Seconds() / eb.timeWindow.Seconds()
    eb.consumedBudget += errorPercentage
    
    // Alert when error budget is running low
    budgetRemaining := eb.budget - eb.consumedBudget
    if budgetRemaining < eb.budget*0.1 { // Less than 10% budget remaining
        // Trigger alert: "Error budget nearly exhausted"
    }
}

// SLO Compliance Dashboard Metrics
type SLOCompliance struct {
    // Rolling window SLO compliance
    sloCompliance30d prometheus.Gauge
    sloCompliance7d  prometheus.Gauge
    sloCompliance24h prometheus.Gauge
}

// ============================================================================
// 5. INCIDENT RESPONSE BASICS - Preparing for and Handling Outages
// ============================================================================

type IncidentResponse struct {
    // Preparedness
    runbooks         map[string]Runbook
    escalationPolicy EscalationPolicy
    communication    CommunicationPlan
    
    // During Incident
    incident         *Incident
    timeline         []TimelineEvent
    statusPage       StatusPage
}

type Runbook struct {
    Name        string
    Description string
    Steps       []RunbookStep
    Triggers    []string // Alert names that trigger this runbook
}

type RunbookStep struct {
    Action      string
    Command     string
    Expected    string
    Timeout     time.Duration
}

type EscalationPolicy struct {
    Levels []EscalationLevel
}

type EscalationLevel struct {
    Level      int
    Notify     []string // Teams, individuals
    Timeout    time.Duration
    Conditions []string
}

type CommunicationPlan struct {
    InternalChannels  []string // Slack, Teams
    ExternalChannels  []string // Status page, Twitter
    CustomerUpdates   []CustomerUpdateTemplate
}

type Incident struct {
    ID          string
    Title       string
    Severity    string // P1 (Critical), P2 (High), P3 (Medium), P4 (Low)
    Status      string // Investigating, Identified, Monitoring, Resolved
    Services    []string
    StartTime   time.Time
    DetectedBy  string // Monitoring, Customer report, Team report
    Impact      string // "Users cannot login", "API is returning 500 errors"
}

type TimelineEvent struct {
    Timestamp time.Time
    Actor     string
    Action    string
    Details   string
}

type StatusPage struct {
    Components []ComponentStatus
    Incidents  []IncidentUpdate
}

type ComponentStatus struct {
    Name   string
    Status string // Operational, Degraded, Outage, Maintenance
}

type IncidentUpdate struct {
    Time    time.Time
    Status  string
    Message string
}

// Incident Response Functions
func (ir *IncidentResponse) StartIncident(title, severity, impact string) *Incident {
    incident := &Incident{
        ID:         generateIncidentID(),
        Title:      title,
        Severity:   severity,
        Status:     "Investigating",
        StartTime:  time.Now(),
        Impact:     impact,
    }
    
    ir.incident = incident
    ir.timeline = append(ir.timeline, TimelineEvent{
        Timestamp: time.Now(),
        Actor:     "System",
        Action:    "Incident declared",
        Details:   fmt.Sprintf("Severity: %s, Impact: %s", severity, impact),
    })
    
    // Trigger alert to on-call engineer
    ir.escalateToOnCall(severity)
    
    // Update status page
    ir.updateStatusPage("investigating", "We are investigating reported issues")
    
    return incident
}

func (ir *IncidentResponse) escalateToOnCall(severity string) {
    // Implementation would integrate with PagerDuty, Opsgenie, etc.
    fmt.Printf("Escalating %s incident to on-call engineer\n", severity)
}

func (ir *IncidentResponse) updateStatusPage(status, message string) {
    // Implementation would update external status page
    fmt.Printf("Status page update: %s - %s\n", status, message)
}

func (ir *IncidentResponse) AddTimelineEvent(actor, action, details string) {
    event := TimelineEvent{
        Timestamp: time.Now(),
        Actor:     actor,
        Action:    action,
        Details:   details,
    }
    ir.timeline = append(ir.timeline, event)
}

func (ir *IncidentResponse) UpdateStatus(newStatus, details string) {
    ir.incident.Status = newStatus
    ir.AddTimelineEvent("Incident Commander", "Status update", details)
    ir.updateStatusPage(newStatus, details)
}

func (ir *IncidentResponse) ResolveIncident(rootCause, resolution string) {
    ir.incident.Status = "Resolved"
    ir.AddTimelineEvent("Incident Commander", "Incident resolved", 
        fmt.Sprintf("Root cause: %s, Resolution: %s", rootCause, resolution))
    ir.updateStatusPage("resolved", "The issue has been resolved")
    
    // TODO: Schedule post-mortem
    // TODO: Update runbooks based on learnings
}

// Post-Mortem / Post-Incident Review
type PostMortem struct {
    IncidentID      string
    Summary         string
    Timeline        []TimelineEvent
    RootCause       string
    Impact          string // Number of users affected, duration, business impact
    Actions         []ActionItem
    Learnings       []string
}

type ActionItem struct {
    Description string
    Owner       string
    DueDate     time.Time
    Status      string // Open, In Progress, Completed
}

func generateIncidentID() string {
    return fmt.Sprintf("INC-%d-%s", 
        time.Now().Year(),
        randomString(6),
    )
}

func randomString(n int) string {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    b := make([]byte, n)
    for i := range b {
        b[i] = letters[time.Now().UnixNano()%int64(len(letters))]
    }
    return string(b)
}

// ============================================================================
// PRACTICAL INTEGRATION - Complete Observability Stack
// ============================================================================

type ObservabilityStack struct {
    logger   *zap.Logger
    metrics  *MetricsCollector
    tracing  *TracingManager
    slos     *ReliabilityMetrics
}

func NewObservabilityStack(serviceName string) (*ObservabilityStack, error) {
    // Initialize logging
    logger, err := zap.NewProduction()
    if err != nil {
        return nil, err
    }
    
    // Initialize metrics
    metrics := NewMetricsCollector()
    
    // Initialize tracing
    tracing, cleanup, err := InitTracing(serviceName)
    if err != nil {
        logger.Error("Failed to initialize tracing", zap.Error(err))
        // Continue without tracing - fail open
    }
    defer cleanup() // In real app, call this on shutdown
    
    // Initialize SLO tracking
    slos := NewReliabilityMetrics()
    
    return &ObservabilityStack{
        logger:  logger,
        metrics: metrics,
        tracing: tracing,
        slos:    slos,
    }, nil
}

func (os *ObservabilityStack) InstrumentHTTPHandler(handler http.Handler) http.Handler {
    // Chain middlewares in correct order
    return LoggingMiddleware(
        TracingMiddleware(
            MetricsMiddleware(os.metrics, handler),
        ),
    )
}

func (os *ObservabilityStack) RecordBusinessTransaction(ctx context.Context, transaction string, success bool, duration time.Duration) {
    // Correlated logging
    os.logger.Info("business_transaction",
        zap.String("transaction", transaction),
        zap.Bool("success", success),
        zap.Duration("duration", duration),
    )
    
    // Record metrics
    if success {
        os.metrics.ordersProcessed.WithLabelValues("success").Inc()
    } else {
        os.metrics.ordersProcessed.WithLabelValues("failed").Inc()
    }
    
    // Record trace span
    if os.tracing != nil {
        _, span := os.tracing.tracer.Start(ctx, transaction)
        defer span.End()
        
        span.SetAttributes(
            attribute.String("transaction.type", transaction),
            attribute.Bool("transaction.success", success),
            attribute.Float64("transaction.duration_ms", duration.Seconds()*1000),
        )
        
        if !success {
            span.SetStatus(codes.Error, "Transaction failed")
        }
    }
}

// ============================================================================
// MAIN FUNCTION - DEMONSTRATION
// ============================================================================

func main() {
    fmt.Println("=== Observability & Reliability Patterns in Go ===")
    
    // 1. Logging Strategies
    sl, err := NewStructuredLogging()
    if err != nil {
        log.Fatal(err)
    }
    defer sl.logger.Sync()
    
    sl.LogUserAction("user123", "delete", "document_456", 150*time.Millisecond)
    
    // 2. Metrics with Prometheus
    metrics := NewMetricsCollector()
    
    // Simulate recording metrics
    metrics.RecordHTTPRequest("GET", "/api/users", "200", 150*time.Millisecond, 2048)
    metrics.RecordBusinessEvent("user_registration")
    metrics.RecordBusinessEvent("order_processed", "paid")
    
    // 3. Distributed Tracing
    tracing, cleanup, err := InitTracing("example-service")
    if err != nil {
        fmt.Printf("Tracing init error: %v\n", err)
    } else {
        defer cleanup()
        
        ctx := context.Background()
        ctx, span := tracing.StartSpan(ctx, "example-operation")
        defer span.End()
    }
    
    // 4. SLIs/SLOs/SLAs
    reliability := NewReliabilityMetrics()
    errorBudget := NewErrorBudget(0.9995, 30*24*time.Hour) // 30-day error budget
    
    // Simulate error
    errorBudget.RecordError(15 * time.Minute) // 15 minutes of downtime
    
    // 5. Incident Response
    ir := &IncidentResponse{}
    incident := ir.StartIncident("Database connectivity issues", "P2", 
        "Users experiencing intermittent errors when accessing profile data")
    
    // Add timeline events
    ir.AddTimelineEvent("Engineer", "Identified root cause", 
        "Database connection pool exhausted due to leak")
    ir.AddTimelineEvent("Engineer", "Applied fix", 
        "Restarted service with increased connection pool size")
    
    // Resolve incident
    ir.ResolveIncident(
        "Database connection leak in v1.2.3",
        "Rolled back to v1.2.2 and applied connection pool fixes",
    )
    
    fmt.Printf("Incident %s resolved\n", incident.ID)
    
    // Complete Observability Stack
    obsStack, err := NewObservabilityStack("user-service")
    if err != nil {
        log.Fatal(err)
    }
    
    // Create HTTP server with full instrumentation
    mux := http.NewServeMux()
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
    })
    
    instrumentedHandler := obsStack.InstrumentHTTPHandler(mux)
    
    // Start metrics endpoint
    go func() {
        http.Handle("/metrics", metrics.MetricsHandler())
        http.ListenAndServe(":9090", nil)
    }()
    
    fmt.Println("\n=== Key Takeaways ===")
    fmt.Println("1. Use structured logging with correlation IDs for debugging")
    fmt.Println("2. Implement the Four Golden Signals: Latency, Traffic, Errors, Saturation")
    fmt.Println("3. Use distributed tracing to follow requests across services")
    fmt.Println("4. Define SLIs, set SLOs, and monitor error budgets")
    fmt.Println("5. Have incident response procedures before incidents happen")
    fmt.Println("6. Observability enables reliability - you can't improve what you can't measure")
    fmt.Println("7. Always include business metrics alongside technical metrics")
    fmt.Println("8. Automate as much of incident response as possible")
    
    // Start server
    fmt.Println("\nServer starting on :8080 with metrics on :9090")
    // Uncomment to start server:
    // http.ListenAndServe(":8080", instrumentedHandler)
}

// Production Checklist:
// 1. Structured JSON logging to stdout
// 2. Metrics exported in Prometheus format
// 3. Distributed tracing with sampling
// 4. Health checks with dependencies
// 5. Alerting on SLO violations
// 6. Runbooks for common failures
// 7. Dashboards for key metrics
// 8. Log aggregation (ELK, Loki)
// 9. Metrics aggregation (Prometheus, Thanos)
// 10. Trace aggregation (Jaeger, Tempo)

// Remember: Observability is not just about debugging - it's about
// understanding system behavior and building confidence in production.