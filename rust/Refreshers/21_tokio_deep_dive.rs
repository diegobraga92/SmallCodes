//// TOKIO DEEP DIVE - ASYNC RUNTIME INTERNALS
/// Comprehensive guide to Tokio async runtime
/// Covers runtime, tasks, channels, I/O, timers, and advanced patterns

// ============================================================================
// 1. TOKIO RUNTIME BASICS
// ============================================================================

/// Tokio is an async runtime for Rust
/// Provides:
/// - Task scheduler
/// - I/O event loop
/// - Timers
/// - Synchronization primitives
/// - Async networking

/*
INSTALLATION:
cargo add tokio --features full
*/

/// CREATING A RUNTIME:
/*
use tokio::runtime::Runtime;

fn main() {
    // Create runtime manually
    let rt = Runtime::new().unwrap();
    
    rt.block_on(async {
        println!("Hello from async!");
    });
}

// Or use #[tokio::main] macro (recommended)
#[tokio::main]
async fn main() {
    println!("Hello from async!");
}

// Equivalent to:
fn main() {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async {
            println!("Hello from async!");
        })
}
*/


// ============================================================================
// 2. RUNTIME CONFIGURATION
// ============================================================================

/*
use tokio::runtime::{Builder, Runtime};

fn create_custom_runtime() -> Runtime {
    Builder::new_multi_thread()
        .worker_threads(4)                    // Number of worker threads
        .thread_name("my-tokio-worker")       // Thread name prefix
        .thread_stack_size(3 * 1024 * 1024)  // Stack size per thread
        .enable_all()                         // Enable I/O and time
        .build()
        .unwrap()
}

// Current thread runtime (single-threaded)
fn create_current_thread_runtime() -> Runtime {
    Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
}

// Multi-threaded runtime (default)
// - Uses work-stealing scheduler
// - Distributes tasks across threads
// - Better for CPU-bound workloads

// Current thread runtime
// - Single-threaded
// - Lower overhead
// - Better for I/O-bound with few tasks
*/


// ============================================================================
// 3. SPAWNING TASKS
// ============================================================================

/*
#[tokio::main]
async fn main() {
    // Spawn a task (runs on the runtime)
    let handle = tokio::spawn(async {
        println!("Task running on runtime");
        42
    });
    
    // Wait for task to complete
    let result = handle.await.unwrap();
    println!("Task result: {}", result);
    
    // Spawn multiple tasks
    let mut handles = vec![];
    
    for i in 0..10 {
        let handle = tokio::spawn(async move {
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
            println!("Task {} completed", i);
            i * 2
        });
        handles.push(handle);
    }
    
    // Wait for all tasks
    for handle in handles {
        let result = handle.await.unwrap();
        println!("Result: {}", result);
    }
}
*/

/// SPAWNING VS ASYNC BLOCKS:
/// 
/// tokio::spawn():
/// - Creates a new task
/// - Runs concurrently
/// - Can continue even if parent is cancelled
/// - Must be 'static (no borrowed data)
/// 
/// async block:
/// - Runs inline
/// - Shares lifetime with parent
/// - Can borrow local data
/// - Cancelled if parent is cancelled


// ============================================================================
// 4. TASK CANCELLATION
// ============================================================================

/*
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    // Spawn task with handle
    let handle = tokio::spawn(async {
        loop {
            println!("Working...");
            sleep(Duration::from_secs(1)).await;
        }
    });
    
    // Let it run for a bit
    sleep(Duration::from_secs(3)).await;
    
    // Cancel the task
    handle.abort();
    
    // Check if cancelled
    match handle.await {
        Ok(_) => println!("Task completed"),
        Err(e) if e.is_cancelled() => println!("Task was cancelled"),
        Err(e) => println!("Task panicked: {}", e),
    }
}

// Graceful cancellation with tokio::select!
async fn cancellable_task() {
    use tokio::sync::oneshot;
    
    let (tx, mut rx) = oneshot::channel();
    
    tokio::spawn(async move {
        loop {
            tokio::select! {
                _ = &mut rx => {
                    println!("Received cancellation signal");
                    break;
                }
                _ = sleep(Duration::from_secs(1)) => {
                    println!("Working...");
                }
            }
        }
    });
    
    sleep(Duration::from_secs(3)).await;
    let _ = tx.send(());  // Send cancellation signal
}
*/


