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