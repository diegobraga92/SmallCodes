# TaskFlow — Event-Driven Task Processing System

A minimal, production-quality Rust project demonstrating **Clean Architecture**, **CQRS principles**, **event-driven processing**, and **gRPC communication** — designed for senior backend engineering interviews.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Deep Dives & Tradeoffs](#deep-dives--tradeoffs)
   - [Clean Architecture](#1-clean-architecture)
   - [CQRS (Command-Query Responsibility Segregation)](#2-cqrs-command-query-responsibility-segregation)
   - [Event-Driven Processing](#3-event-driven-processing)
   - [gRPC over REST](#4-grpc-over-rest)
   - [Sync Repository Traits](#5-sync-repository-traits)
   - [Combined Binary + Separate Binaries](#6-combined-binary--separate-binaries)
4. [Project Structure](#project-structure)
5. [End-to-End Flow](#end-to-end-flow)
6. [Running the System](#running-the-system)
7. [What Would Change in Production](#what-would-change-in-production)

---

## Overview

TaskFlow is an event-driven task processing system with two services:

- **API Service** — accepts gRPC requests to create and query tasks
- **Worker Service** — asynchronously processes tasks and updates their status

The system demonstrates how to build decoupled, maintainable backend services using Rust's async ecosystem. It's intentionally small in scope but rigorous in its architectural decisions.

### The Problem It Solves

Imagine a system where users submit work (e.g., video transcoding, report generation, data export) that takes seconds or minutes to complete. The system must:

1. Accept the request and return immediately (don't block the client)
2. Process the work asynchronously
3. Allow the client to query progress

This is the canonical **asynchronous task processing** pattern, and TaskFlow implements it end-to-end.

---

## Architecture

```
┌──────────────┐     gRPC      ┌──────────────────┐
│   Client     │◄────────────►│   API Service     │
│  (grpcurl)   │              │  (tonic server)   │
└──────────────┘              └────────┬─────────┘
                                       │
                              publishes │ TaskCreated event
                                       │
                              ┌────────▼─────────┐
                              │   Event Bus       │
                              │ (tokio broadcast) │
                              └────────┬─────────┘
                                       │
                              subscribes │
                                       │
                              ┌────────▼─────────┐
                              │  Worker Service   │
                              │  (async loop)     │
                              └────────┬─────────┘
                                       │
                              reads/writes
                                       │
                              ┌────────▼─────────┐
                              │     SQLite        │
                              │  (shared DB)      │
                              └──────────────────┘
```

### Layer Architecture (Clean Architecture)

```
┌──────────────────────────────────────────────┐
│           Infrastructure Layer                │
│  (gRPC server, SQLite repo, event bus impl)  │
├──────────────────────────────────────────────┤
│           Application Layer                   │
│  (use cases: CreateTask, GetTaskStatus)       │
├──────────────────────────────────────────────┤
│           Domain Layer                        │
│  (Task entity, TaskStatus enum, EventBus)     │
└──────────────────────────────────────────────┘
```

Dependencies point **inward**: Infrastructure depends on Application, which depends on Domain. Domain has zero dependencies on external crates (except serde for serialization).

---

## Deep Dives & Tradeoffs

### 1. Clean Architecture

#### What we did

We split the code into three layers:

- **Domain** (`shared/src/domain.rs`, `shared/src/events.rs`): Pure data types and trait contracts. No external dependencies beyond serde.
- **Application** (`api-service/src/application/`): Use case handlers that orchestrate domain objects. Depends on domain traits, not concrete implementations.
- **Infrastructure** (`api-service/src/infrastructure/`, `api-service/src/main.rs`): Concrete implementations — SQLite repository, gRPC server, event bus.

Dependency inversion is achieved through traits:

```rust
// Domain layer defines the contract
pub trait TaskRepository: Send + Sync {
    fn save(&self, task: &Task);
    fn find_by_id(&self, id: &str) -> Option<Task>;
    fn update_status(&self, id: &str, status: &TaskStatus);
}

// Application layer uses the trait
pub struct CreateTaskHandler<R: TaskRepository, E: EventBus> { ... }

// Infrastructure layer implements the trait
impl TaskRepository for SqliteTaskRepository { ... }
```

#### Why this way

- **Testability**: You can swap SQLite for an in-memory mock by implementing the trait differently. Use cases can be tested without a database.
- **Swapability**: Want to move from SQLite to PostgreSQL? Write a new `PgTaskRepository` implementing the same trait. The application layer never changes.
- **Reasoning**: Each layer has a clear responsibility. When debugging, you know exactly where to look.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| Clear separation of concerns | Boilerplate: traits, impls, Arc blanket impls |
| Easy to test in isolation | For 2 endpoints, this is over-engineered |
| Scales to larger teams | Each new use case requires touching 3 layers |
| Domain logic is framework-agnostic | Extra indirection can make flow harder to follow |

**Honest take**: For a system with only 2 endpoints, Clean Architecture adds significant ceremony with little practical benefit. We include it to **demonstrate the pattern**, not because it's the optimal solution for this scope. In a real project, you'd start simpler and introduce layers as complexity grows.

---

### 2. CQRS (Command-Query Responsibility Segregation)

#### What we did

CQRS separates operations that **change state** (commands) from operations that **read state** (queries). We implement this at the handler level:

- **Command**: `CreateTaskHandler` — creates a task, publishes an event
- **Query**: `GetTaskStatusHandler` — reads task state directly

```rust
// Command — changes state, emits events
pub struct CreateTaskHandler<R: TaskRepository, E: EventBus> {
    fn handle(&self, description: String) -> Task {
        // 1. Create task
        // 2. Save to repo
        // 3. Publish event
    }
}

// Query — reads state, no side effects
pub struct GetTaskStatusHandler<R: TaskRepository> {
    fn handle(&self, task_id: &str) -> Option<Task> {
        // 1. Read from repo
        // 2. Return result
    }
}
```

#### Why this way

- **Clarity**: Commands and queries have different constraints. Commands can fail validation; queries return data or 404.
- **Separation**: The command path triggers side effects (events, worker processing). The query path is a simple read.
- **Interview signal**: Demonstrates understanding of CQRS without overcomplicating the implementation.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| Clear separation of read/write paths | True CQRS uses separate read/write stores |
| Commands can evolve independently | Adds handler boilerplate |
| Natural fit for event-driven systems | Overkill when reads/writes share the same model |

**Honest take**: True CQRS means separate read and write databases (e.g., write to Postgres, read from Elasticsearch). We only separate **at the handler level** — both handlers read/write the same SQLite database. This is "CQRS-lite" and we're transparent about it. In an interview, acknowledge this simplification and discuss when you'd introduce a separate read store (high read volume, different query patterns).

---

### 3. Event-Driven Processing

#### What we did

When a task is created, the API service publishes a `TaskCreated` event to an in-memory event bus. The worker subscribes to this bus and processes tasks asynchronously.

```rust
// Event definition
pub enum TaskEvent {
    Created(Task),
}

// Event bus trait
pub trait EventBus: Send + Sync {
    fn publish(&self, event: TaskEvent);
    fn subscribe(&self) -> broadcast::Receiver<TaskEvent>;
}

// In-memory implementation using tokio broadcast
pub struct InMemoryEventBus {
    tx: broadcast::Sender<TaskEvent>,
}
```

The worker runs in a separate tokio task, listening for events:

```rust
async fn worker_loop(mut rx: broadcast::Receiver<TaskEvent>, repo: Arc<SqliteRepo>) {
    while let Ok(event) = rx.recv().await {
        match event {
            TaskEvent::Created(task) => {
                tokio::spawn(async move {
                    process_task(&*repo, &task).await;
                });
            }
        }
    }
}
```

#### Why this way

- **Decoupling**: The API service doesn't wait for processing to complete. It returns immediately after storing the task.
- **Async processing**: The worker can retry, throttle, or prioritize tasks independently.
- **Resilience**: If the worker crashes, tasks remain in the database with status `Pending`. A startup recovery scan can pick them up.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| Zero infrastructure (no Kafka/RabbitMQ) | No persistence — events lost on restart |
| Low latency (in-process channel) | No replay capability |
| Simple to understand and debug | No consumer groups (single consumer) |
| No network overhead | Cannot scale workers independently |

**Honest take**: The in-memory event bus is the biggest simplification in this project. In production, you'd use Kafka, RabbitMQ, or NATS for:

- **Persistence**: Events survive crashes
- **Replay**: Re-process failed events
- **Consumer groups**: Multiple workers can process in parallel
- **Backpressure**: Slow consumers don't block producers

We use a channel because it keeps the project runnable with `cargo run` and zero external dependencies. The `EventBus` trait makes swapping to a real message broker straightforward.

---

### 4. gRPC over REST

#### What we did

We use **gRPC** (via the Tonic framework) instead of REST/HTTP for service communication.

```protobuf
service TaskService {
  rpc CreateTask(CreateTaskRequest) returns (CreateTaskResponse);
  rpc GetTaskStatus(GetTaskStatusRequest) returns (GetTaskStatusResponse);
}
```

#### Why this way

- **Strong typing**: The `.proto` file defines the contract. Both client and server generate code from it — mismatches are caught at compile time.
- **Code generation**: Tonic + prost generate all serialization/deserialization code. No manual JSON parsing.
- **Performance**: gRPC uses HTTP/2 and binary encoding (protobuf), which is faster than JSON over HTTP/1.1.
- **Reflection**: gRPC reflection allows tools like `grpcurl` to discover services at runtime — no need for a separate API docs endpoint.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| Compile-time type safety | Tooling is less mature than REST |
| Binary encoding (smaller, faster) | Harder to debug (need `grpcurl` instead of `curl`) |
| Built-in streaming support | Browser support is limited |
| Strong contract enforcement | Schema evolution requires care |

**Honest take**: For a 2-endpoint system, REST would be simpler and more practical. We choose gRPC because:

1. It's a common interview topic
2. It demonstrates knowledge of protobuf and code generation
3. It's increasingly used in microservices

In an interview, be ready to discuss when you'd choose gRPC vs REST: gRPC for internal service-to-service communication, REST for public-facing APIs and browser clients.

---

### 5. Sync Repository Traits

#### What we did

The `TaskRepository` trait uses synchronous methods, even though the underlying SQLite operations are async:

```rust
pub trait TaskRepository: Send + Sync {
    fn save(&self, task: &Task);
    fn find_by_id(&self, id: &str) -> Option<Task>;
    fn update_status(&self, id: &str, status: &TaskStatus);
}
```

The SQLite implementation bridges the sync/async gap using `block_in_place` + `block_on`:

```rust
fn find_by_id(&self, id: &str) -> Option<Task> {
    tokio::task::block_in_place(|| {
        let rt = tokio::runtime::Handle::current();
        rt.block_on(async { /* sqlx query */ })
    })
}
```

#### Why this way

- **Simpler trait bounds**: Sync traits don't require `#[async_trait]` or `Pin<Box<dyn Future>>`.
- **Easier to implement**: The `Arc<T>` blanket impl is straightforward.
- **SQLite is fast**: SQLite queries complete in microseconds, so blocking is negligible.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| No `async_trait` dependency | Blocks tokio worker threads |
| Simpler trait signatures | Doesn't work with network databases (Postgres, MySQL) |
| Easier to mock in tests | `block_in_place` is a code smell |

**Honest take**: This is a deliberate simplification. In production, you'd use `async_trait` or the upcoming native async traits in Rust. The sync approach works for SQLite because queries are fast, but it would be a problem with a remote database where queries take milliseconds. If this were a real system, we'd make the trait async.

---

### 6. Combined Binary + Separate Binaries

#### What we did

We provide **two ways to run** the system:

1. **Combined binary** (`cargo run --bin taskflow`): Runs API + Worker in a single process, sharing the event bus via an in-memory channel.
2. **Separate binaries** (`cargo run -p api-service`, `cargo run -p worker-service`): Run as independent processes, each with their own event bus.

#### Why this way

- **Combined binary**: Perfect for local development and demos. One command starts everything. The shared event bus means events flow instantly.
- **Separate binaries**: Demonstrates the architecture's potential for distributed deployment. In production, these would be separate services communicating via Kafka.

#### Tradeoffs

| Pro | Con |
|-----|-----|
| Combined: one command to run everything | Combined: single point of failure |
| Separate: demonstrates distributed architecture | Separate: worker has no event source (creates its own bus) |
| Both: shows architectural flexibility | Code duplication between combined binary and crate modules |

**Honest take**: The separate binaries are somewhat artificial — the worker creates its own event bus and never receives events from the API. In a real distributed system, both would connect to the same message broker. The combined binary is the practical way to run this project.

---

## Project Structure

```
taskflow/
├── Cargo.toml                  # Workspace definition
├── README.md                   # This file
├── proto/
│   └── task.proto              # gRPC service definition
├── shared/                     # Shared domain + generated code
│   ├── Cargo.toml
│   ├── build.rs                # tonic-build code generation
│   └── src/
│       ├── lib.rs              # Re-exports domain, events, proto
│       ├── domain.rs           # Task entity, TaskStatus enum
│       └── events.rs           # TaskEvent, EventBus trait, InMemoryEventBus
├── api-service/                # API service crate
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs             # Standalone API binary
│       ├── bin/
│       │   └── taskflow.rs     # Combined API + Worker binary
│       ├── application/
│       │   ├── mod.rs
│       │   ├── create_task.rs  # CreateTask use case + TaskRepository trait
│       │   └── get_task_status.rs  # GetTaskStatus use case
│       └── infrastructure/
│           ├── mod.rs
│           └── sqlite_repo.rs  # SQLite TaskRepository implementation
└── worker-service/             # Worker service crate
    ├── Cargo.toml
    └── src/
        └── main.rs             # Standalone worker binary
```

### File-by-file rationale

| File | Purpose | Why it exists |
|------|---------|---------------|
| `proto/task.proto` | Service contract | Single source of truth for API surface |
| `shared/build.rs` | Code generation | Compiles `.proto` to Rust at build time |
| `shared/src/domain.rs` | Core entities | Zero-dependency business logic |
| `shared/src/events.rs` | Event system | Decouples producers from consumers |
| `api-service/src/application/create_task.rs` | Use case | Orchestrates domain + infrastructure |
| `api-service/src/infrastructure/sqlite_repo.rs` | Persistence | Concrete DB implementation |
| `api-service/src/bin/taskflow.rs` | Combined binary | Local development convenience |
| `worker-service/src/main.rs` | Worker | Async processing with retry logic |

---

## End-to-End Flow

Here's exactly what happens when a client calls `CreateTask`:

```
Client                    API Service              Event Bus              Worker                 SQLite
  │                          │                       │                      │                      │
  │── CreateTask("hello")───►│                       │                      │                      │
  │                          │── validate input      │                      │                      │
  │                          │── create Task(id,     │                      │                      │
  │                          │   status=Pending)     │                      │                      │
  │                          │── save task ──────────┼──────────────────────┼─────────────────────►│
  │                          │                       │                      │                      │
  │                          │── publish event ─────►│                      │                      │
  │                          │                       │                      │                      │
  │◄───── { task_id } ───────│                       │                      │                      │
  │                          │                       │── deliver event ────►│                      │
  │                          │                       │                      │                      │
  │                          │                       │                      │── update status ─────►│
  │                          │                       │                      │   → Processing        │
  │                          │                       │                      │                      │
  │                          │                       │                      │── sleep(2s)           │
  │                          │                       │                      │                      │
  │                          │                       │                      │── update status ─────►│
  │                          │                       │                      │   → Done              │
  │                          │                       │                      │                      │
  │── GetTaskStatus(id)─────►│                       │                      │                      │
  │                          │── query task ─────────┼──────────────────────┼─────────────────────►│
  │◄──── { status: Done } ───│                       │                      │                      │
```

### Status Lifecycle

```
Pending ──► Processing ──► Done
                │
                ▼
            (retry × 3)
                │
                ▼
             Failed
```

---

## Running the System

### Prerequisites

- Rust (stable) — install via [rustup](https://rustup.rs/)
- `grpcurl` — for testing gRPC endpoints

```bash
# Install grpcurl
curl -sSL https://github.com/fullstorydev/grpcurl/releases/download/v1.9.1/grpcurl_1.9.1_linux_amd64.tar.gz | tar xz
sudo mv grpcurl /usr/local/bin/
```

### Build

```bash
cd /home/diego/dev/SmallCodes/rust/Projects/taskflow
cargo build
```

### Run (Combined — recommended for demo)

```bash
# Start both API and Worker in one process
cargo run --bin taskflow
```

### Run (Separate — for distributed demo)

```bash
# Terminal 1: API service
cargo run -p api-service

# Terminal 2: Worker service
cargo run -p worker-service
```

### Test with grpcurl

```bash
# 1. Create a task
grpcurl -plaintext -d '{"description": "Hello TaskFlow!"}' [::1]:50051 task.TaskService/CreateTask

# Expected output:
# {
#   "taskId": "a1b2c3d4-..."
# }

# 2. Query task status (use the taskId from step 1)
grpcurl -plaintext -d '{"taskId": "a1b2c3d4-..."}' [::1]:50051 task.TaskService/GetTaskStatus

# Expected output (after worker processes it):
# {
#   "taskId": "a1b2c3d4-...",
#   "status": "Done",
#   "description": "Hello TaskFlow!"
# }
```

### Using gRPC Reflection

The server has gRPC reflection enabled, so you can discover services dynamically:

```bash
# List all services
grpcurl -plaintext [::1]:50051 list

# Describe the TaskService
grpcurl -plaintext [::1]:50051 describe task.TaskService
```

---

## What Would Change in Production

This project makes deliberate simplifications to keep it runnable locally. Here's what would change in a production system:

### 1. Message Broker (Kafka / RabbitMQ / NATS)

**Current**: In-memory tokio broadcast channel. Events are lost on restart.

**Production**: A persistent message broker with:
- At-least-once delivery guarantees
- Consumer groups for horizontal scaling
- Dead-letter queues for failed messages
- Message replay for recovery

### 2. Database

**Current**: SQLite (single-file, no concurrency).

**Production**: PostgreSQL or MySQL with:
- Connection pooling (bb8, deadpool)
- Migration tooling (sqlx migrate, diesel)
- Read replicas for query scaling
- Write-ahead logging for durability

### 3. Async Repository Traits

**Current**: Sync traits with `block_in_place` hack.

**Production**: Async traits using `#[async_trait]` or native async traits, allowing non-blocking I/O for database queries.

### 4. Observability

**Current**: Structured logging with `tracing`.

**Production**: Add:
- Distributed tracing (OpenTelemetry)
- Metrics (Prometheus + Grafana)
- Health check endpoints
- Structured error types (thiserror, anyhow)

### 5. Configuration

**Current**: Hardcoded values (port, database URL).

**Production**: Environment-based configuration with:
- Environment variables
- Config files (TOML/YAML)
- Secrets management

### 6. Error Handling

**Current**: `expect()` panics in background tasks.

**Production**: Graceful error handling with:
- Retry with exponential backoff
- Circuit breakers
- Graceful shutdown
- Error reporting (Sentry, Datadog)

### 7. Testing

**Current**: Manual testing with `grpcurl`.

**Production**: Add:
- Unit tests for domain logic
- Integration tests with testcontainers
- Property-based testing (proptest)
- Load testing (k6, locust)

---

## License

This project is for educational purposes. Free to use, modify, and share.
