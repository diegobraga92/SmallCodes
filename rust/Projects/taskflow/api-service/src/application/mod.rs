// =============================================================================
// application/mod.rs — Application Layer Module
// =============================================================================
//
// The Application layer contains "use cases" — specific business operations
// that orchestrate domain objects and infrastructure.
//
// CLEAN ARCHITECTURE RULES:
//   - Application layer depends on Domain layer (traits, entities)
//   - Application layer does NOT depend on Infrastructure layer
//   - Dependencies are injected via constructor (Dependency Injection)
//
// Each use case is a single file with a single responsibility:
//   - create_task.rs: Handle CreateTask command
//   - get_task_status.rs: Handle GetTaskStatus query
//
// WHY SEPARATE USE CASES INTO DIFFERENT FILES?
//   - Single Responsibility Principle: each file has one reason to change
//   - Testability: each use case can be tested in isolation
//   - Readability: you can understand the full flow without scrolling
// =============================================================================

pub mod create_task;
pub mod get_task_status;
