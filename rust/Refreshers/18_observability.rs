//// RUST OBSERVABILITY - LOGGING, TRACING, AND METRICS
/// Comprehensive guide to observability in Rust applications
/// Covers logging (log, env_logger), tracing (tracing crate), and metrics (Prometheus)

use std::time::Instant;

// ============================================================================
// 1. LOGGING WITH LOG CRATE
// ============================================================================

/// The log crate provides a logging facade
/// Actual logging implementation provided by:
/// - env_logger (simple, environment-based)
/// - tracing-subscriber (advanced, structured)
/// - log4rs (complex configurations)

/*
use log::{trace, debug, info, warn, error};

fn main() {
    // Initialize logger (env_logger example)
    env_logger::init();
    
    // Log at different levels
    trace!("Very detailed information");
    debug!("Debug information");
    info!("General information");
    warn!("Warning message");
    error!("Error occurred");
    
    // With formatting
    let user_id = 42;
    info!("User {} logged in", user_id);
    
    // With structured data
    info!("Request processed: method={}, path={}, duration={}ms", 
          "GET", "/api/users", 45);
}

// Run with log level:
// RUST_LOG=debug cargo run
// RUST_LOG=info cargo run
// RUST_LOG=myapp=debug cargo run  // Only for myapp
*/

/// LOG LEVELS (from most to least verbose):
/// - TRACE: Very detailed, usually disabled
/// - DEBUG: Debugging information
/// - INFO: General informational messages
/// - WARN: Warning, not an error
/// - ERROR: Error occurred


// ============================================================================
// 2. TRACING CRATE - STRUCTURED LOGGING
// ============================================================================

/// The tracing crate provides structured, async-aware logging
/// More powerful than log crate:
/// - Structured events
/// - Spans (represent time periods)
/// - Context propagation
/// - Async-aware
/// - Instrumentation

/*
use tracing::{info, warn, error, debug, trace, instrument, span, Level};
use tracing_subscriber;

fn main() {
    // Initialize tracing subscriber
    tracing_subscriber::fmt()
        .with_max_level(Level::DEBUG)
        .with_target(false)
        .with_thread_ids(true)
        .with_line_number(true)
        .init();
    
    // Structured logging with fields
    info!(user_id = 123, action = "login", "User logged in");
    
    // Spans - represent periods of time
    let span = span!(Level::INFO, "request", method = "GET", path = "/api/users");
    let _enter = span.enter();
    
    info!("Processing request");
    // Span context automatically included
    
    // Instrument functions
    process_request(42).await;
}

// Automatically creates span with function name and arguments
#[instrument]
async fn process_request(request_id: u64) {
    info!("Processing started");
    
    // Child span
    process_database_query().await;
    
    info!("Processing completed");
}

#[instrument(skip(db), fields(query_type = "select"))]
async fn process_database_query() {
    info!("Querying database");
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
}
*/


// ============================================================================
// 3. ADVANCED TRACING PATTERNS
// ============================================================================

/*
use tracing::{Span, field};

// Creating spans manually with fields
fn handle_request(user_id: u64, request_id: String) {
    let span = tracing::info_span!(
        "handle_request",
        user_id = user_id,
        request_id = %request_id,  // % for Display formatting
        response_status = field::Empty  // Fill later
    );
    
    let _enter = span.enter();
    
    info!("Request received");
    
    // Record additional field later
    span.record("response_status", 200);
}

// Error handling with tracing
#[instrument]
async fn risky_operation(id: u64) -> Result<String, MyError> {
    info!("Starting risky operation");
    
    match perform_operation(id).await {
        Ok(result) => {
            info!(result = %result, "Operation succeeded");
            Ok(result)
        }
        Err(e) => {
            error!(error = %e, "Operation failed");
            Err(e)
        }
    }
}

// Skip sensitive data in spans
#[instrument(skip(password))]
async fn authenticate(username: &str, password: &str) -> Result<Token, AuthError> {
    info!("Authenticating user");
    // password not logged
    todo!()
}
*/


// ============================================================================
// 4. TRACING SUBSCRIBER CONFIGURATION
// ============================================================================

/*
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn setup_tracing() {
    tracing_subscriber::registry()
        // Filter based on environment variable
        .with(EnvFilter::from_default_env())
        // Format layer (console output)
        .with(
            tracing_subscriber::fmt::layer()
                .with_target(true)
                .with_line_number(true)
                .with_thread_ids(true)
                .json()  // JSON output for log aggregation
        )
        .init();
}

// JSON output example:
// {"timestamp":"2024-01-01T12:00:00.000Z","level":"INFO","target":"myapp",
//  "fields":{"message":"User logged in","user_id":123}}
*/


// ============================================================================
// 5. DISTRIBUTED TRACING WITH OPENTELEMETRY
// ============================================================================

/// OpenTelemetry provides distributed tracing standard
/// Traces requests across multiple services

