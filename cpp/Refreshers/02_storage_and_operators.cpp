////////* STORAGE CLASSES *////////

#include <iostream>
#include <thread>
#include <mutex>

// ============ EXTERN ============
// Declaration only (definition in another file)
extern int external_value;  // Tells compiler: "defined elsewhere"

// Actual definition (would normally be in separate .cpp file)
int external_value = 42;

// ============ STATIC ============
// Static global variable - internal linkage
static int static_global = 100;  // Only accessible in this file

// Static function - internal linkage
static void static_function() {
    std::cout << "Static function called" << std::endl;
}

class StorageDemo {
private:
    int instance_var;           // Each instance has its own copy
    static int class_var;       // Shared by all instances
    
public:
    // ============ STATIC MEMBER VARIABLE ============
    static int get_class_var() {
        return class_var;
    }
    
    static void set_class_var(int value) {
        class_var = value;
    }
    
    // ============ STATIC MEMBER FUNCTION ============
    // Can only access static members
    static void class_method() {
        // instance_var = 10;  // ERROR: cannot access non-static member
        class_var = 20;        // OK: accessing static member
    }
    
    // ============ MUTABLE ============
    // mutable allows modification in const member functions
    mutable int mutable_counter;
    
    void regular_method() const {
        // instance_var = 30;  // ERROR: const method
        mutable_counter = 40;  // OK: mutable can be modified
    }
};

// Static member definition (MUST be outside class)
int StorageDemo::class_var = 0;

// ============ THREAD_LOCAL (C++11) ============
thread_local int thread_specific = 0;  // Each thread has its own copy

void thread_function(int id) {
    thread_specific = id * 100;
    std::cout << "Thread " << id << ": thread_specific = " 
              << thread_specific << std::endl;
}

void demonstrate_storage_classes() {
    std::cout << "\n============ STORAGE CLASSES ============\n" << std::endl;
    
    // ============ STATIC LOCAL VARIABLES ============
    std::cout << "=== Static Local Variables ===" << std::endl;
    
    auto counter = []() {
        static int count = 0;  // Persists between calls
        return ++count;
    };
    
    std::cout << "Counter calls: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << counter() << " ";
    }
    std::cout << "\n(Persists between calls)\n" << std::endl;
    
    // Static local in recursive function
    auto recursive_with_static = [](int n) {
        static int depth = 0;
        depth++;
        
        std::cout << "Depth: " << depth << std::endl;
        
        if (n > 0) {
            recursive_with_static(n - 1);
        }
        
        depth--;
    };
    
    std::cout << "Recursive with static counter:" << std::endl;
    recursive_with_static(3);
    std::cout << std::endl;
    
    // ============ STATIC CLASS MEMBERS ============
    std::cout << "=== Static Class Members ===" << std::endl;
    
    StorageDemo obj1, obj2;
    
    obj1.set_class_var(100);
    std::cout << "obj1 set class_var to 100" << std::endl;
    std::cout << "obj2 sees class_var as: " << obj2.get_class_var() << std::endl;
    
    obj2.set_class_var(200);
    std::cout << "obj2 set class_var to 200" << std::endl;
    std::cout << "obj1 sees class_var as: " << obj1.get_class_var() << "\n" << std::endl;
    
    // ============ MUTABLE ============
    std::cout << "=== Mutable ===" << std::endl;
    
    const StorageDemo const_obj;
    const_obj.regular_method();  // Can modify mutable_counter even though const
    
    // Practical use: lazy initialization with caching
    class Cache {
    private:
        mutable std::mutex mtx;  // mutable: can lock in const methods
        mutable bool cached = false;
        mutable int cached_value;
        int compute_value() const { return 42; }  // Expensive computation
        
    public:
        int get_value() const {
            std::lock_guard<std::mutex> lock(mtx);  // OK: mutable mutex
            if (!cached) {
                cached_value = compute_value();
                cached = true;
            }
            return cached_value;
        }
    };
    
    Cache cache;
    std::cout << "Cached value: " << cache.get_value() << "\n" << std::endl;
    
    // ============ THREAD_LOCAL ============
    std::cout << "=== thread_local ===" << std::endl;
    
    // Each thread has independent copy
    std::thread t1(thread_function, 1);
    std::thread t2(thread_function, 2);
    
    thread_specific = 999;
    std::cout << "Main thread: thread_specific = " << thread_specific << std::endl;
    
    t1.join();
    t2.join();
    
    // Thread-local static
    auto thread_id_generator = []() {
        thread_local static int id = 0;  // Each thread gets its own counter
        return ++id;
    };
    
    std::cout << "\nThread-local static counter:" << std::endl;
    std::thread t3([&]() {
        std::cout << "Thread 3: " << thread_id_generator() << ", " 
                  << thread_id_generator() << std::endl;
    });
    
    std::thread t4([&]() {
        std::cout << "Thread 4: " << thread_id_generator() << ", " 
                  << thread_id_generator() << std::endl;
    });
    
    t3.join();
    t4.join();
    
    // ============ EXTERN ============
    std::cout << "\n=== extern ===" << std::endl;
    
    // extern "C" for C linkage
    extern "C" {
        int c_function();  // Declares C function with C linkage
    }
    
    // extern with const
    extern const int global_const;  // Declaration
    // Definition (typically in .cpp file)
    const int global_const = 1000;
    
    std::cout << "External const: " << global_const << std::endl;
    
    // ============ STORAGE CLASS COMBINATIONS ============
    std::cout << "\n=== Storage Class Combinations ===" << std::endl;
    
    // Valid combinations:
    thread_local static int combined = 50;  // thread-local and static
    // static extern int invalid;  // ERROR: cannot combine static and extern
    
    // Order matters (usually): thread_local static, not static thread_local
}

