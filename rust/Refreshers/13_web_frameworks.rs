//// RUST WEB FRAMEWORKS - ACTIX-WEB AND AXUM
/// This guide covers the two most popular Rust web frameworks:
/// - Actix-web: Mature, feature-rich, actor-based
/// - Axum: Modern, ergonomic, tokio-based from Tower ecosystem

// ============================================================================
// 1. ACTIX-WEB FUNDAMENTALS
// ============================================================================

/// Actix-web is built on the actix actor framework
/// Key concepts:
/// - App: Application instance
/// - HttpServer: Server that listens for connections
/// - Routes: URL patterns mapped to handlers
/// - Extractors: Extract data from requests (path, query, body, etc.)
/// - Middleware: Process requests/responses
/// - State: Shared application data

/*
use actix_web::{web, App, HttpServer, HttpResponse, HttpRequest, Result, Error};
use actix_web::middleware::Logger;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

// ============================================================================
// 2. BASIC ACTIX-WEB APPLICATION
// ============================================================================

/// Simple handler function - returns HttpResponse
async fn index() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok()
        .content_type("text/html")
        .body("<h1>Welcome to Actix-Web!</h1>"))
}

/// Handler with JSON response
#[derive(Serialize)]
struct ApiResponse {
    message: String,
    status: i32,
}

async fn api_index() -> Result<HttpResponse> {
    let response = ApiResponse {
        message: "API is running".to_string(),
        status: 200,
    };
    Ok(HttpResponse::Ok().json(response))
}


// ============================================================================
// 3. ACTIX-WEB EXTRACTORS
// ============================================================================

/// Extractors pull data from the request
/// Common extractors:
/// - web::Path<T>: Extract path parameters
/// - web::Query<T>: Extract query parameters  
/// - web::Json<T>: Parse JSON body
/// - web::Data<T>: Access shared app state
/// - HttpRequest: Access to raw request

// Path parameters
async fn user_detail(path: web::Path<(u32,)>) -> Result<HttpResponse> {
    let user_id = path.into_inner().0;
    Ok(HttpResponse::Ok().body(format!("User ID: {}", user_id)))
}

// Query parameters
#[derive(Deserialize)]
struct SearchQuery {
    q: String,
    page: Option<u32>,
}

async fn search(query: web::Query<SearchQuery>) -> Result<HttpResponse> {
    let page = query.page.unwrap_or(1);
    Ok(HttpResponse::Ok().body(
        format!("Search: {}, Page: {}", query.q, page)
    ))
}

// JSON body
#[derive(Deserialize, Serialize)]
struct CreateUser {
    name: String,
    email: String,
}

async fn create_user(user: web::Json<CreateUser>) -> Result<HttpResponse> {
    // In real app, save to database
    Ok(HttpResponse::Created().json(user.into_inner()))
}

// Multiple extractors
async fn complex_handler(
    path: web::Path<(u32,)>,
    query: web::Query<SearchQuery>,
    body: web::Json<CreateUser>,
) -> Result<HttpResponse> {
    // Can use all extractors in one handler
    Ok(HttpResponse::Ok().body("Complex handler"))
}


// ============================================================================
// 4. ACTIX-WEB STATE MANAGEMENT
// ============================================================================

/// State is shared across handlers using web::Data<T>
/// Must be Clone or Arc/Mutex wrapped

struct AppState {
    counter: Mutex<i32>,
    app_name: String,
}

async fn get_count(data: web::Data<AppState>) -> Result<HttpResponse> {
    let mut counter = data.counter.lock().unwrap();
    *counter += 1;
    Ok(HttpResponse::Ok().body(
        format!("Count: {}, App: {}", counter, data.app_name)
    ))
}


// ============================================================================
// 5. ACTIX-WEB MIDDLEWARE
// ============================================================================

/// Middleware wraps handlers to add functionality
/// Common uses: logging, auth, compression, CORS

use actix_web::middleware::{Compress, DefaultHeaders};
use actix_web::http::header;

// Custom middleware (simplified structure)
/*
use actix_web::dev::{Service, ServiceRequest, ServiceResponse, Transform};
use futures::future::{ok, Ready};

pub struct Authentication;

impl<S, B> Transform<S, ServiceRequest> for Authentication
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error>,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Transform = AuthenticationMiddleware<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;
    
    fn new_transform(&self, service: S) -> Self::Future {
        ok(AuthenticationMiddleware { service })
    }
}
*/


