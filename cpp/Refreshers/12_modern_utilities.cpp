#include <iostream>
#include <optional>
#include <variant>
#include <functional>
#include <tuple>
#include <map>
#include <vector>
#include <string>
#include <type_traits>
#include <cassert>

// ============ 1. std::optional (C++17) ============

std::optional<int> divide(int a, int b) {
    if (b == 0) {
        return std::nullopt;  // No value
    }
    return a / b;  // Has value
}

std::optional<std::string> find_name(int id) {
    std::map<int, std::string> database = {
        {1, "Alice"},
        {2, "Bob"},
        {3, "Charlie"}
    };
    
    auto it = database.find(id);
    if (it != database.end()) {
        return it->second;
    }
    return std::nullopt;
}

class User {
    std::optional<std::string> middle_name;
public:
    User(const std::string& first, const std::string& last,
         std::optional<std::string> middle = std::nullopt)
        : middle_name(middle) {}
    
    std::optional<std::string> get_middle_name() const {
        return middle_name;
    }
};

void demonstrate_optional() {
    std::cout << "============ std::optional (C++17) ============\n" << std::endl;
    
    // ============ Basic Usage ============
    std::cout << "=== Basic Usage ===" << std::endl;
    
    std::optional<int> maybe_value;
    std::cout << "maybe_value has value? " << maybe_value.has_value() << std::endl;
    
    maybe_value = 42;
    std::cout << "After assignment, has value? " << maybe_value.has_value() << std::endl;
    std::cout << "Value: " << maybe_value.value() << std::endl;
    std::cout << "Value (operator*): " << *maybe_value << std::endl;
    
    // ============ Safe Division Example ============
    std::cout << "\n=== Safe Division ===" << std::endl;
    
    auto result1 = divide(10, 2);
    auto result2 = divide(10, 0);
    
    if (result1) {
        std::cout << "10 / 2 = " << *result1 << std::endl;
    } else {
        std::cout << "Division by zero!" << std::endl;
    }
    
    if (result2.has_value()) {
        std::cout << "Result: " << result2.value() << std::endl;
    } else {
        std::cout << "No result (division by zero)" << std::endl;
    }
    
    // ============ Database Lookup Example ============
    std::cout << "\n=== Database Lookup ===" << std::endl;
    
    auto name1 = find_name(2);
    auto name2 = find_name(99);
    
    std::cout << "ID 2: ";
    if (name1) {
        std::cout << *name1 << std::endl;
    } else {
        std::cout << "Not found" << std::endl;
    }
    
    std::cout << "ID 99: ";
    std::cout << (name2.value_or("Not found")) << std::endl;
    
    // ============ Class with Optional Member ============
    std::cout << "\n=== Optional Class Member ===" << std::endl;
    
    User user1("John", "Doe");
    User user2("Jane", "Smith", "Marie");
    
    auto middle1 = user1.get_middle_name();
    auto middle2 = user2.get_middle_name();
    
    std::cout << "User1 middle name: " 
              << (middle1 ? *middle1 : "[none]") << std::endl;
    std::cout << "User2 middle name: " 
              << middle2.value_or("[none]") << std::endl;
    
    // ============ Optional with value_or ============
    std::cout << "\n=== value_or ===" << std::endl;
    
    std::optional<int> empty_opt;
    std::optional<int> full_opt = 100;
    
    std::cout << "Empty or default: " << empty_opt.value_or(999) << std::endl;
    std::cout << "Full or default: " << full_opt.value_or(999) << std::endl;
    
    // ============ Optional and References ============
    std::cout << "\n=== Optional References ===" << std::endl;
    
    int value = 42;
    std::optional<std::reference_wrapper<int>> opt_ref = value;
    
    if (opt_ref) {
        opt_ref->get() = 100;  // Modifies original value
        std::cout << "Value after modification: " << value << std::endl;
    }
    
    // ============ Monadic Operations (C++23) ============
    std::cout << "\n=== Monadic Operations (C++23) ===" << std::endl;
    
    #if __cplusplus >= 202302L
    /*
    std::optional<int> opt = 5;
    auto result = opt.and_then([](int n) { 
        return n > 0 ? std::optional{n * 2} : std::nullopt; 
    })
    .transform([](int n) { return std::to_string(n); })
    .or_else([] { return std::optional{std::string{"empty"}}; });
    */
    #endif
    
    // ============ Performance Benefits ============
    std::cout << "\n=== Performance Benefits ===" << std::endl;
    std::cout << "• No heap allocation (uses std::aligned_storage)" << std::endl;
    std::cout << "• Size is sizeof(T) + bool (usually with padding)" << std::endl;
    std::cout << "• More efficient than pointers for optional values" << std::endl;
    
    std::cout << "\n=== When to Use Optional ===" << std::endl;
    std::cout << "1. Function may or may not return a value" << std::endl;
    std::cout << "2. Class members that might not be set" << std::endl;
    std::cout << "3. Safer alternative to nullable pointers" << std::endl;
    std::cout << "4. Clear intent: value is optional, not required" << std::endl;
}

// ============ 2. std::variant (C++17) ============

// Visitor pattern with overloaded (C++17)
template<class... Ts>
struct overloaded : Ts... { using Ts::operator()...; };

template<class... Ts>
overloaded(Ts...) -> overloaded<Ts...>;

void demonstrate_variant() {
    std::cout << "\n============ std::variant (C++17) ============\n" << std::endl;
    
    // ============ Basic Usage ============
    std::cout << "=== Basic Usage ===" << std::endl;
    
    std::variant<int, double, std::string> var;
    
    var = 42;  // Holds int
    std::cout << "Holds int: " << std::get<int>(var) << std::endl;
    
    var = 3.14;  // Holds double
    std::cout << "Holds double: " << std::get<double>(var) << std::endl;
    
    var = "Hello";  // Holds const char*, converts to std::string
    std::cout << "Holds string: " << std::get<std::string>(var) << std::endl;
    
    // ============ Type-Safe Access ============
    std::cout << "\n=== Type-Safe Access ===" << std::endl;
    
    try {
        // std::cout << std::get<int>(var) << std::endl;  // Throws std::bad_variant_access
    } catch (const std::bad_variant_access& e) {
        std::cout << "Exception: " << e.what() << std::endl;
    }
    
    // Safe access with get_if
    if (auto* int_ptr = std::get_if<int>(&var)) {
        std::cout << "Contains int: " << *int_ptr << std::endl;
    } else if (auto* str_ptr = std::get_if<std::string>(&var)) {
        std::cout << "Contains string: " << *str_ptr << std::endl;
    }
    
    // ============ Index-Based Access ============
    std::cout << "\n=== Index-Based Access ===" << std::endl;
    
    std::cout << "Current index: " << var.index() << std::endl;
    std::cout << "Value via index: ";
    
    switch (var.index()) {
        case 0: std::cout << std::get<0>(var) << " (int)"; break;
        case 1: std::cout << std::get<1>(var) << " (double)"; break;
        case 2: std::cout << std::get<2>(var) << " (string)"; break;
    }
    std::cout << std::endl;
    
    // ============ std::visit (Visitor Pattern) ============
    std::cout << "\n=== std::visit ===" << std::endl;
    
    // Using overloaded (C++17)
    auto visitor = overloaded{
        [](int i) { std::cout << "Integer: " << i << std::endl; },
        [](double d) { std::cout << "Double: " << d << std::endl; },
        [](const std::string& s) { std::cout << "String: " << s << std::endl; }
    };
    
    std::visit(visitor, var);
    
    // Alternative: generic lambda
    std::visit([](auto&& arg) {
        using T = std::decay_t<decltype(arg)>;
        if constexpr (std::is_same_v<T, int>) {
            std::cout << "Got int: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, double>) {
            std::cout << "Got double: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, std::string>) {
            std::cout << "Got string: " << arg << std::endl;
        }
    }, var);
    
    // ============ Variant with Monostate ============
    std::cout << "\n=== std::monostate ===" << std::endl;
    
    std::variant<std::monostate, int, std::string> maybe_var;
    
    std::cout << "Initial state (monostate): index = " << maybe_var.index() << std::endl;
    maybe_var = 100;
    std::cout << "After assignment: index = " << maybe_var.index() << std::endl;
    
    // ============ Real-World Example: JSON-like Value ============
    std::cout << "\n=== JSON-like Value Type ===" << std::endl;
    
    using JsonValue = std::variant<
        std::monostate,      // null
        bool,                // boolean
        int,                 // integer
        double,              // number
        std::string,         // string
        std::vector<JsonValue>, // array
        std::map<std::string, JsonValue> // object
    >;
    
    JsonValue json = std::map<std::string, JsonValue>{
        {"name", "Alice"},
        {"age", 30},
        {"active", true}
    };
    
    // ============ Variant vs Inheritance ============
    std::cout << "\n=== Variant vs Inheritance ===" << std::endl;
    std::cout << "Variant advantages:" << std::endl;
    std::cout << "• Value semantics (no heap allocation)" << std::endl;
    std::cout << "• Fixed set of known types" << std::endl;
    std::cout << "• Compile-time type checking" << std::endl;
    std::cout << "• No virtual table overhead" << std::endl;
    
    std::cout << "\nInheritance advantages:" << std::endl;
    std::cout << "• Open for extension (new derived types)" << std::endl;
    std::cout << "• Runtime polymorphism" << std::endl;
    std::cout << "• Heterogeneous collections" << std::endl;
    
    std::cout << "\n=== When to Use Variant ===" << std::endl;
    std::cout << "1. Fixed set of alternative types" << std::endl;
    std::cout << "2. Value semantics preferred" << std::endl;
    std::cout << "3. Performance critical code" << std::endl;
    std::cout << "4. Alternatives are unrelated types" << std::endl;
}

// ============ 3. std::function ============

int add(int a, int b) {
    return a + b;
}

struct Multiplier {
    int factor;
    
    int operator()(int x) const {
        return x * factor;
    }
};

