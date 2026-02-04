/*
Task Description:

Implement a POST /users API endpoint that:
1. Accepts a JSON payload.
2. Expects two properties in the payload: `name` (String) and `age` (number).
3. Returns HTTP 400 if either `name` or `age` is missing.
4. Returns HTTP 400 if `name` is longer than 32 characters.
5. Returns HTTP 400 if `age` is not a number.
6. Returns HTTP 400 if `age` is less than 16.
7. Calls the `save` method on a Database trait object if all validations pass.
8. Returns the Record produced by `save` along with HTTP 201 on success.

Assumptions:
- The Database trait exposes: fn save(&mut self, user: User) -> Record
- User and Record structs are provided and use Rocket Serde.
*/

use crate::db::{Database, Record, User};
use rocket::http::Status;
use rocket::serde::json::Json;
use rocket::{post, State};
use std::sync::Mutex;

/// POST /users
#[post("/users", format = "json", data = "<user>")]
pub fn users(
    user: Json<User>,
    database: &State<Mutex<Box<dyn Database>>>,
) -> Result<(Status, Json<Record>), Status> {
    // Validate name length
    if user.name.len() > 32 {
        return Err(Status::BadRequest);
    }

    // Validate minimum age
    if user.age < 16 {
        return Err(Status::BadRequest);
    }

    // Persist user if validation passes
    let record = database.lock().unwrap().save(user.into_inner());

    Ok((Status::Created, Json(record)))
}
