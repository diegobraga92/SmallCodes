#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <tuple>
#include <memory>
#include <coroutine>  // C++20
#include <compare>    // C++20

// ============ 5. STRUCTURED BINDINGS (C++17) ============

std::tuple<std::string, int, double> get_person() {
    return {"Alice", 30, 65000.50};
}

struct Point {
    double x, y, z;
};

struct Employee {
    std::string name;
    int id;
    double salary;
};

void demonstrate_structured_bindings() {
    std::cout << "============ STRUCTURED BINDINGS (C++17) ============\n" << std::endl;
    
    // ============ With std::pair ============
    std::cout << "=== With std::pair ===" << std::endl;
    
    std::pair<int, std::string> p{42, "answer"};
    
    // Old way:
    int first_old = p.first;
    std::string second_old = p.second;
    
    // New way (C++17):
    auto [first, second] = p;
    std::cout << "Pair: " << first << ", " << second << std::endl;
    
    // With references
    auto& [ref_first, ref_second] = p;
    ref_first = 100;
    std::cout << "Modified through reference: " << p.first << std::endl;
    
    // ============ With std::tuple ============
    std::cout << "\n=== With std::tuple ===" << std::endl;
    
    std::tuple<int, std::string, double> t{1, "hello", 3.14};
    
    auto [id, msg, value] = t;
    std::cout << "Tuple: " << id << ", " << msg << ", " << value << std::endl;
    
    // Returning tuple from function
    auto [name, age, salary] = get_person();
    std::cout << "Person: " << name << ", " << age << ", " << salary << std::endl;
    
    // ============ With Arrays ============
    std::cout << "\n=== With Arrays ===" << std::endl;
    
    int arr[] = {10, 20, 30};
    auto [a, b, c] = arr;
    std::cout << "Array elements: " << a << ", " << b << ", " << c << std::endl;
    
    // ============ With Structs ============
    std::cout << "\n=== With Structs ===" << std::endl;
    
    Point point{1.0, 2.0, 3.0};
    auto [x, y, z] = point;
    std::cout << "Point: (" << x << ", " << y << ", " << z << ")" << std::endl;
    
    // Modify through structured binding
    Employee emp{"Bob", 101, 50000.0};
    auto& [emp_name, emp_id, emp_salary] = emp;
    emp_salary = 55000.0;
    std::cout << "Updated salary: " << emp.salary << std::endl;
    
    // ============ With Maps ============
    std::cout << "\n=== With std::map ===" << std::endl;
    
    std::map<std::string, int> scores = {
        {"Alice", 95},
        {"Bob", 87},
        {"Charlie", 92}
    };
    
    // Old way:
    for (const auto& pair : scores) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    
    // New way:
    std::cout << "\nWith structured bindings:" << std::endl;
    for (const auto& [name, score] : scores) {
        std::cout << name << ": " << score << std::endl;
    }
    
    // ============ Advanced Usage ============
    std::cout << "\n=== Advanced Usage ===" << std::endl;
    
    // Nested structured bindings
    std::pair<Point, Employee> complex_pair{{1,2,3}, {"Dave", 102, 60000}};
    auto& [pt, employee] = complex_pair;
    auto [px, py, pz] = pt;
    
    std::cout << "Nested: Point(" << px << "," << py << "," << pz 
              << "), Employee " << employee.name << std::endl;
    
    // Ignore elements with _
    auto [_, important, __] = std::tuple{1, "important", 3.14};
    std::cout << "Important value: " << important << std::endl;
    
    // ============ Limitations ============
    std::cout << "\n=== Limitations ===" << std::endl;
    
    std::cout << "1. Number of identifiers must match number of elements" << std::endl;
    std::cout << "2. Cannot use structured binding with private members" << std::endl;
    std::cout << "3. Cannot use with classes that have get<> overloaded" << std::endl;
    std::cout << "4. Cannot have nested structured bindings in single declaration\n" << std::endl;
}

// ============ 6. MODULES (C++20) ============

