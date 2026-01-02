#include <iostream>
#include <vector>
#include <string>
#include <type_traits>
#include <concepts>  // C++20
#include <algorithm>
#include <memory>

// ============ 1. FUNCTION TEMPLATES ============

// Basic function template
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Multiple type parameters
template<typename T, typename U>
auto add(T a, U b) {
    return a + b;
}

// Non-type template parameters
template<typename T, int Size>
class FixedArray {
    T data[Size];
public:
    T& operator[](int index) { return data[index]; }
    const T& operator[](int index) const { return data[index]; }
    int size() const { return Size; }
};

void demonstrate_function_templates() {
    std::cout << "============ FUNCTION TEMPLATES ============\n" << std::endl;
    
    // Type deduction
    std::cout << "max(3, 5) = " << max(3, 5) << std::endl;        // T = int
    std::cout << "max(3.14, 2.71) = " << max(3.14, 2.71) << std::endl; // T = double
    std::cout << "max('a', 'z') = " << max('a', 'z') << std::endl; // T = char
    
    // Explicit template arguments
    std::cout << "max<double>(3, 5.5) = " << max<double>(3, 5.5) << std::endl;
    
    // Multiple types
    std::cout << "add(3, 4.5) = " << add(3, 4.5) << std::endl;    // T = int, U = double
    
    // Non-type parameters
    FixedArray<int, 10> array;
    array[0] = 42;
    std::cout << "FixedArray size: " << array.size() << std::endl;
}

// ============ 2. CLASS TEMPLATES ============

template<typename T>
class Box {
    T value;
public:
    Box(const T& val) : value(val) {}
    
    T get() const { return value; }
    void set(const T& val) { value = val; }
    
    // Member function template
    template<typename U>
    bool is_same_type() const {
        return std::is_same_v<T, U>;
    }
};

// Template with default arguments
template<typename T = int, typename Container = std::vector<T>>
class Stack {
    Container elements;
public:
    void push(const T& value) { elements.push_back(value); }
    T pop() {
        T value = elements.back();
        elements.pop_back();
        return value;
    }
    bool empty() const { return elements.empty(); }
};

void demonstrate_class_templates() {
    std::cout << "\n============ CLASS TEMPLATES ============\n" << std::endl;
    
    Box<int> intBox(42);
    std::cout << "intBox value: " << intBox.get() << std::endl;
    
    Box<std::string> stringBox("Hello");
    std::cout << "stringBox value: " << stringBox.get() << std::endl;
    
    // Using default template arguments
    Stack<> defaultStack;  // T = int, Container = vector<int>
    defaultStack.push(10);
    defaultStack.push(20);
    std::cout << "Stack popped: " << defaultStack.pop() << std::endl;
    
    // Custom container
    Stack<double, std::vector<double>> doubleStack;
    doubleStack.push(3.14);
    
    // Member template function
    std::cout << "intBox is same as int? " << intBox.is_same_type<int>() << std::endl;
    std::cout << "intBox is same as double? " << intBox.is_same_type<double>() << std::endl;
}

// ============ 3. TEMPLATE SPECIALIZATION ============

// Primary template
template<typename T>
class TypeInfo {
public:
    static std::string name() { return "unknown"; }
};

// Full specialization for int
template<>
class TypeInfo<int> {
public:
    static std::string name() { return "int"; }
};

// Full specialization for double
template<>
class TypeInfo<double> {
public:
    static std::string name() { return "double"; }
};

// Partial specialization for pointers
template<typename T>
class TypeInfo<T*> {
public:
    static std::string name() { return TypeInfo<T>::name() + "*"; }
};

// Partial specialization for references
template<typename T>
class TypeInfo<T&> {
public:
    static std::string name() { return TypeInfo<T>::name() + "&"; }
};

// Function template specialization
template<typename T>
void print_type() {
    std::cout << "Generic type" << std::endl;
}

template<>
void print_type<int>() {
    std::cout << "Specialized for int" << std::endl;
}

void demonstrate_specialization() {
    std::cout << "\n============ TEMPLATE SPECIALIZATION ============\n" << std::endl;
    
    std::cout << "TypeInfo<int>::name(): " << TypeInfo<int>::name() << std::endl;
    std::cout << "TypeInfo<double>::name(): " << TypeInfo<double>::name() << std::endl;
    std::cout << "TypeInfo<float>::name(): " << TypeInfo<float>::name() << std::endl;
    std::cout << "TypeInfo<int*>::name(): " << TypeInfo<int*>::name() << std::endl;
    std::cout << "TypeInfo<double&>::name(): " << TypeInfo<double&>::name() << std::endl;
    std::cout << "TypeInfo<int**>::name(): " << TypeInfo<int**>::name() << std::endl;
    
    print_type<double>();
    print_type<int>();
}

// ============ 4. VARIADIC TEMPLATES (C++11) ============

// Base case
void print_all() {
    std::cout << std::endl;
}

// Recursive variadic template
template<typename T, typename... Args>
void print_all(T first, Args... args) {
    std::cout << first << " ";
    print_all(args...);
}

// Fold expressions (C++17)
template<typename... Args>
auto sum_all(Args... args) {
    return (... + args);  // Fold expression
}

template<typename... Args>
void print_all_fold(Args... args) {
    (std::cout << ... << args) << std::endl;  // Fold expression
}

// Variadic class template
template<typename... Types>
class Tuple {};

template<typename First, typename... Rest>
class Tuple<First, Rest...> {
    First first;
    Tuple<Rest...> rest;
public:
    Tuple(First f, Rest... r) : first(f), rest(r...) {}
    
    First get_first() const { return first; }
    Tuple<Rest...> get_rest() const { return rest; }
};

