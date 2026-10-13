# Rust Interview Exercises

Merged, deduplicated catalogue for **senior Rust / backend** interviews. It combines the
prioritised PDF exercises with the 40 challenge sketches from the original `ideas.txt`,
and links to the existing crates in this folder. Everything here is **Rust only**.

**Sources:** *C++ and Rust Coding Interview Exercises* (§1 core, §3 Rust drills, §4 order)
and the original `ideas.txt` (40 senior-scoped Rust challenges).

## How to practise

For each 30–60 minute session:

1. Spend 5 minutes designing the API on paper first.
2. Write clean, idiomatic Rust; let the borrow checker guide the design.
3. Add 2–3 unit tests.
4. Explain the tradeoffs aloud: ownership/borrowing, trait vs enum, sync vs async, error
   modeling, complexity.
5. Explain how you would productionise it.

That mimics senior interviews far better than pure algorithm grinding.

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Practice first — highest signal for senior loops. |
| **P1** | Important next. |
| **P2** | Specialized / advanced. |
| **P3** | Defer unless the target role demands it. |

Times are approximate interview-sized sessions (45–60 min box, including basic testing).
Advanced topics (mini async executor, lock-free queues) deserve separate learning
sessions rather than a forced interview-length limit.

---

## A. Core system exercises

| Priority | Exercise | Scope / senior signal | Time | Existing crate |
|----------|----------|-----------------------|------|----------------|
| P0 | Bounded blocking queue | Blocking push/pop, close, blocked waiters; `Mutex` + `Condvar`, deadlock awareness, backpressure. | 45–60 min | — |
| P0 | Thread pool | `execute` an `FnOnce() + Send + 'static`; worker lifecycle, `mpsc`, graceful shutdown/`Drop`. | 45–60 min | [`mini_thread_pool`](mini_thread_pool) |
| P0 | LRU cache | O(1) average get/put and capacity eviction; `HashMap` + ordering, complexity. | 30–45 min | [`mini_lru`](mini_lru) |
| P0 | TLV binary protocol | Encode/decode type-length-value messages; bounds, endianness, malformed input. | 40–60 min | — |
| P0 | Backup manifest diff | Compare two manifests and report added/deleted/modified; start without filesystem scanning. | 40–60 min | — |
| P1 | Token bucket rate limiter | `try_acquire`, time-based refill, injectable clock, then synchronisation; `Instant` vs `SystemTime`, deterministic testing. | 30–45 min | [`rate_limiter`](rate_limiter) |
| P1 | Circuit breaker | Closed/open/half-open states, failure thresholds, reset timeout. | 40–60 min | — |
| P1 | Length-prefixed TCP framing | Partial reads/writes, malformed frames before a full server. | 45–60 min | — |
| P1 | Retry with backoff and jitter | Bound attempts, classify retryable errors, inject delays, add cancellation; `FnMut` vs `FnOnce`. | 30–45 min | — |
| P1 | TTL key-value store | get/set/delete + expiry with a deterministic clock; add snapshots later. | 40–60 min | [`inmem_kv_store`](inmem_kv_store) |
| P1 | Ring buffer | Fixed capacity, wraparound/overwrite semantics; blocking mode as an extension. | 30–45 min | — |
| P1 | Merge k sorted streams | `BinaryHeap`, custom ordering, empty streams, complexity. | 30–45 min | — |
| P1 | Producer–consumer system | One producer, many consumers; channels, data-race avoidance, graceful shutdown. | 40–60 min | — |
| P1 | Thread-safe counter | `Arc` + `AtomicUsize` vs `Mutex`; contention discussion. | 20–30 min | [`threadsafe_counter`](threadsafe_counter) |
| P1 | Simple logger | Log-level enum, thread-safe, stdout; enum design + trait impls. | 30–45 min | [`simple_logger`](simple_logger) |
| P2 | Consistent hashing ring | Virtual nodes, deterministic placement, node add/remove. | 40–60 min | — |
| P2 | Timer heap / scheduler | Min-heap schedule/cancel/expire; time handling, priority-queue usage. | 45–60 min | — |
| P2 | Event bus / observer | subscribe/unsubscribe/publish; trait bounds, `Arc`, thread safety. | 40–60 min | — |
| P2 | Lock-free SPSC queue | Atomics, memory ordering, `Send`/`Sync`; attempt after the blocking queue. | 60+ min | — |
| P2 | Metrics collector | Counters/gauges/histogram; data modeling, concurrency, API design. | 30–45 min | — |
| P2 | Generic cache with expiration | Keyed `K, V` with TTL; trait bounds; background cleanup thread. | 40–60 min | — |
| P2 | Debouncer | Rapid events → process the last after a delay; threading, timing, channel coordination. | 30–45 min | — |
| P2 | Deduplicator with bounded memory | Stream dedupe within a memory bound; hashing tradeoffs, Bloom-filter discussion. | 30–45 min | — |
| P2 | Safe wrapper around unsafe API | Encapsulate raw-pointer usage; soundness boundary, docs, justify `unsafe`. | 30–45 min | — |
| P2 | Interior-mutability cache | `LazyCache<T>::get_or_init`; `RefCell` vs `Mutex` vs `OnceCell`. | 30–45 min | — |
| P2 | Borrowing text index (lifetimes) | `WordIndex<'a>`; explicit lifetimes, `&str` slicing, zero-copy design. | 40–60 min | — |

