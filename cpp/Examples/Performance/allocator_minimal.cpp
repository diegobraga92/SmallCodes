#include <cstddef>
#include <new>

// Minimal STL-style allocator (educational)
template<typename T>
struct MinimalAllocator {
    using value_type = T;

    MinimalAllocator() = default;

    template<typename U>
    MinimalAllocator(const MinimalAllocator<U>&) {}

    T* allocate(std::size_t n) {
        // Allocate raw memory
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }

    void deallocate(T* p, std::size_t) noexcept {
        ::operator delete(p);
    }
};

template<typename T, typename U>
bool operator==(const MinimalAllocator<T>&, const MinimalAllocator<U>&) {
    return true;
}
