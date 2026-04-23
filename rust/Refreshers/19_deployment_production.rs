//// RUST DEPLOYMENT AND PRODUCTION
/// Comprehensive guide to deploying Rust applications to production
/// Covers Docker, Kubernetes, configuration, monitoring, and best practices

// ============================================================================
// 1. BUILDING FOR PRODUCTION
// ============================================================================

/// RELEASE BUILD:
/// cargo build --release
/// 
/// Benefits:
/// - Optimizations enabled
/// - Debug symbols removed (smaller binary)
/// - Much faster runtime (10-100x)
/// - Located in target/release/
/// 
/// Build profiles in Cargo.toml:
/// ```toml
/// [profile.release]
/// opt-level = 3        # Maximum optimization
/// lto = true           # Link-time optimization
/// codegen-units = 1    # Single codegen unit (slower build, faster runtime)
/// strip = true         # Remove debug symbols
/// panic = 'abort'      # Don't unwind on panic
/// ```

/// CROSS-COMPILATION:
/// Build for different targets
/// 
/// ```bash
/// # Install target
/// rustup target add x86_64-unknown-linux-musl
/// 
/// # Build for target
/// cargo build --release --target x86_64-unknown-linux-musl
/// ```
/// 
/// Common targets:
/// - x86_64-unknown-linux-gnu (Linux glibc)
/// - x86_64-unknown-linux-musl (Linux static)
/// - x86_64-pc-windows-gnu (Windows)
/// - x86_64-apple-darwin (macOS)
/// - aarch64-unknown-linux-gnu (ARM64 Linux)


// ============================================================================
// 2. DOCKER CONTAINERIZATION
// ============================================================================

/// MULTI-STAGE DOCKERFILE:
/// Builds small production image

/*
# Dockerfile

# Stage 1: Build
FROM rust:1.75 as builder

WORKDIR /app

# Copy manifests
COPY Cargo.toml Cargo.lock ./

# Create dummy source to cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Copy actual source
COPY src ./src

# Build for release (dependencies cached)
RUN cargo build --release

# Stage 2: Runtime
FROM debian:bookworm-slim

# Install runtime dependencies if needed
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

EXPOSE 8080

CMD ["myapp"]
*/

/// ALPINE-BASED (MUSL):
/// Even smaller image
/*
# Stage 1: Build with musl
FROM rust:1.75-alpine as builder

RUN apk add --no-cache musl-dev

WORKDIR /app
COPY . .

RUN cargo build --release --target x86_64-unknown-linux-musl

# Stage 2: Minimal runtime
FROM alpine:latest

RUN apk add --no-cache ca-certificates

COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/myapp /usr/local/bin/

CMD ["myapp"]
*/

/// DISTROLESS IMAGE:
/// Google's distroless images (no shell, minimal attack surface)
/*
FROM gcr.io/distroless/cc-debian12

COPY --from=builder /app/target/release/myapp /

CMD ["/myapp"]
*/

/// BUILD AND RUN:
/// ```bash
/// docker build -t myapp:latest .
/// docker run -p 8080:8080 myapp:latest
/// ```


// ============================================================================
// 3. KUBERNETES DEPLOYMENT
// ============================================================================

/// KUBERNETES MANIFESTS:

/*
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: RUST_LOG
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
*/


// ============================================================================
// 4. CONFIGURATION MANAGEMENT
// ============================================================================

/// Use config crate for layered configuration

/*
use config::{Config, ConfigError, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Settings {
    pub server: ServerConfig,
    pub database: DatabaseConfig,
    pub redis: RedisConfig,
}

#[derive(Debug, Deserialize)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
}

#[derive(Debug, Deserialize)]
pub struct DatabaseConfig {
    pub url: String,
    pub max_connections: u32,
}

#[derive(Debug, Deserialize)]
pub struct RedisConfig {
    pub url: String,
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        Config::builder()
            // Start with default config
            .add_source(File::with_name("config/default"))
            // Override with environment-specific config
            .add_source(
                File::with_name(&format!("config/{}", 
                    std::env::var("ENV").unwrap_or_else(|_| "development".into())
                ))
                .required(false)
            )
            // Override with environment variables (prefix: APP_)
            .add_source(Environment::with_prefix("APP").separator("__"))
            .build()?
            .try_deserialize()
    }
}

// Usage:
// let settings = Settings::new().expect("Failed to load config");
// println!("Server: {}:{}", settings.server.host, settings.server.port);
*/

