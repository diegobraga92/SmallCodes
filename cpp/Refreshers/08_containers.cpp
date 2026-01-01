#include <iostream>
#include <array>
#include <vector>
#include <deque>
#include <list>
#include <forward_list>
#include <set>
#include <unordered_set>
#include <map>
#include <unordered_map>
#include <stack>
#include <queue>
#include <algorithm>
#include <string>
#include <string_view>
#include <functional>
#include <memory>
#include <iterator>

void demonstrate_containers() {
    std::cout << "============ C++ CONTAINERS COMPLETE GUIDE ============\n" << std::endl;

    // ============ 1. C-STYLE ARRAYS ============
    std::cout << "=== 1. C-style Arrays ===" << std::endl;
    std::cout << "Fixed-size, stack-allocated, minimal overhead\n" << std::endl;
    
    int c_array[5] = {1, 2, 3, 4, 5};
    
    // Problems:
    // - No bounds checking
    // - Size fixed at compile-time
    // - Decays to pointer (loses size info)
    // - Cannot be returned from functions easily
    
    std::cout << "C-array size (tricky): " << sizeof(c_array)/sizeof(c_array[0]) << std::endl;
    std::cout << "Access: c_array[0] = " << c_array[0] << std::endl;
    // c_array[10] = 100; // UNDEFINED BEHAVIOR - no bounds checking!
    std::cout << std::endl;

    // ============ 2. std::array (C++11) ============
    std::cout << "=== 2. std::array<T, N> ===" << std::endl;
    std::cout << "Fixed-size, stack-allocated, STL interface\n" << std::endl;
    
    std::array<int, 5> arr = {1, 2, 3, 4, 5};
    
    // Advantages over C-arrays:
    std::cout << "Size: " << arr.size() << std::endl;
    std::cout << "Empty? " << arr.empty() << std::endl;
    std::cout << "Front: " << arr.front() << std::endl;
    std::cout << "Back: " << arr.back() << std::endl;
    
    // Bounds checking
    try {
        std::cout << "arr.at(2): " << arr.at(2) << std::endl;
        // arr.at(10); // Throws std::out_of_range
    } catch (const std::out_of_range& e) {
        std::cout << "Bounds checking works!" << std::endl;
    }
    
    // Fill
    arr.fill(42);
    std::cout << "After fill(42): ";
    for (int val : arr) std::cout << val << " ";
    std::cout << "\n" << std::endl;

    // ============ 3. std::vector ============
    std::cout << "=== 3. std::vector<T> ===" << std::endl;
    std::cout << "Dynamic array, heap-allocated, contiguous memory\n" << std::endl;
    
    std::vector<int> vec = {1, 2, 3, 4, 5};
    
    // Key operations
    vec.push_back(6);  // O(1) amortized
    vec.pop_back();    // O(1)
    
    std::cout << "Size: " << vec.size() << std::endl;
    std::cout << "Capacity: " << vec.capacity() << std::endl;  // Memory allocated
    std::cout << "Max size: " << vec.max_size() << std::endl;
    
    // Reserve memory to avoid reallocations
    vec.reserve(100);
    std::cout << "After reserve(100), capacity: " << vec.capacity() << std::endl;
    
    // Shrink to fit
    vec.shrink_to_fit();
    std::cout << "After shrink_to_fit, capacity: " << vec.capacity() << std::endl;
    
    // Insert/erase (expensive - O(n) for middle)
    vec.insert(vec.begin() + 2, 99);  // Insert at position 2
    vec.erase(vec.begin() + 3);       // Remove element at position 3
    
    std::cout << "Vector elements: ";
    for (int val : vec) std::cout << val << " ";
    std::cout << "\n" << std::endl;

    // ============ 4. SEQUENCE CONTAINERS COMPARISON ============
    std::cout << "=== 4. Sequence Containers Comparison ===" << std::endl;
    std::cout << "vector vs deque vs list vs forward_list\n" << std::endl;

    // deque - Double-ended queue
    std::deque<int> deq = {1, 2, 3, 4, 5};
    deq.push_front(0);   // O(1) - efficient at both ends
    deq.push_back(6);
    
    std::cout << "Deque front: " << deq.front() << std::endl;
    std::cout << "Deque back: " << deq.back() << std::endl;
    // deque elements NOT guaranteed contiguous in memory
    
    // list - Doubly linked list
    std::list<int> lst = {1, 2, 3, 4, 5};
    lst.push_front(0);     // O(1)
    lst.push_back(6);      // O(1)
    lst.insert(++lst.begin(), 99);  // O(1) for insertion
    
    // Splice - transfer nodes between lists
    std::list<int> lst2 = {100, 200};
    lst.splice(lst.begin(), lst2);  // O(1)
    
    std::cout << "List after splice: ";
    for (int val : lst) std::cout << val << " ";
    std::cout << std::endl;
    
    // forward_list - Singly linked list (C++11)
    std::forward_list<int> flist = {1, 2, 3, 4, 5};
    flist.push_front(0);  // Only push_front available
    
    // Comparison table:
    std::cout << "\nComparison (Big-O):" << std::endl;
    std::cout << "                vector    deque     list" << std::endl;
    std::cout << "Access[i]        O(1)      O(1)      O(n)" << std::endl;
    std::cout << "Insert front     O(n)      O(1)      O(1)" << std::endl;
    std::cout << "Insert middle    O(n)      O(n)      O(1)" << std::endl;
    std::cout << "Insert back      O(1)*     O(1)      O(1)" << std::endl;
    std::cout << "Memory           Contiguous  Chunks   Fragmented" << std::endl;
    std::cout << "Cache friendly   Yes        Partial   No" << std::endl;
    std::cout << "* O(1) amortized, O(n) worst-case when resizing\n" << std::endl;

    // ============ 5. ASSOCIATIVE CONTAINERS ============
    std::cout << "=== 5. Associative Containers (Ordered) ===" << std::endl;
    std::cout << "std::set and std::map - implemented as Red-Black trees\n" << std::endl;
    
    // set - unique keys, sorted
    std::set<int> my_set = {5, 2, 8, 1, 9};
    my_set.insert(3);
    my_set.insert(5);  // Duplicate - ignored
    
    std::cout << "Set (automatically sorted): ";
    for (int val : my_set) std::cout << val << " ";
    std::cout << std::endl;
    
    // Find - O(log n)
    auto it = my_set.find(3);
    if (it != my_set.end()) {
        std::cout << "Found 3 in set" << std::endl;
    }
    
    // Lower/upper bound
    auto lb = my_set.lower_bound(4);  // First element >= 4
    auto ub = my_set.upper_bound(7);  // First element > 7
    
    std::cout << "Elements in range [4,7]: ";
    for (auto iter = lb; iter != ub; ++iter) {
        std::cout << *iter << " ";
    }
    std::cout << std::endl;
    
    // map - key-value pairs, sorted by key
    std::map<std::string, int> population = {
        {"Tokyo", 37400068},
        {"Delhi", 28514000},
        {"Shanghai", 25582000}
    };
    
    population["Beijing"] = 21516000;  // Insert or update
    
    // Iterate (sorted by key)
    std::cout << "\nCities by population (sorted by name):" << std::endl;
    for (const auto& [city, pop] : population) {
        std::cout << city << ": " << pop << std::endl;
    }
    
    // Find in map
    auto city_it = population.find("Tokyo");
    if (city_it != population.end()) {
        std::cout << "Tokyo population: " << city_it->second << std::endl;
    }
    std::cout << std::endl;

    // ============ 6. UNORDERED CONTAINERS (C++11) ============
    std::cout << "=== 6. Unordered Containers (Hash Tables) ===" << std::endl;
    std::cout << "std::unordered_set and std::unordered_map\n" << std::endl;
    
    // unordered_set - hash table implementation
    std::unordered_set<int> u_set = {5, 2, 8, 1, 9};
    u_set.insert(3);
    
    std::cout << "Unordered set (not sorted): ";
    for (int val : u_set) std::cout << val << " ";
    std::cout << std::endl;
    
    // Bucket interface
    std::cout << "Bucket count: " << u_set.bucket_count() << std::endl;
    std::cout << "Load factor: " << u_set.load_factor() << std::endl;
    std::cout << "Max load factor: " << u_set.max_load_factor() << std::endl;
    
    // unordered_map - hash table for key-value pairs
    std::unordered_map<std::string, int> u_population = {
        {"Tokyo", 37400068},
        {"Delhi", 28514000},
        {"Shanghai", 25582000}
    };
    
    // Custom hash function can be provided
    std::cout << "\nUnordered map bucket info:" << std::endl;
    for (size_t i = 0; i < u_population.bucket_count(); ++i) {
        std::cout << "Bucket " << i << " has " << u_population.bucket_size(i) << " elements" << std::endl;
    }

    // ============ 7. MAP vs UNORDERED_MAP COMPARISON ============
    std::cout << "\n=== 7. map vs unordered_map ===" << std::endl;
    std::cout << "map (Red-Black Tree):" << std::endl;
    std::cout << "• Keys sorted in order" << std::endl;
    std::cout << "• O(log n) for insert/find/delete" << std::endl;
    std::cout << "• Needs operator< for key type" << std::endl;
    std::cout << "• Iterators remain valid after insert/erase" << std::endl;
    
    std::cout << "\nunordered_map (Hash Table):" << std::endl;
    std::cout << "• Keys not sorted" << std::endl;
    std::cout << "• O(1) average, O(n) worst-case" << std::endl;
    std::cout << "• Needs std::hash and operator== for key type" << std::endl;
    std::cout << "• May need to provide custom hash function" << std::endl;
    std::cout << "• Rehashing can invalidate iterators" << std::endl;
    
    std::cout << "\nWhen to use:" << std::endl;
    std::cout << "• Use map when you need ordering or stable performance" << std::endl;
    std::cout << "• Use unordered_map when you need maximum speed and don't need ordering" << std::endl;
    std::cout << std::endl;

    // ============ 8. SET vs UNORDERED_SET ============
    std::cout << "=== 8. set vs unordered_set ===" << std::endl;
    std::cout << "Similar trade-offs as map vs unordered_map" << std::endl;
    std::cout << "set: ordered, O(log n), needs operator<" << std::endl;
    std::cout << "unordered_set: not ordered, O(1) avg, needs hash function\n" << std::endl;

    // ============ 9. CONTAINER ADAPTERS ============
    std::cout << "=== 9. Container Adapters ===" << std::endl;
    
    // stack - LIFO
    std::stack<int> stk;
    stk.push(1);
    stk.push(2);
    stk.push(3);
    
    std::cout << "Stack top: " << stk.top() << std::endl;
    stk.pop();
    std::cout << "After pop, top: " << stk.top() << std::endl;
    
    // queue - FIFO
    std::queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    
    std::cout << "Queue front: " << q.front() << std::endl;
    std::cout << "Queue back: " << q.back() << std::endl;
    q.pop();
    std::cout << "After pop, front: " << q.front() << std::endl;
    
    // priority_queue - max-heap by default
    std::priority_queue<int> pq;
    pq.push(3);
    pq.push(1);
    pq.push(4);
    pq.push(2);
    
    std::cout << "Priority queue (max-heap) pops: ";
    while (!pq.empty()) {
        std::cout << pq.top() << " ";
        pq.pop();
    }
    std::cout << "\n" << std::endl;
}

