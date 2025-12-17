//// Option<T> and Result<T, E>
// Option, used for function that might not return a value, such as searches in collections, or safe access to data
enum Option<T> {
    Some(T),  // A value exists
    None,     // No value
}

fn find_port(env: &str) -> Option<u16> {
    if env == "prod" {
        Some(443)
    } else {
        None
    }
}

// Common methods
opt.is_some()
opt.is_none()
opt.unwrap_or(80)
opt.map(|v| v + 1)

// Result, for operations that can fail (e.g. IO), need to return error info or recoverable errors. Error Recovery
enum Result<T, E> {
    Ok(T),   // Operation succeeded
    Err(E),  // Operation failed with error E
}

fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.parse()
}
// Both can be used at the same time with Result<Option<T>, E>

/// map()
// Transforms Ok value, leaves Err unchanged
fn parse_and_double(s: &str) -> Result<i32, std::num::ParseIntError> {
    s.parse::<i32>().map(|n| n * 2)
}

let result = parse_and_double("42");
assert_eq!(result, Ok(84));

let err_result = parse_and_double("not a number");
assert!(err_result.is_err());

// Real-world example: Config processing
fn get_port(config: &Config) -> Result<u16, ConfigError> {
    config.get("port")
        .map(|port_str| port_str.parse())
        .map_err(|e| ConfigError::MissingKey("port".to_string()))?
        .map(|port| port.clamp(1, 65535))
        .map_err(|e| ConfigError::InvalidPort(e))
}

/// map_err, transform error value:
// Transforms Err value, leaves Ok unchanged
enum ApiError {
    Network(String),
    Parse(String),
    Auth(String),
}

fn fetch_data() -> Result<String, ApiError> {
    reqwest::blocking::get("https://api.example.com/data")
        .map_err(|e| ApiError::Network(e.to_string()))?
        .text()
        .map_err(|e| ApiError::Parse(e.to_string()))
}

// Multiple error conversions in a chain
fn process_file(path: &str) -> Result<String, AppError> {
    std::fs::read_to_string(path)
        .map_err(|io_err| AppError::Io {
            path: path.to_string(),
            source: io_err,
        })
        .and_then(|content| {
            serde_json::from_str(&content)
                .map_err(|parse_err| AppError::Parse {
                    path: path.to_string(),
                    source: parse_err,
                })
        })
}

// map_or and map_or_else
// map_or: Transform Ok or use default
let x: Result<&str, &str> = Ok("foo");
assert_eq!(x.map_or(42, |v| v.len()), 3);

let y: Result<&str, &str> = Err("error");
assert_eq!(y.map_or(42, |v| v.len()), 42);

// map_or_else: Transform Ok or compute default from error
fn compute_length(result: Result<String, String>) -> usize {
    result.map_or_else(
        |err| err.len(),  // Use error length if Err
        |ok| ok.len(),    // Use value length if Ok
    )
}

// Practical example: Database query with fallback
fn get_user_name(user_id: u64) -> String {
    database::find_user(user_id)
        .map(|user| user.name)
        .map_or_else(
            |_| "Unknown User".to_string(),
            |name| name,
        )
}

/// and_then
// Also known as flat_map or bind
// Takes a function that returns Result<T, E>

fn parse_and_validate(s: &str) -> Result<i32, String> {
    s.parse::<i32>()
        .map_err(|e| format!("Parse error: {}", e))
        .and_then(|n| {
            if n >= 0 && n <= 100 {
                Ok(n)
            } else {
                Err("Value out of range".to_string())
            }
        })
}
 
/// or_else
// Try alternative if first operation fails

fn read_config() -> Result<Config, ConfigError> {
    read_config_from_file("/etc/app/config.toml")
        .or_else(|_| read_config_from_file("./config.toml"))
        .or_else(|_| read_config_from_env())
        .or_else(|_| Ok(Config::default()))
}


/// and / or:
// and: Returns second result if both are Ok, otherwise first Err
let x: Result<u32, &str> = Ok(2);
let y: Result<&str, &str> = Ok("foo");
assert_eq!(x.and(y), Ok("foo"));

let z: Result<u32, &str> = Err("early error");
let w: Result<&str, &str> = Ok("foo");
assert_eq!(z.and(w), Err("early error"));

