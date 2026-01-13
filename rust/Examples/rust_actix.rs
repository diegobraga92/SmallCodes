/*
[package]
name = "actix_jwt_example"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = "4"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
jsonwebtoken = "9"
reqwest = { version = "0.11", features = ["json"] }
chrono = { version = "0.4", features = ["serde"] }
anyhow = "1"
*/

use actix_web::{
    web, App, HttpRequest, HttpResponse, HttpServer, Responder,
};
use anyhow::Result;
use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};

const SECRET: &[u8] = b"super_secret_key";

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
}

#[derive(Deserialize)]
struct LoginRequest {
    username: String,
}

#[derive(Serialize)]
struct TokenResponse {
    access_token: String,
    refresh_token: String,
}

#[derive(Deserialize)]
struct RefreshRequest {
    refresh_token: String,
}

fn create_token(user: &str, minutes: i64) -> Result<String> {
    let exp = (Utc::now() + Duration::minutes(minutes)).timestamp() as usize;
    let claims = Claims {
        sub: user.to_string(),
        exp,
    };
    Ok(encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret(SECRET),
    )?)
}

fn validate_token(token: &str) -> Result<Claims> {
    let data = decode::<Claims>(
        token,
        &DecodingKey::from_secret(SECRET),
        &Validation::default(),
    )?;
    Ok(data.claims)
}

// -------------------- Handlers --------------------

async fn login(payload: web::Json<LoginRequest>) -> impl Responder {
    let access = create_token(&payload.username, 15).unwrap();
    let refresh = create_token(&payload.username, 60 * 24 * 7).unwrap();

    HttpResponse::Ok().json(TokenResponse {
        access_token: access,
        refresh_token: refresh,
    })
}

async fn refresh(payload: web::Json<RefreshRequest>) -> impl Responder {
    match validate_token(&payload.refresh_token) {
        Ok(claims) => {
            let new_access = create_token(&claims.sub, 15).unwrap();
            HttpResponse::Ok().json(serde_json::json!({
                "access_token": new_access
            }))
        }
        Err(_) => HttpResponse::Unauthorized().finish(),
    }
}

fn extract_user(req: &HttpRequest) -> Result<String> {
    let header = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .ok_or_else(|| anyhow::anyhow!("Missing auth header"))?;

    let token = header.trim_start_matches("Bearer ");
    let claims = validate_token(token)?;
    Ok(claims.sub)
}

async fn proxy(req: HttpRequest) -> impl Responder {
    if extract_user(&req).is_err() {
        return HttpResponse::Unauthorized().finish();
    }

    let response = reqwest::get("https://httpbin.org/get")
        .await
        .unwrap()
        .json::<serde_json::Value>()
        .await
        .unwrap();

    HttpResponse::Ok().json(response)
}

// -------------------- Main --------------------

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/login", web::post().to(login))
            .route("/refresh", web::post().to(refresh))
            .route("/proxy", web::get().to(proxy))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}


/*
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username":"diego"}'

curl http://localhost:8080/proxy \
  -H "Authorization: Bearer <access_token>"

curl -X POST http://localhost:8080/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"<refresh_token>"}'
*/