void demonstrate_function() {
    std::cout << "\n============ std::function ============\n" << std::endl;
    
    // ============ Basic Usage ============
    std::cout << "=== Basic Usage ===" << std::endl;
    
    std::function<int(int, int)> func;
    
    // Store function pointer
    func = add;
    std::cout << "Function pointer: " << func(3, 4) << std::endl;
    
    // Store lambda
    func = [](int a, int b) { return a * b; };
    std::cout << "Lambda: " << func(3, 4) << std::endl;
    
    // Store function object
    Multiplier times2{2};
    std::function<int(int)> func2 = times2;
    std::cout << "Function object: " << func2(5) << std::endl;
    
    // Store member function pointer
    class Calculator {
    public:
        int subtract(int a, int b) { return a - b; }
        static int divide(int a, int b) { return a / b; }
    };
    
    Calculator calc;
    std::function<int(int, int)> member_func = 
        std::bind(&Calculator::subtract, &calc, std::placeholders::_1, std::placeholders::_2);
    std::cout << "Member function: " << member_func(10, 3) << std::endl;
    
    // Store static member function
    std::function<int(int, int)> static_func = Calculator::divide;
    std::cout << "Static member: " << static_func(10, 2) << std::endl;
    
    // ============ Empty std::function ============
    std::cout << "\n=== Empty std::function ===" << std::endl;
    
    std::function<void()> empty_func;
    
    if (empty_func) {
        std::cout << "Function is callable" << std::endl;
    } else {
        std::cout << "Function is empty" << std::endl;
    }
    
    // Can compare with nullptr
    std::cout << "Is null? " << (empty_func == nullptr) << std::endl;
    
    // ============ Real-World Example: Event System ============
    std::cout << "\n=== Event System Example ===" << std::endl;
    
    class EventDispatcher {
        std::vector<std::function<void(int)>> listeners;
    public:
        void add_listener(std::function<void(int)> listener) {
            listeners.push_back(listener);
        }
        
        void dispatch(int event) {
            for (auto& listener : listeners) {
                if (listener) {
                    listener(event);
                }
            }
        }
    };
    
    EventDispatcher dispatcher;
    dispatcher.add_listener([](int e) { std::cout << "Listener 1: " << e << std::endl; });
    dispatcher.add_listener([](int e) { std::cout << "Listener 2: " << e * 2 << std::endl; });
    
    dispatcher.dispatch(42);
    
    // ============ Performance Considerations ============
    std::cout << "\n=== Performance Considerations ===" << std::endl;
    std::cout << "• Small function objects stored inline (Small Buffer Optimization)" << std::endl;
    std::cout << "• Large function objects allocate on heap" << std::endl;
    std::cout << "• Overhead: type erasure + potential heap allocation" << std::endl;
    std::cout << "• Use templates for performance-critical code" << std::endl;
    
    // ============ std::function vs Templates ============
    std::cout << "\n=== std::function vs Templates ===" << std::endl;
    std::cout << "Use std::function when:" << std::endl;
    std::cout << "• Need runtime polymorphism" << std::endl;
    std::cout << "• Storing callbacks in containers" << std::endl;
    std::cout << "• Type erasure is acceptable" << std::endl;
    
    std::cout << "\nUse templates when:" << std::endl;
    std::cout << "• Performance is critical" << std::endl;
    std::cout << "• Compile-time polymorphism suffices" << std::endl;
    std::cout << "• Don't need type erasure" << std::endl;
}

// ============ 4. std::bind ============

class Button {
    std::string label;
public:
    Button(const std::string& lbl) : label(lbl) {}
    
    void click(int x, int y) {
        std::cout << "Button '" << label << "' clicked at (" 
                  << x << ", " << y << ")" << std::endl;
    }
    
    void set_label(const std::string& new_label) {
        label = new_label;
        std::cout << "Label changed to: " << label << std::endl;
    }
};

void print_sum(int a, int b, int c) {
    std::cout << "Sum: " << (a + b + c) << std::endl;
}

void demonstrate_bind() {
    std::cout << "\n============ std::bind ============\n" << std::endl;
    
    // ============ Basic Binding ============
    std::cout << "=== Basic Binding ===" << std::endl;
    
    auto add_five = std::bind(add, std::placeholders::_1, 5);
    std::cout << "add_five(10) = " << add_five(10) << std::endl;
    
    auto add_specific = std::bind(add, 10, 20);
    std::cout << "add_specific() = " << add_specific() << std::endl;
    
    // ============ Reordering Arguments ============
    std::cout << "\n=== Reordering Arguments ===" << std::endl;
    
    auto subtract_reversed = std::bind(
        [](int a, int b) { return a - b; },
        std::placeholders::_2,  // Second argument becomes first
        std::placeholders::_1   // First argument becomes second
    );
    
    std::cout << "subtract_reversed(10, 5) = " << subtract_reversed(10, 5) << std::endl;
    // Equivalent to: 5 - 10 = -5
    
    // ============ Binding Multiple Arguments ============
    std::cout << "\n=== Binding Multiple Arguments ===" << std::endl;
    
    auto partial_sum = std::bind(print_sum, 
        std::placeholders::_1,  // First argument
        20,                     // Fixed second argument
        std::placeholders::_2   // Second argument becomes third
    );
    
    partial_sum(10, 30);  // Equivalent to print_sum(10, 20, 30)
    
    // ============ Binding Member Functions ============
    std::cout << "\n=== Binding Member Functions ===" << std::endl;
    
    Button button("Submit");
    
    // Bind member function with object pointer
    auto click_handler = std::bind(&Button::click, &button,
        std::placeholders::_1, std::placeholders::_2);
    
    click_handler(100, 200);
    
    // Bind with fixed arguments
    auto click_at_fixed = std::bind(&Button::click, &button, 50, 75);
    click_at_fixed();
    
    // ============ Binding with Reference Wrappers ============
    std::cout << "\n=== Binding with Reference Wrappers ===" << std::endl;
    
    std::string original = "Hello";
    auto modify_string = std::bind(
        [](std::string& str, const std::string& append) {
            str += append;
        },
        std::ref(original),  // Capture by reference
        std::placeholders::_1
    );
    
    modify_string(" World");
    std::cout << "Modified string: " << original << std::endl;
    
    // ============ Nested Binding ============
    std::cout << "\n=== Nested Binding ===" << std::endl;
    
    auto add_then_multiply = std::bind(
        [](int a, int b, int multiplier) {
            return (a + b) * multiplier;
        },
        std::placeholders::_1,
        std::placeholders::_2,
        3  // Fixed multiplier
    );
    
    std::cout << "(5 + 4) * 3 = " << add_then_multiply(5, 4) << std::endl;
    
    // ============ Modern Alternatives to std::bind ============
    std::cout << "\n=== Modern Alternatives ===" << std::endl;
    
    std::cout << "Prefer lambdas over std::bind:" << std::endl;
    
    // With std::bind
    auto old_way = std::bind(add, std::placeholders::_1, 5);
    
    // With lambda (clearer, often more efficient)
    auto new_way = [](int a) { return add(a, 5); };
    
    std::cout << "old_way(10) = " << old_way(10) << std::endl;
    std::cout << "new_way(10) = " << new_way(10) << std::endl;
    
    // ============ When to Use std::bind ============
    std::cout << "\n=== When to Use std::bind ===" << std::endl;
    std::cout << "1. Legacy code maintenance" << std::endl;
    std::cout << "2. Need to bind to overloaded functions" << std::endl;
    std::cout << "3. Complex argument reordering" << std::endl;
    std::cout << "4. Interfacing with APIs expecting std::function" << std::endl;
    
    std::cout << "\nPrefer lambdas for:" << std::endl;
    std::cout << "• Most new code" << std::endl;
    std::cout << "• Better performance" << std::endl;
    std::cout << "• Clearer syntax" << std::endl;
    std::cout << "• Better compiler optimizations" << std::endl;
}

// ============ 5. static_assert ============

template<typename T>
T safe_divide(T a, T b) {
    static_assert(std::is_floating_point_v<T>, 
                  "safe_divide requires floating point types");
    static_assert(!std::is_same_v<T, long double>, 
                  "long double not supported for performance reasons");
    return a / b;
}

template<typename T, int Size>
class FixedArray {
    static_assert(Size > 0, "Size must be positive");
    static_assert(Size < 1000, "Size too large");
    T data[Size];
};

constexpr int compile_time_value() {
    return 42;
}

void demonstrate_static_assert() {
    std::cout << "\n============ static_assert ============\n" << std::endl;
    
    // ============ Basic Usage ============
    std::cout << "=== Basic Usage ===" << std::endl;
    
    static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");
    static_assert(sizeof(char) == 1, "char must be 1 byte");
    
    std::cout << "Basic static_assert passed" << std::endl;
    
    // ============ With Type Traits ============
    std::cout << "\n=== With Type Traits ===" << std::endl;
    
    static_assert(std::is_integral_v<int>, "int is integral");
    static_assert(!std::is_pointer_v<int>, "int is not a pointer");
    static_assert(std::is_same_v<int, int>, "int is same as int");
    
    std::cout << "Type trait checks passed" << std::endl;
    
    // ============ In Templates ============
    std::cout << "\n=== In Templates ===" << std::endl;
    
    // These will compile
    safe_divide(3.14, 2.0);
    // safe_divide(3, 2);  // Compile error: static_assert fails
    
    FixedArray<int, 10> array1;
    // FixedArray<int, 0> array2;   // Compile error
    // FixedArray<int, 2000> array3; // Compile error
    
    std::cout << "Template constraints work" << std::endl;
    
    // ============ With constexpr Functions ============
    std::cout << "\n=== With constexpr Functions ===" << std::endl;
    
    constexpr int value = compile_time_value();
    static_assert(value == 42, "compile_time_value must return 42");
    
    std::cout << "constexpr assertion passed" << std::endl;
    
    // ============ C++17: Message Optional ============
    std::cout << "\n=== C++17: Optional Message ===" << std::endl;
    
    #if __cplusplus >= 201703L
    static_assert(sizeof(int) == 4);  // No message needed in C++17+
    #endif
    
    // ============ Real-World Examples ============
    std::cout << "\n=== Real-World Examples ===" << std::endl;
    
    // Platform verification
    static_assert(sizeof(void*) == 8, "64-bit platform required");
    
    // Algorithm requirements
    template<typename Iterator>
    void sort_range(Iterator begin, Iterator end) {
        using value_type = typename std::iterator_traits<Iterator>::value_type;
        static_assert(std::is_arithmetic_v<value_type>,
                     "sort_range requires arithmetic types");
        // Sorting implementation...
    }
    
    // Configuration validation
    constexpr int MAX_USERS = 1000;
    static_assert(MAX_USERS > 0 && MAX_USERS < 1000000,
                 "MAX_USERS must be between 1 and 999,999");
    
    // ============ static_assert vs assert ============
    std::cout << "\n=== static_assert vs assert ===" << std::endl;
    
    std::cout << "static_assert:" << std::endl;
    std::cout << "• Compile-time check" << std::endl;
    std::cout << "• Condition must be compile-time constant" << std::endl;
    std::cout << "• Failure prevents compilation" << std::endl;
    std::cout << "• No runtime overhead" << std::endl;
    
    std::cout << "\nassert (from <cassert>):" << std::endl;
    std::cout << "• Runtime check" << std::endl;
    std::cout << "• Condition evaluated at runtime" << std::endl;
    std::cout << "• Failure terminates program (in debug builds)" << std::endl;
    std::cout << "• Can be disabled with NDEBUG" << std::endl;
    
    // Example showing difference
    constexpr int compile_time = 42;
    int runtime = 42;  // Could be modified at runtime
    
    static_assert(compile_time == 42, "Compile-time check");
    // static_assert(runtime == 42, "Error: not compile-time constant");
    assert(runtime == 42);  // Runtime check
}

