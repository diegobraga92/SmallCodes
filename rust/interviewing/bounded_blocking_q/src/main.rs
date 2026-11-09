use std::collections::VecDeque;
use std::sync::{Condvar, Mutex};

#[derive(Debug, PartialEq, Eq)]
pub enum PushError<T> {
    Closed(T), // hand the item back — never lose data
}

#[derive(Debug, PartialEq, Eq)]
pub enum PopError {
    Closed,
}

pub struct BoundedQueue<T> {
    // One lock over all mutable state: items, capacity, closed.
    inner: Mutex<Inner<T>>,
    // Two condvars so producers and consumers don't steal each other's wakeups.
    not_empty: Condvar, // consumers wait here
    not_full: Condvar,  // producers wait here
}

struct Inner<T> {
    items: VecDeque<T>,
    capacity: usize,
    closed: bool,
}

impl<T> BoundedQueue<T> {
    pub fn new(capacity: usize) -> Self {
        // capacity == 0 would deadlock the first push forever — caller bug.
        assert!(capacity > 0);
        Self {
            inner: Mutex::new(Inner {
                items: VecDeque::with_capacity(capacity),
                capacity,
                closed: false,
            }),
            not_empty: Condvar::new(),
            not_full: Condvar::new(),
        }
    }

    pub fn push(&self, item: T) -> Result<(), PushError<T>> {
        // Recover from poisoning rather than cascade panics — our data is
        // still structurally valid (just a deque + two fields).
        let mut g = self.inner.lock().unwrap_or_else(|e| e.into_inner());

        // `loop`, not `if`: condvar wakes are spurious and another thread
        // may have grabbed the slot between our wakeup and re-locking.
        loop {
            if g.closed {
                return Err(PushError::Closed(item));
            }
            if g.items.len() < g.capacity {
                break;
            }
            // `wait` releases the lock and re-acquires before returning,
            // so consumers can make progress while we're parked.
            g = self.not_full.wait(g).unwrap_or_else(|e| e.into_inner());
        }

        g.items.push_back(item);
        self.not_empty.notify_one(); // exactly one item added → wake one
        Ok(())
    }

    pub fn pop(&self) -> Result<T, PopError> {
        let mut g = self.inner.lock().unwrap_or_else(|e| e.into_inner());

        loop {
            // Check items FIRST: after close(), the queue still drains
            // whatever was already in flight (graceful shutdown).
            if let Some(item) = g.items.pop_front() {
                self.not_full.notify_one(); // exactly one slot freed
                return Ok(item);
            }
            if g.closed {
                return Err(PopError::Closed);
            }
            g = self.not_empty.wait(g).unwrap_or_else(|e| e.into_inner());
        }
    }

    pub fn close(&self) {
        let mut g = self.inner.lock().unwrap_or_else(|e| e.into_inner());
        g.closed = true;
        drop(g); // release lock before notifying — avoids immediate re-block

        // `notify_all` on both sides: we don't know how many waiters exist,
        // and every one of them needs to see `closed = true` and bail.
        // Safe to drop the lock first because `closed` is sticky — a wakeup
        // can't be "lost" in the gap.
        self.not_empty.notify_all();
        self.not_full.notify_all();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::thread;
    use std::time::Duration;

    #[test]
    fn close_wakes_blocked_consumer() {
        let q = Arc::new(BoundedQueue::new(1));
        let q2 = Arc::clone(&q);
        let c = thread::spawn(move || q2.pop());
        thread::sleep(Duration::from_millis(50)); // let it park
        q.close();
        assert_eq!(c.join().unwrap(), Err(PopError::Closed));
    }

    #[test]
    fn close_wakes_blocked_producer_and_returns_item() {
        let q = Arc::new(BoundedQueue::new(1));
        q.push(1).unwrap(); // fill it so next push blocks
        let q2 = Arc::clone(&q);
        let p = thread::spawn(move || q2.push(2));
        thread::sleep(Duration::from_millis(50));
        q.close();
        assert_eq!(p.join().unwrap(), Err(PushError::Closed(2))); // item back
    }

    #[test]
    fn drains_before_reporting_closed() {
        let q = BoundedQueue::new(4);
        q.push(1).unwrap();
        q.push(2).unwrap();
        q.close();
        assert_eq!(q.pop(), Ok(1)); // still drains
        assert_eq!(q.pop(), Ok(2));
        assert_eq!(q.pop(), Err(PopError::Closed));
    }
}

// ============================================================================
// DEMO  (run with `cargo run`)
// ============================================================================

fn main() {
    demo_fifo();
    demo_backpressure();
    demo_close_wakes_blocked_consumer();
}

fn demo_fifo() {
    println!("--- demo 1: FIFO order ---");
    let q = BoundedQueue::new(4);
    for i in 1..=3 {
        q.push(i).unwrap();
    }
    for _ in 0..3 {
        println!("  popped {}", q.pop().unwrap());
    }
}

fn demo_backpressure() {
    println!("\n--- demo 2: backpressure blocks producer ---");
    let q = Arc::new(BoundedQueue::new(1));
    let q2 = Arc::clone(&q);

    let producer = thread::spawn(move || {
        println!("  producer: pushing 1");
        q2.push(1).unwrap();
        println!("  producer: pushing 2 (should block until main pops)");
        q2.push(2).unwrap();
        println!("  producer: done");
    });

    thread::sleep(Duration::from_millis(200));
    println!("  main: popping 1 to make room");
    assert_eq!(q.pop().unwrap(), 1);

    producer.join().unwrap();
    assert_eq!(q.pop().unwrap(), 2);
}

fn demo_close_wakes_blocked_consumer() {
    println!("\n--- demo 3: close wakes blocked consumer ---");
    let q = Arc::new(BoundedQueue::new(1));
    let q2 = Arc::clone(&q);

    let consumer = thread::spawn(move || {
        println!("  consumer: waiting on pop");
        let r = q2.pop();
        println!("  consumer: woke up with {:?}", r);
        r
    });

    thread::sleep(Duration::from_millis(200));
    println!("  main: closing queue");
    q.close();

    assert_eq!(consumer.join().unwrap(), Err(PopError::Closed));
}