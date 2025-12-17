// Import necessary modules
use std::future::Future;
use std::pin::Pin;
use std::sync::Arc;
use std::task::{Context, Poll};
use std::time::Duration;

use serde::{Deserialize, Serialize};
use reqwest::{Client, Response, Error as ReqwestError};
use tokio::sync::{Mutex, RwLock, Semaphore, Notify, broadcast};
use tokio::time::{sleep, timeout, interval};
use anyhow::{Result, Context as AnyhowContext, bail};
use futures::stream::{StreamExt, TryStreamExt};
use async_trait::async_trait;

/// ## API Response Models with Serde
/// Demonstrates serialization/deserialization with serde
#[derive(Debug, Serialize, Deserialize, Clone)]
struct User {
    id: u32,
    name: String,
    email: String,
    #[serde(default)] // Handle missing fields gracefully
    active: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct ApiResponse<T> {
    data: T,
    status: String,
    #[serde(rename = "statusCode")]
    status_code: u16,
}

#[derive(Debug, Serialize)]
struct CreateUserRequest {
    name: String,
    email: String,
}

/// ## Async HTTP Client with Reqwest
/// Demonstrates making HTTP requests in async context
struct ApiClient {
    client: Client,
    base_url: String,
    rate_limit_semaphore: Semaphore, // Rate limiting
    cache: RwLock<std::collections::HashMap<String, User>>, // Response caching
}

impl ApiClient {
    fn new(base_url: &str) -> Self {
        Self {
            client: Client::builder()
                .timeout(Duration::from_secs(10))
                .user_agent("tokio-example/1.0")
                .build()
                .expect("Failed to create HTTP client"),
            base_url: base_url.to_string(),
            rate_limit_semaphore: Semaphore::new(5), // Max 5 concurrent requests
            cache: RwLock::new(std::collections::HashMap::new()),
        }
    }
    
    /// Make GET request with rate limiting and caching
    async fn get_user(&self, id: u32) -> Result<User> {
        let cache_key = format!("user:{}", id);
        
        // Check cache first (read lock)
        {
            let cache = self.cache.read().await;
            if let Some(user) = cache.get(&cache_key) {
                println!("Cache hit for user {}", id);
                return Ok(user.clone());
            }
        }
        
        // Apply rate limiting
        let _permit = self.rate_limit_semaphore.acquire().await
            .context("Rate limit exceeded")?;
        
        let url = format!("{}/users/{}", self.base_url, id);
        
        println!("Making request to: {}", url);
        
        // Make HTTP request with timeout
        let response = timeout(
            Duration::from_secs(5),
            self.client.get(&url).send()
        ).await
            .context("Request timeout")?
            .context("Failed to send request")?;
        
        // Handle HTTP errors
        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            bail!("HTTP {}: {}", status, error_text);
        }
        
        // Parse JSON response
        let api_response: ApiResponse<User> = response.json().await
            .context("Failed to parse JSON response")?;
        
        let user = api_response.data;
        
        // Update cache (write lock)
        {
            let mut cache = self.cache.write().await;
            cache.insert(cache_key, user.clone());
        }
        
        Ok(user)
    }
    
    /// Make POST request with JSON body
    async fn create_user(&self, user_data: CreateUserRequest) -> Result<User> {
        let url = format!("{}/users", self.base_url);
        
        // Apply rate limiting
        let _permit = self.rate_limit_semaphore.acquire().await
            .context("Rate limit exceeded")?;
        
        let response = self.client
            .post(&url)
            .json(&user_data) // Automatic JSON serialization
            .send()
            .await
            .context("Failed to create user")?;
        
        // Parse response
        let api_response: ApiResponse<User> = response.json().await
            .context("Failed to parse create user response")?;
        
        Ok(api_response.data)
    }
    
    /// Concurrent batch requests
    async fn get_users_batch(&self, ids: Vec<u32>) -> Result<Vec<User>> {
        use futures::future::join_all;
        
        // Create futures for all requests
        let futures: Vec<_> = ids.into_iter()
            .map(|id| self.get_user(id))
            .collect();
        
        // Execute all concurrently
        let results = join_all(futures).await;
        
        // Separate successes and errors
        let mut users = Vec::new();
        let mut errors = Vec::new();
        
        for result in results {
            match result {
                Ok(user) => users.push(user),
                Err(e) => errors.push(e),
            }
        }
        
        if !errors.is_empty() {
            bail!("Batch request had {} errors", errors.len());
        }
        
        Ok(users)
    }
    
