#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <string>
#include <atomic>

class Logger {
public:
    Logger()
        : running_(true),
          worker_(&Logger::run, this) {}

    // Non-copyable
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    // Log a message (thread-safe, low contention)
    void log(std::string msg) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            queue_.push(std::move(msg));
        }
        cv_.notify_one();
    }

    // Graceful shutdown
    ~Logger() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            running_ = false;
        }
        cv_.notify_one();
        worker_.join();
    }

private:
    void run() {
        std::unique_lock<std::mutex> lock(mutex_);

        while (running_ || !queue_.empty()) {
            // Wait until there is data or shutdown
            cv_.wait(lock, [this] {
                return !queue_.empty() || !running_;
            });

            // Drain queue
            while (!queue_.empty()) {
                std::string msg = std::move(queue_.front());
                queue_.pop();

                // Release lock during I/O (critical for performance)
                lock.unlock();
                std::cout << msg << '\n';
                lock.lock();
            }
        }
    }

private:
    std::mutex mutex_;
    std::condition_variable cv_;
    std::queue<std::string> queue_;

    bool running_;
    std::thread worker_;
};

// Scales well