// ============ 6. using vs typedef ============

typedef int Integer;                     // Old C style
using IntegerAlias = int;                // Modern C++ style

typedef void (*FuncPtr)(int, int);       // Function pointer typedef
using FuncPtrAlias = void (*)(int, int); // Function pointer alias

template<typename T>
using Vec = std::vector<T>;              // Template alias

// Typedef cannot do this!
// template<typename T>
// typedef std::vector<T> VecTypedef;  // ERROR!

void demonstrate_using_vs_typedef() {
    std::cout << "\n============ using vs typedef ============\n" << std::endl;
    
    // ============ Basic Aliases ============
    std::cout << "=== Basic Aliases ===" << std::endl;
    
    Integer x = 42;
    IntegerAlias y = 100;
    
    std::cout << "x = " << x << ", y = " << y << std::endl;
    
    // ============ Function Pointer Aliases ============
    std::cout << "\n=== Function Pointer Aliases ===" << std::endl;
    
    void print_sum_func(int a, int b) {
        std::cout << "Sum: " << (a + b) << std::endl;
    }
    
    FuncPtr old_func = print_sum_func;
    FuncPtrAlias new_func = print_sum_func;
    
    old_func(3, 4);
    new_func(5, 6);
    
    // ============ Template Aliases ============
    std::cout << "\n=== Template Aliases ===" << std::endl;
    
    Vec<int> int_vector = {1, 2, 3};
    Vec<std::string> string_vector = {"Hello", "World"};
    
    std::cout << "Int vector size: " << int_vector.size() << std::endl;
    std::cout << "String vector: " << string_vector[0] << " " << string_vector[1] << std::endl;
    
    // More complex template alias
    template<typename Key, typename Value>
    using Map = std::map<Key, Value>;
    
    Map<std::string, int> word_counts = {
        {"apple", 3},
        {"banana", 5}
    };
    
    // ============ Alias Templates with Dependent Types ============
    std::cout << "\n=== Dependent Type Aliases ===" << std::endl;
    
    template<typename Container>
    using ValueType = typename Container::value_type;
    
    template<typename Container>
    using Iterator = typename Container::iterator;
    
    std::vector<int> vec = {1, 2, 3};
    ValueType<decltype(vec)> first = vec[0];  // int
    Iterator<decltype(vec)> it = vec.begin(); // vector<int>::iterator
    
    std::cout << "First element: " << first << std::endl;
    
    // ============ using for Bringing Names into Scope ============
    std::cout << "\n=== using for Scope ===" << std::endl;
    
    namespace MyLib {
        int version = 1;
        void print() { std::cout << "MyLib version " << version << std::endl; }
    }
    
    // Bring specific name into scope
    using MyLib::version;
    std::cout << "Version: " << version << std::endl;
    
    // Bring entire namespace (use with caution)
    // using namespace MyLib;
    // print();
    
    // ============ using in Class Inheritance ============
    std::cout << "\n=== using in Inheritance ===" << std::endl;
    
    class Base {
    public:
        void func(int x) { std::cout << "Base::func(int): " << x << std::endl; }
        virtual void virt() { std::cout << "Base::virt()" << std::endl; }
    };
    
    class Derived : public Base {
    public:
        // Bring Base::func into scope (otherwise hidden by func(double))
        using Base::func;
        
        void func(double x) { std::cout << "Derived::func(double): " << x << std::endl; }
        
        // Make Base::virt public (if it was protected in Base)
        using Base::virt;
    };
    
    Derived d;
    d.func(42);      // Calls Base::func(int) - thanks to using declaration
    d.func(3.14);    // Calls Derived::func(double)
    d.virt();        // Calls Base::virt()
    
    // ============ Comparison Table ============
    std::cout << "\n=== Comparison ===" << std::endl;
    std::cout << "Feature                  | typedef        | using" << std::endl;
    std::cout << "-------------------------|----------------|----------------" << std::endl;
    std::cout << "Template aliases         | Not possible   | Possible" << std::endl;
    std::cout << "Readability              | Less readable  | More readable" << std::endl;
    std::cout << "Function pointer syntax  | Complex        | Clear" << std::endl;
    std::cout << "Bring names into scope   | No             | Yes (using X)" << std::endl;
    std::cout << "Inheritance control      | No             | Yes" << std::endl;
    
    std::cout << "\n=== Best Practice ===" << std::endl;
    std::cout << "• Always prefer 'using' over 'typedef' in C++" << std::endl;
    std::cout << "• 'using' is more powerful and readable" << std::endl;
    std::cout << "• Only use 'typedef' when maintaining C compatibility" << std::endl;
}

// ============ 7. STRUCTURED BINDINGS ============

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

std::pair<bool, std::string> find_item(int id) {
    static std::map<int, std::string> items = {
        {1, "Apple"},
        {2, "Banana"},
        {3, "Cherry"}
    };
    
    auto it = items.find(id);
    if (it != items.end()) {
        return {true, it->second};
    }
    return {false, ""};
}

void demonstrate_structured_bindings() {
    std::cout << "\n============ STRUCTURED BINDINGS (C++17) ============\n" << std::endl;
    
    // ============ With std::pair ============
    std::cout << "=== With std::pair ===" << std::endl;
    
    std::pair<int, std::string> p{42, "answer"};
    
    // Old way
    int first_old = p.first;
    std::string second_old = p.second;
    
    // New way with structured bindings
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
    std::cout << "Person: " << name << ", " << age << ", $" << salary << std::endl;
    
    // ============ With Arrays ============
    std::cout << "\n=== With Arrays ===" << std::endl;
    
    int arr[] = {10, 20, 30, 40};
    
    // Get all elements
    auto [a, b, c, d] = arr;
    std::cout << "Array elements: " << a << ", " << b << ", " << c << ", " << d << std::endl;
    
    // Get first N elements (C++20)
    #if __cplusplus >= 202002L
    auto [x, y, z] = arr;  // Gets first 3 elements
    std::cout << "First three: " << x << ", " << y << ", " << z << std::endl;
    #endif
    
    // ============ With Structs/Classes ============
    std::cout << "\n=== With Structs ===" << std::endl;
    
    Point point{1.0, 2.0, 3.0};
    auto [px, py, pz] = point;
    std::cout << "Point: (" << px << ", " << py << ", " << pz << ")" << std::endl;
    
    // Modify through structured binding
    Employee emp{"Bob", 101, 50000.0};
    auto& [emp_name, emp_id, emp_salary] = emp;
    emp_salary = 55000.0;
    std::cout << "Updated salary: $" << emp.salary << std::endl;
    
    // ============ With std::map ============
    std::cout << "\n=== With std::map ===" << std::endl;
    
    std::map<std::string, int> scores = {
        {"Alice", 95},
        {"Bob", 87},
        {"Charlie", 92}
    };
    
    std::cout << "Old way:" << std::endl;
    for (const auto& pair : scores) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    
    std::cout << "\nWith structured bindings:" << std::endl;
    for (const auto& [student, score] : scores) {
        std::cout << student << ": " << score << std::endl;
    }
    
    // ============ Practical Examples ============
    std::cout << "\n=== Practical Examples ===" << std::endl;
    
    // Function returning success/failure
    auto [found, item_name] = find_item(2);
    if (found) {
        std::cout << "Found item: " << item_name << std::endl;
    } else {
        std::cout << "Item not found" << std::endl;
    }
    
    // Multiple return values
    auto min_max = [](const std::vector<int>& vec) -> std::pair<int, int> {
        if (vec.empty()) return {0, 0};
        return {*std::min_element(vec.begin(), vec.end()),
                *std::max_element(vec.begin(), vec.end())};
    };
    
    std::vector<int> numbers = {5, 2, 8, 1, 9};
    auto [min_val, max_val] = min_max(numbers);
    std::cout << "Min: " << min_val << ", Max: " << max_val << std::endl;
    
    // ============ Advanced Usage ============
    std::cout << "\n=== Advanced Usage ===" << std::endl;
    
    // Nested structured bindings
    std::pair<Point, Employee> complex_pair{{1,2,3}, {"Dave", 102, 60000}};
    auto& [pt, employee] = complex_pair;
    auto [ptx, pty, ptz] = pt;
    
    std::cout << "Nested: Point(" << ptx << "," << pty << "," << ptz 
              << "), Employee " << employee.name << std::endl;
    
    // Ignore elements with _
    auto [_, important, __] = std::tuple{1, "important", 3.14};
    std::cout << "Important value: " << important << std::endl;
    
    // ============ Limitations ============
    std::cout << "\n=== Limitations ===" << std::endl;
    std::cout << "1. Number of identifiers must exactly match number of elements" << std::endl;
    std::cout << "2. Cannot be used with private members" << std::endl;
    std::cout << "3. Cannot be used with classes that have get<N> overloaded" << std::endl;
    std::cout << "4. Cannot have nested structured bindings in single declaration" << std::endl;
    std::cout << "5. All elements must be accessible (public)" << std::endl;
    
    // ============ Performance Benefits ============
    std::cout << "\n=== Performance Benefits ===" << std::endl;
    std::cout << "• No runtime overhead (compile-time transformation)" << std::endl;
    std::cout << "• References avoid copies" << std::endl;
    std::cout << "• Cleaner code leads to better optimizations" << std::endl;
}