    /// Stream users as they become available
    async fn stream_users(&self, ids: Vec<u32>) -> impl futures::Stream<Item = Result<User>> + '_ {
        futures::stream::iter(ids)
            .map(|id| async move {
                let result = self.get_user(id).await;
                (id, result)
            })
            .buffer_unordered(3) // Max 3 concurrent requests
            .map(|(id, result)| {
                match result {
                    Ok(user) => {
                        println!("Successfully fetched user {}", id);
                        Ok(user)
                    }
                    Err(e) => {
                        eprintln!("Failed to fetch user {}: {:?}", id, e);
                        Err(e)
                    }
                }
            })
    }
}

/// ## Custom Future with HTTP Request
/// Demonstrates manual Future implementation for HTTP operations
struct DelayedHttpRequest {
    client: Client,
    url: String,
    started: bool,
    notify: Arc<Notify>, // For signaling completion
}

impl DelayedHttpRequest {
    fn new(url: String) -> Self {
        Self {
            client: Client::new(),
            url,
            started: false,
            notify: Arc::new(Notify::new()),
        }
    }
}

impl Future for DelayedHttpRequest {
    type Output = Result<String, ReqwestError>;
    
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if !self.started {
            // First poll - start the request
            self.started = true;
            let client = self.client.clone();
            let url = self.url.clone();
            let waker = cx.waker().clone();
            let notify = Arc::clone(&self.notify);
            
            // Spawn async task
            tokio::spawn(async move {
                // Simulate delay before request
                sleep(Duration::from_millis(100)).await;
                
                // Make the actual request
                match client.get(&url).send().await {
                    Ok(response) => {
                        let text = response.text().await.unwrap_or_default();
                        println!("Request completed: {}", url);
                        // Store result somewhere accessible
                        // In real implementation, you'd store this in the future state
                        waker.wake_by_ref();
                        notify.notify_one();
                    }
                    Err(e) => {
                        eprintln!("Request failed: {}", e);
                        waker.wake_by_ref();
                        notify.notify_one();
                    }
                }
            });
            
            Poll::Pending
        } else {
            // Subsequent polls - check if request is complete
            // Note: This is a simplified example
            // In real implementation, you'd check a shared state
            Poll::Pending
        }
    }
}

/// ## Async Trait with HTTP Operations
#[async_trait]
trait UserRepository: Send + Sync {
    async fn get_user(&self, id: u32) -> Result<User>;
    async fn create_user(&self, name: &str, email: &str) -> Result<User>;
    
    // Default implementation using reqwest
    async fn fetch_from_api(&self, url: &str) -> Result<String> {
        let client = Client::new();
        let response = client.get(url).send().await?;
        Ok(response.text().await?)
    }
}

/// ## Repository Implementation
struct UserRepositoryImpl {
    client: Arc<ApiClient>,
    // Broadcast channel for notifications when users are created
    user_created_tx: broadcast::Sender<User>,
}

impl UserRepositoryImpl {
    fn new(api_client: Arc<ApiClient>) -> Self {
        let (tx, _) = broadcast::channel(100);
        Self {
            client: api_client,
            user_created_tx: tx,
        }
    }
    
    fn subscribe_to_creates(&self) -> broadcast::Receiver<User> {
        self.user_created_tx.subscribe()
    }
}

#[async_trait]
impl UserRepository for UserRepositoryImpl {
    async fn get_user(&self, id: u32) -> Result<User> {
        self.client.get_user(id).await
    }
    
    async fn create_user(&self, name: &str, email: &str) -> Result<User> {
        let user_data = CreateUserRequest {
            name: name.to_string(),
            email: email.to_string(),
        };
        
        let user = self.client.create_user(user_data).await?;
        
        // Broadcast notification about new user
        let _ = self.user_created_tx.send(user.clone());
        
        Ok(user)
    }
}

/// ## Main Application State
struct AppState {
    repository: Arc<dyn UserRepository>,
    request_counter: Mutex<u64>,
    // Shared configuration that can be updated at runtime
    config: RwLock<AppConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct AppConfig {
    api_base_url: String,
    max_concurrent_requests: usize,
    cache_ttl_seconds: u64,
}

impl AppState {
    fn new(repository: Arc<dyn UserRepository>) -> Self {
        Self {
            repository,
            request_counter: Mutex::new(0),
            config: RwLock::new(AppConfig {
                api_base_url: "https://jsonplaceholder.typicode.com".to_string(),
                max_concurrent_requests: 5,
                cache_ttl_seconds: 300,
            }),
        }
    }
    
    async fn increment_request_count(&self) -> u64 {
        let mut counter = self.request_counter.lock().await;
        *counter += 1;
        *counter
    }
    
    async fn update_config(&self, new_config: AppConfig) {
        let mut config = self.config.write().await;
        *config = new_config;
    }
    
