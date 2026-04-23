//// RUST ERROR HANDLING STRATEGIES
/// From basic Result/Option to production-grade error handling with thiserror and anyhow
/// Covers error design patterns, best practices, and real-world scenarios

use std::fmt;
use std::error::Error;
use std::io;
use std::num::ParseIntError;

// ============================================================================
// 1. BASIC ERROR HANDLING REVIEW
// ============================================================================

/// Rust uses Result<T, E> for recoverable errors
/// Option<T> for values that might not exist
/// panic! for unrecoverable errors

fn basic_result() -> Result<i32, String> {
    Ok(42)
}

fn basic_option() -> Option<i32> {
    Some(42)
}

/// The ? operator propagates errors up the call stack
fn using_question_mark() -> Result<i32, String> {
    let value = basic_result()?; // If Err, returns early
    Ok(value * 2)
}


// ============================================================================
// 2. CUSTOM ERROR TYPES - MANUAL IMPLEMENTATION
// ============================================================================

/// Define your own error types for domain-specific errors
/// Must implement: Debug, Display, and optionally Error trait

#[derive(Debug)]
enum DatabaseError {
    ConnectionFailed,
    QueryFailed(String),
    NotFound,
}

impl fmt::Display for DatabaseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DatabaseError::ConnectionFailed => write!(f, "Failed to connect to database"),
            DatabaseError::QueryFailed(msg) => write!(f, "Query failed: {}", msg),
            DatabaseError::NotFound => write!(f, "Record not found"),
        }
    }
}

impl Error for DatabaseError {}

fn query_database() -> Result<String, DatabaseError> {
    Err(DatabaseError::NotFound)
}


// ============================================================================
// 3. ERROR CONVERSION WITH FROM TRAIT
// ============================================================================

/// Implement From trait to convert between error types
/// Enables ? operator to auto-convert errors

#[derive(Debug)]
struct AppError {
    kind: ErrorKind,
    message: String,
}

#[derive(Debug)]
enum ErrorKind {
    Io,
    Parse,
    Database,
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}: {}", self.kind, self.message)
    }
}

impl Error for AppError {}

// Convert io::Error to AppError
impl From<io::Error> for AppError {
    fn from(err: io::Error) -> Self {
        AppError {
            kind: ErrorKind::Io,
            message: err.to_string(),
        }
    }
}

// Convert ParseIntError to AppError
impl From<ParseIntError> for AppError {
    fn from(err: ParseIntError) -> Self {
        AppError {
            kind: ErrorKind::Parse,
            message: err.to_string(),
        }
    }
}

fn read_and_parse() -> Result<i32, AppError> {
    // Both errors auto-convert to AppError
    let content = std::fs::read_to_string("number.txt")?; // io::Error -> AppError
    let number: i32 = content.trim().parse()?; // ParseIntError -> AppError
    Ok(number)
}


// ============================================================================
// 4. THISERROR - DERIVE ERROR TYPES
// ============================================================================

/// thiserror provides derive macros for error types
/// Automatically implements Display and Error traits
/// Simplifies error definition

/*
use thiserror::Error;

#[derive(Error, Debug)]
enum ApiError {
    #[error("Network error: {0}")]
    Network(String),
    
    #[error("Authentication failed")]
    AuthError,
    
    #[error("Rate limit exceeded, retry after {retry_after}s")]
    RateLimit { retry_after: u64 },
    
    #[error("Parse error")]
    Parse(#[from] ParseIntError),  // Auto-implement From
    
    #[error("IO error")]
    Io(#[from] io::Error),  // Auto-implement From
}

// Usage
fn make_api_call() -> Result<String, ApiError> {
    Err(ApiError::Network("Connection refused".to_string()))
}

// The ? operator works seamlessly
fn api_workflow() -> Result<(), ApiError> {
    let data = std::fs::read_to_string("config.json")?;  // auto-converts io::Error
    let port: u16 = data.trim().parse()?;  // auto-converts ParseIntError
    Ok(())
}
*/


// ============================================================================
// 5. ANYHOW - SIMPLIFIED ERROR HANDLING
// ============================================================================

/// anyhow provides a single error type for applications
/// Use for: Applications, not libraries
/// Benefits: Simple, context, backtraces