int main() {
    demonstrate_optional();
    demonstrate_variant();
    demonstrate_function();
    demonstrate_bind();
    demonstrate_static_assert();
    demonstrate_using_vs_typedef();
    demonstrate_structured_bindings();
    
    return 0;
}


#include <iostream>
#include <vector>
#include <list>
#include <algorithm>
#include <ranges>  // C++20 Ranges
#include <numeric>

void demonstrate_ranges() {
    std::cout << "\n=== C++20 RANGES ===\n";
    
    // ============================================================================
    // 1. RANGES VS TRADITIONAL ALGORITHMS
    // ============================================================================
    
    std::vector<int> numbers = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5};
    
    std::cout << "\n1. Traditional STL algorithms:\n";
    // Traditional approach - need begin/end iterators
    auto it = std::find(numbers.begin(), numbers.end(), 9);
    if (it != numbers.end()) {
        std::cout << "Found 9 at position: " << std::distance(numbers.begin(), it) << "\n";
    }
    
    // ============================================================================
    // 2. BASIC RANGES USAGE
    // ============================================================================
    
    std::cout << "\n2. Ranges approach (simpler):\n";
    
    // Ranges work directly on containers
    auto found = std::ranges::find(numbers, 9);
    if (found != numbers.end()) {
        std::cout << "Found 9 using ranges\n";
    }
    
    // Ranges algorithms return iterator-sentinel pairs
    auto [begin, end] = std::ranges::find(numbers, 5);
    if (begin != end) {
        std::cout << "Found first 5\n";
    }
    
    // ============================================================================
    // 3. VIEWS - LAZY TRANSFORMATIONS
    // ============================================================================
    
    std::cout << "\n3. Views (lazy transformations):\n";
    
    // Views don't create new containers - they transform on the fly
    auto squared_view = numbers | std::views::transform([](int n) { 
        return n * n; 
    });
    
    std::cout << "Squared view: ";
    for (int n : squared_view) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // Original container unchanged
    std::cout << "Original numbers: ";
    for (int n : numbers) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // ============================================================================
    // 4. COMMON RANGE VIEWS
    // ============================================================================
    
    std::cout << "\n4. Common range views:\n";
    
    // 4.1 filter - keep only elements matching predicate
    auto evens = numbers | std::views::filter([](int n) { 
        return n % 2 == 0; 
    });
    
    std::cout << "Even numbers: ";
    for (int n : evens) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4.2 take - take first N elements
    auto first_three = numbers | std::views::take(3);
    std::cout << "First three: ";
    for (int n : first_three) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4.3 drop - skip first N elements
    auto after_three = numbers | std::views::drop(3);
    std::cout << "After first three: ";
    for (int n : after_three) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4.4 reverse
    auto reversed = numbers | std::views::reverse;
    std::cout << "Reversed: ";
    for (int n : reversed) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // 4.5 keys/values for map-like structures
    std::map<std::string, int> scores = {
        {"Alice", 85}, {"Bob", 92}, {"Charlie", 78}
    };
    
    std::cout << "Names (keys view): ";
    for (const auto& name : scores | std::views::keys) {
        std::cout << name << " ";
    }
    std::cout << "\n";
    
    std::cout << "Scores (values view): ";
    for (int score : scores | std::views::values) {
        std::cout << score << " ";
    }
    std::cout << "\n";
    
    // ============================================================================
    // 5. VIEW COMPOSITION (PIPELINING)
    // ============================================================================
    
    std::cout << "\n5. View composition (pipelines):\n";
    
    // Chain multiple views together
    auto pipeline = numbers 
        | std::views::filter([](int n) { return n > 3; })     // Keep > 3
        | std::views::transform([](int n) { return n * 2; })  // Double them
        | std::views::take(4)                                 // Take first 4
        | std::views::reverse;                                // Reverse order
    
    std::cout << "Pipeline result: ";
    for (int n : pipeline) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // The pipeline is evaluated lazily
    // No intermediate containers are created!
    
    // ============================================================================
    // 6. RANGE ALGORITHMS
    // ============================================================================
    
    std::cout << "\n6. Range algorithms:\n";
    
    std::vector<int> data = {5, 2, 8, 1, 9, 3};
    
    // Sort using ranges
    std::ranges::sort(data);
    std::cout << "Sorted: ";
    for (int n : data) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // Count using ranges
    int count = std::ranges::count(data, 5);
    std::cout << "Count of 5: " << count << "\n";
    
    // Accumulate using ranges
    int sum = std::accumulate(data.begin(), data.end(), 0);
    std::cout << "Sum: " << sum << "\n";
    
    // For C++23, there's ranges::fold_left
    // For now, we can create a view and use accumulate
    
    // ============================================================================
    // 7. CUSTOM RANGES AND VIEWS
    // ============================================================================
    
    std::cout << "\n7. Creating custom views:\n";
    
    // Create a view that generates a sequence
    auto fibonacci_view = std::views::iota(0)  // Infinite sequence starting from 0
        | std::views::transform([](int n) {
            // Generate nth Fibonacci number
            int a = 0, b = 1;
            for (int i = 0; i < n; ++i) {
                int temp = a + b;
                a = b;
                b = temp;
            }
            return a;
        })
        | std::views::take(10);  // Take first 10
    
    std::cout << "First 10 Fibonacci: ";
    for (int n : fibonacci_view) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // ============================================================================
    // 8. RANGE CONCEPTS
    // ============================================================================
    
    std::cout << "\n8. Range concepts:\n";
    
    // C++20 introduces range concepts that can be used in templates
    
    // Example: Function that works with any range
    auto print_range = []<std::ranges::range R>(const R& range) {
        for (const auto& item : range) {
            std::cout << item << " ";
        }
        std::cout << "\n";
    };
    
    std::cout << "Vector: ";
    print_range(numbers);
    
    std::list<double> doubles = {1.1, 2.2, 3.3};
    std::cout << "List: ";
    print_range(doubles);
    
    // ============================================================================
    // 9. PRACTICAL EXAMPLES
    // ============================================================================
    
    std::cout << "\n9. Practical examples:\n";
    
    // Example 1: Process lines from a file-like source
    std::vector<std::string> lines = {
        "Hello World",
        "C++20 Ranges",
        "Modern C++",
        "Template Metaprogramming"
    };
    
    // Get lines containing "C++", convert to uppercase, take first 2
    auto processed = lines
        | std::views::filter([](const std::string& s) {
            return s.find("C++") != std::string::npos;
        })
        | std::views::transform([](const std::string& s) {
            std::string upper;
            for (char c : s) upper += std::toupper(c);
            return upper;
        })
        | std::views::take(2);
    
    std::cout << "Processed lines:\n";
    for (const auto& line : processed) {
        std::cout << "  " << line << "\n";
    }
    
    // Example 2: Matrix operations with ranges
    std::vector<std::vector<int>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    // Get diagonal using ranges
    auto diagonal = std::views::iota(0, 3)  // indices 0, 1, 2
        | std::views::transform([&matrix](int i) {
            return matrix[i][i];  // matrix[i][i] is the diagonal element
        });
    
    std::cout << "Matrix diagonal: ";
    for (int n : diagonal) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // ============================================================================
    // 10. RANGE ADAPTORS VS RANGE FACTORIES
    // ============================================================================
    
    std::cout << "\n10. Range adaptors vs factories:\n";
    
    // Range adaptors take an existing range and transform it
    auto adapted = numbers | std::views::filter([](int n) { return n > 5; });
    
    // Range factories create new ranges
    auto generated = std::views::iota(1, 10);  // Numbers 1 through 9
    
    std::cout << "Generated range (1-9): ";
    for (int n : generated) {
        std::cout << n << " ";
    }
    std::cout << "\n";
    
    // ============================================================================
    // 11. PERFORMANCE BENEFITS
    // ============================================================================
    
    std::cout << "\n11. Performance benefits:\n";
    
    // Ranges are lazy and compose efficiently
    // Compare traditional vs ranges approach:
    
    // Traditional (creates intermediate vectors):
    std::vector<int> temp;
    std::copy_if(numbers.begin(), numbers.end(), 
                 std::back_inserter(temp),
                 [](int n) { return n > 3; });
    std::vector<int> temp2;
    std::transform(temp.begin(), temp.end(),
                   std::back_inserter(temp2),
                   [](int n) { return n * 2; });
    
    // Ranges (no intermediate containers):
    auto efficient = numbers 
        | std::views::filter([](int n) { return n > 3; })
        | std::views::transform([](int n) { return n * 2; });
    
    std::cout << "Traditional approach created " << temp.size() + temp2.size()
              << " elements in intermediate containers\n";
    std::cout << "Ranges approach creates NO intermediate containers!\n";
    
    // ============================================================================
    // 12. COMMON PITFALLS
    // ============================================================================
    
    std::cout << "\n12. Common pitfalls:\n";
    
    // Pitfall 1: Views are lazy - accessing invalidated data
    std::vector<int> source = {1, 2, 3, 4, 5};
    auto view = source | std::views::filter([](int n) { return n > 2; });
    
    // If source changes, view might reference invalid data
    source.push_back(6);  // Might reallocate
    
    // Pitfall 2: Infinite ranges without take
    auto infinite = std::views::iota(0);  // Goes forever!
    // for (int n : infinite) { /* infinite loop! */ }
    
    auto safe_infinite = std::views::iota(0) | std::views::take(100);
    
    // Pitfall 3: Performance with complex pipelines
    // Very long pipelines might not be optimized well
    
    std::cout << "\n=== RANGES SUMMARY ===\n";
    std::cout << "Advantages:\n";
    std::cout << "  - More readable code\n";
    std::cout << "  - No begin/end iterator pairs\n";
    std::cout << "  - Lazy evaluation\n";
    std::cout << "  - No intermediate containers\n";
    std::cout << "  - Composable transformations\n";
    std::cout << "\nDisadvantages:\n";
    std::cout << "  - C++20 only\n";
    std::cout << "  - Some compiler support limitations\n";
    std::cout << "  - Debugging can be harder\n";
}


#include <iostream>
#include <span>
#include <vector>
#include <array>
#include <algorithm>

