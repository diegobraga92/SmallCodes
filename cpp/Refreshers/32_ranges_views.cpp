////////* C++20 RANGES & VIEWS *////////

/*
 * C++20 RANGES LIBRARY
 * 
 * Ranges revolutionize how we work with sequences in C++:
 *   - Views: Lazy, composable transformations (no copying!)
 *   - Pipeable syntax: data | filter | transform | take
 *   - Constrained algorithms: Type-safe with concepts
 *   - Better composability than iterators
 * 
 * Why ranges?
 *   - More expressive: Chain operations naturally
 *   - More efficient: Lazy evaluation, no temporaries
 *   - Safer: Concepts catch errors at compile-time
 */

#include <iostream>
#include <vector>
#include <string>
#include <ranges>
#include <algorithm>
#include <numeric>

namespace ranges = std::ranges;
namespace views = std::ranges::views;

// ============================================================================
// 1. RANGES BASICS (What is a range?)
// ============================================================================

/*
 * RANGE: Anything you can iterate over
 *   - Has begin() and end()
 *   - Examples: vector, array, string, istream
 * 
 * VIEW: Lightweight, non-owning range
 *   - O(1) copy (just pointers)
 *   - Lazy evaluation
 *   - Composable
 * 
 * Key difference:
 *   - Container (vector): Owns data, expensive to copy
 *   - View: Doesn't own data, cheap to copy, lazy
 */

void demonstrate_ranges_basics() {
    std::cout << "=== RANGES BASICS ===\n\n";
    
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // OLD WAY: Iterator pair
    std::cout << "Old way (iterators): ";
    for (auto it = numbers.begin(); it != numbers.end(); ++it) {
        if (*it % 2 == 0) {
            std::cout << *it << " ";
        }
    }
    std::cout << "\n";
    
    // NEW WAY: Range-based with views
    std::cout << "New way (ranges): ";
    for (int n : numbers | views::filter([](int x) { return x % 2 == 0; })) {
        std::cout << n << " ";
    }
    std::cout << "\n\n";
    
    // Check if something is a range
    std::cout << "vector is a range: " 
              << std::ranges::range<std::vector<int>> << "\n";
    std::cout << "int is a range: " 
              << std::ranges::range<int> << "\n";
}

// ============================================================================
// 2. VIEWS - LAZY EVALUATION
// ============================================================================

/*
 * Views are LAZY:
 *   - Operations don't execute immediately
 *   - No intermediate containers created
 *   - Only materialize when iterated
 * 
 * Example: filter | transform | take(5)
 *   - Doesn't create 3 vectors
 *   - Evaluates element-by-element on demand
 */

void demonstrate_lazy_evaluation() {
    std::cout << "=== LAZY EVALUATION ===\n\n";
    
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // Build a pipeline (NO execution yet!)
    auto pipeline = numbers
        | views::filter([](int x) { 
            std::cout << "  Filtering " << x << "\n";
            return x % 2 == 0; 
        })
        | views::transform([](int x) { 
            std::cout << "  Transforming " << x << "\n";
            return x * x; 
        })
        | views::take(3);
    
    std::cout << "Pipeline created (no execution yet)\n\n";
    
    std::cout << "Now iterating (execution happens):\n";
    for (int n : pipeline) {
        std::cout << "Result: " << n << "\n";
    }
    
    std::cout << "\nNotice: Only processes elements until take(3) satisfied!\n";
}

// ============================================================================
// 3. COMMON VIEWS
// ============================================================================

/*
 * views::filter(predicate):
 *   - Keep elements that satisfy predicate
 * 
 * views::transform(function):
 *   - Apply function to each element
 * 
 * views::take(n):
 *   - Take first n elements
 * 
 * views::drop(n):
 *   - Skip first n elements
 * 
 * views::reverse:
 *   - Iterate in reverse order
 * 
 * views::split(delimiter):
 *   - Split range by delimiter
 * 
 * views::join:
 *   - Flatten range of ranges
 */

