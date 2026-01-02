////////* THREADS *////////

#include <iostream>
#include <thread>
#include <chrono>
#include <vector>

void basic_thread_management() {
    std::cout << "\n=== BASIC THREAD MANAGEMENT ===\n";
    
    // 1. Creating threads with different callables
    auto lambda = []() {
        std::cout << "Thread ID: " << std::this_thread::get_id() 
                  << " - Lambda executing\n";
    };
    
    void function() {
        std::cout << "Thread ID: " << std::this_thread::get_id() 
                  << " - Function executing\n";
    };
    
    struct Functor {
        void operator()() {
            std::cout << "Thread ID: " << std::this_thread::get_id() 
                      << " - Functor executing\n";
        }
    };
    
    // Create threads with different callables
    std::thread t1(lambda);       // Lambda
    std::thread t2(function);     // Function pointer
    std::thread t3(Functor());    // Functor
    std::thread t4([]() {         // Inline lambda
        std::cout << "Thread ID: " << std::this_thread::get_id() 
                  << " - Inline lambda\n";
    });
    
    // 2. JOIN vs DETACH
    // join() - Wait for thread to complete
    t1.join();  // Main thread blocks until t1 finishes
    
    // detach() - Allow thread to run independently
    t2.detach();  // t2 runs independently, becomes a daemon thread
    // WARNING: After detach, can't join or control thread
    // WARNING: If main exits before detached thread, program terminates
    
    // 3. Thread with parameters
    auto worker = [](int id, const std::string& msg) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100 * id));
        std::cout << "Worker " << id << ": " << msg << "\n";
    };
    
    std::thread t5(worker, 1, "Hello from worker!");
    std::thread t6(worker, 2, "Another worker");
    
    t3.join();
    t4.join();
    t5.join();
    t6.join();
    
    // 4. Thread Guard RAII class
    class ThreadGuard {
        std::thread& t;
    public:
        explicit ThreadGuard(std::thread& t_) : t(t_) {}
        
        ~ThreadGuard() {
            if (t.joinable()) {
                std::cout << "ThreadGuard ensuring join\n";
                t.join();  // Automatically join in destructor
            }
        }
        
        // Prevent copying
        ThreadGuard(const ThreadGuard&) = delete;
        ThreadGuard& operator=(const ThreadGuard&) = delete;
    };
    
    std::thread t7([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        std::cout << "Thread with guard finishing\n";
    });
    
    ThreadGuard guard(t7);  // Will automatically join when guard goes out of scope
    // No need to call t7.join() manually
    
    std::cout << "All threads managed\n";
}

void thread_exceptions() {
    // 5. Handling exceptions with threads
    try {
        std::thread t([]() {
            throw std::runtime_error("Thread exception!");
        });
        
        // If exception occurs before join, thread becomes detached
        // Solution: Use RAII or try-catch
        t.join();  // This won't execute if exception thrown above
    }
    catch (...) {
        std::cout << "Exception caught, but thread might still be running!\n";
    }
    
    // Better approach: RAII wrapper
    class SafeThread {
        std::thread t;
    public:
        template<typename Callable, typename... Args>
        SafeThread(Callable&& f, Args&&... args)
            : t(std::forward<Callable>(f), std::forward<Args>(args)...) {}
        
        ~SafeThread() {
            if (t.joinable()) {
                t.join();
            }
        }
        
        // Allow moving
        SafeThread(SafeThread&&) = default;
        SafeThread& operator=(SafeThread&&) = default;
        
        // Disallow copying
        SafeThread(const SafeThread&) = delete;
        SafeThread& operator=(const SafeThread&) = delete;
    };
}


////////* MUTEXES *////////

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>

class BankAccount {
private:
    int balance = 0;
    mutable std::mutex balance_mutex;  // mutable allows locking in const methods
    
public:
    void deposit(int amount) {
        std::lock_guard<std::mutex> lock(balance_mutex);  // RAII lock
        // Automatically locks on construction, unlocks on destruction
        balance += amount;
        std::cout << "Deposited " << amount 
                  << ", balance: " << balance 
                  << " (Thread: " << std::this_thread::get_id() << ")\n";
    }
    
