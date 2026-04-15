#include <iostream>
#include <type_traits>
#include <vector>

// ---------- Version 1: Integral types ----------
template <typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
process(T value) {
    std::cout << "Integral version\n";
    return value * 2;
}

// ---------- Version 2: Floating point types ----------
template <typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
process(T value) {
    std::cout << "Floating point version\n";
    return value / 2;
}

// ---------- Version 3: Containers (vector-like) ----------
template <typename T>
typename std::enable_if<
    !std::is_arithmetic<T>::value,
    void
>::type
process(const T& container) {
    std::cout << "Container version\n";
    for (const auto& x : container) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}

// ---------- Main ----------
int main() {
    int a = 10;
    double b = 10.0;
    std::vector<int> v = {1, 2, 3};

    std::cout << process(a) << "\n";   // integral
    std::cout << process(b) << "\n";   // floating
    process(v);                        // container

    return 0;
}