int main() {
    demonstrate_storage_classes();
    return 0;
}


////////* OPERATORS *////////

#include <iostream>
#include <bitset>
#include <type_traits>

class Complex {
private:
    double real, imag;
    
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    
    // ============ OPERATOR OVERLOADING ============
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
    
    Complex operator-(const Complex& other) const {
        return Complex(real - other.real, imag - other.imag);
    }
    
    Complex operator*(const Complex& other) const {
        return Complex(real * other.real - imag * other.imag,
                      real * other.imag + imag * other.real);
    }
    
    // Unary operators
    Complex operator+() const { return *this; }  // Unary plus
    Complex operator-() const { return Complex(-real, -imag); }  // Unary minus
    
    // Comparison operators
    bool operator==(const Complex& other) const {
        return real == other.real && imag == other.imag;
    }
    
    bool operator!=(const Complex& other) const {
        return !(*this == other);
    }
    
    // Increment operators
    Complex& operator++() {    // Prefix
        ++real;
        return *this;
    }
    
    Complex operator++(int) {  // Postfix (dummy int parameter)
        Complex temp = *this;
        ++real;
        return temp;
    }
    
    // Function call operator (makes it a functor)
    double operator()(double scale) const {
        return (real + imag) * scale;
    }
    
    // Subscript operator (if it made sense for this class)
    double& operator[](int index) {
        if (index == 0) return real;
        if (index == 1) return imag;
        throw std::out_of_range("Complex has only 2 components");
    }
    
    friend std::ostream& operator<<(std::ostream& os, const Complex& c);
};

std::ostream& operator<<(std::ostream& os, const Complex& c) {
    os << c.real << (c.imag >= 0 ? "+" : "") << c.imag << "i";
    return os;
}

