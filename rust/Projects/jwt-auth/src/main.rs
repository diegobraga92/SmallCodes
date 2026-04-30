// =============================================================================
// JWT Auth Demo — Authentication & Authorization with Axum
// =============================================================================
//
// WHAT THIS DEMONSTRATES:
//   1. Password hashing with bcrypt (industry standard)
//   2. JWT token issuance (access + refresh tokens)
//   3. JWT validation via Axum FromRequestParts extractor
//   4. Role-based authorization (admin vs user)
//   5. Secure password storage (never store plaintext)
//
// JD RELEVANCE:
//   The JD mentions "JWT-based authentication and authorization" as a
//   required skill. This demo shows the full auth flow end-to-end.
//
// SECURITY NOTES:
//   - Passwords are hashed with bcrypt (cost factor 12)
//   - JWTs are signed with HMAC-SHA256 (HS256)
//   - Tokens have expiration (15min for access, 7 days for refresh)
//   - In production, use RS256 (asymmetric) and store private key securely
// =============================================================================

use axum::{
    extract::{FromRequestParts, State},
    http::{request::Parts, StatusCode},
    middleware,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{info, warn};

// =============================================================================
// Types
// =============================================================================

/// A user in our system.
#[derive(Debug, Clone, Serialize, Deserialize)]
struct User {
    id: String,
    username: String,
    /// bcrypt password hash (never the plaintext password!)
    password_hash: String,
    role: String, // "admin" or "user"
}

/// JWT claims — the data embedded in the token.
#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,       // subject (user ID)
    username: String,
    role: String,
    exp: usize,        // expiration timestamp (Unix epoch)
    iat: usize,        // issued at timestamp
}

/// In-memory user store (in production, use a database).
struct AppState {
    users: RwLock<HashMap<String, User>>,
    jwt_secret: String,
}

// =============================================================================
// Request/Response types
// =============================================================================

#[derive(Debug, Serialize, Deserialize)]
struct RegisterRequest {
    username: String,
    password: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct LoginRequest {
    username: String,
    password: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct AuthResponse {
    token: String,
    refresh_token: String,
    user_id: String,
    role: String,
}

#[derive(Debug, Serialize)]
struct ErrorResponse {
    error: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct UserInfoResponse {
    id: String,
    username: String,
    role: String,
}

#[derive(Debug, Serialize)]
struct AdminDashboardResponse {
    message: String,
    users: Vec<UserInfoResponse>,
}

// =============================================================================
// Auth Extractor — Extracts authenticated user from request
// =============================================================================

/// Extracted user info from a valid JWT.
#[derive(Debug, Clone)]
struct AuthenticatedUser {
    user_id: String,
    username: String,
    role: String,
}

/// Axum extractor that validates the JWT from the Authorization header.
///
/// This is the key piece of middleware infrastructure. Any handler that
/// takes `AuthenticatedUser` as a parameter will automatically require
/// a valid JWT. If the token is missing or invalid, the request is
/// rejected with 401 Unauthorized.
#[async_trait::async_trait]
impl<S> FromRequestParts<S> for AuthenticatedUser
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, Json<ErrorResponse>);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        // Extract the Authorization header
        let auth_header = parts
            .headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .ok_or_else(|| {
                (
                    StatusCode::UNAUTHORIZED,
                    Json(ErrorResponse {
                        error: "Missing Authorization header".to_string(),
                    }),
                )
            })?;

        // Parse "Bearer <token>"
        let token = auth_header
            .strip_prefix("Bearer ")
            .ok_or_else(|| {
                (
                    StatusCode::UNAUTHORIZED,
                    Json(ErrorResponse {
                        error: "Invalid Authorization header format. Use: Bearer <token>".to_string(),
                    }),
                )
            })?;

        // We need the secret to validate. We'll get it from the extension.
        let secret = parts
            .extensions
            .get::<String>()
            .ok_or_else(|| {
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(ErrorResponse {
                        error: "Server configuration error".to_string(),
                    }),
                )
            })?;

        // Decode and validate the JWT
        let token_data = decode::<Claims>(
            token,
            &DecodingKey::from_secret(secret.as_bytes()),
            &Validation::default(),
        )
        .map_err(|e| {
            warn!("JWT validation failed: {e}");
            (
                StatusCode::UNAUTHORIZED,
                Json(ErrorResponse {
                    error: "Invalid or expired token".to_string(),
                }),
            )
        })?;

        let claims = token_data.claims;

        Ok(AuthenticatedUser {
            user_id: claims.sub,
            username: claims.username,
            role: claims.role,
        })
    }
}

