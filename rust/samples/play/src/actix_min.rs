use actix_web::{get, post, web, App, HttpServer, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Item {
    id: u32,
    name: String,
}

/*
 * Shared application state
 */
struct AppState {
    items: Mutex<Vec<Item>>,
}

#[get("/items")]
async fn get_items(data: web::Data<AppState>) -> impl Responder {
    let items = data.items.lock().unwrap();
    web::Json(items.clone())
}

#[post("/items")]
async fn add_item(
    data: web::Data<AppState>,
    payload: web::Json<Item>,
) -> impl Responder {
    let mut items = data.items.lock().unwrap();
    items.push(payload.into_inner());

    "Item added"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = web::Data::new(AppState {
        items: Mutex::new(Vec::new()),
    });

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .service(get_items)
            .service(add_item)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
