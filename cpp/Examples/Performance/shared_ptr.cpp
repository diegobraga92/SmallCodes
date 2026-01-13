#include <cstddef>

template<typename T>
struct ControlBlock {
    T* ptr;
    std::size_t ref_count;

    explicit ControlBlock(T* p)
        : ptr(p), ref_count(1) {}
};


#include <utility>
#include <cassert>

template<typename T>
class SharedPtr {
public:
    // Default constructor (empty)
    SharedPtr() noexcept = default;

    // Construct from raw pointer
    explicit SharedPtr(T* ptr)
        : control_(ptr ? new ControlBlock<T>(ptr) : nullptr) {}

    // Copy constructor
    SharedPtr(const SharedPtr& other) noexcept
        : control_(other.control_) {
        increment();
    }

    // Move constructor
    SharedPtr(SharedPtr&& other) noexcept
        : control_(other.control_) {
        other.control_ = nullptr;
    }

    // Copy assignment
    SharedPtr& operator=(const SharedPtr& other) noexcept {
        if (this != &other) {
            release();
            control_ = other.control_;
            increment();
        }
        return *this;
    }

    // Move assignment
    SharedPtr& operator=(SharedPtr&& other) noexcept {
        if (this != &other) {
            release();
            control_ = other.control_;
            other.control_ = nullptr;
        }
        return *this;
    }

    // Destructor
    ~SharedPtr() {
        release();
    }

    // Observers
    T* get() const noexcept {
        return control_ ? control_->ptr : nullptr;
    }

    T& operator*() const noexcept {
        assert(get());
        return *get();
    }

    T* operator->() const noexcept {
        return get();
    }

    std::size_t use_count() const noexcept {
        return control_ ? control_->ref_count : 0;
    }

    explicit operator bool() const noexcept {
        return get() != nullptr;
    }

private:
    ControlBlock<T>* control_{nullptr};

    void increment() noexcept {
        if (control_) {
            ++control_->ref_count;
        }
    }

    void release() noexcept {
        if (!control_) return;

        if (--control_->ref_count == 0) {
            delete control_->ptr;
            delete control_;
        }
        control_ = nullptr;
    }
};
