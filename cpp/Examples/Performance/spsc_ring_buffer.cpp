#include <atomic>
#include <thread>
#include <iostream>
#include <utility>
#include <cstddef>

// ==============================
// Cache line size (typical = 64 bytes)
constexpr size_t CACHE_LINE_SIZE = 64;

// ==============================
// Lock-free SPSC ring buffer
// ==============================
template<typename T, size_t Capacity>
class SPSCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0,
                  "Capacity must be power of 2 for fast modulo");

private:
    // Padding to avoid false sharing between head and tail
    alignas(CACHE_LINE_SIZE) std::atomic<size_t> head_{0};
    char pad1_[CACHE_LINE_SIZE - sizeof(std::atomic<size_t>)];

    alignas(CACHE_LINE_SIZE) std::atomic<size_t> tail_{0};
    char pad2_[CACHE_LINE_SIZE - sizeof(std::atomic<size_t>)];

    // Align buffer to cache line
    alignas(CACHE_LINE_SIZE) T buffer_[Capacity];

    // Use bitmask instead of modulo (faster)
    static constexpr size_t MASK = Capacity - 1;

    static size_t next(size_t i) noexcept {
        return (i + 1) & MASK;
    }

public:
    bool push(T&& item) {
        size_t tail = tail_.load(std::memory_order_relaxed);
        size_t next_tail = next(tail);

        // Acquire ensures visibility of consumer updates
        if (next_tail == head_.load(std::memory_order_acquire))
            return false; // full

        buffer_[tail] = std::move(item);

        // Release publishes the write
        tail_.store(next_tail, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        size_t head = head_.load(std::memory_order_relaxed);

        if (head == tail_.load(std::memory_order_acquire))
            return false; // empty

        item = std::move(buffer_[head]);

        head_.store(next(head), std::memory_order_release);
        return true;
    }
};

// ==============================
// Example request
// ==============================
struct Request {
    int id;
    // simulate non-trivial payload
    char payload[64];
};

SPSCQueue<Request, 1024> queue;
std::atomic<bool> done{false};

// ==============================
// Producer
// ==============================
void producer() {
    for (int i = 0; i < 100000; ++i) {
        Request req{i};

        while (!queue.push(std::move(req))) {
            // Busy-spin with hint
            std::this_thread::yield();
        }
    }

    done.store(true, std::memory_order_release);
}

// ==============================
// Consumer
// ==============================
void consumer() {
    Request req;

    while (!done.load(std::memory_order_acquire)) {
        if (queue.pop(req)) {
            // Simulate processing
            asm volatile("" ::: "memory"); // prevent over-optimization
        } else {
            std::this_thread::yield();
        }
    }

    // Drain remaining
    while (queue.pop(req)) {}
}

// ==============================
int main() {
    std::thread t1(producer);
    std::thread t2(consumer);

    t1.join();
    t2.join();
}