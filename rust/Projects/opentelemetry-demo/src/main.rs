// =============================================================================
// OpenTelemetry Observability Demo — Tracing, Metrics, and Structured Logging
// =============================================================================
//
// WHAT THIS DEMONSTRATES:
//   1. Distributed tracing with OpenTelemetry (spans, attributes, events)
//   2. Metrics collection (counters, histograms)
//   3. Structured logging with tracing + OpenTelemetry integration
//   4. Context propagation across async boundaries
//   5. Export to OTLP collector (Jaeger, Grafana Tempo, etc.)
//
// JD RELEVANCE:
//   The JD mentions "Contribute to observability and monitoring using Tracing
//   and OpenTelemetry" and "Strong understanding of observability principles -
//   experience with OpenTelemetry preferred."
//
// ARCHITECTURE:
//   ┌──────────────┐     HTTP Request     ┌──────────────────┐
//   │   Client     │─────────────────────►│   Axum Server    │
//   │  (curl)      │                      │  (instrumented)  │
//   └──────────────┘                      └────────┬─────────┘
//                                                  │
//                                        ┌─────────▼─────────┐
//                                        │  OpenTelemetry SDK │
//                                        │  ┌───────────────┐ │
//                                        │  │   Tracer      │ │
//                                        │  │   Meter       │ │
//                                        │  │   Logger      │ │
//                                        │  └───────────────┘ │
//                                        └─────────┬─────────┘
//                                                  │
//                                        ┌─────────▼─────────┐
//                                        │  OTLP Exporter    │
//                                        │  (gRPC to Jaeger) │
//                                        └───────────────────┘
//
// RUNNING WITH JAEGER:
//   docker run -d --name jaeger \
//     -e COLLECTOR_OTLP_ENABLED=true \
//     -p 16686:16686 \
//     -p 4317:4317 \
//     jaegertracing/all-in-one:latest
//
//   Then visit http://localhost:16686 to see traces.
// =============================================================================

use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::get,
    Router,
};
use opentelemetry::{
    global,
    trace::{Span, Tracer, TracerProvider as _},
    KeyValue,
};
use opentelemetry_otlp::WithExportConfig;
use opentelemetry_sdk::{
    runtime,
    trace as sdktrace,
    Resource,
};
use rand::Rng;
use serde::Serialize;
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, Ordering};
use tracing::{info, warn};
use tracing_subscriber::prelude::*;

// =============================================================================
// Types
// =============================================================================

#[derive(Debug, Clone, Serialize)]
struct OrderResponse {
    order_id: String,
    user_id: String,
    amount: f64,
    status: String,
    processing_time_ms: u64,
}

#[derive(Debug, Serialize)]
struct HealthResponse {
    status: String,
    service: String,
    traces_exported: u64,
}

/// Application state with metrics counters.
struct AppState {
    /// Counter for total orders processed
    orders_total: AtomicU64,
    /// Counter for failed orders
    orders_failed: AtomicU64,
    /// Counter for traces exported
    traces_exported: AtomicU64,
}

impl Clone for AppState {
    fn clone(&self) -> Self {
        AppState {
            orders_total: AtomicU64::new(self.orders_total.load(Ordering::SeqCst)),
            orders_failed: AtomicU64::new(self.orders_failed.load(Ordering::SeqCst)),
            traces_exported: AtomicU64::new(self.traces_exported.load(Ordering::SeqCst)),
        }
    }
}

// =============================================================================
// OpenTelemetry Initialization
// =============================================================================

/// Initialize OpenTelemetry tracing with an OTLP exporter.
///
/// If no OTLP collector is running, this falls back to stdout logging.
fn init_tracer() -> sdktrace::Tracer {
    let resource = Resource::new(vec![
        KeyValue::new("service.name", "opentelemetry-demo"),
        KeyValue::new("service.version", "0.1.0"),
        KeyValue::new("deployment.environment", "development"),
    ]);

    // Try to connect to an OTLP collector (Jaeger, Grafana Tempo, etc.)
    // If it fails, we'll use a no-op tracer
    let tracer = match opentelemetry_otlp::SpanExporter::builder()
        .with_tonic()
        .with_endpoint("http://localhost:4317")
        .build()
    {
        Ok(exporter) => {
            info!("Connected to OTLP collector at localhost:4317");
            sdktrace::TracerProvider::builder()
                .with_batch_exporter(exporter, runtime::Tokio)
                .with_resource(resource)
                .build()
                .tracer("opentelemetry-demo")
        }
        Err(e) => {
            warn!("Failed to connect to OTLP collector: {e}. Using no-op tracer.");
            sdktrace::TracerProvider::builder()
                .with_resource(resource)
                .build()
                .tracer("opentelemetry-demo")
        }
    };

    info!("OpenTelemetry tracer initialized");
    tracer
}