/*
use anyhow::{Result, Context, anyhow, bail};

// Simple Result type alias - can hold any error
fn read_config() -> Result<String> {
    let path = "config.toml";
    
    // Add context to errors for better debugging
    let content = std::fs::read_to_string(path)
        .context(format!("Failed to read config from {}", path))?;
    
    Ok(content)
}

// Create ad-hoc errors
fn validate_age(age: i32) -> Result<()> {
    if age < 0 {
        bail!("Age cannot be negative: {}", age);
    }
    
    if age > 150 {
        return Err(anyhow!("Age too high: {}", age));
    }
    
    Ok(())
}

// Context can be chained
fn complex_operation() -> Result<()> {
    read_config()
        .context("Loading configuration")
        .context("Application startup")?;
    Ok(())
}

// Error display shows full context chain:
// Error: Application startup
// Caused by:
//     0: Loading configuration
//     1: Failed to read config from config.toml
//     2: No such file or directory (os error 2)
*/


// ============================================================================
// 6. WHEN TO USE WHAT: THISERROR VS ANYHOW
// ============================================================================

/// THISERROR - Use in LIBRARIES
/// ✓ Define specific error types
/// ✓ Library consumers need to handle specific errors
/// ✓ Public API with typed errors
/// ✓ Pattern matching on error variants
/// 
/// Example: A database library
/*
#[derive(Error, Debug)]
pub enum DbError {
    #[error("Connection failed")]
    ConnectionFailed,
    #[error("Record not found")]
    NotFound,
}
*/

/// ANYHOW - Use in APPLICATIONS
/// ✓ Don't need specific error types
/// ✓ Just want to propagate errors up
/// ✓ Need context and backtraces
/// ✓ Error is logged, not matched
/// 
/// Example: CLI application
/*
fn main() -> Result<()> {
    let config = read_config()?;
    let db = connect_database(&config)?;
    run_migrations(&db)?;
    Ok(())
}
*/


// ============================================================================
// 7. ERROR HANDLING PATTERNS
// ============================================================================

/// Pattern 1: Error Wrapping - Add Context
fn read_user_file(user_id: u64) -> Result<String, AppError> {
    let path = format!("users/{}.json", user_id);
    
    match std::fs::read_to_string(&path) {
        Ok(content) => Ok(content),
        Err(e) => Err(AppError {
            kind: ErrorKind::Io,
            message: format!("Failed to read user {} from {}: {}", user_id, path, e),
        }),
    }
}

/// Pattern 2: Error Downgrading - Convert error to Option
fn try_parse_optional(s: &str) -> Option<i32> {
    s.parse().ok()  // Convert Result to Option, discarding error
}

/// Pattern 3: Error Recovery - Provide default
fn read_or_default(path: &str) -> String {
    std::fs::read_to_string(path).unwrap_or_else(|_| String::from("default"))
}

/// Pattern 4: Multiple Error Types - Early Returns
fn process_data(input: &str) -> Result<i32, Box<dyn Error>> {
    let trimmed = input.trim();
    
    if trimmed.is_empty() {
        return Err("Input is empty".into());
    }
    
    let number: i32 = trimmed.parse()?;
    
    if number < 0 {
        return Err("Number must be positive".into());
    }
    
    Ok(number * 2)
}


// ============================================================================
// 8. CUSTOM ERROR WITH CONTEXT
// ============================================================================

/// Advanced error type with source and context

#[derive(Debug)]
struct ContextualError {
    message: String,
    source: Option<Box<dyn Error + Send + Sync>>,
}

impl ContextualError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
            source: None,
        }
    }
    
    fn with_source<E>(message: impl Into<String>, error: E) -> Self
    where
        E: Error + Send + Sync + 'static,
    {
        Self {
            message: message.into(),
            source: Some(Box::new(error)),
        }
    }
}

impl fmt::Display for ContextualError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message)?;
        if let Some(source) = &self.source {
            write!(f, ": {}", source)?;
        }
        Ok(())
    }
}

impl Error for ContextualError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.source.as_ref().map(|e| e.as_ref() as &(dyn Error + 'static))
    }
}


// ============================================================================
// 9. VALIDATION ERRORS
// ============================================================================

/// Pattern for collecting multiple validation errors

#[derive(Debug)]
struct ValidationErrors {
    errors: Vec<String>,
}

