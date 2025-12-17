//// Message Passing libs
/// crossbeam, best for high-performance
use crossbeam_channel::{bounded, unbounded, select};
use std::thread;

// More features than std::mpsc
let (tx, rx) = unbounded();  // Unbounded channel

// Select on multiple channels
let (tx1, rx1) = bounded(1);
let (tx2, rx2) = bounded(1);

thread::spawn(move || {
    tx1.send("channel 1").unwrap();
});

thread::spawn(move || {
    thread::sleep(std::time::Duration::from_millis(100));
    tx2.send("channel 2").unwrap();
});

select! {
    recv(rx1) -> msg => println!("Got from rx1: {:?}", msg),
    recv(rx2) -> msg => println!("Got from rx2: {:?}", msg),
    default(std::time::Duration::from_millis(500)) => println!("Timeout"),
}

// Advanced patterns
let (tx, rx) = bounded(0);  // Rendezvous channel (no buffer)

thread::spawn(move || {
    tx.send("message").unwrap();  // Blocks until receiver is ready
});

let msg = rx.recv().unwrap();  // Blocks until sender is ready
println!("Got: {}", msg);



/// tokio message passing, async, non-blocking
use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    // Async MPSC channel
    let (mut tx, mut rx) = mpsc::channel::<i32>(100);  // Buffer size
    
    // Producer task
    let producer = tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
            sleep(Duration::from_millis(100)).await;
        }
    });
    
    // Consumer task
    let consumer = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Received: {}", msg);
        }
    });
    
    tokio::join!(producer, consumer).0.unwrap();
}

// Broadcast channel (multiple consumers)
use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (tx, _) = broadcast::channel::<String>(16);
    
    let mut rx1 = tx.subscribe();
    let mut rx2 = tx.subscribe();
    
    tokio::spawn(async move {
        tx.send("Hello".to_string()).unwrap();
        tx.send("World".to_string()).unwrap();
    });
    
    let task1 = tokio::spawn(async move {
        println!("Task 1: {}", rx1.recv().await.unwrap());
        println!("Task 1: {}", rx1.recv().await.unwrap());
    });
    
    let task2 = tokio::spawn(async move {
        println!("Task 2: {}", rx2.recv().await.unwrap());
        println!("Task 2: {}", rx2.recv().await.unwrap());
    });
    
    tokio::join!(task1, task2);
}



//// async/await
/// Future Trait
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

// The Future trait
pub trait Future {
    type Output;
    
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

// Simple future example
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
            // Schedule wakeup
            let waker = cx.waker().clone();
            let duration = self.duration;
            
            std::thread::spawn(move || {
                std::thread::sleep(duration);
                waker.wake();  // Notify executor
            });
            
            self.elapsed = true;
            Poll::Pending
        }
    }
}

// Using async/await
async fn async_function() -> i32 {
    let result = some_async_operation().await;
    result * 2
}


/// Pin and Unpin
use std::pin::Pin;
use std::marker::PhantomPinned;

// Pin: Guarantees an object won't be moved in memory
// Unpin: Types that can be safely moved (most types)

// Regular types are Unpin by default
struct RegularStruct {
    data: i32,
}  // Auto-implements Unpin

// Types that are !Unpin (cannot be moved)
struct NotUnpin {
    data: i32,
    _pin: PhantomPinned,  // Opts out of Unpin
}

// Pin guarantees for !Unpin types
let mut not_unpin = NotUnpin {
    data: 42,
    _pin: PhantomPinned,
};

// Pin it to stack (unsafe because we guarantee it won't move)
let pinned = unsafe { Pin::new_unchecked(&mut not_unpin) };

// Can't move pinned value
// let moved = pinned;  // ERROR

// Safe pinning for Unpin types
let mut regular = RegularStruct { data: 42 };
let pinned_regular = Pin::new(&mut regular);  // Safe
// Can still move regular if needed

// Why Pin matters for async
async fn async_example() {
    let local = 42;
    let _ = &local;  // Creates a reference
    
    // If the future was moved, the reference would be invalid!
    // That's why futures generated from async fn are !Unpin
    // when they contain references to local variables.
}

/// Async Patterns
use tokio::time::{sleep, Duration};

// 1. Timeouts
async fn with_timeout<F, T>(fut: F, timeout: Duration) -> Result<T, tokio::time::error::Elapsed>
where
    F: Future<Output = T>,
{
    tokio::time::timeout(timeout, fut).await
}