// ============================================================================
// 6. ACTIX-WEB ROUTING
// ============================================================================

/// Routes can be configured using:
/// - service() with route() builders
/// - Direct macros like #[get], #[post]
/// - Scope for grouping routes

use actix_web::{get, post, put, delete};

#[get("/users")]
async fn list_users() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(vec!["Alice", "Bob"]))
}

#[get("/users/{id}")]
async fn get_user(path: web::Path<u32>) -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().body(format!("User {}", path)))
}

#[post("/users")]
async fn create_user_macro(user: web::Json<CreateUser>) -> Result<HttpResponse> {
    Ok(HttpResponse::Created().json(user.into_inner()))
}

#[put("/users/{id}")]
async fn update_user(
    path: web::Path<u32>,
    user: web::Json<CreateUser>,
) -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(user.into_inner()))
}

#[delete("/users/{id}")]
async fn delete_user(path: web::Path<u32>) -> Result<HttpResponse> {
    Ok(HttpResponse::NoContent().finish())
}


// ============================================================================
// 7. ACTIX-WEB ERROR HANDLING
// ============================================================================

/// actix-web provides ResponseError trait for custom errors
use actix_web::error::ResponseError;
use std::fmt;

#[derive(Debug)]
enum ApiError {
    NotFound,
    BadRequest(String),
    InternalError,
}

impl fmt::Display for ApiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ApiError::NotFound => write!(f, "Resource not found"),
            ApiError::BadRequest(msg) => write!(f, "Bad request: {}", msg),
            ApiError::InternalError => write!(f, "Internal server error"),
        }
    }
}

