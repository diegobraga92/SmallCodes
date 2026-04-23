//// RUST MACROS - FROM BASICS TO ADVANCED
/// Macros are metaprogramming constructs that write code at compile time.
/// They're more powerful than functions because they operate on syntax trees, not values.

// ============================================================================
// 1. DECLARATIVE MACROS (macro_rules!)
// ============================================================================

/// Declarative macros use pattern matching on Rust syntax
/// They're like match expressions but for code structure
/// Syntax: macro_rules! name { (pattern) => (expansion); }

// Simple declarative macro - no arguments
macro_rules! hello {
    () => {
        println!("Hello from macro!");
    };
}

// Macro with arguments - pattern matching
macro_rules! create_function {
    ($func_name:ident) => {
        fn $func_name() {
            println!("You called {:?}()", stringify!($func_name));
        }
    };
}

// Create multiple functions using the macro
create_function!(foo);
create_function!(bar);

fn demo_basic_macros() {
    hello!();
    foo();
    bar();
}


// ============================================================================
// 2. MACRO PATTERN MATCHING
// ============================================================================

/// Macros can have multiple arms like match expressions
/// Pattern types:
/// - $name:expr  - expressions (1 + 2, foo(), etc.)
/// - $name:ident - identifiers (variable/function names)
/// - $name:ty    - types (i32, String, etc.)
/// - $name:stmt  - statements
/// - $name:block - code blocks { ... }
/// - $name:item  - items (functions, structs, etc.)
/// - $name:pat   - patterns (for match arms)
/// - $name:path  - paths (std::collections::HashMap)
/// - $name:tt    - token tree (any single token)
/// - $name:meta  - attribute contents

macro_rules! calculate {
    // Single expression
    (eval $e:expr) => {
        {
            let val = $e;
            println!("{} = {}", stringify!($e), val);
        }
    };
    
    // Multiple expressions with repetition
    (eval $($e:expr),*) => {
        $(
            calculate!(eval $e);
        )*
    };
}

fn demo_pattern_matching() {
    calculate!(eval 1 + 2);
    calculate!(eval 5 * 3);
    calculate!(eval 1 + 2, 3 + 4, 5 * 6);
}


// ============================================================================
// 3. REPETITIONS IN MACROS
// ============================================================================

/// Repetition syntax: $( ... )*  or  $( ... )+  or  $( ... ),*
/// - * means zero or more
/// - + means one or more
/// - Can specify separators like commas

// Vector initialization macro similar to vec![]
macro_rules! my_vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

// HashMap initialization macro
macro_rules! hashmap {
    ( $( $key:expr => $val:expr ),* ) => {
        {
            let mut map = ::std::collections::HashMap::new();
            $(
                map.insert($key, $val);
            )*
            map
        }
    };
}

fn demo_repetitions() {
    let v = my_vec![1, 2, 3, 4, 5];
    println!("my_vec: {:?}", v);
    
    let map = hashmap! {
        "name" => "Alice",
        "role" => "Developer"
    };
    println!("hashmap: {:?}", map);
}


// ============================================================================
// 4. ADVANCED DECLARATIVE MACROS
// ============================================================================

/// Complex macros can implement mini DSLs (Domain-Specific Languages)
/// They can have nested patterns and recursive expansions

// Implement a simple test framework macro
macro_rules! test_suite {
    (
        $suite_name:ident {
            $( $test_name:ident: $test_body:expr ),* $(,)?
        }
    ) => {
        mod $suite_name {
            $(
                #[test]
                fn $test_name() {
                    $test_body
                }
            )*
        }
    };
}

// Usage example (commented out since it needs cfg(test))
/*
test_suite! {
    math_tests {
        addition: assert_eq!(2 + 2, 4),
        subtraction: assert_eq!(5 - 3, 2),
    }
}
*/

