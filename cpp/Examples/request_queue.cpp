// [ Producers ] → [ Bounded Queue ] → [ Worker Thread Pool ] → [ Response ]

#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <atomic>
#include <chrono>

// =======================
// Configuration
// =======================
constexpr size_t MAX_QUEUE_SIZE = 10;
constexpr int NUM_WORKERS = 4;

// =======================
// Request definition
// =======================
struct Request {
    int id;
};

// =======================
// Shared state
// =======================
std::mutex mtx;
std::condition_variable cv_not_empty;
std::condition_variable cv_not_full;

std::queue<Request> queue;
bool shutting_down = false;

// =======================
// Worker thread function
// =======================
void worker_thread(int worker_id) {
    while (true) {
        Request req;

        {
            std::unique_lock<std::mutex> lock(mtx);

            // Wait until work is available or shutdown requested
            cv_not_empty.wait(lock, [] {
                return !queue.empty() || shutting_down;
            });

            // Exit condition
            if (shutting_down && queue.empty())
                return;

            req = queue.front();
            queue.pop();

            // Signal that queue has space
            cv_not_full.notify_one();
        }

        // ---- Process request outside lock ----
        std::cout << "[Worker " << worker_id
                  << "] Processing request " << req.id << "\n";

        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        std::cout << "[Worker " << worker_id
                  << "] Finished request " << req.id << "\n";
    }
}

// =======================
// Producer (request submitter)
// =======================
void submit_request(Request req) {
    std::unique_lock<std::mutex> lock(mtx);

    // Backpressure: wait until queue has space
    cv_not_full.wait(lock, [] {
        return queue.size() < MAX_QUEUE_SIZE || shutting_down;
    });

    if (shutting_down)
        return;

    queue.push(req);
    cv_not_empty.notify_one();
}

// =======================
// Main
// =======================
int main() {
    // Start worker pool
    std::vector<std::thread> workers;
    for (int i = 0; i < NUM_WORKERS; ++i)
        workers.emplace_back(worker_thread, i);

    // Simulate incoming requests
    for (int i = 1; i <= 25; ++i) {
        submit_request(Request{i});
        std::cout << "[Main] Submitted request " << i << "\n";
    }

    // Graceful shutdown
    {
        std::lock_guard<std::mutex> lock(mtx);
        shutting_down = true;
    }

    cv_not_empty.notify_all();
    cv_not_full.notify_all();

    for (auto& t : workers)
        t.join();

    std::cout << "All requests processed. Shutdown complete.\n";
    return 0;
}
