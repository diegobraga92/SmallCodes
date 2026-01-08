#include <vector>
#include <mutex>
#include <condition_variable>

template<typename T>
class BoundedBuffer {
public:
    explicit BoundedBuffer(std::size_t capacity)
        : capacity_(capacity) {}

    // Producer operation
    void put(T value) {
        std::unique_lock<std::mutex> lock(mtx_);

        // Wait until buffer is not full
        not_full_.wait(lock, [this] {
            return buffer_.size() < capacity_;
        });

        buffer_.push_back(std::move(value));

        // Signal that buffer is no longer empty
        not_empty_.notify_one();
    }

    // Consumer operation
    T get() {
        std::unique_lock<std::mutex> lock(mtx_);

        // Wait until buffer is not empty
        not_empty_.wait(lock, [this] {
            return !buffer_.empty();
        });

        T value = std::move(buffer_.front());
        buffer_.erase(buffer_.begin());

        // Signal that buffer is no longer full
        not_full_.notify_one();

        return value;
    }

private:
    std::mutex mtx_;                      // Monitor lock
    std::condition_variable not_full_;    // Condition: buffer has space
    std::condition_variable not_empty_;   // Condition: buffer has data

    std::vector<T> buffer_;               // Shared state (protected)
    const std::size_t capacity_;
};


/* USAGE
#include <thread>
#include <iostream>

BoundedBuffer<int> buffer(4);

void producer() {
    for (int i = 0; i < 10; ++i) {
        buffer.put(i);
        std::cout << "Produced " << i << "\n";
    }
}

void consumer() {
    for (int i = 0; i < 10; ++i) {
        int v = buffer.get();
        std::cout << "Consumed " << v << "\n";
    }
}

int main() {
    std::thread p(producer);
    std::thread c(consumer);

    p.join();
    c.join();
}

*/