////////* TYPE TRAITS & TEMPLATE METAPROGRAMMING *////////

/*
 * TEMPLATE METAPROGRAMMING - Compile-time computation
 * 
 * Template metaprogramming uses templates to:
 *   - Compute values at compile-time (no runtime cost!)
 *   - Generate code based on types
 *   - Enable/disable code based on type properties
 *   - Create type-safe, zero-overhead abstractions
 * 
 * Key tools:
 *   - Type traits: Query type properties
 *   - SFINAE: Substitution Failure Is Not An Error
 *   - Constexpr: Compile-time evaluation (C++11+)
 *   - Concepts: Constrain templates (C++20)
 */

#include <iostream>
#include <type_traits>
#include <concepts>
#include <vector>
#include <string>

// ============================================================================
// 1. TYPE TRAITS BASICS (std::is_*, std::enable_if, etc.)
// ============================================================================

/*
 * Type traits query type properties at compile-time:
 *   - std::is_integral<T>: Is T an integer type?
 *   - std::is_floating_point<T>: Is T a floating-point type?
 *   - std::is_pointer<T>: Is T a pointer?
 *   - std::is_same<T, U>: Are T and U the same type?
 *   - std::is_const<T>: Is T const-qualified?
 * 
 * Returns: std::true_type or std::false_type
 * Use: ::value for bool result, or _v shorthand (C++17)
 */

void demonstrate_type_traits_basics() {
    std::cout << "=== TYPE TRAITS BASICS ===\n\n";
    
    // Primary type categories
    std::cout << "Primary categories:\n";
    std::cout << "  int is integral: " << std::is_integral_v<int> << "\n";
    std::cout << "  double is integral: " << std::is_integral_v<double> << "\n";
    std::cout << "  double is floating point: " << std::is_floating_point_v<double> << "\n";
    std::cout << "  int* is pointer: " << std::is_pointer_v<int*> << "\n";
    std::cout << "  int is pointer: " << std::is_pointer_v<int> << "\n";
    
    // Type comparisons
    std::cout << "\nType comparisons:\n";
    std::cout << "  int == int: " << std::is_same_v<int, int> << "\n";
    std::cout << "  int == long: " << std::is_same_v<int, long> << "\n";
    std::cout << "  int == const int: " << std::is_same_v<int, const int> << "\n";
    
    // Type properties
    std::cout << "\nType properties:\n";
    std::cout << "  const int is const: " << std::is_const_v<const int> << "\n";
    std::cout << "  int is const: " << std::is_const_v<int> << "\n";
    std::cout << "  string is class: " << std::is_class_v<std::string> << "\n";
    std::cout << "  int is class: " << std::is_class_v<int> << "\n";
}

// ============================================================================
// 2. TYPE TRANSFORMATIONS (std::remove_*, std::add_*, etc.)
// ============================================================================

/*
 * Type transformations modify types at compile-time:
 *   - std::remove_const<T>: Remove const qualifier
 *   - std::remove_reference<T>: Remove reference
 *   - std::add_pointer<T>: Add pointer
 *   - std::decay<T>: Convert to value type (remove ref/const/volatile)
 * 
 * Access result: typename TraitName<T>::type, or _t shorthand (C++14)
 */

void demonstrate_type_transformations() {
    std::cout << "\n=== TYPE TRANSFORMATIONS ===\n\n";
    
    using T1 = const int;
    using T2 = std::remove_const_t<T1>;  // int
    
    std::cout << "const int -> remove_const: ";
    std::cout << std::is_same_v<T2, int> << " (should be 1)\n";
    
    using T3 = int&;
    using T4 = std::remove_reference_t<T3>;  // int
    
    std::cout << "int& -> remove_reference: ";
    std::cout << std::is_same_v<T4, int> << " (should be 1)\n";
    
    using T5 = const int&;
    using T6 = std::decay_t<T5>;  // int (removes const, ref, volatile)
    
    std::cout << "const int& -> decay: ";
    std::cout << std::is_same_v<T6, int> << " (should be 1)\n";
    
    // Pointer manipulation
    using T7 = int;
    using T8 = std::add_pointer_t<T7>;  // int*
    using T9 = std::remove_pointer_t<T8>;  // int
    
    std::cout << "int -> add_pointer -> remove_pointer: ";
    std::cout << std::is_same_v<T9, int> << " (should be 1)\n";
}

// ============================================================================
// 3. SFINAE (Substitution Failure Is Not An Error)
// ============================================================================

