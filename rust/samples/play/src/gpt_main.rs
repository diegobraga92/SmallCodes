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
    async fn fetch_todo(&sel_