// ============================================================================
// 5. TOKIO CHANNELS
// ============================================================================

/// Tokio provides several channel types:
/// - oneshot: Single value, one sender, one receiver
/// - mpsc: Multiple producers, single consumer
/// - broadcast: Multiple producers, multiple consumers (cloned)
/// - watch: Single value that changes over time

/*
use tokio::sync::{oneshot, mpsc, broadcast, watch};

// ONESHOT CHANNEL (single value)
async fn demo_oneshot() {
    let (tx, rx) = oneshot::channel();
    
    tokio::spawn(async move {
        let result = expensive_computation().await;
        let _ = tx.send(result);
    });
    
    match rx.await {
        Ok(result) => println!("Got: {}", result),
        Err(_) => println!("Sender dropped"),
    }
}

// MPSC CHANNEL (multiple producers, single consumer)
async fn demo_mpsc() {
    let (tx, mut rx) = mpsc::channel(32);  // Buffer size 32
    
    // Spawn multiple producers
    for i in 0..5 {
        let tx = tx.clone();
        tokio::spawn(async move {
            tx.send(i).await.unwrap();
        });
    }
    
    drop(tx);  // Drop original sender
    
    // Receive all messages
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}

// BROADCAST CHANNEL (publish-subscribe)
async fn demo_broadcast() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();
    
    tokio::spawn(async move {
        for i in 0..5 {
            tx.send(i).unwrap();
        }
    });
    
    // Both receivers get all messages
    tokio::spawn(async move {
        while let Ok(msg) = rx1.recv().await {
            println!("Receiver 1: {}", msg);
        }
    });
    
    tokio::spawn(async move {
        while let Ok(msg) = rx2.recv().await {
            println!("Receiver 2: {}", msg);
        }
    });
}

// WATCH CHANNEL (state changes)
async fn demo_watch() {
    let (tx, mut rx) = watch::channel(0);
    
    tokio::spawn(async move {
        for i in 1..=5 {
            tx.send(i).unwrap();
            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    });
    
    // Receiver only sees latest value
    while rx.changed().await.is_ok() {
        println!("Value changed to: {}", *rx.borrow());
    }
}
*/


// ============================================================================
// 6. SYNCHRONIZATION PRIMITIVES
// ============================================================================

/*
use tokio::sync::{Mutex, RwLock, Semaphore, Notify, Barrier};

// MUTEX (mutual exclusion)
async fn demo_mutex() {
    let mutex = std::sync::Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for _ in 0..10 {
        let mutex = mutex.clone();
        let handle = tokio::spawn(async move {
            let mut lock = mutex.lock().await;
            *lock += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
    
    println!("Final value: {}", *mutex.lock().await);
}

// RWLOCK (multiple readers or one writer)
async fn demo_rwlock() {
    let lock = std::sync::Arc::new(RwLock::new(0));
    
    // Multiple readers
    let lock1 = lock.clone();
    tokio::spawn(async move {
        let value = lock1.read().await;
        println!("Read: {}", *value);
    });
    
    // Single writer
    let mut write_lock = lock.write().await;
    *write_lock = 42;
}

// SEMAPHORE (limit concurrent access)
async fn demo_semaphore() {
    let semaphore = std::sync::Arc::new(Semaphore::new(3));  // Max 3 concurrent
    
    let mut handles = vec![];
    
    for i in 0..10 {
        let semaphore = semaphore.clone();
        let handle = tokio::spawn(async move {
            let _permit = semaphore.acquire().await.unwrap();
            println!("Task {} acquired permit", i);
            tokio::time::sleep(Duration::from_secs(1)).await;
            println!("Task {} releasing permit", i);
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
}

// NOTIFY (wake up tasks)
async fn demo_notify() {
    let notify = std::sync::Arc::new(Notify::new());
    
    let notify2 = notify.clone();
    tokio::spawn(async move {
        notify2.notified().await;
        println!("Notified!");
    });
    
    tokio::time::sleep(Duration::from_secs(1)).await;
    notify.notify_one();  // Wake one waiter
    // notify.notify_waiters();  // Wake all waiters
}

// BARRIER (synchronization point)
async fn demo_barrier() {
    let barrier = std::sync::Arc::new(Barrier::new(3));
    let mut handles = vec![];
    
    for i in 0..3 {
        let barrier = barrier.clone();
        let handle = tokio::spawn(async move {
            println!("Task {} before barrier", i);
            barrier.wait().await;
            println!("Task {} after barrier", i);
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
}
*/