void demonstrate_variadic_templates() {
    std::cout << "\n============ VARIADIC TEMPLATES ============\n" << std::endl;
    
    std::cout << "Recursive print: ";
    print_all(1, 2.5, "hello", 'a');
    
    std::cout << "Fold expression sum: " << sum_all(1, 2, 3, 4, 5) << std::endl;
    
    std::cout << "Fold expression print: ";
    print_all_fold(1, " + ", 2, " = ", 3);
    
    // Perfect forwarding with variadic templates
    auto make_unique = [](auto&&... args) {
        return std::make_unique<std::string>(std::forward<decltype(args)>(args)...);
    };
    
    auto str = make_unique("Hello, World!");
    std::cout << "Made unique string: " << *str << std::endl;
}

// ============ 5. TYPE TRAITS & SFINAE ============

// SFINAE (Substitution Failure Is Not An Error)
template<typename T>
typename std::enable_if<std::is_integral<T>::value, T>::type
increment(T value) {
    return value + 1;
}

template<typename T>
typename std::enable_if<std::is_floating_point<T>::value, T>::type
increment(T value) {
    return value + 0.1;
}

// Using type traits
template<typename T>
void process_integral(T value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "Integral: " << value << std::endl;
    } else if constexpr (std::is_floating_point_v<T>) {
        std::cout << "Floating: " << value << std::endl;
    } else {
        std::cout << "Other type" << std::endl;
    }
}

// SFINAE with decltype
template<typename T>
auto get_value(T t) -> decltype(t.get()) {
    return t.get();
}

template<typename T>
auto get_value(T* t) -> T {
    return *t;
}

void demonstrate_type_traits() {
    std::cout << "\n============ TYPE TRAITS & SFINAE ============\n" << std::endl;
    
    std::cout << "increment(5) = " << increment(5) << std::endl;
    std::cout << "increment(3.14) = " << increment(3.14) << std::endl;
    // increment("hello");  // Error - no matching function
    
    process_integral(10);
    process_integral(3.14);
    process_integral("hello");
    
    // Type traits examples
    std::cout << "\nType traits:" << std::endl;
    std::cout << "is_integral<int>: " << std::is_integral<int>::value << std::endl;
    std::cout << "is_pointer<int*>: " << std::is_pointer<int*>::value << std::endl;
    std::cout << "is_same<int, double>: " << std::is_same<int, double>::value << std::endl;
    
    // Transform types
    using IntPtr = std::add_pointer_t<int>;
    std::cout << "add_pointer_t<int> is same as int*: " 
              << std::is_same<IntPtr, int*>::value << std::endl;
}

// ============ 6. TEMPLATE METAPROGRAMMING ============

// Compile-time factorial
template<int N>
struct Factorial {
    static const int value = N * Factorial<N-1>::value;
};

template<>
struct Factorial<0> {
    static const int value = 1;
};

// Compile-time Fibonacci
template<int N>
struct Fibonacci {
    static const int value = Fibonacci<N-1>::value + Fibonacci<N-2>::value;
};

template<>
struct Fibonacci<0> {
    static const int value = 0;
};

template<>
struct Fibonacci<1> {
    static const int value = 1;
};

// Type list manipulation
template<typename... Types>
struct TypeList {};

template<typename List>
struct Front;

template<typename First, typename... Rest>
struct Front<TypeList<First, Rest...>> {
    using type = First;
};

template<typename List>
struct Size;

template<typename... Types>
struct Size<TypeList<Types...>> {
    static constexpr std::size_t value = sizeof...(Types);
};

void demonstrate_template_metaprogramming() {
    std::cout << "\n============ TEMPLATE METAPROGRAMMING ============\n" << std::endl;
    
    std::cout << "Factorial<5>::value = " << Factorial<5>::value << std::endl;
    std::cout << "Factorial<10>::value = " << Factorial<10>::value << std::endl;
    
    std::cout << "Fibonacci<10>::value = " << Fibonacci<10>::value << std::endl;
    
    using MyList = TypeList<int, double, char, std::string>;
    std::cout << "Size of TypeList<int, double, char, string>: " 
              << Size<MyList>::value << std::endl;
    
    using FirstType = typename Front<MyList>::type;
    std::cout << "First type in list: " << typeid(FirstType).name() << std::endl;
}

// ============ 7. CONCEPTS (C++20) ============

#ifdef __cpp_concepts
// Basic concept
template<typename T>
concept Integral = std::is_integral_v<T>;

template<typename T>
concept FloatingPoint = std::is_floating_point_v<T>;

template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

// Using concepts
template<Integral T>
T square_int(T x) {
    return x * x;
}

template<FloatingPoint T>
T square_float(T x) {
    return x * x;
}

template<Addable T>
T add_concept(T a, T b) {
    return a + b;
}

// Compound concepts
template<typename T>
concept Numeric = Integral<T> || FloatingPoint<T>;

template<Numeric T>
T process_numeric(T value) {
    return value * 2;
}

// Concept with auto
void print_integral(Integral auto value) {
    std::cout << "Integral: " << value << std::endl;
}
#endif

void demonstrate_concepts() {
    std::cout << "\n============ CONCEPTS (C++20) ============\n" << std::endl;
    
    #ifdef __cpp_concepts
    std::cout << "square_int(5) = " << square_int(5) << std::endl;
    std::cout << "square_float(3.14) = " << square_float(3.14) << std::endl;
    // square_int(3.14);  // Error: doesn't satisfy Integral concept
    
    std::cout << "add_concept(10, 20) = " << add_concept(10, 20) << std::endl;
    std::cout << "process_numeric(5) = " << process_numeric(5) << std::endl;
    std::cout << "process_numeric(3.14) = " << process_numeric(3.14) << std::endl;
    
    print_integral(42);
    // print_integral(3.14);  // Error
    #else
    std::cout << "Concepts not supported in this compiler" << std::endl;
    #endif
}

// ============ 8. TEMPLATE TEMPLATE PARAMETERS ============

template<template<typename> class Container, typename T>
class Wrapper {
    Container<T> data;
public:
    void add(const T& value) { data.push_back(value); }
    T get(int index) const { return data[index]; }
};