#ifdef __cpp_modules
/*
// math.ixx (module interface file)
export module math;

export int add(int a, int b) {
    return a + b;
}

export double pi = 3.141592653589793;

// main.cpp
import math;
import <iostream>;

int main() {
    std::cout << "2 + 3 = " << add(2, 3) << std::endl;
    std::cout << "Pi = " << pi << std::endl;
    return 0;
}
*/
#endif

void demonstrate_modules() {
    std::cout << "============ MODULES (C++20) ============\n" << std::endl;
    
    std::cout << "=== Problems with Headers ===" << std::endl;
    std::cout << "1. Textual inclusion (copy-paste)" << std::endl;
    std::cout << "2. Slow compilation (process same headers repeatedly)" << std::endl;
    std::cout << "3. Order dependencies" << std::endl;
    std::cout << "4. Macro pollution" << std::endl;
    std::cout << "5. One Definition Rule violations\n" << std::endl;
    
    std::cout << "=== Modules Solution ===" << std::endl;
    std::cout << "1. Compiled once, cached" << std::endl;
    std::cout << "2. No textual inclusion" << std::endl;
    std::cout << "3. Faster compilation" << std::endl;
    std::cout << "4. Better encapsulation" << std::endl;
    std::cout << "5. No ODR violations\n" << std::endl;
    
    std::cout << "=== Basic Syntax ===" << std::endl;
    std::cout << "// Module interface (math.ixx)" << std::endl;
    std::cout << "export module math;" << std::endl;
    std::cout << "export int add(int a, int b) { return a + b; }" << std::endl;
    std::cout << std::endl;
    std::cout << "// Client code" << std::endl;
    std::cout << "import math;" << std::cout;
    std::cout << "import <iostream>;  // Import header units" << std::endl;
    
    std::cout << "\n=== Module Partitions ===" << std::endl;
    std::cout << "// math-core.ixx" << std::endl;
    std::cout << "export module math:core;" << std::endl;
    std::cout << "export int add(int a, int b);" << std::endl;
    std::cout << std::endl;
    std::cout << "// math.ixx" << std::endl;
    std::cout << "export module math;" << std::endl;
    std::cout << "export import :core;" << std::endl;
    
    std::cout << "\n=== Transition from Headers ===" << std::endl;
    std::cout << "// Legacy header wrapper" << std::endl;
    std::cout << "export module legacy;" << std::endl;
    std::cout << "export {" << std::endl;
    std::cout << "    #include \"old_header.h\"" << std::endl;
    std::cout << "}" << std::endl;
}

// ============ 7. COROUTINES (C++20) ============

#if __cpp_coroutines

#include <coroutine>
#include <future>

// Simple coroutine example
struct Generator {
    struct promise_type {
        int current_value;
        
        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void unhandled_exception() { std::terminate(); }
        
        std::suspend_always yield_value(int value) {
            current_value = value;
            return {};
        }
        
        void return_void() {}
    };
    
    std::coroutine_handle<promise_type> handle;
    
    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }
    
    int next() {
        handle.resume();
        return handle.promise().current_value;
    }
    
    bool done() {
        return handle.done();
    }
};

Generator sequence() {
    int i = 0;
    while (true) {
        co_yield i++;  // Suspend and return value
    }
}

#endif

void demonstrate_coroutines() {
    std::cout << "============ COROUTINES (C++20) ============\n" << std::endl;
    
    std::cout << "=== What are Coroutines? ===" << std::endl;
    std::cout << "Functions that can be suspended and resumed" << std::endl;
    std::cout << "Maintain state between calls" << std::endl;
    std::cout << "Enable asynchronous programming\n" << std::endl;
    
    std::cout << "=== Keywords ===" << std::endl;
    std::cout << "co_await - suspend until operation completes" << std::endl;
    std::cout << "co_yield - suspend and return value" << std::endl;
    std::cout << "co_return - complete coroutine\n" << std::endl;
    
    #if __cpp_coroutines
    std::cout << "=== Simple Generator Example ===" << std::endl;
    
    Generator gen = sequence();
    for (int i = 0; i < 5; ++i) {
        std::cout << gen.next() << " ";
    }
    std::cout << std::endl;
    
    #else
    std::cout << "Coroutines not supported in this compiler" << std::endl;
    #endif
    
    std::cout << "\n=== Use Cases ===" << std::endl;
    std::cout << "1. Generators (lazy sequences)" << std::endl;
    std::cout << "2. Asynchronous I/O" << std::cout;
    std::cout << "3. State machines" << std::endl;
    std::cout << "4. Cooperative multitasking\n" << std::endl;
    
    std::cout << "=== Coroutine Types ===" << std::endl;
    std::cout << "1. Generator<T> - yields values" << std::endl;
    std::cout << "2. Task<T> - represents async operation" << std::endl;
    std::cout << "3. Lazy<T> - deferred computation" << std::endl;
}

