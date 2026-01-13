//! Rust Review File – Concurrency, Ownership, Async, and Core Concepts
//! Run with:
//!   cargo new rust_review && replace src/main.rs with this file
//!   cargo add tokio
//!   cargo run

use std::{
    borrow::Cow,
    error::Error,
    fmt::{self, Display},
    rc::Rc,
    sync::{
        atomic::{AtomicUsize, Ordering},
        mpsc,
        Arc, Mutex, RwLock,
    },
    thread,
    time::Duration,
};

use tokio::{sync::mpsc as async_mpsc, task};

// ============================================================
// 0a - Send / Sync
// ============================================================
//
// Send: a type can be moved to another thread
// Sync: a type can be shared between threads safely (&T is Send)
//
// Rule of thumb:
// - Arc<T> is Send + Sync if T is Send + Sync
// - Rc<T> is NOT Send / Sync
//

fn send_sync_example() {
    let value = Arc::new(10);

    let v2 = Arc::clone(&value);
    let handle = thread::spawn(move || {
        println!("Send example value = {}", v2);
    });

    handle.join().unwrap();
}

// ============================================================
// 0b - Arc, Mutex, RwLock, Atomic
// ============================================================

// Arc: Atomic Reference Counting for thread-safe shared ownership
// RwLock: Multiple readers OR single writer
// Atomic types provide lock-free thread-safe operations

fn shared_state_example() {
    let counter = Arc::new(Mutex::new(0));
    let atomic_counter = Arc::new(AtomicUsize::new(0));
    let rwlock = Arc::new(RwLock::new(100));

    let mut handles = vec![];

    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        let atomic = Arc::clone(&atomic_counter);
        let rw = Arc::clone(&rwlock);

        handles.push(thread::spawn(move || {
            *counter.lock().unwrap() += 1;
            atomic.fetch_add(1, Ordering::Relaxed);

            let read = *rw.read().unwrap();
            println!("RwLock read: {}", read);

            *rw.write().unwrap() += 1;
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!(
        "Mutex = {}, Atomic = {}, RwLock = {}",
        *counter.lock().unwrap(),
        atomic_counter.load(Ordering::Relaxed),
        *rwlock.read().unwrap()
    );
}

// ============================================================
// 0c - Box, Rc, Cow
// ============================================================

fn ownership_types() {
    // Box: heap allocation, single owner
    let boxed = Box::new(5);
    println!("Box = {}", boxed);

    // Rc: reference counting (single-thread only)
    let rc1 = Rc::new(String::from("shared"));
    let rc2 = Rc::clone(&rc1);
    println!("Rc count = {}", Rc::strong_count(&rc1));
    drop(rc2);

    // Cow: clone-on-write
    fn uppercase(input: Cow<str>) -> Cow<str> {
        if input.chars().all(|c| c.is_uppercase()) {
            input
        } else {
            Cow::Owned(input.to_uppercase())
        }
    }

    let borrowed = Cow::Borrowed("hello");
    let owned = uppercase(borrowed);
    println!("Cow result = {}", owned);
}


// ============================================================
// 0d - Traits, Generics
// ============================================================

trait Processor<T> {
    fn process(&self, value: T) -> T;
}

struct Doubler;

impl Processor<i32> for Doubler {
    fn process(&self, value: i32) -> i32 {
        value * 2
    }
}

fn generic_fn<T, P>(value: T, processor: P) -> T
where
    P: Processor<T>,
{
    processor.process(value)
}

// ============================================================
// 0e - Error Handling
// ============================================================

#[derive(Debug)]
struct MyError;

impl Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "custom error")
    }
}

impl Error for MyError {}

fn might_fail(ok: bool) -> Result<i32, MyError> {
    if ok {
        Ok(42)
    } else {
        Err(MyError)
    }
}

// ============================================================
// 0f - Async / Await, Future
// ============================================================
//
// async fn returns a Future
// Futures are lazy – they do nothing until awaited
//

async fn async_work(id: u32) -> u32 {
    tokio::time::sleep(Duration::from_millis(100)).await;
    id * 2
}

// ============================================================
// 0g - Tokio
// ============================================================
//
// Tokio provides:
// - async runtime
// - task scheduler
// - async IO, timers, channels
//

async fn tokio_tasks() {
    let t1 = task::spawn(async_work(1));
    let t2 = task::spawn(async_work(2));

    let (r1, r2) = tokio::join!(t1, t2);
    println!("Tokio results: {}, {}", r1.unwrap(), r2.unwrap());
}

// ============================================================
// 0h - Threads vs Async
// ============================================================
//
// Threads:
// - OS-level
// - expensive context switch
// - good for CPU-bound work
//
// Async:
// - cooperative scheduling
// - great for IO-bound work
// - fewer OS threads
//

fn thread_example() {
    let handle = thread::spawn(|| {
        thread::sleep(Duration::from_millis(50));
        println!("Thread finished");
    });

    handle.join().unwrap();
}

// ============================================================
// 0i - Channels
// ============================================================

fn sync_channel_example() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        tx.send("hello from thread").unwrap();
    });

    println!("Received: {}", rx.recv().unwrap());
}

async fn async_channel_example() {
    let (tx, mut rx) = async_mpsc::channel(8);

    tokio::spawn(async move {
        tx.send("hello async").await.unwrap();
    });

    if let Some(msg) = rx.recv().await {
        println!("Async received: {}", msg);
    }
}


// ============================================================
// Main
// ============================================================

#[tokio::main]
async fn main() {
    println!("--- Send / Sync ---");
    send_sync_example();

    println!("\n--- Arc / Mutex / RwLock / Atomic ---");
    shared_state_example();

    println!("\n--- Box / Rc / Cow ---");
    ownership_types();

    println!("\n--- Traits / Generics ---");
    let result = generic_fn(10, Doubler);
    println!("Generic result = {}", result);

    println!("\n--- Error Handling ---");
    match might_fail(true) {
        Ok(v) => println!("Success: {}", v),
        Err(e) => println!("Error: {}", e),
    }

    println!("\n--- Threads ---");
    thread_example();

    println!("\n--- Tokio Async ---");
    tokio_tasks().await;

    println!("\n--- Channels ---");
    sync_channel_example();
    async_channel_example().await;
}