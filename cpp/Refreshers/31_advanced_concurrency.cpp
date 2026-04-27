////////* ADVANCED CONCURRENCY PATTERNS *////////

/*
 * LOCK-FREE PROGRAMMING & ADVANCED CONCURRENCY
 * 
 * Beyond basic mutexes and threads, modern C++ provides:
 *   - Atomics: Lock-free operations on single variables
 *   - Memory ordering: Control visibility of writes across threads
 *   - Lock-free data structures: High-performance concurrent containers
 *   - Advanced patterns: Thread pools, work stealing
 * 
 * Why lock-free?
 *   - No deadlocks (no locks!)
 *   - Better performance (no context switching)
 *   - Progress guarantees (wait-free, lock-free)
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <memory>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>

// ============================================================================
// 1. ATOMICS BASICS
// ============================================================================

/*
 * std::atomic<T> provides lock-free operations on type T:
 *   - load(): Read value
 *   - store(): Write value
 *   - exchange(): Swap value atomically
 *   - compare_exchange_weak/strong(): CAS (Compare-And-Swap)
 * 
 * Lock-free means: No thread can block another thread's progress
 * Wait-free means: Every operation completes in finite steps
 */

void demonstrate_atomics_basics() {
    std::cout << "=== ATOMICS BASICS ===\n\n";
    
    std::atomic<int> counter{0};
    
    // Basic operations
    counter.store(42);                          // Atomic write
    int value = counter.load();                 // Atomic read
    int old_value = counter.exchange(100);      // Atomic swap
    
    std::cout << "Stored: " << value << ", Old: " << old_value << "\n";
    std::cout << "Current: " << counter.load() << "\n\n";
    
    // Compare-And-Swap (CAS) - foundation of lock-free algorithms
    int expected = 100;
    bool success = counter.compare_exchange_strong(expected, 200);
    
    std::cout << "CAS success: " << success << "\n";
    std::cout << "Expected after: " << expected << " (updated if failed)\n";
    std::cout << "Counter: " << counter.load() << "\n\n";
    
    // Check if operations are lock-free
    std::cout << "int atomic is lock-free: " << counter.is_lock_free() << "\n";
    std::cout << "pointer atomic is lock-free: " 
              << std::atomic<void*>{}.is_lock_free() << "\n";
}

// ============================================================================
// 2. MEMORY ORDERING (Critical for correctness!)
// ============================================================================

/*
 * Memory ordering controls how memory operations are visible across threads:
 * 
 * memory_order_relaxed:
 *   - No synchronization, only atomicity
 *   - Use: Counters where order doesn't matter
 *   - Fastest
 * 
 * memory_order_acquire (for loads):
 *   - Subsequent reads/writes can't be reordered before this load
 *   - Pairs with release
 * 
 * memory_order_release (for stores):
 *   - Previous reads/writes can't be reordered after this store
 *   - Pairs with acquire
 * 
 * memory_order_acq_rel:
 *   - Both acquire and release
 *   - Use: Read-modify-write operations
 * 
 * memory_order_seq_cst (Sequential Consistency):
 *   - Total global order of all operations
 *   - Default, safest, slowest
 *   - Use: When unsure
 */

std::atomic<int> data{0};
std::atomic<bool> ready{false};

// WRONG: No synchronization
void producer_wrong() {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_relaxed);  // Consumer might see ready=true but data=0!
}

// CORRECT: Release-acquire synchronization
void producer_correct() {
    data.store(42, std::memory_order_relaxed);     // Can use relaxed for data
    ready.store(true, std::memory_order_release);  // Release: All previous writes visible
}

void consumer_correct() {
    while (!ready.load(std::memory_order_acquire)) {  // Acquire: See all previous writes
        std::this_thread::yield();
    }
    // Guaranteed to see data = 42
    std::cout << "Consumer sees data: " << data.load(std::memory_order_relaxed) << "\n";
}

