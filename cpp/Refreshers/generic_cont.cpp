// tiny_vec.h — a tiny generic container
#ifndef TINY_VEC_H
#define TINY_VEC_H

#include <cstddef>   // std::size_t
#include <utility>   // std::move, std::swap
#include <algorithm> // std::min

template<typename T>
class TinyVec {
public:
    TinyVec() noexcept : data_(nullptr), sz_(0), cap_(0) {}
    ~TinyVec() { delete[] data_; }

    // move-only (simple)
    TinyVec(TinyVec&& o) noexcept : data_(o.data_), sz_(o.sz_), cap_(o.cap_) {
        o.data_ = nullptr; o.sz_ = o.cap_ = 0;
    }
    TinyVec& operator=(TinyVec&& o) noexcept {
        if (this != &o) {
            delete[] data_;
            data_ = o.data_; sz_ = o.sz_; cap_ = o.cap_;
            o.data_ = nullptr; o.sz_ = o.cap_ = 0;
        }
        return *this;
    }
    TinyVec(const TinyVec&) = delete;
    TinyVec& operator=(const TinyVec&) = delete;

    // basics
    std::size_t size() const noexcept { return sz_; }
    std::size_t capacity() const noexcept { return cap_; }
    bool empty() const noexcept { return sz_ == 0; }

    T& operator[](std::size_t i) noexcept { return data_[i]; }
    const T& operator[](std::size_t i) const noexcept { return data_[i]; }

    void push_back(const T& v) {
        ensure_space();
        data_[sz_++] = v;
    }
    void push_back(T&& v) {
        ensure_space();
        data_[sz_++] = std::move(v);
    }
    void pop_back() noexcept { if (sz_) --sz_; }

    void clear() noexcept { sz_ = 0; }

    void reserve(std::size_t new_cap) {
        if (new_cap <= cap_) return;
        T* new_data = new T[new_cap];
        for (std::size_t i = 0; i < sz_; ++i) new_data[i] = std::move(data_[i]);
        delete[] data_;
        data_ = new_data;
        cap_ = new_cap;
    }

private:
    void ensure_space() {
        if (sz_ < cap_) return;
        std::size_t newcap = (cap_ == 0) ? 1 : cap_ * 2;
        reserve(newcap);
    }

    T* data_;
    std::size_t sz_;
    std::size_t cap_;
};

#endif // TINY_VEC_H