    async fn get_config(&self) -> AppConfig {
        let config = self.config.read().await;
        config.clone()
    }
}

/// ## Background Task with Interval
/// Demonstrates periodic tasks in Tokio
async fn background_cache_cleaner(
    client: Arc<ApiClient>,
    interval_secs: u64,
    shutdown_signal: tokio_util::sync::CancellationToken,
) {
    let mut interval = interval(Duration::from_secs(interval_secs));
    
    loop {
        tokio::select! {
            _ = interval.tick() => {
                println!("Running cache cleanup...");
                // In real implementation, clean expired cache entries
                // For demo, just log and clear cache
                let mut cache = client.cache.write().await;
                let count = cache.len();
                cache.clear();
                println!("Cleared {} entries from cache", count);
            }
            _ = shutdown_signal.cancelled() => {
                println!("Cache cleaner shutting down");
                break;
            }
        }
    }
}

/// ## Concurrent User Processing
async fn process_users_concurrently(
    app_state: Arc<AppState>,
    user_ids: Vec<u32>,
) -> Result<Vec<User>> {
    use futures::future::try_join_all;
    
    // Create futures for processing each user
    let futures: Vec<_> = user_ids.into_iter()
        .map(|user_id| {
            let state = Arc::clone(&app_state);
            async move {
                // Track request count
                let request_num = state.increment_request_count().await;
                
                println!("Request #{}: Fetching user {}", request_num, user_id);
                
                // Get user with timeout
                let result = timeout(
                    Duration::from_secs(3),
                    state.repository.get_user(user_id)
                ).await;
                
                match result {
                    Ok(Ok(user)) => {
                        println!("Request #{}: Successfully fetched user {}", request_num, user_id);
                        Ok(user)
                    }
                    Ok(Err(e)) => {
                        eprintln!("Request #{}: Error fetching user {}: {:?}", request_num, user_id, e);
                        Err(e)
                    }
                    Err(_) => {
                        eprintln!("Request #{}: Timeout fetching user {}", request_num, user_id);
                        Err(anyhow::anyhow!("Timeout"))
                    }
                }
            }
        })
        .collect();
    
    // Execute with maximum concurrency
    try_join_all(futures).await
}

/// ## Serde JSON Operations
async fn json_operations_example() -> Result<()> {
    println!("\n=== Serde JSON Operations ===");
    
    // Serialize to JSON
    let user = User {
        id: 1,
        name: "John Doe".to_string(),
        email: "john@example.com".to_string(),
        active: true,
    };
    
    let json_string = serde_json::to_string(&user)?;
    println!("Serialized JSON: {}", json_string);
    
    // Pretty print JSON
    let pretty_json = serde_json::to_string_pretty(&user)?;
    println!("Pretty JSON:\n{}", pretty_json);
    
    // Deserialize from JSON
    let json_data = r#"
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
    "#;
    
    let user2: User = serde_json::from_str(json_data)?;
    println!("Deserialized user: {:?}", user2);
    
    // Handle missing fields with default
    let partial_json = r#"{"id": 3, "name": "Bob"}"#;
    let user3: User = serde_json::from_str(partial_json)?;
    println!("User with default email: {:?}", user3);
    
    Ok(())
}

/// ## HTTP Mock Server for Testing
/// (This would normally be in a separate test module)
#[cfg(test)]
mod tests {
    use super::*;
    use wiremock::{MockServer, Mock, ResponseTemplate};
    use wiremock::matchers::{method, path};
    
