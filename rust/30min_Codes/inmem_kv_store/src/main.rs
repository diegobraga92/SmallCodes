/*
In-Memory Key-Value Store
--------------------------------------------------------
Implement:

pub struct KvStore { ... }

impl KvStore {
    pub fn new() -> Self
    pub fn set(&mut self, key: String, value: String)
    pub fn get(&self, key: &str) -> Option<&String>
    pub fn delete(&mut self, key: &str) -> bool
}

Senior signal:
- API clarity
- Borrowing decisions
- &str vs String ergonomics
- Testability

Extension: Add TTL support.
*/

use std::collections::HashMap;
use std::time::{Duration, Instant};

struct Entry {
    value: String,
    expires_at: Option<Instant>,
}

pub struct KvStore {
    map: HashMap<String, Entry>,
}

impl KvStore {
    pub fn new() -> Self {
        Self {
            map: HashMap::new(),
        }
    }

    pub fn set(&mut self, key: String, value: String) {
        self.set_with_ttl(key, value, None);
    }

    pub fn set_with_ttl(&mut self, key: String, value: String, ttl: Option<Duration>) {
        let expires_at = ttl.map(|d| Instant::now() + d);

        let entry = Entry { value, expires_at };

        self.map.insert(key, entry);
    }

    pub fn get(&mut self, key: &str) -> Option<&String> {
        self.cleanup_if_expired(key);
        self.map.get(key).map(|entry| &entry.value)
    }

    pub fn delete(&mut self, key: &str) -> bool {
        self.cleanup_if_expired(key);
        self.map.remove(key).is_some()
    }

    fn cleanup_if_expired(&mut self, key: &str) {
        if let Some(entry) = self.map.get(key) {
            if let Some(expiry) = entry.expires_at {
                if Instant::now() >= expiry {
                    self.map.remove(key);
                }
            }
        }
    }
}

use std::thread::sleep;

fn main() {
    println!("Running KvStore tests...");

    // ==========================
    // Basic set/get test
    // ==========================
    let mut store = KvStore::new();
    store.set("name".to_string(), "Diego".to_string());

    assert_eq!(store.get("name"), Some(&"Diego".to_string()));
    println!("✔ Basic set/get passed");

    // ==========================
    // Delete test
    // ==========================
    assert!(store.delete("name"));
    assert!(store.get("name").is_none());
    println!("✔ Delete passed");

    // ==========================
    // Overwrite test
    // ==========================
    store.set("key".to_string(), "v1".to_string());
    store.set("key".to_string(), "v2".to_string());

    assert_eq!(store.get("key"), Some(&"v2".to_string()));
    println!("✔ Overwrite passed");

    // ==========================
    // TTL expiration test
    // ==========================
    store.set_with_ttl(
        "temp".to_string(),
        "123".to_string(),
        Some(Duration::from_millis(100)),
    );

    assert!(store.get("temp").is_some());

    sleep(Duration::from_millis(150));

    assert!(store.get("temp").is_none());
    println!("✔ TTL expiration passed");

    // ==========================
    // Non-expiring value test
    // ==========================
    store.set("persistent".to_string(), "alive".to_string());
    sleep(Duration::from_millis(150));

    assert_eq!(store.get("persistent"), Some(&"alive".to_string()));
    println!("✔ Non-expiring key passed");

    println!("All tests passed successfully!");
}