// =============================================================================
// Middleware — Injects JWT secret into request extensions
// =============================================================================

/// Middleware that injects the JWT secret into request extensions so the
/// AuthenticatedUser extractor can access it.
///
/// This is necessary because Axum's FromRequestParts doesn't have access
/// to application state directly (it uses the generic S parameter which
/// we can't constrain).
async fn inject_jwt_secret(
    State(state): State<Arc<AppState>>,
    mut request: axum::extract::Request,
    next: middleware::Next,
) -> impl IntoResponse {
    request.extensions_mut().insert(state.jwt_secret.clone());
    next.run(request).await
}

// =============================================================================
// Handlers
// =============================================================================

/// POST /register — Create a new user account.
async fn register(
    State(state): State<Arc<AppState>>,
    Json(body): Json<RegisterRequest>,
) -> Result<Json<AuthResponse>, (StatusCode, Json<ErrorResponse>)> {
    // Validate input
    if body.username.is_empty() || body.password.is_empty() {
        return Err((
            StatusCode::BAD_REQUEST,
            Json(ErrorResponse {
                error: "Username and password are required".to_string(),
            }),
        ));
    }

    if body.password.len() < 8 {
        return Err((
            StatusCode::BAD_REQUEST,
            Json(ErrorResponse {
                error: "Password must be at least 8 characters".to_string(),
            }),
        ));
    }

    // Check if username already exists
    {
        let users = state.users.read().await;
        if users.values().any(|u| u.username == body.username) {
            return Err((
                StatusCode::CONFLICT,
                Json(ErrorResponse {
                    error: "Username already exists".to_string(),
                }),
            ));
        }
    }

    // Hash the password with bcrypt
    let password_hash = bcrypt::hash(&body.password, 12).map_err(|e| {
        warn!("Password hashing failed: {e}");
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: "Failed to hash password".to_string(),
            }),
        )
    })?;

    let user_id = uuid::Uuid::new_v4().to_string();
    let role = if body.username == "admin" { "admin" } else { "user" };

    let user = User {
        id: user_id.clone(),
        username: body.username.clone(),
        password_hash,
        role: role.to_string(),
    };

    // Store the user
    state.users.write().await.insert(user_id.clone(), user);

    info!("User registered: {username} (role: {role})", username = body.username);

    // Generate tokens
    let (token, refresh_token) = generate_tokens(&state.jwt_secret, &user_id, &body.username, role)?;

    Ok(Json(AuthResponse {
        token,
        refresh_token,
        user_id,
        role: role.to_string(),
    }))
}

/// POST /login — Authenticate and get JWT tokens.
async fn login(
    State(state): State<Arc<AppState>>,
    Json(body): Json<LoginRequest>,
) -> Result<Json<AuthResponse>, (StatusCode, Json<ErrorResponse>)> {
    // Find the user
    let user = {
        let users = state.users.read().await;
        users
            .values()
            .find(|u| u.username == body.username)
            .cloned()
    }
    .ok_or_else(|| {
        (
            StatusCode::UNAUTHORIZED,
            Json(ErrorResponse {
                error: "Invalid username or password".to_string(),
            }),
        )
    })?;

    // Verify the password
    let password_valid = bcrypt::verify(&body.password, &user.password_hash).map_err(|e| {
        warn!("Password verification error: {e}");
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: "Authentication error".to_string(),
            }),
        )
    })?;

    if !password_valid {
        return Err((
            StatusCode::UNAUTHORIZED,
            Json(ErrorResponse {
                error: "Invalid username or password".to_string(),
            }),
        ));
    }

    info!("User logged in: {username}", username = body.username);

    // Generate tokens
    let (token, refresh_token) =
        generate_tokens(&state.jwt_secret, &user.id, &user.username, &user.role)?;

    Ok(Json(AuthResponse {
        token,
        refresh_token,
        user_id: user.id,
        role: user.role,
    }))
}

/// GET /me — Get the current user's info (requires auth).
async fn get_me(user: AuthenticatedUser) -> Json<UserInfoResponse> {
    Json(UserInfoResponse {
        id: user.user_id,
        username: user.username,
        role: user.role,
    })
}

