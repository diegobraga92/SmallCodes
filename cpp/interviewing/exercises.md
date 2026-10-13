# C++ Interview Exercises

Merged, deduplicated catalogue for **senior C++ / systems / backend** interviews. It
combines the prioritised PDF exercises with the 30 challenge sketches from the original
`ideas.txt`. Everything here is **C++ only**.

**Sources:** *C++ and Rust Coding Interview Exercises* (§1 core, §2 C++ drills, §4 order)
and the original `ideas.txt` (30 senior-scoped C++ challenges).

## How to practise

For each 30–60 minute session:

1. Spend 5 minutes designing the API on paper first.
2. Write clean, modern C++ (C++17 minimum; reach for C++20/23 where relevant).
3. Add minimal tests (or a test `main`).
4. Explain the tradeoffs aloud: why this container, why this synchronisation, which
   exception-safety guarantee, what the complexity is.
5. Explain how you would productionise it.

That last step is what separates senior from mid-level candidates.

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Practice first — highest signal for senior loops. |
| **P1** | Important next. |
| **P2** | Specialized / advanced. |
| **P3** | Defer unless the target role demands it. |

Times are approximate interview-sized sessions (45–60 min box, including basic testing).
Advanced topics (lock-free queues, custom async executors) deserve separate learning
sessions rather than a forced interview-length limit.

---

## A. Core system exercises

| Priority | Exercise | Scope / senior signal | Time | Existing C++ code |
|----------|----------|-----------------------|------|-------------------|
| P0 | Bounded blocking queue | Blocking push/pop, close, blocked waiters; move-only values; `std::condition_variable`, spurious wakeups. | 45–60 min | [`31_advanced_concurrency.cpp`](../Refreshers/31_advanced_concurrency.cpp) |
| P0 | Thread pool | Submit tasks, return results, propagate errors, shut down gracefully; condition variables, work stealing only as discussion. | 45–60 min | [`thread_pool.cpp`](../Examples/thread_pool.cpp), [`14_threads.cpp`](../Refreshers/14_threads.cpp) |
| P0 | LRU cache | O(1) average get/put and capacity eviction; `unordered_map` + `list`, iterator stability, move semantics. | 30–45 min | [`08_containers.cpp`](../Refreshers/08_containers.cpp) |
| P0 | TLV binary protocol | Encode/decode type-length-value messages; validate bounds, endianness, malformed input. | 40–60 min | [`bin_parser.cpp`](../Examples/bin_parser.cpp), [`packet_receiver.cpp`](../Examples/packet_receiver.cpp) |
| P0 | Backup manifest diff | Compare two manifests and report added/deleted/modified; start without filesystem scanning. | 40–60 min | — |
| P1 | Token bucket rate limiter | `try_acquire`, time-based refill, injectable clock, then synchronisation; `std::chrono` precision. | 30–45 min | — |
| P1 | Circuit breaker | Closed/open/half-open states, failure thresholds, reset timeout; enum vs class hierarchy. | 40–60 min | [`26_design_patterns.cpp`](../Refreshers/26_design_patterns.cpp) |
| P1 | Length-prefixed TCP framing | Handle partial reads/writes and malformed frames before a full server. | 45–60 min | [`22_network_ipc.cpp`](../Refreshers/22_network_ipc.cpp) |
| P1 | Retry with backoff and jitter | Bound attempts, classify retryable errors, inject delays, add cancellation; perfect forwarding, `noexcept`. | 30–45 min | — |
| P1 | TTL key-value store | get/set/delete + expiry with a deterministic clock; add snapshots later; `string` vs `string_view`. | 40–60 min | [`08_containers.cpp`](../Refreshers/08_containers.cpp) |
| P1 | Ring buffer | Fixed capacity, wraparound/overwrite semantics; blocking mode as an extension. | 30–45 min | [`circ_buffer.cpp`](../Examples/circ_buffer.cpp) |
| P1 | Merge k sorted streams | Priority queue, custom ordering, empty streams, complexity. | 30–45 min | — |
| P1 | Producer–consumer system | One producer, many consumers; data-race avoidance, graceful shutdown. | 40–60 min | [`thread_queue.cpp`](../Examples/thread_queue.cpp), [`request_queue.cpp`](../Examples/request_queue.cpp) |
| P1 | Thread-safe counter | `std::mutex` vs `std::atomic<size_t>`; false sharing, memory-ordering basics. | 20–30 min | [`31_advanced_concurrency.cpp`](../Refreshers/31_advanced_concurrency.cpp) |
| P2 | Consistent hashing ring | Virtual nodes, deterministic key placement, node add/remove. | 40–60 min | — |
| P2 | Timer heap / timer wheel | Min-heap schedule/cancel/expire first; defer a full timer wheel. | 45–60 min | — |
| P2 | Event bus / observer | subscribe/unsubscribe/publish; callback lifetime, `weak_ptr`, reentrancy. | 40–60 min | [`observer.cpp`](../Examples/observer.cpp), [`event_dispatcher.cpp`](../Examples/event_dispatcher.cpp) |
| P2 | Lock-free SPSC queue | Atomics + memory ordering; attempt only after the blocking queue. | 60+ min | [`31_advanced_concurrency.cpp`](../Refreshers/31_advanced_concurrency.cpp) |
| P2 | Metrics collector | Counters/gauges; thread safety, API ergonomics, lock granularity. | 30–45 min | — |
| P2 | Memory pool / arena allocator | Fixed-size blocks; fragmentation, custom allocator interface, alignment. | 40–60 min | [`33_allocators_memory.cpp`](../Refreshers/33_allocators_memory.cpp) |
| P2 | Deduplicator with bounded memory | Stream strings, dedupe within a memory bound; Bloom-filter discussion, false positives. | 30–45 min | — |
| P2 | Domain model with invariants | e.g. `BankAccount` (no negative balance, immutable ID); private ctors, factory methods. | 30–45 min | [`16_classes.cpp`](../Refreshers/16_classes.cpp), [`17_advanced_oop.cpp`](../Refreshers/17_advanced_oop.cpp) |
| P2 | Refactor a bad API | Turn `vector<string> process(vector<string>)` into clear ownership, naming, error modeling. | 30–45 min | [`18_solid.cpp`](../Refreshers/18_solid.cpp) |