// Can be used with any container that has push_back and operator[]
template<typename T>
using MyVector = std::vector<T>;

void demonstrate_template_template() {
    std::cout << "\n============ TEMPLATE TEMPLATE PARAMETERS ============\n" << std::endl;
    
    Wrapper<std::vector, int> wrapper;
    wrapper.add(10);
    wrapper.add(20);
    std::cout << "Wrapper get(0): " << wrapper.get(0) << std::endl;
    
    // Using alias
    Wrapper<MyVector, std::string> stringWrapper;
    stringWrapper.add("Hello");
    stringWrapper.add("World");
}

// ============ 9. ADVANCED TEMPLATE PATTERNS ============

// CRTP (Curiously Recurring Template Pattern)
template<typename Derived>
class Base {
public:
    void interface() {
        static_cast<Derived*>(this)->implementation();
    }
    
    static void static_interface() {
        Derived::static_implementation();
    }
};

class Derived1 : public Base<Derived1> {
public:
    void implementation() {
        std::cout << "Derived1 implementation" << std::endl;
    }
    
    static void static_implementation() {
        std::cout << "Derived1 static implementation" << std::endl;
    }
};

class Derived2 : public Base<Derived2> {
public:
    void implementation() {
        std::cout << "Derived2 implementation" << std::endl;
    }
    
    static void static_implementation() {
        std::cout << "Derived2 static implementation" << std::endl;
    }
};

// Type erasure with templates
template<typename T>
class TypeErasure {
    struct Concept {
        virtual ~Concept() = default;
        virtual void print() const = 0;
        virtual std::unique_ptr<Concept> clone() const = 0;
    };
    
    template<typename U>
    struct Model : Concept {
        U data;
        Model(const U& d) : data(d) {}
        void print() const override { std::cout << data << std::endl; }
        std::unique_ptr<Concept> clone() const override {
            return std::make_unique<Model>(data);
        }
    };
    
    std::unique_ptr<Concept> object;
    
public:
    template<typename U>
    TypeErasure(U&& value) : object(std::make_unique<Model<std::decay_t<U>>>(std::forward<U>(value))) {}
    
    TypeErasure(const TypeErasure& other) : object(other.object ? other.object->clone() : nullptr) {}
    
    void print() const {
        if (object) object->print();
    }
};

// Expression templates for optimization
template<typename Lhs, typename Rhs>
struct AddExpr {
    const Lhs& lhs;
    const Rhs& rhs;
    
    AddExpr(const Lhs& l, const Rhs& r) : lhs(l), rhs(r) {}
    
    auto operator[](std::size_t i) const {
        return lhs[i] + rhs[i];
    }
};

template<typename T>
class Vector {
    std::vector<T> data;
public:
    Vector(std::size_t size, T value = T{}) : data(size, value) {}
    
    template<typename Expr>
    Vector& operator=(const Expr& expr) {
        for (std::size_t i = 0; i < data.size(); ++i) {
            data[i] = expr[i];
        }
        return *this;
    }
    
    T operator[](std::size_t i) const { return data[i]; }
    T& operator[](std::size_t i) { return data[i]; }
    
    std::size_t size() const { return data.size(); }
};

template<typename Lhs, typename Rhs>
auto operator+(const Lhs& lhs, const Rhs& rhs) {
    return AddExpr<Lhs, Rhs>(lhs, rhs);
}

void demonstrate_advanced_patterns() {
    std::cout << "\n============ ADVANCED TEMPLATE PATTERNS ============\n" << std::endl;
    
    // CRTP
    std::cout << "=== CRTP ===" << std::endl;
    Derived1 d1;
    Derived2 d2;
    d1.interface();
    d2.interface();
    Derived1::static_interface();
    Derived2::static_interface();
    
    // Type erasure
    std::cout << "\n=== Type Erasure ===" << std::endl;
    TypeErasure<int> te1(42);
    TypeErasure<std::string> te2("Hello");
    te1.print();
    te2.print();
    
    // Expression templates
    std::cout << "\n=== Expression Templates ===" << std::endl;
    Vector<double> v1(3, 1.0);
    Vector<double> v2(3, 2.0);
    Vector<double> v3(3, 0.0);
    
    v3 = v1 + v2;  // No temporary vectors created!
    
    for (std::size_t i = 0; i < v3.size(); ++i) {
        std::cout << "v3[" << i << "] = " << v3[i] << std::endl;
    }
}

// ============ 10. TEMPLATE BEST PRACTICES & PITFALLS ============