/*
 * SFINAE: When template substitution fails, don't error - just remove candidate
 * 
 * Use cases:
 *   - Function overloading based on type properties
 *   - Enable/disable functions for certain types
 *   - Type-based dispatch
 * 
 * Modern alternatives: if constexpr (C++17), concepts (C++20)
 */

// Example 1: std::enable_if - Enable function only for integral types
template<typename T>
typename std::enable_if_t<std::is_integral_v<T>, T>
add_one(T value) {
    return value + 1;
}

// Example 2: std::enable_if in template parameter - Enable for floating-point
template<typename T, typename = std::enable_if_t<std::is_floating_point_v<T>>>
T add_one_float(T value) {
    return value + 1.0;
}

// Example 3: SFINAE with decltype - Check if type has member function
template<typename T>
auto has_size_method(T t) -> decltype(t.size(), std::true_type{}) {
    return std::true_type{};
}

std::false_type has_size_method(...) {
    return std::false_type{};
}

void demonstrate_sfinae() {
    std::cout << "\n=== SFINAE ===\n\n";
    
    std::cout << "add_one(5) = " << add_one(5) << " (works with int)\n";
    std::cout << "add_one_float(3.14) = " << add_one_float(3.14) << " (works with double)\n";
    
    // These would fail to compile:
    // add_one(3.14);  // Error: double is not integral
    // add_one_float(5);  // Error: int is not floating-point
    
    std::cout << "\nhas_size_method:\n";
    std::cout << "  vector: " << decltype(has_size_method(std::vector<int>{}))::value << "\n";
    std::cout << "  int: " << decltype(has_size_method(5))::value << "\n";
    
    std::cout << "\nSFINAE enables compile-time function overload resolution!\n";
}

// ============================================================================
// 4. CONSTEXPR METAPROGRAMMING (C++11+)
// ============================================================================

/*
 * constexpr: Evaluate at compile-time
 *   - C++11: constexpr functions (limited)
 *   - C++14: Relaxed constexpr (loops, locals)
 *   - C++17: constexpr if
 *   - C++20: constexpr virtual, constexpr vector
 * 
 * Benefits:
 *   - Zero runtime cost
 *   - Type-safe
 *   - Easier to read than template recursion
 */

// Example 1: Compile-time factorial
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

// Example 2: Compile-time string length
constexpr std::size_t strlen_constexpr(const char* str) {
    std::size_t len = 0;
    while (str[len] != '\0') {
        ++len;
    }
    return len;
}

// Example 3: constexpr if (C++17) - Compile-time branching
template<typename T>
auto get_value(T t) {
    if constexpr (std::is_pointer_v<T>) {
        return *t;  // Dereference pointers
    } else {
        return t;   // Return value types directly
    }
}

void demonstrate_constexpr() {
    std::cout << "\n=== CONSTEXPR METAPROGRAMMING ===\n\n";
    
    // Computed at compile-time!
    constexpr int fact5 = factorial(5);
    constexpr std::size_t len = strlen_constexpr("Hello");
    
    std::cout << "factorial(5) = " << fact5 << " (compile-time)\n";
    std::cout << "strlen(\"Hello\") = " << len << " (compile-time)\n";
    
    // constexpr if example
    int value = 42;
    int* ptr = &value;
    
    std::cout << "\nget_value(42) = " << get_value(42) << "\n";
    std::cout << "get_value(&42) = " << get_value(ptr) << "\n";
    
    std::cout << "\nconstexpr advantages:\n";
    std::cout << "  - Zero runtime cost\n";
    std::cout << "  - More readable than template recursion\n";
    std::cout << "  - Can use normal C++ control flow\n";
}

// ============================================================================
// 5. TEMPLATE TEMPLATE PARAMETERS
// ============================================================================

/*
 * Template template parameters: Templates that take templates as arguments
 * 
 * Syntax: template<template<typename> class Container>
 * 
 * Use cases:
 *   - Generic algorithms that work with any container
 *   - Type-generic wrappers
 */

// Example: Function that works with any container type
template<template<typename, typename> class Container>
void print_container_type() {
    if constexpr (std::is_same_v<Container<int, std::allocator<int>>, std::vector<int>>) {
        std::cout << "Container is vector\n";
    } else {
        std::cout << "Container is something else\n";
    }
}

// Example: Generic container wrapper
template<typename T, template<typename> class Container>
class GenericWrapper {
private:
    Container<T> data;
    
public:
    void add(T value) {
        data.push_back(value);
    }
    
    std::size_t size() const {
        return data.size();
    }
};

