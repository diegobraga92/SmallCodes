/// Most useful allocator in practice

#include <vector>
#include <cstdlib>
#include <cstddef>
#include <cassert>

// Simple arena (monotonic) allocator
class ArenaAllocator {
public:
    explicit ArenaAllocator(std::size_t block_size = 4096)
        : block_size_(block_size) {
        allocate_block();
    }

    ~ArenaAllocator() {
        for (void* block : blocks_) {
            std::free(block);
        }
    }

    void* allocate(std::size_t size,
                   std::size_t alignment = alignof(std::max_align_t)) {
        std::size_t current =
            reinterpret_cast<std::size_t>(ptr_);
        std::size_t aligned =
            (current + alignment - 1) & ~(alignment - 1);

        if (aligned + size > reinterpret_cast<std::size_t>(end_)) {
            allocate_block();
            aligned = reinterpret_cast<std::size_t>(ptr_);
        }

        ptr_ = reinterpret_cast<char*>(aligned + size);
        return reinterpret_cast<void*>(aligned);
    }

    // Free all allocations at once
    void reset() {
        ptr_ = blocks_.front();
        end_ = ptr_ + block_size_;
    }

private:
    void allocate_block() {
        void* block = std::malloc(block_size_);
        assert(block && "Arena allocation failed");

        blocks_.push_back(static_cast<char*>(block));
        ptr_ = static_cast<char*>(block);
        end_ = ptr_ + block_size_;
    }

    std::vector<char*> blocks_;
    std::size_t block_size_;

    char* ptr_{nullptr};
    char* end_{nullptr};
};
