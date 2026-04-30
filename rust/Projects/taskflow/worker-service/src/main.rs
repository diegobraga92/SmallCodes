// =============================================================================
// worker-service/src/main.rs — Worker Service Entry Point
// =============================================================================
//
// This is the standalone Worker service binary. It connects to the same SQLite
// database as the API service and processes tasks asynchronously.
//
// HOW THE WORKER GETS EVENTS:
//   In a real distributed system, the worker would subscribe to a Kafka topic
//   or RabbitMQ queue. The API service would publish events to the same broker.
//
//   In this local demo, the worker creates its OWN event bus and listens on it.
//   This means the standalone worker will NEVER receive events from the API
//   service when running separately. Events only flow when both services run
//   in the same process (see the `taskflow` combined binary).
//
//   WHY BOTHER WITH THE STANDALONE BINARY THEN?
//   - It demonstrates the architecture of a separate worker service
//   - It shows how the worker would be structured in production
//   - It can be extended to connect to a real message broker
//   - It's useful for testing worker logic in isolation
//
// POLLING FALLBACK:
//   In production, you'd add a startup scan for Pending tasks:
//   ```rust
//   // On startup, find all tasks with status = 'Pending' and process them
//   let pending_tasks = repo.find_by_status("Pending");
//   for task in pending_tasks {
//       tokio::spawn(process_task(&repo, &task));
//   }
//   ```
//   This handles the case where the worker crashed and restarted — any tasks
//   that were left in Pending state get picked up.
// =============================================================================

use shared::domain::{Task, TaskStatus};
use shared::events::{EventBus, InMemoryEventBus, TaskEvent};
use sqlx::SqlitePool;
use std::sync::Arc;
use tokio::sync::broadcast;

// =============================================================================
// TaskRepository Trait
// =============================================================================
//
// WHY REDEFINE THIS HERE INSTEAD OF USING THE ONE FROM api-service?
//   The worker-service crate doesn't depend on api-service. It only depends
//   on shared. The TaskRepository trait is defined in api-service's application
//   layer, so we can't use it here without creating a circular dependency.
//
//   In a larger project, you'd extract TaskRepository into the shared crate.
//   For this demo, the duplication is acceptable.
//
// WHY DOES THE WORKER ONLY NEED find_by_id AND update_status?
//   The worker doesn't create tasks — it only processes existing ones.
//   It needs to:
//   - Read task details (find_by_id)
//   - Update task status (update_status)
//   It does NOT need save() — that's the API service's job.
trait TaskRepository: Send + Sync {
    fn find_by_id(&self, id: &str) -> Option<Task>;
    fn update_status(&self, id: &str, status: &TaskStatus);
}

impl<T: TaskRepository> TaskRepository for Arc<T> {
    fn find_by_id(&self, id: &str) -> Option<Task> {
        T::find_by_id(self, id)
    }
    fn update_status(&self, id: &str, status: &TaskStatus) {
        T::update_status(self, id, status);
    }
}

// =============================================================================
// SQLite Repository (Worker-specific)
// =============================================================================
//
// Same pattern as SqliteTaskRepository in api-service, but only implements
// the methods the worker needs (no save()).
struct SqliteWorkerRepository {
    pool: SqlitePool,
}

impl SqliteWorkerRepository {
    fn new(pool: SqlitePool) -> Self {
        Self { pool }
    }
}