void demonstrate_template_template_parameters() {
    std::cout << "\n=== TEMPLATE TEMPLATE PARAMETERS ===\n\n";
    
    print_container_type<std::vector>();
    
    std::cout << "\nTemplate template parameters allow:\n";
    std::cout << "  - Generic algorithms over container types\n";
    std::cout << "  - Type-generic wrappers\n";
    std::cout << "  - Policy-based design\n";
}

// ============================================================================
// 6. TYPE LISTS & TUPLE METAPROGRAMMING
// ============================================================================

/*
 * Type lists: Compile-time lists of types
 * 
 * Use std::tuple for type lists:
 *   - std::tuple_element: Get Nth type
 *   - std::tuple_size: Get number of types
 * 
 * Use cases:
 *   - Type-based dispatch
 *   - Compile-time type selection
 */

// Get first type from tuple
template<typename Tuple>
using first_type_t = std::tuple_element_t<0, Tuple>;

// Get size of tuple
template<typename Tuple>
constexpr std::size_t tuple_size_v = std::tuple_size_v<Tuple>;

// Check if type is in tuple
template<typename T, typename Tuple>
struct contains;

template<typename T>
struct contains<T, std::tuple<>> : std::false_type {};

template<typename T, typename U, typename... Rest>
struct contains<T, std::tuple<U, Rest...>> 
    : contains<T, std::tuple<Rest...>> {};

template<typename T, typename... Rest>
struct contains<T, std::tuple<T, Rest...>> : std::true_type {};

template<typename T, typename Tuple>
constexpr bool contains_v = contains<T, Tuple>::value;

void demonstrate_type_lists() {
    std::cout << "\n=== TYPE LISTS & TUPLE METAPROGRAMMING ===\n\n";
    
    using MyTypes = std::tuple<int, double, std::string>;
    
    std::cout << "Tuple contains 3 types: int, double, string\n";
    std::cout << "  Size: " << tuple_size_v<MyTypes> << "\n";
    std::cout << "  First type is int: " << std::is_same_v<first_type_t<MyTypes>, int> << "\n";
    std::cout << "  Contains int: " << contains_v<int, MyTypes> << "\n";
    std::cout << "  Contains float: " << contains_v<float, MyTypes> << "\n";
}

// ============================================================================
// 7. PRACTICAL EXAMPLE: COMPILE-TIME UNIT SYSTEM
// ============================================================================

/*
 * Real-world example: Type-safe units at compile-time
 *   - No runtime overhead
 *   - Catch dimension errors at compile-time
 *   - Example: meters + seconds = compile error!
 */

template<int M, int S>  // M = meters, S = seconds
struct Unit {
    double value;
    
    constexpr Unit(double v) : value(v) {}
    
    // Addition: Same dimensions required
    constexpr Unit operator+(Unit other) const {
        return Unit(value + other.value);
    }
    
    // Multiplication: Dimensions add
    template<int M2, int S2>
    constexpr Unit<M + M2, S + S2> operator*(Unit<M2, S2> other) const {
        return Unit<M + M2, S + S2>(value * other.value);
    }
    
    // Division: Dimensions subtract
    template<int M2, int S2>
    constexpr Unit<M - M2, S - S2> operator/(Unit<M2, S2> other) const {
        return Unit<M - M2, S - S2>(value / other.value);
    }
};

// Convenient type aliases
using Meters = Unit<1, 0>;
using Seconds = Unit<0, 1>;
using MetersPerSecond = Unit<1, -1>;
using MetersPerSecondSquared = Unit<1, -2>;

void demonstrate_unit_system() {
    std::cout << "\n=== COMPILE-TIME UNIT SYSTEM ===\n\n";
    
    constexpr Meters distance(100.0);
    constexpr Seconds time(10.0);
    
    // Velocity = distance / time
    constexpr MetersPerSecond velocity = distance / time;
    std::cout << "Velocity = 100m / 10s = " << velocity.value << " m/s\n";
    
    // Acceleration = velocity / time
    constexpr MetersPerSecondSquared acceleration = velocity / time;
    std::cout << "Acceleration = 10 m/s / 10s = " << acceleration.value << " m/s²\n";
    
    // This would fail at compile-time:
    // auto invalid = distance + time;  // Error: Can't add meters + seconds!
    
    std::cout << "\nType-safe units at compile-time:\n";
    std::cout << "  - Zero runtime overhead\n";
    std::cout << "  - Catch dimension errors at compile-time\n";
    std::cout << "  - Self-documenting code\n";
}

// ============================================================================
// 8. C++20 CONCEPTS (Modern alternative to SFINAE)
// ============================================================================