impl ResponseError for ApiError {
    fn status_code(&self) -> actix_web::http::StatusCode {
        match self {
            ApiError::NotFound => actix_web::http::StatusCode::NOT_FOUND,
            ApiError::BadRequest(_) => actix_web::http::StatusCode::BAD_REQUEST,
            ApiError::InternalError => actix_web::http::StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
}

async fn may_fail() -> Result<HttpResponse, ApiError> {
    Err(ApiError::NotFound)
}


// ============================================================================
// 8. ACTIX-WEB COMPLETE APPLICATION
// ============================================================================

#[actix_web::main]
async fn main_actix() -> std::io::Result<()> {
    // Initialize logger
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    
    // Create shared state
    let app_state = web::Data::new(AppState {
        counter: Mutex::new(0),
        app_name: "My API".to_string(),
    });
    
    HttpServer::new(move || {
        App::new()
            // Middleware
            .wrap(Logger::default())
            .wrap(Compress::default())
            .wrap(
                DefaultHeaders::new()
                    .add((header::X_CONTENT_TYPE_OPTIONS, "nosniff"))
            )
            // State
            .app_data(app_state.clone())
            // Routes
            .service(list_users)
            .service(get_user)
            .service(create_user_macro)
            .service(update_user)
            .service(delete_user)
            // Scoped routes
            .service(
                web::scope("/api/v1")
                    .service(api_index)
                    .route("/count", web::get().to(get_count))
            )
            // Catch-all
            .default_service(web::route().to(|| async {
                HttpResponse::NotFound().body("Not Found")
            }))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
*/


// ============================================================================
// 9. AXUM FUNDAMENTALS
// ============================================================================

/// Axum is built on tokio and tower
/// Key concepts:
/// - Router: Route builder using method chaining
/// - Handlers: Async functions with extractors
/// - State: Shared via Extension or State
/// - Middleware: Tower layers and services
/// - Extractors: Similar to actix but different syntax

/*
use axum::{
    Router,
    routing::{get, post},
    http::StatusCode,
    response::{IntoResponse, Response, Json},
    extract::{Path, Query, State},
    middleware::{self, Next},
};
use std::sync::Arc;
use tokio::net::TcpListener;


// ============================================================================
// 10. BASIC AXUM APPLICATION
// ============================================================================

/// Simple handler - returns impl IntoResponse
async fn axum_index() -> &'static str {
    "Welcome to Axum!"
}

/// JSON response
#[derive(Serialize)]
struct AxumApiResponse {
    message: String,
    status: u16,
}

async fn axum_api_index() -> Json<AxumApiResponse> {
    Json(AxumApiResponse {
        message: "Axum API running".to_string(),
        status: 200,
    })
}


// ============================================================================
// 11. AXUM EXTRACTORS
// ============================================================================

/// Axum extractors work similarly but have different API
/// Order matters! Some extractors must come last

// Path parameters
async fn axum_user_detail(Path(user_id): Path<u32>) -> String {
    format!("User ID: {}", user_id)
}

// Multiple path parameters
async fn axum_post_detail(
    Path((user_id, post_id)): Path<(u32, u32)>
) -> String {
    format!("User {} Post {}", user_id, post_id)
}

// Query parameters
#[derive(Deserialize)]
struct AxumSearchQuery {
    q: String,
    page: Option<u32>,
}

async fn axum_search(Query(query): Query<AxumSearchQuery>) -> String {
    let page = query.page.unwrap_or(1);
    format!("Search: {}, Page: {}", query.q, page)
}

// JSON body
#[derive(Deserialize, Serialize)]
struct AxumCreateUser {
    name: String,
    email: String,
}

async fn axum_create_user(
    Json(user): Json<AxumCreateUser>
) -> (StatusCode, Json<AxumCreateUser>) {
    (StatusCode::CREATED, Json(user))
}


// ============================================================================
// 12. AXUM STATE MANAGEMENT
// ============================================================================

/// Axum uses State extractor for shared state
/// State must be Clone

#[derive(Clone)]
struct AxumAppState {
    counter: Arc<Mutex<i32>>,
    app_name: String,
}

async fn axum_get_count(State(state): State<AxumAppState>) -> String {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    format!("Count: {}, App: {}", counter, state.app_name)
}


// ============================================================================
// 13. AXUM RESPONSE TYPES
// ============================================================================

/// Axum handlers can return anything that implements IntoResponse
/// Built-in implementations:
/// - &str, String
/// - Json<T>
/// - StatusCode
/// - (StatusCode, impl IntoResponse)
/// - Result<T, E> where both implement IntoResponse

use axum::http::header;

async fn custom_response() -> Response {
    Response::builder()
        .status(StatusCode::OK)
        .header(header::CONTENT_TYPE, "text/html")
        .body("<h1>Custom Response</h1>".into())
        .unwrap()
}

// Returning Result
async fn may_fail_axum() -> Result<Json<AxumApiResponse>, StatusCode> {
    Ok(Json(AxumApiResponse {
        message: "Success".to_string(),
        status: 200,
    }))
}


// ============================================================================
// 14. AXUM ERROR HANDLING
// ============================================================================

/// Custom error type that implements IntoResponse

#[derive(Debug)]
enum AxumApiError {
    NotFound,
    BadRequest(String),
    InternalError,
}

impl IntoResponse for AxumApiError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AxumApiError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            AxumApiError::BadRequest(ref msg) => (StatusCode::BAD_REQUEST, msg.as_str()),
            AxumApiError::InternalError => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };
        
        (status, message).into_response()
    }
}

async fn axum_handler_with_error() -> Result<String, AxumApiError> {
    Err(AxumApiError::NotFound)
}


// ============================================================================
// 15. AXUM MIDDLEWARE
// ============================================================================

/// Axum middleware uses Tower layers
/// Can be function-based or layer-based

use axum::http::Request;
use axum::body::Body;

// Function middleware
async fn auth_middleware(
    request: Request<Body>,
    next: Next,
) -> Response {
    // Check authentication
    let auth_header = request.headers()
        .get("authorization")
        .and_then(|h| h.to_str().ok());
    
    if auth_header != Some("Bearer secret") {
        return (StatusCode::UNAUTHORIZED, "Unauthorized").into_response();
    }
    
    next.run(request).await
}

// Logging middleware
async fn logging_middleware(
    request: Request<Body>,
    next: Next,
) -> Response {
    let method = request.method().clone();
    let uri = request.uri().clone();
    
    println!("Request: {} {}", method, uri);
    
    let response = next.run(request).await;
    
    println!("Response: {}", response.status());
    
    response
}


// ============================================================================
// 16. AXUM ROUTING
// ============================================================================

/// Axum routing is builder-based with method chaining
/// Supports nesting and merging routers

fn api_routes() -> Router<AxumAppState> {
    Router::new()
        .route("/users", get(list_users).post(axum_create_user))
        .route("/users/:id", get(axum_user_detail))
        .route("/search", get(axum_search))
}

fn create_router(state: AxumAppState) -> Router {
    Router::new()
        // Basic routes
        .route("/", get(axum_index))
        .route("/api", get(axum_api_index))
        // Nested routes
        .nest("/api/v1", api_routes())
        // Middleware
        .layer(middleware::from_fn(logging_middleware))
        .route("/protected", get(|| async { "Protected" })
            .layer(middleware::from_fn(auth_middleware)))
        // State
        .with_state(state)
}


// ============================================================================
// 17. AXUM COMPLETE APPLICATION
// ============================================================================

#[tokio::main]
async fn main_axum() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::fmt::init();
    
    // Create state
    let state = AxumAppState {
        counter: Arc::new(Mutex::new(0)),
        app_name: "Axum API".to_string(),
    };
    
    // Create router
    let app = create_router(state);
    
    // Run server
    let listener = TcpListener::bind("127.0.0.1:3000").await?;
    println!("Listening on {}", listener.local_addr()?);
    
    axum::serve(listener, app).await?;
    
    Ok(())
}
*/


// ============================================================================
// 18. COMPARISON: ACTIX-WEB VS AXUM
// ============================================================================

/// PERFORMANCE:
/// - Both are extremely fast
/// - Actix-web slightly faster in some benchmarks
/// - Performance difference negligible in real apps
///
/// ERGONOMICS:
/// - Axum: More idiomatic Rust, better type inference
/// - Actix-web: More explicit, more configuration options
///
/// ECOSYSTEM:
/// - Actix-web: Mature, many plugins, larger community
/// - Axum: Growing, Tower ecosystem, official tokio project
///
/// LEARNING CURVE:
/// - Axum: Easier for Rust beginners
/// - Actix-web: Requires understanding actor model
///
/// USE CASES:
/// - Actix-web: High-performance APIs, WebSockets, complex routing
/// - Axum: Modern async apps, Tower middleware, simple APIs


// ============================================================================
// 19. COMMON PATTERNS
// ============================================================================

/// Pattern 1: Database Connection Pool (both frameworks)
/*
use sqlx::PgPool;

// Actix-web
let pool = PgPool::connect(&database_url).await?;
let app_data = web::Data::new(pool);

async fn handler(pool: web::Data<PgPool>) -> Result<HttpResponse> {
    let row: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM users")
        .fetch_one(pool.get_ref())
        .await?;
    Ok(HttpResponse::Ok().json(row.0))
}

// Axum
#[derive(Clone)]
struct AppState {
    pool: PgPool,
}

async fn handler(State(state): State<AppState>) -> Result<String, StatusCode> {
    let row: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM users")
        .fetch_one(&state.pool)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    Ok(format!("Users: {}", row.0))
}
*/

/// Pattern 2: Request Validation
/*
use validator::{Validate, ValidationError};

#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(length(min = 3, max = 50))]
    name: String,
    #[validate(email)]
    email: String,
}

// Actix-web
async fn create_user_validated(
    user: web::Json<CreateUserRequest>
) -> Result<HttpResponse> {
    user.validate()
        .map_err(|e| actix_web::error::ErrorBadRequest(e))?;
    Ok(HttpResponse::Created().json(user.into_inner()))
}

// Axum - need custom extractor
struct ValidatedJson<T>(T);

#[async_trait]
impl<T, S> FromRequest<S> for ValidatedJson<T>
where
    T: DeserializeOwned + Validate,
    S: Send + Sync,
{
    type Rejection = (StatusCode, String);
    
    async fn from_request(req: Request<Body>, state: &S) -> Result<Self, Self::Rejection> {
        let Json(value) = Json::<T>::from_request(req, state)
            .await
            .map_err(|e| (StatusCode::BAD_REQUEST, format!("{}", e)))?;
        
        value.validate()
            .map_err(|e| (StatusCode::BAD_REQUEST, format!("{}", e)))?;
        
        Ok(ValidatedJson(value))
    }
}
*/


// ============================================================================
// 20. TESTING WEB APPLICATIONS
// ============================================================================

/// Testing actix-web
/*
#[cfg(test)]
mod actix_tests {
    use super::*;
    use actix_web::{test, App};
    
    #[actix_web::test]
    async fn test_index() {
        let app = test::init_service(
            App::new().route("/", web::get().to(index))
        ).await;
        
        let req = test::TestRequest::get().uri("/").to_request();
        let resp = test::call_service(&app, req).await;
        
        assert!(resp.status().is_success());
    }
}
*/

/// Testing axum
/*
#[cfg(test)]
mod axum_tests {
    use super::*;
    use axum::body::Body;
    use tower::ServiceExt;
    
    #[tokio::test]
    async fn test_index() {
        let app = Router::new().route("/", get(axum_index));
        
        let response = app
            .oneshot(Request::builder().uri("/").body(Body::empty()).unwrap())
            .await
            .unwrap();
        
        assert_eq!(response.status(), StatusCode::OK);
    }
}
*/


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

fn main() {
    println!("=== RUST WEB FRAMEWORKS ===\n");
    println!("This file demonstrates patterns for Actix-web and Axum.");
    println!("Uncomment the examples to see them in action.\n");
    
    println!("ACTIX-WEB:");
    println!("  ✓ Mature and battle-tested");
    println!("  ✓ Rich feature set");
    println!("  ✓ Actor-based architecture");
    println!("  ✓ Extensive middleware");
    
    println!("\nAXUM:");
    println!("  ✓ Modern and ergonomic");
    println!("  ✓ Tower ecosystem");
    println!("  ✓ Type-safe extractors");
    println!("  ✓ Simple to learn");
    
    println!("\nCHOOSE ACTIX-WEB IF:");
    println!("  • You need maximum performance");
    println!("  • You want a mature ecosystem");
    println!("  • You need complex routing");
    
    println!("\nCHOOSE AXUM IF:");
    println!("  • You want modern async patterns");
    println!("  • You use Tower middleware");
    println!("  • You prefer simpler API");
}

/// DEPENDENCIES FOR ACTIX-WEB:
/// ```toml
/// actix-web = "4"
/// tokio = { version = "1", features = ["full"] }
/// serde = { version = "1", features = ["derive"] }
/// serde_json = "1"
/// env_logger = "0.10"
/// ```
///
/// DEPENDENCIES FOR AXUM:
/// ```toml
/// axum = "0.7"
/// tokio = { version = "1", features = ["full"] }
/// serde = { version = "1", features = ["derive"] }
/// serde_json = "1"
/// tower = "0.4"
/// tower-http = { version = "0.5", features = ["fs", "trace"] }
/// tracing = "0.1"
/// tracing-subscriber = "0.3"
/// ```
