//// Threads, use OS threads 1:1, scheduled preemptively, cheap to create but not free
use std::thread;
use std::time::Duration;

// Basic thread spawning
let handle = thread::spawn(|| {
    println!("Hello from a thread!");
    42 // Return value
});

// Main thread continues immediately
println!("Hello from main thread");

// Wait for thread to complete and get result
let result = handle.join().expect("Thread panicked");
println!("Thread returned: {}", result);

/// Ownership, data must be 'Send' between threads, shared data must be 'Sync', enforced by compiler
let data = vec![1, 2, 3];

// Use move keyword to transfer ownership to thread
let handle = thread::spawn(move || {
    println!("Data in thread: {:?}", data);
    // data is moved here, can't be used in main thread anymore
});

handle.join().unwrap();
// println!("{:?}", data); // Error: value moved

/// Configuration
// Builder pattern for thread configuration
let builder = thread::Builder::new()
    .name("worker-1".to_string())
    .stack_size(1024 * 1024); // 1MB stack

let handle = builder.spawn(|| {
    let name = thread::current().name().unwrap();
    println!("Running thread: {}", name);
    // Do work
}).unwrap();

handle.join().unwrap();

/// Panics and Recovery
// Threads can panic independently
let handle = thread::spawn(|| {
    panic!("Oops! Thread crashed!");
});

match handle.join() {
    Ok(_) => println!("Thread completed successfully"),
    Err(e) => {
        println!("Thread panicked: {:?}", e);
        // Can continue with other work
    }
}


/// Scope Threads
// Scoped threads can borrow from parent scope
let mut data = vec![1, 2, 3];

thread::scope(|s| {
    // Can borrow data immutably in multiple threads
    s.spawn(|| {
        println!("Thread 1: data length = {}", data.len());
    });
    
    s.spawn(|| {
        println!("Thread 2: first element = {}", data[0]);
    });
    
    // Can even borrow mutably in one thread
    s.spawn(|| {
        data.push(4);
        println!("Thread 3: added element");
    });
}); // All threads joined automatically here

println!("Final data: {:?}", data); // Can use data here

/// Thread Local Storage
use std::cell::RefCell;

// Thread-local variable
thread_local! {
    static COUNTER: RefCell<u32> = RefCell::new(0);
}

let handles: Vec<_> = (0..5).map(|i| {
    thread::spawn(move || {
        COUNTER.with(|counter| {
            let mut num = counter.borrow_mut();
            *num += i;
            println!("Thread {}: counter = {}", i, *num);
        });
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

// Each thread has its own independent counter


//// Thread Pool Pattern
use std::sync::{Arc, Mutex};
use std::collections::VecDeque;

struct ThreadPool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: std::sync::mpsc::Sender<Job>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    fn new(size: usize) -> Self {
        let (sender, receiver) = std::sync::mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));
        
        let mut workers = Vec::with_capacity(size);
        
        for id in 0..size {
            let receiver = Arc::clone(&receiver);
            let worker = thread::spawn(move || loop {
                let job = receiver.lock().unwrap().recv();
                match job {
                    Ok(job) => {
                        println!("Worker {} got a job", id);
                        job();
                    }
                    Err(_) => {
                        println!("Worker {} shutting down", id);
                        break;
                    }
                }
            });
            workers.push(worker);
        }
        
        ThreadPool { workers, sender }
    }
    
    fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        // Drop sender to signal workers to stop
        // Workers will join automatically
    }
}



//// Message Passing (std::sync::mpsc), multi-producer, single-consumer channels, thread-safe messaging, ownership is transfered
use std::sync::mpsc;
use std::thread;

// Create a channel
let (tx, rx) = mpsc::channel();

// Spawn a thread that sends a message
thread::spawn(move || {
    let val = String::from("hello");
    tx.send(val).unwrap();
    // val is moved, can't be used here anymore
});

// Receive the message in main thread
let received = rx.recv().unwrap();
println!("Got: {}", received); // "hello"


