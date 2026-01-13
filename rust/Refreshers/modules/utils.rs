// This file is automatically a module named `utils`

// Public function accessible from parent module
pub fn format_data(data: &str) -> String {
    let processed = private_helper(data);
    format!("Formatted: {}", processed)
}

// Public struct with both public and private fields
pub struct Parser {
    pub delimiter: char,      // Public field
    strict_mode: bool,        // Private field
}

impl Parser {
    // Public constructor
    pub fn new(delimiter: char) -> Self {
        Parser {
            delimiter,
            strict_mode: true,
        }
    }
    
    // Public method
    pub fn parse(&self, input: &str) -> Vec<String> {
        input.split(self.delimiter)
            .map(|s| s.trim().to_string())
            .collect()
    }
    
    // Private method (only visible within this module)
    fn validate(&self) -> bool {
        self.strict_mode
    }
}

// Private function (only visible within this module)
fn private_helper(data: &str) -> String {
    data.to_uppercase()
}

// Nested module within utils
pub mod math {
    // This function is public within `utils::math`
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }
    
    // This is private to `utils::math`
    fn subtract(a: i32, b: i32) -> i32 {
        a - b
    }
    
    // Re-export from parent module's scope
    pub use super::format_data;
}