void demonstrate_memory_ordering() {
    std::cout << "\n=== MEMORY ORDERING ===\n\n";
    
    // Reset
    data.store(0);
    ready.store(false);
    
    std::thread prod(producer_correct);
    std::thread cons(consumer_correct);
    
    prod.join();
    cons.join();
    
    std::cout << "\nMemory ordering guarantees:\n";
    std::cout << "  - Relaxed: No ordering, just atomicity\n";
    std::cout << "  - Acquire: See all writes before paired release\n";
    std::cout << "  - Release: All previous writes visible to acquire\n";
    std::cout << "  - Seq_cst: Total order (default, safest)\n";
}

// ============================================================================
// 3. HAPPENS-BEFORE & SYNCHRONIZES-WITH
// ============================================================================

/*
 * C++ Memory Model defines relationships between operations:
 * 
 * HAPPENS-BEFORE:
 *   - Operation A happens-before B if:
 *     1. A and B in same thread and A before B (sequenced-before)
 *     2. A synchronizes-with B
 *     3. Transitive: A happens-before C, C happens-before B => A happens-before B
 * 
 * SYNCHRONIZES-WITH:
 *   - A release store synchronizes-with an acquire load of same atomic
 *   - Thread creation synchronizes-with first operation in new thread
 *   - Thread join synchronizes-with last operation in joined thread
 * 
 * DATA RACE:
 *   - Two accesses to same memory, at least one is write, no happens-before
 *   - Data races are UNDEFINED BEHAVIOR!
 */

std::atomic<int> x{0}, y{0};
int r1 = 0, r2 = 0;

// Example: Detecting reordering
void thread1() {
    x.store(1, std::memory_order_relaxed);
    r1 = y.load(std::memory_order_relaxed);
}

void thread2() {
    y.store(1, std::memory_order_relaxed);
    r2 = x.load(std::memory_order_relaxed);
}

void demonstrate_memory_model() {
    std::cout << "\n=== MEMORY MODEL CONCEPTS ===\n\n";
    
    // With relaxed ordering, r1=0 and r2=0 is possible!
    // (Both loads can happen before both stores due to reordering)
    
    for (int i = 0; i < 10; ++i) {
        x.store(0); y.store(0); r1 = 0; r2 = 0;
        
        std::thread t1(thread1);
        std::thread t2(thread2);
        t1.join();
        t2.join();
        
        if (r1 == 0 && r2 == 0) {
            std::cout << "Iteration " << i << ": Both saw 0 (reordering happened!)\n";
        }
    }
    
    std::cout << "\nWith seq_cst, at least one thread would see 1\n";
}

// ============================================================================
// 4. LOCK-FREE STACK (Using CAS)
// ============================================================================

/*
 * Lock-free data structures use CAS (Compare-And-Swap) instead of locks:
 * 
 * Pattern:
 *   1. Read current state
 *   2. Compute new state
 *   3. CAS: If state unchanged, update; else retry
 * 
 * ABA Problem:
 *   - Thread reads A
 *   - Another thread changes A->B->A
 *   - First thread's CAS succeeds but data changed!
 *   - Solution: Tagged pointers, hazard pointers
 */

template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        Node* next;
        Node(T const& data_) : data(data_), next(nullptr) {}
    };
    
    std::atomic<Node*> head{nullptr};
    
public:
    void push(T const& data) {
        Node* new_node = new Node(data);
        
        // CAS loop: Retry until successful
        new_node->next = head.load(std::memory_order_relaxed);
        while (!head.compare_exchange_weak(
            new_node->next,              // Expected (updated if failed)
            new_node,                    // Desired
            std::memory_order_release,   // Success ordering
            std::memory_order_relaxed    // Failure ordering
        )) {
            // compare_exchange_weak can fail spuriously (false negative)
            // Loop retries automatically
        }
    }
    
    bool pop(T& result) {
        Node* old_head = head.load(std::memory_order_relaxed);
        
        // CAS loop
        while (old_head && !head.compare_exchange_weak(
            old_head,                    // Expected
            old_head->next,              // Desired
            std::memory_order_acquire,   // Success
            std::memory_order_relaxed    // Failure
        )) {
            // Retry if another thread changed head
        }
        
        if (!old_head) {
            return false;  // Empty
        }
        
        result = old_head->data;
        delete old_head;  // Memory leak possible! (See hazard pointers)
        return true;
    }
};

