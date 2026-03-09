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
use axum::{
    extract::{Path, State},
    routing::{get, post},
    Json, Router,
    http::StatusCode,
};
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
};

#[tokio::main]
async fn main() {
    let state = AppState {
        users: Arc::new(Mutex::new(HashMap::new())),
    };

    let app = build_router(state);

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}

fn build_router(state: AppState) -> Router {
    Router::new()
        .route("/users", post(create_user))
        .route("/users/{id}", get(get_user))
        .with_state(state)
}

#[derive(Clone)]
struct AppState {
    users: Arc<Mutex<HashMap<u64, User>>>,
}

#[derive(Serialize, Deserialize, Clone)]
struct User {
    id: u64,
    name: String,
}

#[derive(Deserialize)]
struct CreateUserRequest {
    name: String,
}

async fn create_user(
    State(state): State<AppState>,
    Json(payload): Json<CreateUserRequest>,
) -> Json<User> {
    let mut users = state.users.lock().unwrap();

    let id = users.len() as u64 + 1;
    let user = User {
        id,
        name: payload.name,
    };

    users.insert(id, user.clone());

    Json(user)
}

async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<u64>,
) -> Result<Json<User>, StatusCode> {
    let users = state.users.lock().unwrap();

    match users.get(&id) {
        Some(user) => Ok(Json(user.clone())),
        None => Err(StatusCode::NOT_FOUND),
    }
}
