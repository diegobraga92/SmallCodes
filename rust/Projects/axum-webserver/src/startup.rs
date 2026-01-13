use axum::{
    Router,
    routing::{get, post},
};
use diesel_migrations::{EmbeddedMigrations, embed_migrations};
use std::net::SocketAddr;
use tracing_subscriber;

use crate::routes::health::health_check;
use crate::routes::todo::{create_todo, list_todos, mark_todo_done, unmark_todo_done};
use crate::routes::user::{create_user, list_users};

pub const MIGRATIONS: EmbeddedMigrations = embed_migrations!("migrations/");

pub async fn build_app() -> Router {
    // Start DB connection pool
    let db_url =
        std::env::var("DATABASE_URL").expect("DATABASE_URL environment variable must be set");
    let manager = deadpool_diesel::postgres::Manager::new(db_url, deadpool_diesel::Runtime::Tokio1);
    let pool = deadpool_diesel::postgres::Pool::builder(manager)
        .build()
        .expect("Failed to create database connection pool");

    Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .route("/health", get(health_check))
        .route("/user/list", get(list_users))
        .route("/user/create", post(create_user))
        // Todo endpoints
        .route("/todo", post(create_todo))
        .route("/todo", get(list_todos))
        .route("/todo/:id/done", post(mark_todo_done))
        .route("/todo/:id/undone", post(unmark_todo_done))
        .with_state(pool)
}

pub async fn run() {
    tracing_subscriber::fmt::init();
    let app = build_app().await;
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    println!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}
