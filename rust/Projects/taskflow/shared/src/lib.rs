// =============================================================================
// shared/src/lib.rs — Crate Root
// =============================================================================
//
// This is the entry point for the `shared` crate. It re-exports the modules
// that both api-service and worker-service need.
//
// MODULE ORGANIZATION:
//   - domain: Pure business logic (Task, TaskStatus) — zero external deps
//   - events: Event system (EventBus trait, InMemoryEventBus)
//   - proto: Generated gRPC code (included at compile time via tonic)
//
// WHY NOT PUT EVERYTHING IN ONE FILE?
//   Separation of concerns. Domain types don't need to know about events.
//   Events don't need to know about gRPC. Each module has a single
//   responsibility and can be understood in isolation.
// =============================================================================

/// Domain layer — core business entities and rules.
/// This is the innermost layer of Clean Architecture.
pub mod domain;

/// Event system — defines how services communicate asynchronously.
/// This is part of the domain layer (the EventBus trait is a contract),
/// but separated because it's a cross-cutting concern.
pub mod events;

/// Generated gRPC code from proto/task.proto.
/// This is infrastructure — it's generated code that changes when the
/// .proto file changes. We keep it in a separate module to isolate
/// generated code from hand-written code.
pub mod proto {
    // tonic::include_proto! is a macro that includes the Rust code generated
    // by tonic-build at compile time. The argument "task" matches the
    // `package = "task"` in our .proto file.
    //
    // This generates:
    //   - pub mod task { ... } containing all message types and service stubs
    //   - task_service_server::TaskService (the trait we implement)
    //   - task_service_server::TaskServiceServer (the tonic server wrapper)
    //   - task_service_client::TaskServiceClient (for gRPC clients)
    tonic::include_proto!("task");

    /// File descriptor set for gRPC reflection.
    /// This is a binary blob that describes our .proto schema. It's embedded
    /// into the binary at compile time and served by the gRPC reflection API.
    /// Tools like grpcurl use this to discover services without needing the
    /// .proto file.
    ///
    /// The "task_descriptor" string matches the file name we configured in
    /// build.rs (task_descriptor.bin).
    pub const FILE_DESCRIPTOR_SET: &[u8] = tonic::include_file_descriptor_set!("task_descriptor");
}
