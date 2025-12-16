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

// Result, for operations that can fail (e.g. IO), need to return error info or recoverable errors
enum Result<T, E> {
    Ok(T),   // Operation succeeded
    Err(E),  // Operation failed with error E
}

fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> {
    s.parse()
}
// Both can be used at the same time with Result<Option<T>, E>



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