// ============ 10. ITERATORS ============
void demonstrate_iterators() {
    std::cout << "============ ITERATORS ============\n" << std::endl;
    
    std::vector<int> vec = {1, 2, 3, 4, 5};
    
    // ============ Iterator Categories ============
    std::cout << "=== Iterator Categories ===" << std::endl;
    std::cout << "1. Input Iterator: read-only, forward movement" << std::endl;
    std::cout << "   Example: std::istream_iterator" << std::endl;
    
    std::cout << "\n2. Output Iterator: write-only, forward movement" << std::endl;
    std::cout << "   Example: std::ostream_iterator" << std::endl;
    
    std::cout << "\n3. Forward Iterator: read/write, forward only" << std::endl;
    std::cout << "   Example: std::forward_list iterator" << std::endl;
    
    std::cout << "\n4. Bidirectional Iterator: forward and backward" << std::endl;
    std::cout << "   Example: std::list iterator" << std::endl;
    
    std::cout << "\n5. Random Access Iterator: jump to any position" << std::endl;
    std::cout << "   Example: vector, deque, array iterators" << std::endl;
    
    std::cout << "\n6. Contiguous Iterator (C++20): adjacent memory" << std::endl;
    std::cout << "   Example: vector, array iterators\n" << std::endl;
    
    // ============ Basic Iterator Usage ============
    std::cout << "=== Basic Iterator Usage ===" << std::endl;
    
    // Begin/end iterators
    auto begin_it = vec.begin();
    auto end_it = vec.end();
    
    std::cout << "First element: " << *begin_it << std::endl;
    std::cout << "Last element: " << *(end_it - 1) << std::endl;
    
    // Loop with iterators
    std::cout << "Using iterators: ";
    for (auto it = vec.begin(); it != vec.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
    
    // Reverse iterators
    std::cout << "Reverse: ";
    for (auto rit = vec.rbegin(); rit != vec.rend(); ++rit) {
        std::cout << *rit << " ";
    }
    std::cout << std::endl;
    
    // Const iterators
    const std::vector<int> const_vec = {1, 2, 3};
    for (auto cit = const_vec.cbegin(); cit != const_vec.cend(); ++cit) {
        // *cit = 10;  // ERROR: cannot modify through const iterator
        std::cout << *cit << " ";
    }
    std::cout << std::endl;
    
    // ============ Iterator Traits ============
    std::cout << "\n=== Iterator Traits ===" << std::endl;
    
    using iterator_type = std::vector<int>::iterator;
    using traits = std::iterator_traits<iterator_type>;
    
    std::cout << "Value type: " << typeid(traits::value_type).name() << std::endl;
    std::cout << "Difference type: " << typeid(traits::difference_type).name() << std::endl;
    std::cout << "Pointer type: " << typeid(traits::pointer).name() << std::endl;
    std::cout << "Reference type: " << typeid(traits::reference).name() << std::endl;
    std::cout << "Iterator category: ";
    
    if constexpr (std::is_same_v<traits::iterator_category, 
                                 std::random_access_iterator_tag>) {
        std::cout << "random access" << std::endl;
    }
    
    // ============ Iterator Invalidation Rules ============
    std::cout << "\n=== Iterator Invalidation Rules ===" << std::endl;
    std::cout << "When operations invalidate iterators:\n" << std::endl;
    
    std::cout << "vector:" << std::endl;
    std::cout << "• Insert: All iterators after insertion point invalidated if reallocation" << std::endl;
    std::cout << "• Erase: All iterators after erasure point invalidated" << std::endl;
    std::cout << "• push_back: All iterators invalidated if reallocation" << std::endl;
    
    std::cout << "\ndeque:" << std::endl;
    std::cout << "• Insert at ends: Iterators invalidated, references not" << std::endl;
    std::cout << "• Insert in middle: All iterators and references invalidated" << std::endl;
    
    std::cout << "\nlist/set/map:" << std::endl;
    std::cout << "• Insert/erase: Only iterators to removed elements invalidated" << std::endl;
    std::cout << "• References never invalidated (until element destroyed)" << std::endl;
    
    std::cout << "\nunordered containers:" << std::endl;
    std::cout << "• Rehash: All iterators invalidated" << std::cout;
    std::cout << "• Insert: May cause rehash" << std::endl;
    
    // ============ Custom Iterator Example ============
    std::cout << "\n=== Custom Iterator (Simplified) ===" << std::endl;
    
    class RangeIterator {
        int current;
        int step;
    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = int;
        using difference_type = std::ptrdiff_t;
        using pointer = int*;
        using reference = int&;
        
        RangeIterator(int start, int step = 1) : current(start), step(step) {}
        
        int operator*() const { return current; }
        RangeIterator& operator++() { current += step; return *this; }
        RangeIterator operator++(int) { RangeIterator temp = *this; ++(*this); return temp; }
        
        bool operator==(const RangeIterator& other) const { 
            return current >= other.current;  // Simplified for range
        }
        bool operator!=(const RangeIterator& other) const { return !(*this == other); }
    };
    
    std::cout << "Custom range [0,10) step 2: ";
    for (auto it = RangeIterator(0, 2); it != RangeIterator(10, 2); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n" << std::endl;
}

// ============ 11. ALGORITHMS ============
#include <algorithm>
#include <numeric>
#include <execution>  // C++17 parallel algorithms

void demonstrate_algorithms() {
    std::cout << "============ ALGORITHMS ============\n" << std::endl;
    
    std::vector<int> numbers = {5, 2, 8, 1, 9, 3, 7, 4, 6};
    
    // ============ Non-modifying Algorithms ============
    std::cout << "=== Non-modifying Algorithms ===" << std::endl;
    
    // count
    int count_of_even = std::count_if(numbers.begin(), numbers.end(),
                                      [](int n) { return n % 2 == 0; });
    std::cout << "Even numbers: " << count_of_even << std::endl;
    
    // find
    auto found = std::find(numbers.begin(), numbers.end(), 7);
    if (found != numbers.end()) {
        std::cout << "Found 7 at position: " << std::distance(numbers.begin(), found) << std::endl;
    }
    
    // all_of, any_of, none_of
    bool all_positive = std::all_of(numbers.begin(), numbers.end(),
                                    [](int n) { return n > 0; });
    std::cout << "All positive? " << all_positive << std::endl;
    
    // ============ Modifying Algorithms ============
    std::cout << "\n=== Modifying Algorithms ===" << std::endl;
    
    // transform
    std::vector<int> squares(numbers.size());
    std::transform(numbers.begin(), numbers.end(), squares.begin(),
                   [](int n) { return n * n; });
    
    std::cout << "Squares: ";
    for (int n : squares) std::cout << n << " ";
    std::cout << std::endl;
    
    // copy
    std::vector<int> copy_vec(numbers.size());
    std::copy(numbers.begin(), numbers.end(), copy_vec.begin());
    
    // copy_if
    std::vector<int> evens;
    std::copy_if(numbers.begin(), numbers.end(), std::back_inserter(evens),
                 [](int n) { return n % 2 == 0; });
    
    // fill
    std::fill(copy_vec.begin(), copy_vec.end(), 0);
    
    // generate
    std::vector<int> generated(5);
    int counter = 0;
    std::generate(generated.begin(), generated.end(), 
                  [&counter]() { return ++counter; });
    
    // ============ Sorting Algorithms ============
    std::cout << "\n=== Sorting Algorithms ===" << std::endl;
    
    // sort
    std::vector<int> to_sort = numbers;
    std::sort(to_sort.begin(), to_sort.end());
    std::cout << "Sorted: ";
    for (int n : to_sort) std::cout << n << " ";
    std::cout << std::endl;
    
    // stable_sort (preserves order of equal elements)
    std::vector<std::pair<int, char>> pairs = {{1, 'a'}, {2, 'b'}, {1, 'c'}};
    std::stable_sort(pairs.begin(), pairs.end(),
                     [](auto& a, auto& b) { return a.first < b.first; });
    
    // partial_sort (sort first N elements)
    std::vector<int> partial = numbers;
    std::partial_sort(partial.begin(), partial.begin() + 3, partial.end());
    std::cout << "First 3 sorted: ";
    for (int i = 0; i < 3; ++i) std::cout << partial[i] << " ";
    std::cout << std::endl;
    
    // nth_element
    std::vector<int> nth_vec = numbers;
    auto middle = nth_vec.begin() + nth_vec.size()/2;
    std::nth_element(nth_vec.begin(), middle, nth_vec.end());
    std::cout << "Median: " << *middle << std::endl;
    
    // ============ Numeric Algorithms ============
    std::cout << "\n=== Numeric Algorithms ===" << std::endl;
    
    // accumulate
    int sum = std::accumulate(numbers.begin(), numbers.end(), 0);
    std::cout << "Sum: " << sum << std::endl;
    
    // with custom operation
    int product = std::accumulate(numbers.begin(), numbers.end(), 1,
                                  [](int a, int b) { return a * b; });
    std::cout << "Product: " << product << std::endl;
    
    // inner_product
    std::vector<int> v1 = {1, 2, 3};
    std::vector<int> v2 = {4, 5, 6};
    int dot_product = std::inner_product(v1.begin(), v1.end(), v2.begin(), 0);
    std::cout << "Dot product: " << dot_product << std::endl;
    
    // partial_sum
    std::vector<int> prefix_sum(numbers.size());
    std::partial_sum(numbers.begin(), numbers.end(), prefix_sum.begin());
    std::cout << "Prefix sums: ";
    for (int n : prefix_sum) std::cout << n << " ";
    std::cout << std::endl;
    
    // adjacent_difference
    std::vector<int> diffs(numbers.size());
    std::adjacent_difference(numbers.begin(), numbers.end(), diffs.begin());
    std::cout << "Differences: ";
    for (int n : diffs) std::cout << n << " ";
    std::cout << std::endl;
    
    // ============ C++17 Parallel Algorithms ============
    std::cout << "\n=== Parallel Algorithms (C++17) ===" << std::endl;
    
    std::vector<int> big_vec(1000000, 1);
    
    // Sequential execution
    auto start = std::chrono::high_resolution_clock::now();
    std::sort(big_vec.begin(), big_vec.end());
    auto end = std::chrono::high_resolution_clock::now();
    auto seq_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // Parallel execution
    start = std::chrono::high_resolution_clock::now();
    std::sort(std::execution::par, big_vec.begin(), big_vec.end());
    end = std::chrono::high_resolution_clock::now();
    auto par_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Sequential sort: " << seq_time.count() << " μs" << std::endl;
    std::cout << "Parallel sort: " << par_time.count() << " μs" << std::endl;
    std::cout << "Speedup: " << (double)seq_time.count() / par_time.count() << "x\n" << std::endl;
}

// ============ 12. FUNCTORS & LAMBDAS ============
#include <functional>

void demonstrate_functors_lambdas() {
    std::cout << "============ FUNCTORS & LAMBDAS ============\n" << std::endl;
    
    // ============ Functors (Function Objects) ============
    std::cout << "=== Functors ===" << std::endl;
    
    // Functor class
    class Adder {
        int value;
    public:
        Adder(int v) : value(v) {}
        int operator()(int x) const { return x + value; }
    };
    
    Adder add5(5);
    std::cout << "add5(10) = " << add5(10) << std::endl;
    
    // Standard library functors
    std::plus<int> add;
    std::cout << "std::plus: 3 + 4 = " << add(3, 4) << std::endl;
    
    std::greater<int> gt;
    std::cout << "5 > 3? " << gt(5, 3) << std::endl;
    
    // ============ Lambda Expressions (C++11) ============
    std::cout << "\n=== Lambda Expressions ===" << std::endl;
    
    // Basic lambda
    auto basic = []() { std::cout << "Hello from lambda!" << std::endl; };
    basic();
    
    // Lambda with parameters
    auto add_lambda = [](int a, int b) { return a + b; };
    std::cout << "Lambda add: " << add_lambda(3, 4) << std::endl;
    
    // Lambda with capture
    int external = 100;
    
    // Capture by value [=] or specific variables [external]
    auto capture_by_value = [external]() {
        std::cout << "Captured by value: " << external << std::endl;
        // external = 200; // ERROR: cannot modify
    };
    capture_by_value();
    
    // Capture by reference [&] or [&external]
    auto capture_by_reference = [&external]() {
        external = 200;  // Can modify original
        std::cout << "Modified external to: " << external << std::endl;
    };
    capture_by_reference();
    
    // Mixed capture
    int a = 1, b = 2, c = 3;
    auto mixed = [a, &b, c = c + 10]() {  // c is new variable
        return a + b + c;
    };
    std::cout << "Mixed capture result: " << mixed() << std::endl;
    
    // ============ Generic Lambdas (C++14) ============
    std::cout << "\n=== Generic Lambdas (C++14) ===" << std::endl;
    
    auto generic = [](auto x, auto y) {
        return x + y;
    };
    
    std::cout << "Generic int add: " << generic(3, 4) << std::endl;
    std::cout << "Generic double add: " << generic(3.14, 2.71) << std::endl;
    std::cout << "Generic string concat: " << generic(std::string("Hello"), std::string(" World")) << std::endl;
    
    // ============ Mutable Lambdas ============
    std::cout << "\n=== Mutable Lambdas ===" << std::endl;
    
    // Without mutable
    auto counter1 = [count = 0]() mutable {
        return ++count;
    };
    
    std::cout << "Counter (mutable): ";
    for (int i = 0; i < 5; ++i) {
        std::cout << counter1() << " ";
    }
    std::cout << std::endl;
    
    // ============ Lambda with std::function ============
    std::cout << "\n=== std::function ===" << std::endl;
    
    std::function<int(int, int)> func;
    
    // Can store lambdas
    func = [](int a, int b) { return a + b; };
    std::cout << "std::function add: " << func(5, 3) << std::endl;
    
    // Can store functors
    func = std::plus<int>();
    std::cout << "std::function plus: " << func(5, 3) << std::endl;
    
    // Can store function pointers
    int (*func_ptr)(int, int) = [](int a, int b) { return a * b; };
    func = func_ptr;
    std::cout << "std::function from pointer: " << func(5, 3) << std::endl;
    
    // ============ Lambda as Algorithm Parameter ============
    std::cout << "\n=== Lambdas with Algorithms ===" << std::endl;
    
    std::vector<int> numbers = {5, 2, 8, 1, 9};
    
    // Sort with custom comparator
    std::sort(numbers.begin(), numbers.end(), 
              [](int a, int b) { return a > b; });  // Descending
    
    std::cout << "Sorted descending: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << std::endl;
    
    // Find_if with lambda
    auto it = std::find_if(numbers.begin(), numbers.end(),
                           [](int n) { return n % 2 == 0; });
    if (it != numbers.end()) {
        std::cout << "First even: " << *it << std::endl;
    }
    
    // Transform with lambda
    std::vector<int> doubled(numbers.size());
    std::transform(numbers.begin(), numbers.end(), doubled.begin(),
                   [](int n) { return n * 2; });
    
    // ============ Capture Initializers (C++14) ============
    std::cout << "\n=== Capture Initializers (C++14) ===" << std::endl;
    
    auto factory = [](int base) {
        return [value = base](int x) { return x + value; };
    };
    
    auto add10 = factory(10);
    std::cout << "Factory created lambda: add10(5) = " << add10(5) << std::endl;
    
    // ============ Immediately Invoked Lambda ============
    std::cout << "\n=== Immediately Invoked Lambda ===" << std::endl;
    
    int result = [](int a, int b) {
        return a * a + b * b;
    }(3, 4);  // Invoked immediately
    
    std::cout << "3² + 4² = " << result << "\n" << std::endl;
}

// ============ 13. ALLOCATORS ============
#include <memory_resource>  // C++17 polymorphic allocator

void demonstrate_allocators() {
    std::cout << "============ ALLOCATORS ============\n" << std::endl;
    
    // ============ Default Allocator ============
    std::cout << "=== Default Allocator ===" << std::endl;
    
    std::vector<int, std::allocator<int>> vec;  // Default
    vec.push_back(42);
    std::cout << "Default allocator used: " << vec[0] << std::endl;
    
    // ============ Custom Allocator ============
    std::cout << "\n=== Custom Allocator ===" << std::endl;
    
    template<typename T>
    class SimpleAllocator {
    public:
        using value_type = T;
        
        SimpleAllocator() = default;
        
        template<typename U>
        SimpleAllocator(const SimpleAllocator<U>&) {}
        
        T* allocate(std::size_t n) {
            std::cout << "Allocating " << n << " elements of size " << sizeof(T) << std::endl;
            return static_cast<T*>(::operator new(n * sizeof(T)));
        }
        
        void deallocate(T* p, std::size_t n) {
            std::cout << "Deallocating " << n << " elements" << std::endl;
            ::operator delete(p);
        }
    };
    
    // Using custom allocator
    std::vector<int, SimpleAllocator<int>> custom_vec;
    custom_vec.push_back(1);
    custom_vec.push_back(2);
    custom_vec.push_back(3);
    
    // ============ Polymorphic Allocator (C++17) ============
    std::cout << "\n=== Polymorphic Allocator (C++17) ===" << std::endl;
    
    // Memory resource
    std::pmr::monotonic_buffer_resource buffer(1024);  // 1KB buffer
    std::pmr::polymorphic_allocator<int> poly_alloc(&buffer);
    
    // Vector with polymorphic allocator
    std::pmr::vector<int> poly_vec(poly_alloc);
    poly_vec.push_back(10);
    poly_vec.push_back(20);
    poly_vec.push_back(30);
    
    std::cout << "Polymorphic allocator vector: ";
    for (int n : poly_vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // Different memory resources
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> pooled_vec(&pool);
    
    // ============ Scoped Allocator ============
    std::cout << "\n=== Scoped Allocator ===" << std::endl;
    
    // Propagates allocator to contained objects
    using MyString = std::pmr::string;
    using MyVector = std::pmr::vector<MyString>;
    
    std::pmr::monotonic_buffer_resource mr;
    MyVector scoped_vec(&mr);
    
    scoped_vec.push_back("Hello");
    scoped_vec.push_back("World");
    
    std::cout << "Scoped allocator ensures strings use same memory resource\n" << std::endl;
}

// ============ 14. STRINGS ============
#include <string_view>

void demonstrate_strings() {
    std::cout << "============ STRINGS ============\n" << std::endl;
    
    // ============ std::string ============
    std::cout << "=== std::string ===" << std::endl;
    
    std::string str1 = "Hello";
    std::string str2 = "World";
    
    // Concatenation
    std::string result = str1 + " " + str2;
    std::cout << "Concatenated: " << result << std::endl;
    
    // Access
    std::cout << "First char: " << result[0] << std::endl;
    std::cout << "Front: " << result.front() << std::endl;
    std::cout << "Back: " << result.back() << std::endl;
    
    // Size
    std::cout << "Size: " << result.size() << std::endl;
    std::cout << "Length: " << result.length() << std::endl;
    std::cout << "Capacity: " << result.capacity() << std::endl;
    
    // Modification
    result.append("!");
    std::cout << "After append: " << result << std::endl;
    
    result.insert(5, " C++");
    std::cout << "After insert: " << result << std::endl;
    
    result.erase(5, 4);  // Remove " C++"
    std::cout << "After erase: " << result << std::endl;
    
    // Find
    size_t pos = result.find("World");
    if (pos != std::string::npos) {
        std::cout << "'World' found at position: " << pos << std::endl;
    }
    
    // Substring
    std::string sub = result.substr(6, 5);  // "World"
    std::cout << "Substring: " << sub << std::endl;
    
    // Compare
    std::cout << "Compare 'Hello' with 'Hello': " << str1.compare("Hello") << std::endl;
    
    // Numeric conversions
    std::string num_str = "123";
    int num = std::stoi(num_str);
    std::cout << "String to int: " << num << std::endl;
    
    // ============ std::string_view (C++17) ============
    std::cout << "\n=== std::string_view (C++17) ===" << std::endl;
    
    // string_view is a non-owning view of a string
    std::string_view sv1 = "Hello World";  // View of C-string
    std::string_view sv2 = result;         // View of std::string
    
    std::cout << "string_view: " << sv1 << std::endl;
    std::cout << "Size: " << sv1.size() << std::endl;
    std::cout << "Is empty? " << sv1.empty() << std::endl;
    
    // Subview (O(1), no copy!)
    std::string_view subview = sv1.substr(0, 5);
    std::cout << "Subview 'Hello': " << subview << std::endl;
    
    // Compare
    std::cout << "Starts with 'Hello'? " << sv1.starts_with("Hello") << std::endl;
    std::cout << "Ends with 'World'? " << sv1.ends_with("World") << std::endl;
    
    // Find
    size_t sv_pos = sv1.find("World");
    std::cout << "'World' at: " << sv_pos << std::endl;
    
    // string_view is cheap to copy (just pointer + size)
    std::string_view sv_copy = sv1;
    
    // ============ string vs string_view ============
    std::cout << "\n=== string vs string_view ===" << std::endl;
    
    std::cout << "std::string:" << std::endl;
    std::cout << "• Owns the memory" << std::endl;
    std::cout << "• Can modify content" << std::endl;
    std::cout << "• Heap allocation (usually)" << std::endl;
    std::cout << "• Safe (guaranteed null-terminated)" << std::endl;
    
    std::cout << "\nstd::string_view:" << std::endl;
    std::cout << "• Non-owning view" << std::endl;
    std::cout << "• Read-only (cannot modify underlying string)" << std::endl;
    std::cout << "• No allocation (just pointer + size)" << std::endl;
    std::cout << "• Not guaranteed null-terminated" << std::endl;
    std::cout << "• Must ensure viewed string outlives the view" << std::endl;
    
    // ============ Best Practices ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "Use std::string when:" << std::endl;
    std::cout << "• You need to own/modify the string" << std::endl;
    std::cout << "• String lifetime needs to be managed" << std::endl;
    std::cout << "• Passing to C APIs that need null termination" << std::endl;
    
    std::cout << "\nUse std::string_view when:" << std::endl;
    std::cout << "• You only need read-only access" << std::endl;
    std::cout << "• Function parameters (avoid copies)" << std::endl;
    std::cout << "• Parsing/substring without allocation" << std::endl;
    std::cout << "• You can guarantee the viewed string lives long enough" << std::endl;
    
    // ============ Example: Function Parameters ============
    std::cout << "\n=== Example: Function Parameters ===" << std::endl;
    
    // BAD: Unnecessary copy
    // void process_string(std::string str);
    
    // GOOD: No copy if caller has std::string
    // void process_string(const std::string& str);
    
    // BETTER: Works with both std::string and string literals
    // void process_string(std::string_view str);
    
    auto print_string = [](std::string_view str) {
        std::cout << "Processing: " << str << std::endl;
    };
    
    print_string("Hello");  // Works with C-string
    print_string(str1);     // Works with std::string
    print_string(sv1);      // Works with string_view
    
    // ============ Raw String Literals ============
    std::cout << "\n=== Raw String Literals ===" << std::endl;
    
    std::string raw = R"(This is a "raw" string
with multiple lines
and no need to escape quotes)";
    
    std::cout << "Raw string:\n" << raw << std::endl;
    
    // ============ User-defined Literals ============
    std::cout << "\n=== User-defined Literals ===" << std::endl;
    
    using namespace std::string_literals;  // For s suffix
    
    auto s1 = "Hello";  // const char*
    auto s2 = "Hello"s; // std::string
    
    std::cout << "Type of \"Hello\": " << typeid(s1).name() << std::endl;
    std::cout << "Type of \"Hello\"s: " << typeid(s2).name() << "\n" << std::endl;
}

// ============ 15. BIG-O COMPLEXITY SUMMARY ============
void print_complexity_table() {
    std::cout << "============ BIG-O COMPLEXITY SUMMARY ============\n" << std::endl;
    
    std::cout << "                     | Access  | Search  | Insert  | Delete  | Notes" << std::endl;
    std::cout << "---------------------|---------|---------|---------|---------|----------------" << std::endl;
    std::cout << "vector               | O(1)    | O(n)    | O(n)    | O(n)    | Fast access" << std::endl;
    std::cout << "deque                | O(1)    | O(n)    | O(1)*   | O(n)    | Fast ends" << std::endl;
    std::cout << "list                 | O(n)    | O(n)    | O(1)    | O(1)    | Stable iterators" << std::endl;
    std::cout << "forward_list         | O(n)    | O(n)    | O(1)    | O(1)    | No size()" << std::endl;
    std::cout << std::endl;
    std::cout << "set/multiset         | N/A     | O(log n)| O(log n)| O(log n)| Ordered" << std::endl;
    std::cout << "map/multimap         | O(log n)| O(log n)| O(log n)| O(log n)| Ordered" << std::endl;
    std::cout << std::endl;
    std::cout << "unordered_set        | O(1)†   | O(1)†   | O(1)†   | O(1)†   | Hash table" << std::endl;
    std::cout << "unordered_map        | O(1)†   | O(1)†   | O(1)†   | O(1)†   | Hash table" << std::endl;
    std::cout << std::endl;
    std::cout << "array                | O(1)    | O(n)    | N/A     | N/A     | Fixed size" << std::endl;
    std::cout << "string               | O(1)    | O(n)    | O(n)    | O(n)    | Like vector" << std::endl;
    std::cout << "\n* O(1) at ends, O(n) in middle" << std::endl;
    std::cout << "† Average case, O(n) worst-case with collisions" << std::endl;
}

int main() {
    demonstrate_containers();
    demonstrate_iterators();
    demonstrate_algorithms();
    demonstrate_functors_lambdas();
    demonstrate_allocators();
    demonstrate_strings();
    print_complexity_table();
    
    return 0;
}