#include <memory>

template<typename T>
T max(T a, T b) {
    if (a >= b) return a;
    else return b;
}

template<typename T>
class Container {
public:
    T item;

private:
    Container(T i): item(i) {}

    T get() {return item; }
};

void main() {
    auto c = std::make_unique<Container<int>>(30);
}

// Variadic templates, T is the first argument, and Rest the rest
template <typename T, typename... Rest>
void print(const T& value, const Rest&... rest) {
    std::cout << value << " ";
    print(rest...);  // recursive expansion
}

// SFINAE are ways to limit template usage to prevent compile errors:
// Method 1: Using enable_if
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
process(T value) {
    std::cout << "Processing integral: " << value << std::endl;
    return value * 2;
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
process(T value) {
    std::cout << "Processing floating point: " << value << std::endl;
    return value * 1.5;
}

// Method 2: Using return type deduction with decltype
template<typename T>
auto process_string(T value) -> decltype(std::declval<T>().length(), void()) {
    std::cout << "Processing string-like with length: " << value.length() << std::endl;
}