// or: Returns first Ok, otherwise second result
let a: Result<u32, &str> = Ok(2);
let b: Result<u32, &str> = Err("later error");
assert_eq!(a.or(b), Ok(2));

let c: Result<u32, &str> = Err("early error");
let d: Result<u32, &str> = Err("later error");
assert_eq!(c.or(d), Err("later error"));


/// inspect and inspect_err
// Inspect values without consuming them (Rust 1.76+)
use std::fs;

fn process_file(path: &str) -> Result<String, std::io::Error> {
    fs::read_to_string(path)
        .inspect(|content| {
            println!("Read {} bytes from {}", content.len(), path);
        })
        .inspect_err(|err| {
            eprintln!("Failed to read {}: {}", path, err);
        })
}



//// unwrap() and expect()
// unwrap extracts value from Some or Ok, or panics:
let some_value = Some(42);
let value = some_value.unwrap();  // 42

let none_value: Option<i32> = None;
// let value = none_value.unwrap();  // PANICS: "called `Option::unwrap()` on a `None` value"

let ok_result: Result<i32, &str> = Ok(100);
let ok_value = ok_result.unwrap();  // 100

let err_result: Result<i32, &str> = Err("failure");
// let value = err_result.unwrap();  // PANICS: "called `Result::unwrap()` on an `Err` value"

// expect works similarly, but has a custom error message
let some_value = Some(42);
let value = some_value.expect("Should have a value");  // 42

let none_value: Option<i32> = None;
// let value = none_value.expect("Value is missing");  
// PANICS: "Value is missing: called `Option::unwrap()` on a `None` value"

let err_result: Result<i32, &str> = Err("database error");
// let value = err_result.expect("Failed to read database");
// PANICS: "Failed to read database: database error"

// Safer alternatives, unwrap is best to be avoided in prod, unless failure is impossible or unrecoverable
// Instead of unwrap():
let value = some_option.unwrap_or(default_value);
let value = some_option.unwrap_or_else(|| calculate_default());

// Instead of expect():
match some_result {
    Ok(value) => process(value),
    Err(e) => handle_error(e),  // Graceful error handling
}



//// ? Operator (Try Operator), propagates error or None up the call stack
fn read_config() -> Result<String, io::Error> {
    let mut file = File::open("config.txt")?;  // Returns early if Err
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;  // Returns early if Err
    Ok(contents)
}

// ? is the same as this:
// This:
let result = function_that_returns_result()?;

// Is equivalent to:
let result = match function_that_returns_result() {
    Ok(value) => value,
    Err(e) => return Err(e.into()),  // Note: converts error if needed
};


// Can be used with Option:
fn get_first_char(s: &str) -> Option<char> {
    let first = s.chars().next()?;  // Returns None if string is empty
    Some(first.to_uppercase().next()?)
}

// Equivalent to:
fn get_first_char_manual(s: &str) -> Option<char> {
    let first = match s.chars().next() {
        Some(c) => c,
        None => return None,
    };
    match first.to_uppercase().next() {
        Some(uc) => Some(uc),
        None => return None,
    }
}

// Error Type conversion
use std::fs;
use std::io;

// Different error types
fn read_and_parse() -> Result<i32, io::Error> {
    let contents = fs::read_to_string("data.txt")?;  // io::Error
    let number: i32 = contents.trim().parse()
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
    Ok(number)
}

// Or use a custom error enum (see section 4)
fn process_data() -> Result<i32, MyError> {
    let contents = fs::read_to_string("data.txt")
        .map_err(MyError::Io)?;  // Convert io::Error to MyError
    
    let number: i32 = contents.trim().parse()
        .map_err(MyError::Parse)?;  // Convert parse error to MyError
    
    Ok(number)
}

// It only works in functions that return Result or Option
// The ? operator works in functions that return Result or Option
fn valid_use() -> Result<(), io::Error> {
    let _file = File::open("test.txt")?;  // OK
    Ok(())
}

fn also_valid() -> Option<()> {
    let value = Some(42)?;  // OK
    Some(())
}

// ERROR: main doesn't return Result/Option
fn main() {
    // let file = File::open("test.txt")?;  // Won't compile!
}

// FIX: Change main's return type
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("test.txt")?;  // Now it works!
    Ok(())
}