/// CONFIG FILE STRUCTURE:
/// ```
/// config/
/// ├── default.toml       # Default settings
/// ├── development.toml   # Development overrides
/// ├── production.toml    # Production overrides
/// └── test.toml          # Test overrides
/// ```
///
/// Environment variable override:
/// APP__SERVER__PORT=9000 cargo run


// ============================================================================
// 5. GRACEFUL SHUTDOWN
// ============================================================================

/*
use tokio::signal;
use tokio::sync::broadcast;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {
            info!("Received Ctrl+C signal");
        },
        _ = terminate => {
            info!("Received terminate signal");
        },
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Setup
    let pool = create_pool().await?;
    let app = create_router(pool);
    
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    
    info!("Server listening on 0.0.0.0:8080");
    
    // Run server with graceful shutdown
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    
    info!("Server shutdown complete");
    
    Ok(())
}
*/


// ============================================================================
// 6. MONITORING AND ALERTING
// ============================================================================

/// MONITORING STACK:
/// 
/// 1. PROMETHEUS:
///    - Metrics collection
///    - Time-series database
///    - PromQL query language
/// 
/// 2. GRAFANA:
///    - Visualization
///    - Dashboards
///    - Alerting
/// 
/// 3. ALERTMANAGER:
///    - Alert routing
///    - Grouping
///    - Notifications

/// PROMETHEUS CONFIGURATION:
/*
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
*/

/// EXAMPLE QUERIES (PromQL):
/// - rate(http_requests_total[5m]) - Request rate
/// - histogram_quantile(0.95, http_request_duration_seconds) - p95 latency
/// - up{job="myapp"} - Service up/down


// ============================================================================
// 7. BEST PRACTICES
// ============================================================================

/// DEPLOYMENT BEST PRACTICES:
/// 
/// CONTAINER IMAGE:
/// ✓ Multi-stage builds (small image)
/// ✓ Non-root user
/// ✓ Distroless or Alpine base
/// ✓ Pin base image versions
/// ✓ Scan for vulnerabilities
/// ✓ Sign images
/// 
/// CONFIGURATION:
/// ✓ 12-factor app principles
/// ✓ Environment variables for config
/// ✓ Secrets in secret management (Vault, K8s Secrets)
/// ✓ Configuration validation at startup
/// ✗ Don't commit secrets
/// 
/// KUBERNETES:
/// ✓ Resource limits (CPU, memory)
/// ✓ Liveness and readiness probes
/// ✓ Rolling updates
/// ✓ Horizontal Pod Autoscaler
/// ✓ Network policies
/// ✓ Use namespaces
/// 
/// MONITORING:
/// ✓ Expose metrics endpoint
/// ✓ Structured logging
/// ✓ Distributed tracing
/// ✓ Error tracking (Sentry)
/// ✓ Uptime monitoring
/// ✓ Alert on SLO violations
/// 
/// SECURITY:
/// ✓ Run as non-root user
/// ✓ Minimal base image
/// ✓ No secrets in code/images
/// ✓ TLS for all connections
/// ✓ Security scanning
/// ✓ Least privilege
/// 
/// RELIABILITY:
/// ✓ Graceful shutdown
/// ✓ Health checks
/// ✓ Circuit breakers
/// ✓ Retry logic
/// ✓ Timeout on all I/O
/// ✓ Connection pooling
/// 
/// SCALABILITY:
/// ✓ Stateless services
/// ✓ Horizontal scaling
/// ✓ Database connection pooling
/// ✓ Caching (Redis)
/// ✓ Load balancing
/// ✓ CDN for static assets

/// RUST-SPECIFIC OPTIMIZATIONS:
/// 
/// 1. RELEASE PROFILE:
///    - Enable LTO (link-time optimization)
///    - Single codegen unit
///    - Strip symbols
/// 
/// 2. BINARY SIZE:
///    - Use musl target for static linking
///    - Strip with strip command
///    - Use upx for compression (careful with performance)
/// 
/// 3. STARTUP TIME:
///    - Lazy initialization
///    - Reduce dependencies
///    - Profile startup
/// 
/// 4. MEMORY:
///    - Use appropriate data structures
///    - Avoid unnecessary allocations
///    - Profile memory usage
/// 
/// 5. CPU:
///    - Use release builds
///    - Profile with flamegraph
///    - Optimize hot paths

