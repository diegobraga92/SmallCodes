/*
Simple Logger
--------------------------------------------------------
- Log levels enum
- Thread-safe
- Output to stdout

Senior signal:
- Enum design
- Trait implementations
- API ergonomics
*/
use std::fmt;
use std::sync::Arc;
use std::thread;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum LogLevel {
    Error = 1,
    Warning = 2,
    Log = 3,
    Verbose = 4,
}

impl fmt::Display for LogLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            LogLevel::Error => "ERROR",
            LogLevel::Warning => "WARN",
            LogLevel::Log => "LOG",
            LogLevel::Verbose => "VERBOSE",
        };
        write!(f, "{}", s)
    }
}

struct Logger;

impl Logger {
    fn log(&self, level: LogLevel, message: &str) {
        println!("[{}] {}", level, message);
    }
}

fn main() {
    let logger = Arc::new(Logger);

    println!("--- Test 1: Basic logging ---");
    logger.log(LogLevel::Error, "Something failed");
    logger.log(LogLevel::Warning, "This is a warning");
    logger.log(LogLevel::Log, "Normal log message");
    logger.log(LogLevel::Verbose, "Verbose details");

    println!("\n--- Test 2: Multiple calls loop ---");
    for i in 0..5 {
        logger.log(LogLevel::Log, &format!("Loop iteration {}", i));
    }

    println!("\n--- Test 3: Multi-thread logging ---");
    let mut handles = vec![];

    for i in 0..3 {
        let logger_clone = Arc::clone(&logger);
        handles.push(thread::spawn(move || {
            for j in 0..5 {
                logger_clone.log(LogLevel::Log, &format!("Thread {} - message {}", i, j));
            }
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("\n--- Test 4: High concurrency stress test ---");
    let mut stress_handles = vec![];

    for i in 0..10 {
        let logger_clone = Arc::clone(&logger);
        stress_handles.push(thread::spawn(move || {
            logger_clone.log(LogLevel::Verbose, &format!("Stress thread {}", i));
        }));
    }

    for handle in stress_handles {
        handle.join().unwrap();
    }

    println!("\n--- Test 5: LogLevel ordering sanity check ---");
    assert!(LogLevel::Error < LogLevel::Warning);
    assert!(LogLevel::Warning < LogLevel::Log);
    assert!(LogLevel::Log < LogLevel::Verbose);

    println!("All tests completed successfully.");
}