void demonstrate_operators() {
    std::cout << "============ OPERATORS & EXPRESSIONS ============\n" << std::endl;
    
    // ============ ARITHMETIC OPERATORS ============
    std::cout << "=== Arithmetic Operators ===" << std::endl;
    
    int a = 10, b = 3;
    std::cout << a << " + " << b << " = " << (a + b) << std::endl;
    std::cout << a << " - " << b << " = " << (a - b) << std::endl;
    std::cout << a << " * " << b << " = " << (a * b) << std::endl;
    std::cout << a << " / " << b << " = " << (a / b) << " (integer division!)" << std::endl;
    std::cout << a << " % " << b << " = " << (a % b) << std::endl;
    
    double x = 10.0, y = 3.0;
    std::cout << x << " / " << y << " = " << (x / y) << " (floating division)\n" << std::endl;
    
    // ============ RELATIONAL OPERATORS ============
    std::cout << "=== Relational Operators ===" << std::endl;
    
    std::cout << a << " == " << b << ": " << (a == b) << std::endl;
    std::cout << a << " != " << b << ": " << (a != b) << std::endl;
    std::cout << a << " < " << b << ": " << (a < b) << std::endl;
    std::cout << a << " <= " << b << ": " << (a <= b) << std::endl;
    std::cout << a << " > " << b << ": " << (a > b) << std::endl;
    std::cout << a << " >= " << b << ": " << (a >= b) << "\n" << std::endl;
    
    // ============ LOGICAL OPERATORS ============
    std::cout << "=== Logical Operators ===" << std::endl;
    
    bool p = true, q = false;
    std::cout << std::boolalpha;
    std::cout << p << " && " << q << ": " << (p && q) << std::endl;
    std::cout << p << " || " << q << ": " << (p || q) << std::endl;
    std::cout << "!" << p << ": " << (!p) << std::endl;
    
    // Short-circuit evaluation
    auto expensive_check = []() {
        std::cout << "  (expensive check executed)" << std::endl;
        return true;
    };
    
    std::cout << "\nShort-circuit evaluation:" << std::endl;
    if (false && expensive_check()) {  // expensive_check NOT called
        std::cout << "This won't execute" << std::endl;
    }
    
    if (true || expensive_check()) {  // expensive_check NOT called
        std::cout << "This executes without calling expensive_check" << std::endl;
    }
    std::cout << std::noboolalpha << std::endl;
    
    // ============ BITWISE OPERATORS ============
    std::cout << "=== Bitwise Operators ===" << std::endl;
    
    unsigned char flags = 0b00001101;  // Binary literal (C++14)
    unsigned char mask = 0b00000111;
    
    std::cout << "flags: " << std::bitset<8>(flags) << std::endl;
    std::cout << "mask:  " << std::bitset<8>(mask) << std::endl;
    std::cout << "flags & mask: " << std::bitset<8>(flags & mask) << " (AND)" << std::endl;
    std::cout << "flags | mask: " << std::bitset<8>(flags | mask) << " (OR)" << std::endl;
    std::cout << "flags ^ mask: " << std::bitset<8>(flags ^ mask) << " (XOR)" << std::endl;
    std::cout << "~flags: " << std::bitset<8>(~flags) << " (NOT)" << std::endl;
    std::cout << "flags << 2: " << std::bitset<8>(flags << 2) << " (left shift)" << std::endl;
    std::cout << "flags >> 2: " << std::bitset<8>(flags >> 2) << " (right shift)\n" << std::endl;
    
    // ============ ASSIGNMENT OPERATORS ============
    std::cout << "=== Assignment Operators ===" << std::endl;
    
    int value = 10;
    value += 5;  // value = value + 5
    std::cout << "value += 5: " << value << std::endl;
    
    value -= 3;  // value = value - 3
    std::cout << "value -= 3: " << value << std::endl;
    
    value *= 2;  // value = value * 2
    std::cout << "value *= 2: " << value << std::endl;
    
    value /= 4;  // value = value / 4
    std::cout << "value /= 4: " << value << std::endl;
    
    value %= 3;  // value = value % 3
    std::cout << "value %= 3: " << value << std::endl;
    
    // Bitwise assignment operators also exist
    unsigned int bits = 0b1010;
    bits &= 0b0011;  // bits = bits & 0b0011
    std::cout << "bits &= 0b0011: " << std::bitset<4>(bits) << "\n" << std::endl;
    
    // ============ INCREMENT/DECREMENT OPERATORS ============
    std::cout << "=== Increment/Decrement Operators ===" << std::endl;
    
    int i = 5;
    std::cout << "i = " << i << std::endl;
    std::cout << "++i: " << ++i << " (prefix, then use)" << std::endl;
    std::cout << "i++: " << i++ << " (use, then postfix)" << std::endl;
    std::cout << "i after i++: " << i << std::endl;
    std::cout << "--i: " << --i << " (prefix)" << std::endl;
    std::cout << "i--: " << i-- << " (postfix)" << std::endl;
    std::cout << "i after i--: " << i << "\n" << std::endl;
    
    // ============ TERNARY (CONDITIONAL) OPERATOR ============
    std::cout << "=== Ternary Operator ===" << std::endl;
    
    int age = 20;
    std::string status = (age >= 18) ? "adult" : "minor";
    std::cout << "Age " << age << " is " << status << std::endl;
    
    // Nested ternary (use with caution)
    int score = 85;
    std::string grade = (score >= 90) ? "A" :
                       (score >= 80) ? "B" :
                       (score >= 70) ? "C" :
                       (score >= 60) ? "D" : "F";
    std::cout << "Score " << score << " gets grade " << grade << "\n" << std::endl;
    
    // ============ COMMA OPERATOR ============
    std::cout << "=== Comma Operator ===" << std::endl;
    
    // Evaluates all expressions, returns the last one
    int j = (i = 5, i + 3);  // i = 5, then j = i + 3 = 8
    std::cout << "j = (i = 5, i + 3): " << j << std::endl;
    
    // Common in for loops
    for (int k = 0, l = 10; k < 5; ++k, --l) {
        std::cout << "k=" << k << ", l=" << l << std::endl;
    }
    std::cout << std::endl;
    
    // ============ SIZEOF OPERATOR ============
    std::cout << "=== sizeof Operator ===" << std::endl;
    
    std::cout << "sizeof(int): " << sizeof(int) << " bytes" << std::endl;
    std::cout << "sizeof(double): " << sizeof(double) << " bytes" << std::endl;
    
    int arr[10];
    std::cout << "sizeof(arr): " << sizeof(arr) << " bytes (10 * sizeof(int))" << std::endl;
    std::cout << "sizeof(arr) / sizeof(arr[0]): " 
              << sizeof(arr) / sizeof(arr[0]) << " (array length)\n" << std::endl;
    
    // ============ OPERATOR OVERLOADING ============
    std::cout << "=== Operator Overloading ===" << std::endl;
    
    Complex c1(2, 3), c2(4, 5);
    std::cout << "c1 = " << c1 << std::endl;
    std::cout << "c2 = " << c2 << std::endl;
    std::cout << "c1 + c2 = " << (c1 + c2) << std::endl;
    std::cout << "c1 - c2 = " << (c1 - c2) << std::endl;
    std::cout << "c1 * c2 = " << (c1 * c2) << std::endl;
    std::cout << "-c1 = " << (-c1) << std::endl;
    std::cout << "c1 == c2: " << (c1 == c2) << std::endl;
    
    Complex c3 = c1++;
    std::cout << "c1++ (postfix): returns " << c3 << ", c1 becomes " << c1 << std::endl;
    
    Complex c4 = ++c2;
    std::cout << "++c2 (prefix): returns " << c4 << ", c2 becomes " << c2 << std::endl;
    
    std::cout << "c1(2.5) = " << c1(2.5) << " (function call operator)" << std::endl;
    std::cout << "c1[0] = " << c1[0] << ", c1[1] = " << c1[1] << " (subscript operator)\n" << std::endl;
    
    // ============ OPERATOR PRECEDENCE ============
    std::cout << "=== Operator Precedence Examples ===" << std::endl;
    
    int result1 = 2 + 3 * 4;      // Multiplication before addition
    int result2 = (2 + 3) * 4;    // Parentheses override precedence
    std::cout << "2 + 3 * 4 = " << result1 << std::endl;
    std::cout << "(2 + 3) * 4 = " << result2 << std::endl;
    
    // Tricky example
    int a1 = 5, b1 = 10, c1 = 15;
    int tricky = a1 = b1 = c1;  // Right-to-left associativity for =
    std::cout << "a1 = b1 = c1: all become " << tricky << std::endl;
    
    // Common pitfall: bitwise shift vs comparison
    int val = 5;
    bool confusing = val & 1 == 0;  // == has higher precedence than &
    // Actually evaluates as: val & (1 == 0) → val & 0 → 0
    bool correct = (val & 1) == 0;  // Use parentheses!
    std::cout << "val & 1 == 0: " << confusing << " (WRONG!)" << std::endl;
    std::cout << "(val & 1) == 0: " << correct << " (correct)" << std::endl;
    
    // ============ OPERATOR PRECEDENCE TABLE (SUMMARY) ============
    std::cout << "\n=== Operator Precedence (Highest to Lowest) ===" << std::endl;
    std::cout << "1. ::          Scope resolution" << std::endl;
    std::cout << "2. ++ --       Suffix increment/decrement" << std::endl;
    std::cout << "3. ++ --       Prefix increment/decrement, + - (unary)" << std::endl;
    std::cout << "4. * / %       Multiplication, division, modulus" << std::endl;
    std::cout << "5. + -         Addition, subtraction" << std::endl;
    std::cout << "6. << >>       Bitwise shift" << std::endl;
    std::cout << "7. < <= > >=   Relational" << std::endl;
    std::cout << "8. == !=       Equality" << std::endl;
    std::cout << "9. &           Bitwise AND" << std::endl;
    std::cout << "10. ^          Bitwise XOR" << std::endl;
    std::cout << "11. |          Bitwise OR" << std::endl;
    std::cout << "12. &&         Logical AND" << std::endl;
    std::cout << "13. ||         Logical OR" << std::endl;
    std::cout << "14. ?:         Ternary conditional" << std::endl;
    std::cout << "15. = += -= etc. Assignment" << std::endl;
    std::cout << "16. ,          Comma" << std::endl;
    std::cout << "\nRULE: When in doubt, use parentheses!" << std::endl;
}

