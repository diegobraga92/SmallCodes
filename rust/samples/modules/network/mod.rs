// Declares child modules, could also be called network.rs
// Declare the client submodule (looks for client.rs in same directory)
pub mod client;

// Also declare a server module defined inline
pub mod server {
    // Public struct
    pub struct Server {
        address: String,  // Private field
        pub port: u16,    // Public field
    }
    
    impl Server {
        // Public constructor
        pub fn new(address: &str, port: u16) -> Self {
            Server {
                address: address.to_string(),
                port,
            }
        }
        
        // Public method
        pub fn start(&self) {
            println!("Server starting on {}:{}", self.address, self.port);
        }
        
        // Private method
        fn validate_address(&self) -> bool {
            !self.address.is_empty()
        }
    }
    
    // Public enum
    pub enum Protocol {
        Http,
        Https,
        WebSocket,
    }
}

// Re-export client's Client type for easier access
pub use client::Client;

// Public function in network module
pub fn connect(endpoint: &str) -> Result<(), String> {
    if endpoint.is_empty() {
        Err("Empty endpoint".to_string())
    } else {
        Ok(())
    }
}

// Private module only visible within network
mod internal {
    pub(super) fn log_connection() {  // Visible to parent (network)
        println!("Connection logged");
    }
}

// Use the internal module
pub fn connect_and_log(endpoint: &str) -> Result<(), String> {
    let result = connect(endpoint);
    super::internal::log_connection();  // Call internal function
    result
}