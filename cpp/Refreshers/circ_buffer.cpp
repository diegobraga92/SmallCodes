#include <vector>
#include <mutex>
#include <atomic>

template<typename T>
class RingBuffer {
private:
    std::vector<T> buffer_;
    size_t capacity_;
    std::atomic<size_t> head_{0};
    std::atomic<size_t> tail_{0};
    std::atomic<size_t> count_{0};
    mutable std::mutex mutex_;

public:
    explicit RingBuffer(size_t capacity) 
        : capacity_(capacity), buffer_(capacity) {}
    
    // Push element (overwrites oldest if full)
    bool push(T value) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (count_.load() == capacity_) {
            // Overwrite oldest element
            head_.store((head_.load() + 1) % capacity_);
            count_.fetch_sub(1);
        }
        
        buffer_[tail_.load()] = std::move(value);
        tail_.store((tail_.load() + 1) % capacity_);
        count_.fetch_add(1);
        return true;
    }
    
    // Try to pop element
    std::optional<T> pop() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (count_.load() == 0) {
            return std::nullopt;
        }
        
        T value = std::move(buffer_[head_.load()]);
        head_.store((head_.load() + 1) % capacity_);
        count_.fetch_sub(1);
        return value;
    }
    
    // Check if empty
    bool empty() const {
        return count_.load() == 0;
    }
    
    // Check if full
    bool full() const {
        return count_.load() == capacity_;
    }
    
    // Get size
    size_t size() const {
        return count_.load();
    }
    
    // Get capacity
    size_t capacity() const {
        return capacity_;
    }
};