/*
 * Concepts (C++20): Named constraints on template parameters
 * 
 * Benefits over SFINAE:
 *   - Clearer syntax
 *   - Better error messages
 *   - Can be composed
 * 
 * Standard concepts:
 *   - std::integral, std::floating_point
 *   - std::same_as, std::convertible_to
 *   - std::copyable, std::movable
 */

// Define custom concept
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// Use concept as constraint
template<Numeric T>
T add_two(T value) {
    return value + 2;
}

// Concept in requires clause
template<typename T>
requires std::integral<T>
T multiply_by_three(T value) {
    return value * 3;
}

// Compound concept
template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

template<Addable T>
T add_generic(T a, T b) {
    return a + b;
}

void demonstrate_concepts() {
    std::cout << "\n=== C++20 CONCEPTS ===\n\n";
    
    std::cout << "add_two(5) = " << add_two(5) << "\n";
    std::cout << "add_two(3.14) = " << add_two(3.14) << "\n";
    std::cout << "multiply_by_three(7) = " << multiply_by_three(7) << "\n";
    std::cout << "add_generic(10, 20) = " << add_generic(10, 20) << "\n";
    
    // These would give clear error messages:
    // add_two("hello");  // Error: "hello" does not satisfy Numeric
    // multiply_by_three(3.14);  // Error: double is not integral
    
    std::cout << "\nConcepts advantages:\n";
    std::cout << "  - Clearer syntax than SFINAE\n";
    std::cout << "  - Better error messages\n";
    std::cout << "  - Self-documenting constraints\n";
}

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

int main() {
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║    TYPE TRAITS & TEMPLATE METAPROGRAMMING DEMONSTRATION  ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n\n";
    
    demonstrate_type_traits_basics();
    demonstrate_type_transformations();
    demonstrate_sfinae();
    demonstrate_constexpr();
    demonstrate_template_template_parameters();
    demonstrate_type_lists();
    demonstrate_unit_system();
    demonstrate_concepts();
    
    std::cout << "\n=== SUMMARY ===\n\n";
    std::cout << "Type Traits: Query type properties at compile-time\n";
    std::cout << "SFINAE: Enable/disable overloads based on types\n";
    std::cout << "Constexpr: Compile-time evaluation\n";
    std::cout << "Concepts: Modern type constraints (C++20)\n";
    
    return 0;
}

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/*
 * 1. TYPE TRAITS:
 *    - Query type properties: is_integral, is_pointer, is_same
 *    - Transform types: remove_const, add_pointer, decay
 *    - Use _v suffix for values, _t suffix for types (C++14/17)
 * 
 * 2. SFINAE (Substitution Failure Is Not An Error):
 *    - Enable/disable functions based on type properties
 *    - std::enable_if for conditional compilation
 *    - decltype for detecting member functions
 *    - Modern alternative: concepts (C++20)
 * 
 * 3. CONSTEXPR:
 *    - Compile-time evaluation (zero runtime cost!)
 *    - C++11: Simple functions
 *    - C++14: Loops, locals
 *    - C++17: constexpr if (compile-time branching)
 *    - C++20: Richer constexpr (virtual, containers)
 * 
 * 4. TEMPLATE METAPROGRAMMING PATTERNS:
 *    - Type lists: std::tuple for compile-time type containers
 *    - Template template parameters: Templates taking templates
 *    - Recursive templates: Compile-time iteration
 *    - Tag dispatch: Select overload by type
 * 
 * 5. PRACTICAL APPLICATIONS:
 *    - Type-safe units (meters, seconds)
 *    - Compile-time string hashing
 *    - Expression templates (Eigen, Blaze)
 *    - Type-based dispatch
 *    - Zero-cost abstractions
 * 
 * 6. C++20 CONCEPTS:
 *    - Named constraints on templates
 *    - Better than SFINAE: clearer syntax, better errors
 *    - Standard concepts: integral, floating_point, copyable
 *    - Custom concepts with requires
 * 
 * 7. BEST PRACTICES:
 *    - Prefer concepts over SFINAE (C++20+)
 *    - Use constexpr for compile-time computation
 *    - Keep metaprogramming simple (readability matters!)
 *    - Use standard type traits (don't reinvent)
 * 
 * 8. WHEN TO USE:
 *    - Generic libraries (need type flexibility)
 *    - Performance critical (compile-time = zero runtime cost)
 *    - Type safety (catch errors at compile-time)
 *    - Zero-cost abstractions
 * 
 * Template metaprogramming is a powerful tool for:
 *   - Generic programming
 *   - Zero-overhead abstractions
 *   - Type-safe APIs
 *   - Compile-time error checking
 * 
 * Master this and you can create elegant, efficient, type-safe libraries!
 */
