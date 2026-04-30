// =============================================================================
// get_task_status.rs — GetTaskStatus Use Case (CQRS Query)
// =============================================================================
//
// CQRS: This is a QUERY (read operation).
//   Queries read state and return it. They have NO side effects:
//   - No events published
//   - No state changes
//   - No validation (beyond existence check)
//
// CONTRAST WITH COMMANDS:
//   Commands (like CreateTask) change state and emit events.
//   Queries (like GetTaskStatus) just read state.
//   Separating them means:
//   - Each has a clear, single responsibility
//   - Queries can be optimized differently (caching, read replicas)
//   - Commands can be validated more strictly
//
// WHY IS THIS A SEPARATE FILE FROM create_task.rs?
//   Single Responsibility Principle. If we need to change how status queries
//   work (e.g., add caching), we only touch this file. If we need to change
//   how task creation works, we only touch create_task.rs.
// =============================================================================

use shared::domain::Task;

// Re-use the TaskRepository trait defined in create_task.rs.
// In a larger project, this would be in its own file or in the domain layer.
use super::create_task::TaskRepository;

/// Use case: get the current status of a task.
///
/// This handler only needs a TaskRepository — it doesn't need an EventBus
/// because queries don't emit events. This is a key CQRS distinction.
pub struct GetTaskStatusHandler<R: TaskRepository> {
    repo: R,
}

impl<R: TaskRepository> GetTaskStatusHandler<R> {
    pub fn new(repo: R) -> Self {
        Self { repo }
    }

    /// Execute the GetTaskStatus query.
    ///
    /// Returns:
    ///   - Some(Task) if the task exists
    ///   - None if the task doesn't exist (caller handles 404)
    ///
    /// WHY RETURN Option<Task> INSTEAD OF A CUSTOM RESPONSE TYPE?
    ///   Returning the domain entity is simpler and more flexible.
    ///   The gRPC handler (infrastructure layer) converts it to the
    ///   protobuf response type. This keeps the application layer
    ///   framework-agnostic.
    pub fn handle(&self, task_id: &str) -> Option<Task> {
        let task = self.repo.find_by_id(task_id)?;

        tracing::info!(
            task_id = %task.id,
            status = %task.status.as_str(),
            "Task status queried"
        );

        Some(task)
    }
}
