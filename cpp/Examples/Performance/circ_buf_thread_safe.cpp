//// Keeps a fixed-size array, head index, tail index

#include <vector>
#include <mutex>
#include <condition_variable>
#include <optional>

template <typename T>
class ThreadSafeCircularBuffer {
public:
    explicit ThreadSafeCircularBuffer(std::size_t capacity)
        : buffer_(capacity), capacity_(capacity) {}

    ThreadSafeCircularBuffer(const ThreadSafeCircularBuffer&) = delete;
    ThreadSafeCircularBuffer& operator=(const ThreadSafeCircularBuffer&) = delete;

    // Producer: blocks if buffer is full
    // Returns false if buffer is closed
    bool push(T value) {
        std::unique_lock<std::mutex> lock(mutex_);

        not_full_.wait(lock, [this] {
            return count_ < capacity_ || closed_;
        });

        if (closed_) {
            return false;
        }

        buffer_[tail_] = std::move(value);
        tail_ = (tail_ + 1) % capacity_;
        ++count_;

        not_empty_.notify_one();
        return true;
    }

    // Consumer: blocks if buffer is empty
    // Returns std::nullopt if buffer is closed and empty
    std::optional<T> pop() {
        std::unique_lock<std::mutex> lock(mutex_);

        not_empty_.wait(lock, [this] {
            return count_ > 0 || closed_;
        });

        if (count_ == 0) {
            return std::nullopt; // closed and empty
        }

        T value = std::move(buffer_[head_]);
        head_ = (head_ + 1) % capacity_;
        --count_;

        not_full_.notify_one();
        return value;
    }

    // Close the buffer (wakes all waiting threads)
    void close() {
        std::lock_guard<std::mutex> lock(mutex_);
        closed_ = true;
        not_empty_.notify_all();
        not_full_.notify_all();
    }

    std::size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_;
    }

    std::size_t capacity() const {
        return capacity_;
    }

private:
    std::vector<T> buffer_;
    const std::size_t capacity_;

    std::size_t head_{0};
    std::size_t tail_{0};
    std::size_t count_{0};

    bool closed_{false};

    mutable std::mutex mutex_;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
};

//// No Data Races

/* USAGE
#include <thread>
#include <iostream>

ThreadSafeCircularBuffer<int> buffer(4);

void producer() {
    for (int i = 0; i < 10; ++i) {
        buffer.push(i);
    }
    buffer.close();
}

void consumer() {
    while (true) {
        auto item = buffer.pop();
        if (!item) break;
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