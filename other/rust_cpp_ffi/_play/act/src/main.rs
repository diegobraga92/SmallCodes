use actix_web::{HttpRequest, HttpResponse, Responder, web};
use chrono::Utc;
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey};
use serde::{Serialize, Deserialize};

const SECRET: &[u8] = b"my_secret_key";

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
}

#[derive(Debug, Serialize, Deserialize)]
struct LoginRequest {
    username: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct TokenResponse {
    access_token: String,
    refresh_token: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct RefreshToken {
    token: String,
}

fn create_token(user: &str, minutes: i64) -> Result<String> {
    let exp = (Utc::now()  + chrono::Duration::minutes(minutes)).timestamp() as usize;
    let claims = Claims {
        sub: user.to_owned(),
        exp,
    }; 

    Ok(encode(&Header::default(), &claims, &EncodingKey::from_secret(SECRET),)?)
}

fn validate_token(token: &str) -> Result<Claims> {
    let token_data = decode::<Claims>(
        token,
        &DecodingKey::from_secret(SECRET),
        &Validation::default(),
    )?;
    Ok(token_data.claims)
}

async fn login(payload: web::Json<LoginRequest>) -> impl Responder {
    let access_token = create_token(&payload.username, 15)?; // 15 minutes
    let refresh_token = create_token(&payload.username, 43200)?; // 30 days

    HttpResponse::Ok().json(TokenResponse {
        access_token,
        refresh_token,
    })
}

async fn refresh_token(payload: web::Json<RefreshToken>) -> impl Responder {
    match validate_token(&payload.token) {
        Ok(claims) => {
            let new_access_token = create_token(&claims.sub, 15)?; // 15 minutes

            HttpResponse::Ok().json(serde_json::json!({
                "access_token": new_access_token   
            }))
        }
        Err(_) => HttpResponse::Unauthorized().body("Invalid refresh token"),
    }
}

fn extract_username_from_token(req: &HttpRequest) -> Result<String> {
    let token = req.headers().get("Authorization").unwrap().to_str().unwrap();
    let claims = validate_token(token)?;
    Ok(claims.sub)
}

async fn proxy(req: HttpRequest) -> impl Responder {
    if extract_username_from_token(&req).is_err() {
        return HttpResponse::Unauthorized().body("Invalid access token");
    }

    let response = reqwest::get("https://httpbin.org/get").await.unwrap().text().await.unwrap();

    HttpResponse::Ok().json(response)
}