/// Multiple Messages
let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    let vals = vec![
        String::from("hi"),
        String::from("from"),
        String::from("the"),
        String::from("thread"),
    ];
    
    for val in vals {
        tx.send(val).unwrap();
        thread::sleep(Duration::from_millis(100));
    }
});

// Receive messages as they come
for received in rx {
    println!("Got: {}", received);
    if received == "thread" {
        break;
    }
}


/// Multiple Producers
let (tx, rx) = mpsc::channel();
let tx1 = tx.clone(); // Clone the transmitter

// First producer
thread::spawn(move || {
    let vals = vec![1, 2, 3];
    for val in vals {
        tx.send(val).unwrap();
    }
});

// Second producer
thread::spawn(move || {
    let vals = vec![4, 5, 6];
    for val in vals {
        tx1.send(val).unwrap();
    }
});

// Consumer receives from both producers
for received in rx {
    println!("Got: {}", received);
}


/// Synchronous Channels:
// Bounded channel with capacity
let (tx, rx) = mpsc::sync_channel(3); // Buffer size of 3

thread::spawn(move || {
    for i in 0..10 {
        println!("Sending {}", i);
        tx.send(i).unwrap(); // Will block when buffer is full
        thread::sleep(Duration::from_millis(100));
    }
});

// Consumer is slower
for received in rx {
    println!("Received {}", received);
    thread::sleep(Duration::from_millis(200));
}


/// Error Handling with try_recv:
let (tx, rx) = mpsc::channel();

// Non-blocking receive
match rx.try_recv() {
    Ok(msg) => println!("Got message: {}", msg),
    Err(mpsc::TryRecvError::Empty) => println!("No messages yet"),
    Err(mpsc::TryRecvError::Disconnected) => println!("Senders disconnected"),
}

// Send a message
tx.send("hello").unwrap();

// Now try_recv will succeed
match rx.try_recv() {
    Ok(msg) => println!("Got message: {}", msg),
    Err(_) => println!("No message"),
}


/// Channel with timeout
use std::sync::mpsc::{self, RecvTimeoutError};
use std::time::Duration;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    thread::sleep(Duration::from_secs(2));
    tx.send("delayed message").unwrap();
});

// Wait with timeout
match rx.recv_timeout(Duration::from_secs(1)) {
    Ok(msg) => println!("Got: {}", msg),
    Err(RecvTimeoutError::Timeout) => println!("Timeout!"),
    Err(RecvTimeoutError::Disconnected) => println!("Channel disconnected"),
}


//// Shared State Concurrency
/// Mutex Basics
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap()); // 10

/// RwLock
use std::sync::{Arc, RwLock};
use std::thread;

let data = Arc::new(RwLock::new(vec![1, 2, 3]));
let mut handles = vec![];

// Multiple readers
for i in 0..5 {
    let data = Arc::clone(&data);
    handles.push(thread::spawn(move || {
        let reader = data.read().unwrap();
        println!("Reader {}: {:?}", i, *reader);
    }));
}

// Single writer
let data_writer = Arc::clone(&data);
handles.push(thread::spawn(move || {
    let mut writer = data_writer.write().unwrap();
    writer.push(4);
    println!("Writer: added element");
}));

for handle in handles {
    handle.join().unwrap();
}

/// Atomic Types
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

let atomic_counter = Arc::new(AtomicUsize::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&atomic_counter);
    handles.push(thread::spawn(move || {
        // No lock needed!
        counter.fetch_add(1, Ordering::SeqCst);
    }));
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", atomic_counter.load(Ordering::SeqCst)); // 10

// Atomics Memory Ordering
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::thread;

// Relaxed: No ordering guarantees, just atomicity
let relaxed = AtomicUsize::new(0);
relaxed.store(1, Ordering::Relaxed);
let _ = relaxed.load(Ordering::Relaxed);

// Release-Acquire: Synchronization between threads
let data = Arc::new(AtomicUsize::new(0));
let ready = Arc::new(AtomicBool::new(false));

let data_clone = Arc::clone(&data);
let ready_clone = Arc::clone(&ready);

// Producer thread (uses Release)
thread::spawn(move || {
    data_clone.store(42, Ordering::Relaxed);
    ready_clone.store(true, Ordering::Release);  // Everything before this is visible
});