/// DEPLOYMENT CHECKLIST:
/// 
/// Before deploying:
/// ☐ All tests pass (cargo test)
/// ☐ No clippy warnings (cargo clippy)
/// ☐ Code formatted (cargo fmt)
/// ☐ Dependencies audited (cargo audit)
/// ☐ Release build tested
/// ☐ Configuration validated
/// ☐ Secrets secured
/// ☐ Documentation updated
/// ☐ Monitoring configured
/// ☐ Alerts set up
/// ☐ Rollback plan ready
/// ☐ Load tested
/// ☐ Security scanned
/// ☐ Backup strategy in place

/// EXAMPLE: COMPLETE PRODUCTION SETUP
/*
use axum::{Router, routing::get};
use sqlx::PgPool;
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Setup tracing
    setup_tracing();
    
    // 2. Load configuration
    let settings = Settings::new()?;
    info!("Configuration loaded");
    
    // 3. Connect to database
    let pool = create_pool(&settings.database.url).await?;
    run_migrations(&pool).await?;
    info!("Database connected");
    
    // 4. Setup Redis
    let redis_client = redis::Client::open(settings.redis.url)?;
    info!("Redis connected");
    
    // 5. Create application
    let app = Router::new()
        .route("/", get(|| async { "OK" }))
        .route("/health/live", get(liveness))
        .route("/health/ready", get(readiness))
        .route("/metrics", get(metrics_handler))
        .layer(TraceLayer::new_for_http())
        .with_state(AppState { pool, redis_client });
    
    // 6. Start server
    let addr = format!("{}:{}", settings.server.host, settings.server.port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    
    info!("Server starting on {}", addr);
    
    // 7. Run with graceful shutdown
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;
    
    info!("Server shutdown complete");
    
    Ok(())
}

async fn run_migrations(pool: &PgPool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations")
        .run(pool)
        .await?;
    Ok(())
}
*/


// ============================================================================
// 3. ENVIRONMENT-SPECIFIC CONFIGURATION
// ============================================================================

/// CONFIG FILES:
/*
# config/default.toml
[server]
host = "0.0.0.0"
port = 8080

[database]
max_connections = 10

[logging]
level = "info"

# config/production.toml
[server]
port = 80

[database]
max_connections = 20

[logging]
level = "warn"
*/


// ============================================================================
// 4. SECRET MANAGEMENT
// ============================================================================

/// NEVER COMMIT SECRETS!
/// 
/// Options for secret management:
/// 
/// 1. ENVIRONMENT VARIABLES:
///    - Simple, widely supported
///    - export SECRET_KEY="xyz"
/// 
/// 2. .ENV FILES (development only):
///    - Use dotenv crate
///    - Add .env to .gitignore
/// 
/// 3. KUBERNETES SECRETS:
///    - kubectl create secret generic db-secret --from-literal=url=postgres://...
///    - Mount as env vars or files
/// 
/// 4. HASHICORP VAULT:
///    - Centralized secret management
///    - Dynamic secrets
///    - Audit logging
/// 
/// 5. AWS SECRETS MANAGER / AZURE KEY VAULT:
///    - Cloud-native secret management
///    - Rotation support

/*
use std::env;

fn load_secrets() -> Result<Secrets, ConfigError> {
    // Load from environment
    let database_url = env::var("DATABASE_URL")
        .map_err(|_| ConfigError::MissingDatabaseUrl)?;
    
    let api_key = env::var("API_KEY")
        .map_err(|_| ConfigError::MissingApiKey)?;
    
    Ok(Secrets {
        database_url,
        api_key,
    })
}
*/


// ============================================================================
// 5. LOGGING IN PRODUCTION
// ============================================================================

/// PRODUCTION LOGGING SETUP:

/*
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn setup_tracing() {
    tracing_subscriber::registry()
        // Environment filter
        .with(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into())
        )
        // JSON output for log aggregation
        .with(
            tracing_subscriber::fmt::layer()
                .json()
                .with_current_span(false)
        )
        .init();
}
*/

/// SEND LOGS TO:
/// - Stdout/stderr (captured by container runtime)
/// - Log aggregation (ELK, Datadog, CloudWatch)
/// - Never log to local files in containers


