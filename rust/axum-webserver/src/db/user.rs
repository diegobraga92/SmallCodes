use crate::models::user::{NewUser, User};
use crate::schema::users;
use diesel::prelude::*;

pub fn create_user(conn: &mut PgConnection, new_user: NewUser) -> QueryResult<User> {
    diesel::insert_into(users::table)
        .values(new_user)
        .returning(User::as_returning())
        .get_result(conn)
}

pub fn list_users(conn: &mut PgConnection) -> QueryResult<Vec<User>> {
    users::table.select(User::as_select()).load(conn)
}
