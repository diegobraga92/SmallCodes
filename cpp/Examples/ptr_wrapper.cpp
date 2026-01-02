// simple_unique_ptr.h
#ifndef SIMPLE_UNIQUE_PTR_H
#define SIMPLE_UNIQUE_PTR_H

#include <utility>   // std::exchange
#include <cstddef>   // std::nullptr_t

template<typename T>
class SimpleUniquePtr {
public:
    // constructors
    constexpr SimpleUniquePtr() noexcept : ptr_(nullptr) {}
    explicit SimpleUniquePtr(T* p) noexcept : ptr_(p) {}

    // move-only
    SimpleUniquePtr(SimpleUniquePtr&& other) noexcept : ptr_(std::exchange(other.ptr_, nullptr)) {}
    SimpleUniquePtr& operator=(SimpleUniquePtr&& other) noexcept {
        if (this != &other) {
            reset(std::exchange(other.ptr_, nullptr));
        }
        return *this;
    }
    SimpleUniquePtr(const SimpleUniquePtr&) = delete;
    SimpleUniquePtr& operator=(const SimpleUniquePtr&) = delete;

    // destructor
    ~SimpleUniquePtr() { delete ptr_; }

    // dereference
    T& operator*() const { return *ptr_; }
    T* operator->() const noexcept { return ptr_; }

    // modifiers / observers
    T* get() const noexcept { return ptr_; }
    explicit operator bool() const noexcept { return ptr_ != nullptr; }

    // release ownership (caller must delete)
    T* release() noexcept { return std::exchange(ptr_, nullptr); }

    // delete managed object and take new pointer (default null)
    void reset(T* p = nullptr) noexcept {
        T* old = std::exchange(ptr_, p);
        if (old) delete old;
    }

    // swap
    void swap(SimpleUniquePtr& other) noexcept { std::swap(ptr_, other.ptr_); }

private:
    T* ptr_;
};

// convenience helper like std::make_unique for single objects
template<typename T, typename... Args>
SimpleUniquePtr<T> make_simple_unique(Args&&... args) {
    return SimpleUniquePtr<T>(new T(std::forward<Args>(args)...));
}

#endif // SIMPLE_UNIQUE_PTR_H