/// FromResidual, is how ? knows how to turn one error type into another
// How ? works with FromResidual:
// expr? becomes:
match Try::branch(expr) {
    ControlFlow::Continue(v) => v,
    ControlFlow::Break(r) => return FromResidual::from_residual(r),
}



//// Custom Error Enums, better to use custom errors than String propagation everywhere
#[derive(Debug)]  // Allows printing with {:?}
enum AppError {
    FileNotFound(String),
    ParseError(String),
    ValidationError { field: String, reason: String },
    NetworkError(u32),  // HTTP status code
}

impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::FileNotFound(path) => 
                write!(f, "File not found: {}", path),
            AppError::ParseError(msg) => 
                write!(f, "Parse error: {}", msg),
            AppError::ValidationError { field, reason } => 
                write!(f, "Validation failed for {}: {}", field, reason),
            AppError::NetworkError(code) => 
                write!(f, "Network error with status: {}", code),
        }
    }
}

impl std::error::Error for AppError {}  // Implement the Error trait

// Using custom errors
fn read_config_file(path: &str) -> Result<String, AppError> {
    std::fs::read_to_string(path)
        .map_err(|_| AppError::FileNotFound(path.to_string()))
}

// Using with ?
// Now we can use `?` with automatic conversion
fn process_file(path: &str) -> Result<i32, MyError> {
    // io::Error automatically converts to MyError::Io
    let contents = std::fs::read_to_string(path)?;
    
    // ParseIntError automatically converts to MyError::Parse
    let number: i32 = contents.trim().parse()?;
    
    if number < 0 {
        return Err(MyError::Custom("Negative numbers not allowed".to_string()));
    }
    
    Ok(number)
}

// Error Patterns
// 1. Match all cases explicitly
fn handle_result(result: Result<i32, AppError>) {
    match result {
        Ok(value) => println!("Success: {}", value),
        Err(AppError::FileNotFound(path)) => 
            println!("Please create file: {}", path),
        Err(AppError::ParseError(_)) => 
            println!("Invalid format in config file"),
        Err(AppError::ValidationError { field, reason }) => 
            println!("Fix {}: {}", field, reason),
        Err(AppError::NetworkError(code)) if code == 404 => 
            println!("Resource not found"),
        Err(AppError::NetworkError(code)) => 
            println!("Network issue, code: {}", code),
    }
}

// 2. Using combinators
fn get_value_or_default() -> i32 {
    compute_value()
        .unwrap_or(0)                    // Default value
        .unwrap_or_else(|e| {            // Compute default on error
            eprintln!("Error: {}", e);
            fallback_value()
        })
}

// 3. Early return with ?
fn process_data_chain() -> Result<ProcessedData, AppError> {
    let input = read_input()?;
    let parsed = parse_input(&input)?;
    let validated = validate(&parsed)?;
    let transformed = transform(validated)?;
    Ok(transformed)
}



//// Custom Error Trait Object Types, more flexible, easy propagation, but bad for matching
// Using Box<dyn Error> for heterogeneous errors
use std::error::Error;

type GenericResult<T> = Result<T, Box<dyn Error + Send + Sync + 'static>>;

fn read_config() -> GenericResult<Config> {
    let path = std::env::var("CONFIG_PATH")?;  // std::env::VarError → Box<dyn Error>
    let file = std::fs::File::open(path)?;     // std::io::Error → Box<dyn Error>
    let config: Config = serde_yaml::from_reader(file)?; // serde_yaml::Error → Box<dyn Error>
    Ok(config)
}

// With additional context
fn process_with_context() -> Result<(), Box<dyn Error + Send + Sync>> {
    let data = load_data().context("Failed to load data")?;
    let result = transform(data).context("Failed to transform data")?;
    save_result(result).context("Failed to save result")?;
    Ok(())
}



//// Propagating Context with .inspect and .context
/// inspect for observability
// Rust 1.76+ stable inspect methods
use std::fs;

// Inspect success values
fn load_data(path: &str) -> Result<String, std::io::Error> {
    fs::read_to_string(path)
        .inspect(|content| {
            log::info!("Loaded {} bytes from {}", content.len(), path);
        })
        .inspect(|content| {
            if content.is_empty() {
                log::warn!("File {} is empty", path);
            }
        })
}