## B. Rust language, async & backend drills

| Priority | Exercise | Scope / senior signal | Time | Existing crate / project |
|----------|----------|-----------------------|------|--------------------------|
| P0 | JWT authentication with Axum | Login, token validation, protected endpoint via a JWT crate; request extensions, secret handling, expiration/clock skew. | 45–60 min | [`Projects/jwt-auth`](../Projects/jwt-auth) |
| P0 | CRUD endpoint with Axum | Routing, request validation, shared state (`Arc`), status codes, tests. | 40–60 min | [`simple_router_axum`](simple_router_axum), [`simple_router_actix`](simple_router_actix) |
| P0 | PostgreSQL-backed endpoint | SQLx or the target-job framework; parameterised queries, error mapping. | 45–60 min | [`Projects/rust-rocket-newsletter`](../Projects/rust-rocket-newsletter) |
| P0 | Simple router | Match request path to handler (`GET /users/:id`); pattern matching, routing vs handling separation. | 30–45 min | [`simple_router_axum`](simple_router_axum) |
| P1 | Custom error type and conversions | `Result`, `?`, domain errors, `TryFrom`, mapping errors to HTTP responses. | 30–45 min | [`tryfrom`](tryfrom), [`Refreshers/15_error_handling_strategies.rs`](../Refreshers/15_error_handling_strategies.rs) |
| P1 | Typestate / enum state machine | Model valid transitions (e.g. a backup-job lifecycle). | 30–45 min | — |
| P1 | Parallel file scanner | `rayon`, error aggregation, performance with a small initial scope. | 40–60 min | — |
| P1 | Trait-object plugin system | `dyn Trait`, object safety, ownership, error types. | 40–60 min | — |
| P1 | Async worker pool | Bounded work, shutdown/cancellation, error propagation. | 45–60 min | [`Projects/taskflow`](../Projects/taskflow) |
| P1 | Async job runner (Tokio) | Bounded concurrency via `Semaphore`; `Send` across await points. | 45–60 min | [`Refreshers/21_tokio_deep_dive.rs`](../Refreshers/21_tokio_deep_dive.rs) |
| P1 | Graceful shutdown worker system | Channel-closing semantics, `JoinHandle`, `Drop`, cancellation. | 45–60 min | [`Projects/taskflow`](../Projects/taskflow) |
| P1 | Repository trait with dependency injection | `Arc<dyn UserRepository + Send + Sync>`, mock impl; inversion of control. | 40–60 min | [`Projects/rust-payment-engine`](../Projects/rust-payment-engine) |
| P1 | HTTP client abstraction | `trait HttpClient` + mock; dependency inversion, testability. | 30–45 min | — |
| P1 | Versioned API payload handling | `enum CreateUserRequest { V1, V2 }` → unified domain; enum modeling, backward compatibility. | 40–60 min | — |
| P1 | Expression evaluator | Evaluate `"3 + 4 * 2"`; tokenization vs evaluation, stack modeling, errors. | 45–60 min | — |
| P2 | Iterator adapter with lifetimes | Implement one adapter (`window`/`dedup`), not a whole iterator library. | 30–45 min | [`custom_iter`](custom_iter), [`Refreshers/09_iter_closures.rs`](../Refreshers/09_iter_closures.rs) |
| P2 | Custom iterator implementation | Implement `Iterator` (e.g. `EvenNumbers`); state ownership, lifetimes if borrowing. | 30–45 min | [`custom_iter`](custom_iter) |
| P2 | Zero-copy CSV line parser | `parse_line(&str) -> Result<Vec<&str>, ParseError>`; slicing, lifetimes, malformed input. | 30–45 min | — |
| P2 | Shared-state primitives | Choosing `Rc`/`RefCell` vs `Arc`/`Mutex`; reimplementing std types unnecessary. | 30–45 min | [`Refreshers/07_concurrency.rs`](../Refreshers/07_concurrency.rs) |
| P2 | Small domain-driven module | `Order`/`OrderItem`/status transitions; valid transitions, module boundaries. | 40–60 min | — |
| P2 | Miri / clippy debugging | Diagnose a concrete issue rather than only clearing warnings. | 30–45 min | [`Refreshers/10_tools.rs`](../Refreshers/10_tools.rs) |
| P3 | Mini async executor | Runtime internals; defer unless targeting runtime/infrastructure work. | 60+ min | — |
| P3 | Unsafe SPSC queue | Advanced; sound reasoning about atomics, aliasing, `Send`/`Sync`. | 60+ min | — |

