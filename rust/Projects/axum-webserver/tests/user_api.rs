use reqwest::StatusCode;
use serde_json::json;
use tracing_subscriber;

#[tokio::test]
async fn test_health_check() {
    let _ = tracing_subscriber::fmt::try_init();
    let resp = reqwest::get("http://localhost:3000/health")
        .await
        .expect("Failed to send request");
    let status = resp.status();
    let body = resp.text().await.unwrap();
    assert_eq!(status, StatusCode::OK, "Health check failed: {}", body);
    assert_eq!(body, "OK");
}

#[tokio::test]
async fn test_create_and_list_user() {
    let _ = tracing_subscriber::fmt::try_init();
    // Create a new user
    let client = reqwest::Client::new();
    let new_user = json!({ "username": "testuser" });
    let resp = client
        .post("http://localhost:3000/user/create")
        .json(&new_user)
        .send()
        .await
        .expect("Failed to send create user request");
    if resp.status() != StatusCode::OK {
        let status = resp.status();
        let err_body = resp.text().await.unwrap();
        panic!("Create user failed: {} - {}", status, err_body);
    }

    // List users and check if the new user is present
    let resp = client
        .get("http://localhost:3000/user/list")
        .send()
        .await
        .expect("Failed to send list users request");
    if resp.status() != StatusCode::OK {
        let status = resp.status();
        let err_body = resp.text().await.unwrap();
        panic!("List users failed: {} - {}", status, err_body);
    }
    let users: Vec<serde_json::Value> = resp.json().await.unwrap();
    assert!(users.iter().any(|u| u["username"] == "testuser"));
}