int main() {
    demonstrate_operators();
    return 0;
}


////////* CONST CORRECTNESS *////////

#include <iostream>
#include <string>
#include <vector>

// ============ const VARIABLES ============
const int MAX_SIZE = 100;  // Must be initialized, cannot be modified

// const vs constexpr
constexpr int COMPILE_TIME_CONST = 200;  // Known at compile-time

// ============ const PARAMETERS ============
void print_string(const std::string& str) {
    // str cannot be modified
    // str.clear();  // ERROR
    std::cout << str << std::endl;
}

// ============ const MEMBER FUNCTIONS ============
class Account {
private:
    mutable int login_count;  // Can be modified in const functions
    double balance;
    std::string name;
    
public:
    Account(const std::string& n, double b) : name(n), balance(b), login_count(0) {}
    
    // const member function - can be called on const objects
    double get_balance() const {
        // balance = 0;  // ERROR: cannot modify in const function
        login_count++;  // OK: mutable member
        return balance;
    }
    
    // Non-const member function
    void deposit(double amount) {
        balance += amount;
    }
    
    // Overloading based on const
    const std::string& get_name() const {
        std::cout << "const version called" << std::endl;
        return name;
    }
    
    std::string& get_name() {
        std::cout << "non-const version called" << std::endl;
        return name;
    }
    
