/*
Simple Router
--------------------------------------------------------
Given routes like:

GET /users/:id
POST /users

Match request path to handler.

Senior signal:
- Pattern matching
- Data modeling
- Clean separation of routing vs handling
*/
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};

#[get("/users/{id}")]
async fn get_user(path: web::Path<String>) -> impl Responder {
    let id = path.into_inner();
    HttpResponse::Ok().body(format!("User {}", id))
}

#[post("/users")]
async fn post_user() -> impl Responder {
    HttpResponse::Ok().body("User created")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new().service(get_user).service(post_user)
    }).bind(("127.0.0.1", 8080))?
    .run()
    .await
}