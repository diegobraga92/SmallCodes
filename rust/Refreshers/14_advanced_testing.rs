//// RUST ADVANCED TESTING AND BENCHMARKING
/// Comprehensive guide to testing strategies, advanced patterns, and performance benchmarking
/// in Rust from junior to senior level

// ============================================================================
// 1. BASIC TESTING REVIEW
// ============================================================================

/// Tests are functions annotated with #[test]
/// Run with: cargo test
/// Assertions: assert!, assert_eq!, assert_ne!

#[test]
fn basic_test() {
    assert_eq!(2 + 2, 4);
    assert!(true);
    assert_ne!(5, 6);
}

#[test]
#[should_panic]
fn test_should_panic() {
    panic!("This test should panic!");
}

#[test]
#[should_panic(expected = "division by zero")]
fn test_panic_message() {
    let _ = 10 / 0;
}

#[test]
#[ignore]
fn expensive_test() {
    // Run with: cargo test -- --ignored
    // Expensive tests that shouldn't run normally
}


// ============================================================================
// 2. TEST ORGANIZATION
// ============================================================================

/// Tests can be organized in multiple ways:
/// 1. Inline tests in the same file
/// 2. Tests module at bottom of file
/// 3. Separate tests/ directory for integration tests

// Example: Tests module (most common pattern)
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_in_module() {
        assert_eq!(add(2, 3), 5);
    }
    
    // Helper functions for tests
    fn setup() -> TestContext {
        TestContext {
            value: 42
        }
    }
    
    struct TestContext {
        value: i32,
    }
}

fn add(a: i32, b: i32) -> i32 {
    a + b
}


// ============================================================================
// 3. RESULT-BASED TESTS
// ============================================================================

/// Tests can return Result<(), E> for cleaner error handling
/// Use ? operator instead of unwrap()

#[test]
fn test_with_result() -> Result<(), String> {
    let result = try_operation()?;
    assert_eq!(result, 42);
    Ok(())
}

fn try_operation() -> Result<i32, String> {
    Ok(42)
}


// ============================================================================
// 4. TESTING PRIVATE FUNCTIONS
// ============================================================================

/// Tests in the same module can access private functions
/// Use #[cfg(test)] module to keep tests close to code

fn private_function(x: i32) -> i32 {
    x * 2
}

#[cfg(test)]
mod private_tests {
    use super::*;
    
    #[test]
    fn test_private_function() {
        assert_eq!(private_function(5), 10);
    }
}


// ============================================================================
// 5. INTEGRATION TESTS
// ============================================================================

/// Integration tests go in tests/ directory
/// Each file in tests/ is a separate crate
/// Can only test public API
///
/// Example: tests/integration_test.rs
/// ```rust
/// use my_crate::public_function;
/// 
/// #[test]
/// fn test_public_api() {
///     assert_eq!(public_function(), 42);
/// }
/// ```


// ============================================================================
// 6. TEST FIXTURES AND SETUP/TEARDOWN
// ============================================================================

/// Rust doesn't have built-in setup/teardown
/// Use helper functions or RAII pattern

struct TestDatabase {
    path: String,
}

impl TestDatabase {
    fn new() -> Self {
        // Setup
        let path = "/tmp/test.db".to_string();
        println!("Setting up test database: {}", path);
        TestDatabase { path }
    }
}

impl Drop for TestDatabase {
    fn drop(&mut self) {
        // Teardown
        println!("Cleaning up test database: {}", self.path);
    }
}

#[test]
fn test_with_fixture() {
    let db = TestDatabase::new();
    // Test code
    assert!(db.path.contains("test"));
    // db is automatically dropped here
}


// ============================================================================
// 7. PROPERTY-BASED TESTING WITH QUICKCHECK
// ============================================================================

/// Property-based testing generates random inputs
/// Tests properties that should always hold true

/*
use quickcheck::{quickcheck, TestResult};
use quickcheck_macros::quickcheck;

// Property: reversing a vector twice gives original
#[quickcheck]
fn prop_reverse_reverse(xs: Vec<i32>) -> bool {
    let mut ys = xs.clone();
    ys.reverse();
    ys.reverse();
    xs == ys
}

// Property with custom logic
#[quickcheck]
fn prop_sorted_is_ordered(mut xs: Vec<i32>) -> bool {
    xs.sort();
    xs.windows(2).all(|w| w[0] <= w[1])
}

// Conditional property testing
fn prop_division(x: i32, y: i32) -> TestResult {
    if y == 0 {
        return TestResult::discard(); // Skip this case
    }
    TestResult::from_bool((x / y) * y + (x % y) == x)
}
*/