/*
use opentelemetry::{global, sdk::trace as sdktrace, trace::Tracer};
use tracing_subscriber::{layer::SubscriberExt, Registry};
use tracing_opentelemetry::OpenTelemetryLayer;

fn setup_opentelemetry() {
    // Create tracer
    let tracer = opentelemetry_jaeger::new_pipeline()
        .with_service_name("my-service")
        .install_simple()
        .expect("Failed to install OpenTelemetry tracer");
    
    // Create tracing layer
    let telemetry = tracing_opentelemetry::layer().with_tracer(tracer);
    
    // Setup subscriber
    let subscriber = Registry::default()
        .with(telemetry)
        .with(tracing_subscriber::fmt::layer());
    
    tracing::subscriber::set_global_default(subscriber)
        .expect("Failed to set subscriber");
}

// Spans automatically create OpenTelemetry spans
#[instrument]
async fn http_request() {
    info!("Making HTTP request");
    
    // Trace context automatically propagated
    call_another_service().await;
}

#[instrument]
async fn call_another_service() {
    info!("Calling another service");
    // Trace ID propagated automatically
}
*/


// ============================================================================
// 6. METRICS WITH PROMETHEUS
// ============================================================================

/// Prometheus metrics in Rust
/// Types:
/// - Counter: Monotonically increasing (requests, errors)
/// - Gauge: Can go up/down (active connections, memory)
/// - Histogram: Distribution (request duration, response size)
/// - Summary: Similar to histogram with quantiles

/*
use prometheus::{
    Counter, Histogram, Gauge, Registry,
    IntCounter, IntGauge, HistogramVec,
    Encoder, TextEncoder,
    opts, register_counter, register_histogram, register_gauge,
};
use once_cell::sync::Lazy;

// Define metrics (global, initialized once)
static HTTP_REQUESTS: Lazy<IntCounter> = Lazy::new(|| {
    register_counter!(
        "http_requests_total",
        "Total HTTP requests"
    ).unwrap()
});

static HTTP_REQUEST_DURATION: Lazy<HistogramVec> = Lazy::new(|| {
    register_histogram_vec!(
        "http_request_duration_seconds",
        "HTTP request duration",
        &["method", "endpoint", "status"]
    ).unwrap()
});

static ACTIVE_CONNECTIONS: Lazy<IntGauge> = Lazy::new(|| {
    register_gauge!(
        "active_connections",
        "Active connections"
    ).unwrap()
});

// Use in application
async fn handle_request(method: &str, endpoint: &str) -> Result<(), MyError> {
    HTTP_REQUESTS.inc();
    ACTIVE_CONNECTIONS.inc();
    
    let timer = HTTP_REQUEST_DURATION
        .with_label_values(&[method, endpoint, "200"])
        .start_timer();
    
    // Process request
    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
    
    timer.observe_duration();
    ACTIVE_CONNECTIONS.dec();
    
    Ok(())
}

// Expose metrics endpoint
use axum::{response::IntoResponse, http::StatusCode};

async fn metrics_handler() -> impl IntoResponse {
    let encoder = TextEncoder::new();
    let metric_families = prometheus::gather();
    let mut buffer = vec![];
    
    encoder.encode(&metric_families, &mut buffer).unwrap();
    
    (
        StatusCode::OK,
        [("Content-Type", encoder.format_type())],
        buffer
    )
}

// Add to router:
// .route("/metrics", get(metrics_handler))
*/


// ============================================================================
// 7. CUSTOM METRICS MIDDLEWARE
// ============================================================================

/*
use axum::{
    middleware::{self, Next},
    http::Request,
    body::Body,
    response::Response,
};

async fn metrics_middleware(
    request: Request<Body>,
    next: Next,
) -> Response {
    let method = request.method().clone();
    let uri = request.uri().clone();
    
    ACTIVE_CONNECTIONS.inc();
    
    let start = Instant::now();
    
    // Process request
    let response = next.run(request).await;
    
    let duration = start.elapsed().as_secs_f64();
    let status = response.status().as_u16().to_string();
    
    // Record metrics
    HTTP_REQUESTS.inc();
    HTTP_REQUEST_DURATION
        .with_label_values(&[method.as_str(), uri.path(), &status])
        .observe(duration);
    
    ACTIVE_CONNECTIONS.dec();
    
    response
}

// Add to app:
// .layer(middleware::from_fn(metrics_middleware))
*/


// ============================================================================
// 8. HEALTH CHECKS
// ============================================================================

/*
use axum::Json;
use serde::Serialize;

#[derive(Serialize)]
struct HealthCheck {
    status: String,
    timestamp: String,
    checks: Vec<ComponentHealth>,
}

#[derive(Serialize)]
struct ComponentHealth {
    name: String,
    status: String,
    details: Option<String>,
}

async fn health_handler(
    State(state): State<AppState>
) -> Json<HealthCheck> {
    let mut checks = vec![];
    
    // Check database
    let db_status = match sqlx::query("SELECT 1")
        .execute(&state.pool)
        .await
    {
        Ok(_) => ComponentHealth {
            name: "database".to_string(),
            status: "healthy".to_string(),
            details: None,
        },
        Err(e) => ComponentHealth {
            name: "database".to_string(),
            status: "unhealthy".to_string(),
            details: Some(e.to_string()),
        },
    };
    
    checks.push(db_status);
    
    // Overall status
    let all_healthy = checks.iter().all(|c| c.status == "healthy");
    let status = if all_healthy { "healthy" } else { "unhealthy" };
    
    Json(HealthCheck {
        status: status.to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
        checks,
    })
}

// Liveness probe (always returns 200 if app is running)
async fn liveness_handler() -> impl IntoResponse {
    StatusCode::OK
}

// Readiness probe (returns 200 if ready to serve traffic)
async fn readiness_handler(State(state): State<AppState>) -> impl IntoResponse {
    // Check if database is reachable
    match sqlx::query("SELECT 1").execute(&state.pool).await {
        Ok(_) => StatusCode::OK,
        Err(_) => StatusCode::SERVICE_UNAVAILABLE,
    }
}
*/