/// GET /admin/dashboard — Admin-only endpoint (requires auth + admin role).
async fn admin_dashboard(
    user: AuthenticatedUser,
    State(state): State<Arc<AppState>>,
) -> Result<Json<AdminDashboardResponse>, (StatusCode, Json<ErrorResponse>)> {
    // Role check
    if user.role != "admin" {
        return Err((
            StatusCode::FORBIDDEN,
            Json(ErrorResponse {
                error: "Admin access required".to_string(),
            }),
        ));
    }

    let users = state.users.read().await;
    let user_list: Vec<UserInfoResponse> = users
        .values()
        .map(|u| UserInfoResponse {
            id: u.id.clone(),
            username: u.username.clone(),
            role: u.role.clone(),
        })
        .collect();

    Ok(Json(AdminDashboardResponse {
        message: format!("Welcome admin {}! Here are all users:", user.username),
        users: user_list,
    }))
}

/// GET /public/health — Public endpoint (no auth required).
async fn health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "ok",
        "service": "jwt-auth-demo",
        "version": "0.1.0"
    }))
}

// =============================================================================
// Token Generation
// =============================================================================

/// Generate an access token (15 min) and a refresh token (7 days).
fn generate_tokens(
    secret: &str,
    user_id: &str,
    username: &str,
    role: &str,
) -> Result<(String, String), (StatusCode, Json<ErrorResponse>)> {
    let now = Utc::now();

    // Access token: short-lived (15 minutes)
    let access_claims = Claims {
        sub: user_id.to_string(),
        username: username.to_string(),
        role: role.to_string(),
        exp: (now + Duration::minutes(15)).timestamp() as usize,
        iat: now.timestamp() as usize,
    };

    let token = encode(
        &Header::default(),
        &access_claims,
        &EncodingKey::from_secret(secret.as_bytes()),
    )
    .map_err(|e| {
        warn!("Token generation failed: {e}");
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: "Failed to generate token".to_string(),
            }),
        )
    })?;

    // Refresh token: long-lived (7 days)
    let refresh_claims = Claims {
        sub: user_id.to_string(),
        username: username.to_string(),
        role: role.to_string(),
        exp: (now + Duration::days(7)).timestamp() as usize,
        iat: now.timestamp() as usize,
    };

    let refresh_token = encode(
        &Header::default(),
        &refresh_claims,
        &EncodingKey::from_secret(secret.as_bytes()),
    )
    .map_err(|e| {
        warn!("Refresh token generation failed: {e}");
        (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(ErrorResponse {
                error: "Failed to generate refresh token".to_string(),
            }),
        )
    })?;

    Ok((token, refresh_token))
}