// ============================================================================
// 6. DEPLOYMENT STRATEGIES
// ============================================================================

/// DEPLOYMENT STRATEGIES:
/// 
/// 1. ROLLING UPDATE (Default K8s):
///    - Update pods gradually
///    - Zero downtime
///    - Easy rollback
/// 
/// 2. BLUE-GREEN:
///    - Two identical environments
///    - Switch traffic instantly
///    - Easy rollback
///    - Doubles infrastructure
/// 
/// 3. CANARY:
///    - Deploy to small percentage
///    - Monitor metrics
///    - Gradually increase
///    - Rollback if issues
/// 
/// 4. A/B TESTING:
///    - Multiple versions simultaneously
///    - Route based on criteria
///    - Compare metrics


// ============================================================================
// 7. MONITORING IN PRODUCTION
// ============================================================================

/// WHAT TO MONITOR:
/// 
/// APPLICATION METRICS:
/// - Request rate, latency, errors (RED method)
/// - Saturation (CPU, memory, connections)
/// - Business metrics (signups, orders)
/// 
/// INFRASTRUCTURE METRICS:
/// - CPU usage
/// - Memory usage
/// - Disk I/O
/// - Network I/O
/// - Pod restarts
/// 
/// DATABASE METRICS:
/// - Query performance
/// - Connection pool usage
/// - Slow queries
/// - Replication lag
/// 
/// ALERTS:
/// - Error rate > threshold
/// - Latency p95 > threshold
/// - Service down
/// - Database connection issues
/// - Memory usage > 80%
/// - Certificate expiration


// ============================================================================
// 8. BEST PRACTICES SUMMARY
// ============================================================================

fn main() {
    println!("=== RUST DEPLOYMENT & PRODUCTION ===\n");
    
    println!("BUILD:");
    println!("  ✓ cargo build --release");
    println!("  ✓ Enable LTO and optimizations");
    println!("  ✓ Strip debug symbols");
    println!("  ✓ Consider musl for static linking");
    
    println!("\nDOCKER:");
    println!("  ✓ Multi-stage builds");
    println!("  ✓ Minimal base image (Alpine/Distroless)");
    println!("  ✓ Non-root user");
    println!("  ✓ Cache dependencies");
    
    println!("\nKUBERNETES:");
    println!("  ✓ Resource limits");
    println!("  ✓ Health probes");
    println!("  ✓ Rolling updates");
    println!("  ✓ Horizontal autoscaling");
    
    println!("\nCONFIGURATION:");
    println!("  ✓ Environment variables");
    println!("  ✓ Layered config files");
    println!("  ✓ Secret management");
    println!("  ✓ Validate at startup");
    
    println!("\nOBSERVABILITY:");
    println!("  ✓ Structured logging (JSON)");
    println!("  ✓ Prometheus metrics");
    println!("  ✓ Distributed tracing");
    println!("  ✓ Health checks");
    
    println!("\nSECURITY:");
    println!("  ✓ No secrets in code");
    println!("  ✓ Run as non-root");
    println!("  ✓ Scan for vulnerabilities");
    println!("  ✓ TLS everywhere");
    
    println!("\n=== Complete ===");
}

/// KEY TAKEAWAYS:
/// 
/// 1. Build with --release and optimizations
/// 2. Use multi-stage Docker builds for small images
/// 3. Deploy to Kubernetes with proper resources
/// 4. Layer configuration (files → env vars)
/// 5. Manage secrets securely (never commit)
/// 6. Implement graceful shutdown
/// 7. Export metrics for Prometheus
/// 8. Structured JSON logging
/// 9. Health check endpoints (liveness, readiness)
/// 10. Monitor The Four Golden Signals
/// 11. Set up alerts for critical issues
/// 12. Test thoroughly before deployment
/// 
/// DEPENDENCIES:
/// ```toml
/// [dependencies]
/// tokio = { version = "1", features = ["full"] }
/// axum = "0.7"
/// sqlx = { version = "0.7", features = ["postgres", "runtime-tokio-rustls"] }
/// redis = "0.24"
/// config = "0.13"
/// serde = { version = "1", features = ["derive"] }
/// tracing = "0.1"
/// tracing-subscriber = { version = "0.3", features = ["json"] }
/// prometheus = "0.13"
/// tower-http = { version = "0.5", features = ["trace"] }
/// ```
