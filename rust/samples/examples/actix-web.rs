//// Best performance, very opinionated, more abstraction
use actix_web::{web, App, HttpServer, HttpResponse, Responder};
use actix_web::middleware::Logger;
use std::sync::Mutex;

// State shared across application
struct AppState {
    counter: Mutex<i32>,
}

async fn index(data: web::Data<AppState>) -> impl Responder {
    let mut counter = data.counter.lock().unwrap();
    *counter += 1;
    HttpResponse::Ok().body(format!("Request count: {}", counter))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "actix_web=info");
    env_logger::init();
    
    let app_state = web::Data::new(AppState {
        counter: Mutex::new(0),
    });
    
    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .wrap(Logger::default())
            .wrap(actix_web::middleware::Compress::default())
            .service(
                web::scope("/api")
                    .route("/count", web::get().to(index))
                    .route("/health", web::get().to(|| async { HttpResponse::Ok() }))
            )
            .default_service(
                web::route().to(|| async { 
                    HttpResponse::NotFound().body("Not Found") 
                })
            )
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}


//// Routing and Extractors
use actix_web::{web, get, post, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct Pagination {
    page: u32,
    per_page: u32,
}

#[derive(Deserialize)]
struct CreateUser {
    name: String,
    email: String,
}

#[derive(Serialize)]
struct User {
    id: u64,
    name: String,
    email: String,
}

// Path parameters
#[get("/users/{id}")]
async fn get_user(path: web::Path<u64>) -> impl Responder {
    let user_id = path.into_inner();
    HttpResponse::Ok().json(User {
        id: user_id,
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    })
}

// Query parameters
#[get("/users")]
async fn list_users(query: web::Query<Pagination>) -> impl Responder {
    HttpResponse::Ok().json(vec![
        User {
            id: 1,
            name: "Alice".to_string(),
            email: "alice@example.com".to_string(),
        }
    ])
}

// JSON body with validation
#[post("/users")]
async fn create_user(
    user: web::Json<CreateUser>,
    // Custom validator
) -> impl Responder {
    if user.name.is_empty() {
        return HttpResponse::BadRequest().body("Name cannot be empty");
    }
    
    HttpResponse::Created().json(User {
        id: 42,
        name: user.name.clone(),
        email: user.email.clone(),
    })
}

// Multiple extractors
#[get("/users/{id}/posts/{post_id}")]
async fn get_user_post(
    path: web::Path<(u64, u64)>,
    query: web::Query<Pagination>,
    req: actix_web::HttpRequest,
) -> impl Responder {
    let (user_id, post_id) = path.into_inner();
    let page = query.page;
    
    HttpResponse::Ok().body(format!(
        "User {}, Post {}, Page {}",
        user_id, post_id, page
    ))
}


//// Middleware
use actix_web::{middleware, web, App, HttpServer, HttpResponse};
use actix_web::dev::{Service, ServiceRequest, ServiceResponse, Transform};
use futures_util::future::{ready, Ready};
use std::rc::Rc;

// Custom middleware
pub struct CustomMiddleware;

impl<S, B> Transform<S, ServiceRequest> for CustomMiddleware
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = actix_web::Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = actix_web::Error;
    type Transform = CustomMiddlewareMiddleware<S>;
    type InitError = ();
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(CustomMiddlewareMiddleware {
            service: Rc::new(service),
        }))
    }
}

pub struct CustomMiddlewareMiddleware<S> {
    service: Rc<S>,
}

impl<S, B> Service<ServiceRequest> for CustomMiddlewareMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = actix_web::Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = actix_web::Error;
    type Future = futures_util::future::LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    actix_web::dev::forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let service = Rc::clone(&self.service);
        
        Box::pin(async move {
            // Pre-process
            println!("Before: {}", req.path());
            
            // Add custom header
            let mut res = service.call(req).await?;
            res.headers_mut().insert(
                "X-Custom-Middleware",
                "processed".parse().unwrap(),
            );
            
            // Post-process
            println!("After: {}", res.status());
            
            Ok(res)
        })
    }
}

// Using middleware in Actix
#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .wrap(middleware::Logger::default())
            .wrap(middleware::Compress::default())
            .wrap(middleware::NormalizePath::trim())
            .wrap(CustomMiddleware)
            .wrap_fn(|req, srv| {
                // Ad-hoc middleware
                let fut = srv.call(req);
                async move {
                    let res = fut.await?;
                    Ok(res)
                }
            })
            .route("/", web::get().to(HttpResponse::Ok))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}


//// Error handling
use actix_web::{error, web, App, HttpResponse, HttpServer, ResponseError};
use derive_more::{Display, Error};
use serde_json::json;

#[derive(Debug, Display, Error)]
enum ApiError {
    #[display(fmt = "Internal server error")]
    InternalError,
    
    #[display(fmt = "Bad request: {}", _0)]
    BadRequest(String),
    
    #[display(fmt = "Not found")]
    NotFound,
}

impl ResponseError for ApiError {
    fn error_response(&self) -> HttpResponse {
        match self {
            ApiError::InternalError => {
                HttpResponse::InternalServerError()
                    .json(json!({"error": "Internal server error"}))
            }
            ApiError::BadRequest(msg) => {
                HttpResponse::BadRequest()
                    .json(json!({"error": msg}))
            }
            ApiError::NotFound => {
                HttpResponse::NotFound()
                    .json(json!({"error": "Resource not found"}))
            }
        }
    }
}

// Handler returning Result
async fn get_item(item_id: web::Path<String>) -> Result<HttpResponse, ApiError> {
    if item_id.is_empty() {
        return Err(ApiError::BadRequest("Item ID is required".to_string()));
    }
    
    // Simulate database error
    let item = fetch_item(&item_id).await
        .map_err(|_| ApiError::InternalError)?
        .ok_or(ApiError::NotFound)?;
    
    Ok(HttpResponse::Ok().json(item))
}

// Global error handler
fn configure_error_handlers(cfg: &mut web::ServiceConfig) {
    cfg.app_data(
        web::JsonConfig::default()
            .limit(4096)
            .error_handler(|err, _req| {
                error::InternalError::from_response(
                    err,
                    HttpResponse::BadRequest().body("JSON error"),
                )
                .into()
            })
    );
}


//// Testing
use actix_web::{test, web, App, http};
use serde_json::json;

#[actix_web::test]
async fn test_get_user() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(AppState::new()))
            .route("/users/{id}", web::get().to(get_user))
    ).await;
    
    let req = test::TestRequest::get()
        .uri("/users/123")
        .to_request();
    
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), http::StatusCode::OK);
    
    let body: serde_json::Value = test::read_body_json(resp).await;
    assert_eq!(body["id"], json!(123));
}

#[actix_web::test]
async fn test_create_user() {
    let app = test::init_service(
        App::new()
            .app_data(web::Data::new(AppState::new()))
            .route("/users", web::post().to(create_user))
    ).await;
    
    let user_data = json!({
        "name": "John Doe",
        "email": "john@example.com"
    });
    
    let req = test::TestRequest::post()
        .uri("/users")
        .set_json(&user_data)
        .to_request();
    
    let resp = test::call_service(&app, req).await;
    assert_eq!(resp.status(), http::StatusCode::CREATED);
}