void demonstrate_span() {
    std::cout << "\n=== std::span (C++20) ===\n";
    
    // ============================================================================
    // 1. WHAT IS std::span?
    // ============================================================================
    
    // std::span is a non-owning view over a contiguous sequence of elements
    // Think of it as a "pointer + length" with bounds checking (optional)
    
    // ============================================================================
    // 2. CREATING SPANS
    // ============================================================================
    
    std::cout << "\n1. Creating spans:\n";
    
    // From C-style array
    int c_array[] = {1, 2, 3, 4, 5};
    std::span<int> span1{c_array};  // Deduces size from array
    std::cout << "Span from C-array: ";
    for (int n : span1) std::cout << n << " ";
    std::cout << "\n";
    
    // From std::array
    std::array<int, 6> std_array = {10, 20, 30, 40, 50, 60};
    std::span<int> span2{std_array};
    std::cout << "Span from std::array: ";
    for (int n : span2) std::cout << n << " ";
    std::cout << "\n";
    
    // From std::vector
    std::vector<int> vec = {100, 200, 300, 400, 500};
    std::span<int> span3{vec};
    std::cout << "Span from vector: ";
    for (int n : span3) std::cout << n << " ";
    std::cout << "\n";
    
    // From pointer and size
    int* data_ptr = vec.data();
    size_t size = vec.size();
    std::span<int> span4{data_ptr, size};
    
    // ============================================================================
    // 3. SPAN OPERATIONS
    // ============================================================================
    
    std::cout << "\n2. Span operations:\n";
    
    std::span<int> numbers = span3;  // Copy span (shallow - doesn't copy data)
    
    // Access elements
    std::cout << "First element: " << numbers.front() << "\n";
    std::cout << "Last element: " << numbers.back() << "\n";
    std::cout << "Element at index 2: " << numbers[2] << "\n";
    
    // Bounds-checked access (C++26: at() in std::span)
    // For now, use operator[] or check bounds manually
    if (numbers.size() > 10) {
        // numbers[10] would be undefined behavior
    }
    
    // Size information
    std::cout << "Size: " << numbers.size() << "\n";
    std::cout << "Size in bytes: " << numbers.size_bytes() << "\n";
    std::cout << "Empty? " << (numbers.empty() ? "Yes" : "No") << "\n";
    
    // Data access
    int* raw_ptr = numbers.data();
    std::cout << "Raw pointer: " << raw_ptr << "\n";
    
    // ============================================================================
    // 4. SPAN SUBVIEWS
    // ============================================================================
    
    std::cout << "\n3. Span subviews:\n";
    
    std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::span<int> full_view{data};
    
    // first() - first N elements
    auto first_three = full_view.first(3);
    std::cout << "First 3: ";
    for (int n : first_three) std::cout << n << " ";
    std::cout << "\n";
    
    // last() - last N elements
    auto last_three = full_view.last(3);
    std::cout << "Last 3: ";
    for (int n : last_three) std::cout << n << " ";
    std::cout << "\n";
    
    // subspan() - range from offset
    auto middle = full_view.subspan(3, 4);  // Start at index 3, length 4
    std::cout << "Middle 4 (starting at index 3): ";
    for (int n : middle) std::cout << n << " ";
    std::cout << "\n";
    
    // subspan() with dynamic_extent
    auto tail = full_view.subspan(7);  // From index 7 to end
    std::cout << "Tail (from index 7): ";
    for (int n : tail) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 5. CONST SPANS
    // ============================================================================
    
    std::cout << "\n4. Const spans:\n";
    
    // Span to const data - can't modify through span
    std::span<const int> const_span{data};
    // const_span[0] = 99;  // ERROR: can't modify through const span
    
    // But can still create subviews
    auto const_sub = const_span.first(5);
    std::cout << "Const subview: ";
    for (int n : const_sub) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 6. FIXED-SIZE SPANS
    // ============================================================================
    
    std::cout << "\n5. Fixed-size spans:\n";
    
    // Span with compile-time known size
    std::span<int, 5> fixed_span{c_array};  // Size must match exactly
    
    // Fixed-size spans have more compile-time checks
    std::cout << "Fixed-size span size: " << fixed_span.size() << " (compile-time)\n";
    
    // Can convert fixed-size to dynamic-size
    std::span<int> dynamic_from_fixed = fixed_span;
    
    // But not vice versa (unless size matches)
    // std::span<int, 5> from_dynamic = span3;  // ERROR: size not known at compile time
    
    // ============================================================================
    // 7. REAL-WORLD USE CASES
    // ============================================================================
    
    std::cout << "\n6. Real-world use cases:\n";
    
    // Case 1: Function accepting array-like parameters
    auto process_data = [](std::span<const int> data) {
        std::cout << "Processing " << data.size() << " elements\n";
        int sum = 0;
        for (int n : data) sum += n;
        return sum;
    };
    
    // Can pass different containers
    std::cout << "Sum of C-array: " << process_data(span1) << "\n";
    std::cout << "Sum of vector: " << process_data(span3) << "\n";
    std::cout << "Sum of std::array: " << process_data(span2) << "\n";
    
    // Case 2: Processing chunks of data
    std::vector<char> file_data = {'H', 'e', 'l', 'l', 'o', ' ', 
                                   'W', 'o', 'r', 'l', 'd', '!'};
    
    // Process in 4-byte chunks
    std::cout << "Processing in chunks:\n";
    for (size_t i = 0; i < file_data.size(); i += 4) {
        auto chunk = std::span{file_data}.subspan(i, std::min<size_t>(4, file_data.size() - i));
        std::cout << "Chunk: ";
        for (char c : chunk) std::cout << c;
        std::cout << "\n";
    }
    
    // Case 3: Interfacing with C APIs
    auto c_api_function = [](int* data, size_t size) {
        // Simulating C API
        for (size_t i = 0; i < size; ++i) {
            data[i] *= 2;
        }
    };
    
    std::vector<int> values = {1, 2, 3};
    // Safe: span ensures we pass correct size
    c_api_function(values.data(), values.size());
    
    // Even better with span:
    std::span<int> value_span{values};
    c_api_function(value_span.data(), value_span.size());
    
    std::cout << "After C API: ";
    for (int n : values) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 8. SPAN VS OTHER TYPES
    // ============================================================================
    
    std::cout << "\n7. Span vs other types:\n";
    
    // vs raw pointer + size
    // - Span provides bounds checking (optional)
    // - Span provides container-like interface
    // - Span clearly expresses non-ownership
    
    // vs std::string_view (for characters)
    std::string str = "Hello World";
    std::string_view sv{str};  // Specifically for strings
    std::span<const char> char_span{str.data(), str.size()};  // Generic
    
    // vs std::vector
    // - Vector owns its data, span doesn't
    // - Vector can grow/shrink, span is fixed view
    
    // ============================================================================
    // 9. SPAN AND ALGORITHMS
    // ============================================================================
    
    std::cout << "\n8. Span with algorithms:\n";
    
    std::vector<int> unsorted = {5, 2, 8, 1, 9, 3};
    std::span<int> unsorted_span{unsorted};
    
    // Can use std algorithms with spans
    std::sort(unsorted_span.begin(), unsorted_span.end());
    
    std::cout << "Sorted via span: ";
    for (int n : unsorted_span) std::cout << n << " ";
    std::cout << "\n";
    
    // C++20 ranges work with spans too
    auto even_numbers = unsorted_span 
        | std::views::filter([](int n) { return n % 2 == 0; });
    
    std::cout << "Even numbers: ";
    for (int n : even_numbers) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 10. SPAN SAFETY AND LIFETIME
    // ============================================================================
    
    std::cout << "\n9. Safety and lifetime considerations:\n";
    
    // DANGER: Span doesn't extend lifetime
    std::span<const char> dangerous_span;
    {
        std::string temp = "temporary";
        dangerous_span = std::span<const char>{temp.data(), temp.size()};
        // temp destroyed here
    }
    // dangerous_span now points to destroyed memory!
    // Accessing it is undefined behavior
    
    std::cout << "Warning: Span lifetime must be managed carefully\n";
    
    // Safe pattern: Keep original data alive
    std::string permanent = "permanent data";
    std::span<const char> safe_span{permanent.data(), permanent.size()};
    // permanent must outlive safe_span
    
    // ============================================================================
    // 11. MULTI-DIMENSIONAL SPANS
    // ============================================================================
    
    std::cout << "\n10. Multi-dimensional data (advanced):\n";
    
    // For 2D data, you can have spans of spans
    std::vector<std::vector<int>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    
    // Create spans for each row
    std::vector<std::span<int>> row_spans;
    for (auto& row : matrix) {
        row_spans.emplace_back(row);
    }
    
    // Span of spans
    std::span<std::span<int>> matrix_span{row_spans};
    
    std::cout << "Matrix via spans:\n";
    for (const auto& row : matrix_span) {
        for (int n : row) {
            std::cout << n << " ";
        }
        std::cout << "\n";
    }
    
    // ============================================================================
    // 12. PERFORMANCE
    // ============================================================================
    
    std::cout << "\n11. Performance characteristics:\n";
    
    // Span has zero overhead compared to raw pointer + size
    // All operations are compile-time when possible
    
    // Example: Fixed-size span operations can be optimized away
    std::array<int, 4> small_array = {1, 2, 3, 4};
    std::span<int, 4> fixed{small_array};
    
    // Compiler knows size at compile time
    // Can optimize loops, bounds checks, etc.
    
    std::cout << "Span has no runtime overhead when used correctly\n";
    
    // ============================================================================
    // SUMMARY
    // ============================================================================
    
    std::cout << "\n=== std::span SUMMARY ===\n";
    std::cout << "Use std::span when:\n";
    std::cout << "  1. You need a view over contiguous data\n";
    std::cout << "  2. You want to avoid copying\n";
    std::cout << "  3. You're interfacing with C APIs\n";
    std::cout << "  4. You want to write generic code\n";
    std::cout << "  5. You need subviews/slices\n";
    std::cout << "\nAdvantages:\n";
    std::cout << "  - Non-owning (no allocation/deallocation)\n";
    std::cout << "  - Bounds information always available\n";
    std::cout << "  - Compatible with existing containers\n";
    std::cout << "  - Zero overhead\n";
    std::cout << "  - Type-safe alternative to void*\n";
    std::cout << "\nCaveats:\n";
    std::cout << "  - C++20 or later required\n";
    std::cout << "  - Must manage data lifetime carefully\n";
    std::cout << "  - Only for contiguous data\n";
}


#include <iostream>
#include <any>
#include <vector>
#include <string>
#include <typeinfo>
#include <type_traits>
#include <cassert>

