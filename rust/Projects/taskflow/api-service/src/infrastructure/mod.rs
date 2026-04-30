// =============================================================================
// infrastructure/mod.rs — Infrastructure Layer Module
// =============================================================================
//
// The Infrastructure layer contains concrete implementations of the
// abstractions defined in the Application and Domain layers.
//
// CLEAN ARCHITECTURE RULES:
//   - Infrastructure depends on Application (implements TaskRepository)
//   - Infrastructure depends on Domain (uses Task, TaskStatus)
//   - Infrastructure does NOT define abstractions (traits)
//
// WHAT GOES HERE:
//   - Database implementations (SQLite, Postgres, in-memory)
//   - External service clients (HTTP, gRPC)
//   - Message queue implementations (Kafka, RabbitMQ)
//   - File system operations
//   - Any I/O or framework-specific code
// =============================================================================

pub mod sqlite_repo;
