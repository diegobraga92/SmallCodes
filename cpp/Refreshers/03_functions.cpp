////////* FUNCTIONS *////////

#include <iostream>
#include <vector>
#include <functional>

// ============ FUNCTION DECLARATION vs DEFINITION ============
// Declaration (prototype) - tells compiler about function
int add(int a, int b);  // No body

// Definition - actual implementation
int add(int a, int b) {
    return a + b;
}

// ============ DEFAULT ARGUMENTS ============
double calculate_price(double base, double tax_rate = 0.08, double discount = 0.0) {
    return base * (1 + tax_rate) * (1 - discount);
}

// Default arguments must be trailing
// void bad_example(int a = 0, int b) {}  // ERROR

// ============ FUNCTION OVERLOADING ============
int multiply(int a, int b) {
    std::cout << "int version: ";
    return a * b;
}

double multiply(double a, double b) {
    std::cout << "double version: ";
    return a * b;
}

double multiply(int a, double b) {
    std::cout << "mixed version: ";
    return a * b;
}

// ============ INLINE FUNCTIONS ============
// Suggestion to compiler: insert code directly instead of calling
inline int square(int x) {
    return x * x;
}

// Inline member functions
class Math {
public:
    inline int cube(int x) {  // inline keyword optional in class definition
        return x * x * x;
    }
};

// ============ CONSTEXPR FUNCTIONS (C++11) ============
// Can be evaluated at compile-time if arguments are constant
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