    // constexpr member function (C++14)
    constexpr double get_balance_constexpr() const {
        return balance;
    }
};

// ============ constexpr FUNCTIONS ============
constexpr int square(int x) {
    return x * x;
}

// C++14: constexpr functions can have loops
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// ============ CONSTEXPR VARIABLES ============
constexpr int ARRAY_SIZE = square(10);  // Computed at compile-time

void demonstrate_const_correctness() {
    std::cout << "============ const CORRECTNESS ============\n" << std::endl;
    
    // ============ const VARIABLES ============
    std::cout << "=== const Variables ===" << std::endl;
    
    const int read_only = 42;
    // read_only = 100;  // ERROR: cannot modify const
    
    // const pointers (see pointer section)
    int value = 10;
    const int* ptr_to_const = &value;  // Can't modify through pointer
    int* const const_ptr = &value;     // Can't change pointer
    
    // ============ const vs constexpr ============
    std::cout << "\n=== const vs constexpr ===" << std::endl;
    
    // const: runtime or compile-time constant
    int runtime_value;
    std::cout << "Enter a number: ";
    std::cin >> runtime_value;
    const int runtime_const = runtime_value;  // Determined at runtime
    
    // constexpr: MUST be compile-time constant
    constexpr int compile_time = 100;  // Known at compile-time
    // constexpr int bad = runtime_value;  // ERROR: not compile-time
    
    std::cout << "runtime_const: " << runtime_const << std::endl;
    std::cout << "compile_time: " << compile_time << std::endl;
    std::cout << "square(5) at compile-time: " << square(5) << std::endl;
    std::cout << "factorial(5): " << factorial(5) << "\n" << std::endl;
    
    // ============ const MEMBER FUNCTIONS ============
    std::cout << "=== const Member Functions ===" << std::endl;
    
    Account alice("Alice", 1000.0);
    const Account bob("Bob", 2000.0);  // const object
    
    // Can call const functions on both
    std::cout << "Alice balance: " << alice.get_balance() << std::endl;
    std::cout << "Bob balance: " << bob.get_balance() << std::endl;
    
    // Can call non-const functions only on non-const objects
    alice.deposit(500.0);
    // bob.deposit(500.0);  // ERROR: cannot call non-const on const object
    
    // const overloading
    std::cout << "\nConst overloading:" << std::endl;
    std::cout << alice.get_name() << std::endl;  // Calls non-const version
    std::cout << bob.get_name() << std::endl;    // Calls const version
    
    // ============ mutable KEYWORD ============
    std::cout << "\n=== mutable ===" << std::endl;
    
    // mutable allows modification in const member functions
    // Useful for:
    // 1. Caching/memoization
    // 2. Thread synchronization (mutexes)
    // 3. Reference counting
    
    class Cache {
    private:
        mutable bool calculated = false;
        mutable int cached_value;
        int expensive_computation() const { return 42; }
        
    public:
        int get_value() const {
            if (!calculated) {
                cached_value = expensive_computation();
                calculated = true;
            }
            return cached_value;
        }
    };
    
    const Cache cache;
    std::cout << "Cached value: " << cache.get_value() << std::endl;
    
    // ============ const CORRECTNESS BENEFITS ============
    std::cout << "\n=== Benefits of const Correctness ===" << std::endl;
    
    // 1. Self-documenting code
    // 2. Compiler-enforced correctness
    // 3. Enables optimizations
    // 4. Prevents accidental modifications
    
    // ============ const WITH TEMPLATES ============
    std::cout << "\n=== const with Templates ===" << std::endl;
    
    template<typename T>
    T get_max(const T& a, const T& b) {
        return (a > b) ? a : b;
    }
    
    // const prevents modification of parameters
    // Also enables passing temporaries
    
    // ============ constexpr IN MODERN C++ ============
    std::cout << "\n=== constexpr in Modern C++ ===" << std::endl;
    
    // C++11: constexpr functions very restrictive
    // C++14: constexpr functions can have loops, variables
    // C++17: constexpr if, constexpr lambdas
    // C++20: constexpr virtual functions, try-catch, allocations
    
    // consteval (C++20): immediate functions - MUST be evaluated at compile-time
    /*
    consteval int must_be_compile_time(int x) {
        return x * x;
    }
    */
    
    // constinit (C++20): initialized at compile-time (but not const!)
    /*
    constinit int fast_init = 100;  // No runtime initialization cost
    */
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Use const by default" << std::endl;
    std::cout << "2. Pass large objects by const reference" << std::endl;
    std::cout << "3. Make member functions const when they don't modify" << std::endl;
    std::cout << "4. Use constexpr for compile-time constants" << std::endl;
    std::cout << "5. Use mutable sparingly (for caching, mutexes)" << std::endl;
    std::cout << "6. const enables compiler optimizations" << std::endl;
}