// ============================================================================
// 8. MOCKING AND TEST DOUBLES
// ============================================================================

/// Rust uses traits for mocking
/// Pattern: Define trait, implement for real and mock types

trait UserRepository {
    fn get_user(&self, id: u64) -> Option<User>;
    fn save_user(&mut self, user: User) -> Result<(), String>;
}

#[derive(Debug, Clone, PartialEq)]
struct User {
    id: u64,
    name: String,
}

// Real implementation
struct PostgresUserRepository {
    // connection details
}

impl UserRepository for PostgresUserRepository {
    fn get_user(&self, id: u64) -> Option<User> {
        // Real database query
        None
    }
    
    fn save_user(&mut self, user: User) -> Result<(), String> {
        // Real database save
        Ok(())
    }
}

// Mock implementation for testing
struct MockUserRepository {
    users: std::collections::HashMap<u64, User>,
}

impl MockUserRepository {
    fn new() -> Self {
        Self {
            users: std::collections::HashMap::new(),
        }
    }
}

impl UserRepository for MockUserRepository {
    fn get_user(&self, id: u64) -> Option<User> {
        self.users.get(&id).cloned()
    }
    
    fn save_user(&mut self, user: User) -> Result<(), String> {
        self.users.insert(user.id, user);
        Ok(())
    }
}

#[cfg(test)]
mod mock_tests {
    use super::*;
    
    #[test]
    fn test_with_mock() {
        let mut repo = MockUserRepository::new();
        
        let user = User {
            id: 1,
            name: "Alice".to_string(),
        };
        
        repo.save_user(user.clone()).unwrap();
        assert_eq!(repo.get_user(1), Some(user));
    }
}


// ============================================================================
// 9. MOCKALL - POWERFUL MOCKING LIBRARY
// ============================================================================

/// mockall generates mocks automatically from traits

/*
use mockall::{automock, predicate::*};

#[automock]
trait Calculator {
    fn add(&self, a: i32, b: i32) -> i32;
    fn divide(&self, a: i32, b: i32) -> Result<i32, String>;
}

#[cfg(test)]
mod mockall_tests {
    use super::*;
    
    #[test]
    fn test_calculator_mock() {
        let mut mock = MockCalculator::new();
        
        // Set expectations
        mock.expect_add()
            .with(eq(2), eq(3))
            .times(1)
            .returning(|a, b| a + b);
        
        // Use mock
        assert_eq!(mock.add(2, 3), 5);
    }
    
    #[test]
    fn test_divide_mock() {
        let mut mock = MockCalculator::new();
        
        mock.expect_divide()
            .with(eq(10), eq(0))
            .returning(|_, _| Err("division by zero".to_string()));
        
        assert!(mock.divide(10, 0).is_err());
    }
}
*/


// ============================================================================
// 10. SNAPSHOT TESTING WITH INSTA
// ============================================================================

/// Snapshot testing compares output against saved snapshots
/// Useful for testing complex outputs (JSON, HTML, etc.)

/*
use insta::assert_snapshot;

#[test]
fn test_json_output() {
    let data = User {
        id: 1,
        name: "Alice".to_string(),
    };
    
    let json = serde_json::to_string_pretty(&data).unwrap();
    assert_snapshot!(json);
}

#[test]
fn test_debug_output() {
    let data = vec![1, 2, 3, 4, 5];
    assert_snapshot!(format!("{:?}", data));
}
*/


// ============================================================================
// 11. TESTING ASYNC CODE
// ============================================================================

/// Use tokio::test or async-std::test for async tests

/*
#[tokio::test]
async fn test_async_function() {
    let result = async_operation().await;
    assert_eq!(result, 42);
}

async fn async_operation() -> i32 {
    tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
    42
}

// Test concurrent operations
#[tokio::test]
async fn test_concurrent() {
    let (r1, r2) = tokio::join!(
        async_operation(),
        async_operation()
    );
    assert_eq!(r1, r2);
}
*/


// ============================================================================
// 12. CRITERION - BENCHMARKING FRAMEWORK
// ============================================================================

/// Criterion provides statistical benchmarking
/// More accurate than built-in #[bench] (which is unstable)

/*
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn fibonacci_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, fibonacci_benchmark);
criterion_main!(benches);
*/

/// Cargo.toml configuration:
/// ```toml
/// [[bench]]
/// name = "my_benchmark"
/// harness = false
/// 
/// [dev-dependencies]
/// criterion = "0.5"
/// ```
///
/// Run with: cargo bench


