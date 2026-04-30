// =============================================================================
// create_task.rs — CreateTask Use Case (CQRS Command)
// =============================================================================
//
// WHAT IS A USE CASE?
//   A use case is a specific business operation that the system can perform.
//   It's the "application logic" — it orchestrates domain objects and
//   infrastructure to accomplish a goal.
//
//   In Clean Architecture, use cases live in the Application layer and:
//   1. Accept input from the outside (gRPC handler calls handle())
//   2. Validate the input (or delegate validation)
//   3. Execute business logic (create a Task entity)
//   4. Persist state (save to repository)
//   5. Publish events (notify other services)
//   6. Return a result
//
// CQRS: This is a COMMAND (write operation).
//   Commands change state and have side effects (events).
//   They are separated from QUERIES (read operations) per CQRS principles.
//   See get_task_status.rs for the query side.
//
// DEPENDENCY INVERSION:
//   This use case depends on:
//   - TaskRepository trait (defined here, implemented in infrastructure)
//   - EventBus trait (defined in shared/events.rs)
//   It does NOT depend on concrete implementations (SQLite, channels).
//   This is the Dependency Inversion Principle (D in SOLID).
// =============================================================================

use shared::domain::{Task, TaskStatus};
use shared::events::{EventBus, TaskEvent};
use uuid::Uuid;

// =============================================================================
// TaskRepository Trait
// =============================================================================
//
// WHY IS THE REPOSITORY TRAIT DEFINED HERE AND NOT IN DOMAIN?
//   In strict Clean Architecture, the repository interface belongs in the
//   domain layer. However, since our domain is very simple (just Task and
//   TaskStatus), defining the trait here keeps things pragmatic.
//
//   In a larger project, you'd define it in the domain layer because:
//   - The domain defines what persistence operations are needed
//   - The infrastructure implements them
//   - The application uses them
//
// WHY Send + Sync?
//   - Send: The repository can be moved between threads (for tokio::spawn)
//   - Sync: The repository can be shared between threads (for Arc)
//   These bounds are needed because we use Arc<impl TaskRepository> everywhere.
pub trait TaskRepository: Send + Sync {
    /// Persist a new task.
    fn save(&self, task: &Task);

    /// Find a task by its ID.
    /// Returns None if the task doesn't exist.
    fn find_by_id(&self, id: &str) -> Option<Task>;

    /// Update a task's status.
    fn update_status(&self, id: &str, status: &TaskStatus);
}

// =============================================================================
// Arc Blanket Implementation
// =============================================================================
//
// Same pattern as EventBus — allows using Arc<SqliteTaskRepository> anywhere
// a TaskRepository is expected. Without this, every function that takes a
// TaskRepository would need to handle Arc separately.
impl<T: TaskRepository> TaskRepository for std::sync::Arc<T> {
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

// =============================================================================
// CreateTaskHandler
// =============================================================================
//
// WHY A STRUCT WITH GENERICS INSTEAD OF A FREE FUNCTION?
//   A struct with generics lets us inject dependencies at construction time.
//   This is called "Dependency Injection" and enables:
//   - Testing with mock repositories
//   - Swapping implementations without changing callers
//   - Clear documentation of what each use case needs
//
// GENERIC PARAMETERS:
//   R: TaskRepository — any type that can persist tasks
//   E: EventBus — any type that can publish events
//   Both are bounded by traits, not concrete types.
pub struct CreateTaskHandler<R: TaskRepository, E: EventBus> {
    repo: R,
    event_bus: E,
}

impl<R: TaskRepository, E: EventBus> CreateTaskHandler<R, E> {
    /// Create a new handler with the given dependencies.
    /// This is called "constructor injection" — dependencies are provided
    /// when the handler is created, not looked up or created internally.
    pub fn new(repo: R, event_bus: E) -> Self {
        Self { repo, event_bus }
    }

    /// Execute the CreateTask use case.
    ///
    /// Steps:
    ///   1. Create a Task entity with a new UUID and status=Pending
    ///   2. Save it to the repository
    ///   3. Publish a TaskCreated event (so the worker can process it)
    ///   4. Return the created task
    ///
    /// WHY RETURN THE TASK INSTEAD OF JUST THE ID?
    ///   The caller (gRPC handler) needs the ID to return to the client.
    ///   Returning the full Task is more flexible and costs nothing.
    pub fn handle(&self, description: String) -> Task {
        // Create the domain entity
        let task = Task {
            id: Uuid::new_v4().to_string(),
            description,
            status: TaskStatus::Pending,
        };

        // Persist (fire-and-forget via tokio::spawn in the SQLite impl)
        self.repo.save(&task);

        // Publish event (non-blocking send to broadcast channel)
        self.event_bus.publish(TaskEvent::Created(task.clone()));

        // Log with structured fields (key=value pairs, not string formatting)
        tracing::info!(task_id = %task.id, "Task created");

        task
    }
}
