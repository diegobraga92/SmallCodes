// =============================================================================
// sqlite_repo.rs — SQLite TaskRepository Implementation
// =============================================================================
//
// This is the concrete implementation of the TaskRepository trait using SQLite.
//
// WHY SQLITE?
//   - Zero configuration: no server to install, no connection strings to manage
//   - Single file: the entire database is one .db file
//   - Good enough: for a demo with low concurrency, SQLite performs well
//   - sqlx support: first-class async SQLite support via sqlx
//
// TRADEOFF: SQLite vs PostgreSQL
//   SQLite: Single-writer, no network, file-based, great for dev/demo
//   PostgreSQL: Multi-writer, network-based, production-grade, needs server
//   For this demo, SQLite is perfect. In production, you'd swap to Postgres.
//
// WHY SYNC TRAIT METHODS WITH block_in_place?
//   The TaskRepository trait is synchronous (not async). This is a deliberate
//   simplification to avoid needing #[async_trait]. However, sqlx queries
//   are async. We bridge this gap using:
//   1. tokio::task::block_in_place — allows blocking on the current thread
//   2. tokio::runtime::Handle::current() — gets the current tokio runtime
//   3. rt.block_on() — runs the async query synchronously
//
//   TRADEOFF: This blocks a tokio worker thread while the query runs.
//   For SQLite (microsecond queries), this is fine.
//   For Postgres (millisecond queries), this would waste threads.
//   In production, you'd make the trait async.
// =============================================================================

use crate::application::create_task::TaskRepository;
use shared::domain::{Task, TaskStatus};
use sqlx::SqlitePool;

/// SQLite-backed implementation of TaskRepository.
pub struct SqliteTaskRepository {
    pool: SqlitePool,
}

impl SqliteTaskRepository {
    /// Create a new repository with the given connection pool.
    pub fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }

    /// Create the tasks table if it doesn't exist.
    ///
    /// WHY NOT USE SQL MIGRATIONS?
    ///   sqlx supports compile-time checked migrations, but for this demo
    ///   a simple CREATE TABLE IF NOT EXISTS is sufficient. In production,
    ///   you'd use `sqlx migrate run` with versioned migration files.
    pub async fn init(&self) -> Result<(), sqlx::Error> {
        sqlx::query(
            "CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
            )",
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }
}

impl TaskRepository for SqliteTaskRepository {
    /// Save a new task to the database.
    ///
    /// WHY tokio::spawn?
    ///   The trait method is synchronous, but sqlx queries are async.
    ///   We use tokio::spawn to run the query on a tokio worker thread.
    ///   This is "fire-and-forget" — we don't wait for the result.
    ///
    ///   TRADEOFF: If the insert fails, we won't know (the .expect() will
    ///   panic in the background task). In production, you'd want error
    ///   handling and retry logic here.
    fn save(&self, task: &Task) {
        let pool = self.pool.clone();
        let id = task.id.clone();
        let description = task.description.clone();
        let status = task.status.as_str().to_string();

        tokio::spawn(async move {
            sqlx::query("INSERT INTO tasks (id, description, status) VALUES (?, ?, ?)")
                .bind(&id)
                .bind(&description)
                .bind(&status)
                .execute(&pool)
                .await
                .expect("Failed to insert task");
        });
    }

    /// Find a task by its ID.
    ///
    /// WHY block_in_place + block_on?
    ///   The trait is sync, but sqlx is async. We use block_in_place to
    ///   tell tokio "this thread will block, please allow it" and then
    ///   block_on to run the async query synchronously.
    ///
    ///   This pattern is acceptable for SQLite because queries are fast.
    ///   For a network database, you'd want async traits.
    fn find_by_id(&self, id: &str) -> Option<Task> {
        let pool = self.pool.clone();
        let id = id.to_string();

        tokio::task::block_in_place(|| {
            let rt = tokio::runtime::Handle::current();
            rt.block_on(async {
                // query_as maps each row to a tuple (id, description, status)
                // We use a tuple instead of a custom struct for simplicity.
                sqlx::query_as::<_, (String, String, String)>(
                    "SELECT id, description, status FROM tasks WHERE id = ?",
                )
                .bind(&id)
                .fetch_optional(&pool)
                .await
                .ok() // Convert Result to Option (ignore errors)
                .flatten() // Unwrap Option<Option<T>> to Option<T>
                .map(|(id, description, status)| Task {
                    id,
                    description,
                    // Parse the status string back to enum.
                    // Default to Pending if the value is somehow invalid.
                    status: TaskStatus::from_str(&status).unwrap_or(TaskStatus::Pending),
                })
            })
        })
    }

    /// Update a task's status.
    ///
    /// Same fire-and-forget pattern as save().
    fn update_status(&self, id: &str, status: &TaskStatus) {
        let pool = self.pool.clone();
        let id = id.to_string();
        let status_str = status.as_str().to_string();

        tokio::spawn(async move {
            sqlx::query("UPDATE tasks SET status = ? WHERE id = ?")
                .bind(&status_str)
                .bind(&id)
                .execute(&pool)
                .await
                .expect("Failed to update task status");
        });
    }
}