// =============================================================================
// Main
// =============================================================================

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("jwt_auth=info")
        .init();

    println!("╔══════════════════════════════════════════════════════════╗");
    println!("║        JWT Auth Demo                                    ║");
    println!("╚══════════════════════════════════════════════════════════╝");
    println!();

    let state = Arc::new(AppState {
        users: RwLock::new(HashMap::new()),
        jwt_secret: "super-secret-key-change-in-production-123456".to_string(),
    });

    // Build the router
    let app = Router::new()
        // Public routes (no auth required)
        .route("/public/health", get(health))
        .route("/register", post(register))
        .route("/login", post(login))
        // Protected routes (auth required)
        .route("/me", get(get_me))
        .route("/admin/dashboard", get(admin_dashboard))
        // Middleware that injects JWT secret for the AuthenticatedUser extractor
        .layer(axum::middleware::from_fn_with_state(
            state.clone(),
            inject_jwt_secret,
        ))
        .with_state(state);

    let addr = "0.0.0.0:3000";
    println!("   🚀 Server starting on http://{addr}");
    println!();
    println!("   Endpoints:");
    println!("     POST /register         - Register a new user");
    println!("     POST /login            - Login and get JWT tokens");
    println!("     GET  /me               - Get current user info (auth required)");
    println!("     GET  /admin/dashboard  - Admin dashboard (auth + admin role)");
    println!("     GET  /public/health    - Health check (no auth)");
    println!();
    println!("   Test with curl:");
    println!("     # Register a user");
    println!("     curl -X POST http://localhost:3000/register \\");
    println!("       -H 'Content-Type: application/json' \\");
    println!("       -d '{{\"username\":\"alice\",\"password\":\"password123\"}}'");
    println!();
    println!("     # Login");
    println!("     curl -X POST http://localhost:3000/login \\");
    println!("       -H 'Content-Type: application/json' \\");
    println!("       -d '{{\"username\":\"alice\",\"password\":\"password123\"}}'");
    println!();
    println!("     # Access protected endpoint");
    println!("     curl http://localhost:3000/me \\");
    println!("       -H 'Authorization: Bearer <token>'");
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
        http::{self, Request},
    };
    use tower::ServiceExt;

    fn test_state() -> Arc<AppState> {
        Arc::new(AppState {
            users: RwLock::new(HashMap::new()),
            jwt_secret: "test-secret-key".to_string(),
        })
    }

    fn test_app(state: Arc<AppState>) -> Router {
        Router::new()
            .route("/public/health", get(health))
            .route("/register", post(register))
            .route("/login", post(login))
            .route("/me", get(get_me))
            .route("/admin/dashboard", get(admin_dashboard))
            .layer(axum::middleware::from_fn_with_state(
                state.clone(),
                inject_jwt_secret,
            ))
            .with_state(state)
    }

    #[tokio::test]
    async fn test_health_endpoint() {
        let app = test_app(test_state());

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/public/health")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_register_and_login() {
        let state = test_state();
        let app = test_app(state.clone());

        // Register
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/register")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&RegisterRequest {
                            username: "testuser".to_string(),
                            password: "password123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let body: AuthResponse =
            serde_json::from_slice(&axum::body::to_bytes(response.into_body(), usize::MAX)
                .await
                .unwrap())
            .unwrap();

        assert_eq!(body.role, "user");
        assert!(!body.token.is_empty());

        // Login
        let app = test_app(state.clone());
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/login")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&LoginRequest {
                            username: "testuser".to_string(),
                            password: "password123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_protected_endpoint_without_token() {
        let app = test_app(test_state());

        let response = app
            .oneshot(
                Request::builder()
                    .uri("/me")
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::UNAUTHORIZED);
    }

    #[tokio::test]
    async fn test_protected_endpoint_with_token() {
        let state = test_state();
        let app = test_app(state.clone());

        // Register first
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/register")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&RegisterRequest {
                            username: "alice".to_string(),
                            password: "password123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        let body: AuthResponse =
            serde_json::from_slice(&axum::body::to_bytes(response.into_body(), usize::MAX)
                .await
                .unwrap())
            .unwrap();

        // Access /me with the token
        let app = test_app(state.clone());
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/me")
                    .header("Authorization", format!("Bearer {}", body.token))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);

        let user_info: UserInfoResponse =
            serde_json::from_slice(&axum::body::to_bytes(response.into_body(), usize::MAX)
                .await
                .unwrap())
            .unwrap();

        assert_eq!(user_info.username, "alice");
        assert_eq!(user_info.role, "user");
    }

    #[tokio::test]
    async fn test_admin_dashboard_requires_admin() {
        let state = test_state();
        let app = test_app(state.clone());

        // Register a regular user
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/register")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&RegisterRequest {
                            username: "bob".to_string(),
                            password: "password123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        let body: AuthResponse =
            serde_json::from_slice(&axum::body::to_bytes(response.into_body(), usize::MAX)
                .await
                .unwrap())
            .unwrap();

        // Try to access admin dashboard with regular user token
        let app = test_app(state.clone());
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/admin/dashboard")
                    .header("Authorization", format!("Bearer {}", body.token))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::FORBIDDEN);
    }

    #[tokio::test]
    async fn test_admin_dashboard_with_admin() {
        let state = test_state();
        let app = test_app(state.clone());

        // Register as admin (username "admin" gets admin role)
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/register")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&RegisterRequest {
                            username: "admin".to_string(),
                            password: "adminpass123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        let body: AuthResponse =
            serde_json::from_slice(&axum::body::to_bytes(response.into_body(), usize::MAX)
                .await
                .unwrap())
            .unwrap();

        assert_eq!(body.role, "admin");

        // Access admin dashboard
        let app = test_app(state.clone());
        let response = app
            .oneshot(
                Request::builder()
                    .uri("/admin/dashboard")
                    .header("Authorization", format!("Bearer {}", body.token))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::OK);
    }

    #[tokio::test]
    async fn test_invalid_login() {
        let state = test_state();
        let app = test_app(state.clone());

        // Register
        let _response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/register")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&RegisterRequest {
                            username: "charlie".to_string(),
                            password: "password123".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        // Try wrong password
        let app = test_app(state.clone());
        let response = app
            .oneshot(
                Request::builder()
                    .method(http::Method::POST)
                    .uri("/login")
                    .header("Content-Type", "application/json")
                    .body(Body::from(
                        serde_json::to_string(&LoginRequest {
                            username: "charlie".to_string(),
                            password: "wrongpassword".to_string(),
                        })
                        .unwrap(),
                    ))
                    .unwrap(),
            )
            .await
            .unwrap();

        assert_eq!(response.status(), StatusCode::UNAUTHORIZED);
    }
}