void demonstrate_best_practices() {
    std::cout << "\n============ TEMPLATE BEST PRACTICES ============\n" << std::endl;
    
    std::cout << "=== Best Practices ===" << std::endl;
    std::cout << "1. Use typename for dependent types" << std::endl;
    std::cout << "   template<typename T>" << std::endl;
    std::cout << "   typename T::value_type get_value(const T& container)" << std::endl;
    
    std::cout << "\n2. Prefer const references for template parameters" << std::endl;
    std::cout << "   template<typename T>" << std::endl;
    std::cout << "   void process(const T& obj)  // Avoids unnecessary copies" << std::endl;
    
    std::cout << "\n3. Use perfect forwarding for factory functions" << std::endl;
    std::cout << "   template<typename T, typename... Args>" << std::endl;
    std::cout << "   T create(Args&&... args) {" << std::endl;
    std::cout << "       return T(std::forward<Args>(args)...);" << std::endl;
    std::cout << "   }" << std::endl;
    
    std::cout << "\n4. Separate declaration and definition in headers" << std::endl;
    std::cout << "   // .hpp file" << std::endl;
    std::cout << "   template<typename T>" << std::endl;
    std::cout << "   class MyClass {" << std::endl;
    std::cout << "   public:" << std::endl;
    std::cout << "       void method();" << std::endl;
    std::cout << "   };" << std::endl;
    std::cout << "   " << std::endl;
    std::cout << "   // Inline in same header" << std::endl;
    std::cout << "   template<typename T>" << std::endl;
    std::cout << "   void MyClass<T>::method() { /* implementation */ }" << std::endl;
    
    std::cout << "\n5. Use concepts (C++20) for better error messages" << std::endl;
    std::cout << "   template<Integral T>" << std::endl;
    std::cout << "   T square(T x) { return x * x; }" << std::endl;
    
    std::cout << "\n=== Common Pitfalls ===" << std::endl;
    std::cout << "1. Template code bloat (instantiated for each type)" << std::endl;
    std::cout << "   Solution: Factor common code into non-template base" << std::endl;
    
    std::cout << "\n2. Two-phase lookup issues" << std::endl;
    std::cout << "   template<typename T>" << std::endl;
    std::cout << "   void foo() {" << std::endl;
    std::cout << "       bar();  // Must be visible at template definition time" << std::endl;
    std::cout << "   }" << std::endl;
    
    std::cout << "\n3. All template code must be in headers" << std::endl;
    std::cout << "   (Or use explicit instantiation in .cpp files)" << std::endl;
    
    std::cout << "\n4. Default arguments in template template parameters" << std::endl;
    std::cout << "   template<template<typename T = int> class Container>" << std::endl;
    std::cout << "   class Widget {};  // Problematic" << std::endl;
    
    std::cout << "\n5. Non-type template parameter limitations" << std::endl;
    std::cout << "   Must be integral, enum, pointer, or reference types" << std::endl;
}

// ============ 11. REAL-WORLD TEMPLATE EXAMPLES ============

// Smart pointer implementation
template<typename T>
class SimpleUniquePtr {
    T* ptr;
public:
    explicit SimpleUniquePtr(T* p = nullptr) : ptr(p) {}
    ~SimpleUniquePtr() { delete ptr; }
    
    // Delete copy operations
    SimpleUniquePtr(const SimpleUniquePtr&) = delete;
    SimpleUniquePtr& operator=(const SimpleUniquePtr&) = delete;
    
    // Move operations
    SimpleUniquePtr(SimpleUniquePtr&& other) noexcept : ptr(other.ptr) {
        other.ptr = nullptr;
    }
    
    SimpleUniquePtr& operator=(SimpleUniquePtr&& other) noexcept {
        if (this != &other) {
            delete ptr;
            ptr = other.ptr;
            other.ptr = nullptr;
        }
        return *this;
    }
    
    T& operator*() const { return *ptr; }
    T* operator->() const { return ptr; }
    T* get() const { return ptr; }
    
    // Reset functionality
    void reset(T* p = nullptr) {
        delete ptr;
        ptr = p;
    }
    
    // Release ownership
    T* release() {
        T* temp = ptr;
        ptr = nullptr;
        return temp;
    }
};

// Generic function object wrapper
template<typename T>
class Function;

template<typename Ret, typename... Args>
class Function<Ret(Args...)> {
    struct CallableBase {
        virtual ~CallableBase() = default;
        virtual Ret call(Args...) = 0;
        virtual std::unique_ptr<CallableBase> clone() const = 0;
    };
    
    template<typename F>
    struct Callable : CallableBase {
        F func;
        Callable(F f) : func(std::move(f)) {}
        Ret call(Args... args) override { return func(args...); }
        std::unique_ptr<CallableBase> clone() const override {
            return std::make_unique<Callable>(func);
        }
    };
    
    std::unique_ptr<CallableBase> callable;
    
public:
    Function() = default;
    
    template<typename F>
    Function(F f) : callable(std::make_unique<Callable<F>>(std::move(f))) {}
    
    Function(const Function& other) : 
        callable(other.callable ? other.callable->clone() : nullptr) {}
    
    Function& operator=(const Function& other) {
        if (this != &other) {
            callable = other.callable ? other.callable->clone() : nullptr;
        }
        return *this;
    }
    
    Ret operator()(Args... args) const {
        if (!callable) throw std::bad_function_call();
        return callable->call(args...);
    }
    
    explicit operator bool() const { return static_cast<bool>(callable); }
};

void demonstrate_real_world() {
    std::cout << "\n============ REAL-WORLD TEMPLATE EXAMPLES ============\n" << std::endl;
    
    // SimpleUniquePtr
    {
        SimpleUniquePtr<int> ptr(new int(42));
        std::cout << "SimpleUniquePtr value: " << *ptr << std::endl;
        
        SimpleUniquePtr<int> ptr2 = std::move(ptr);
        std::cout << "After move, ptr2 value: " << *ptr2 << std::endl;
    }
    
    // Function wrapper
    {
        Function<int(int, int)> add = [](int a, int b) { return a + b; };
        Function<int(int, int)> multiply = [](int a, int b) { return a * b; };
        
        std::cout << "add(3, 4) = " << add(3, 4) << std::endl;
        std::cout << "multiply(3, 4) = " << multiply(3, 4) << std::endl;
    }
}

int main() {
    demonstrate_function_templates();
    demonstrate_class_templates();
    demonstrate_specialization();
    demonstrate_variadic_templates();
    demonstrate_type_traits();
    demonstrate_template_metaprogramming();
    demonstrate_concepts();
    demonstrate_template_template();
    demonstrate_advanced_patterns();
    demonstrate_best_practices();
    demonstrate_real_world();
    
    return 0;
}


#include <iostream>
#include <vector>
#include <string>
#include <type_traits>
#include <memory>
#include <initializer_list>

// ============ 1. TEMPLATE ARGUMENT DEDUCTION GUIDES (C++17) ============

// Without deduction guide
template<typename T>
class Container {
    std::vector<T> data;
public:
    Container(const std::vector<T>& vec) : data(vec) {}
    
    template<typename Iter>
    Container(Iter begin, Iter end) : data(begin, end) {}
    
