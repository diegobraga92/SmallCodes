use crate::schema::users;
use diesel::prelude::*;

#[derive(serde::Serialize, Selectable, Queryable)]
pub struct User {
    pub id: i32,
    pub username: String,
}

#[derive(serde::Deserialize, Insertable)]
#[diesel(table_name = users)]
pub struct NewUser {
    pub username: String,
}