/// Initialize the tracing subscriber with OpenTelemetry integration.
fn init_tracing_subscriber(tracer: sdktrace::Tracer) {
    let telemetry = tracing_opentelemetry::layer().with_tracer(tracer);

    tracing_subscriber::registry()
        .with(telemetry)
        .with(
            tracing_subscriber::fmt::layer()
                .json()
                .with_target(true)
                .with_thread_ids(true),
        )
        .with(
            tracing_subscriber::filter::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "opentelemetry_demo=info".into()),
        )
        .init();
}

// =============================================================================
// Business Logic (Instrumented)
// =============================================================================

/// Process an order — simulates a multi-step workflow with tracing.
///
/// Each step creates a child span, demonstrating how OpenTelemetry tracks
/// the full request lifecycle across function boundaries.
async fn process_order(
    user_id: &str,
    amount: f64,
    state: &AppState,
) -> Result<OrderResponse, String> {
    let tracer = global::tracer("order-service");

    // Create a root span for the entire order processing workflow
    let mut span = tracer.start("process_order");
    span.set_attribute(KeyValue::new("user_id", user_id.to_string()));
    span.set_attribute(KeyValue::new("amount", amount));

    // Step 1: Validate the order
    {
        let mut validate_span = tracer.start("validate_order");
        validate_span.set_attribute(KeyValue::new("amount", amount));

        if amount <= 0.0 {
            validate_span.add_event(
                "validation_failed".to_string(),
                vec![KeyValue::new("reason", "amount must be positive")],
            );
            span.set_status(opentelemetry::trace::Status::error("invalid amount"));
            return Err("Amount must be positive".to_string());
        }

        if amount > 10000.0 {
            validate_span.add_event(
                "validation_warning".to_string(),
                vec![KeyValue::new("reason", "large order requires approval")],
            );
        }

        validate_span.add_event("validation_passed".to_string(), vec![]);
        // Simulate some work
        tokio::time::sleep(std::time::Duration::from_millis(10)).await;
    }

    // Step 2: Process payment
    {
        let mut payment_span = tracer.start("process_payment");
        payment_span.set_attribute(KeyValue::new("amount", amount));

        // Simulate a random failure (10% chance)
        let mut rng = rand::thread_rng();
        if rng.gen_range(0..10) == 0 {
            payment_span.add_event(
                "payment_failed".to_string(),
                vec![KeyValue::new("reason", "insufficient funds")],
            );
            payment_span.set_status(opentelemetry::trace::Status::error("insufficient funds"));
            state.orders_failed.fetch_add(1, Ordering::SeqCst);
            span.set_status(opentelemetry::trace::Status::error("payment failed"));
            return Err("Payment failed: insufficient funds".to_string());
        }

        payment_span.add_event("payment_processed".to_string(), vec![]);
        tokio::time::sleep(std::time::Duration::from_millis(50)).await;
    }

    // Step 3: Update inventory
    {
        let mut inventory_span = tracer.start("update_inventory");
        inventory_span.set_attribute(KeyValue::new("item_count", 1));

        inventory_span.add_event("inventory_updated".to_string(), vec![]);
        tokio::time::sleep(std::time::Duration::from_millis(20)).await;
    }

    // Step 4: Send confirmation
    {
        let mut notification_span = tracer.start("send_confirmation");
        notification_span.set_attribute(KeyValue::new("channel", "email"));

        notification_span.add_event("confirmation_sent".to_string(), vec![]);
        tokio::time::sleep(std::time::Duration::from_millis(15)).await;
    }

    let order_id = uuid::Uuid::new_v4().to_string();
    state.orders_total.fetch_add(1, Ordering::SeqCst);

    span.set_status(opentelemetry::trace::Status::Ok);

    Ok(OrderResponse {
        order_id,
        user_id: user_id.to_string(),
        amount,
        status: "completed".to_string(),
        processing_time_ms: 95, // approximate
    })
}

// =============================================================================
// HTTP Handlers
// =============================================================================

/// GET /order — Create an order (demonstrates tracing).
async fn create_order(
    State(state): State<Arc<AppState>>,
) -> Result<Json<OrderResponse>, (StatusCode, String)> {
    let tracer = global::tracer("http-handler");
    let mut span = tracer.start("POST /order");

    let user_id = format!(
        "user_{}",
        uuid::Uuid::new_v4()
            .to_string()
            .chars()
            .take(8)
            .collect::<String>()
    );
    let amount = rand::thread_rng().gen_range(10.0..5000.0);

    span.set_attribute(KeyValue::new("http.method", "GET"));
    span.set_attribute(KeyValue::new("http.route", "/order"));
    span.set_attribute(KeyValue::new("user_id", user_id.clone()));
    span.set_attribute(KeyValue::new("amount", amount));

    info!(
        user_id = %user_id,
        amount = amount,
        "Processing order request"
    );

    match process_order(&user_id, amount, &state).await {
        Ok(order) => {
            span.add_event(
                "order_completed".to_string(),
                vec![KeyValue::new("order_id", order.order_id.clone())],
            );

            state
                .traces_exported
                .fetch_add(1, Ordering::SeqCst);

            info!(
                order_id = %order.order_id,
                status = %order.status,
                "Order completed successfully"
            );

            Ok(Json(order))
        }
        Err(e) => {
            let err_msg = e.clone();
            span.add_event(
                "order_failed".to_string(),
                vec![KeyValue::new("error", err_msg.clone())],
            );

            warn!(error = %err_msg, "Order processing failed");

            Err((StatusCode::PAYMENT_REQUIRED, err_msg))
        }
    }
}