// Builder pattern macro
macro_rules! builder {
    (
        struct $name:ident {
            $( $field:ident: $field_type:ty ),* $(,)?
        }
    ) => {
        pub struct $name {
            $( pub $field: $field_type, )*
        }
        
        impl $name {
            pub fn new() -> Self {
                Self {
                    $( $field: Default::default(), )*
                }
            }
            
            $(
                paste::paste! {
                    pub fn [<with_ $field>](mut self, $field: $field_type) -> Self {
                        self.$field = $field;
                        self
                    }
                }
            )*
        }
    };
}

// Note: The builder macro above uses paste crate for identifier concatenation


// ============================================================================
// 5. PROCEDURAL MACROS - OVERVIEW
// ============================================================================

/// Procedural macros are more powerful - they're Rust functions that transform code
/// Three types:
/// 1. Function-like macros: custom!(...)
/// 2. Derive macros: #[derive(CustomDerive)]
/// 3. Attribute macros: #[custom_attribute]

/// Procedural macros must be defined in a separate crate with:
/// [lib]
/// proc-macro = true

/// They receive TokenStream as input and return TokenStream as output
/// Use syn crate for parsing and quote crate for code generation


// ============================================================================
// 6. DERIVE MACROS (USAGE)
// ============================================================================

/// Derive macros automatically implement traits
/// Common derives: Debug, Clone, Copy, PartialEq, Eq, Hash, Default

use std::fmt;

// Built-in derives
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct User {
    id: u64,
    name: String,
    email: String,
}

// Custom derive example (usage - implementation would be in proc-macro crate)
// This would typically generate From<Row> implementation for database mapping
/*
#[derive(FromRow)]
struct Post {
    id: i64,
    title: String,
    content: String,
}
*/

fn demo_derives() {
    let user = User {
        id: 1,
        name: "Alice".to_string(),
        email: "alice@example.com".to_string(),
    };
    
    // Debug trait allows {:?} formatting
    println!("{:?}", user);
    
    // Clone trait
    let user2 = user.clone();
    
    // PartialEq trait
    assert_eq!(user, user2);
}


// ============================================================================
// 7. ATTRIBUTE MACROS (USAGE)
// ============================================================================

/// Attribute macros transform the item they're attached to
/// Examples from popular crates:
/// - #[tokio::main] - creates async runtime
/// - #[derive(Serialize)] from serde
/// - #[get("/users")] from actix-web/axum

// Example: tokio's attribute macro
/*
#[tokio::main]
async fn main() {
    println!("Async main!");
}
*/

// Example: Custom attribute for logging (conceptual)
/*
#[log_execution]
fn expensive_operation() {
    // Macro would add timing and logging code
}
*/


// ============================================================================
// 8. FUNCTION-LIKE PROCEDURAL MACROS (USAGE)
// ============================================================================

/// Function-like macros look like declarative macros but are more flexible
/// Examples: sql!, html!, format_args!

// Example: SQL query macro from sqlx
/*
let users = sqlx::query!(
    "SELECT id, name FROM users WHERE active = ?",
    true
)
.fetch_all(&pool)
.await?;
*/


// ============================================================================
// 9. COMMON MACRO PATTERNS
// ============================================================================

/// Pattern 1: Conditional Compilation
macro_rules! log_debug {
    ($($arg:tt)*) => {
        #[cfg(debug_assertions)]
        {
            println!($($arg)*);
        }
    };
}

/// Pattern 2: Type-safe builder
macro_rules! method_builder {
    ($name:ident, $field:ident: $type:ty) => {
        pub fn $name(mut self, value: $type) -> Self {
            self.$field = value;
            self
        }
    };
}

/// Pattern 3: Generating similar implementations
macro_rules! impl_arithmetic {
    ($($t:ty),*) => {
        $(
            impl Addable for $t {
                fn add_custom(&self, other: &Self) -> Self {
                    self + other
                }
            }
        )*
    };
}

trait Addable {
    fn add_custom(&self, other: &Self) -> Self;
}

impl_arithmetic!(i32, i64, f32, f64);

fn demo_common_patterns() {
    log_debug!("Debug message: {}", 42);
    
    let result = 5i32.add_custom(&10);
    println!("Custom add: {}", result);
}


