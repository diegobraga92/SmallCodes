////////* ASYNC *////////

#include <iostream>
#include <future>
#include <thread>
#include <chrono>
#include <vector>
#include <numeric>

void demonstrate_async_operations() {
    std::cout << "\n=== ASYNC OPERATIONS & FUTURES ===\n";
    
    // 1. std::async - simplest way to run async tasks
    auto compute_sum = [](int start, int end) -> int {
        int sum = 0;
        for (int i = start; i <= end; ++i) {
            sum += i;
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
        return sum;
    };
    
    // Launch policy: std::launch::async (run in new thread)
    //                std::launch::deferred (run when get() is called)
    std::future<int> future1 = std::async(std::launch::async, 
                                          compute_sum, 1, 100);
    
    std::future<int> future2 = std::async(std::launch::async,
                                          compute_sum, 101, 200);
    
    // Do other work while async tasks run
    std::cout << "Main thread doing other work...\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    
    // Get results (blocks until ready if not already)
    int result1 = future1.get();  // Can only call get() once!
    int result2 = future2.get();
    
    std::cout << "Sum 1-100: " << result1 << "\n";
    std::cout << "Sum 101-200: " << result2 << "\n";
    std::cout << "Total: " << (result1 + result2) << "\n";
    
    // 2. std::promise - for setting value from one thread, getting in another
    std::promise<int> promise;
    std::future<int> promise_future = promise.get_future();
    
    std::thread worker_thread([&promise]() {
        std::cout << "Worker thread computing...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        // Set the value (can also set exception with set_exception)
        promise.set_value(42);
        
        // Note: can also use promise.set_value_at_thread_exit()
        // to set value when thread exits
    });
    
    // Main thread waits for value
    std::cout << "Main thread waiting for promise...\n";
    int promised_value = promise_future.get();
    std::cout << "Got promised value: " << promised_value << "\n";
    
    worker_thread.join();
    
    // 3. std::packaged_task - wraps callable to produce future
    std::packaged_task<int(int, int)> task([](int a, int b) {
        std::cout << "Packaged task executing with " << a << ", " << b << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        return a * b;
    });
    
    std::future<int> task_future = task.get_future();
    
    // Can run task in different ways:
    // - In thread
    std::thread task_thread(std::move(task), 6, 7);
    
    // - Or directly (synchronous)
    // task(6, 7);
    
    int task_result = task_future.get();
    std::cout << "Task result: " << task_result << "\n";
    
    task_thread.join();
    
    // 4. std::future utilities
    std::future<void> void_future = std::async(std::launch::async, []() {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        std::cout << "Void future completed\n";
    });
    
    // Check if future is ready
    if (void_future.wait_for(std::chrono::milliseconds(10)) == 
        std::future_status::ready) {
        std::cout << "Future is ready\n";
    } else {
        std::cout << "Future not ready yet\n";
    }
    
    void_future.wait();  // Block until ready
    // void_future.get();  // For void futures, get() returns void
    
    // 5. std::shared_future - can be shared/copied (unlike std::future)
    std::promise<std::string> shared_promise;
    std::shared_future<std::string> shared_future = shared_promise.get_future().share();
    
    std::vector<std::thread> shared_threads;
    
    // Multiple threads can wait on same shared_future
    for (int i = 0; i < 3; ++i) {
        shared_threads.emplace_back([shared_future, i]() {
            // Each thread gets its own copy of shared_future
            std::string result = shared_future.get();  // Can call get() multiple times
            std::cout << "Thread " << i << " got: " << result << "\n";
        });
    }
    
    // Set value once, all threads receive it
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    shared_promise.set_value("Hello from shared future!");
    
    for (auto& t : shared_threads) t.join();
    
    // 6. Exception handling with futures
    std::future<int> exception_future = std::async(std::launch::async, []() -> int {
        throw std::runtime_error("Task failed!");
        return 42;  // Never reached
    });
    
    try {
        int value = exception_future.get();
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception from future: " << e.what() << "\n";
    }
}


////////* PARALLEL ALGORITHMS *////////

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <execution>  // For parallel algorithms
#include <chrono>
#include <random>

void demonstrate_parallel_algorithms() {
    std::cout << "\n=== PARALLEL ALGORITHMS (C++17) ===\n";
    
    // Create large dataset
    std::vector<int> data(1000000);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 1000);
    
    std::generate(data.begin(), data.end(), [&]() { return dis(gen); });
    
    // 1. Execution policies
    // std::execution::seq - sequential (default)
    // std::execution::par - parallel (may use multiple threads)
    // std::execution::par_unseq - parallel + vectorized (SIMD)
    
    auto time_algorithm = [&data](auto policy, const std::string& name) {
        auto start = std::chrono::high_resolution_clock::now();
        
        // Different parallel algorithms
        std::sort(policy, data.begin(), data.end());
        // Other parallel algorithms available:
        // std::for_each, std::transform, std::reduce, std::count_if, etc.
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << name << " sort took: " << duration.count() << "ms\n";
    };
    
    // Make a copy for fair comparison
    std::vector<int> data_copy = data;
    
    // Test different execution policies
    time_algorithm(std::execution::seq, "Sequential");
    
    data = data_copy;  // Reset data
    time_algorithm(std::execution::par, "Parallel");
    
    // 2. Parallel transform
    std::vector<int> source(1000000, 1);
    std::vector<int> destination(1000000);
    
    auto start = std::chrono::high_resolution_clock::now();
    
    std::transform(std::execution::par,
                   source.begin(), source.end(),
                   destination.begin(),
                   [](int x) { 
                       // Simulate some work
                       return x * x + 2 * x + 1; 
                   });
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Parallel transform took: " << duration.count() << "ms\n";
    
    // 3. Parallel reduce (like accumulate but parallel)
    std::vector<int> numbers(1000000);
    std::iota(numbers.begin(), numbers.end(), 1);  // 1, 2, 3, ..., 1000000
    
    start = std::chrono::high_resolution_clock::now();
    
    // Parallel sum
    long long parallel_sum = std::reduce(std::execution::par,
                                         numbers.begin(), numbers.end(),
                                         0LL);
    
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Parallel sum of 1..1000000 = " << parallel_sum 
              << " (took " << duration.count() << "ms)\n";
    
    // 4. Parallel for_each
    std::vector<double> values(1000000, 1.0);
    
    start = std::chrono::high_resolution_clock::now();
    
    std::for_each(std::execution::par,
                  values.begin(), values.end(),
                  [](double& x) {
                      // Apply some computation to each element
                      x = std::sin(x) + std::cos(x);
                  });
    
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Parallel for_each took: " << duration.count() << "ms\n";
    
    // 5. Important considerations:
    // - Avoid data races in parallel algorithms
    // - Operations must be associative and commutative for parallel reduce
    // - Some algorithms require random access iterators for parallel execution
    // - Exception handling: if any element throws, std::terminate is called
    
    // Example with potential data race (WRONG!)
    int shared_counter = 0;
    std::vector<int> items(1000, 1);
    
    // This has a data race - DON'T DO THIS!
    // std::for_each(std::execution::par, items.begin(), items.end(),
    //               [&](int) { ++shared_counter; });  // DATA RACE!
    
    // Correct way: use atomic or avoid sharing mutable state
    std::atomic<int> atomic_counter(0);
    std::for_each(std::execution::par, items.begin(), items.end(),
                  [&](int) { atomic_counter.fetch_add(1, std::memory_order_relaxed); });
    
    std::cout << "Atomic counter: " << atomic_counter.load() << "\n";
}