// Consumer thread (uses Acquire)
thread::spawn(move || {
    while !ready.load(Ordering::Acquire) {  // Wait for release
        std::thread::yield_now();
    }
    // Now we can safely read data
    println!("Data: {}", data.load(Ordering::Relaxed));
});

// SeqCst: Sequential consistency (strongest ordering)
let seq1 = AtomicUsize::new(0);
let seq2 = AtomicUsize::new(0);

seq1.store(1, Ordering::SeqCst);
let val = seq2.load(Ordering::SeqCst);  // Sees all SeqCst operations in order



/// Condition Variables, condvar, notify and receive
use std::sync::{Arc, Mutex, Condvar};

let pair = Arc::new((Mutex::new(false), Condvar::new()));
let pair2 = Arc::clone(&pair);

// Thread that sets the condition
thread::spawn(move || {
    let (lock, cvar) = &*pair2;
    let mut started = lock.lock().unwrap();
    *started = true;
    cvar.notify_one();
    println!("Thread notified main thread");
});

// Main thread waits for condition
let (lock, cvar) = &*pair;
let mut started = lock.lock().unwrap();
while !*started {
    started = cvar.wait(started).unwrap();
}
println!("Main thread woke up!");


/// Barriers
use std::sync::{Arc, Barrier};

let barrier = Arc::new(Barrier::new(3)); // 3 threads must wait
let mut handles = vec![];

for id in 0..3 {
    let barrier = Arc::clone(&barrier);
    handles.push(thread::spawn(move || {
        println!("Thread {} before barrier", id);
        barrier.wait(); // All threads wait here until 3 have arrived
        println!("Thread {} after barrier", id);
    }));
}

for handle in handles {
    handle.join().unwrap();
}


/// Once (One-Time Initialization)
use std::sync::Once;

static INIT: Once = Once::new();
static mut CONFIG: Option<String> = None;

// This will only run once, even if called from multiple threads
INIT.call_once(|| {
    unsafe {
        CONFIG = Some("configuration".to_string());
    }
});

// Now safe to access (initialization is complete)
unsafe {
    println!("Config: {:?}", CONFIG);
}


/// Lazy Initialization with OnceLock/OnceCell:
use std::sync::OnceLock;

static GLOBAL_DATA: OnceLock<Vec<u8>> = OnceLock::new();

fn get_global_data() -> &'static Vec<u8> {
    GLOBAL_DATA.get_or_init(|| {
        println!("Initializing global data");
        vec![1, 2, 3, 4, 5]
    })
}

// First call initializes
let data1 = get_global_data();
// Second call uses cached value
let data2 = get_global_data();
assert!(std::ptr::eq(data1, data2)); // Same reference


/// Deadlock Prevention Patterns
use std::sync::{Arc, Mutex};

// BAD: Potential deadlock
let lock1 = Arc::new(Mutex::new(0));
let lock2 = Arc::new(Mutex::new(0));

let lock1_clone = Arc::clone(&lock1);
let lock2_clone = Arc::clone(&lock2);

let handle1 = thread::spawn(move || {
    let _a = lock1.lock().unwrap();
    thread::sleep(Duration::from_millis(10));
    let _b = lock2.lock().unwrap(); // Might deadlock
});

let handle2 = thread::spawn(move || {
    let _b = lock2_clone.lock().unwrap();
    thread::sleep(Duration::from_millis(10));
    let _a = lock1_clone.lock().unwrap(); // Might deadlock
});

// GOOD: Lock ordering
let handle1 = thread::spawn(move || {
    let locks = if lock1.data_ptr() < lock2.data_ptr() {
        (lock1.lock().unwrap(), lock2.lock().unwrap())
    } else {
        (lock2.lock().unwrap(), lock1.lock().unwrap())
    };
    // Use locks
});

// BETTER: Use try_lock with backoff
let handle1 = thread::spawn(move || {
    let mut backoff = 1;
    loop {
        if let Ok(lock1_guard) = lock1.try_lock() {
            if let Ok(lock2_guard) = lock2.try_lock() {
                // Got both locks
                break;
            }
        }
        thread::sleep(Duration::from_millis(backoff));
        backoff = std::cmp::min(backoff * 2, 100);
    }
});

