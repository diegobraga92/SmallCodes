/*
Thread-Safe Counter Service
--------------------------------------------------------
Implement a counter shared across threads:

pub struct Counter { ... }

impl Counter {
    pub fn inc(&self)
    pub fn get(&self) -> usize
}

Spawn 10 threads incrementing it.

Senior signal:
- Arc
- Mutex vs AtomicUsize tradeoffs
- Contention discussion
*/
use std::sync::{
    atomic::{AtomicUsize, Ordering},
    Arc,
};
use std::thread;

pub struct Counter {
    count: AtomicUsize,
}

impl Counter {
    pub fn new() -> Self {
        Self {
            count: AtomicUsize::new(0),
        }
    }

    pub fn inc(&self) {
        self.count.fetch_add(1, Ordering::Relaxed);
    }

    pub fn get(&self) -> usize {
        self.count.load(Ordering::Relaxed)
    }
}

fn main() {
    let arc = Arc::new(Counter::new());

    let mut handles = vec![];

    for _ in 0..10 {
        let c = Arc::clone(&arc);
        let t = thread::spawn(move || {
            for _ in 0..1000 {
                c.inc()
            }
        });
        handles.push(t);
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("Final count: {}", arc.get());
}