## C. Algorithms & data structures

| Priority | Exercise | Scope / senior signal | Time | Existing crate |
|----------|----------|-----------------------|------|----------------|
| P1 | Streaming median | Two heaps; complexity analysis; ownership modeling. | 30–45 min | [`stream_median`](stream_median) |
| P1 | Generic binary search tree | insert/contains/inorder iterator; `Option<Box<Node<T>>>`, generics with `Ord`. | 45–60 min | [`bin_search_tree`](bin_search_tree) |
| P2 | Graph with BFS and DFS | Adjacency list; borrowing with graph structures, visited tracking. | 30–45 min | — |
| P2 | Top-K frequent elements | `BinaryHeap`, complexity. | 30–45 min | — |
| P2 | Warm-ups: arrays, strings, number theory | two-sum, reverse string, palindrome, prime check, fibonacci, fizzbuzz, max value, vowel counter. | 15–30 min | [`two_sum`](two_sum), [`reverse_string`](reverse_string), [`palindrome_check`](palindrome_check), [`prime_check`](prime_check), [`fibonacci`](fibonacci), [`fizzbuzz`](fizzbuzz), [`max_val`](max_val), [`vowel_counter`](vowel_counter) |

## D. Suggested first pass (Rust)

> **JWT authentication with Axum → CRUD API with Axum → PostgreSQL endpoint → streaming/zero-copy parser → bounded async worker → typestate / backup-job state machine.**

Ordered starting point (six Rust exercises). Time-box each to **45–60 minutes**; keep
advanced topics (mini async executor, lock-free queues) for separate learning sessions.

## E. Follow-ups by target role

| Target role | Recommended follow-ups |
|-------------|------------------------|
| Rust backend | Idempotent endpoint, pagination, middleware, database transactions, resilient HTTP client. |
| Systems / infrastructure | TCP framing, circuit breaker, rate limiter, TTL store, custom allocators. |
| Distributed systems | Consistent hashing, event processing, retries, timer scheduling. |

> **Rust backend gap to cover explicitly:** idempotency, pagination, middleware, database
> transactions, and resilient downstream HTTP clients.

---

## Appendix — API sketches from `ideas.txt`

The original 40 challenge sketches are folded into the tables above (their priorities and
senior signals); they are preserved here as concrete API shapes.

```rust
// --- Core systems ---
// 1. In-Memory Key-Value Store (+ TTL extension)
pub struct KvStore { /* ... */ }
impl KvStore {
    pub fn new() -> Self;
    pub fn set(&mut self, key: String, value: String);
    pub fn get(&self, key: &str) -> Option<&String>;
    pub fn delete(&mut self, key: &str) -> bool;
}
// API clarity; borrowing; &str vs String; testability.

// 2. Thread-Safe Counter Service
impl Counter { pub fn inc(&self); pub fn get(&self) -> usize; }
// Arc; Mutex vs AtomicUsize; contention.

// 3. Mini LRU Cache — get/put, evict least recently used.
// HashMap + ordering structure; complexity.

// 4. Generic Rate Limiter (Token Bucket)
pub struct RateLimiter { /* ... */ }
pub fn allow(&mut self) -> bool;
// Instant vs SystemTime; deterministic testing.

// 6. Simple Logger — level enum, thread-safe, stdout.
// 7. Mini Thread Pool
pub fn execute<F>(&self, job: F) where F: FnOnce() + Send + 'static;
// mpsc channels; worker lifecycle; Drop handling.

// 16. Debouncer — process the last event after a delay.
// 17. Mini Metrics Collector
pub fn record_counter(name: &str, value: u64);
// counter/gauge/histogram; data modeling; concurrency.
// 18. Safe Wrapper Around Unsafe API — safety boundary, docs, justify unsafe.
// 20. Bounded Queue — Mutex + Condvar; deadlock awareness; backpressure.
// 21. Mini Scheduler — priority queue; time handling.
// 25. Lock-Free Stack (Simplified) — AtomicPtr; memory ordering.
// 26. Circuit Breaker — Closed/Open/HalfOpen.
// 27. Simple Event Bus — subscribe/publish; Arc; thread safety.
// 28. Generic Cache with Expiration — keyed K,V with TTL.
// 33. Interior Mutability Cache
pub struct LazyCache<T> { /* ... */ }
impl<T> LazyCache<T> {
    pub fn new() -> Self;
    pub fn get_or_init<F>(&self, f: F) -> &T where F: FnOnce() -> T;
}
// 34. Graceful Shutdown Worker System
pub struct WorkerPool { /* ... */ }
impl WorkerPool {
    pub fn new(size: usize) -> Self;
    pub fn submit(&self, job: Job);
    pub async fn shutdown(self);
}
```

