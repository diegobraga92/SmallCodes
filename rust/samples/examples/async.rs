//// Async Rust is cooperative concurrency, not parallelism. All about IO
/// Rust async is built on state machines + polling, not green threads.
// Synchronous (blocking) code
fn synchronous_download() -> Result<String, Error> {
    let response = reqwest::blocking::get("https://api.example.com/data")?;
    response.text()
}

// Asynchronous (non-blocking) code
async fn async_download() -> Result<String, Error> {
    let response = reqwest::get("https://api.example.com/data").await?;
    response.text().await
}

/// async fn returns a Future<Output = Result<String, Error>>, not the actual result. The .await is where the magic happens.


/// Futures & The Future Trait
pub trait Future {
    type Output;
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}

// In practice
use std::{future::Future, pin::Pin, task::{Context, Poll}};

struct Delay {
    duration: std::time::Duration,
    elapsed: bool,
}

impl Future for Delay {
    type Output = ();
    
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.elapsed {
            Poll::Ready(())
        } else {
            // Schedule wakeup (simplified)
            let waker = cx.waker().clone();
            let duration = self.duration;
            
            std::thread::spawn(move || {
                std::thread::sleep(duration);
                waker.wake(); // Signals executor to poll again
            });
            
            self.elapsed = true;
            Poll::Pending
        }
    }
}


//// Rust doesn't include a builtin async runtime, that's why Tokio is used:
/// Tokio provide I/O reactors, Task Scheduler and Thread Pool
use tokio::{task, time::{sleep, Duration}};

#[tokio::main]
async fn main() {
    // Spawn concurrent tasks
    let task1 = task::spawn(async {
        sleep(Duration::from_secs(1)).await; // Await is a Yield Point. Can suspend and resume on another Thread
        println!("Task 1 completed");
    });
    
    let task2 = task::spawn(async {
        sleep(Duration::from_secs(2)).await;
        println!("Task 2 completed");
    });
    
    // Join handles to wait for completion
    let _ = tokio::join!(task1, task2);
    
    // Select for the first completed
    tokio::select! {
        _ = sleep(Duration::from_secs(1)) => {
            println!("1 second passed first");
        }
        _ = sleep(Duration::from_secs(2)) => {
            println!("2 seconds passed first");
        }
    }
}

/// There is also async-std:
use async_std::{task, prelude::*};

#[async_std::main]
async fn main() {
    let mut handles = vec![];
    
    for i in 0..10 {
        handles.push(task::spawn(async move {
            task::sleep(std::time::Duration::from_millis(i * 100)).await;
            println!("Task {} completed", i);
        }));
    }
    
    for handle in handles {
        handle.await;
    }
}


//// Concurrency Patterns and Sync
/// Channels
use tokio::sync::{mpsc, oneshot};
use std::time::Duration;

#[tokio::main]
async fn main() {
    // Multi-producer, single-consumer channel
    let (tx, mut rx) = mpsc::channel::<String>(32);
    
    // Spawn multiple producers
    for i in 0..3 {
        let tx_clone = tx.clone();
        tokio::spawn(async move {
            for j in 0..5 {
                tx_clone.send(format!("Message {} from producer {}", j, i)).await.unwrap();
                tokio::time::sleep(Duration::from_millis(100)).await;
            }
        });
    }
    
    // Drop the original sender so the channel closes
    drop(tx);
    
    // Consumer
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
    
    // One-shot channel for request-response pattern
    let (resp_tx, resp_rx) = oneshot::channel();
    
    tokio::spawn(async move {
        // Do some work
        tokio::time::sleep(Duration::from_millis(500)).await;
        resp_tx.send("Response!").unwrap();
    });
    
    let response = resp_rx.await.unwrap();
    println!("Got response: {}", response);
}

/// Shared State with Async Mutexes
use tokio::sync::{Mutex, RwLock};
use std::sync::Arc;

#[tokio::main]
async fn main() {
    // Shared counter with Mutex
    let counter = Arc::new(Mutex::new(0));
    
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(tokio::spawn(async move {
            let mut num = counter.lock().await;
            *num += 1;
        }));
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
    
    println!("Result: {}", *counter.lock().await);
    
    // Read-Write Lock for read-heavy workloads
    let cache = Arc::new(RwLock::new(std::collections::HashMap::new()));
    
    // Multiple concurrent readers
    let cache_clone = Arc::clone(&cache);
    let readers: Vec<_> = (0..5).map(|i| {
        let cache = Arc::clone(&cache_clone);
        tokio::spawn(async move {
            let cache = cache.read().await;
            println!("Reader {} sees {:?}", i, cache.keys());
        })
    }).collect();
    
    // Single writer
    let writer = tokio::spawn(async move {
        let mut cache = cache.write().await;
        cache.insert("key", "value");
    });
    
    for reader in readers {
        reader.await.unwrap();
    }
    writer.await.unwrap();
}