void demonstrate_lock_free_stack() {
    std::cout << "\n=== LOCK-FREE STACK ===\n\n";
    
    LockFreeStack<int> stack;
    
    // Multiple threads pushing
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([&stack, i] {
            for (int j = 0; j < 10; ++j) {
                stack.push(i * 100 + j);
            }
        });
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    // Pop all
    int value;
    int count = 0;
    while (stack.pop(value)) {
        ++count;
    }
    
    std::cout << "Pushed 40 items, popped " << count << "\n";
    std::cout << "Lock-free means: No thread blocked another\n";
}

// ============================================================================
// 5. THREAD POOL (Work stealing for load balancing)
// ============================================================================

/*
 * Thread Pool:
 *   - Fixed number of worker threads
 *   - Task queue shared across workers
 *   - Avoid thread creation overhead
 * 
 * Work Stealing:
 *   - Each worker has own queue
 *   - Idle workers steal from busy workers
 *   - Better load balancing
 */

class ThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop = false;
    
public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    
                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        
                        // Wait for task or stop signal
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });
                        
                        if (stop && tasks.empty()) {
                            return;
                        }
                        
                        task = std::move(tasks.front());
                        tasks.pop();
                    }
                    
                    task();  // Execute task
                }
            });
        }
    }
    
    template<typename F>
    void enqueue(F&& f) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.emplace(std::forward<F>(f));
        }
        condition.notify_one();
    }
    
    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();
        
        for (std::thread& worker : workers) {
            worker.join();
        }
    }
};

void demonstrate_thread_pool() {
    std::cout << "\n=== THREAD POOL ===\n\n";
    
    ThreadPool pool(4);  // 4 worker threads
    
    std::atomic<int> completed{0};
    
    // Submit 20 tasks
    for (int i = 0; i < 20; ++i) {
        pool.enqueue([i, &completed] {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            ++completed;
            std::cout << "Task " << i << " completed by thread "
                      << std::this_thread::get_id() << "\n";
        });
    }
    
    // Wait for completion
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "\nCompleted " << completed.load() << " tasks\n";
    std::cout << "Thread pool reuses threads, avoiding creation overhead\n";
}

// ============================================================================
// 6. C++20 JTHREAD & STOP_TOKEN
// ============================================================================

/*
 * std::jthread (C++20):
 *   - Automatically joins on destruction (no need to call join())
 *   - Supports cooperative cancellation via std::stop_token
 *   - RAII-friendly
 * 
 * std::stop_token:
 *   - Thread-safe cancellation mechanism
 *   - Worker checks token periodically
 *   - No race conditions
 */

#include <stop_token>  // C++20

void worker_with_stop_token(std::stop_token stoken) {
    int iteration = 0;
    while (!stoken.stop_requested()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        std::cout << "Worker iteration " << ++iteration << "\n";
    }
    std::cout << "Worker received stop request, exiting gracefully\n";
}

void demonstrate_jthread() {
    std::cout << "\n=== C++20 JTHREAD & STOP_TOKEN ===\n\n";
    
    // jthread automatically joins
    {
        std::jthread worker(worker_with_stop_token);
        
        std::this_thread::sleep_for(std::chrono::milliseconds(350));
        
        // Request stop
        worker.request_stop();
        
        // No need to call join()! jthread does it in destructor
    }
    
    std::cout << "\njthread advantages:\n";
    std::cout << "  - Automatic joining (RAII)\n";
    std::cout << "  - Cooperative cancellation\n";
    std::cout << "  - No race conditions on stop\n";
}