impl TaskRepository for SqliteWorkerRepository {
    fn find_by_id(&self, id: &str) -> Option<Task> {
        let pool = self.pool.clone();
        let id = id.to_string();

        tokio::task::block_in_place(|| {
            let rt = tokio::runtime::Handle::current();
            rt.block_on(async {
                sqlx::query_as::<_, (String, String, String)>(
                    "SELECT id, description, status FROM tasks WHERE id = ?",
                )
                .bind(&id)
                .fetch_optional(&pool)
                .await
                .ok()
                .flatten()
                .map(|(id, description, status)| Task {
                    id,
                    description,
                    status: TaskStatus::from_str(&status).unwrap_or(TaskStatus::Pending),
                })
            })
        })
    }

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

// =============================================================================
// Task Processing Logic
// =============================================================================
//
// RETRY STRATEGY EXPLANATION:
//   We use a simple retry-with-random-failure pattern to demonstrate how
//   retry logic works in an event-driven system.
//
//   The flow:
//   1. Mark task as Processing
//   2. Simulate work (sleep 2 seconds)
//   3. Randomly fail (50% chance) on attempts 1 and 2
//   4. Always succeed on attempt 3
//   5. If all 3 attempts fail, log an error
//
//   WHY RANDOM FAILURE?
//   To demonstrate the retry mechanism. Without it, every task would succeed
//   on the first attempt and you'd never see retries in action.
//
//   PRODUCTION RETRY STRATEGY:
//   - Exponential backoff: wait 1s, then 2s, then 4s, then 8s...
//   - Jitter: add random delay to prevent thundering herd
//   - Circuit breaker: stop retrying after N failures in a time window
//   - Dead-letter queue: move permanently failed tasks to a separate queue
//   - Alerting: notify operators when tasks fail repeatedly

/// Process a single task with retry logic.
async fn process_task(repo: &impl TaskRepository, task: &Task) {
    let max_retries = 3;
    let task_id = task.id.clone();

    for attempt in 1..=max_retries {
        tracing::info!(
            task_id = %task_id,
            attempt = attempt,
            "Processing task"
        );

        // Mark as Processing (idempotent — safe to call multiple times)
        repo.update_status(&task_id, &TaskStatus::Processing);

        // Simulate work (2 seconds)
        // In production, this would be actual work like:
        // - Transcoding a video
        // - Generating a PDF report
        // - Calling an external API
        // - Running a machine learning model
        tokio::time::sleep(std::time::Duration::from_secs(2)).await;

        // Simulate random failure on early attempts (for retry demo)
        // fastrand::bool() returns true ~50% of the time
        if attempt < max_retries && fastrand::bool() {
            tracing::warn!(
                task_id = %task_id,
                attempt = attempt,
                "Task processing failed, retrying..."
            );
            tokio::time::sleep(std::time::Duration::from_secs(1)).await;
            continue;
        }

        // Mark as Done
        repo.update_status(&task_id, &TaskStatus::Done);
        tracing::info!(task_id = %task_id, attempt = attempt, "Task completed");
        return;
    }

    // All retries exhausted — task failed permanently
    tracing::error!(task_id = %task_id, "Task failed after all retries");
}

// =============================================================================
// Worker Event Loop
// =============================================================================
//
// The worker loop listens for TaskCreated events and spawns a new tokio task
// for each one. This allows concurrent processing of multiple tasks.
//
// WHY tokio::spawn?
//   Without it, the worker would process tasks sequentially:
//     Task 1: sleep 2s -> complete
//     Task 2: sleep 2s -> complete
//     Total: 4 seconds
//
//   With tokio::spawn, tasks run concurrently:
//     Task 1: sleep 2s -> complete
//     Task 2: sleep 2s -> complete (in parallel)
//     Total: ~2 seconds
//
// CONCURRENCY LIMIT:
//   Currently unlimited — every event spawns a new task.
//   In production, you'd use tokio::sync::Semaphore to limit concurrency:
//   ```rust
//   let semaphore = Arc::new(Semaphore::new(10)); // max 10 concurrent
//   let permit = semaphore.acquire().await.unwrap();
//   tokio::spawn(async move {
//       let _permit = permit; // held until task completes
//       process_task(...).await;
//   });
//   ```
async fn worker_loop(mut rx: broadcast::Receiver<TaskEvent>, repo: Arc<SqliteWorkerRepository>) {
    while let Ok(event) = rx.recv().await {
        match event {
            TaskEvent::Created(task) => {
                tracing::info!(task_id = %task.id, "Worker received task event");
                let repo = repo.clone();
                tokio::spawn(async move {
                    process_task(&*repo, &task).await;
                });
            }
        }
    }
}

// =============================================================================
// Main
// =============================================================================

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .with_env_filter("worker_service=info")
        .init();

    // Connect to the same SQLite database as the API service
    let db_url = "sqlite:./nextlink.db?mode=rwc";
    let pool = SqlitePool::connect(db_url).await?;
    let repo = Arc::new(SqliteWorkerRepository::new(pool));

    // Create an event bus. In a real distributed system, this would be
    // a Kafka consumer. For this local demo, the worker creates its own
    // bus and listens on it.
    //
    // NOTE: When running standalone, this worker will never receive events
    // from the API service. Use the combined binary (`cargo run --bin taskflow`)
    // for a working end-to-end demo.
    let event_bus = Arc::new(InMemoryEventBus::new(100));
    let rx = event_bus.subscribe();

    tracing::info!("Worker service started, waiting for tasks...");

    worker_loop(rx, repo).await;

    Ok(())
}
