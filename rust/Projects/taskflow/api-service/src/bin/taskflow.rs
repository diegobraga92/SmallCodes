// =============================================================================
// taskflow.rs — Combined API + Worker Binary
// =============================================================================
//
// This binary runs BOTH the API gRPC server and the Worker loop in a single
// process, sharing the same event bus via an in-memory broadcast channel.
//
// WHY A COMBINED BINARY?
//   The separate api-service and worker-service binaries each create their own
//   event bus. In a real distributed system, they'd connect to the same Kafka
//   topic. But for local development, that requires running Kafka.
//
//   This combined binary solves that: both services share the same event bus
//   instance, so events flow from API to Worker instantly. No Kafka needed.
//
//   Tradeoff: This is a monolith. In production, you'd deploy them separately.
//   But for demo purposes, one command (`cargo run --bin taskflow`) starts
//   everything.
//
// WHY DUPLICATE CODE FROM api-service AND worker-service?
//   This binary re-implements the repository and gRPC service inline instead
//   of reusing the modules from api-service/src/. This is intentional:
//   - The combined binary is a separate entry point with different wiring
//   - It includes worker logic that the standalone API binary doesn't need
//   - It avoids circular dependencies (worker-service can't depend on api-service)
//
//   In a larger project, you'd extract the shared code into a library crate.
//   For this demo, the duplication is acceptable for clarity.
// =============================================================================

use shared::domain::{Task, TaskStatus};
use shared::events::{EventBus, InMemoryEventBus, TaskEvent};
use shared::proto::task_service_server::{TaskService, TaskServiceServer};
use shared::proto::{
    CreateTaskRequest, CreateTaskResponse, GetTaskStatusRequest, GetTaskStatusResponse,
};
use sqlx::SqlitePool;
use std::sync::Arc;
use tokio::sync::broadcast;
use tonic::{Request, Response, Status};
use uuid::Uuid;

// =============================================================================
// Repository (duplicated from api-service/src/infrastructure/sqlite_repo.rs)
// =============================================================================
//
// WHY REDEFINE THE TRAIT AND IMPL HERE?
//   The TaskRepository trait is defined in api-service/src/application/.
//   This binary can't use it because it's a separate binary target within
//   the same crate. We redefine it here for self-containment.
//
//   In a real project, you'd extract TaskRepository into the shared crate.

trait TaskRepository: Send + Sync {
    fn save(&self, task: &Task);
    fn find_by_id(&self, id: &str) -> Option<Task>;
    fn update_status(&self, id: &str, status: &TaskStatus);
}

impl<T: TaskRepository> TaskRepository for Arc<T> {
    fn save(&self, task: &Task) {
        T::save(self, task);
    }
    fn find_by_id(&self, id: &str) -> Option<Task> {
        T::find_by_id(self, id)
    }
    fn update_status(&self, id: &str, status: &TaskStatus) {
        T::update_status(self, id, status);
    }
}

/// SQLite repository implementation (same as SqliteTaskRepository in api-service).
struct SqliteRepo {
    pool: SqlitePool,
}

impl SqliteRepo {
    async fn new(db_url: &str) -> Result<Self, sqlx::Error> {
        let pool = SqlitePool::connect(db_url).await?;
        let repo = Self { pool };
        repo.init().await?;
        Ok(repo)
    }

