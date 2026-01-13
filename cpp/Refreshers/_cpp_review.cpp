// ============================================================
// C++ Review File – Ownership, Concurrency, Performance
// Build:
//   g++ -std=c++20 -O2 review.cpp -pthread -o review
// ============================================================

#include <iostream>
#include <memory>
#include <vector>
#include <thread>
#include <mutex>
#include <future>
#include <chrono>
#include <atomic>

// ============================================================
// 6a - Smart Pointers, RAII, Move Semantics,
//      Stack vs Heap, Object Lifetime
// ============================================================

// RAII: Resource Acquisition Is Initialization
// Constructor acquires resource, destructor releases it
class FileRAII {
public:
    FileRAII() {
        std::cout << "Resource acquired\n";
    }

    ~FileRAII() {
        std::cout << "Resource released\n";
    }

    // Disable copy
    FileRAII(const FileRAII&) = delete;
    FileRAII& operator=(const FileRAII&) = delete;

    // Enable move
    FileRAII(FileRAII&&) noexcept {
        std::cout << "Resource moved\n";
    }
};

void smart_pointers_and_lifetime() {
    // Stack allocation (automatic lifetime)
    FileRAII stack_obj;

    // Heap allocation with unique ownership
    std::unique_ptr<FileRAII> unique = std::make_unique<FileRAII>();

    // Transfer ownership (move semantics)
    std::unique_ptr<FileRAII> moved = std::move(unique);

    // Shared ownership (reference counted)
    std::shared_ptr<int> shared1 = std::make_shared<int>(42);
    std::shared_ptr<int> shared2 = shared1;

    std::cout << "Shared count = " << shared1.use_count() << "\n";
}


// ============================================================
// 6b - Concurrency: thread, mutex, async,
//      future, promise
// ============================================================

std::mutex mtx;

void increment(int& value) {
    std::lock_guard<std::mutex> lock(mtx);
    value++;
}

void concurrency_examples() {
    int counter = 0;

    // Threads
    std::thread t1(increment, std::ref(counter));
    std::thread t2(increment, std::ref(counter));
    t1.join();
    t2.join();

    std::cout << "Counter (mutex protected): " << counter << "\n";

    // std::async + future
    auto future_value = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        return 123;
    });

    std::cout << "Async result: " << future_value.get() << "\n";

    // promise / future
    std::promise<int> promise;
    std::future<int> future = promise.get_future();

    std::thread producer([&promise] {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        promise.set_value(99);
    });

    std::cout << "Promise result: " << future.get() << "\n";
    producer.join();
}


// ============================================================
// 6c - Performance Optimization
// ============================================================

struct Heavy {
    std::vector<int> data;

    Heavy(size_t n) : data(n, 42) {}

    // Copy constructor (expensive)
    Heavy(const Heavy& other) : data(other.data) {
        std::cout << "Copied\n";
    }

    // Move constructor (cheap)
    Heavy(Heavy&& other) noexcept : data(std::move(other.data)) {
        std::cout << "Moved\n";
    }
};

void performance_examples() {
    // Prefer move over copy
    Heavy a(1'000'000);
    Heavy b = std::move(a); // avoids deep copy

    // Reserve capacity to avoid reallocations
    std::vector<int> v;
    v.reserve(1'000);
    for (int i = 0; i < 1'000; ++i) {
        v.push_back(i);
    }

    // Avoid unnecessary synchronization
    std::atomic<int> fast_counter{0};
    fast_counter.fetch_add(1, std::memory_order_relaxed);

    std::cout << "Atomic counter: " << fast_counter.load() << "\n";
}


// ============================================================
// Main
// ============================================================

int main() {
    std::cout << "\n--- Ownership & Lifetime ---\n";
    smart_pointers_and_lifetime();

    std::cout << "\n--- Concurrency ---\n";
    concurrency_examples();

    std::cout << "\n--- Performance ---\n";
    performance_examples();

    return 0;
}

/*
Q: "How would you optimize this C++ code for performance?"
“First I’d measure using a profiler to find real bottlenecks. Then I’d focus on algorithmic improvements, reduce allocations, 
improve data locality, and minimize synchronization. I’d prefer move semantics over copies, reserve container capacity, and 
use atomics instead of mutexes when appropriate. Finally, I’d validate with benchmarks and compiler optimizations like -O3 and LTO.”

Q: "Compare Rust and C++ approaches to memory safety"
“C++ relies on RAII, smart pointers, and developer discipline, so memory safety issues are possible at runtime. Rust enforces 
ownership and borrowing rules at compile time, preventing use-after-free and data races in safe code, while still achieving 
performance comparable to C++ through zero-cost abstractions.”

Q: "You need to expose a C++ library to Rust via FFI. What are the challenges?"
“The main challenges are ABI stability, type safety, memory ownership, error handling, and thread safety. C++ ABI isn’t stable, 
so I’d expose a C-style API with extern "C", use plain data types, make ownership explicit, avoid exceptions across FFI, and clearly 
define threading guarantees.”

Why unique_ptr is preferred over shared_ptr
“unique_ptr has zero ownership overhead and clear lifetime semantics, while shared_ptr uses atomic reference counting, which is 
slower and can hide ownership problems.”

When stack allocation is better than heap
“Stack allocation is faster, cache-friendly, and automatically cleaned up, so it’s preferred for small, short-lived objects with clear lifetimes.”

Why move is cheaper than copy
“Move transfers ownership of resources by swapping pointers, while copy duplicates the underlying data, which is much more expensive.”

How RAII prevents leaks
“RAII ties resource acquisition to object lifetime, so resources are released automatically in destructors, even during early returns or exceptions.”

Difference between thread and async
“thread creates an OS thread, while async represents a task that may run on a thread pool and is scheduled cooperatively, making it 
more efficient for I/O-bound work.”

When to use mutex vs atomic
“Use atomics for simple shared state like counters, and mutexes when you need to protect complex data structures or multi-step invariants.”

Why promise / future exists
“They provide a safe way to transfer a value or error from one thread to another, enabling synchronization without shared mutable state.”

Data race vs race condition
“A data race is unsynchronized concurrent access to the same memory, which is undefined behavior, while a race condition is a logical timing 
bug that can happen even with correct synchronization.”

Copy vs move cost
“Copy allocates and duplicates data, while move usually just transfers ownership of pointers, making it significantly cheaper.”

Memory allocation strategies
“Prefer stack allocation, reuse memory, reserve container capacity, and use custom allocators or pools when allocation becomes a bottleneck.”

False sharing
“False sharing happens when unrelated data used by different threads resides on the same cache line, causing unnecessary cache 
invalidations and performance loss.”

Lock contention vs lock-free
“Lock contention blocks threads and hurts scalability, while lock-free approaches use atomics to make progress without blocking, 
improving throughput at the cost of complexity.”
*/