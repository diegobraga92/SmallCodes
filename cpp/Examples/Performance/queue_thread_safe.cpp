#include <queue>
#include <mutex>
#include <condition_variable>
#include <optional>

template <typename T>
class ThreadSafeQueue {
public:
    ThreadSafeQueue() = default;

    // Disable copying (queues are shared state)
    ThreadSafeQueue(const ThreadSafeQueue&) = delete;
    ThreadSafeQueue& operator=(const ThreadSafeQueue&) = delete;

    // Producer: push an item
    void push(T value) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            queue_.push(std::move(value));
        }
        // Notify AFTER releasing the lock. Only one consumer, not all
        cv_.notify_one();
    }

    // Consumer: blocking pop
    // Returns std::nullopt if queue is closed
    std::optional<T> pop() {
        std::unique_lock<std::mutex> lock(mutex_);

        // Wait until:
        //  - queue is not empty OR
        //  - queue is closed
        cv_.wait(lock, [this] {
            return !queue_.empty() || closed_;
        });

        if (queue_.empty()) {
            // Must be closed
            return std::nullopt;
        }

        T value = std::move(queue_.front());
        queue_.pop();
        return value;
    }

    // Signal no more data will arrive
    void close() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            closed_ = true;
        }
        cv_.notify_all();
    }

private:
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;
    bool closed_{false};
};

/* USAGE:
#include <thread>
#include <iostream>

ThreadSafeQueue<int> queue;

void producer() {
    for (int i = 0; i < 10; ++i) {
        queue.push(i);
    }
    queue.close(); // signal end
}

void consumer() {
    while (true) {
        auto item = queue.pop();
        if (!item) {
            break; // queue closed and empty
        }
        std::cout << "Consumed: " << *item << "\n";
    }
}

int main() {
    std::thread p(producer);
    std::thread c(consumer);

    p.join();
    c.join();
}
*/