impl ValidationErrors {
    fn new() -> Self {
        Self { errors: Vec::new() }
    }
    
    fn add(&mut self, error: String) {
        self.errors.push(error);
    }
    
    fn is_empty(&self) -> bool {
        self.errors.is_empty()
    }
    
    fn into_result(self) -> Result<(), Self> {
        if self.is_empty() {
            Ok(())
        } else {
            Err(self)
        }
    }
}

impl fmt::Display for ValidationErrors {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Validation failed:\n")?;
        for error in &self.errors {
            write!(f, "  - {}\n", error)?;
        }
        Ok(())
    }
}

impl Error for ValidationErrors {}

#[derive(Debug)]
struct UserInput {
    username: String,
    email: String,
    age: i32,
}

fn validate_user(input: &UserInput) -> Result<(), ValidationErrors> {
    let mut errors = ValidationErrors::new();
    
    if input.username.len() < 3 {
        errors.add("Username must be at least 3 characters".to_string());
    }
    
    if !input.email.contains('@') {
        errors.add("Email must contain @".to_string());
    }
    
    if input.age < 0 || input.age > 150 {
        errors.add("Age must be between 0 and 150".to_string());
    }
    
    errors.into_result()
}


// ============================================================================
// 10. OPTION VS RESULT
// ============================================================================

/// When to use Option<T>:
/// - Value might not exist (not an error condition)
/// - Example: Looking up in a map
fn find_user(id: u64) -> Option<String> {
    let users = vec![(1, "Alice"), (2, "Bob")];
    users.iter()
        .find(|(uid, _)| *uid == id)
        .map(|(_, name)| name.to_string())
}

/// When to use Result<T, E>:
/// - Operation can fail with an error
/// - Need to know why it failed
/// - Example: File I/O
fn read_file(path: &str) -> Result<String, io::Error> {
    std::fs::read_to_string(path)
}

/// Converting between them:
fn demo_option_result_conversion() {
    // Option -> Result
    let opt: Option<i32> = Some(42);
    let res: Result<i32, &str> = opt.ok_or("Value missing");
    
    // Result -> Option
    let res: Result<i32, String> = Ok(42);
    let opt: Option<i32> = res.ok();
}


// ============================================================================
// 11. ERROR CHAINING
// ============================================================================

/// Properly chain errors to preserve context

fn read_config_file() -> Result<String, io::Error> {
    std::fs::read_to_string("config.toml")
}

fn parse_config(content: &str) -> Result<Config, ParseError> {
    // Parsing logic
    Err(ParseError("Invalid TOML".to_string()))
}

#[derive(Debug)]
struct Config;

#[derive(Debug)]
struct ParseError(String);

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Parse error: {}", self.0)
    }
}

impl Error for ParseError {}

#[derive(Debug)]
enum ConfigError {
    Io(io::Error),
    Parse(ParseError),
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfigError::Io(e) => write!(f, "IO error: {}", e),
            ConfigError::Parse(e) => write!(f, "Parse error: {}", e),
        }
    }
}

impl Error for ConfigError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            ConfigError::Io(e) => Some(e),
            ConfigError::Parse(e) => Some(e),
        }
    }
}

impl From<io::Error> for ConfigError {
    fn from(err: io::Error) -> Self {
        ConfigError::Io(err)
    }
}

impl From<ParseError> for ConfigError {
    fn from(err: ParseError) -> Self {
        ConfigError::Parse(err)
    }
}

fn load_config() -> Result<Config, ConfigError> {
    let content = read_config_file()?;  // io::Error -> ConfigError
    let config = parse_config(&content)?;  // ParseError -> ConfigError
    Ok(config)
}


// ============================================================================
// 12. TRANSIENT VS PERMANENT ERRORS
// ============================================================================

/// Distinguish between retryable and permanent errors

#[derive(Debug)]
enum NetworkError {
    Transient(String),  // Can retry
    Permanent(String),  // Don't retry
}

impl NetworkError {
    fn is_retryable(&self) -> bool {
        matches!(self, NetworkError::Transient(_))
    }
}

impl fmt::Display for NetworkError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NetworkError::Transient(msg) => write!(f, "Transient error: {}", msg),
            NetworkError::Permanent(msg) => write!(f, "Permanent error: {}", msg),
        }
    }
}

impl Error for NetworkError {}