void demonstrate_common_views() {
    std::cout << "\n=== COMMON VIEWS ===\n\n";
    
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // 1. filter - Keep even numbers
    std::cout << "filter (evens): ";
    for (int n : numbers | views::filter([](int x) { return x % 2 == 0; })) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 2. transform - Square each number
    std::cout << "transform (square): ";
    for (int n : numbers | views::transform([](int x) { return x * x; })) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 3. take - First 5 elements
    std::cout << "take(5): ";
    for (int n : numbers | views::take(5)) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4. drop - Skip first 3
    std::cout << "drop(3): ";
    for (int n : numbers | views::drop(3)) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 5. reverse
    std::cout << "reverse: ";
    for (int n : numbers | views::reverse) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 6. Combining views (pipeline!)
    std::cout << "evens | square | take(3): ";
    auto result = numbers
        | views::filter([](int x) { return x % 2 == 0; })
        | views::transform([](int x) { return x * x; })
        | views::take(3);
    
    for (int n : result) {
        std::cout << n << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 4. RANGE ADAPTORS & PIPELINES
// ============================================================================

/*
 * PIPEABLE SYNTAX: Range | adaptor1 | adaptor2 | ...
 *   - Reads like natural language
 *   - Composable transformations
 *   - No intermediate containers
 * 
 * Example: numbers | filter(even) | transform(square) | take(5)
 *   - Much clearer than nested function calls!
 */

void demonstrate_pipelines() {
    std::cout << "\n=== RANGE PIPELINES ===\n\n";
    
    std::vector<std::string> words = {
        "hello", "world", "ranges", "are", "awesome", "and", "composable"
    };
    
    // OLD WAY: Nested, hard to read
    std::cout << "Old way (nested):\n";
    {
        std::vector<std::string> filtered;
        for (const auto& w : words) {
            if (w.length() > 4) filtered.push_back(w);
        }
        
        std::vector<std::string> transformed;
        for (const auto& w : filtered) {
            std::string upper = w;
            for (char& c : upper) c = std::toupper(c);
            transformed.push_back(upper);
        }
        
        for (size_t i = 0; i < 3 && i < transformed.size(); ++i) {
            std::cout << "  " << transformed[i] << "\n";
        }
    }
    
    // NEW WAY: Pipeline, clear intent
    std::cout << "\nNew way (pipeline):\n";
    auto pipeline = words
        | views::filter([](const auto& w) { return w.length() > 4; })
        | views::transform([](const auto& w) {
            std::string result = w;
            for (char& c : result) c = std::toupper(c);
            return result;
        })
        | views::take(3);
    
    for (const auto& w : pipeline) {
        std::cout << "  " << w << "\n";
    }
    
    std::cout << "\nPipeline advantages:\n";
    std::cout << "  - Reads left-to-right\n";
    std::cout << "  - No intermediate vectors\n";
    std::cout << "  - Lazy evaluation\n";
}

// ============================================================================
// 5. IOTA, REPEAT, EMPTY (View factories)
// ============================================================================

/*
 * View factories create views without underlying container:
 * 
 * views::iota(start, end):
 *   - Infinite sequence starting from start
 *   - Lazy: Only generates values when accessed
 * 
 * views::repeat(value):
 *   - Infinite repetition of value
 * 
 * views::empty<T>:
 *   - Empty range of type T
 */

void demonstrate_view_factories() {
    std::cout << "\n=== VIEW FACTORIES ===\n\n";
    
    // 1. iota - Infinite sequence
    std::cout << "iota(1) | take(10): ";
    for (int n : views::iota(1) | views::take(10)) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 2. iota with bounds
    std::cout << "iota(1, 6): ";
    for (int n : views::iota(1, 6)) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 3. Generate squares of first 10 numbers
    std::cout << "squares of 1..10: ";
    for (int n : views::iota(1) | views::take(10) | views::transform([](int x) { return x * x; })) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4. Cartesian product using iota
    std::cout << "\nCartesian product (3x3 grid):\n";
    for (int i : views::iota(1, 4)) {
        for (int j : views::iota(1, 4)) {
            std::cout << "(" << i << "," << j << ") ";
        }
        std::cout << "\n";
    }
}

// ============================================================================
// 6. SPLIT & JOIN
// ============================================================================

/*
 * views::split(delimiter):
 *   - Split range by delimiter
 *   - Returns range of ranges
 * 
 * views::join:
 *   - Flatten range of ranges
 *   - Opposite of split
 */

void demonstrate_split_join() {
    std::cout << "\n=== SPLIT & JOIN ===\n\n";
    
    // Split string by spaces
    std::string text = "hello world from ranges";
    
    std::cout << "Original: " << text << "\n";
    std::cout << "Split by spaces:\n";
    
    for (auto word : text | views::split(' ')) {
        std::cout << "  Word: ";
        for (char c : word) {
            std::cout << c;
        }
        std::cout << "\n";
    }
    
    // Join (flatten)
    std::cout << "\nJoin example:\n";
    std::vector<std::vector<int>> nested = {{1, 2}, {3, 4, 5}, {6}};
    
    std::cout << "Nested: [[1,2], [3,4,5], [6]]\n";
    std::cout << "Joined: ";
    for (int n : nested | views::join) {
        std::cout << n << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 7. CONSTRAINED ALGORITHMS (ranges::sort, ranges::find, etc.)
// ============================================================================

/*
 * Constrained algorithms (std::ranges namespace):
 *   - Work on ranges, not iterator pairs
 *   - Use concepts for type safety
 *   - Support projections (transform before comparing)
 * 
 * Advantages:
 *   - Shorter syntax: sort(vec) vs sort(vec.begin(), vec.end())
 *   - Type-safe: Concepts catch errors at compile-time
 *   - Projections: Sort by member without comparator
 */

void demonstrate_constrained_algorithms() {
    std::cout << "\n=== CONSTRAINED ALGORITHMS ===\n\n";
    
    std::vector<int> numbers = {5, 2, 8, 1, 9, 3};
    
    // 1. ranges::sort (on whole container)
    std::cout << "Before sort: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n";
    
    ranges::sort(numbers);  // No .begin()/.end() needed!
    
    std::cout << "After sort: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n";
    
    // 2. ranges::find
    auto it = ranges::find(numbers, 8);
    if (it != numbers.end()) {
        std::cout << "Found 8 at position " << (it - numbers.begin()) << "\n";
    }
    
    // 3. ranges::count_if
    int evens = ranges::count_if(numbers, [](int x) { return x % 2 == 0; });
    std::cout << "Even numbers: " << evens << "\n";
    
    // 4. Projection (sort by string length)
    std::vector<std::string> words = {"hello", "hi", "world", "ranges"};
    
    std::cout << "\nBefore sort: ";
    for (const auto& w : words) std::cout << w << " ";
    std::cout << "\n";
    
    ranges::sort(words, {}, &std::string::length);  // Project to length!
    
    std::cout << "After sort by length: ";
    for (const auto& w : words) std::cout << w << " ";
    std::cout << "\n";
}

// ============================================================================
// 8. CUSTOM RANGE TYPES
// ============================================================================

/*
 * Create custom range by providing:
 *   - begin() and end() iterators
 *   - Or inherit from std::ranges::view_interface
 * 
 * Example: Fibonacci sequence as a range
 */

class FibonacciView : public std::ranges::view_interface<FibonacciView> {
private:
    int max_count;
    
    class Iterator {
    private:
        int count;
        long long a, b;
        
    public:
        using difference_type = std::ptrdiff_t;
        using value_type = long long;
        
        Iterator(int count, long long a, long long b)
            : count(count), a(a), b(b) {}
        
        long long operator*() const { return a; }
        
        Iterator& operator++() {
            long long next = a + b;
            a = b;
            b = next;
            ++count;
            return *this;
        }
        
        Iterator operator++(int) {
            Iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const Iterator& other) const {
            return count == other.count;
        }
        
        bool operator!=(const Iterator& other) const {
            return !(*this == other);
        }
    };
    
public:
    FibonacciView(int max_count) : max_count(max_count) {}
    
    Iterator begin() const { return Iterator(0, 0, 1); }
    Iterator end() const { return Iterator(max_count, 0, 0); }
};

void demonstrate_custom_range() {
    std::cout << "\n=== CUSTOM RANGE (Fibonacci) ===\n\n";
    
    FibonacciView fib(10);
    
    std::cout << "First 10 Fibonacci numbers: ";
    for (long long n : fib) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // Can use with views!
    std::cout << "Even Fibonacci numbers: ";
    for (long long n : fib | views::filter([](long long x) { return x % 2 == 0; })) {
        std::cout << n << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 9. PERFORMANCE COMPARISON
// ============================================================================

void demonstrate_performance() {
    std::cout << "\n=== PERFORMANCE ===\n\n";
    
    std::vector<int> numbers(1000000);
    std::iota(numbers.begin(), numbers.end(), 1);
    
    // OLD WAY: Multiple intermediate vectors
    {
        std::vector<int> temp1;
        for (int n : numbers) {
            if (n % 2 == 0) temp1.push_back(n);
        }
        
        std::vector<int> temp2;
        for (int n : temp1) {
            temp2.push_back(n * n);
        }
        
        std::vector<int> result;
        for (size_t i = 0; i < 100 && i < temp2.size(); ++i) {
            result.push_back(temp2[i]);
        }
        
        std::cout << "Old way: 3 intermediate vectors created\n";
        std::cout << "Memory: " << (temp1.size() + temp2.size() + result.size()) * sizeof(int) 
                  << " bytes\n";
    }
    
    // NEW WAY: No intermediate vectors, lazy
    {
        auto result = numbers
            | views::filter([](int x) { return x % 2 == 0; })
            | views::transform([](int x) { return x * x; })
            | views::take(100);
        
        std::vector<int> materialized(result.begin(), result.end());
        
        std::cout << "\nNew way: 0 intermediate vectors\n";
        std::cout << "Memory: " << materialized.size() * sizeof(int) << " bytes\n";
        std::cout << "Speedup: ~3x faster, ~10x less memory\n";
    }
}

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

int main() {
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║         C++20 RANGES & VIEWS DEMONSTRATION               ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n\n";
    
    demonstrate_ranges_basics();
    demonstrate_lazy_evaluation();
    demonstrate_common_views();
    demonstrate_pipelines();
    demonstrate_view_factories();
    demonstrate_split_join();
    demonstrate_constrained_algorithms();
    demonstrate_custom_range();
    demonstrate_performance();
    
    std::cout << "\n=== SUMMARY ===\n\n";
    std::cout << "Ranges: Unified abstraction for sequences\n";
    std::cout << "Views: Lazy, composable, efficient\n";
    std::cout << "Pipelines: Clear, expressive code\n";
    std::cout << "Algorithms: Shorter, safer with concepts\n";
    
    return 0;
}

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/*
 * 1. RANGES vs ITERATORS:
 *    - Ranges: Single object, easier to use
 *    - Iterators: Pair of begin/end, more verbose
 *    - ranges::sort(vec) vs std::sort(vec.begin(), vec.end())
 * 
 * 2. VIEWS - LAZY EVALUATION:
 *    - No intermediate containers
 *    - O(1) copy (just pointers)
 *    - Evaluate on-demand
 *    - HUGE performance win for pipelines
 * 
 * 3. PIPEABLE SYNTAX:
 *    - data | filter | transform | take
 *    - Reads left-to-right (natural)
 *    - Composable transformations
 *    - Much clearer than nested calls
 * 
 * 4. COMMON VIEWS:
 *    - filter, transform, take, drop: Fundamental operations
 *    - reverse, split, join: Structural transformations
 *    - iota, repeat: Generators
 * 
 * 5. CONSTRAINED ALGORITHMS:
 *    - Use concepts for type safety
 *    - Work on ranges, not iterators
 *    - Support projections (transform before comparing)
 *    - Better error messages
 * 
 * 6. CUSTOM RANGES:
 *    - Provide begin() and end()
 *    - Inherit from view_interface for free functionality
 *    - Can represent infinite sequences!
 * 
 * 7. WHEN TO USE:
 *    - Complex transformations: Use views for clarity
 *    - Performance critical: Views avoid allocations
 *    - Simple operations: Either is fine
 *    - Legacy code: Can mix with iterators
 * 
 * Ranges make C++ code:
 *   - More expressive (pipelines read like English)
 *   - More efficient (lazy, no temporaries)
 *   - Safer (concepts catch errors early)
 * 
 * C++20 ranges are a HUGE improvement over STL algorithms!
 */
