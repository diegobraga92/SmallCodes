#[macro_use] extern crate rocket;

#[get("/health")]
pub fn health_check() -> &'static str {
    "OK"
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![health_check])
}