// Child module
// This is a submodule of network

// Public struct
pub struct Client {
    id: u64,            // Private field
    pub name: String,   // Public field
    timeout: u32,       // Private field
}

impl Client {
    // Associated function (constructor)
    pub fn new(name: &str) -> Self {
        Client {
            id: rand::random(),  // Would need rand crate for this to work
            name: name.to_string(),
            timeout: 30,
        }
    }
    
    // Method with &self
    pub fn send(&self, message: &str) -> Result<(), String> {
        if message.len() > 1000 {
            Err("Message too long".to_string())
        } else {
            println!("Client {} sending: {}", self.name, message);
            Ok(())
        }
    }
    
    // Method with &mut self
    pub fn set_timeout(&mut self, timeout: u32) {
        self.timeout = timeout;
    }
    
    // Method that consumes self
    pub fn into_parts(self) -> (u64, String) {
        (self.id, self.name)
    }
    
    // Private method
    fn validate_message(&self, message: &str) -> bool {
        !message.is_empty() && message.len() <= self.timeout as usize
    }
}

// Public enum
pub enum ClientError {
    Timeout,
    ConnectionFailed,
    InvalidData,
}

// Implement a trait for Client
impl std::fmt::Display for Client {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "Client {} (ID: {})", self.name, self.id)
    }
}