// Compare and Swap

#include <atomic>

class AtomicCounterCAS {
public:
    int increment() noexcept {
        int old = value_.load(std::memory_order_relaxed);
        while (!value_.compare_exchange_weak(
            old, old + 1,
            std::memory_order_relaxed,
            std::memory_order_relaxed)) {
            // 'old' is updated with the current value automatically
        }
        return old + 1;
    }

    int get() const noexcept {
        return value_.load(std::memory_order_relaxed);
    }

private:
    std::atomic<int> value_{0};
};