// C++14: constexpr functions can have loops
constexpr int factorial14(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

void demonstrate_functions() {
    std::cout << "============ FUNCTIONS ============\n" << std::endl;
    
    // ============ FUNCTION CALLS ============
    std::cout << "=== Basic Function Calls ===" << std::endl;
    
    int sum = add(10, 20);
    std::cout << "add(10, 20) = " << sum << std::endl;
    
    // ============ DEFAULT ARGUMENTS ============
    std::cout << "\n=== Default Arguments ===" << std::endl;
    
    std::cout << "calculate_price(100.0) = " << calculate_price(100.0) << std::endl;
    std::cout << "calculate_price(100.0, 0.1) = " << calculate_price(100.0, 0.1) << std::endl;
    std::cout << "calculate_price(100.0, 0.08, 0.1) = " 
              << calculate_price(100.0, 0.08, 0.1) << std::endl;
    
    // Can't skip arguments (except trailing ones with defaults)
    // calculate_price(100.0, , 0.1);  // ERROR
    
    // ============ FUNCTION OVERLOADING ============
    std::cout << "\n=== Function Overloading ===" << std::endl;
    
    std::cout << multiply(3, 4) << std::endl;      // Calls int version
    std::cout << multiply(3.0, 4.0) << std::endl;  // Calls double version
    std::cout << multiply(3, 4.0) << std::endl;    // Calls mixed version
    
    // Overload resolution rules:
    // 1. Exact match
    // 2. Promotion (char → int, float → double)
    // 3. Standard conversion (int → double)
    // 4. User-defined conversion
    
    // Ambiguity example
    // void f(int);
    // void f(double);
    // f(3.14f);  // Ambiguous: float promotes to double or converts to int?
    
    // ============ PASS BY VALUE vs REFERENCE ============
    std::cout << "\n=== Pass by Value vs Reference ===" << std::endl;
    
    auto modify_by_value = [](int x) {
        x = 100;  // Only modifies local copy
    };
    
    auto modify_by_reference = [](int& x) {
        x = 100;  // Modifies original
    };
    
    auto modify_by_const_reference = [](const int& x) {
        // x = 100;  // ERROR: can't modify const reference
        return x * 2;
    };
    
    auto modify_by_pointer = [](int* x) {
        if (x) *x = 100;  // Modifies original through pointer
    };
    
    int val = 10;
    std::cout << "Original: " << val << std::endl;
    
    modify_by_value(val);
    std::cout << "After by-value: " << val << std::endl;
    
    modify_by_reference(val);
    std::cout << "After by-reference: " << val << std::endl;
    
    modify_by_pointer(&val);
    std::cout << "After by-pointer: " << val << std::endl;
    
    // Guidelines:
    // - Small, cheap-to-copy types (int, double): pass by value
    // - Large types (vector, string): pass by const reference
    // - Need to modify original: pass by reference
    // - Optional parameters: pass by pointer (or use std::optional)
    
    // ============ INLINE FUNCTIONS ============
    std::cout << "\n=== Inline Functions ===" << std::endl;
    
    int result = square(5);  // Compiler may insert code directly: 5 * 5
    
    // Inline is a REQUEST, not a command. Compiler may ignore it if:
    // 1. Function is too large
    // 2. Function is recursive
    // 3. Function address is taken
    // 4. Compiler optimization settings
    
    // Modern compilers are good at inlining automatically
    // Use inline primarily for header-only libraries
    
    // ============ CONSTEXPR FUNCTIONS ============
    std::cout << "\n=== constexpr Functions ===" << std::endl;
    
    // Can be used at compile-time
    constexpr int fact5 = factorial(5);  // Evaluated at compile-time
    int x = 5;
    int fact_x = factorial(x);  // Evaluated at runtime
    
    std::cout << "factorial(5) at compile-time: " << fact5 << std::endl;
    std::cout << "factorial(x) at runtime: " << fact_x << std::endl;
    
    // constexpr implies inline
    // consteval (C++20): MUST be evaluated at compile-time
    
    // ============ TRAILING RETURN TYPE (C++11) ============
    std::cout << "\n=== Trailing Return Type ===" << std::endl;
    
    auto complex_function(int x, double y) -> double {
        return x * y;
    }
    
    // Useful with templates and decltype
    template<typename T, typename U>
    auto add(T t, U u) -> decltype(t + u) {
        return t + u;
    }
    
    // ============ LAMBDA FUNCTIONS (C++11) ============
    std::cout << "\n=== Lambda Functions ===" << std::endl;
    
    // Basic lambda
    auto lambda1 = []() {
        std::cout << "Hello from lambda!" << std::endl;
    };
    lambda1();
    
    // Lambda with parameters and return type
    auto add_lambda = [](int a, int b) -> int {
        return a + b;
    };
    std::cout << "Lambda add: " << add_lambda(10, 20) << std::endl;
    
    // Capture clauses
    int external = 100;
    
    // [=] capture by value (everything)
    auto capture_by_value = [=]() {
        // external is a copy
        return external + 10;
        // external = 200;  // ERROR: can't modify copy
    };
    
    // [&] capture by reference
    auto capture_by_reference = [&]() {
        external = 200;  // Modifies original
        return external;
    };
    
    // Specific captures
    int a = 1, b = 2, c = 3;
    auto specific = [a, &b, c = c + 10]() {  // a by value, b by ref, c init-capture
        // a is copy, b is reference, c is new variable initialized to 13
        return a + b + c;
    };
    
    // mutable lambda (allows modifying captured-by-value variables)
    auto counter = [count = 0]() mutable {
        return ++count;
    };
    
    std::cout << "Counter: " << counter() << ", " << counter() << std::endl;
    
    // Generic lambda (C++14)
    auto generic = [](auto x, auto y) {
        return x + y;
    };
    std::cout << "Generic lambda: " << generic(3, 4) << ", " 
              << generic(3.1, 4.2) << std::endl;

    // Lambda for stdlib functions
    std::vector<int> values = {3, 7, 8, 5, 2};

    auto it = std::find_if(values.begin(), values.end(),
                           [](int n) { return n % 2 == 0; });

    if (it != values.end())
        std::cout << "First even number: " << *it << '\n';
    
    // ============ FUNCTION POINTERS ============
    std::cout << "\n=== Function Pointers ===" << std::endl;
    
    // Pointer to function
    int (*func_ptr)(int, int) = &add;
    std::cout << "Function pointer: " << func_ptr(10, 20) << std::endl;
    
    // Array of function pointers
    int (*operations[2])(int, int) = {add, multiply};
    std::cout << "operations[0](10, 20): " << operations[0](10, 20) << std::endl;
    std::cout << "operations[1](10, 20): " << operations[1](10, 20) << std::endl;
    
    // std::function (C++11) - more flexible
    std::function<int(int, int)> func_obj = add;
    std::cout << "std::function: " << func_obj(10, 20) << std::endl;
    
    // Can store lambdas, function objects, etc.
    func_obj = [](int a, int b) { return a - b; };
    std::cout << "std::function with lambda: " << func_obj(20, 10) << std::endl;
    
    // ============ RETURN TYPE DEDUCTION (C++14) ============
    std::cout << "\n=== Return Type Deduction (C++14) ===" << std::endl;
    
    auto deduce_return(int x) {  // Compiler deduces return type
        if (x > 0) {
            return x * 1.5;  // double
        } else {
            return x * 2;    // Still double (consistent type!)
        }
    }
    
    // All return statements must deduce to same type
    /*
    auto bad_deduction(bool flag) {
        if (flag) {
            return 10;    // int
        } else {
            return 10.5;  // double - ERROR: inconsistent
        }
    }
    */
    
    // ============ MAIN FUNCTION VARIATIONS ============
    std::cout << "\n=== Main Function ===" << std::endl;
    
    // Standard signature
    // int main() { ... }
    
    // With command line arguments
    // int main(int argc, char* argv[]) { ... }
    
    // Return 0 is optional (compiler adds it if missing)
    // main is the only function where this is true!
}

// ============ RECURSIVE FUNCTIONS ============
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Tail recursion (some compilers can optimize)
int factorial_tail(int n, int accumulator = 1) {
    if (n <= 1) return accumulator;
    return factorial_tail(n - 1, n * accumulator);
}

int main() {
    demonstrate_functions();
    return 0;
}


////////* OVERLOADING *////////

#include <iostream>
#include <string>
#include <vector>
#include <cmath>

// ============ BASIC FUNCTION OVERLOADING ============

// Overloaded functions have same name but different parameters
void print(int value) {
    std::cout << "Integer: " << value << std::endl;
}

void print(double value) {
    std::cout << "Double: " << value << std::endl;
}

void print(const std::string& value) {
    std::cout << "String: " << value << std::endl;
}

void print(const char* value) {
    std::cout << "C-string: " << value << std::endl;
}

// Overloading with different number of parameters
void display() {
    std::cout << "No arguments" << std::endl;
}

void display(int a) {
    std::cout << "One argument: " << a << std::endl;
}

void display(int a, int b) {
    std::cout << "Two arguments: " << a << ", " << b << std::endl;
}

// Overloading with const/non-const parameters
void process(int& value) {
    std::cout << "Non-const reference: can modify" << std::endl;
    value = 100;
}

void process(const int& value) {
    std::cout << "Const reference: read-only, value = " << value << std::endl;
}

// Overloading with pointer vs reference
void handle(int* ptr) {
    if (ptr) {
        std::cout << "Pointer to int: " << *ptr << std::endl;
    } else {
        std::cout << "Null pointer" << std::endl;
    }
}

void handle(int& ref) {
    std::cout << "Reference to int: " << ref << std::endl;
}

void demonstrate_function_overloading() {
    std::cout << "============ FUNCTION OVERLOADING ============\n" << std::endl;
    
    // ============ BASIC OVERLOADING EXAMPLES ============
    std::cout << "=== Basic Overloading Examples ===" << std::endl;
    
    print(42);                 // Calls print(int)
    print(3.14159);           // Calls print(double)
    print("Hello");           // Calls print(const char*)
    print(std::string("World")); // Calls print(const std::string&)
    
    std::cout << std::endl;
    
    display();                // Calls display()
    display(10);              // Calls display(int)
    display(20, 30);          // Calls display(int, int)
    
    std::cout << std::endl;
    
    // ============ OVERLOAD RESOLUTION RULES ============
    std::cout << "=== Overload Resolution Rules ===" << std::endl;
    std::cout << "Compiler chooses the BEST match in this order:" << std::endl;
    std::cout << "1. Exact match" << std::endl;
    std::cout << "2. Promotion (e.g., char → int, float → double)" << std::endl;
    std::cout << "3. Standard conversion (e.g., int → double)" << std::endl;
    std::cout << "4. User-defined conversion" << std::endl;
    std::cout << "5. Variadic functions (...)\n" << std::endl;
    
    // Example demonstrating rules:
    void func(int);
    void func(double);
    
    char c = 'A';
    func(c);     // Calls func(int) - char promotes to int (rule 2)
    func(3.14f); // Calls func(double) - float promotes to double (rule 2)
    
    short s = 5;
    func(s);     // Calls func(int) - short promotes to int (rule 2)
    
    // ============ CONST OVERLOADING ============
    std::cout << "=== Const Overloading ===" << std::endl;
    
    int x = 42;
    const int y = 100;
    
    process(x);  // Calls non-const version (exact match for non-const)
    process(y);  // Calls const version (exact match for const)
    process(50); // Calls const version (temporary binds to const ref)
    
    std::cout << "x after process: " << x << std::endl;
    
    // ============ POINTER VS REFERENCE OVERLOADING ============
    std::cout << "\n=== Pointer vs Reference Overloading ===" << std::endl;
    
    handle(&x);  // Calls pointer version
    handle(x);   // Calls reference version
    handle(nullptr); // Calls pointer version
    
    // ============ AMBIGUOUS OVERLOADS ============
    std::cout << "\n=== Ambiguous Overloads ===" << std::endl;
    
    // Example of ambiguous overload
    /*
    void ambiguous(int);
    void ambiguous(double);
    
    ambiguous(3.14f); // AMBIGUOUS: float → int OR float → double?
    */
    
    // Solution: add explicit float version or cast
    void ambiguous(int);
    void ambiguous(double);
    void ambiguous(float);  // Resolves ambiguity
    
    // ============ DEFAULT ARGUMENTS & OVERLOADING ============
    std::cout << "\n=== Default Arguments & Overloading ===" << std::endl;
    
    void with_default(int a, int b = 0);
    void with_default(int a);
    
    // with_default(5); // AMBIGUOUS: which one to call?
    
    // Better design:
    void better(int a);           // One parameter
    void better(int a, int b);    // Two parameters (no defaults)
    
    // ============ FUNCTION OVERLOADING IN CLASSES ============
    std::cout << "\n=== Overloading in Classes ===" << std::endl;
    
    class Calculator {
    public:
        // Overloaded member functions
        int add(int a, int b) {
            return a + b;
        }
        
        double add(double a, double b) {
            return a + b;
        }
        
        // Overloading with const member functions
        void display() const {
            std::cout << "Const display" << std::endl;
        }
        
        void display() {
            std::cout << "Non-const display" << std::endl;
        }
    };
    
    Calculator calc;
    const Calculator const_calc;
    
    std::cout << "calc.add(1, 2) = " << calc.add(1, 2) << std::endl;
    std::cout << "calc.add(1.5, 2.5) = " << calc.add(1.5, 2.5) << std::endl;
    
    calc.display();        // Calls non-const version
    const_calc.display();  // Calls const version
    
    // ============ TEMPLATES & OVERLOADING ============
    std::cout << "\n=== Templates & Overloading ===" << std::endl;
    
    // Template function
    template<typename T>
    T maximum(T a, T b) {
        std::cout << "Template version: ";
        return (a > b) ? a : b;
    }
    
    // Overloaded non-template version
    const char* maximum(const char* a, const char* b) {
        std::cout << "Specialized C-string version: ";
        return (std::strcmp(a, b) > 0) ? a : b;
    }
    
    std::cout << maximum(10, 20) << std::endl;       // Calls template version
    std::cout << maximum("apple", "banana") << std::endl; // Calls specialized version
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Overload for semantic similarity" << std::endl;
    std::cout << "   - Same operation on different types" << std::endl;
    std::cout << "   - Different numbers of parameters" << std::endl;
    
    std::cout << "\n2. Avoid ambiguous overloads" << std::endl;
    std::cout << "   - Watch for implicit conversions" << std::endl;
    std::cout << "   - Be careful with default arguments" << std::endl;
    
    std::cout << "\n3. Use const overloading for const correctness" << std::endl;
    
    std::cout << "\n4. Consider templates for type-generic operations" << std::endl;
    
    std::cout << "\n5. Document overloaded functions clearly" << std::endl;
    
    // ============ COMMON USE CASES ============
    std::cout << "\n=== Common Use Cases ===" << std::endl;
    
    std::cout << "1. Constructor overloading:" << std::endl;
    class Person {
        std::string name;
        int age;
    public:
        Person() : name("Unknown"), age(0) {}  // Default
        Person(const std::string& n) : name(n), age(0) {}  // Name only
        Person(const std::string& n, int a) : name(n), age(a) {}  // Full
    };
    
    std::cout << "\n2. Operator overloading (special case):" << std::endl;
    class Complex {
        double real, imag;
    public:
        Complex operator+(const Complex& other) const {
            return Complex(real + other.real, imag + other.imag);
        }
        Complex operator+(double value) const {
            return Complex(real + value, imag);
        }
    };
    
    std::cout << "\n3. Stream insertion/extraction:" << std::endl;
    // std::cout << value works for many types due to overloading
}

// ============ MORE ADVANCED EXAMPLES ============

// Overloading based on value category (C++11)
void handle_value(int&& value) {
    std::cout << "Rvalue reference: " << value << std::endl;
}

void handle_value(const int&& value) {
    std::cout << "Const rvalue reference: " << value << std::endl;
}

// SFINAE-based overloading (advanced)
template<typename T>
typename std::enable_if<std::is_integral<T>::value, void>::type
process_integral(T value) {
    std::cout << "Integral type: " << value << std::endl;
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, void>::type
process_integral(T value) {
    std::cout << "Floating point type: " << value << std::endl;
}

int main() {
    demonstrate_function_overloading();
    
    // Test value category overloading
    int val = 42;
    handle_value(100);          // Calls rvalue version
    handle_value(std::move(val)); // Calls rvalue version
    handle_value(val);          // ERROR: no lvalue version
    
    // Test SFINAE overloading
    process_integral(10);       // Calls integral version
    process_integral(3.14);     // Calls floating point version
    
    return 0;
}

////////* CONSTEXPR FUNCTIONS *////////

#include <iostream>
#include <array>
#include <type_traits>

// ============ BASIC CONSTEXPR FUNCTIONS ============

// constexpr indicates function can be evaluated at compile-time
// if given compile-time constants as arguments

// Simple constexpr function (C++11)
constexpr int square(int x) {
    return x * x;
}

// constexpr function with conditional (C++11)
constexpr int factorial(int n) {
    // C++11: constexpr functions can only have a return statement
    // and very limited other statements
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

// C++14: constexpr functions can have loops and variables
constexpr int factorial14(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// constexpr function with multiple statements (C++14)
constexpr int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// constexpr function returning custom type
struct Point {
    int x, y;
    
    // constexpr constructor
    constexpr Point(int x, int y) : x(x), y(y) {}
    
    // constexpr member function
    constexpr int manhattan_distance() const {
        return x + y;  // Simplified for example
    }
};

// constexpr function creating objects
constexpr Point create_point(int x, int y) {
    return Point(x, y);
}

// constexpr function with arrays
template<std::size_t N>
constexpr std::array<int, N> create_array() {
    std::array<int, N> arr{};
    for (std::size_t i = 0; i < N; ++i) {
        arr[i] = i * i;
    }
    return arr;
}

void demonstrate_constexpr_functions() {
    std::cout << "============ CONSTEXPR FUNCTIONS ============\n" << std::endl;
    
    // ============ WHAT IS CONSTEXPR? ============
    std::cout << "=== What is constexpr? ===" << std::endl;
    std::cout << "constexpr indicates that:" << std::endl;
    std::cout << "1. Function CAN be evaluated at compile-time" << std::endl;
    std::cout << "2. Given constant expressions as arguments" << std::endl;
    std::cout << "3. Can also be used at runtime" << std::endl;
    std::cout << "4. Implicitly inline\n" << std::endl;
    
    // ============ COMPILE-TIME VS RUNTIME ============
    std::cout << "=== Compile-time vs Runtime Evaluation ===" << std::endl;
    
    // Compile-time evaluation
    constexpr int compile_time_result = square(5);  // Evaluated during compilation
    std::cout << "square(5) at compile-time: " << compile_time_result << std::endl;
    
    // Can be used where constant expressions are required
    int array1[factorial(5)];  // OK: array size known at compile-time
    std::cout << "Array size using factorial(5): " << sizeof(array1)/sizeof(array1[0]) << std::endl;
    
    // Runtime evaluation
    int runtime_value;
    std::cout << "\nEnter a number: ";
    std::cin >> runtime_value;
    
    int runtime_result = square(runtime_value);  // Evaluated at runtime
    std::cout << "square(" << runtime_value << ") at runtime: " << runtime_result << std::endl;
    
    // Mixed usage
    const int constant_value = 10;
    int mixed_result = square(constant_value);  // May be compile-time or runtime
    
    // ============ CONSTEXPR VARIABLES ============
    std::cout << "\n=== constexpr Variables ===" << std::endl;
    
    // constexpr variables MUST be initialized with constant expression
    constexpr int max_size = 100;           // OK: literal is constant
    constexpr int computed = square(10);    // OK: square(10) is constant expression
    
    // constexpr vs const
    const int const_var = 42;        // Can be initialized at runtime
    constexpr int constexpr_var = 42; // MUST be initialized at compile-time
    
    std::cout << "constexpr max_size: " << max_size << std::endl;
    std::cout << "constexpr computed: " << computed << std::endl;
    
    // ============ CONSTEXPR WITH CUSTOM TYPES ============
    std::cout << "\n=== constexpr with Custom Types ===" << std::endl;
    
    // Compile-time object creation
    constexpr Point origin = create_point(0, 0);
    constexpr Point p(3, 4);
    
    std::cout << "Point p: (" << p.x << ", " << p.y << ")" << std::endl;
    std::cout << "Manhattan distance: " << p.manhattan_distance() << std::endl;
    
    // Can use in constant expressions
    constexpr int distance = p.manhattan_distance();
    std::cout << "Compile-time distance: " << distance << std::endl;
    
    // ============ CONSTEXPR WITH ARRAYS AND LOOPS ============
    std::cout << "\n=== constexpr with Arrays (C++14) ===" << std::endl;
    
    // Compile-time array generation
    constexpr auto squares = create_array<5>();
    
    std::cout << "Compile-time generated array: ";
    for (int val : squares) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
    
    // ============ CONSTEXPR IF (C++17) ============
    std::cout << "\n=== constexpr if (C++17) ===" << std::endl;
    
    // constexpr if allows compile-time conditional compilation
    template<typename T>
    constexpr auto get_value(T t) {
        if constexpr (std::is_pointer_v<T>) {
            return *t;  // Dereference if pointer
        } else {
            return t;   // Return directly otherwise
        }
    }
    
    int value = 42;
    int* ptr = &value;
    
    std::cout << "get_value(value): " << get_value(value) << std::endl;
    std::cout << "get_value(ptr): " << get_value(ptr) << std::endl;
    
    // ============ CONSTEXPR LIMITATIONS ============
    std::cout << "\n=== constexpr Limitations ===" << std::endl;
    
    std::cout << "C++11 constexpr functions CANNOT:" << std::endl;
    std::cout << "• Have loops (except recursion)" << std::endl;
    std::cout << "• Have variables (except parameters)" << std::endl;
    std::cout << "• Call non-constexpr functions" << std::endl;
    std::cout << "• Have try-catch blocks" << std::endl;
    
    std::cout << "\nC++14 relaxed many restrictions:" << std::endl;
    std::cout << "• Can have loops" << std::endl;
    std::cout << "• Can have variables" << std::endl;
    std::cout << "• Can have if-else statements" << std::endl;
    
    std::cout << "\nC++20 added even more:" << std::endl;
    std::cout << "• Can have virtual functions" << std::endl;
    std::cout << "• Can use try-catch (but not throw)" << std::endl;
    std::cout << "• Can allocate memory (with restrictions)" << std::endl;
    
    // ============ PRACTICAL EXAMPLES ============
    std::cout << "\n=== Practical Examples ===" << std::endl;
    
    // 1. Compile-time configuration
    constexpr int BUFFER_SIZE = 1024;
    constexpr double PI = 3.141592653589793;
    constexpr int MAX_RETRIES = 3;
    
    // 2. Compile-time computations
    constexpr int array_size = 100;
    constexpr int total_elements = array_size * array_size;
    
    // 3. Template metaprogramming replacement
    // Old way with templates:
    template<int N>
    struct Factorial {
        static const int value = N * Factorial<N-1>::value;
    };
    
    template<>
    struct Factorial<0> {
        static const int value = 1;
    };
    
    // New way with constexpr:
    constexpr int factorial_constexpr(int n) {
        return (n <= 1) ? 1 : n * factorial_constexpr(n - 1);
    }
    
    std::cout << "Template factorial<5>: " << Factorial<5>::value << std::endl;
    std::cout << "constexpr factorial(5): " << factorial_constexpr(5) << std::endl;
    
    // ============ CONSTEXPR VS INLINE ============
    std::cout << "\n=== constexpr vs inline ===" << std::endl;
    
    std::cout << "constexpr functions:" << std::endl;
    std::cout << "• Can be evaluated at compile-time" << std::endl;
    std::cout << "• Implicitly inline" << std::endl;
    std::cout << "• Have restrictions on implementation" << std::endl;
    
    std::cout << "\ninline functions:" << std::endl;
    std::cout << "• Suggestion to compiler to inline calls" << std::endl;
    std::cout << "• No compile-time evaluation guarantee" << std::endl;
    std::cout << "• No implementation restrictions" << std::endl;
    
    // ============ CONSTEVAL (C++20) ============
    std::cout << "\n=== consteval (C++20) ===" << std::endl;
    
    // consteval functions MUST be evaluated at compile-time
    #if __cplusplus >= 202002L
    /*
    consteval int must_be_compile_time(int x) {
        return x * x;
    }
    
    constexpr int a = must_be_compile_time(5);  // OK
    int runtime_val;
    std::cin >> runtime_val;
    // int b = must_be_compile_time(runtime_val);  // ERROR: not compile-time
    */
    #endif
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Use constexpr for functions that can be compile-time evaluated" << std::endl;
    std::cout << "2. Mark constructors constexpr when possible" << std::endl;
    std::cout << "3. Use constexpr variables for compile-time constants" << std::endl;
    std::cout << "4. Prefer constexpr over old template metaprogramming" << std::endl;
    std::cout << "5. Use constexpr for mathematical utilities" << std::endl;
    std::cout << "6. Consider consteval for functions that must be compile-time" << std::endl;
    
    // ============ REAL-WORLD EXAMPLES ============
    std::cout << "\n=== Real-World Examples ===" << std::endl;
    
    // 1. Mathematical constants and functions
    constexpr double deg_to_rad(double deg) {
        return deg * PI / 180.0;
    }
    
    // 2. String processing at compile-time (C++20)
    constexpr std::size_t string_length(const char* str) {
        std::size_t len = 0;
        while (str[len] != '\0') {
            ++len;
        }
        return len;
    }
    
    constexpr std::size_t len = string_length("Hello");
    std::cout << "Length of 'Hello' at compile-time: " << len << std::endl;
    
    // 3. Compile-time validation
    constexpr bool is_power_of_two(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }
    
    static_assert(is_power_of_two(8), "Must be power of two");
    // static_assert(is_power_of_two(10), "Error: not power of two");
}

// ============ ADVANCED CONSTEXPR EXAMPLES ============

// Recursive constexpr function
constexpr int fibonacci(int n) {
    return (n <= 1) ? n : fibonacci(n - 1) + fibonacci(n - 2);
}

// constexpr function with multiple return points (C++14)
constexpr int absolute(int n) {
    if (n < 0) {
        return -n;
    } else {
        return n;
    }
}

// constexpr member function
class Circle {
private:
    double radius;
    
public:
    constexpr Circle(double r) : radius(r) {}
    
    constexpr double area() const {
        return 3.141592653589793 * radius * radius;
    }
    
    constexpr double circumference() const {
        return 2 * 3.141592653589793 * radius;
    }
};

// constexpr template function
template<typename T>
constexpr T min(T a, T b) {
    return (a < b) ? a : b;
}

template<typename T>
constexpr T max(T a, T b) {
    return (a > b) ? a : b;
}

// constexpr with switch (C++14)
constexpr int switch_example(int n) {
    switch (n) {
        case 1: return 10;
        case 2: return 20;
        case 3: return 30;
        default: return 0;
    }
}

int main() {
    demonstrate_constexpr_functions();
    
    // Additional tests
    std::cout << "\n=== Additional constexpr Tests ===" << std::endl;
    
    // Compile-time computations
    constexpr int fib10 = fibonacci(10);
    std::cout << "Fibonacci(10) at compile-time: " << fib10 << std::endl;
    
    constexpr Circle unit_circle(1.0);
    std::cout << "Unit circle area: " << unit_circle.area() << std::endl;
    
    constexpr int min_val = min(10, 20);
    constexpr int max_val = max(10, 20);
    std::cout << "min(10, 20): " << min_val << std::endl;
    std::cout << "max(10, 20): " << max_val << std::endl;
    
    // Using static_assert with constexpr
    static_assert(square(5) == 25, "square(5) should be 25");
    static_assert(factorial(5) == 120, "factorial(5) should be 120");
    static_assert(gcd(48, 18) == 6, "gcd(48, 18) should be 6");
    
    std::cout << "\nAll static_asserts passed!" << std::endl;
    
    return 0;
}

// ============ LAMBDA EXPRESSIONS & IIFE ============

void demonstrate_lambdas_iife() {
    std::cout << "============ LAMBDAS & IIFE ============\n" << std::endl;
    
    // ============ Lambda Features ============
    std::cout << "=== Lambda Features ===" << std::endl;
    
    // Basic lambda
    auto add = [](int a, int b) { return a + b; };
    std::cout << "add(3, 4) = " << add(3, 4) << std::endl;
    
    // With capture
    int x = 10;
    auto add_x = [x](int y) { return x + y; };
    std::cout << "add_x(5) = " << add_x(5) << std::endl;
    
    // Generic lambda (C++14)
    auto generic_add = [](auto a, auto b) { return a + b; };
    std::cout << "generic_add(3, 4.5) = " << generic_add(3, 4.5) << std::endl;
    
    // Mutable lambda
    auto counter = [count = 0]() mutable {
        return ++count;
    };
    std::cout << "Counter: " << counter() << ", " << counter() << std::endl;
    
    // ============ IIFE (Immediately Invoked Function Expression) ============
    std::cout << "\n=== IIFE Pattern ===" << std::endl;
    std::cout << "Define and invoke lambda immediately\n" << std::endl;
    
    // Basic IIFE
    int result = [](int a, int b) {
        return a * a + b * b;
    }(3, 4);
    
    std::cout << "3² + 4² = " << result << std::endl;
    
    // IIFE for complex initialization
    std::string message = [](const std::string& name) {
        return "Hello, " + name + "!";
    }("World");
    
    std::cout << "Message: " << message << std::endl;
    
    // IIFE for scope control
    auto complex_object = [&]() -> std::vector<int> {
        std::vector<int> vec;
        for (int i = 0; i < 10; ++i) {
            if (i % 2 == 0) {
                vec.push_back(i * i);
            }
        }
        return vec;
    }();
    
    std::cout << "Complex object size: " << complex_object.size() << std::endl;
    
    // ============ Use Cases for IIFE ============
    std::cout << "\n=== IIFE Use Cases ===" << std::endl;
    
    std::cout << "1. Complex initialization:" << std::endl;
    auto config = []() {
        struct Config {
            int timeout;
            std::string host;
            bool debug;
        };
        Config c;
        c.timeout = 1000;
        c.host = "localhost";
        c.debug = true;
        return c;
    }();
    
    std::cout << "Config host: " << config.host << std::endl;
    
    std::cout << "\n2. Avoiding temporary variables:" << std::endl;
    // Instead of:
    // auto temp = some_complex_calculation();
    // use_result(temp);
    
    // Use:
    // use_result([](){ return some_complex_calculation(); }());
    
    std::cout << "\n3. Limiting scope of helper variables:" << std::endl;
    {
        // Helper variables don't pollute outer scope
        auto processed = [](const std::string& input) {
            std::string temp = input;
            // Complex processing...
            return temp + " processed";
        }("input");
        std::cout << "Processed: " << processed << std::endl;
    }
    // temp is not accessible here
    
    std::cout << "\n4. One-time initialization:" << std::endl;
    static auto init_value = []() {
        std::cout << "Initializing once..." << std::endl;
        return 42;
    }();
    
    std::cout << "Init value: " << init_value << std::endl;
}