// ============================================================================
// 7. ASYNC I/O
// ============================================================================

/*
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::fs::File;
use tokio::net::TcpListener;

// FILE I/O
async fn demo_file_io() {
    // Read file
    let mut file = File::open("input.txt").await.unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).await.unwrap();
    
    // Write file
    let mut file = File::create("output.txt").await.unwrap();
    file.write_all(b"Hello, world!").await.unwrap();
}

// TCP SERVER
async fn demo_tcp_server() {
    let listener = TcpListener::bind("127.0.0.1:8080").await.unwrap();
    
    loop {
        let (mut socket, addr) = listener.accept().await.unwrap();
        
        tokio::spawn(async move {
            println!("New connection from: {}", addr);
            
            let mut buf = [0; 1024];
            
            loop {
                match socket.read(&mut buf).await {
                    Ok(0) => break,  // Connection closed
                    Ok(n) => {
                        // Echo back
                        socket.write_all(&buf[..n]).await.unwrap();
                    }
                    Err(e) => {
                        eprintln!("Error: {}", e);
                        break;
                    }
                }
            }
        });
    }
}
*/


// ============================================================================
// 8. TIMERS AND INTERVALS
// ============================================================================

/*
use tokio::time::{sleep, interval, timeout, Instant, Duration};

async fn demo_timers() {
    // Sleep
    sleep(Duration::from_secs(1)).await;
    println!("Slept for 1 second");
    
    // Interval
    let mut interval = interval(Duration::from_millis(500));
    
    for _ in 0..5 {
        interval.tick().await;
        println!("Tick!");
    }
    
    // Timeout
    match timeout(Duration::from_secs(1), slow_operation()).await {
        Ok(result) => println!("Completed: {:?}", result),
        Err(_) => println!("Timed out!"),
    }
    
    // Measure time
    let start = Instant::now();
    expensive_computation().await;
    let duration = start.elapsed();
    println!("Took: {:?}", duration);
}

async fn slow_operation() -> String {
    sleep(Duration::from_secs(2)).await;
    "Done".to_string()
}
*/


// ============================================================================
// 9. TOKIO SELECT - CONCURRENT OPERATIONS
// ============================================================================

/*
use tokio::time::{sleep, Duration};

async fn demo_select() {
    let mut count = 0;
    
    loop {
        tokio::select! {
            // First branch
            _ = sleep(Duration::from_secs(1)) => {
                println!("1 second passed");
                count += 1;
            }
            
            // Second branch
            _ = sleep(Duration::from_millis(500)) => {
                println!("500ms passed");
            }
            
            // Exit condition
            _ = sleep(Duration::from_secs(5)), if count >= 5 => {
                println!("Exiting");
                break;
            }
        }
    }
}

// select! with channels
async fn demo_select_channels() {
    let (tx1, mut rx1) = mpsc::channel(10);
    let (tx2, mut rx2) = mpsc::channel(10);
    
    tokio::spawn(async move {
        tx1.send(1).await.unwrap();
    });
    
    tokio::spawn(async move {
        tx2.send(2).await.unwrap();
    });
    
    tokio::select! {
        Some(val) = rx1.recv() => {
            println!("Got from channel 1: {}", val);
        }
        Some(val) = rx2.recv() => {
            println!("Got from channel 2: {}", val);
        }
    }
}
*/

/// select! PATTERNS:
/// - Race multiple futures
/// - Timeout operations
/// - Cancellation
/// - Priority (biased select)


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/// TOKIO BEST PRACTICES:
/// 
/// TASK SPAWNING:
/// ✓ Use tokio::spawn for independent tasks
/// ✓ Use async blocks for dependent work
/// ✓ Don't spawn too many tasks (use Semaphore)
/// ✓ Handle task panics
/// 
/// CHANNELS:
/// ✓ Choose right channel type
/// ✓ Set appropriate buffer sizes
/// ✓ Drop senders when done
/// ✓ Handle closed channels
/// 
/// SYNCHRONIZATION:
/// ✓ Prefer channels over locks
/// ✓ Use Tokio's async locks, not std
/// ✓ Keep critical sections small
/// ✓ Avoid lock contention
/// 
/// I/O:
/// ✓ Use Tokio's async I/O types
/// ✓ Buffer I/O operations
/// ✓ Set timeouts on I/O
/// ✓ Handle errors gracefully
/// 
/// PERFORMANCE:
/// ✓ Avoid blocking operations in async code
/// ✓ Use spawn_blocking for CPU-intensive work
/// ✓ Configure runtime appropriately
/// ✓ Monitor task count
/// ✓ Profile async performance
/// 
/// ERROR HANDLING:
/// ✓ Handle all errors
/// ✓ Don't unwrap in async code
/// ✓ Use ? operator
/// ✓ Log errors appropriately