// ============================================================================
// 9. BEST PRACTICES
// ============================================================================

/// OBSERVABILITY BEST PRACTICES:
/// 
/// LOGGING:
/// ✓ Use tracing crate for structured logging
/// ✓ Include correlation IDs (request_id, trace_id)
/// ✓ Log at appropriate levels
/// ✓ Never log secrets
/// ✓ Use JSON format for production
/// ✓ Configure via environment variables
/// 
/// TRACING:
/// ✓ Use #[instrument] on async functions
/// ✓ Add spans for important operations
/// ✓ Include context in spans
/// ✓ Propagate trace context across services
/// ✓ Sample traces (don't trace everything)
/// ✓ Use OpenTelemetry for distributed tracing
/// 
/// METRICS:
/// ✓ Expose /metrics endpoint (Prometheus format)
/// ✓ Track The Four Golden Signals:
///   - Latency (request duration)
///   - Traffic (request rate)
///   - Errors (error rate)
///   - Saturation (resource usage)
/// ✓ Use appropriate metric types
/// ✓ Add labels for dimensions
/// ✓ Don't have too many label values (cardinality explosion)
/// 
/// HEALTH CHECKS:
/// ✓ Implement /health endpoints
/// ✓ Separate liveness vs readiness
/// ✓ Check critical dependencies
/// ✓ Keep checks fast (<1s)
/// ✓ Return proper HTTP status codes
/// 
/// ALERTING:
/// ✓ Alert on SLO violations
/// ✓ Meaningful thresholds
/// ✓ Include context in alerts
/// ✓ Avoid alert fatigue
/// ✓ Test alert rules


fn main() {
    println!("=== RUST OBSERVABILITY ===\n");
    println!("This file demonstrates observability patterns.");
    println!("See comments for complete examples.\n");
    
    println!("THREE PILLARS OF OBSERVABILITY:");
    println!("  1. LOGS: Discrete events");
    println!("  2. METRICS: Numerical measurements");
    println!("  3. TRACES: Request flow through system");
    
    println!("\nLOGGING:");
    println!("  • log crate: Simple facade");
    println!("  • env_logger: Basic implementation");
    println!("  • tracing: Structured, async-aware");
    
    println!("\nMETRICS:");
    println!("  • prometheus crate: Metrics collection");
    println!("  • Counter: Monotonic increase");
    println!("  • Gauge: Up and down");
    println!("  • Histogram: Distribution");
    
    println!("\nTRACING:");
    println!("  • OpenTelemetry: Standard");
    println!("  • Jaeger: Visualization");
    println!("  • Spans: Time periods");
    println!("  • Context propagation");
    
    println!("\nHEALTH CHECKS:");
    println!("  • Liveness: Is app running?");
    println!("  • Readiness: Can app serve traffic?");
    println!("  • Check dependencies");
    
    println!("\n=== Complete ===");
}

/// DEPENDENCIES:
/// ```toml
/// [dependencies]
/// # Logging
/// log = "0.4"
/// env_logger = "0.10"
/// 
/// # Tracing
/// tracing = "0.1"
/// tracing-subscriber = { version = "0.3", features = ["json", "env-filter"] }
/// tracing-opentelemetry = "0.21"
/// opentelemetry = "0.21"
/// opentelemetry-jaeger = "0.20"
/// 
/// # Metrics
/// prometheus = "0.13"
/// 
/// # Async runtime
/// tokio = { version = "1", features = ["full"] }
/// 
/// # Web framework (for metrics/health endpoints)
/// axum = "0.7"
/// ```

/// ENVIRONMENT VARIABLES:
/// - RUST_LOG=debug - Set log level
/// - RUST_LOG=myapp=trace,sqlx=info - Per-module levels
/// - OTEL_EXPORTER_JAEGER_ENDPOINT - Jaeger endpoint
/// - OTEL_SERVICE_NAME - Service name for tracing

/// KEY TAKEAWAYS:
/// 
/// 1. Use tracing crate for structured, async-aware logging
/// 2. Add #[instrument] to important functions
/// 3. Create spans for significant operations
/// 4. Expose Prometheus metrics on /metrics
/// 5. Track The Four Golden Signals
/// 6. Implement health check endpoints
/// 7. Use OpenTelemetry for distributed tracing
/// 8. Configure via environment variables
/// 9. Never log sensitive data
/// 10. Test observability in development
/// 11. Set up dashboards (Grafana)
/// 12. Alert on anomalies