    void withdraw(int amount) {
        std::lock_guard<std::mutex> lock(balance_mutex);
        if (balance >= amount) {
            balance -= amount;
            std::cout << "Withdrew " << amount 
                      << ", balance: " << balance 
                      << " (Thread: " << std::this_thread::get_id() << ")\n";
        }
    }
    
    int get_balance() const {
        std::lock_guard<std::mutex> lock(balance_mutex);
        return balance;
    }
    
    // Using unique_lock for more flexibility
    bool transfer(BankAccount& to, int amount) {
        // Need to lock both accounts to prevent deadlock
        std::unique_lock<std::mutex> lock1(balance_mutex, std::defer_lock);
        std::unique_lock<std::mutex> lock2(to.balance_mutex, std::defer_lock);
        
        // Lock both mutexes atomically to prevent deadlock
        std::lock(lock1, lock2);  // Uses deadlock avoidance algorithm
        
        if (balance >= amount) {
            balance -= amount;
            to.balance += amount;
            
            std::cout << "Transferred " << amount << " between accounts\n";
            
            // Can manually unlock if needed (unique_lock specific)
            lock1.unlock();
            lock2.unlock();
            
            return true;
        }
        return false;
    }
};

void demonstrate_synchronization() {
    std::cout << "\n=== SYNCHRONIZATION PRIMITIVES ===\n";
    
    BankAccount account;
    std::vector<std::thread> threads;
    
    // Multiple threads accessing shared resource
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&account, i]() {
            for (int j = 0; j < 3; ++j) {
                account.deposit(100 + i * 10);
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        });
    }
    
    for (auto& t : threads) t.join();
    threads.clear();
    
    std::cout << "Final balance: " << account.get_balance() << "\n";
    
    // 2. std::scoped_lock (C++17) - improved version of std::lock with RAII
    class DualAccount {
        std::mutex mtx1, mtx2;
        int account1 = 1000;
        int account2 = 1000;
        
    public:
        void transfer_between(int amount) {
            // scoped_lock automatically locks all mutexes using deadlock avoidance
            std::scoped_lock lock(mtx1, mtx2);  // RAII, automatically unlocks
            
            if (account1 >= amount) {
                account1 -= amount;
                account2 += amount;
                std::cout << "Internal transfer: " << amount << "\n";
            }
        }
        
        // Deadlock-prone version (WRONG!)
        void bad_transfer(DualAccount& other, int amount) {
            std::lock_guard<std::mutex> lock1(mtx1);
            std::this_thread::sleep_for(std::chrono::milliseconds(1));  // Increase deadlock chance
            std::lock_guard<std::mutex> lock2(other.mtx1);  // WRONG ORDER!
            // Could deadlock if other thread tries to lock in reverse order
            
            if (account1 >= amount) {
                account1 -= amount;
                other.account1 += amount;
            }
        }
        
        // Correct version with scoped_lock
        void safe_transfer(DualAccount& other, int amount) {
            // Lock both accounts' mutexes atomically
            std::scoped_lock lock(mtx1, other.mtx1);
            
            if (account1 >= amount) {
                account1 -= amount;
                other.account1 += amount;
                std::cout << "Safe transfer completed\n";
            }
        }
    };
    
    // 3. unique_lock features
    std::mutex mtx;
    std::condition_variable cv;
    bool data_ready = false;
    
    std::thread producer([&]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        std::unique_lock<std::mutex> lock(mtx);
        data_ready = true;
        
        // Can unlock before notifying for better performance
        lock.unlock();
        cv.notify_one();
    });
    
    std::thread consumer([&]() {
        std::unique_lock<std::mutex> lock(mtx);
        
        // Wait with predicate to handle spurious wakeups
        cv.wait(lock, [&]() { return data_ready; });
        
        std::cout << "Consumer got data\n";
    });
    
    producer.join();
    consumer.join();
}


