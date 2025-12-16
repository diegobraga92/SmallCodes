// Root module
// Declare the utils module (looks for utils.rs or utils/mod.rs)
pub mod utils;

// Declare the network module (looks for network/mod.rs)
pub mod network;

// Re-export commonly used items to simplify public API
pub use network::Client;
pub use utils::format_data;

/// A public struct that's part of our library's main API
pub struct Library {
    name: String,
    version: String,
}

impl Library {
    /// Public constructor
    pub fn new(name: &str) -> Self {
        Library {
            name: name.to_string(),
            version: String::from("1.0.0"),
        }
    }
    
    /// Public method
    pub fn info(&self) -> String {
        format!("{} v{}", self.name, self.version)
    }
}

// Private module only visible within this file
mod internal {
    pub(crate) fn internal_helper() -> i32 {
        42
    }
}

// Public function that uses internal module
pub fn get_answer() -> i32 {
    internal::internal_helper()
}