// ============================================================================
// 10. MACRO HYGIENE
// ============================================================================

/// Macro hygiene prevents name collisions
/// Macros create separate scopes for identifiers
/// Variables from macro expansion don't clash with surrounding code

macro_rules! using_temp {
    ($e:expr) => {
        {
            let temp = $e; // This 'temp' won't collide with outer scope
            temp * 2
        }
    };
}

fn demo_hygiene() {
    let temp = 5;
    let result = using_temp!(10); // Macro's 'temp' doesn't affect outer 'temp'
    println!("temp: {}, result: {}", temp, result);
}


// ============================================================================
// 11. DEBUGGING MACROS
// ============================================================================

/// Tips for debugging macros:
/// 1. Use cargo expand to see macro expansions
/// 2. Use trace_macros!(true) for debugging (nightly only)
/// 3. Use log_syntax! to print during compilation (nightly only)
/// 4. Add println! inside macros during development

// Example: Debug-friendly macro
macro_rules! debug_calc {
    ($e:expr) => {
        {
            let result = $e;
            println!("Expression: {}", stringify!($e));
            println!("Result: {}", result);
            result
        }
    };
}


// ============================================================================
// 12. PRACTICAL MACRO EXAMPLES
// ============================================================================

/// Example 1: Lazy static initialization pattern
macro_rules! lazy_static_pattern {
    ($name:ident: $type:ty = $init:expr) => {
        static $name: std::sync::OnceLock<$type> = std::sync::OnceLock::new();
        
        impl $name {
            fn get() -> &'static $type {
                $name.get_or_init(|| $init)
            }
        }
    };
}

/// Example 2: Enum with string conversion
macro_rules! string_enum {
    (
        $vis:vis enum $name:ident {
            $( $variant:ident ),* $(,)?
        }
    ) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        $vis enum $name {
            $( $variant, )*
        }
        
        impl $name {
            pub fn as_str(&self) -> &'static str {
                match self {
                    $( Self::$variant => stringify!($variant), )*
                }
            }
            
            pub fn from_str(s: &str) -> Option<Self> {
                match s {
                    $( stringify!($variant) => Some(Self::$variant), )*
                    _ => None,
                }
            }
        }
        
        impl std::fmt::Display for $name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "{}", self.as_str())
            }
        }
    };
}

string_enum! {
    pub enum Status {
        Active,
        Inactive,
        Pending,
    }
}

fn demo_string_enum() {
    let status = Status::Active;
    println!("Status: {}", status);
    println!("As string: {}", status.as_str());
    
    let parsed = Status::from_str("Pending");
    println!("Parsed: {:?}", parsed);
}


// ============================================================================
// 13. PROCEDURAL MACRO IMPLEMENTATION EXAMPLE
// ============================================================================

/// This is what a procedural macro crate structure looks like:
/// 
/// Cargo.toml:
/// ```toml
/// [lib]
/// proc-macro = true
/// 
/// [dependencies]
/// syn = "2.0"
/// quote = "1.0"
/// proc-macro2 = "1.0"
/// ```
///
/// lib.rs:
/// ```rust
/// use proc_macro::TokenStream;
/// use quote::quote;
/// use syn::{parse_macro_input, DeriveInput};
/// 
/// #[proc_macro_derive(Builder)]
/// pub fn derive_builder(input: TokenStream) -> TokenStream {
///     let input = parse_macro_input!(input as DeriveInput);
///     let name = &input.ident;
///     let builder_name = format!("{}Builder", name);
///     let builder_ident = syn::Ident::new(&builder_name, name.span());
///     
///     let expanded = quote! {
///         impl #name {
///             pub fn builder() -> #builder_ident {
///                 #builder_ident::default()
///             }
///         }
///     };
///     
///     TokenStream::from(expanded)
/// }
/// ```


// ============================================================================
// 14. MACRO BEST PRACTICES
// ============================================================================

