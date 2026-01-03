//// Function Signatures, define interface without implementation
// Basic signature
fn function_name(param1: Type1, param2: Type2) -> ReturnType;

// Examples
fn add(x: i32, y: i32) -> i32;
fn process_data(data: &str) -> Result<String, Error>;
fn max<T: Ord>(a: T, b: T) -> T;  // Generic function



//// Impl blocks, attach functionality to types (struct, enum, trait)
struct Rectangle {
    width: u32,
    height: u32,
}

// impl block for Rectangle
impl Rectangle {
    // Method - takes &self, &mut self, or self
    fn area(&self) -> u32 {
        self.width * self.height
    }
    
    // Associated function (no self parameter)
    fn square(size: u32) -> Self {
        Rectangle {
            width: size,
            height: size,
        }
    }
}

// Multiple implementations are allowed
impl Counter {
    fn new() -> Self {
        Self { value: 0 }
    }
}

impl Counter {
    fn reset(&mut self) {
        self.value = 0;
    }
}

// Trait implementation
impl Iterator for Counter {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        self.value += 1;
        Some(self.value)
    }
}
// Can also be Generic: impl<T> Type<T> { ... }



//// Associated Functions and Methods, associated do not have self, while methods need self
impl Circle {
    // Associated function
    fn new(radius: f64) -> Self {
        Circle { radius }
    }
    
    // Method
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius.powi(2)
    }
}

// Usage
let circle = Circle::new(5.0);  // Associated function
let area = circle.area();       // Method
// Associated are usually used for Constructors and Utility, while methods operate the instance



//// Visibility Rules, privacy is module-based, not type-based
// Everything is private unless marked with pub. Children modules can see private items in parent modules
struct Secret {
    value: i32, // private
}

pub struct Config {
    pub port: u16,
}
// Making a struct pub does NOT make its fields public

mod outer {
    pub mod inner {
        pub(in crate::outer) fn semi_private() {}  // Visible only in outer
        pub(super) fn parent_visible() {}          // Visible to parent
        pub(crate) fn crate_visible() {}           // Visible in entire crate
        // pub(self) is the same as no modifier (private)
        
        pub struct PublicStruct {
            pub field: i32,     // Public field
            private_field: i32, // Private field
        }
        
        impl PublicStruct {
            pub fn new() -> Self { /* ... */ }
        }
    }
    
    // Can access inner::semi_private() here
}
// Cannot access outer::inner::semi_private() here

// Re-exporting, enforce encapsulation while providing APIs
// src/lib.rs
mod internal {
    pub mod utils {
        pub fn helper() {}
    }
}

// Re-export to simplify public API
pub use internal::utils::helper;

// Now users can call: crate::helper()
// Instead of: crate::internal::utils::helper()