// ============ 8. THREE-WAY COMPARISON (C++20) ============

class Version {
    int major, minor, patch;
public:
    Version(int mj, int mn, int pt) : major(mj), minor(mn), patch(pt) {}
    
    // Define spaceship operator
    auto operator<=>(const Version& other) const = default;
    // Generates: ==, !=, <, <=, >, >=
    
    // Or custom implementation:
    /*
    auto operator<=>(const Version& other) const {
        if (auto cmp = major <=> other.major; cmp != 0) return cmp;
        if (auto cmp = minor <=> other.minor; cmp != 0) return cmp;
        return patch <=> other.patch;
    }
    */
    
    // Can still define custom equality if needed
    bool operator==(const Version& other) const {
        return major == other.major && minor == other.minor && patch == other.patch;
    }
};

void demonstrate_three_way() {
    std::cout << "============ THREE-WAY COMPARISON (C++20) ============\n" << std::endl;
    
    // ============ Comparison Categories ============
    std::cout << "=== Comparison Categories ===" << std::endl;
    
    std::cout << "std::strong_ordering:" << std::endl;
    std::cout << "  • Values are exactly comparable" << std::endl;
    std::cout << "  • Examples: integers, pointers" << std::endl;
    
    std::cout << "\nstd::weak_ordering:" << std::endl;
    std::cout << "  • Values comparable but not exactly" << std::endl;
    std::cout << "  • Example: case-insensitive strings" << std::endl;
    
    std::cout << "\nstd::partial_ordering:" << std::endl;
    std::cout << "  • Some values may not be comparable" << std::endl;
    std::cout << "  • Example: floating point (NaN)" << std::endl;
    
    // ============ Spaceship Operator Examples ============
    std::cout << "\n=== Spaceship Operator Examples ===" << std::endl;
    
    Version v1{1, 2, 3};
    Version v2{1, 2, 4};
    Version v3{1, 2, 3};
    
    std::cout << "v1{1,2,3} < v2{1,2,4}: " << (v1 < v2) << std::endl;
    std::cout << "v1 == v3: " << (v1 == v3) << std::endl;
    std::cout << "v1 <=> v2: ";
    
    auto result = v1 <=> v2;
    if (result < 0) std::cout << "less" << std::endl;
    else if (result > 0) std::cout << "greater" << std::endl;
    else std::cout << "equal" << std::endl;
    
    // ============ Defaulted Comparisons ============
    std::cout << "\n=== Defaulted Comparisons ===" << std::endl;
    
    struct Point3D {
        int x, y, z;
        
        // Generate all comparison operators
        auto operator<=>(const Point3D&) const = default;
    };
    
    Point3D p1{1, 2, 3};
    Point3D p2{1, 2, 4};
    
    std::cout << "p1 < p2: " << (p1 < p2) << std::endl;
    std::cout << "p1 == p2: " << (p1 == p2) << std::endl;
    
    // ============ With Inheritance ============
    std::cout << "\n=== With Inheritance ===" << std::endl;
    
    struct Base {
        int id;
        auto operator<=>(const Base&) const = default;
    };
    
    struct Derived : Base {
        std::string name;
        
        auto operator<=>(const Derived& other) const {
            if (auto cmp = static_cast<const Base&>(*this) <=> static_cast<const Base&>(other); 
                cmp != 0) return cmp;
            return name <=> other.name;
        }
        
        bool operator==(const Derived& other) const {
            return static_cast<const Base&>(*this) == static_cast<const Base&>(other) 
                   && name == other.name;
        }
    };
}