/// BEST PRACTICES:
/// 
/// 1. PREFER FUNCTIONS WHEN POSSIBLE
///    - Macros are harder to debug and understand
///    - Use macros only when you need compile-time code generation
/// 
/// 2. DOCUMENT YOUR MACROS
///    - Show example usage
///    - Explain what code is generated
///    - Document edge cases
/// 
/// 3. USE DESCRIPTIVE NAMES
///    - Macro names should end with ! when calling
///    - Make purpose clear from name
/// 
/// 4. KEEP MACROS SIMPLE
///    - Complex logic belongs in functions
///    - Macros should mainly generate boilerplate
/// 
/// 5. TEST YOUR MACROS
///    - Write tests for different input patterns
///    - Test edge cases and error conditions
/// 
/// 6. AVOID MACRO SOUP
///    - Don't create macros that call macros that call macros
///    - Keep expansion depth reasonable
/// 
/// 7. USE PROCEDURAL MACROS FOR COMPLEX CASES
///    - Declarative macros are limited in what they can do
///    - Procedural macros have full power of Rust
/// 
/// 8. WATCH OUT FOR HYGIENE
///    - Be careful with variable names
///    - Use gensym or unique names when needed


// ============================================================================
// 15. REAL-WORLD MACRO EXAMPLES
// ============================================================================

/// These are patterns you'll see in production Rust code:

// Pattern: Error type generation (like thiserror does)
macro_rules! define_error {
    ($name:ident { $($variant:ident($inner:ty)),* $(,)? }) => {
        #[derive(Debug)]
        pub enum $name {
            $( $variant($inner), )*
        }
        
        impl std::fmt::Display for $name {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                match self {
                    $( Self::$variant(e) => write!(f, "{}: {}", stringify!($variant), e), )*
                }
            }
        }
        
        impl std::error::Error for $name {}
        
        $(
            impl From<$inner> for $name {
                fn from(e: $inner) -> Self {
                    Self::$variant(e)
                }
            }
        )*
    };
}

define_error! {
    MyError {
        Io(std::io::Error),
        Parse(std::num::ParseIntError),
    }
}

fn demo_error_macro() -> Result<(), MyError> {
    // Auto-conversion thanks to From implementations
    let _file = std::fs::read_to_string("nonexistent.txt")?;
    Ok(())
}


// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

fn main() {
    println!("=== RUST MACROS COMPREHENSIVE GUIDE ===\n");
    
    println!("--- Basic Macros ---");
    demo_basic_macros();
    
    println!("\n--- Pattern Matching ---");
    demo_pattern_matching();
    
    println!("\n--- Repetitions ---");
    demo_repetitions();
    
    println!("\n--- Derives ---");
    demo_derives();
    
    println!("\n--- Common Patterns ---");
    demo_common_patterns();
    
    println!("\n--- Hygiene ---");
    demo_hygiene();
    
    println!("\n--- String Enum ---");
    demo_string_enum();
    
    println!("\n--- Error Macro ---");
    if let Err(e) = demo_error_macro() {
        println!("Error (expected): {}", e);
    }
    
    println!("\n=== Complete ===");
}


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/// WHEN TO USE MACROS:
/// ✓ Reducing boilerplate code
/// ✓ Creating domain-specific languages (DSLs)
/// ✓ Compile-time code generation
/// ✓ Implementing traits for many types
/// ✓ Creating type-safe APIs
/// 
/// WHEN NOT TO USE MACROS:
/// ✗ When a function would work
/// ✗ For complex business logic
/// ✗ When clarity suffers
/// 
/// MACRO TYPES COMPARISON:
/// 
/// Declarative Macros (macro_rules!):
/// - Simple pattern matching
/// - Limited to syntax transformations
/// - Easier to write for simple cases
/// - Examples: vec!, println!, assert!
/// 
/// Procedural Macros:
/// - Full Rust power for code generation
/// - Can parse and analyze input thoroughly
/// - More complex to implement
/// - Examples: #[derive(Serialize)], #[tokio::main]
/// 
/// Function-like Procedural Macros:
/// - Look like declarative but with proc-macro power
/// - Good for DSLs
/// - Examples: html!, sql!