> **Note:** *Backup manifest diff* is P0 because it matches relevant experience, not
> because it is a common interview question.

## B. C++ language & tooling drills

| Priority | Exercise | Scope / senior signal | Time | Existing C++ code |
|----------|----------|-----------------------|------|-------------------|
| P0 | RAII file descriptor / socket wrapper | Ownership, move construction/assignment, invalid-handle handling; acquisition in ctor, exception safety. | 30–45 min | [`13_smart_pointers.cpp`](../Refreshers/13_smart_pointers.cpp), [`ffi_raii_inference_handle.cpp`](../Examples/ffi_raii_inference_handle.cpp) |
| P1 | `std::vector`-like dynamic array | size/capacity/reserve/push_back; exception safety; inline storage (SmallVector) discussion. | 45–60 min | [`generic_container.cpp`](../Examples/generic_container.cpp) |
| P1 | Move semantics / Rule of Five | Fix copy/move/dtor, test self-assignment and moved-from; value categories, copy elision. | 30–45 min | [`09_move_and_copyelision.cpp`](../Refreshers/09_move_and_copyelision.cpp), [`07_value_categories.cpp`](../Refreshers/07_value_categories.cpp) |
| P1 | Sanitizer debugging | Diagnose a small use-after-free, data race, or UB issue (ASan/TSan/UBSan). | 30–45 min | [`25_testing.cpp`](../Refreshers/25_testing.cpp), [`27_perf_optimization.cpp`](../Refreshers/27_perf_optimization.cpp) |
| P2 | Type-erasure wrapper (mini `std::function`) | Type erasure + virtual dispatch; heap-allocation tradeoffs; small-buffer optimisation optional. | 45–60 min | [`23_advanced_templates.cpp`](../Refreshers/23_advanced_templates.cpp) |
| P2 | SFINAE / concepts | Constraints and overload selection; implement a small exercise if role-relevant. | 40–60 min | [`template_sfinae.cpp`](../Examples/template_sfinae.cpp), [`34_type_traits_metaprogramming.cpp`](../Refreshers/34_type_traits_metaprogramming.cpp) |
| P2 | Custom STL-compatible iterator | Iterator traits, categories, STL compatibility. | 30–45 min | [`file_int_iter.cpp`](../Examples/file_int_iter.cpp) |
| P2 | Scope guard | Run a function on scope exit; lambda capture, move-only callable, `noexcept` destructor. | 30–45 min | — |
| P2 | Safe division API | `std::expected<double, Error>` (C++23) or `std::optional`; exception vs value-based errors. | 30–45 min | [`24_exceptions.cpp`](../Refreshers/24_exceptions.cpp) |
| P2 | Config loader | Parse a simple config file into a struct; exception boundaries, validation vs parsing. | 30–45 min | [`12_modern_utilities.cpp`](../Refreshers/12_modern_utilities.cpp) |
| P2 | Plugin system with interfaces | `virtual` interface, ownership of plugin instances, factory discussion. | 40–60 min | [`17_advanced_oop.cpp`](../Refreshers/17_advanced_oop.cpp), [`factory.cpp`](../Examples/factory.cpp) |
| P2 | Expression evaluator | Parse `"3 + 4 * 2"`; separate parsing/evaluation, `std::variant` tokens, error strategy. | 45–60 min | — |
| P3 | Minimal `unique_ptr` / `shared_ptr` | Ownership + control blocks; reimplementation usually low priority. | 45–60 min | [`13_smart_pointers.cpp`](../Refreshers/13_smart_pointers.cpp) |
| P3 | C++20 coroutine mini-task | Specialized; defer unless target roles emphasise coroutines/async runtimes. | 60+ min | [`15_async.cpp`](../Refreshers/15_async.cpp) |

