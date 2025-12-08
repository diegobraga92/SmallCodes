use crate::db::user as db_user;
use crate::error::internal_error;
use crate::models::user::{NewUser, User};
use axum::{extract::State, http::StatusCode, response::Json};
use deadpool_diesel::postgres::Pool;

pub async fn create_user(
    State(pool): State<Pool>,
    Json(new_user): Json<NewUser>,
) -> Result<Json<User>, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;
    let res = conn
        .interact(move |conn| db_user::create_user(conn, new_user))
        .await
        .map_err(internal_error)?
        .map_err(internal_error)?;

    Ok(Json(res))
}

pub async fn list_users(State(pool): State<Pool>) -> Result<Json<Vec<User>>, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;
    let res = conn
        .interact(|conn| db_user::list_users(conn))
        .await
        .map_err(internal_error)?
        .map_err(internal_error)?;

    Ok(Json(res))
}