void demonstrate_any() {
    std::cout << "\n=== std::any (C++17) ===\n";
    
    // ============================================================================
    // 1. WHAT IS std::any?
    // ============================================================================
    
    // std::any is a type-safe container for single values of any type
    // Similar to void* but with type safety
    
    // ============================================================================
    // 2. BASIC USAGE
    // ============================================================================
    
    std::cout << "\n1. Basic usage:\n";
    
    std::any value;
    
    // Store different types
    value = 42;  // int
    std::cout << "Stored int: " << std::any_cast<int>(value) << "\n";
    
    value = 3.14159;  // double
    std::cout << "Stored double: " << std::any_cast<double>(value) << "\n";
    
    value = std::string("Hello");  // std::string
    std::cout << "Stored string: " << std::any_cast<std::string>(value) << "\n";
    
    value = 'A';  // char
    std::cout << "Stored char: " << std::any_cast<char>(value) << "\n";
    
    // ============================================================================
    // 3. TYPE SAFETY
    // ============================================================================
    
    std::cout << "\n2. Type safety:\n";
    
    value = 100;
    
    try {
        // Wrong type cast throws std::bad_any_cast
        double d = std::any_cast<double>(value);
        std::cout << "This won't print\n";
    }
    catch (const std::bad_any_cast& e) {
        std::cout << "Caught bad_any_cast: " << e.what() << "\n";
    }
    
    // Safe cast with pointer (returns nullptr if wrong type)
    if (int* ptr = std::any_cast<int>(&value)) {
        std::cout << "Successfully cast to int: " << *ptr << "\n";
    }
    
    if (double* ptr = std::any_cast<double>(&value)) {
        std::cout << "This won't print (wrong type)\n";
    }
    
    // ============================================================================
    // 4. ANY OPERATIONS
    // ============================================================================
    
    std::cout << "\n3. Any operations:\n";
    
    std::any a;
    
    // Check if contains a value
    std::cout << "Initially has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    a = 42;
    std::cout << "After assignment has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // Get type information
    std::cout << "Type name: " << a.type().name() << "\n";
    
    // Reset/clear
    a.reset();
    std::cout << "After reset has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // ============================================================================
    // 5. STORING COMPLEX TYPES
    // ============================================================================
    
    std::cout << "\n4. Storing complex types:\n";
    
    // Store custom types
    struct Person {
        std::string name;
        int age;
        
        void print() const {
            std::cout << name << " (" << age << ")\n";
        }
    };
    
    Person alice{"Alice", 30};
    std::any person_any = alice;
    
    // Access custom type
    Person retrieved = std::any_cast<Person>(person_any);
    retrieved.print();
    
    // Store containers
    std::any vector_any = std::vector<int>{1, 2, 3, 4, 5};
    auto& vec_ref = std::any_cast<std::vector<int>&>(vector_any);
    vec_ref.push_back(6);
    
    std::cout << "Vector in any: ";
    for (int n : vec_ref) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 6. ANY IN CONTAINERS
    // ============================================================================
    
    std::cout << "\n5. Any in containers (heterogeneous collections):\n";
    
    std::vector<std::any> heterogeneous;
    
    heterogeneous.push_back(42);
    heterogeneous.push_back(3.14);
    heterogeneous.push_back(std::string("Hello"));
    heterogeneous.push_back(true);
    heterogeneous.push_back(std::vector<int>{1, 2, 3});
    
    std::cout << "Heterogeneous collection:\n";
    for (const auto& item : heterogeneous) {
        if (item.type() == typeid(int)) {
            std::cout << "  int: " << std::any_cast<int>(item) << "\n";
        }
        else if (item.type() == typeid(double)) {
            std::cout << "  double: " << std::any_cast<double>(item) << "\n";
        }
        else if (item.type() == typeid(std::string)) {
            std::cout << "  string: " << std::any_cast<std::string>(item) << "\n";
        }
        else if (item.type() == typeid(bool)) {
            std::cout << "  bool: " << std::any_cast<bool>(item) << "\n";
        }
        else if (item.type() == typeid(std::vector<int>)) {
            std::cout << "  vector<int>: ";
            for (int n : std::any_cast<std::vector<int>>(item)) {
                std::cout << n << " ";
            }
            std::cout << "\n";
        }
    }
    
    // ============================================================================
    // 7. VISITOR PATTERN WITH ANY
    // ============================================================================
    
    std::cout << "\n6. Visitor pattern with any:\n";
    
    // Function to handle any type
    auto print_any = [](const std::any& a) {
        if (a.type() == typeid(int)) {
            std::cout << "Integer: " << std::any_cast<int>(a) << "\n";
        }
        else if (a.type() == typeid(double)) {
            std::cout << "Double: " << std::any_cast<double>(a) << "\n";
        }
        else if (a.type() == typeid(std::string)) {
            std::cout << "String: " << std::any_cast<std::string>(a) << "\n";
        }
        else {
            std::cout << "Unknown type: " << a.type().name() << "\n";
        }
    };
    
    std::any var1 = 100;
    std::any var2 = 2.71828;
    std::any var3 = std::string("Euler's number");
    
    print_any(var1);
    print_any(var2);
    print_any(var3);
    
    // ============================================================================
    // 8. ANY WITH POLYMORPHIC TYPES
    // ============================================================================
    
    std::cout << "\n7. Any with polymorphic types:\n";
    
    class Shape {
    public:
        virtual ~Shape() = default;
        virtual void draw() const = 0;
    };
    
    class Circle : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Circle\n";
        }
    };
    
    class Square : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Square\n";
        }
    };
    
    // Store polymorphic objects in any
    std::any shape1 = Circle{};
    std::any shape2 = Square{};
    
    // Need to cast to base pointer/reference
    auto draw_shape = [](const std::any& shape) {
        if (shape.type() == typeid(Circle)) {
            std::any_cast<Circle>(shape).draw();
        }
        else if (shape.type() == typeid(Square)) {
            std::any_cast<Square>(shape).draw();
        }
    };
    
    draw_shape(shape1);
    draw_shape(shape2);
    
    // Better: Store std::unique_ptr<Shape>
    std::any ptr_shape = std::make_unique<Circle>();
    if (auto* ptr = std::any_cast<std::unique_ptr<Shape>>(&ptr_shape)) {
        (*ptr)->draw();
    }
    
    // ============================================================================


#include <iostream>
#include <any>
#include <vector>
#include <string>
#include <typeinfo>
#include <type_traits>
#include <cassert>