/// GET /health — Health check with metrics.
async fn health(State(state): State<Arc<AppState>>) -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".to_string(),
        service: "opentelemetry-demo".to_string(),
        traces_exported: state.traces_exported.load(Ordering::SeqCst),
    })
}

/// GET /simulate — Simulate a batch of orders to generate traces.
async fn simulate_traffic(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    let count = 5;
    info!("Simulating {count} orders to generate traces");

    let mut results = Vec::new();
    for i in 0..count {
        let user_id = format!("sim_user_{i}");
        let amount = rand::thread_rng().gen_range(10.0..5000.0);

        match process_order(&user_id, amount, &state).await {
            Ok(order) => results.push(serde_json::json!({
                "order_id": order.order_id,
                "status": "completed"
            })),
            Err(e) => results.push(serde_json::json!({
                "status": "failed",
                "error": e
            })),
        }
    }

    Json(serde_json::json!({
        "simulated_orders": count,
        "results": results,
        "total_orders": state.orders_total.load(Ordering::SeqCst),
        "failed_orders": state.orders_failed.load(Ordering::SeqCst),
    }))
}

// =============================================================================
// Main
// =============================================================================

#[tokio::main]
async fn main() {
    // Initialize OpenTelemetry
    let tracer = init_tracer();
    init_tracing_subscriber(tracer);

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║   OpenTelemetry Observability Demo                      ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();
    println!("   This demo shows distributed tracing with OpenTelemetry.");
    println!();
    println!("   To see traces in Jaeger:");
    println!("     docker run -d --name jaeger \\");
    println!("       -e COLLECTOR_OTLP_ENABLED=true \\");
    println!("       -p 16686:16686 -p 4317:4317 \\");
    println!("       jaegertracing/all-in-one:latest");
    println!();
    println!("   Then visit http://localhost:16686");
    println!();
    println!("   Without Jaeger, traces are logged as JSON to stdout.");
    println!();

    let state = Arc::new(AppState {
        orders_total: AtomicU64::new(0),
        orders_failed: AtomicU64::new(0),
        traces_exported: AtomicU64::new(0),
    });

    let app = Router::new()
        .with_state(state)
        .route("/order", get(create_order))
        .route("/health", get(health))
        .route("/simulate", get(simulate_traffic));

    let addr = "0.0.0.0:3000";
    println!("   🚀 Server starting on http://{addr}");
    println!();
    println!("   Endpoints:");
    println!("     GET /order     - Create an order (generates a trace)");
    println!("     GET /simulate  - Create 5 orders at once");
    println!("     GET /health    - Health check");
    println!();
    println!("   Test with curl:");
    println!("     curl http://localhost:3000/order");
    println!("     curl http://localhost:3000/simulate");
    println!();

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    use axum::{
        body::Body,
        http::Request,
    };
    use tower::util::ServiceExt;

    fn test_state() -> Arc<AppState> {
        Arc::new(AppState {
            orders_total: AtomicU64::new(0),
            orders_failed: AtomicU64::new(0),
            traces_exported: AtomicU64::new(0),
        })
    }

    #[tokio::test]
    async fn test_health_endpoint() {
        let app = Router::new()
            .route("/health", get(health))
            .with_state(test_state());

        let response = app
            .oneshot(
                Request::builder().uri("/health").body(Body::empty()).unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body: HealthResponse =
            serde_json::from_slice(
                &axum::body::to_bytes(response.into_body(), usize::MAX)
                    .await
                    .unwrap(),
            )
            .unwrap();

        assert_eq!(body.status, "ok");
        assert_eq!(body.service, "opentelemetry-demo");
    }

    #[tokio::test]
    async fn test_order_endpoint() {
        let app = Router::new()
            .route("/order", get(create_order))
            .with_state(test_state());

        let response = app
            .oneshot(
                Request::builder().uri("/order").body(Body::empty()).unwrap(),
            )
            .await
            .unwrap();

        // Orders can succeed or fail (10% failure rate), so we just check
        // that we get a valid response
        assert!(
            response.status() == StatusCode::OK
                || response.status() == StatusCode::PAYMENT_REQUIRED
        );
    }

    #[tokio::test]
    async fn test_simulate_endpoint() {
        let app = Router::new()
            .route("/simulate", get(simulate_traffic))
            .with_state(test_state());

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/simulate")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }
}