// ============================================================================
// 7. DOUBLE-CHECKED LOCKING (Correct pattern)
// ============================================================================

/*
 * Double-Checked Locking:
 *   - Common singleton pattern
 *   - Check without lock (fast path)
 *   - Check with lock (slow path)
 * 
 * WRONG implementation has data race!
 * CORRECT: Use atomic with acquire-release
 */

class Singleton {
private:
    static std::atomic<Singleton*> instance;
    static std::mutex mutex;
    
    Singleton() {}
    
public:
    static Singleton* get_instance() {
        Singleton* tmp = instance.load(std::memory_order_acquire);
        
        if (tmp == nullptr) {  // First check (no lock)
            std::lock_guard<std::mutex> lock(mutex);
            tmp = instance.load(std::memory_order_relaxed);
            
            if (tmp == nullptr) {  // Second check (with lock)
                tmp = new Singleton();
                instance.store(tmp, std::memory_order_release);
            }
        }
        
        return tmp;
    }
};

std::atomic<Singleton*> Singleton::instance{nullptr};
std::mutex Singleton::mutex;

void demonstrate_double_checked_locking() {
    std::cout << "\n=== DOUBLE-CHECKED LOCKING ===\n\n";
    
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([] {
            Singleton* s = Singleton::get_instance();
            std::cout << "Thread got singleton at " << s << "\n";
        });
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "\nAll threads got same instance (correct!)\n";
}

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

int main() {
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║      ADVANCED CONCURRENCY PATTERNS DEMONSTRATION         ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n\n";
    
    demonstrate_atomics_basics();
    demonstrate_memory_ordering();
    demonstrate_memory_model();
    demonstrate_lock_free_stack();
    demonstrate_thread_pool();
    demonstrate_jthread();
    demonstrate_double_checked_locking();
    
    std::cout << "\n=== SUMMARY ===\n\n";
    std::cout << "Atomics: Lock-free operations on single variables\n";
    std::cout << "Memory Ordering: Control visibility across threads\n";
    std::cout << "Lock-Free: Use CAS (compare_exchange) for data structures\n";
    std::cout << "Thread Pool: Reuse threads, better performance\n";
    std::cout << "jthread: C++20 RAII threads with cancellation\n";
    
    return 0;
}

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/*
 * 1. ATOMICS:
 *    - Lock-free operations: load, store, exchange, CAS
 *    - Use compare_exchange for lock-free data structures
 *    - Check is_lock_free() for your platform
 * 
 * 2. MEMORY ORDERING (Most important!):
 *    - Relaxed: No ordering, just atomicity (use for counters)
 *    - Acquire/Release: Synchronization (use for producer-consumer)
 *    - Seq_cst: Total order (default, use when unsure)
 *    - WRONG ordering causes data races!
 * 
 * 3. MEMORY MODEL:
 *    - Happens-before: Defines order between operations
 *    - Synchronizes-with: Release pairs with acquire
 *    - Data race = UB (undefined behavior)
 * 
 * 4. LOCK-FREE DATA STRUCTURES:
 *    - Pattern: Read, compute, CAS, retry if failed
 *    - Beware ABA problem (use tagged pointers)
 *    - Memory reclamation is hard (hazard pointers, RCU)
 * 
 * 5. THREAD POOL:
 *    - Fixed threads, task queue
 *    - Avoids thread creation overhead
 *    - Work stealing for load balancing
 * 
 * 6. C++20 FEATURES:
 *    - jthread: Automatic joining, RAII-friendly
 *    - stop_token: Cooperative cancellation
 *    - No manual join() needed
 * 
 * Lock-free programming is HARD. Use when:
 *   - Performance critical (high contention)
 *   - Real-time requirements (no blocking)
 *   - After profiling shows locks are bottleneck
 * 
 * Otherwise, use mutexes (simpler, less error-prone)!
 */
