//// Build on 'tower' ecosystem, follow Rust more closely, official Tokio project, more explicit
/// Tower is a lib for building robust network clients and servers, uses the Service and Layer Traits
use axum::{
    routing::{get, post},
    Router, extract::{State, Path, Query, Json},
    response::{Html, IntoResponse},
    http::StatusCode,
    middleware,
};
use std::sync::Arc;
use tokio::sync::RwLock;
use serde::{Deserialize, Serialize};
use tower_http::{trace::TraceLayer, compression::CompressionLayer};

// Application state
#[derive(Clone)]
struct AppState {
    counter: Arc<RwLock<i32>>,
    db_pool: DatabasePool, // Hypothetical DB connection pool
}

// Custom extractor for authentication
struct AuthenticatedUser {
    user_id: String,
    role: String,
}

impl AuthenticatedUser {
    async fn from_request(req: &mut axum::http::Request<axum::body::Body>) -> Result<Self, StatusCode> {
        // Extract and validate auth token
        let auth_header = req.headers()
            .get("Authorization")
            .and_then(|h| h.to_str().ok())
            .ok_or(StatusCode::UNAUTHORIZED)?;
            
        // Validate token (simplified)
        if auth_header.starts_with("Bearer ") {
            Ok(AuthenticatedUser {
                user_id: "user123".to_string(),
                role: "admin".to_string(),
            })
        } else {
            Err(StatusCode::UNAUTHORIZED)
        }
    }
}

#[tokio::main]
async fn main() {
    // Setup tracing
    tracing_subscriber::fmt::init();
    
    let shared_state = AppState {
        counter: Arc::new(RwLock::new(0)),
        db_pool: DatabasePool::new(), // Hypothetical
    };
    
    // Build our application with layers (middleware) and routes
    let app = Router::new()
        .route("/", get(root_handler))
        .route("/api/count", get(get_count).post(increment_count))
        .route("/api/users/:id", get(get_user))
        .route("/api/protected", get(protected_route))
        .route("/api/upload", post(upload_file))
        .layer(CompressionLayer::new())
        .layer(TraceLayer::new_for_http())
        .layer(middleware::from_fn(auth_middleware))
        .with_state(shared_state);
    
    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();
    
    tracing::info!("Listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}


//// Routing and Extractors
use axum::{
    extract::{Path, Query, Json, State, FromRequest, Request},
    response::IntoResponse,
    Router, routing::get,
    async_trait,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// Custom extractor with trait implementation
struct Pagination {
    page: u32,
    per_page: u32,
}

// Manual extractor implementation
#[async_trait]
impl<S> FromRequest<S> for Pagination
where
    S: Send + Sync,
{
    type Rejection = (axum::http::StatusCode, &'static str);
    
    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let query = req.uri().query().unwrap_or("");
        let params: HashMap<String, String> = serde_qs::from_str(query)
            .map_err(|_| (StatusCode::BAD_REQUEST, "Invalid query parameters"))?;
        
        Ok(Pagination {
            page: params.get("page").and_then(|p| p.parse().ok()).unwrap_or(1),
            per_page: params.get("per_page").and_then(|p| p.parse().ok()).unwrap_or(20),
        })
    }
}

// Route handlers
async fn get_user(
    Path(id): Path<u64>,
    pagination: Query<Pagination>,
) -> impl IntoResponse {
    Json(User {
        id,
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    })
}

// Type-safe path parameters
async fn get_user_post(
    Path((user_id, post_id)): Path<(u64, u64)>,
    State(state): State<AppState>,
) -> Result<Json<Post>, StatusCode> {
    // Database query with error handling
    match state.db_pool.get_post(user_id, post_id).await {
        Ok(Some(post)) => Ok(Json(post)),
        Ok(None) => Err(StatusCode::NOT_FOUND),
        Err(_) => Err(StatusCode::INTERNAL_SERVER_ERROR),
    }
}

// JSON extraction with validation
async fn create_user(
    State(state): State<AppState>,
    Json(payload): Json<CreateUser>,
) -> Result<(StatusCode, Json<User>), StatusCode> {
    if payload.name.len() < 3 {
        return Err(StatusCode::BAD_REQUEST);
    }
    
    let user = state.db_pool.create_user(payload).await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok((StatusCode::CREATED, Json(user)))
}


//// Middleware
use axum::{
    Router,
    middleware::{self, Next},
    response::{Response, IntoResponse},
    http::{Request, StatusCode, HeaderValue},
    body::Body,
};
use tower::{ServiceBuilder, Layer};
use tower_http::{
    trace::TraceLayer,
    cors::CorsLayer,
    compression::CompressionLayer,
    classify::StatusInRangeAsFailures,
};
use std::time::Duration;

// Custom middleware function
async fn auth_middleware<B>(
    req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    // Check authentication
    let auth_header = req.headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok());
    
    match auth_header {
        Some(token) if token.starts_with("Bearer ") => {
            // Validate token (simplified)
            let mut req = req;
            // Add user info to request extensions
            req.extensions_mut().insert(AuthenticatedUser {
                user_id: "user123".to_string(),
            });
            Ok(next.run(req).await)
        }
        _ => Err(StatusCode::UNAUTHORIZED),
    }
}

// Metrics middleware using tower::Layer
#[derive(Clone)]
struct MetricsLayer;

impl<S> Layer<S> for MetricsLayer {
    type Service = MetricsMiddleware<S>;

    fn layer(&self, inner: S) -> Self::Service {
        MetricsMiddleware { inner }
    }
}

#[derive(Clone)]
struct MetricsMiddleware<S> {
    inner: S,
}

impl<S, B> tower::Service<Request<B>> for MetricsMiddleware<S>
where
    S: tower::Service<Request<B>>,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = S::Future;

    fn poll_ready(&mut self, cx: &mut std::task::Context<'_>) -> std::task::Poll<Result<(), Self::Error>> {
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Request<B>) -> Self::Future {
        let start = std::time::Instant::now();
        let path = req.uri().path().to_string();
        
        let fut = self.inner.call(req);
        
        Box::pin(async move {
            let res = fut.await?;
            let duration = start.elapsed();
            println!("{} took {:?}", path, duration);
            Ok(res)
        })
    }
}

// Building middleware stack in Axum
fn create_app() -> Router {
    let middleware_stack = ServiceBuilder::new()
        .layer(TraceLayer::new_for_http())
        .layer(CompressionLayer::new())
        .layer(CorsLayer::very_permissive())
        .layer(MetricsLayer)
        .timeout(Duration::from_secs(30))
        .layer(middleware::from_fn(auth_middleware))
        .layer(middleware::from_fn(logging_middleware));
    
    Router::new()
        // Routes here
        .layer(middleware_stack)
}

//// Error Handling
use axum::{
    response::{Response, IntoResponse},
    Json, http::StatusCode,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Validation error: {0}")]
    Validation(String),
    
    #[error("Authentication error")]
    Unauthorized,
    
    #[error("Not found")]
    NotFound,
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_message) = match self {
            AppError::Database(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "Internal server error".to_string(),
            ),
            AppError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Unauthorized => (
                StatusCode::UNAUTHORIZED,
                "Authentication required".to_string(),
            ),
            AppError::NotFound => (
                StatusCode::NOT_FOUND,
                "Resource not found".to_string(),
            ),
        };
        
        let body = Json(json!({
            "error": error_message,
            "code": status.as_u16(),
        }));
        
        (status, body).into_response()
    }
}

