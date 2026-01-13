#include <vector>
#include <cstddef>
#include <cassert>

// Fixed-size object pool
template<typename T>
class PoolAllocator {
public:
    explicit PoolAllocator(std::size_t capacity)
        : storage_(capacity) {

        // Initialize free list
        for (std::size_t i = 0; i < capacity; ++i) {
            free_list_.push_back(&storage_[i]);
        }
    }

    // Allocate one object
    T* allocate() {
        if (free_list_.empty()) {
            return nullptr; // pool exhausted
        }

        T* obj = free_list_.back();
        free_list_.pop_back();
        return obj;
    }

    // Free one object
    void deallocate(T* obj) {
        free_list_.push_back(obj);
    }

    std::size_t free_count() const {
        return free_list_.size();
    }

private:
    std::vector<T>  storage_;    // actual storage
    std::vector<T*> free_list_;  // available objects
};