## C. Algorithms & data structures (senior-scoped)

| Priority | Exercise | Scope / senior signal | Time | Existing C++ code |
|----------|----------|-----------------------|------|-------------------|
| P1 | Streaming median | Two heaps, complexity tradeoffs, `priority_queue`. | 30–45 min | — |
| P1 | Top-K frequent elements | Heap vs `partial_sort`, complexity. | 30–45 min | — |
| P2 | Generic binary search (iterator-based) | Iterator categories, random-access vs forward constraints. | 30–45 min | — |
| P2 | Flatten nested vector | `reserve` optimisation, move semantics, cache locality. | 30–45 min | — |

## D. Suggested first pass (C++)

> **Bounded queue → LRU cache → TLV parser → RAII wrapper → thread pool → sanitizer debugging.**

Ordered starting point (six C++ exercises). Time-box each to **45–60 minutes**; keep
advanced topics (lock-free queues, custom async executors) for separate learning sessions.

## E. Follow-ups by target role

| Target role | Recommended follow-ups |
|-------------|------------------------|
| Systems / infrastructure | TCP framing, circuit breaker, rate limiter, TTL store, allocators. |
| Low-level C++ | Dynamic array, type erasure, atomic SPSC queue, memory/concurrency debugging. |
| Distributed systems | Consistent hashing, event processing, retries, timer scheduling. |

---

## Appendix — API sketches from `ideas.txt`

The original 30 challenge sketches are folded into the tables above (their priorities and
senior signals); they are preserved here as concrete API shapes.

### Core system sketches

```cpp
// 1. In-Memory Key-Value Store
class KvStore {
public:
    void set(std::string key, std::string value);
    std::optional<std::string> get(std::string_view key) const;
    bool erase(std::string_view key);
};
// std::string vs std::string_view; const correctness; complexity. Extension: TTL.

// 2. Thread-Safe Counter
class Counter { public: void increment(); size_t value() const; };
// std::mutex vs std::atomic<size_t>; false sharing; memory ordering.

// 3. LRU Cache  — get(key)/put(key,value), fixed capacity.
// unordered_map + list; iterator stability; O(1); move semantics.

// 4. Token Bucket Rate Limiter  — allow() respects the rate limit.
// std::chrono; time precision; thread safety.

// 5. Thread Pool
class ThreadPool {
public:
    explicit ThreadPool(size_t n);
    ~ThreadPool();
    template<class F> void enqueue(F&& task);
};
// condition variables; graceful shutdown; exception propagation; work stealing.
```