/// Summary:
/// Clear pipeline, use Channels
/// Stateful Shared config, use Arc<RwLock<t>>
/// Counters/metrics, use Atomics
/// Complex mutables, use Mutex or RwLock
/// Avoiding Contentions, use message passing



//// Data Races vs Race Conditions
/// Data Races are prevented in Rust at compile-time
// This is a data race - Rust won't compile it!
// let mut data = 0;
// thread::spawn(|| {
//     data += 1; // Error: cannot borrow `data` as mutable
// });
// println!("{}", data); // Error: cannot borrow `data` as immutable

// Rust prevents data races at compile time through:
// 1. Ownership rules
// 2. Borrow checker
// 3. Send and Sync traits

// A data race occurs when:
// 1. Two or more threads access the same memory location
// 2. At least one access is a write
// 3. The accesses are not synchronized


/// Race Condition, not prevented by Rust
use std::sync::{Arc, Mutex};

// This compiles but has a race condition
let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        // RACE CONDITION: between lock and increment
        // Another thread could modify shared state
        // in a way that violates invariants
        
        // This specific increment is safe due to Mutex,
        // but the pattern shows where race conditions can occur
        
        let mut num = counter.lock().unwrap();
        
        // Check-then-act race condition
        if *num < 5 {
            // What if another thread modified num between check and increment?
            *num += 1;
        }
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());



/// Send and Sync Traits
// Send: Types safe to transfer across thread boundaries
// If T: Send, then ownership of T can be transferred to another thread

use std::thread;

// Most types are Send by default
let x = 42;  // i32 is Send
thread::spawn(move || {
    println!("x = {}", x);  // x moved into thread
});

// Types that are NOT Send (!Send):
// - Rc<T> (non-atomic reference counting)
// - Cell<T>, RefCell<T> (interior mutability without synchronization)
// - *const T, *mut T (raw pointers)
// - Non-Send types composed together

// Example: Rc is !Send
use std::rc::Rc;

let rc = Rc::new(42);
// thread::spawn(move || { println!("{}", rc); });  // ERROR: Rc<i32> is not Send

// Making custom types Send
struct MyType {
    data: Vec<u8>,
    // Automatically Send because Vec<u8> is Send
}

// Explicit Send bound
fn spawn_thread<T: Send + 'static>(value: T) {
    thread::spawn(move || {
        drop(value);  // Consume value in new thread
    });
}

// Send is automatically derived for structs/enums where all fields are Send
#[derive(Clone)]
struct SafeStruct {
    a: i32,        // Send
    b: String,     // Send
    c: Vec<f64>,   // Send
}  // Auto-implements Send


/// Sync: Types safe to share references between threads
// If T: Sync, then &T is Send

use std::sync::{Arc, Mutex};

// Basic Sync types
let data = vec![1, 2, 3];
let ref1 = &data;
let ref2 = &data;

// Both references can be used in different threads
thread::spawn(move || println!("Thread 1: {:?}", ref1));
println!("Main thread: {:?}", ref2);

// Types that are NOT Sync (!Sync):
// - Cell<T>, RefCell<T> (runtime borrow checking not thread-safe)
// - Rc<T> (reference counting not thread-safe)

// Example: RefCell is !Sync
use std::cell::RefCell;

let cell = RefCell::new(42);
// thread::spawn(move || { println!("{}", cell.borrow()); });  // ERROR: RefCell<i32> is not Sync

// Arc + Mutex is both Send and Sync
let shared = Arc::new(Mutex::new(42));
let shared_clone = Arc::clone(&shared);

thread::spawn(move || {
    let mut guard = shared_clone.lock().unwrap();
    *guard += 1;
});

// Sync bound example
fn share_between_threads<T: Sync>(data: &T) {
    let handle1 = thread::spawn(|| {
        // Can safely read from data
    });
    let handle2 = thread::spawn(|| {
        // Can also safely read from data
    });
}