////////* CONDITION VARIABLES *////////

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <chrono>

class ThreadSafeQueue {
private:
    std::queue<int> queue;
    mutable std::mutex mtx;
    std::condition_variable cv_not_empty;  // Signals when queue has items
    std::condition_variable cv_not_full;   // Signals when queue has space
    size_t max_size = 10;
    bool shutdown = false;
    
public:
    void push(int value) {
        std::unique_lock<std::mutex> lock(mtx);
        
        // Wait until queue has space OR shutdown requested
        cv_not_full.wait(lock, [this]() { 
            return queue.size() < max_size || shutdown; 
        });
        
        if (shutdown) return;
        
        queue.push(value);
        std::cout << "Produced: " << value 
                  << " (size: " << queue.size() << ")\n";
        
        // Notify one consumer that data is available
        cv_not_empty.notify_one();
        // cv_not_empty.notify_all();  // To notify all waiting threads
    }
    
    bool pop(int& value) {
        std::unique_lock<std::mutex> lock(mtx);
        
        // Wait with predicate to handle SPURIOUS WAKEUPS
        // Spurious wakeup: thread can wake up even without notify!
        // Always use predicate in wait() calls
        cv_not_empty.wait(lock, [this]() { 
            return !queue.empty() || shutdown; 
        });
        
        if (shutdown && queue.empty()) return false;
        
        value = queue.front();
        queue.pop();
        std::cout << "Consumed: " << value 
                  << " (size: " << queue.size() << ")\n";
        
        cv_not_full.notify_one();
        return true;
    }
    
    void shutdown_queue() {
        {
            std::lock_guard<std::mutex> lock(mtx);
            shutdown = true;
        }
        // Notify ALL waiting threads to check shutdown flag
        cv_not_empty.notify_all();
        cv_not_full.notify_all();
    }
    
    size_t size() const {
        std::lock_guard<std::mutex> lock(mtx);
        return queue.size();
    }
};

void demonstrate_condition_variables() {
    std::cout << "\n=== CONDITION VARIABLES ===\n";
    
    ThreadSafeQueue queue;
    std::vector<std::thread> producers;
    std::vector<std::thread> consumers;
    
    // Create producer threads
    for (int i = 0; i < 3; ++i) {
        producers.emplace_back([&queue, i]() {
            for (int j = 0; j < 5; ++j) {
                queue.push(i * 100 + j);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }
        });
    }
    
    // Create consumer threads
    for (int i = 0; i < 2; ++i) {
        consumers.emplace_back([&queue, i]() {
            int value;
            while (queue.pop(value)) {
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
            }
            std::cout << "Consumer " << i << " shutting down\n";
        });
    }
    
    // Let producers finish
    for (auto& t : producers) t.join();
    
    // Give consumers time to process
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    
    // Shutdown queue
    queue.shutdown_queue();
    
    // Wait for consumers to finish
    for (auto& t : consumers) t.join();
    
    std::cout << "Queue size at end: " << queue.size() << "\n";
    
    // 2. Producer-Consumer with timeout
    std::mutex mtx;
    std::condition_variable cv;
    bool ready = false;
    
    std::thread worker([&]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
        cv.notify_one();
    });
    
    std::unique_lock<std::mutex> lock(mtx);
    
    // wait_for with timeout
    auto status = cv.wait_for(lock, std::chrono::milliseconds(100), 
                             [&]() { return ready; });
    
    if (status) {
        std::cout << "Condition met within timeout\n";
    } else {
        std::cout << "Timeout reached, condition not met\n";
    }
    
    worker.join();
}


////////* ATOMICS *////////

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <cassert>