// 2. Select (first completed)
async fn select_example() {
    tokio::select! {
        result = async_operation1() => {
            println!("Operation 1 completed: {:?}", result);
        }
        result = async_operation2() => {
            println!("Operation 2 completed: {:?}", result);
        }
        _ = sleep(Duration::from_secs(5)) => {
            println!("Timeout");
        }
    }
}

// 3. Join (run concurrently, wait for all)
async fn join_example() {
    let (result1, result2) = tokio::join!(
        async_operation1(),
        async_operation2(),
    );
    println!("Results: {:?}, {:?}", result1, result2);
}

// 4. Stream processing
use tokio_stream::{Stream, StreamExt};

async fn process_stream<S>(mut stream: S)
where
    S: Stream<Item = i32> + Unpin,
{
    while let Some(item) = stream.next().await {
        println!("Got: {}", item);
    }
}

// 5. Async trait objects
trait AsyncTrait {
    async fn operation(&self) -> i32;
}

// Using async-trait crate
#[async_trait::async_trait]
impl AsyncTrait for MyType {
    async fn operation(&self) -> i32 {
        // async implementation
        42
    }
}



//// Executors and Reactors
/// Executor, drives futures to completion
// Simple executor example
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Wake, Waker};
use std::sync::Arc;
use std::collections::VecDeque;

struct Task {
    future: Pin<Box<dyn Future<Output = ()>>>,
}

impl Task {
    fn new(future: impl Future<Output = ()> + 'static) -> Self {
        Task {
            future: Box::pin(future),
        }
    }
    
    fn poll(&mut self, context: &mut Context) -> Poll<()> {
        self.future.as_mut().poll(context)
    }
}

// Waker implementation
struct DummyWaker;

impl Wake for DummyWaker {
    fn wake(self: Arc<Self>) {
        // Notify executor
    }
}

// Simple single-threaded executor
struct Executor {
    tasks: VecDeque<Task>,
}

impl Executor {
    fn new() -> Self {
        Executor {
            tasks: VecDeque::new(),
        }
    }
    
    fn spawn(&mut self, future: impl Future<Output = ()> + 'static) {
        self.tasks.push_back(Task::new(future));
    }
    
    fn run(&mut self) {
        let waker = Arc::new(DummyWaker).into();
        let mut context = Context::from_waker(&waker);
        
        while let Some(mut task) = self.tasks.pop_front() {
            match task.poll(&mut context) {
                Poll::Ready(()) => {
                    // Task completed
                }
                Poll::Pending => {
                    // Task not ready, reschedule
                    self.tasks.push_back(task);
                }
            }
        }
    }
}

// Usage
async fn example_task() {
    println!("Task running");
}

fn main() {
    let mut executor = Executor::new();
    executor.spawn(example_task());
    executor.run();
}

/// Reactor, notifies when IO is Ready
// Simple reactor using mio (low-level IO multiplexing)
use mio::{Events, Interest, Poll, Token};
use mio::net::TcpListener;
use std::io;

struct Reactor {
    poll: Poll,
    events: Events,
}

impl Reactor {
    fn new() -> io::Result<Self> {
        let poll = Poll::new()?;
        let events = Events::with_capacity(128);
        Ok(Reactor { poll, events })
    }
    
    fn register(&self, listener: &TcpListener, token: Token) -> io::Result<()> {
        self.poll.registry()
            .register(listener, token, Interest::READABLE)?;
        Ok(())
    }
    
    fn poll(&mut self) -> io::Result<()> {
        self.poll.poll(&mut self.events, None)?;
        
        for event in self.events.iter() {
            let token = event.token();
            // Notify task associated with this token
            println!("IO ready for token: {:?}", token);
        }
        
        Ok(())
    }
}
// The reactor notifies executors when IO operations are ready


/// Tokio
// Tokio combines executor and reactor
#[tokio::main]  // Creates a multi-threaded executor
async fn main() {
    // Runtime includes:
    // 1. Multi-threaded executor (for CPU-bound tasks)
    // 2. IO driver (reactor using epoll/kqueue/IOCP)
    // 3. Timer driver (for timeouts and delays)
    
    // Spawn tasks on executor
    let handle = tokio::spawn(async {
        // This runs on tokio's executor
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        42
    });
    
    // Block on future (driven by executor)
    let result = handle.await.unwrap();
    println!("Result: {}", result);
}

// Custom runtime configuration
fn custom_runtime() -> tokio::runtime::Runtime {
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)  // 4 worker threads
        .enable_io()        // Enable IO driver
        .enable_time()      // Enable timer
        .thread_name("my-worker")
        .build()
        .unwrap()
}