void demonstrate_any() {
    std::cout << "\n=== std::any (C++17) ===\n";
    
    // ============================================================================
    // 1. WHAT IS std::any?
    // ============================================================================
    
    // std::any is a type-safe container for single values of any type
    // Similar to void* but with type safety
    
    // ============================================================================
    // 2. BASIC USAGE
    // ============================================================================
    
    std::cout << "\n1. Basic usage:\n";
    
    std::any value;
    
    // Store different types
    value = 42;  // int
    std::cout << "Stored int: " << std::any_cast<int>(value) << "\n";
    
    value = 3.14159;  // double
    std::cout << "Stored double: " << std::any_cast<double>(value) << "\n";
    
    value = std::string("Hello");  // std::string
    std::cout << "Stored string: " << std::any_cast<std::string>(value) << "\n";
    
    value = 'A';  // char
    std::cout << "Stored char: " << std::any_cast<char>(value) << "\n";
    
    // ============================================================================
    // 3. TYPE SAFETY
    // ============================================================================
    
    std::cout << "\n2. Type safety:\n";
    
    value = 100;
    
    try {
        // Wrong type cast throws std::bad_any_cast
        double d = std::any_cast<double>(value);
        std::cout << "This won't print\n";
    }
    catch (const std::bad_any_cast& e) {
        std::cout << "Caught bad_any_cast: " << e.what() << "\n";
    }
    
    // Safe cast with pointer (returns nullptr if wrong type)
    if (int* ptr = std::any_cast<int>(&value)) {
        std::cout << "Successfully cast to int: " << *ptr << "\n";
    }
    
    if (double* ptr = std::any_cast<double>(&value)) {
        std::cout << "This won't print (wrong type)\n";
    }
    
    // ============================================================================
    // 4. ANY OPERATIONS
    // ============================================================================
    
    std::cout << "\n3. Any operations:\n";
    
    std::any a;
    
    // Check if contains a value
    std::cout << "Initially has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    a = 42;
    std::cout << "After assignment has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // Get type information
    std::cout << "Type name: " << a.type().name() << "\n";
    
    // Reset/clear
    a.reset();
    std::cout << "After reset has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // ============================================================================
    // 5. STORING COMPLEX TYPES
    // ============================================================================
    
    std::cout << "\n4. Storing complex types:\n";
    
    // Store custom types
    struct Person {
        std::string name;
        int age;
        
        void print() const {
            std::cout << name << " (" << age << ")\n";
        }
    };
    
    Person alice{"Alice", 30};
    std::any person_any = alice;
    
    // Access custom type
    Person retrieved = std::any_cast<Person>(person_any);
    retrieved.print();
    
    // Store containers
    std::any vector_any = std::vector<int>{1, 2, 3, 4, 5};
    auto& vec_ref = std::any_cast<std::vector<int>&>(vector_any);
    vec_ref.push_back(6);
    
    std::cout << "Vector in any: ";
    for (int n : vec_ref) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 6. ANY IN CONTAINERS
    // ============================================================================
    
    std::cout << "\n5. Any in containers (heterogeneous collections):\n";
    
    std::vector<std::any> heterogeneous;
    
    heterogeneous.push_back(42);
    heterogeneous.push_back(3.14);
    heterogeneous.push_back(std::string("Hello"));
    heterogeneous.push_back(true);
    heterogeneous.push_back(std::vector<int>{1, 2, 3});
    
    std::cout << "Heterogeneous collection:\n";
    for (const auto& item : heterogeneous) {
        if (item.type() == typeid(int)) {
            std::cout << "  int: " << std::any_cast<int>(item) << "\n";
        }
        else if (item.type() == typeid(double)) {
            std::cout << "  double: " << std::any_cast<double>(item) << "\n";
        }
        else if (item.type() == typeid(std::string)) {
            std::cout << "  string: " << std::any_cast<std::string>(item) << "\n";
        }
        else if (item.type() == typeid(bool)) {
            std::cout << "  bool: " << std::any_cast<bool>(item) << "\n";
        }
        else if (item.type() == typeid(std::vector<int>)) {
            std::cout << "  vector<int>: ";
            for (int n : std::any_cast<std::vector<int>>(item)) {
                std::cout << n << " ";
            }
            std::cout << "\n";
        }
    }
    
    // ============================================================================
    // 7. VISITOR PATTERN WITH ANY
    // ============================================================================
    
    std::cout << "\n6. Visitor pattern with any:\n";
    
    // Function to handle any type
    auto print_any = [](const std::any& a) {
        if (a.type() == typeid(int)) {
            std::cout << "Integer: " << std::any_cast<int>(a) << "\n";
        }
        else if (a.type() == typeid(double)) {
            std::cout << "Double: " << std::any_cast<double>(a) << "\n";
        }
        else if (a.type() == typeid(std::string)) {
            std::cout << "String: " << std::any_cast<std::string>(a) << "\n";
        }
        else {
            std::cout << "Unknown type: " << a.type().name() << "\n";
        }
    };
    
    std::any var1 = 100;
    std::any var2 = 2.71828;
    std::any var3 = std::string("Euler's number");
    
    print_any(var1);
    print_any(var2);
    print_any(var3);
    
    // ============================================================================
    // 8. ANY WITH POLYMORPHIC TYPES
    // ============================================================================
    
    std::cout << "\n7. Any with polymorphic types:\n";
    
    class Shape {
    public:
        virtual ~Shape() = default;
        virtual void draw() const = 0;
    };
    
    class Circle : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Circle\n";
        }
    };
    
    class Square : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Square\n";
        }
    };
    
    // Store polymorphic objects in any
    std::any shape1 = Circle{};
    std::any shape2 = Square{};
    
    // Need to cast to base pointer/reference
    auto draw_shape = [](const std::any& shape) {
        if (shape.type() == typeid(Circle)) {
            std::any_cast<Circle>(shape).draw();
        }
        else if (shape.type() == typeid(Square)) {
            std::any_cast<Square>(shape).draw();
        }
    };
    
    draw_shape(shape1);
    draw_shape(shape2);
    
    // Better: Store std::unique_ptr<Shape>
    std::any ptr_shape = std::make_unique<Circle>();
    if (auto* ptr = std::any_cast<std::unique_ptr<Shape>>(&ptr_shape)) {
        (*ptr)->draw();
    }
    
    // ============================================================================
    // 9. ANY FOR CONFIGURATION DATA
    // ============================================================================
    
    std::cout << "\n8. Any for configuration data:\n";
    
    // std::any is useful for configuration settings that can be different types
    std::map<std::string, std::any> config;
    
    config["timeout"] = 30;              // int
    config["pi"] = 3.14159;              // double
    config["name"] = std::string("app"); // string
    config["verbose"] = true;            // bool
    config["ports"] = std::vector<int>{80, 443}; // vector
    
    // Retrieve with type checking
    auto get_config = [&config](const std::string& key) -> std::any {
        auto it = config.find(key);
        if (it != config.end()) {
            return it->second;
        }
        return {};  // empty any
    };
    
    if (auto timeout = get_config("timeout"); timeout.has_value()) {
        std::cout << "Timeout: " << std::any_cast<int>(timeout) << " seconds\n";
    }
    
    // ============================================================================
    // 10. PERFORMANCE CONSIDERATIONS
    // ============================================================================
    
    std::cout << "\n9. Performance considerations:\n";
    
    // std::any uses small buffer optimization (SBO)
    // Small types are stored inline, large types on heap
    
    std::any small = 'X';      // Likely stored inline
    std::any medium = 3.14;    // Likely stored inline
    std::any large = std::vector<int>(1000);  // Likely heap allocated
    
    std::cout << "Small type in any: " << std::any_cast<char>(small) << "\n";
    std::cout << "Implementation uses SBO for efficiency\n";
    
    // Type casting has runtime cost (type checking)
    // Not suitable for performance-critical code
    
    // ============================================================================
    // 11. ANY VS VARIANT VS OPTIONAL
    // ============================================================================
    
    std::cout << "\n10. Any vs Variant vs Optional:\n";
    
    // std::any: Any type, runtime type checking
    // std::variant: Type-safe union, compile-time known types
    // std::optional: Maybe a value of specific type
    
    std::any any_value;           // Can be anything
    std::variant<int, double, std::string> variant_value;  // One of these three
    std::optional<int> optional_value;  // Maybe an int, maybe nothing
    
    std::cout << "Use std::any when:\n";
    std::cout << "  - You truly need any type\n";
    std::cout << "  - Types are determined at runtime\n";
    std::cout << "  - You need maximum flexibility\n";
    
    std::cout << "\nPrefer std::variant when:\n";
    std::cout << "  - Possible types are known at compile time\n";
    std::cout << "  - You want type safety\n";
    std::cout << "  - You want to use std::visit\n";
    
    std::cout << "\nUse std::optional when:\n";
    std::cout << "  - You need 'maybe a value of specific type'\n";
    
    // ============================================================================
    // 12. ADVANCED: ANY WITH CUSTOM TYPE INFO
    // ============================================================================
    
    std::cout << "\n11. Advanced: Custom type handling:\n";
    
    // Register types with custom handlers
    struct TypeHandler {
        std::string type_name;
        std::function<void(const std::any&)> printer;
    };
    
    std::map<std::type_index, TypeHandler> handlers;
    
    handlers[typeid(int)] = {"int", [](const std::any& a) {
        std::cout << "Integer: " << std::any_cast<int>(a) << "\n";
    }};
    
    handlers[typeid(std::string)] = {"string", [](const std::any& a) {
        std::cout << "String: " << std::any_cast<std::string>(a) << "\n";
    }};
    
    // Use handlers
    std::any data1 = 42;
    std::any data2 = std::string("test");
    
    auto it1 = handlers.find(data1.type());
    if (it1 != handlers.end()) {
        std::cout << "Type: " << it1->second.type_name << " -> ";
        it1->second.printer(data1);
    }
    
    auto it2 = handlers.find(data2.type());
    if (it2 != handlers.end()) {
        std::cout << "Type: " << it2->second.type_name << " -> ";
        it2->second.printer(data2);
    }
    
    // ============================================================================
    // 13. REAL-WORLD EXAMPLE: COMMAND PARSER
    // ============================================================================
    
    std::cout << "\n12. Real-world example: Command parser:\n";
    
    struct Command {
        std::string name;
        std::vector<std::any> args;
        
        void execute() const {
            if (name == "print") {
                for (const auto& arg : args) {
                    if (arg.type() == typeid(std::string)) {
                        std::cout << std::any_cast<std::string>(arg);
                    }
                    else if (arg.type() == typeid(int)) {
                        std::cout << std::any_cast<int>(arg);
                    }
                }
                std::cout << "\n";
            }
            else if (name == "add") {
                if (args.size() == 2) {
                    int a = std::any_cast<int>(args[0]);
                    int b = std::any_cast<int>(args[1]);
                    std::cout << a << " + " << b << " = " << (a + b) << "\n";
                }
            }
        }
    };
    
    Command cmd1{"print", {std::string("Hello "), std::string("World!")}};
    Command cmd2{"add", {10, 20}};
    
    cmd1.execute();
    cmd2.execute();
    
    // ============================================================================
    // SUMMARY
    // ============================================================================
    
    std::cout << "\n=== std::any SUMMARY ===\n";
    std::cout << "Advantages:\n";
    std::cout << "  - True heterogeneous storage\n";
    std::cout << "  - Type-safe (unlike void*)\n";
    std::cout << "  - Small Buffer Optimization\n";
    std::cout << "  - Standard library support\n";
    
    std::cout << "\nDisadvantages:\n";
    std::cout << "  - Runtime type checking overhead\n";
    std::cout << "  - No compile-time type safety\n";
    std::cout << "  - Can't use with templates easily\n";
    std::cout << "  - Visitor pattern needed for operations\n";
    
    std::cout << "\nBest practices:\n";
    std::cout << "  1. Use for truly dynamic types\n";
    std::cout << "  2. Prefer variant when types known at compile time\n";
    std::cout << "  3. Always check type before casting\n";
    std::cout << "  4. Consider performance implications\n";
    std::cout << "  5. Use with polymorphism carefully\n";
}

#include <iostream>
#include <any>
#include <vector>
#include <string>
#include <typeinfo>
#include <type_traits>
#include <cassert>