void demonstrate_atomics() {
    std::cout << "\n=== ATOMIC OPERATIONS ===\n";
    
    // 1. Basic atomic operations
    std::atomic<int> counter(0);
    std::vector<std::thread> threads;
    
    // Atomic operations are thread-safe without locks
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) {
                counter.fetch_add(1, std::memory_order_relaxed);
            }
        });
    }
    
    for (auto& t : threads) t.join();
    std::cout << "Counter value: " << counter.load() << "\n";
    
    // 2. Memory ordering - understanding the hierarchy
    // memory_order_relaxed: No synchronization, just atomicity
    // memory_order_acquire: Read barrier (load operations)
    // memory_order_release: Write barrier (store operations)
    // memory_order_acq_rel: Both acquire and release
    // memory_order_seq_cst: Sequential consistency (default, strongest)
    
    // Producer-Consumer with memory barriers
    struct Data {
        int x = 0;
        int y = 0;
    };
    
    std::atomic<Data*> atomic_ptr(nullptr);
    Data* shared_data = nullptr;
    
    std::thread writer([&]() {
        Data* new_data = new Data{1, 2};
        
        // Initialize data
        new_data->x = 42;
        new_data->y = 100;
        
        // Release store: ensures all writes before this point
        // are visible to threads that do an acquire load
        atomic_ptr.store(new_data, std::memory_order_release);
    });
    
    std::thread reader([&]() {
        Data* local_ptr = nullptr;
        
        // Spin until data is available
        while (!(local_ptr = atomic_ptr.load(std::memory_order_acquire))) {
            // busy wait
        }
        
        // Acquire load: ensures we see all writes that happened
        // before the release store
        std::cout << "Read data: x=" << local_ptr->x 
                  << ", y=" << local_ptr->y << "\n";
        
        delete local_ptr;
    });
    
    writer.join();
    reader.join();
    
    // 3. Compare-and-swap (CAS) - building block for lock-free algorithms
    std::atomic<int> value(0);
    
    auto atomic_update = [&value](int expected, int desired) {
        // Try to update only if current value matches expected
        bool success = value.compare_exchange_weak(
            expected, 
            desired,
            std::memory_order_acq_rel,
            std::memory_order_relaxed
        );
        
        if (success) {
            std::cout << "CAS succeeded: " << expected 
                      << " -> " << desired << "\n";
        } else {
            std::cout << "CAS failed, current value is: " << expected << "\n";
        }
        return success;
    };
    
    std::thread t1([&atomic_update]() {
        atomic_update(0, 10);
    });
    
    std::thread t2([&atomic_update]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        atomic_update(0, 20);  // Will fail because value changed
    });
    
    t1.join();
    t2.join();
    
    // 4. Lock-free stack example
    template<typename T>
    class LockFreeStack {
    private:
        struct Node {
            T data;
            Node* next;
            Node(const T& d) : data(d), next(nullptr) {}
        };
        
        std::atomic<Node*> head = nullptr;
        
    public:
        void push(const T& value) {
            Node* new_node = new Node(value);
            new_node->next = head.load(std::memory_order_relaxed);
            
            // CAS loop to update head atomically
            while (!head.compare_exchange_weak(
                new_node->next,
                new_node,
                std::memory_order_release,
                std::memory_order_relaxed)) {
                // Loop until successful
            }
        }
        
        bool pop(T& value) {
            Node* old_head = head.load(std::memory_order_relaxed);
            if (!old_head) return false;
            
            // CAS loop to remove head atomically
            while (old_head && 
                   !head.compare_exchange_weak(
                       old_head,
                       old_head->next,
                       std::memory_order_acq_rel,
                       std::memory_order_relaxed)) {
                // Loop until successful
            }
            
            if (!old_head) return false;
            
            value = old_head->data;
            delete old_head;
            return true;
        }
    };
    
    // Test lock-free stack
    LockFreeStack<int> stack;
    std::vector<std::thread> stack_threads;
    
    for (int i = 0; i < 5; ++i) {
        stack_threads.emplace_back([&stack, i]() {
            for (int j = 0; j < 10; ++j) {
                stack.push(i * 100 + j);
            }
        });
    }
    
    for (auto& t : stack_threads) t.join();
    
    int popped_value;
    int pop_count = 0;
    while (stack.pop(popped_value)) {
        ++pop_count;
    }
    
    std::cout << "Popped " << pop_count << " items from lock-free stack\n";
}