### Value semantics & RAII

```cpp
// 6. Small Smart Pointer — minimal unique_ptr-like type.
// Rule of 5; move ctor/assignment; deleted copy; ownership modeling.

// 7. RAII File Wrapper — wrap FILE* or a file descriptor.
// Resource acquisition in ctor; destructor correctness; exception safety.

// 8. Scope Guard — execute a function on destruction.
// Lambda capture; move-only callable; noexcept destructor.
```

### Algorithmic but senior-scoped

```cpp
// 9. Streaming Median — maintain the median as numbers arrive.
// Two heaps; complexity tradeoffs; priority_queue.

// 10. Top-K Frequent Elements — heap vs partial_sort; complexity.

// 11. Generic Binary Search
template<typename It, typename T>
It binary_search(It begin, It end, const T& value);
// Iterator categories; random access vs forward constraints.

// 12. Flatten Nested Vector — vector<vector<int>> -> vector<int>.
// reserve optimisation; move semantics; cache locality.
```

### Design & abstraction

```cpp
// 13. Plugin System with Interfaces
struct Plugin {
    virtual ~Plugin() = default;
    virtual std::string name() const = 0;
    virtual void execute() = 0;
};
// Virtual destructors; ownership of instances; factory pattern.

// 14. Expression Evaluator — parse "3 + 4 * 2".
// Separate parsing/evaluation; error strategy; std::variant tokens.

// 15. State Machine (Circuit Breaker) — Closed / Open / HalfOpen.
// Enum vs class hierarchy; time-based transitions; thread safety.
```

### Error handling & safety

```cpp
// 16. Safe Division API
std::expected<double, Error> divide(double a, double b);
// std::expected (C++23) or std::optional; exception vs value-based errors.

// 17. Config Loader — parse a simple config file into a struct.
// Exception boundaries; validation vs parsing separation.

// 18. Retry Utility
template<typename F>
auto retry(F&& f, int attempts);
// Perfect forwarding; noexcept correctness; backoff.
```

### Concurrency & synchronisation

```cpp
// 19. Bounded Blocking Queue — push() / pop().
// condition_variable; spurious wakeups; shutdown signaling.

// 20. Producer-Consumer System — one producer, multiple consumers.
// Data-race avoidance; graceful shutdown; performance tradeoffs.

// 21. Lock-Free Stack (Simplified) — std::atomic<Node*>.
// ABA problem; memory ordering; why production code is hard.
```

### Modern C++ mastery

```cpp
// 22. Custom Iterator — iterator for a custom container.
// Iterator traits; STL compatibility.

// 23. Small Vector — like llvm::SmallVector.
// Inline storage; alignment; move semantics.

// 24. Type-Erased Callable (mini std::function).
// Type erasure; virtual dispatch; heap-allocation tradeoffs.
```

### Systems thinking in miniature

```cpp
// 25. Metrics Collector — counters, gauges.
// Thread safety; API ergonomics; lock granularity.

// 26. Event Bus — subscribe/publish.
// Observer pattern; lifetime management; weak_ptr.

// 27. Memory Pool Allocator — allocate fixed-size blocks.
// Fragmentation; custom allocator interface.

// 28. Deduplicator with Bounded Memory — stream strings, deduplicate.
// Bloom filter; false positives.

// 29. Domain Model with Invariants — e.g. BankAccount.
// Private constructors; factory methods; invariant enforcement.

// 30. Refactor a Bad API
std::vector<std::string> process(std::vector<std::string> data);
// Clear ownership; better naming; composable functions; error modeling;
// value vs reference correctness; exception safety.
```