```rust
// --- Domain modeling & errors ---
// 8. TryFrom<&str> for Domain Type
struct Email(String); // validate format; custom error enum; From/TryFrom.
// 19. Generic Retry Mechanism
fn retry<F, T, E>(f: F, attempts: usize) -> Result<T, E>;
// FnMut vs FnOnce; backoff strategy.
// 22. Domain Model with Invariants — struct BankAccount; no negative balance.
// 23. HTTP Client Abstraction
trait HttpClient { fn get(&self, url: &str) -> Result<Response, Error>; }
// 24. Memory-Efficient Deduplicator — hashing tradeoffs; Bloom filter.
// 29. Small Domain-Driven Module — Order / OrderItem / status transitions.
// 30. Refactor a Bad API
fn process(data: Vec<String>) -> Vec<String>;
// smaller traits; error types; better naming; borrowing improvements.
// 39. Repository Trait with Dependency Injection
trait UserRepository { fn find(&self, id: UserId) -> Result<User, RepoError>; }
// 40. Versioned API Payload Handling
enum CreateUserRequest { V1(V1Payload), V2(V2Payload) }
```

```rust
// --- Language, lifetimes & iterators ---
// 5. Generic Binary Search Tree — insert/contains/inorder; Option<Box<Node<T>>>.
// 10. File-Based Config Loader — Result propagation; parsing vs IO separation.
// 11. Custom Iterator Implementation
pub struct EvenNumbers { /* ... */ } // impl Iterator for EvenNumbers
// state ownership; Iterator trait mastery; lifetimes if borrowing.
// 14. Graph with BFS and DFS — adjacency list; borrowing with graphs.
// 15. Plugin System with Traits
trait Plugin { fn name(&self) -> &str; fn execute(&self, input: &str) -> String; }
// store heterogeneous plugins in a Vec<Box<dyn Plugin>>.
// 31. Borrowing-Based Text Index (Lifetimes Focus)
pub struct WordIndex<'a> { text: &'a str, index: HashMap<&'a str, Vec<usize>> }
impl<'a> WordIndex<'a> {
    pub fn new(text: &'a str) -> Self;
    pub fn positions(&self, word: &str) -> Option<&[usize]>;
}
// explicit lifetime annotations; &str slicing without allocation; zero-copy.
// 35. Zero-Copy CSV Line Parser
pub fn parse_line(input: &str) -> Result<Vec<&str>, ParseError>;
```

```rust
// --- Web & async ---
// 12. Simple Router — match request path to handler (GET /users/:id).
// 32. Async Job Runner (Tokio)
pub struct JobRunner { /* ... */ }
impl JobRunner {
    pub fn new(limit: usize) -> Self;
    pub async fn run<F>(&self, job: F)
    where F: Future<Output = Result<(), Error>> + Send + 'static;
}
// Semaphore for concurrency control; Send across await points.
// 36. Minimal Axum REST Service — POST /users, GET /users/:id; JSON bodies, Arc state.
// 37. JWT Authentication Middleware — POST /login, protected route, token extractor.
// 38. Async Rate Limiter Middleware — per-IP limiting, 429 responses, shared async state.
```

```rust
// --- Algorithms ---
// 9. Streaming Median — two-heap solution; complexity; ownership.
// 13. Expression Evaluator — "3 + 4 * 2"; tokenization vs evaluation; error handling.
```