    #[tokio::test]
    async fn test_api_client() {
        let mock_server = MockServer::start().await;
        
        // Mock the response
        let mock_response = ApiResponse {
            data: User {
                id: 1,
                name: "Test User".to_string(),
                email: "test@example.com".to_string(),
                active: true,
            },
            status: "success".to_string(),
            status_code: 200,
        };
        
        Mock::given(method("GET"))
            .and(path("/users/1"))
            .respond_with(ResponseTemplate::new(200)
                .set_body_json(&mock_response))
            .mount(&mock_server)
            .await;
        
        let client = ApiClient::new(&mock_server.uri());
        let user = client.get_user(1).await.unwrap();
        
        assert_eq!(user.id, 1);
        assert_eq!(user.name, "Test User");
    }
}

/// ## Main Application
#[tokio::main]
async fn main() -> Result<()> {
    println!("=== Rust Tokio with Reqwest & Serde Demo ===\n");
    
    // 1. Initialize API client
    println!("1. Initializing API Client...");
    let api_client = Arc::new(ApiClient::new("https://jsonplaceholder.typicode.com"));
    
    // 2. Setup repository and app state
    println!("2. Setting up Application State...");
    let repository: Arc<dyn UserRepository> = Arc::new(UserRepositoryImpl::new(Arc::clone(&api_client)));
    let app_state = Arc::new(AppState::new(Arc::clone(&repository)));
    
    // 3. Setup shutdown signal
    let shutdown_signal = tokio_util::sync::CancellationToken::new();
    
    // 4. Start background tasks
    println!("3. Starting Background Tasks...");
    let bg_task_handle = tokio::spawn(background_cache_cleaner(
        Arc::clone(&api_client),
        10, // Run every 10 seconds
        shutdown_signal.clone(),
    ));
    
    // 5. Subscribe to user creation events
    let repo_impl = repository.as_any().downcast_ref::<UserRepositoryImpl>()
        .expect("Repository should be UserRepositoryImpl");
    let mut user_created_rx = repo_impl.subscribe_to_creates();
    
    // Spawn task to listen for user creation events
    let event_listener_handle = tokio::spawn(async move {
        while let Ok(user) = user_created_rx.recv().await {
            println!("🎉 New user created event: {} ({})", user.name, user.email);
        }
    });
    
    // 6. Demonstrate JSON operations
    json_operations_example().await?;
    
    // 7. Make concurrent HTTP requests
    println!("\n=== Concurrent HTTP Requests ===");
    
    let user_ids = vec![1, 2, 3, 4, 5];
    let users_result = process_users_concurrently(
        Arc::clone(&app_state),
        user_ids.clone(),
    ).await;
    
    match users_result {
        Ok(users) => {
            println!("Successfully fetched {} users:", users.len());
            for user in users {
                println!("  - {}: {}", user.id, user.name);
            }
        }
        Err(e) => {
            eprintln!("Error fetching users: {:?}", e);
        }
    }
    
    // 8. Stream example
    println!("\n=== Streaming Users ===");
    let stream = api_client.stream_users(vec![6, 7, 8, 9, 10]).await;
    
    let mut user_count = 0;
    tokio::pin!(stream);
    
    while let Some(result) = stream.next().await {
        match result {
            Ok(user) => {
                user_count += 1;
                println!("Stream received user: {}", user.name);
            }
            Err(e) => {
                eprintln!("Stream error: {:?}", e);
            }
        }
    }
    println!("Stream completed. Received {} users.", user_count);
    
    // 9. Batch request example
    println!("\n=== Batch Request Example ===");
    match api_client.get_users_batch(vec![11, 12, 13]).await {
        Ok(users) => {
            println!("Batch request successful. Got {} users.", users.len());
        }
        Err(e) => {
            eprintln!("Batch request failed: {:?}", e);
        }
    }
    
    // 10. Create user example (commented out to avoid actual POST)
    println!("\n=== Create User Example ===");
    println!("Note: POST request is commented out to avoid actual API call");
    /*
    match api_client.create_user(CreateUserRequest {
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    }).await {
        Ok(user) => println!("Created user: {:?}", user),
        Err(e) => eprintln!("Failed to create user: {:?}", e),
    }
    */
    
    // 11. Demonstrate config update
    println!("\n=== Configuration Update ===");
    let current_config = app_state.get_config().await;
    println!("Current config: {:?}", current_config);
    
    let new_config = AppConfig {
        max_concurrent_requests: 10,
        ..current_config
    };
    
    app_state.update_config(new_config).await;
    println!("Config updated");
    
    // 12. Custom future example
    println!("\n=== Custom Future Example ===");
    let custom_future = DelayedHttpRequest::new(
        "https://jsonplaceholder.typicode.com/users/1".to_string()
    );
    
    // Note: This is a simplified example
    println!("Custom future created (would make HTTP request)");
    
    // 13. Graceful shutdown
    println!("\n=== Initiating Graceful Shutdown ===");
    
    // Send shutdown signal
    shutdown_signal.cancel();
    
    // Wait for background tasks
    tokio::select! {
        _ = bg_task_handle => println!("Background task shut down"),
        _ = event_listener_handle => println!("Event listener shut down"),
        _ = sleep(Duration::from_secs(2)) => println!("Shutdown timeout"),
    }
    
    println!("\n=== Application Shutdown Complete ===");
    Ok(())
}

// Helper trait for downcasting
trait AsAny {
    fn as_any(&self) -> &dyn std::any::Any;
}

impl AsAny for UserRepositoryImpl {
    fn as_any(&self) -> &dyn std::any::Any {
        self
    }
}

// If we want to use AsAny on trait objects
impl<T: 'static> AsAny for T {
    fn as_any(&self) -> &dyn std::any::Any {
        self
    }
}