int main() {
    demonstrate_const_correctness();
    return 0;
}

// ============ 4. CONSTEXPR ============

constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

constexpr int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

template<typename T>
constexpr auto get_type_name() {
    if constexpr (std::is_integral_v<T>) {
        return "integral";
    } else if constexpr (std::is_floating_point_v<T>) {
        return "floating";
    } else {
        return "other";
    }
}

void demonstrate_constexpr() {
    std::cout << "============ CONSTEXPR ============\n" << std::endl;
    
    // ============ constexpr Variables ============
    std::cout << "=== constexpr Variables ===" << std::endl;
    
    constexpr int max_size = 100;           // Compile-time constant
    constexpr int fact5 = factorial(5);     // Computed at compile-time
    constexpr int fib10 = fibonacci(10);    // Computed at compile-time
    
    std::cout << "factorial(5) = " << fact5 << std::endl;
    std::cout << "fibonacci(10) = " << fib10 << std::endl;
    
    // Can be used where constants are required
    int array[fact5];  // Array size known at compile-time
    std::cout << "Array size: " << sizeof(array)/sizeof(array[0]) << std::endl;
    
    // ============ constexpr Functions ============
    std::cout << "\n=== constexpr Functions ===" << std::endl;
    
    // Can be used at compile-time or runtime
    int runtime_n = 10;
    int runtime_result = factorial(runtime_n);  // Evaluated at runtime
    
    std::cout << "factorial(10) at runtime: " << runtime_result << std::endl;
    
    // ============ constexpr if (C++17) ============
    std::cout << "\n=== constexpr if (C++17) ===" << std::endl;
    std::cout << "Condition evaluated at compile-time, unused branches discarded\n" << std::endl;
    
    std::cout << "Type of int: " << get_type_name<int>() << std::endl;
    std::cout << "Type of double: " << get_type_name<double>() << std::endl;
    std::cout << "Type of std::string: " << get_type_name<std::string>() << std::endl;
    
    // Example: Compile-time recursion depth limit
    template<int N>
    constexpr int sum() {
        if constexpr (N > 0) {
            return N + sum<N-1>();
        } else {
            return 0;
        }
    }
    
    std::cout << "sum<10>() = " << sum<10>() << std::endl;
    
    // ============ constexpr in C++20 ============
    std::cout << "\n=== constexpr in C++20 ===" << std::endl;
    
    // C++20 allows more in constexpr:
    // - Virtual functions
    // - try-catch (but not throw)
    // - Dynamic memory allocation (with restrictions)
    // - Changing union active members
    
    // Example: constexpr vector (C++20)
    #if __cplusplus >= 202002L
    /*
    constexpr std::vector<int> create_vector() {
        std::vector<int> vec;
        vec.push_back(1);
        vec.push_back(2);
        vec.push_back(3);
        return vec;
    }
    
    constexpr auto vec = create_vector();
    */
    #endif
}

////////* CASTING *////////

#include <iostream>
#include <typeinfo>
#include <memory>
#include <string>

