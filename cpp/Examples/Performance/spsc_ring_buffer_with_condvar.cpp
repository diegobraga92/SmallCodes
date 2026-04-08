#include <thread>
#include <iostream>
#include <mutex>
#include <condition_variable>
#include <utility>
#include <cstddef>

// ==============================
constexpr size_t CACHE_LINE_SIZE = 64;

// ==============================
template<typename T, size_t Capacity>
class BlockingQueue {
    static_assert((Capacity & (Capacity - 1)) == 0,
                  "Capacity must be power of 2");

private:
    alignas(CACHE_LINE_SIZE) size_t head_ = 0;
    alignas(CACHE_LINE_SIZE) size_t tail_ = 0;

    alignas(CACHE_LINE_SIZE) T buffer_[Capacity];

    std::mutex m_;
    std::condition_variable cv_;

    static constexpr size_t MASK = Capacity - 1;

    size_t next(size_t i) const {
        return (i + 1) & MASK;
    }

public:
    void push(T&& item) {
        std::unique_lock<std::mutex> lock(m_);

        // Wait until not full
        cv_.wait(lock, [&] {
            return next(tail_) != head_;
        });

        buffer_[tail_] = std::move(item);
        tail_ = next(tail_);

        lock.unlock();      // reduce contention
        cv_.notify_one();   // wake consumer
    }

    void pop(T& item) {
        std::unique_lock<std::mutex> lock(m_);

        // Wait until not empty
        cv_.wait(lock, [&] {
            return head_ != tail_;
        });

        item = std::move(buffer_[head_]);
        head_ = next(head_);

        lock.unlock();
        cv_.notify_one();   // wake producer
    }
};

// ==============================
struct Request {
    int id;
    char payload[64];
};

BlockingQueue<Request, 1024> queue;
bool done = false;

// ==============================
void producer() {
    for (int i = 0; i < 100000; ++i) {
        queue.push(Request{i});
    }

    done = true;
}

// ==============================
void consumer() {
    Request req;

    while (!done) {
        queue.pop(req);

        // Simulate processing
        asm volatile("" ::: "memory");
    }
}

// ==============================
int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();
}