// ============================================================================
// 13. ADVANCED BENCHMARKING PATTERNS
// ============================================================================

/*
fn advanced_benchmarks(c: &mut Criterion) {
    // Benchmark with different inputs
    let mut group = c.benchmark_group("sorting");
    for size in [10, 100, 1000].iter() {
        group.bench_with_input(
            format!("vec size {}", size),
            size,
            |b, &size| {
                b.iter(|| {
                    let mut vec: Vec<i32> = (0..size).collect();
                    vec.sort();
                });
            },
        );
    }
    group.finish();
    
    // Benchmark with setup
    c.bench_function("with_setup", |b| {
        let data = vec![1, 2, 3, 4, 5]; // Setup outside iteration
        b.iter(|| {
            let sum: i32 = data.iter().sum();
            black_box(sum); // Prevent optimization
        });
    });
    
    // Compare implementations
    let mut group = c.benchmark_group("string_concat");
    group.bench_function("String::push_str", |b| {
        b.iter(|| {
            let mut s = String::new();
            for i in 0..100 {
                s.push_str("test");
            }
        });
    });
    
    group.bench_function("format!", |b| {
        b.iter(|| {
            let mut s = String::new();
            for i in 0..100 {
                s = format!("{}test", s);
            }
        });
    });
    group.finish();
}
*/


// ============================================================================
// 14. PERFORMANCE PROFILING
// ============================================================================

/// Tools for finding performance bottlenecks:
/// 
/// 1. CARGO-FLAMEGRAPH
///    cargo install flamegraph
///    cargo flamegraph --bin my_app
///    Generates flamegraph.svg showing where time is spent
/// 
/// 2. VALGRIND/CALLGRIND
///    valgrind --tool=callgrind target/release/my_app
///    kcachegrind callgrind.out.*
///    Shows detailed call graphs and cache usage
/// 
/// 3. PERF (Linux)
///    perf record target/release/my_app
///    perf report
///    System-level profiling
/// 
/// 4. CARGO-INSTRUMENTS (macOS)
///    cargo install cargo-instruments
///    cargo instruments -t time
///    Uses Xcode Instruments


// ============================================================================
// 15. MICRO-BENCHMARKING BEST PRACTICES
// ============================================================================

/// TIPS FOR ACCURATE BENCHMARKS:
/// 
/// 1. Use black_box() to prevent compiler optimizations
/// 2. Run in release mode (cargo bench always uses --release)
/// 3. Warm up before measuring
/// 4. Measure multiple times and use statistics
/// 5. Be aware of CPU frequency scaling
/// 6. Close other programs to reduce noise
/// 7. Benchmark relative performance, not absolute

fn demonstrate_black_box() {
    // Without black_box, compiler might optimize away
    /*
    let result = 2 + 2;
    // Compiler: "I know this is 4, no need to compute"
    */
    
    // With black_box, compiler must compute
    /*
    let result = black_box(2) + black_box(2);
    // Compiler: "I don't know what black_box returns"
    */
}


// ============================================================================
// 16. FUZZING WITH CARGO-FUZZ
// ============================================================================

/// Fuzzing finds bugs by feeding random inputs
/// 
/// Setup:
/// ```bash
/// cargo install cargo-fuzz
/// cargo fuzz init
/// ```
/// 
/// Create fuzz target in fuzz/fuzz_targets/fuzz_target_1.rs:
/// ```rust
/// #![no_main]
/// use libfuzzer_sys::fuzz_target;
/// 
/// fuzz_target!(|data: &[u8]| {
///     // Test your function with random data
///     if let Ok(s) = std::str::from_utf8(data) {
///         my_parser(s);
///     }
/// });
/// ```
/// 
/// Run: cargo fuzz run fuzz_target_1


// ============================================================================
// 17. CODE COVERAGE
// ============================================================================

/// Measure test coverage using cargo-tarpaulin or cargo-llvm-cov
/// 
/// TARPAULIN:
/// ```bash
/// cargo install cargo-tarpaulin
/// cargo tarpaulin --out Html
/// ```
/// 
/// LLVM-COV (more accurate):
/// ```bash
/// cargo install cargo-llvm-cov
/// cargo llvm-cov --html
/// ```
/// 
/// Generates HTML report showing which lines are tested


// ============================================================================
// 18. TEST ORGANIZATION PATTERNS
// ============================================================================

/// Pattern 1: Builder pattern for test data
#[cfg(test)]
mod builder_tests {
    use super::*;
    
    struct UserBuilder {
        id: u64,
        name: String,
    }
    