class Base {
public:
    virtual ~Base() = default;
    virtual void print() const { std::cout << "Base" << std::endl; }
};

class Derived : public Base {
public:
    void print() const override { std::cout << "Derived" << std::endl; }
    void derived_only() const { std::cout << "Derived only method" << std::endl; }
};

class Unrelated {};

void demonstrate_type_conversions() {
    std::cout << "============ TYPE CONVERSIONS ============\n" << std::endl;
    
    // ============ IMPLICIT CONVERSIONS ============
    std::cout << "=== Implicit Conversions ===" << std::endl;
    
    // Numeric promotions
    char c = 'A';
    int i = c;  // char → int
    std::cout << "char 'A' to int: " << i << std::endl;
    
    float f = 3.14f;
    double d = f;  // float → double
    std::cout << "float to double: " << d << std::endl;
    
    // Numeric conversions (potential loss of data)
    double pi = 3.14159;
    int approx = pi;  // double → int (truncation)
    std::cout << "double " << pi << " to int: " << approx << std::endl;
    
    // Boolean conversions
    bool b1 = 100;    // Non-zero → true
    bool b2 = 0.0;    // Zero → false
    std::cout << "100 to bool: " << b1 << std::endl;
    std::cout << "0.0 to bool: " << b2 << std::endl;
    
    // Pointer conversions
    Derived derived;
    Base* base_ptr = &derived;  // Derived* → Base* (upcast)
    std::cout << "Derived* to Base*: OK" << std::endl;
    
    // Array to pointer decay
    int arr[3] = {1, 2, 3};
    int* arr_ptr = arr;  // int[3] → int*
    std::cout << "Array to pointer: OK\n" << std::endl;
    
    // ============ EXPLICIT CONVERSIONS (C-STYLE) ============
    std::cout << "=== C-style Casts ===" << std::endl;
    
    double price = 19.99;
    int dollars = (int)price;  // C-style cast
    std::cout << "(int)19.99 = " << dollars << std::endl;
    
    // Problems with C-style casts:
    // 1. Does different things in different contexts
    // 2. Hard to search for in code
    // 3. No compile-time checking
    // AVOID in C++!
    
    // ============ static_cast ============
    std::cout << "\n=== static_cast ===" << std::endl;
    
    // Numeric conversions
    double value = 3.14159;
    int int_value = static_cast<int>(value);  // Explicit truncation
    std::cout << "static_cast<int>(3.14159) = " << int_value << std::endl;
    
    // Pointer upcast (safe)
    Derived* d_ptr = new Derived();
    Base* b_ptr = static_cast<Base*>(d_ptr);  // Safe upcast
    b_ptr->print();
    
    // Pointer downcast (unsafe - no runtime check!)
    Base* base2 = new Derived();
    Derived* derived2 = static_cast<Derived*>(base2);  // UNSAFE if not actually Derived
    if (derived2) {
        derived2->derived_only();
    }
    
    // void* conversions
    void* void_ptr = static_cast<void*>(d_ptr);
    Derived* back = static_cast<Derived*>(void_ptr);
    
    delete d_ptr;
    delete base2;
    
    // ============ dynamic_cast ============
    std::cout << "\n=== dynamic_cast ===" << std::endl;
    
    // Requires polymorphic types (virtual functions)
    Base* maybe_derived = new Derived();
    
    // Safe downcast with runtime check
    Derived* safe_derived = dynamic_cast<Derived*>(maybe_derived);
    if (safe_derived) {
        std::cout << "dynamic_cast succeeded: ";
        safe_derived->derived_only();
    } else {
        std::cout << "dynamic_cast failed (nullptr)" << std::endl;
    }
    
    // Trying to cast to unrelated type
    Unrelated* unrelated = dynamic_cast<Unrelated*>(maybe_derived);
    if (!unrelated) {
        std::cout << "Cast to unrelated type returns nullptr" << std::endl;
    }
    
    // Reference version (throws on failure)
    try {
        Derived& derived_ref = dynamic_cast<Derived&>(*maybe_derived);
        std::cout << "Reference cast succeeded" << std::endl;
    } catch (const std::bad_cast& e) {
        std::cout << "bad_cast: " << e.what() << std::endl;
    }
    
    delete maybe_derived;
    
    // ============ const_cast ============
    std::cout << "\n=== const_cast ===" << std::endl;
    
    // ONLY for adding/removing const (and volatile)
    const int const_val = 42;
    
    // Removing const (DANGEROUS!)
    int& mutable_val = const_cast<int&>(const_val);
    mutable_val = 100;  // UNDEFINED BEHAVIOR if original was const!
    
    std::cout << "const_val: " << const_val << std::endl;
    std::cout << "mutable_val: " << mutable_val << std::endl;
    // May print different values due to compiler optimizations!
    
    // Legitimate use: calling old C APIs
    void legacy_function(char* str);  // C function that modifies string
    
    std::string modern_str = "hello";
    // legacy_function(modern_str.c_str());  // ERROR: c_str() returns const char*
    
    // Workaround (if you know function won't modify)
    legacy_function(const_cast<char*>(modern_str.c_str()));
    
    // Better: use mutable buffer
    std::vector<char> buffer(modern_str.begin(), modern_str.end());
    buffer.push_back('\0');
    legacy_function(buffer.data());
    
    // ============ reinterpret_cast ============
    std::cout << "\n=== reinterpret_cast ===" << std::endl;
    
    // Most dangerous cast - reinterprets bit pattern
    int num = 0x12345678;
    char* bytes = reinterpret_cast<char*>(&num);
    
    std::cout << "int " << std::hex << num << " as bytes: ";
    for (size_t i = 0; i < sizeof(int); ++i) {
        std::cout << static_cast<int>(bytes[i]) << " ";
    }
    std::cout << std::dec << std::endl;
    
    // Pointer to integer and back
    int* ptr = new int(100);
    uintptr_t int_representation = reinterpret_cast<uintptr_t>(ptr);
    int* ptr_again = reinterpret_cast<int*>(int_representation);
    std::cout << "Pointer -> uintptr_t -> pointer: " << *ptr_again << std::endl;
    
    delete ptr;
    
    // Use cases:
    // 1. Serialization/deserialization
    // 2. Low-level system programming
    // 3. Type punning (but prefer std::bit_cast in C++20)
    // 4. Working with hardware registers
    
    // ============ TYPE CONVERSION OPERATORS ============
    std::cout << "\n=== User-defined Conversions ===" << std::endl;
    
    class SmartInt {
    private:
        int value;
    public:
        SmartInt(int v) : value(v) {}
        
        // Conversion to int
        operator int() const {
            return value;
        }
        
        // Conversion to string
        operator std::string() const {
            return std::to_string(value);
        }
        
        // explicit operator (C++11)
        explicit operator bool() const {
            return value != 0;
        }
    };
    
    SmartInt si(42);
    int converted_int = si;  // Implicit conversion
    std::string str = si;    // Implicit conversion
    
    std::cout << "SmartInt to int: " << converted_int << std::endl;
    std::cout << "SmartInt to string: " << str << std::endl;
    
    // bool conversion requires explicit cast
    if (static_cast<bool>(si)) {
        std::cout << "SmartInt is non-zero" << std::endl;
    }
    
    // ============ TYPE TRAITS (C++11) ============
    std::cout << "\n=== Type Traits ===" << std::endl;
    
    // Compile-time type information and transformations
    std::cout << "is_integral<int>: " << std::is_integral<int>::value << std::endl;
    std::cout << "is_floating_point<float>: " << std::is_floating_point<float>::value << std::endl;
    
    // Remove const
    using non_const_t = std::remove_const<const int>::type;
    std::cout << "remove_const<const int> is same as int: " 
              << std::is_same<non_const_t, int>::value << std::endl;
    
    // ============ SAFE CONVERSIONS WITH std::any (C++17) ============
    std::cout << "\n=== Safe Conversions ===" << std::endl;
    
    // Use std::any for type-safe containers
    std::any anything = 42;
    
    try {
        int val = std::any_cast<int>(anything);
        std::cout << "any_cast<int> succeeded: " << val << std::endl;
    } catch (const std::bad_any_cast& e) {
        std::cout << "bad_any_cast: " << e.what() << std::endl;
    }
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. AVOID C-style casts" << std::endl;
    std::cout << "2. Prefer static_cast for numeric conversions" << std::endl;
    std::cout << "3. Use dynamic_cast for safe downcasting" << std::endl;
    std::cout << "4. Use const_cast only when necessary (rarely)" << std::endl;
    std::cout << "5. reinterpret_cast is dangerous - document well" << std::endl;
    std::cout << "6. Use explicit for single-argument constructors" << std::endl;
    std::cout << "7. Use type traits for compile-time type manipulation" << std::endl;
}

// Dummy legacy function
void legacy_function(char* str) {
    // Simulate C function that might modify string
}

int main() {
    demonstrate_type_conversions();
    return 0;
}