    void print() const {
        for (const auto& item : data) {
            std::cout << item << " ";
        }
        std::cout << std::endl;
    }
};

// With deduction guide (C++17)
template<typename Iter>
Container(Iter, Iter) -> Container<typename std::iterator_traits<Iter>::value_type>;

// Pair-like class
template<typename T1, typename T2>
class MyPair {
    T1 first;
    T2 second;
public:
    MyPair(T1 f, T2 s) : first(f), second(s) {}
    
    void print() const {
        std::cout << "(" << first << ", " << second << ")" << std::endl;
    }
};

// Deduction guide for MyPair
template<typename T1, typename T2>
MyPair(T1, T2) -> MyPair<T1, T2>;

// Complex example with inheritance
template<typename T>
class Base {
    T value;
public:
    Base(T v) : value(v) {}
};

// Deduction guide for derived class
template<typename T>
class Derived : public Base<T> {
public:
    Derived(T v) : Base<T>(v) {}
    
    // Additional constructor that needs deduction guide
    Derived(std::initializer_list<T> init) : Base<T>(init.size()) {}
};

// Deduction guide for initializer_list constructor
template<typename T>
Derived(std::initializer_list<T>) -> Derived<T>;

void demonstrate_deduction_guides() {
    std::cout << "============ TEMPLATE ARGUMENT DEDUCTION GUIDES (C++17) ============\n" << std::endl;
    
    // ============ Before C++17 ============
    std::cout << "=== Before C++17 ===" << std::endl;
    
    // Always had to specify template arguments
    std::vector<int> vec = {1, 2, 3, 4, 5};
    Container<int> c1(vec);  // Must specify <int>
    
    // With iterator constructor - even worse!
    // Container<int> c2(vec.begin(), vec.end());  // Couldn't deduce from iterators
    
    std::cout << "Container c1: ";
    c1.print();
    
    // ============ Class Template Argument Deduction (CTAD) ============
    std::cout << "\n=== C++17: Class Template Argument Deduction ===" << std::endl;
    
    // Now the compiler can deduce template arguments!
    Container c2(vec);  // Deduces Container<int>
    std::cout << "Container c2 (deduced): ";
    c2.print();
    
    // Even with iterators (thanks to deduction guide)
    Container c3(vec.begin(), vec.end());  // Deduces Container<int>
    std::cout << "Container c3 (from iterators): ";
    c3.print();
    
    // ============ MyPair Example ============
    std::cout << "\n=== MyPair Example ===" << std::endl;
    
    // Without deduction guide (C++17): need to specify types
    // MyPair<int, std::string> p1(42, "answer");
    
    // With deduction guide: types are deduced
    MyPair p1(42, "answer");
    std::cout << "MyPair p1: ";
    p1.print();
    
    MyPair p2(3.14, 2.71);
    std::cout << "MyPair p2: ";
    p2.print();
    
    // ============ Standard Library Examples ============
    std::cout << "\n=== Standard Library Examples ===" << std::endl;
    
    // C++17: No need to specify template arguments for common cases
    std::vector v = {1, 2, 3, 4, 5};  // Deduces vector<int>
    std::pair p(42, "hello");         // Deduces pair<int, const char*>
    std::tuple t(1, 2.5, "world");    // Deduces tuple<int, double, const char*>
    
    std::cout << "vector size: " << v.size() << std::endl;
    std::cout << "pair: (" << p.first << ", " << p.second << ")" << std::endl;
    
    // ============ Complex Deduction ============
    std::cout << "\n=== Complex Deduction ===" << std::endl;
    
    // Derived class with inheritance
    Derived d1(42);  // Deduces Derived<int>
    Derived d2({1, 2, 3});  // Deduces Derived<int> from initializer_list
    
    // ============ Explicit Deduction Guides ============
    std::cout << "\n=== Explicit Deduction Guides ===" << std::endl;
    
    // Sometimes you need to guide the deduction
    template<typename T>
    class Wrapper {
        T value;
    public:
        Wrapper(T v) : value(v) {}
        
        // Constructor from pointer - needs guidance
        Wrapper(T* ptr) : value(*ptr) {}
    };
    
    // Deduction guide for pointer constructor
    template<typename T>
    Wrapper(T*) -> Wrapper<T>;
    
    int x = 100;
    Wrapper w1(x);     // Deduces Wrapper<int>
    Wrapper w2(&x);    // Deduces Wrapper<int> (with guide)
    
    // ============ Aggregates with CTAD ============
    std::cout << "\n=== Aggregates with CTAD ===" << std::endl;
    
    template<typename T>
    struct Point {
        T x, y, z;
    };
    
    // For aggregates, CTAD works automatically in C++20
    #if __cplusplus >= 202002L
    Point p3{1.0, 2.0, 3.0};  // Deduces Point<double>
    #endif
    
    // ============ Limitations and Workarounds ============
    std::cout << "\n=== Limitations ===" << std::endl;
    
    std::cout << "1. Cannot deduce from inheritance alone:" << std::endl;
    /*
    template<typename T>
    class Base2 { T value; };
    
    template<typename T>
    class Derived2 : Base2<T> {};
    
    // Derived2 d;  // ERROR: Cannot deduce T
    */
    
    std::cout << "\n2. Ambiguous deduction:" << std::endl;
    /*
    template<typename T>
    class Ambiguous {
    public:
        Ambiguous(T) {}
        Ambiguous(const char*) {}  // Could be T = const char* or std::string
    };
    */
    
    std::cout << "\n3. Need explicit guides for complex patterns" << std::endl;
}

// ============ 2. typename vs class ============

// In template parameters, they are INTERCHANGEABLE
template<typename T>  // Preferred for type parameters
void func1(T value) {}

template<class T>     // Also works, but implies "class type"
void func2(T value) {}

// However, they have DIFFERENT meanings in other contexts