    async fn init(&self) -> Result<(), sqlx::Error> {
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

impl TaskRepository for SqliteRepo {
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
// gRPC Service (duplicated from api-service/src/main.rs)
// =============================================================================

struct GrpcService {
    repo: Arc<SqliteRepo>,
    event_bus: Arc<InMemoryEventBus>,
}

#[tonic::async_trait]
impl TaskService for GrpcService {
    async fn create_task(
        &self,
        request: Request<CreateTaskRequest>,
    ) -> Result<Response<CreateTaskResponse>, Status> {
        let description = request.into_inner().description;

        if description.trim().is_empty() {
            return Err(Status::invalid_argument("Description cannot be empty"));
        }

        let task = Task {
            id: Uuid::new_v4().to_string(),
            description,
            status: TaskStatus::Pending,
        };

        self.repo.save(&task);
        self.event_bus.publish(TaskEvent::Created(task.clone()));

        tracing::info!(task_id = %task.id, "Task created via gRPC");

        Ok(Response::new(CreateTaskResponse { task_id: task.id }))
    }

    async fn get_task_status(
        &self,
        request: Request<GetTaskStatusRequest>,
    ) -> Result<Response<GetTaskStatusResponse>, Status> {
        let task_id = request.into_inner().task_id;

        match self.repo.find_by_id(&task_id) {
            Some(task) => Ok(Response::new(GetTaskStatusResponse {
                task_id: task.id,
                status: task.status.as_str().to_string(),
                description: task.description,
            })),
            None => Err(Status::not_found(format!("Task {} not found", task_id))),
        }
    }
}

// =============================================================================
// Worker (duplicated from worker-service/src/main.rs)
// =============================================================================
//
// The worker processes tasks asynchronously with retry logic.
//
// RETRY STRATEGY:
//   - Maximum 3 attempts
//   - Each attempt simulates 2 seconds of work
//   - Random failure on early attempts (to demonstrate retry)
//   - If all attempts fail, the task is left in Processing state
//
//   In production, you'd use:
//   - Exponential backoff (1s, 2s, 4s, ...)
//   - Jitter (random delay to avoid thundering herd)
//   - Dead-letter queue for permanently failed tasks
//   - Configurable max retries

/// Process a single task with retry logic.
async fn process_task(repo: &impl TaskRepository, task: &Task) {
    let max_retries = 3;
    let task_id = task.id.clone();

    for attempt in 1..=max_retries {
        tracing::info!(task_id = %task_id, attempt = attempt, "Processing task");

        // Mark as Processing
        repo.update_status(&task_id, &TaskStatus::Processing);

        // Simulate work (e.g., transcoding a video, generating a report)
        tokio::time::sleep(std::time::Duration::from_secs(2)).await;

        // Simulate random failure (50% chance on early attempts)
        // fastrand::bool() returns true/false with equal probability
        if attempt < max_retries && fastrand::bool() {
            tracing::warn!(task_id = %task_id, attempt = attempt, "Retrying...");
            tokio::time::sleep(std::time::Duration::from_secs(1)).await;
            continue;
        }

        // Mark as Done
        repo.update_status(&task_id, &TaskStatus::Done);
        tracing::info!(task_id = %task_id, attempt = attempt, "Task completed");
        return;
    }

    // All retries exhausted
    tracing::error!(task_id = %task_id, "Task failed after all retries");
}

/// Listen for TaskCreated events and process them.
///
/// WHY tokio::spawn INSIDE THE LOOP?
///   Each task is processed in its own tokio task. This allows multiple
///   tasks to be processed concurrently. Without this, the worker would
///   process tasks sequentially (blocking on each 2-second sleep).
///
///   Tradeoff: No limit on concurrent tasks. In production, you'd use a
///   semaphore or channel to limit concurrency (e.g., max 10 concurrent).
async fn worker_loop(mut rx: broadcast::Receiver<TaskEvent>, repo: Arc<SqliteRepo>) {
    tracing::info!("Worker started, waiting for tasks...");
    while let Ok(event) = rx.recv().await {
        match event {
            TaskEvent::Created(task) => {
                tracing::info!(task_id = %task.id, "Worker received event");
                let repo = repo.clone();
                tokio::spawn(async move {
                    process_task(&*repo, &task).await;
                });
            }
        }
    }
}

// =============================================================================
// Main — Composition Root
// =============================================================================

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging with env-filter support
    tracing_subscriber::fmt()
        .with_env_filter("taskflow=info")
        .init();

    // -----------------------------------------------------------------------
    // Infrastructure Setup (shared between API and Worker)
    // -----------------------------------------------------------------------

    let db_url = "sqlite:./nextlink.db?mode=rwc";
    let repo = Arc::new(SqliteRepo::new(db_url).await?);
    let event_bus = Arc::new(InMemoryEventBus::new(100));

    // -----------------------------------------------------------------------
    // Start Worker (background task)
    // -----------------------------------------------------------------------
    //
    // The worker subscribes to the SAME event bus as the API service.
    // This is the key difference from running separate binaries — they
    // share the in-memory channel.
    let worker_rx = event_bus.subscribe();
    let worker_repo = repo.clone();
    tokio::spawn(async move {
        worker_loop(worker_rx, worker_repo).await;
    });

    // -----------------------------------------------------------------------
    // Start gRPC Server (with reflection)
    // -----------------------------------------------------------------------

    let grpc = GrpcService { repo, event_bus };

    // gRPC reflection allows grpcurl to discover services at runtime
    let reflection = tonic_reflection::server::Builder::configure()
        .register_encoded_file_descriptor_set(shared::proto::FILE_DESCRIPTOR_SET)
        .build_v1()?;

    let addr = "[::1]:50051".parse()?;
    tracing::info!("TaskFlow API listening on {}", addr);

    tonic::transport::Server::builder()
        .add_service(TaskServiceServer::new(grpc))
        .add_service(reflection)
        .serve(addr)
        .await?;

    Ok(())
}
