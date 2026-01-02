#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <functional>
#include <future>
#include <condition_variable>
#include <atomic>

class ThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    
    std::mutex queue_mutex;
    std::condition_variable condition;
    std::atomic<bool> stop;
    
public:
    ThreadPool(size_t num_threads) : stop(false) {
        workers.reserve(num_threads);
        
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this]() {
                this->worker_loop();
            });
        }
    }
    
    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();
        
        for (std::thread& worker : workers) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }
    
    // Enqueue a task and return a future
    template<typename F, typename... Args>
    auto enqueue(F&& f, Args&&... args) 
        -> std::future<typename std::invoke_result<F, Args...>::type> {
        
        using return_type = typename std::invoke_result<F, Args...>::type;
        
        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );
        
        std::future<return_type> result = task->get_future();
        
        {
            std::lock_guard<std::mutex> lock(queue_mutex);
            if (stop) {
                throw std::runtime_error("enqueue on stopped ThreadPool");
            }
            
            tasks.emplace([task]() { (*task)(); });
        }
        
        condition.notify_one();
        return result;
    }
    
private:
    void worker_loop() {
        while (true) {
            std::function<void()> task;
            
            {
                std::unique_lock<std::mutex> lock(queue_mutex);
                
                // Wait for task or stop signal
                condition.wait(lock, [this]() { 
                    return stop || !tasks.empty(); 
                });
                
                if (stop && tasks.empty()) {
                    return;
                }
                
                task = std::move(tasks.front());
                tasks.pop();
            }
            
            // Execute the task
            task();
        }
    }
};

class TaskSystem {
private:
    ThreadPool pool;
    std::vector<std::future<void>> futures;
    
public:
    TaskSystem(size_t num_workers = std::thread::hardware_concurrency())
        : pool(num_workers) {}
    
    template<typename F, typename... Args>
    void submit(F&& f, Args&&... args) {
        auto future = pool.enqueue(std::forward<F>(f), 
                                   std::forward<Args>(args)...);
        futures.push_back(std::move(future));
    }
    
    void wait_all() {
        for (auto& future : futures) {
            future.wait();
        }
        futures.clear();
    }
    
    template<typename F, typename... Args>
    auto submit_with_result(F&& f, Args&&... args) {
        return pool.enqueue(std::forward<F>(f), 
                            std::forward<Args>(args)...);
    }
};

void demonstrate_thread_pools() {
    std::cout << "\n=== THREAD POOLS & TASK SYSTEMS ===\n";
    
    // 1. Basic thread pool usage
    ThreadPool pool(4);  // 4 worker threads
    
    std::vector<std::future<int>> results;
    
    // Submit tasks to thread pool
    for (int i = 0; i < 10; ++i) {
        results.emplace_back(
            pool.enqueue([i]() -> int {
                std::cout << "Task " << i << " started on thread " 
                          << std::this_thread::get_id() << "\n";
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
                return i * i;
            })
        );
    }
    
    // Collect results
    for (auto& result : results) {
        std::cout << "Result: " << result.get() << "\n";
    }
    
    // 2. Task system with dependency tracking
    std::cout << "\n=== TASK SYSTEM WITH DEPENDENCIES ===\n";
    
    TaskSystem task_system;
    std::promise<int> initial_promise;
    std::future<int> initial_future = initial_promise.get_future();
    
    // Chain of dependent tasks
    auto task1 = task_system.submit_with_result([initial_future = std::move(initial_future)]() mutable {
        int value = initial_future.get();  // Wait for initial value
        std::cout << "Task1 processing: " << value << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        return value * 2;
    });
    
    auto task2 = task_system.submit_with_result([&task1]() {
        int value = task1.get();  // Wait for task1
        std::cout << "Task2 processing: " << value << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        return value + 10;
    });
    
    auto task3 = task_system.submit_with_result([&task1]() {
        int value = task1.get();  // Wait for task1 (fan-out)
        std::cout << "Task3 processing: " << value << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        return value - 5;
    });
    
    // Start the chain
    initial_promise.set_value(42);
    
    // Get final results
    std::cout << "Task2 result: " << task2.get() << "\n";
    std::cout << "Task3 result: " << task3.get() << "\n";
    
    // 3. Work-stealing thread pool (more advanced)
    class WorkStealingThreadPool {
        // Implementation would have multiple task queues
        // Workers steal tasks from other workers when idle
        // More complex but better load balancing
    };
    
    // 4. Priority thread pool
    class PriorityThreadPool {
    private:
        struct Task {
            std::function<void()> func;
            int priority;
            
            bool operator<(const Task& other) const {
                // Lower priority number = higher priority
                return priority > other.priority;
            }
        };
        
        std::vector<std::thread> workers;
        std::priority_queue<Task> tasks;
        // ... similar to ThreadPool but with priority queue
    };
}