template<typename Container>
void print_container(const Container& container) {
    // typename is REQUIRED for dependent types
    typename Container::value_type first_element;
    // Without typename, compiler thinks value_type is a value, not a type
    
    typename Container::const_iterator it = container.begin();
    
    for (; it != container.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
}

// Dependent types in template parameters
template<typename T>
class Node {
    // typename needed for nested dependent type
    typename T::NestedType member;
    
    // But not here - T is the template parameter, not dependent
    T direct_member;
};

// Real-world example with traits
template<typename T>
void process() {
    // typename required for traits
    typename std::iterator_traits<T>::value_type value;
    typename std::iterator_traits<T>::difference_type diff;
    
    // Not required for non-dependent types
    std::size_t size;  // Not dependent on T
}

// The rule: Use typename when referring to a dependent type
// Dependent type = type that depends on a template parameter

void demonstrate_typename_vs_class() {
    std::cout << "\n============ typename vs class ============\n" << std::endl;
    
    // ============ In Template Parameters ============
    std::cout << "=== In Template Parameters ===" << std::endl;
    
    std::cout << "These are EQUIVALENT:" << std::endl;
    std::cout << "template<typename T>  // Preferred for clarity" << std::endl;
    std::cout << "template<class T>     // Works, but suggests 'class type'" << std::endl;
    
    std::cout << "\nModern C++ convention:" << std::endl;
    std::cout << "• Use typename for type parameters" << std::endl;
    std::cout << "• Use class only when parameter must be a class type" << std::endl;
    std::cout << "  (though both still accept any type)" << std::endl;
    
    // ============ typename for Dependent Types ============
    std::cout << "\n=== typename for Dependent Types ===" << std::endl;
    
    template<typename T>
    struct HasType {
        using type = T;  // Nested type
    };
    
    template<typename T>
    void example() {
        // ERROR without typename: 'HasType<T>::type' is a dependent name
        // typename HasType<T>::type value;  // Correct
        
        // Not dependent - no typename needed
        int x;
    }
    
    std::cout << "Rule: Use typename when referring to a nested type that" << std::endl;
    std::cout << "depends on a template parameter.\n" << std::endl;
    
    // ============ Common Patterns ============
    std::cout << "=== Common Patterns ===" << std::endl;
    
    // 1. Iterator types
    std::vector<int> vec = {1, 2, 3};
    typename std::vector<int>::iterator it = vec.begin();
    
    // 2. Type traits
    typename std::remove_reference<int&>::type non_ref;  // int
    
    // 3. Nested types in templates
    template<typename T>
    using ValueType = typename T::value_type;  // typename required!
    
    // ============ typename vs class Examples ============
    std::cout << "\n=== Comparison Examples ===" << std::endl;
    
    // Example 1: Template template parameter
    template<template<typename> class Container>  // Must use 'class' here
    class Adapter {
        Container<int> data;
    };
    
    // Example 2: Multiple parameters with different purposes
    template<
        typename T,           // Any type
        class Allocator,      // Should be a class (convention)
        typename = void       // Default template parameter
    >
    class AdvancedContainer {};
    
    // Example 3: Dependent scope resolution
    template<typename T>
    struct Outer {
        struct Inner {};
        
        template<typename U>
        struct Nested {};
    };
    
    template<typename T>
    void access_nested() {
        typename Outer<T>::Inner inner1;      // typename needed
        typename Outer<T>::template Nested<int> nested1;  // template keyword needed!
    }
    
    // ============ template keyword for Dependent Templates ============
    std::cout << "\n=== template keyword ===" << std::endl;
    
    std::cout << "When a dependent name is a template:" << std::endl;
    /*
    template<typename T>
    void call_template() {
        T::template nested_template<int>();  // template keyword required
    }
    */
    
    // ============ Best Practices ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Use typename for template type parameters" << std::endl;
    std::cout << "2. Use typename for dependent type names" << std::endl;
    std::cout << "3. Use class for template template parameters" << std::endl;
    std::cout << "4. Use class when emphasizing 'class type' (convention)" << std::endl;
    std::cout << "5. Remember: In template parameters, they're interchangeable" << std::endl;
    
    std::cout << "\nCommon error messages:" << std::endl;
    std::cout << "• 'missing typename before dependent type name'" << std::endl;
    std::cout << "• 'expected a type, got ...'" << std::endl;
}

// ============ 3. TEMPLATE INSTANTIATION ============

template<typename T>
T add(T a, T b) {
    return a + b;
}

// Explicit instantiation declaration
extern template int add<int>(int, int);

// Class template
template<typename T>
class Calculator {
    T value;
public:
    Calculator(T v) : value(v) {}
    
    T square() const {
        return value * value;
    }
    
    template<typename U>
    U convert() const {
        return static_cast<U>(value);
    }
};

// Explicit instantiation definitions
template int add<int>(int, int);
template class Calculator<double>;

// Special member functions can be instantiated separately
template class Calculator<std::string>;  // Instantiates all members
template std::string Calculator<int>::convert<std::string>() const;  // Just one member

void demonstrate_template_instantiation() {
    std::cout << "\n============ TEMPLATE INSTANTIATION ============\n" << std::endl;
    
    // ============ Implicit Instantiation ============
    std::cout << "=== Implicit Instantiation ===" << std::endl;
    
    // Code generated when template is used
    int result = add(3, 4);  // Instantiates add<int>
    std::cout << "add(3, 4) = " << result << std::endl;
    
    double dresult = add(3.14, 2.71);  // Instantiates add<double>
    std::cout << "add(3.14, 2.71) = " << dresult << std::endl;
    
    // Class template instantiation
    Calculator<int> calc(5);
    std::cout << "5² = " << calc.square() << std::endl;
    
    // ============ Two-Phase Lookup ============
    std::cout << "\n=== Two-Phase Lookup ===" << std::endl;
    
    // Phase 1: Template definition (non-dependent names)
    // Phase 2: Template instantiation (dependent names)
    
    template<typename T>
    void two_phase_example() {
        // Non-dependent - resolved at definition
        std::cout << "Hello";  // Must be visible when template defined
        
        // Dependent - resolved at instantiation
        T::static_method();  // Must be visible when template instantiated
        typename T::NestedType obj;
    }
    
    // ============ Explicit Instantiation ============
    std::cout << "\n=== Explicit Instantiation ===" << std::endl;
    
    // Forces instantiation in current translation unit
    template class Calculator<float>;
    
    // Benefits:
    std::cout << "1. Reduces compilation time (one compilation)" << std::endl;
    std::cout << "2. Reduces binary size (one copy in program)" << std::endl;
    std::cout << "3. Hides implementation in .cpp files" << std::endl;
    
    // ============ Explicit Instantiation Declaration ============
    std::cout << "\n=== Explicit Instantiation Declaration ===" << std::endl;
    
    // Tells compiler: "Don't instantiate here, it's defined elsewhere"
    extern template class Calculator<long>;
    
    // Used in headers to prevent instantiation in every TU
    
    // ============ Instantiation Location ============
    std::cout << "\n=== Where Templates Are Instantiated ===" << std::endl;
    
    std::cout << "Header file (usual):" << std::endl;
    std::cout << "  // math.hpp" << std::endl;
    std::cout << "  template<typename T> T add(T a, T b) { return a + b; }" << std::endl;
    
    std::cout << "\nSource file with explicit instantiation:" << std::endl;
    std::cout << "  // math.cpp" << std::endl;
    std::cout << "  #include \"math.hpp\"" << std::endl;
    std::cout << "  template int add<int>(int, int);" << std::endl;
    std::cout << "  template double add<double>(double, double);" << std::endl;
    
    // ============ Lazy Instantiation ============
    std::cout << "\n=== Lazy Instantiation ===" << std::endl;
    
    // Only members that are used get instantiated
    template<typename T>
    class LazyExample {
    public:
        void used() { std::cout << "Used method" << std::endl; }
        void unused() { T::non_existent_method(); }  // Error only if called
    };
    
    LazyExample<int> lazy;
    lazy.used();  // OK
    // lazy.unused();  // ERROR if uncommented
    
    // ============ Point of Instantiation ============
    std::cout << "\n=== Point of Instantiation ===" << std::endl;
    
    // For function templates: after the code that uses them
    // For class templates: at the point of use for each member
    
    // ============ Multiple Instantiations ============
    std::cout << "\n=== Multiple Instantiations ===" << std::endl;
    
    // Same template instantiated in different TUs
    // Linker merges them (One Definition Rule)
    
    // Problem: Different instantiations with same args?
    // Violates ODR - undefined behavior
    
    // ============ Template Instantiation Model ============
    std::cout << "\n=== Template Instantiation Models ===" << std::endl;
    
    std::cout << "1. Inclusion model (default):" << std::endl;
    std::cout << "   • Template definitions in headers" << std::endl;
    std::cout << "   • Instantiated in each TU that uses them" << std::endl;
    std::cout << "   • Linker removes duplicates" << std::endl;
    
    std::cout << "\n2. Separation model (deprecated):" << std::endl;
    std::cout << "   • export keyword (removed in C++11)" << std::endl;
    std::cout << "   • Never widely implemented" << std::endl;
    
    // ============ Instantiation Depth ============
    std::cout << "\n=== Instantiation Depth ===" << std::endl;
    
    // Recursive template instantiation
    template<int N>
    struct Factorial {
        static const int value = N * Factorial<N-1>::value;
    };
    
    template<>
    struct Factorial<0> {
        static const int value = 1;
    };
    
    // Compilers have limits (can be adjusted with -ftemplate-depth)
    std::cout << "Factorial<10> = " << Factorial<10>::value << std::endl;
    // Factorial<1000>::value;  // Might exceed compiler limits
}

// ============ 4. COMMON TEMPLATE ERRORS ============

template<typename T>
void ambiguous_template(T a, T b) {
    // Common error: ambiguous template parameter deduction
}

template<typename T>
void requires_increment(T value) {
    ++value;  // What if T doesn't support ++?
}

template<typename Container>
typename Container::value_type first_element(const Container& c) {
    // What if Container doesn't have value_type?
    return *c.begin();
}

void demonstrate_template_errors() {
    std::cout << "\n============ COMMON TEMPLATE ERRORS ============\n" << std::endl;
    
    // ============ 1. Ambiguous Template Argument Deduction ============
    std::cout << "=== 1. Ambiguous Template Argument Deduction ===" << std::endl;
    
    /*
    ambiguous_template(5, 5.0);  // ERROR: Cannot deduce T
    // Is T int or double?
    */
    
    // Solutions:
    std::cout << "Solutions:" << std::endl;
    std::cout << "1. Specify type explicitly: ambiguous_template<double>(5, 5.0)" << std::endl;
    std::cout << "2. Use different parameter types:" << std::endl;
    std::cout << "   template<typename T1, typename T2>" << std::endl;
    std::cout << "   void func(T1 a, T2 b)" << std::endl;
    
    // ============ 2. Missing typename ============
    std::cout << "\n=== 2. Missing typename ===" << std::endl;
    
    template<typename T>
    struct HasType {
        using type = T;
    };
    
    /*
    template<typename T>
    void missing_typename() {
        HasType<T>::type value;  // ERROR: missing 'typename'
    }
    */
    
    std::cout << "Error: expected a type, got HasType<T>::type" << std::endl;
    std::cout << "Fix: typename HasType<T>::type value;" << std::endl;
    
    // ============ 3. Missing template Keyword ============
    std::cout << "\n=== 3. Missing template Keyword ===" << std::endl;
    
    template<typename T>
    struct HasTemplate {
        template<typename U>
        static void method() {}
    };
    
    /*
    template<typename T>
    void missing_template() {
        HasTemplate<T>::method<int>();  // ERROR: < interpreted as less-than
    }
    */
    
    std::cout << "Error: expected primary-expression before '>' token" << std::endl;
    std::cout << "Fix: HasTemplate<T>::template method<int>();" << std::endl;
    
    // ============ 4. Template/Non-Template Name Hiding ============
    std::cout << "\n=== 4. Name Hiding ===" << std::endl;
    
    class Base {
    public:
        void method() {}  // Non-template
    };
    
    template<typename T>
    class Derived : public Base {
    public:
        template<typename U>
        void method() {  // Hides Base::method
            Base::method();  // Need to specify scope
        }
    };
    
    // ============ 5. Non-Deducible Contexts ============
    std::cout << "\n=== 5. Non-Deducible Contexts ===" << std::endl;
    
    /*
    template<typename T>
    void non_deducible(typename T::type value) {
        // T cannot be deduced from T::type
    }
    
    non_deducible(some_value);  // ERROR: Cannot deduce T
    */
    
    std::cout << "T appears in non-deducible context: T::type" << std::endl;
    std::cout << "Solution: Provide T explicitly or use different parameter" << std::endl;
    
    // ============ 6. Access Checking in Templates ============
    std::cout << "\n=== 6. Access Checking ===" << std::endl;
    
    class PrivateBase {
    private:
        typedef int secret_type;
    };
    
    template<typename T>
    class AccessCheck : public T {
    public:
        /*
        typename T::secret_type get_secret() {  // ERROR even if T=PrivateBase
            return 42;
        }
        */
    };
    
    std::cout << "Access checked at instantiation time, not definition" << std::endl;
    
    // ============ 7. Incomplete Types ============
    std::cout << "\n=== 7. Incomplete Types ===" << std::endl;
    
    class Incomplete;  // Forward declaration
    
    /*
    template<typename T>
    void use_size() {
        sizeof(T);  // ERROR if T is incomplete
    }
    
    use_size<Incomplete>();  // ERROR
    */
    
    // ============ 8. Instantiation Errors ============
    std::cout << "\n=== 8. Instantiation Errors ===" << std::endl;
    
    template<typename T>
    void requires_default_constructible() {
        T obj;  // Requires default constructor
    }
    
    class NoDefaultCtor {
        NoDefaultCtor(int) {}  // No default constructor
    };
    
    // requires_default_constructible<NoDefaultCtor>();  // ERROR at instantiation
    
    // ============ 9. Linker Errors ============
    std::cout << "\n=== 9. Linker Errors ===" << std::endl;
    
    // Header:
    // template<typename T> void declared_but_not_defined();
    
    // Source that uses it:
    // declared_but_not_defined<int>();  // LINKER ERROR: undefined reference
    
    std::cout << "Template must be defined in every TU that uses it" << std::endl;
    std::cout << "(or use explicit instantiation)" << std::endl;
    
    // ============ 10. SFINAE vs Hard Errors ============
    std::cout << "\n=== 10. SFINAE vs Hard Errors ===" << std::endl;
    
    // SFINAE: Substitution Failure Is Not An Error
    template<typename T>
    auto test_has_plus(T a, T b) -> decltype(a + b, void()) {
        std::cout << "Has operator+" << std::endl;
    }
    
    void test_has_plus(...) {
        std::cout << "No operator+" << std::endl;
    }
    
    class NoPlus {};
    
    test_has_plus(1, 2);      // Calls first version
    test_has_plus(NoPlus{}, NoPlus{});  // Calls second version (SFINAE)
    
    // ============ Debugging Template Errors ============
    std::cout << "\n=== Debugging Tips ===" << std::endl;
    
    std::cout << "1. Simplify: Remove template parameters one by one" << std::endl;
    std::cout << "2. Check typename/template keywords" << std::endl;
    std::cout << "3. Verify dependent names are accessible" << std::endl;
    std::cout << "4. Use static_assert for requirements" << std::endl;
    std::cout << "5. Try explicit template arguments" << std::endl;
    std::cout << "6. Check for ODR violations" << std::endl;
    
    // ============ Common Error Messages ============
    std::cout << "\n=== Common Error Messages ===" << std::endl;
    
    std::cout << "\"no matching function for call to...\"" << std::endl;
    std::cout << "  • Check template argument deduction" << std::endl;
    std::cout << "  • Check function overload resolution" << std::endl;
    
    std::cout << "\"template argument deduction/substitution failed\"" << std::endl;
    std::cout << "  • SFINAE context" << std::endl;
    std::cout << "  • Check constraints on template parameters" << std::endl;
    
    std::cout << "\"invalid use of incomplete type\"" << std::endl;
    std::cout << "  • Forward declared type used in template" << std::endl;
    
    std::cout << "\"undefined reference to...\"" << std::endl;
    std::cout << "  • Template not instantiated or defined" << std::endl;
}

// ============ BONUS: Template Debugging Techniques ============

// Technique 1: static_assert for debugging
template<typename T>
void debug_type() {
    static_assert(sizeof(T) == 0, "Debug: Check T type");
    // Actually: sizeof(T) == 0 is always false
    // But with dependent false: sizeof(T) != sizeof(T)
}

// Technique 2: Type printing
template<typename T>
struct TypePrinter;

// Technique 3: Concept checking (C++20)
#ifdef __cpp_concepts
template<typename T>
concept HasPlus = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

template<HasPlus T>
T safe_add(T a, T b) {
    return a + b;
}
#endif

// Technique 4: Enable_if for debugging
template<typename T>
typename std::enable_if<sizeof(T) == 4>::type
check_size() {
    std::cout << "T is 4 bytes" << std::endl;
}

int main() {
    demonstrate_deduction_guides();
    demonstrate_typename_vs_class();
    demonstrate_template_instantiation();
    demonstrate_template_errors();
    
    return 0;
}