// Using Result in handlers
async fn create_user(
    State(pool): State<sqlx::PgPool>,
    Json(payload): Json<CreateUser>,
) -> Result<(StatusCode, Json<User>), AppError> {
    // Validate input
    if payload.name.len() < 3 {
        return Err(AppError::Validation(
            "Name must be at least 3 characters".to_string()
        ));
    }
    
    // Database operation with error conversion
    let user = sqlx::query_as!(
        User,
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        payload.name,
        payload.email
    )
    .fetch_one(&pool)
    .await?; // Automatically converts sqlx::Error to AppError
    
    Ok((StatusCode::CREATED, Json(user)))
}

// Custom error mapper middleware
async fn handle_errors_middleware(
    req: Request<Body>,
    next: Next,
) -> Result<Response, AppError> {
    let response = next.run(req).await;
    
    // Transform any unhandled errors
    let status = response.status();
    if status.is_server_error() {
        Err(AppError::Database(
            sqlx::Error::Protocol("Server error occurred".to_string())
        ))
    } else {
        Ok(response)
    }
}


//// Testing
use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt; // for `oneshot`

#[tokio::test]
async fn test_get_user() {
    let app = create_app(); // Your app builder
    
    let response = app
        .oneshot(
            Request::builder()
                .uri("/users/123")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::OK);
    
    let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let user: User = serde_json::from_slice(&body).unwrap();
    assert_eq!(user.id, 123);
}

#[tokio::test]
async fn test_protected_route() {
    let app = create_app();
    
    // Test without auth
    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/api/protected")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::UNAUTHORIZED);
    
    // Test with auth
    let response = app
        .oneshot(
            Request::builder()
                .uri("/api/protected")
                .header("Authorization", "Bearer valid-token")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    
    assert_eq!(response.status(), StatusCode::OK);
}