//// 1. cargo: the Build & Package Manager
/// Cargo’s role
/// - Dependency management
/// - Builds, tests, benches
/// - Feature flags and profiles
/// - Workspace orchestration

//// 2. Cargo Features
/// What features are
/// - Compile-time flags
/// - Enable/disable code paths and dependencies
/// - Zero runtime cost

[features]
default = ["metrics"]
metrics = []
tls = ["rustls"]


#[cfg(feature = "metrics")]
fn record_metrics() {}


//// Why use features
/// - Optional dependencies
/// - Platform-specific functionality
/// - Reduce binary size
/// - Support multiple backends

//// 3. Cargo Profiles
/// What profiles control
/// - Optimization level
/// - Debug info
/// - LTO
/// - Panic strategy

[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
lto = true
panic = "abort"

//// When to customize
/// - Data-plane binaries → aggressive release
/// - Faster CI builds → tuned dev
/// - Smaller binaries → panic = "abort"

//// Data-plane angle
/// - panic = "abort" avoids unwinding cost
/// - LTO improves hot-path performance

//// 4. Cargo Workspaces
/// What a workspace is
/// - A collection of related crates
/// - Shared Cargo.lock
/// - Unified dependency resolution

[workspace]
members = ["core", "cli", "bench"]

//// Why use workspaces
/// - Large codebases
/// - Library + binary split
/// - Faster builds via shared artifacts
/// - Cleaner dependency graph

workspace/
 ├─ core/      # library
 ├─ dataplane/ # binary
 ├─ control/   # binary
 └─ common/    # shared utils

//// 5. rustfmt
/// What it does
/// - Canonical formatting
/// - Reduces diff noise
/// - Enforces team consistency

cargo fmt

//// Best practices
/// - Run on save
/// - Never bikeshed formatting
/// - Commit formatted code only

//// 6. clippy
/// What it is
/// - Linting tool for correctness, performance, idioms
/// - Goes far beyond compiler warnings

cargo clippy -- -D warnings

//// What clippy catches
/// - Inefficient iterators
/// - Suspicious clones
/// - Incorrect comparisons
/// - Lifetime and ownership smells

//// Production advice
/// - Treat clippy warnings as CI failures
/// - Allow lints explicitly when justified

#[allow(clippy::needless_collect)]

//// Unit Tests
/// What they are
/// - Test small, isolated pieces
/// - Live next to the code

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_header() {
        assert!(parse_header(&[0x01]).is_ok());
    }
}

/// Characteristics
/// - Fast
/// - Fine-grained
/// - Can access private items

/// Best for
/// - Algorithms
/// - Parsers
/// - Error cases


//// 8. Integration Tests
/// What they are
/// - Test public API behavior
/// - Live in tests/ directory

// tests/api.rs
use mycrate::run;

#[test]
fn runs_successfully() {
    assert!(run().is_ok());
}

/// Characteristics
/// - Use crate as an external consumer
/// - Slower but more realistic
/// - No access to private internals


//// 9. Doc Tests
/// What they are
/// - Code blocks in documentation that compile and run
/// - Executed by cargo test

/// Adds two numbers.
///
/// ```
/// use mycrate::add;
/// assert_eq!(add(2, 2), 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Why they matter
/// - Documentation stays correct
/// - Users learn by example
/// - API changes break docs early

/// Doc test tips
/// - Keep examples minimal
/// - Prefer /// over //! for APIs
/// - Use no_run when needed

/// ```no_run
/// start_server();
/// ```
/// 