void demonstrate_any() {
    std::cout << "\n=== std::any (C++17) ===\n";
    
    // ============================================================================
    // 1. WHAT IS std::any?
    // ============================================================================
    
    // std::any is a type-safe container for single values of any type
    // Similar to void* but with type safety
    
    // ============================================================================
    // 2. BASIC USAGE
    // ============================================================================
    
    std::cout << "\n1. Basic usage:\n";
    
    std::any value;
    
    // Store different types
    value = 42;  // int
    std::cout << "Stored int: " << std::any_cast<int>(value) << "\n";
    
    value = 3.14159;  // double
    std::cout << "Stored double: " << std::any_cast<double>(value) << "\n";
    
    value = std::string("Hello");  // std::string
    std::cout << "Stored string: " << std::any_cast<std::string>(value) << "\n";
    
    value = 'A';  // char
    std::cout << "Stored char: " << std::any_cast<char>(value) << "\n";
    
    // ============================================================================
    // 3. TYPE SAFETY
    // ============================================================================
    
    std::cout << "\n2. Type safety:\n";
    
    value = 100;
    
    try {
        // Wrong type cast throws std::bad_any_cast
        double d = std::any_cast<double>(value);
        std::cout << "This won't print\n";
    }
    catch (const std::bad_any_cast& e) {
        std::cout << "Caught bad_any_cast: " << e.what() << "\n";
    }
    
    // Safe cast with pointer (returns nullptr if wrong type)
    if (int* ptr = std::any_cast<int>(&value)) {
        std::cout << "Successfully cast to int: " << *ptr << "\n";
    }
    
    if (double* ptr = std::any_cast<double>(&value)) {
        std::cout << "This won't print (wrong type)\n";
    }
    
    // ============================================================================
    // 4. ANY OPERATIONS
    // ============================================================================
    
    std::cout << "\n3. Any operations:\n";
    
    std::any a;
    
    // Check if contains a value
    std::cout << "Initially has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    a = 42;
    std::cout << "After assignment has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // Get type information
    std::cout << "Type name: " << a.type().name() << "\n";
    
    // Reset/clear
    a.reset();
    std::cout << "After reset has value? " << (a.has_value() ? "Yes" : "No") << "\n";
    
    // ============================================================================
    // 5. STORING COMPLEX TYPES
    // ============================================================================
    
    std::cout << "\n4. Storing complex types:\n";
    
    // Store custom types
    struct Person {
        std::string name;
        int age;
        
        void print() const {
            std::cout << name << " (" << age << ")\n";
        }
    };
    
    Person alice{"Alice", 30};
    std::any person_any = alice;
    
    // Access custom type
    Person retrieved = std::any_cast<Person>(person_any);
    retrieved.print();
    
    // Store containers
    std::any vector_any = std::vector<int>{1, 2, 3, 4, 5};
    auto& vec_ref = std::any_cast<std::vector<int>&>(vector_any);
    vec_ref.push_back(6);
    
    std::cout << "Vector in any: ";
    for (int n : vec_ref) std::cout << n << " ";
    std::cout << "\n";
    
    // ============================================================================
    // 6. ANY IN CONTAINERS
    // ============================================================================
    
    std::cout << "\n5. Any in containers (heterogeneous collections):\n";
    
    std::vector<std::any> heterogeneous;
    
    heterogeneous.push_back(42);
    heterogeneous.push_back(3.14);
    heterogeneous.push_back(std::string("Hello"));
    heterogeneous.push_back(true);
    heterogeneous.push_back(std::vector<int>{1, 2, 3});
    
    std::cout << "Heterogeneous collection:\n";
    for (const auto& item : heterogeneous) {
        if (item.type() == typeid(int)) {
            std::cout << "  int: " << std::any_cast<int>(item) << "\n";
        }
        else if (item.type() == typeid(double)) {
            std::cout << "  double: " << std::any_cast<double>(item) << "\n";
        }
        else if (item.type() == typeid(std::string)) {
            std::cout << "  string: " << std::any_cast<std::string>(item) << "\n";
        }
        else if (item.type() == typeid(bool)) {
            std::cout << "  bool: " << std::any_cast<bool>(item) << "\n";
        }
        else if (item.type() == typeid(std::vector<int>)) {
            std::cout << "  vector<int>: ";
            for (int n : std::any_cast<std::vector<int>>(item)) {
                std::cout << n << " ";
            }
            std::cout << "\n";
        }
    }
    
    // ============================================================================
    // 7. VISITOR PATTERN WITH ANY
    // ============================================================================
    
    std::cout << "\n6. Visitor pattern with any:\n";
    
    // Function to handle any type
    auto print_any = [](const std::any& a) {
        if (a.type() == typeid(int)) {
            std::cout << "Integer: " << std::any_cast<int>(a) << "\n";
        }
        else if (a.type() == typeid(double)) {
            std::cout << "Double: " << std::any_cast<double>(a) << "\n";
        }
        else if (a.type() == typeid(std::string)) {
            std::cout << "String: " << std::any_cast<std::string>(a) << "\n";
        }
        else {
            std::cout << "Unknown type: " << a.type().name() << "\n";
        }
    };
    
    std::any var1 = 100;
    std::any var2 = 2.71828;
    std::any var3 = std::string("Euler's number");
    
    print_any(var1);
    print_any(var2);
    print_any(var3);
    
    // ============================================================================
    // 8. ANY WITH POLYMORPHIC TYPES
    // ============================================================================
    
    std::cout << "\n7. Any with polymorphic types:\n";
    
    class Shape {
    public:
        virtual ~Shape() = default;
        virtual void draw() const = 0;
    };
    
    class Circle : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Circle\n";
        }
    };
    
    class Square : public Shape {
    public:
        void draw() const override {
            std::cout << "Drawing Square\n";
        }
    };
    
    // Store polymorphic objects in any
    std::any shape1 = Circle{};
    std::any shape2 = Square{};
    
    // Need to cast to base pointer/reference
    auto draw_shape = [](const std::any& shape) {
        if (shape.type() == typeid(Circle)) {
            std::any_cast<Circle>(shape).draw();
        }
        else if (shape.type() == typeid(Square)) {
            std::any_cast<Square>(shape).draw();
        }
    };
    
    draw_shape(shape1);
    draw_shape(shape2);
    
    // Better: Store std::unique_ptr<Shape>
    std::any ptr_shape = std::make_unique<Circle>();
    if (auto* ptr = std::any_cast<std::unique_ptr<Shape>>(&ptr_shape)) {
        (*ptr)->draw();
    }
    
    // ============================================================================
    // 9. ANY FOR CONFIGURATION DATA
    // ============================================================================
    
    std::cout << "\n8. Any for configuration data:\n";
    
    // std::any is useful for configuration settings that can be different types
    std::map<std::string, std::any> config;
    
    config["timeout"] = 30;              // int
    config["pi"] = 3.14159;              // double
    config["name"] = std::string("app"); // string
    config["verbose"] = true;            // bool
    config["ports"] = std::vector<int>{80, 443}; // vector
    
    // Retrieve with type checking
    auto get_config = [&config](const std::string& key) -> std::any {
        auto it = config.find(key);
        if (it != config.end()) {
            return it->second;
        }
        return {};  // empty any
    };
    
    if (auto timeout = get_config("timeout"); timeout.has_value()) {
        std::cout << "Timeout: " << std::any_cast<int>(timeout) << " seconds\n";
    }
    
    // ============================================================================
    // 10. PERFORMANCE CONSIDERATIONS
    // ============================================================================
    
    std::cout << "\n9. Performance considerations:\n";
    
    // std::any uses small buffer optimization (SBO)
    // Small types are stored inline, large types on heap
    
    std::any small = 'X';      // Likely stored inline
    std::any medium = 3.14;    // Likely stored inline
    std::any large = std::vector<int>(1000);  // Likely heap allocated
    
    std::cout << "Small type in any: " << std::any_cast<char>(small) << "\n";
    std::cout << "Implementation uses SBO for efficiency\n";
    
    // Type casting has runtime cost (type checking)
    // Not suitable for performance-critical code
    
    // ============================================================================
    // 11. ANY VS VARIANT VS OPTIONAL
    // ============================================================================
    
    std::cout << "\n10. Any vs Variant vs Optional:\n";
    
    // std::any: Any type, runtime type checking
    // std::variant: Type-safe union, compile-time known types
    // std::optional: Maybe a value of specific type
    
    std::any any_value;           // Can be anything
    std::variant<int, double, std::string> variant_value;  // One of these three
    std::optional<int> optional_value;  // Maybe an int, maybe nothing
    
    std::cout << "Use std::any when:\n";
    std::cout << "  - You truly need any type\n";
    std::cout << "  - Types are determined at runtime\n";
    std::cout << "  - You need maximum flexibility\n";
    
    std::cout << "\nPrefer std::variant when:\n";
    std::cout << "  - Possible types are known at compile time\n";
    std::cout << "  - You want type safety\n";
    std::cout << "  - You want to use std::visit\n";
    
    std::cout << "\nUse std::optional when:\n";
    std::cout << "  - You need 'maybe a value of specific type'\n";
    
    // ============================================================================
    // 12. ADVANCED: ANY WITH CUSTOM TYPE INFO
    // ============================================================================
    
    std::cout << "\n11. Advanced: Custom type handling:\n";
    
    // Register types with custom handlers
    struct TypeHandler {
        std::string type_name;
        std::function<void(const std::any&)> printer;
    };
    
    std::map<std::type_index, TypeHandler> handlers;
    
    handlers[typeid(int)] = {"int", [](const std::any& a) {
        std::cout << "Integer: " << std::any_cast<int>(a) << "\n";
    }};
    
    handlers[typeid(std::string)] = {"string", [](const std::any& a) {
        std::cout << "String: " << std::any_cast<std::string>(a) << "\n";
    }};
    
    // Use handlers
    std::any data1 = 42;
    std::any data2 = std::string("test");
    
    auto it1 = handlers.find(data1.type());
    if (it1 != handlers.end()) {
        std::cout << "Type: " << it1->second.type_name << " -> ";
        it1->second.printer(data1);
    }
    
    auto it2 = handlers.find(data2.type());
    if (it2 != handlers.end()) {
        std::cout << "Type: " << it2->second.type_name << " -> ";
        it2->second.printer(data2);
    }
    
    // ============================================================================
    // 13. REAL-WORLD EXAMPLE: COMMAND PARSER
    // ============================================================================
    
    std::cout << "\n12. Real-world example: Command parser:\n";
    
    struct Command {
        std::string name;
        std::vector<std::any> args;
        
        void execute() const {
            if (name == "print") {
                for (const auto& arg : args) {
                    if (arg.type() == typeid(std::string)) {
                        std::cout << std::any_cast<std::string>(arg);
                    }
                    else if (arg.type() == typeid(int)) {
                        std::cout << std::any_cast<int>(arg);
                    }
                }
                std::cout << "\n";
            }
            else if (name == "add") {
                if (args.size() == 2) {
                    int a = std::any_cast<int>(args[0]);
                    int b = std::any_cast<int>(args[1]);
                    std::cout << a << " + " << b << " = " << (a + b) << "\n";
                }
            }
        }
    };
    
    Command cmd1{"print", {std::string("Hello "), std::string("World!")}};
    Command cmd2{"add", {10, 20}};
    
    cmd1.execute();
    cmd2.execute();
    
    // ============================================================================
    // SUMMARY
    // ============================================================================
    
    std::cout << "\n=== std::any SUMMARY ===\n";
    std::cout << "Advantages:\n";
    std::cout << "  - True heterogeneous storage\n";
    std::cout << "  - Type-safe (unlike void*)\n";
    std::cout << "  - Small Buffer Optimization\n";
    std::cout << "  - Standard library support\n";
    
    std::cout << "\nDisadvantages:\n";
    std::cout << "  - Runtime type checking overhead\n";
    std::cout << "  - No compile-time type safety\n";
    std::cout << "  - Can't use with templates easily\n";
    std::cout << "  - Visitor pattern needed for operations\n";
    
    std::cout << "\nBest practices:\n";
    std::cout << "  1. Use for truly dynamic types\n";
    std::cout << "  2. Prefer variant when types known at compile time\n";
    std::cout << "  3. Always check type before casting\n";
    std::cout << "  4. Consider performance implications\n";
    std::cout << "  5. Use with polymorphism carefully\n";
}