// ============================================================================
// 11. BLOCKING OPERATIONS
// ============================================================================

/*
#[tokio::main]
async fn main() {
    // DON'T do this - blocks the runtime
    // std::thread::sleep(Duration::from_secs(1));
    
    // DO this - async sleep
    tokio::time::sleep(Duration::from_secs(1)).await;
    
    // For blocking operations, use spawn_blocking
    let result = tokio::task::spawn_blocking(|| {
        // CPU-intensive work or blocking I/O
        expensive_cpu_work()
    })
    .await
    .unwrap();
    
    println!("Result: {}", result);
}

fn expensive_cpu_work() -> u64 {
    // Simulate CPU-intensive work
    (0..1_000_000).sum()
}
*/


// ============================================================================
// 12. RUNTIME INTROSPECTION
// ============================================================================

/*
use tokio::runtime::Handle;

fn get_runtime_info() {
    let handle = Handle::current();
    
    // Get number of worker threads
    // (requires unstable features or metrics)
    
    println!("Runtime: {:?}", handle);
}
*/


fn main() {
    println!("=== TOKIO DEEP DIVE ===\n");
    println!("This file demonstrates Tokio async runtime.");
    println!("See comments for complete examples.\n");
    
    println!("TOKIO RUNTIME:");
    println!("  • Multi-threaded (default)");
    println!("  • Current-thread (single)");
    println!("  • Work-stealing scheduler");
    println!("  • I/O event loop");
    
    println!("\nTASKS:");
    println!("  • tokio::spawn - Concurrent tasks");
    println!("  • JoinHandle - Wait for tasks");
    println!("  • Cancellation via abort()");
    println!("  • Must be 'static");
    
    println!("\nCHANNELS:");
    println!("  • oneshot - Single value");
    println!("  • mpsc - Multiple producers");
    println!("  • broadcast - Pub/sub");
    println!("  • watch - State changes");
    
    println!("\nSYNC PRIMITIVES:");
    println!("  • Mutex - Mutual exclusion");
    println!("  • RwLock - Read/write lock");
    println!("  • Semaphore - Limit concurrency");
    println!("  • Notify - Wake tasks");
    println!("  • Barrier - Sync point");
    
    println!("\nI/O:");
    println!("  • Async file I/O");
    println!("  • Async networking");
    println!("  • Buffered I/O");
    println!("  • Timeouts");
    
    println!("\nBEST PRACTICES:");
    println!("  ✓ Use tokio::spawn wisely");
    println!("  ✓ Choose right channel type");
    println!("  ✓ Prefer channels over locks");
    println!("  ✓ Never block the runtime");
    println!("  ✓ Use spawn_blocking for CPU work");
    println!("  ✓ Set timeouts on I/O");
    
    println!("\n=== Complete ===");
}

/// DEPENDENCIES:
/// ```toml
/// [dependencies]
/// tokio = { version = "1", features = ["full"] }
/// ```

/// KEY TAKEAWAYS:
/// 
/// 1. Tokio provides async runtime for Rust
/// 2. Multi-threaded by default (work-stealing)
/// 3. Use tokio::spawn for concurrent tasks
/// 4. Choose appropriate channel type
/// 5. Use Tokio's async locks, not std
/// 6. Never block the runtime (use spawn_blocking)
/// 7. Set timeouts on I/O operations
/// 8. Handle task cancellation gracefully
/// 9. Prefer channels over locks
/// 10. Monitor and tune runtime configuration
/// 11. Profile async performance
/// 12. Test async code thoroughly
/// 
/// COMMON PITFALLS:
/// ✗ Blocking operations in async code
/// ✗ Using std synchronization primitives
/// ✗ Not handling channel closure
/// ✗ Spawning too many tasks
/// ✗ Not setting timeouts
/// ✗ Holding locks across await points
/// ✗ Not handling task panics