    impl UserBuilder {
        fn new() -> Self {
            Self {
                id: 1,
                name: "Test User".to_string(),
            }
        }
        
        fn with_id(mut self, id: u64) -> Self {
            self.id = id;
            self
        }
        
        fn with_name(mut self, name: impl Into<String>) -> Self {
            self.name = name.into();
            self
        }
        
        fn build(self) -> User {
            User {
                id: self.id,
                name: self.name,
            }
        }
    }
    
    #[test]
    fn test_with_builder() {
        let user = UserBuilder::new()
            .with_id(42)
            .with_name("Alice")
            .build();
        
        assert_eq!(user.id, 42);
        assert_eq!(user.name, "Alice");
    }
}

/// Pattern 2: Test modules per function
mod my_function {
    pub fn process(input: i32) -> i32 {
        input * 2
    }
    
    #[cfg(test)]
    mod tests {
        use super::*;
        
        #[test]
        fn positive_input() {
            assert_eq!(process(5), 10);
        }
        
        #[test]
        fn negative_input() {
            assert_eq!(process(-5), -10);
        }
        
        #[test]
        fn zero_input() {
            assert_eq!(process(0), 0);
        }
    }
}


// ============================================================================
// 19. TESTING BEST PRACTICES
// ============================================================================

/// BEST PRACTICES:
/// 
/// 1. TEST NAMING
///    - Use descriptive names: test_divide_by_zero_returns_error
///    - Pattern: test_[function]_[condition]_[expected_result]
/// 
/// 2. ARRANGE-ACT-ASSERT (AAA)
///    - Arrange: Set up test data
///    - Act: Execute the code being tested
///    - Assert: Verify the result
/// 
/// 3. ONE ASSERTION PER TEST
///    - Each test should verify one thing
///    - Makes failures easier to diagnose
/// 
/// 4. AVOID TEST INTERDEPENDENCIES
///    - Tests should be independent
///    - Should pass in any order
/// 
/// 5. TEST EDGE CASES
///    - Empty collections
///    - Null/None values
///    - Boundary values (0, -1, MAX)
/// 
/// 6. FAST TESTS
///    - Keep unit tests fast (<1ms)
///    - Use #[ignore] for slow tests
/// 
/// 7. DON'T TEST IMPLEMENTATION
///    - Test behavior, not implementation details
///    - Refactoring shouldn't break tests

#[cfg(test)]
mod best_practice_tests {
    #[test]
    fn test_add_positive_numbers_returns_sum() {
        // Arrange
        let a = 2;
        let b = 3;
        
        // Act
        let result = a + b;
        
        // Assert
        assert_eq!(result, 5);
    }
}


// ============================================================================
// 20. MUTATION TESTING
// ============================================================================

/// Mutation testing modifies code to see if tests catch bugs
/// Use cargo-mutants:
/// 
/// ```bash
/// cargo install cargo-mutants
/// cargo mutants
/// ```
/// 
/// It will:
/// 1. Modify your code (mutate)
/// 2. Run tests
/// 3. Report if tests caught the mutation
/// 
/// High mutation score = good test coverage


// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

fn main() {
    println!("=== RUST ADVANCED TESTING & BENCHMARKING ===\n");
    
    println!("TESTING STRATEGIES:");
    println!("  ✓ Unit tests with #[test]");
    println!("  ✓ Integration tests in tests/");
    println!("  ✓ Property-based testing");
    println!("  ✓ Mocking with traits");
    println!("  ✓ Snapshot testing");
    println!("  ✓ Async testing");
    
    println!("\nBENCHMARKING:");
    println!("  ✓ Criterion for statistical benchmarks");
    println!("  ✓ Flamegraphs for profiling");
    println!("  ✓ Black box to prevent optimization");
    
    println!("\nQUALITY TOOLS:");
    println!("  ✓ Fuzzing with cargo-fuzz");
    println!("  ✓ Coverage with cargo-tarpaulin");
    println!("  ✓ Mutation testing with cargo-mutants");
    
    println!("\nRun tests: cargo test");
    println!("Run benchmarks: cargo bench");
    println!("Run ignored tests: cargo test -- --ignored");
    println!("Run specific test: cargo test test_name");
}

/// RECOMMENDED DEV-DEPENDENCIES:
/// ```toml
/// [dev-dependencies]
/// quickcheck = "1"
/// quickcheck_macros = "1"
/// mockall = "0.12"
/// insta = "1"
/// tokio = { version = "1", features = ["test-util"] }
/// criterion = "0.5"
/// ```