fn make_request() -> Result<String, NetworkError> {
    // Simulated network call
    Err(NetworkError::Transient("Connection timeout".to_string()))
}

fn retry_logic() -> Result<String, NetworkError> {
    for attempt in 1..=3 {
        match make_request() {
            Ok(result) => return Ok(result),
            Err(e) if e.is_retryable() => {
                println!("Attempt {} failed, retrying...", attempt);
                std::thread::sleep(std::time::Duration::from_secs(1));
                continue;
            }
            Err(e) => return Err(e),  // Permanent error, don't retry
        }
    }
    Err(NetworkError::Permanent("Max retries exceeded".to_string()))
}


// ============================================================================
// 13. LOGGING ERRORS
// ============================================================================

/// Best practices for logging errors in production

/*
use log::{error, warn, info};

fn handle_request() -> Result<(), AppError> {
    match process_request() {
        Ok(result) => {
            info!("Request processed successfully");
            Ok(())
        }
        Err(e) => {
            // Log with context
            error!("Request processing failed: {}", e);
            
            // Log source chain
            let mut source = e.source();
            while let Some(err) = source {
                error!("  Caused by: {}", err);
                source = err.source();
            }
            
            Err(e)
        }
    }
}
*/


// ============================================================================
// 14. BEST PRACTICES
// ============================================================================

/// ERROR HANDLING BEST PRACTICES:
/// 
/// 1. USE SPECIFIC ERROR TYPES IN LIBRARIES
///    - Let consumers handle errors appropriately
///    - Implement From for conversions
/// 
/// 2. USE ANYHOW IN APPLICATIONS
///    - Simplifies error propagation
///    - Add context at each layer
/// 
/// 3. AVOID PANIC IN LIBRARY CODE
///    - Use Result instead
///    - Let consumers decide how to handle
/// 
/// 4. PRESERVE ERROR CONTEXT
///    - Wrap errors with additional info
///    - Implement source() to chain errors
/// 
/// 5. FAIL FAST
///    - Validate input early
///    - Return errors immediately
/// 
/// 6. LOG ERRORS APPROPRIATELY
///    - Error: Requires attention
///    - Warn: Unexpected but handled
///    - Info: Normal operation
/// 
/// 7. DOCUMENT ERROR CONDITIONS
///    - What errors can occur
///    - When they occur
///    - How to handle them
/// 
/// 8. USE TYPE SYSTEM
///    - Encode error possibilities in types
///    - Result<T, E> documents fallibility
/// 
/// 9. AVOID STRINGLY-TYPED ERRORS
///    - Use enums, not String
///    - Enable exhaustive matching


// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

fn main() {
    println!("=== RUST ERROR HANDLING STRATEGIES ===\n");
    
    println!("--- Basic Errors ---");
    match query_database() {
        Ok(data) => println!("Data: {}", data),
        Err(e) => println!("Error: {}", e),
    }
    
    println!("\n--- Validation ---");
    let input = UserInput {
        username: "ab".to_string(),
        email: "invalid",
        age: 200,
    };
    
    match validate_user(&input) {
        Ok(_) => println!("Validation passed"),
        Err(e) => println!("{}", e),
    }
    
    println!("\n--- Option vs Result ---");
    match find_user(1) {
        Some(name) => println!("Found user: {}", name),
        None => println!("User not found"),
    }
    
    println!("\n--- Retry Logic ---");
    match retry_logic() {
        Ok(result) => println!("Success: {}", result),
        Err(e) => println!("Failed: {}", e),
    }
    
    println!("\n=== Complete ===");
}

/// KEY TAKEAWAYS:
/// 
/// ERROR TYPES:
/// - Result<T, E>: For recoverable errors
/// - Option<T>: For missing values
/// - panic!: For unrecoverable errors
/// 
/// LIBRARY vs APPLICATION:
/// - Libraries: Use thiserror, specific error types
/// - Applications: Use anyhow, simple error propagation
/// 
/// PATTERN MATCHING:
/// - Match on error variants for specific handling
/// - Use ? for simple propagation
/// - Add context with .context()
/// 
/// DEPENDENCIES:
/// ```toml
/// [dependencies]
/// thiserror = "1"  # For libraries
/// anyhow = "1"     # For applications
/// log = "0.4"      # For logging
/// ```
