/*
Mini LRU Cache (Real Version)
--------------------------------------------------------
Capacity-bound LRU:

- get
- put
- Evict least recently used

Senior signal:
- HashMap + VecDeque or LinkedHashMap pattern
- Complexity discussion
- API design
*/

use linked_hash_map::LinkedHashMap;
use std::hash::Hash;

struct LruCache<K, V> {
    capacity: usize,
    map: LinkedHashMap<K, V>,
}

impl<K: Eq + Hash, V> LruCache<K, V> {
    fn new(capacity: usize) -> Self {
        Self {
            capacity,
            map: LinkedHashMap::new(),
        }
    }

    fn get(&mut self, key: &K) -> Option<&V> {
        self.map.get_refresh(key).map(|v| &*v)
    }

    fn put(&mut self, key: K, value: V) {
        if self.map.contains_key(&key) {
            self.map.insert(key, value);
            return;
        }

        if self.map.len() == self.capacity {
            self.map.pop_front(); // evict LRU
        }

        self.map.insert(key, value);
    }
}

fn main() {
    println!("Test 1: Basic put/get");
    let mut cache = LruCache::new(2);

    cache.put(1, "A");
    cache.put(2, "B");

    assert_eq!(cache.get(&1), Some(&"A"));
    assert_eq!(cache.get(&2), Some(&"B"));
    println!("✔ Passed");

    println!("Test 2: Eviction order");
    let mut cache = LruCache::new(2);

    cache.put(1, "A");
    cache.put(2, "B");
    cache.put(3, "C"); // evicts 1

    assert_eq!(cache.get(&1), None);
    assert_eq!(cache.get(&2), Some(&"B"));
    assert_eq!(cache.get(&3), Some(&"C"));
    println!("✔ Passed");

    println!("Test 3: Access refreshes recency");
    let mut cache = LruCache::new(2);

    cache.put(1, "A");
    cache.put(2, "B");
    cache.get(&1); // 1 becomes MRU
    cache.put(3, "C"); // should evict 2

    assert_eq!(cache.get(&2), None);
    assert_eq!(cache.get(&1), Some(&"A"));
    assert_eq!(cache.get(&3), Some(&"C"));
    println!("✔ Passed");

    println!("Test 4: Updating existing key");
    let mut cache = LruCache::new(2);

    cache.put(1, "A");
    cache.put(1, "Updated");

    assert_eq!(cache.get(&1), Some(&"Updated"));
    println!("✔ Passed");

    println!("Test 5: Capacity = 1");
    let mut cache = LruCache::new(1);

    cache.put(1, "A");
    cache.put(2, "B"); // evicts 1

    assert_eq!(cache.get(&1), None);
    assert_eq!(cache.get(&2), Some(&"B"));
    println!("✔ Passed");

    println!("Test 6: Update refreshes recency");
    let mut cache = LruCache::new(2);

    cache.put(1, "A");
    cache.put(2, "B");
    cache.put(1, "Updated"); // should move 1 to MRU
    cache.put(3, "C"); // should evict 2

    assert_eq!(cache.get(&2), None);
    assert_eq!(cache.get(&1), Some(&"Updated"));
    assert_eq!(cache.get(&3), Some(&"C"));
    println!("✔ Passed");

    println!("All tests passed 🚀");
}