////////* DEADLOCKS AND SAFE CONDITIONS *////////

#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
#include <vector>

void demonstrate_deadlocks_races() {
    std::cout << "\n=== DEADLOCKS & RACE CONDITIONS ===\n";
    
    // 1. RACE CONDITION EXAMPLE
    std::cout << "\n=== RACE CONDITION ===\n";
    
    class Counter {
        int value = 0;
    public:
        void increment() {
            // NOT thread-safe - race condition!
            ++value;  // This is multiple operations: read, modify, write
        }
        int get() const { return value; }
    };
    
    Counter unsafe_counter;
    std::vector<std::thread> race_threads;
    
    for (int i = 0; i < 10; ++i) {
        race_threads.emplace_back([&unsafe_counter]() {
            for (int j = 0; j < 1000; ++j) {
                unsafe_counter.increment();
            }
        });
    }
    
    for (auto& t : race_threads) t.join();
    
    std::cout << "Unsafe counter (should be 10000): " 
              << unsafe_counter.get() << "\n";
    
    // 2. DEADLOCK EXAMPLES
    std::cout << "\n=== DEADLOCK EXAMPLE ===\n";
    
    std::mutex mtx1, mtx2;
    
    auto deadlock_task1 = [&]() {
        std::lock_guard<std::mutex> lock1(mtx1);
        std::cout << "Thread 1 locked mutex1\n";
        
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        
        std::cout << "Thread 1 trying to lock mutex2...\n";
        std::lock_guard<std::mutex> lock2(mtx2);  // DEADLOCK!
        std::cout << "Thread 1 locked mutex2\n";
    };
    
    auto deadlock_task2 = [&]() {
        std::lock_guard<std::mutex> lock1(mtx2);
        std::cout << "Thread 2 locked mutex2\n";
        
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        
        std::cout << "Thread 2 trying to lock mutex1...\n";
        std::lock_guard<std::mutex> lock2(mtx1);  // DEADLOCK!
        std::cout << "Thread 2 locked mutex1\n";
    };
    
    // Uncomment to see deadlock (program will hang)
    // std::thread t1(deadlock_task1);
    // std::thread t2(deadlock_task2);
    // t1.join();
    // t2.join();
    
    // 3. DEADLOCK PREVENTION STRATEGIES
    std::cout << "\n=== DEADLOCK PREVENTION ===\n";
    
    // Strategy 1: Always lock in same order
    auto safe_task1 = [&]() {
        std::scoped_lock lock(mtx1, mtx2);  // Locks both atomically
        std::cout << "Safe thread 1 locked both mutexes\n";
    };
    
    auto safe_task2 = [&]() {
        std::scoped_lock lock(mtx1, mtx2);  // Same order!
        std::cout << "Safe thread 2 locked both mutexes\n";
    };
    
    std::thread safe_t1(safe_task1);
    std::thread safe_t2(safe_task2);
    
    safe_t1.join();
    safe_t2.join();
    
    // Strategy 2: Use std::lock with unique_lock
    auto safe_task3 = [&]() {
        std::unique_lock<std::mutex> lock1(mtx1, std::defer_lock);
        std::unique_lock<std::mutex> lock2(mtx2, std::defer_lock);
        std::lock(lock1, lock2);  // Deadlock-free locking
        std::cout << "Task3 locked both mutexes\n";
    };
    
    // Strategy 3: Lock timeouts (try_lock)
    auto timeout_task = [&]() {
        std::unique_lock<std::mutex> lock1(mtx1, std::defer_lock);
        
        if (lock1.try_lock_for(std::chrono::milliseconds(100))) {
            std::cout << "Got lock1, trying lock2...\n";
            
            std::unique_lock<std::mutex> lock2(mtx2, std::defer_lock);
            if (lock2.try_lock_for(std::chrono::milliseconds(100))) {
                std::cout << "Got both locks!\n";
                return true;
            } else {
                std::cout << "Couldn't get lock2, releasing lock1\n";
                lock1.unlock();
                return false;
            }
        }
        return false;
    };
    
    // 4. LIVELOCK EXAMPLE
    std::cout << "\n=== LIVELOCK EXAMPLE ===\n";
    
    bool resource_available = false;
    std::mutex livelock_mutex;
    
    auto polite_worker = [&](int id) {
        for (int i = 0; i < 3; ++i) {
            std::unique_lock<std::mutex> lock(livelock_mutex);
            
            if (resource_available) {
                std::cout << "Worker " << id << " got resource\n";
                resource_available = false;
                lock.unlock();
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
                
                // Make resource available again
                std::lock_guard<std::mutex> lg(livelock_mutex);
                resource_available = true;
                break;
            } else {
                std::cout << "Worker " << id << " yielding\n";
                lock.unlock();
                std::this_thread::yield();  // Try to avoid livelock
                std::this_thread::sleep_for(std::chrono::milliseconds(1));
            }
        }
    };
    
    resource_available = true;
    std::thread worker1(polite_worker, 1);
    std::thread worker2(polite_worker, 2);
    
    worker1.join();
    worker2.join();
    
    // 5. DETECTION TOOLS & BEST PRACTICES
    std::cout << "\n=== DETECTION & BEST PRACTICES ===\n";
    
    // Best practices:
    // 1. Use RAII locks (lock_guard, unique_lock, scoped_lock)
    // 2. Always lock in same order
    // 3. Avoid nested locks when possible
    // 4. Use lock-free algorithms for simple cases
    // 5. Keep critical sections small
    // 6. Use thread sanitizers (TSan) for detection
    
    // Example of thread-safe class design
    class ThreadSafeBank {
    private:
        struct Account {
            int balance = 0;
            std::mutex mtx;
        };
        
        std::unordered_map<int, Account> accounts;
        mutable std::shared_mutex accounts_mtx;  // For reader-writer pattern
        
    public:
        void transfer(int from, int to, int amount) {
            // Lock accounts in consistent order (by account ID)
            if (from == to) return;
            
            int first = std::min(from, to);
            int second = std::max(from, to);
            
            // Use shared_lock for reading, unique_lock for writing
            std::shared_lock read_lock(accounts_mtx);
            auto& acc1 = accounts[first];
            auto& acc2 = accounts[second];
            read_lock.unlock();
            
            // Lock both account mutexes atomically
            std::scoped_lock lock(acc1.mtx, acc2.mtx);
            
            if (acc1.balance >= amount) {
                acc1.balance -= amount;
                acc2.balance += amount;
                std::cout << "Transfer successful: " << amount 
                          << " from " << from << " to " << to << "\n";
            }
        }
        
        int get_balance(int account_id) const {
            std::shared_lock lock(accounts_mtx);  // Shared lock for reading
            auto it = accounts.find(account_id);
            if (it != accounts.end()) {
                std::lock_guard acc_lock(it->second.mtx);
                return it->second.balance;
            }
            return 0;
        }
    };
    
    // 6. USING THREAD SANITIZER
    // Compile with: -fsanitize=thread -g
    // Run to detect data races and deadlocks
    
    ThreadSafeBank bank;
    
    std::thread bank_t1([&bank]() {
        bank.transfer(1, 2, 100);
    });
    
    std::thread bank_t2([&bank]() {
        bank.transfer(2, 1, 50);
    });
    
    bank_t1.join();
    bank_t2.join();
}

int main() {
    std::cout << "=== COMPREHENSIVE C++ CONCURRENCY DEMONSTRATION ===\n";
    
    basic_thread_management();
    demonstrate_synchronization();
    demonstrate_condition_variables();
    demonstrate_atomics();
    demonstrate_async_operations();
    demonstrate_parallel_algorithms();
    demonstrate_thread_pools();
    demonstrate_deadlocks_races();
    
    std::cout << "\n=== ALL DEMONSTRATIONS COMPLETED ===\n";
    return 0;
}