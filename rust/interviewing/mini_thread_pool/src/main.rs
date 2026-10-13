/*
Mini Thread Pool
--------------------------------------------------------
pub struct ThreadPool { ... }

pub fn execute<F>(&self, job: F)
where
    F: FnOnce() + Send + 'static

Senior signal:
- mpsc channels
- Worker lifecycle
- Drop handling
*/
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Duration;

type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: Option<mpsc::Sender<Job>>,
}

impl ThreadPool {
    pub fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::new();

        for _ in 0..size {
            let rx = Arc::clone(&receiver);
            let handle = thread::spawn(move || {
                while let Ok(job) = rx.lock().unwrap().recv() {
                    job();
                }
            });

            workers.push(handle);
        }

        Self {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, job: F)
    where
        F: FnOnce() + Send + 'static,
    {
        if let Some(sender) = &self.sender {
            sender.send(Box::new(job)).unwrap();
        }
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in self.workers.drain(..) {
            worker.join().unwrap()
        }
    }
}

fn main() {
    println!("Test 1: All jobs execute");

    let pool = ThreadPool::new(4);
    let counter = Arc::new(Mutex::new(0));

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        pool.execute(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
    }

    drop(pool); // ensure all jobs complete

    let result = *counter.lock().unwrap();
    println!("Expected: 10, Got: {}", result);
    assert_eq!(result, 10);

    println!("Test 2: Parallel execution demo");

    let pool = ThreadPool::new(2);

    for i in 0..4 {
        pool.execute(move || {
            println!("Starting job {}", i);
            thread::sleep(Duration::from_millis(500));
            println!("Finished job {}", i);
        });
    }

    println!("Main thread done submitting jobs.");
}
