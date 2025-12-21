use std::{
    pin::Pin,
    sync::Arc,
    time::Duration,
};

use tokio::{
    sync::Mutex,
    task::JoinHandle,
    time::sleep,
};

use async_trait::async_trait;
use serde::Deserialize;
use thiserror::Error;

/* -------------------------------------------------
 * ERROR HANDLING
 * ------------------------------------------------- */

#[derive(Debug, Error)]
pub enum AppError {
    #[error("http error")]
    Http(#[from] reqwest::Error),

    #[error("invalid input: {0}")]
    InvalidInput(String),
}

type AppResult<T> = Result<T, AppError>;

/* -------------------------------------------------
 * SERDE MODEL
 * ------------------------------------------------- */

#[derive(Debug, Deserialize)]
struct Todo {
    id: u64,
    title: String,
    completed: bool,
}

/* -------------------------------------------------
 * SHARED STATE
 * ------------------------------------------------- */

#[derive(Debug)]
struct Stats {
    requests: u64,
}

impl Stats {
    fn increment(&mut self) {
        self.requests += 1;
    }
}

/* -------------------------------------------------
 * LIFETIME-BOUND CONFIG
 * ------------------------------------------------- */

/// Configuration borrowed from the caller.
///
/// This struct does NOT own the data.
/// `'a` ties the lifetime of the struct to the input references.
struct Config<'a> {
    base_url: &'a str,
    user_agent: &'a str,
}

/* -------------------------------------------------
 * ASYNC TRAIT
 * ------------------------------------------------- */

#[async_trait]
trait Worker: Send + Sync {
    async fn do_work(&self, id: u64) -> AppResult<()>;
}

/* -------------------------------------------------
 * WORKER IMPLEMENTATION WITH LIFETIMES
 * ------------------------------------------------- */

/// Worker holds references with lifetime `'a`
///
/// This is safe because:
/// - The worker itself is not moved after creation
/// - The borrowed data outlives the worker
struct HttpWorker<'a> {
    client: reqwest::Client,
    config: Config<'a>,
    stats: Arc<Mutex<Stats>>,
}

impl<'a> HttpWorker<'a> {
    fn new(
        client: reqwest::Client,
        config: Config<'a>,
        stats: Arc<Mutex<Stats>>,
    ) -> Self {
        Self {
            client,
            config,
            stats,
        }
    }

    /// Async method borrowing `self`
    ///
    /// The borrow of `&self` is held across `.await`,
    /// which is allowed because `self` is owned by the task.
    async fn fetch_todo(&self, id: u64) -> AppResult<Todo> {
        let url = format!("{}/todos/{id}", self.config.base_url);

        let response = self
            .client
            .get(url)
            .header("User-Agent", self.config.user_agent)
            .send()
            .await?
            .error_for_status()?;

        let todo = response.json::<Todo>().await?;
        Ok(todo)
    }
}

#[async_trait]
impl<'a> Worker for HttpWorker<'a> {
    async fn do_work(&self, id: u64) -> AppResult<()> {
        let todo = self.fetch_todo(id).await?;

        {
            let mut stats = self.stats.lock().await;
            stats.increment();
        }

        println!(
            "Fetched todo {} → {}",
            todo.id, todo.title
        );

        Ok(())
    }
}

/* -------------------------------------------------
 * FUTURE + PIN
 * ------------------------------------------------- */

fn pinned_future_example() -> Pin<Box<dyn std::future::Future<Output = ()> + Send>> {
    Box::pin(async {
        println!("Pinned future running");
        sleep(Duration::from_millis(100)).await;
        println!("Pinned future finished");
    })
}

/* -------------------------------------------------
 * TASK SPAWNING
 * ------------------------------------------------- */

async fn run_workers(worker: Arc<dyn Worker>) -> AppResult<()> {
    let mut handles = Vec::<JoinHandle<AppResult<()>>>::new();

    for id in 1..=5 {
        let worker = worker.clone();
        handles.push(tokio::spawn(async move {
            worker.do_work(id).await
        }));
    }

    for handle in handles {
        handle.await??;
    }

    Ok(())
}

/* -------------------------------------------------
 * MAIN
 * ------------------------------------------------- */

#[tokio::main]
async fn main() -> AppResult<()> {
    let stats = Arc::new(Mutex::new(Stats { requests: 0 }));

    // Data that will be borrowed
    let base_url = "https://jsonplaceholder.typicode.com";
    let user_agent = "tokio-lifetime-demo";

    let config = Config {
        base_url,
        user_agent,
    };

    let client = reqwest::Client::new();

    // Worker borrows `config` via lifetime `'a`
    let worker: Arc<dyn Worker> = Arc::new(
        HttpWorker::new(client, config, stats.clone())
    );

    run_workers(worker).await?;

    pinned_future_example().await;

    let final_stats = stats.lock().await;
    println!("Total requests made: {}", final_stats.requests);

    Ok(())
}
