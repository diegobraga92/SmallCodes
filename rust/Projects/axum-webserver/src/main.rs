mod db;
mod error;
mod models;
mod routes;
mod schema;
mod startup;

#[tokio::main]
async fn main() {
    startup::run().await;
}