// Inspect errors
fn process_data(path: &str) -> Result<Data, ProcessError> {
    load_data(path)
        .inspect_err(|err| {
            log::error!("Failed to load {}: {}", path, err);
            metrics::increment("load_errors");
        })
        .and_then(|content| parse_data(&content))
        .inspect(|data| {
            log::debug!("Parsed data: {:?}", data);
        })
}

/// Context for error Context
use anyhow::{Context, Result};

// Adding context to errors
fn load_config() -> Result<Config> {
    let path = "config.toml";
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config file: {}", path))?;
    
    let config: Config = toml::from_str(&content)
        .context("Failed to parse config file")?;
    
    Ok(config)
}

// Context with lazy evaluation
fn complex_operation() -> Result<()> {
    let data = load_data()
        .with_context(|| {
            let timestamp = std::time::SystemTime::now();
            format!("Failed to load data at {:?}", timestamp)
        })?;
    
    process(&data)
        .context("Failed to process data")?;
    
    Ok(())
}



//// thiserror, Library for Custom Errors
/// Provide macro for implementing errors, auto Display and Error implementation
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Parse error at line {line}: {source}")]
    Parse {
        line: usize,
        #[source]
        source: std::num::ParseIntError,
    },
    
    #[error("Invalid data: expected {expected}, got {actual}")]
    InvalidData {
        expected: String,
        actual: String,
    },
    
    #[error("Timeout after {0} seconds")]
    Timeout(u64),
}

// Automatic From implementations with #[from]
fn read_file() -> Result<String, DataError> {
    let content = std::fs::read_to_string("data.txt")?;  // Automatically converts io::Error -> DataError::Io
    Ok(content)
}

#[derive(Error, Debug)]
pub enum ApplicationError {
    #[error("config error: {0}")]
    Config(#[from] ConfigError),
    
    #[error("database error: {0}")]
    Database(#[from] DatabaseError),
    
    // Transparent error wrapper - uses inner error's Display
    #[error(transparent)]
    Other(#[from] anyhow::Error),
    
    // Backtrace support (nightly Rust)
    #[error("internal error")]
    Internal {
        #[from]
        source: std::io::Error,
        backtrace: std::backtrace::Backtrace,
    },
}

// Contextual errors with source chaining
#[derive(Error, Debug)]
#[error("failed to process user {user_id}")]
pub struct ProcessingError {
    user_id: u64,
    #[source]
    source: anyhow::Error,
}



//// anyhow, Lib for easy error handling
/// Helpful for applications, adds context to errors, with easy propagation
use anyhow::{Context, Result, bail};

// Generic Result type
fn process_data(path: &str) -> Result<()> {
    let file = std::fs::File::open(path)
        .with_context(|| format!("Failed to open {}", path))?;
    
    let data = parse_file(&file)
        .context("Failed to parse file")?;
    
    if data.is_empty() {
        bail!("Empty data file");  // Shortcut to return error
    }
    
    Ok(())
}

// Function that can return any error
fn read_config() -> Result<Config> {
    let config_str = std::fs::read_to_string("config.toml")?;
    let config: Config = toml::from_str(&config_str)?;
    Ok(config)
}

// Creating errors with context
fn validate_user(user: &User) -> Result<()> {
    if user.age < 13 {
        anyhow::bail!("User {} is too young (age: {})", user.name, user.age);
    }
    
    if !user.email.contains('@') {
        return Err(anyhow::anyhow!("Invalid email for user {}", user.name));
    }
    
    Ok(())
}

use anyhow::{Context, Result};

fn complex_operation() -> Result<Vec<Data>> {
    let config = load_config()
        .context("Loading configuration")?;
    
    let connection = connect_db(&config.db_url)
        .with_context(|| format!("Connecting to database at {}", config.db_url))?;
    
    let data = fetch_data(&connection)
        .context("Fetching data from database")?;
    
    let processed = process(&data)
        .context("Processing fetched data")?;
    
    Ok(processed)
}

// When this fails, you get a chain of context:
// "Processing fetched data"
// "Fetching data from database"  
// "Connecting to database at localhost:5432"
// "Loading configuration"
// Original error: "Connection refused"



//// snafu, error handling lib, similar to thiserror, but more opinionated
use snafu::Snafu;

#[derive(Debug, Snafu)]
enum Error {
    #[snafu(display("failed to open {path}"))]
    OpenFile { path: String, source: std::io::Error },

    #[snafu(display("invalid config"))]
    InvalidConfig,
}


