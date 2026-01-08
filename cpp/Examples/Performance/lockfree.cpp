// Uses atomic read-modify-write (RMW)

#include <atomic>

class AtomicCounter {
public:
    AtomicCounter() = default;
    explicit AtomicCounter(int initial) : value_(initial) {}

    // Increment and return new value
    int increment() noexcept {
        return value_.fetch_add(1) + 1;
    }

    // Decrement and return new value
    int decrement() noexcept {
        return value_.fetch_sub(1) - 1;
    }

    int get() const noexcept {
        return value_.load();
    }

private:
    std::atomic<int> value_{0};
};



// MEMORY ORDERING

#include <thread>
#include <vector>
#include <iostream>

int main() {
    AtomicCounter counter;

    constexpr int threads = 4;
    constexpr int iters = 1'000'000;

    std::vector<std::thread> workers;

    for (int i = 0; i < threads; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < iters; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : workers) {
        t.join();
    }

    std::cout << "Final value = " << counter.get() << "\n";
}