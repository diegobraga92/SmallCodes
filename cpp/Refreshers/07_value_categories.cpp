////////* VALUE CATEGORIES *////////

#include <iostream>
#include <string>
#include <utility>
#include <vector>

// Helper function to demonstrate value categories
void check_value_category(const std::string& name) {
    std::cout << "  Checking: " << name << std::endl;
}

class Resource {
private:
    int* data;
    
public:
    Resource(int value) : data(new int(value)) {
        std::cout << "Resource(" << value << ") constructed" << std::endl;
    }
    
    // Copy constructor
    Resource(const Resource& other) : data(new int(*other.data)) {
        std::cout << "Resource copy constructed" << std::endl;
    }
    
    // Move constructor
    Resource(Resource&& other) noexcept : data(other.data) {
        other.data = nullptr;
        std::cout << "Resource move constructed" << std::endl;
    }
    
    ~Resource() {
        delete data;
        std::cout << "Resource destroyed" << std::endl;
    }
    
    int get() const { return data ? *data : -1; }
};

Resource create_resource() {
    return Resource(42);  // prvalue
}

Resource&& get_rvalue_ref() {
    static Resource r(100);
    return std::move(r);  // xvalue
}

void demonstrate_value_categories() {
    std::cout << "============ VALUE CATEGORIES ============\n" << std::endl;
    
    // ============ HISTORICAL BACKGROUND ============
    std::cout << "=== Historical Background ===" << std::endl;
    std::cout << "C++98: lvalue vs rvalue" << std::endl;
    std::cout << "C++11: Added move semantics, need more categories" << std::endl;
    std::cout << "C++17: Formalized value categories as shown below\n" << std::endl;
    
    // ============ VALUE CATEGORY TAXONOMY ============
    std::cout << "=== Value Category Taxonomy ===" << std::endl;
    std::cout << "        expression" << std::endl;
    std::cout << "        /      \\" << std::endl;
    std::cout << "    glvalue   rvalue" << std::endl;
    std::cout << "    /    \\    /    \\" << std::endl;
    std::cout << "lvalue  xvalue  prvalue\n" << std::endl;
    
    std::cout << "Key:" << std::endl;
    std::cout << "• glvalue: generalized lvalue (has identity)" << std::endl;
    std::cout << "• rvalue: can be moved from" << std::endl;
    std::cout << "• lvalue: has identity, cannot be moved from" << std::endl;
    std::cout << "• xvalue: has identity, can be moved from" << std::endl;
    std::cout << "• prvalue: pure rvalue (no identity)\n" << std::endl;
    
    // ============ LVALUES ============
    std::cout << "=== Lvalues (Left values) ===" << std::endl;
    std::cout << "Properties:" << std::endl;
    std::cout << "1. Has identity (can take address)" << std::endl;
    std::cout << "2. Cannot be moved from" << std::endl;
    std::cout << "3. Usually appears on left side of assignment\n" << std::endl;
    
    std::cout << "Examples:" << std::endl;
    
    // 1. Variable names
    int x = 10;
    std::cout << "1. Variable name: int x = 10;" << std::endl;
    std::cout << "   &x = " << &x << " (has address)" << std::endl;
    
    // 2. String literals (special case)
    const char* str = "hello";
    std::cout << "2. String literal: \"hello\"" << std::endl;
    std::cout << "   &\"hello\"[0] = " << (void*)&"hello"[0] << std::endl;
    
    // 3. Function returning lvalue reference
    auto get_ref = [](int& val) -> int& { return val; };
    int& ref = get_ref(x);  // lvalue
    std::cout << "3. Function returning lvalue reference" << std::endl;
    
    // 4. Array subscript
    int arr[3] = {1, 2, 3};
    arr[0] = 10;  // arr[0] is lvalue
    std::cout << "4. Array subscript: arr[0]" << std::endl;
    
    // 5. Dereferenced pointer
    int* ptr = &x;
    *ptr = 20;  // *ptr is lvalue
    std::cout << "5. Dereferenced pointer: *ptr" << std::endl;
    
    // 6. Pre-increment/decrement
    ++x;  // ++x is lvalue
    std::cout << "6. Pre-increment: ++x" << std::endl;
    
    // 7. Member access of lvalue
    struct Point { int x, y; };
    Point p{1, 2};
    p.x = 3;  // p.x is lvalue
    std::cout << "7. Member of lvalue: p.x" << std::endl;
    
    // ============ PRVALUES ============
    std::cout << "\n=== Prvalues (Pure rvalues) ===" << std::endl;
    std::cout << "Properties:" << std::endl;
    std::cout << "1. No identity (no address)" << std::endl;
    std::cout << "2. Can be moved from" << std::endl;
    std::cout << "3. Usually temporary objects\n" << std::endl;
    
    std::cout << "Examples:" << std::endl;
    
    // 1. Literals (except string)
    std::cout << "1. Literals: 42, 3.14, 'a', true" << std::endl;
    
    // 2. Function returning non-reference
    auto get_value = []() -> int { return 42; };
    int val = get_value();  // get_value() is prvalue
    std::cout << "2. Function returning by value" << std::endl;
    
    // 3. Arithmetic expressions
    int result = x + 5;  // x + 5 is prvalue
    std::cout << "3. Arithmetic expression: x + 5" << std::endl;
    
    // 4. Constructor calls
    Resource r1 = Resource(10);  // Resource(10) is prvalue
    std::cout << "4. Constructor call: Resource(10)" << std::endl;
    
    // 5. Lambda expressions
    auto lambda = [](){ return 42; };  // Lambda is prvalue
    std::cout << "5. Lambda expression" << std::endl;
    
    // 6. this pointer
    // this is prvalue (pointer, not the object)
    
    // ============ XVALUES ============
    std::cout << "\n=== Xvalues (eXpiring values) ===" << std::endl;
    std::cout << "Properties:" << std::endl;
    std::cout << "1. Has identity" << std::endl;
    std::cout << "2. Can be moved from" << std::endl;
    std::cout << "3. About to expire (can be reused)\n" << std::endl;
    
    std::cout << "Examples:" << std::endl;
    
    // 1. Function returning rvalue reference
    Resource&& rref = get_rvalue_ref();  // xvalue
    std::cout << "1. Function returning rvalue reference" << std::endl;
    
    // 2. std::move result
    Resource r2(20);
    Resource r3 = std::move(r2);  // std::move(r2) is xvalue
    std::cout << "2. std::move result" << std::endl;
    
    // 3. Cast to rvalue reference
    Resource r4(30);
    Resource r5 = static_cast<Resource&&>(r4);  // xvalue
    std::cout << "3. Cast to rvalue reference" << std::endl;
    
    // 4. Member of xvalue
    struct Wrapper { Resource r; };
    Wrapper w{Resource(40)};
    Resource r6 = std::move(w).r;  // std::move(w).r is xvalue
    std::cout << "4. Member of xvalue" << std::endl;
    
    // ============ PRACTICAL IMPLICATIONS ============
    std::cout << "\n=== Practical Implications ===" << std::endl;
    
    // 1. Overload resolution
    void process(int&);    // #1: takes lvalue
    void process(int&&);   // #2: takes rvalue
    
    int num = 42;
    process(num);   // Calls #1 (lvalue)
    process(42);    // Calls #2 (prvalue)
    process(std::move(num));  // Calls #2 (xvalue)
    
    // 2. Move semantics
    std::vector<Resource> resources;
    resources.push_back(Resource(50));  // Move from prvalue
    resources.push_back(std::move(r1)); // Move from xvalue
    
    // 3. Copy elision and RVO
    Resource r7 = create_resource();  // May construct directly (no copy/move)
    
    // ============ TESTING VALUE CATEGORIES ============
    std::cout << "\n=== Testing Value Categories ===" << std::endl;
    
    // decltype tells us the type AND value category
    int i = 10;
    
    // decltype(variable) gives declared type (lvalue)
    decltype(i) a = 20;  // int (lvalue)
    
    // decltype((variable)) gives type of expression (lvalue reference for lvalues)
    decltype((i)) b = i;  // int& (because (i) is lvalue expression)
    
    // decltype(literal) gives type (prvalue)
    decltype(42) c = 30;  // int (prvalue)
    
    std::cout << "decltype(i): " << typeid(decltype(i)).name() << " (lvalue)" << std::endl;
    std::cout << "decltype((i)): " << typeid(decltype((i))).name() << " (lvalue reference)" << std::endl;
    std::cout << "decltype(42): " << typeid(decltype(42)).name() << " (prvalue)" << std::endl;
    
    // ============ C++17 GUARANTEED COPY ELISION ============
    std::cout << "\n=== C++17 Guaranteed Copy Elision ===" << std::endl;
    
    // Before C++17: Might create temporary then copy/move
    // C++17: Direct construction (mandatory elision)
    Resource r8 = Resource(60);  // Constructs directly, no copy/move
    
    // Even with prvalues as function arguments
    auto consume = [](Resource res) {
        return res.get();
    };
    
    int result2 = consume(Resource(70));  // Constructs directly in parameter
    
    // ============ MATERIALIZATION ============
    std::cout << "\n=== Materialization (C++17) ===" << std::endl;
    std::cout << "prvalue → xvalue conversion when needed" << std::endl;
    std::cout << "Happens when prvalue needs to have identity:" << std::endl;
    std::cout << "1. Binding to reference" << std::endl;
    std::cout << "2. Taking address" << std::endl;
    std::cout << "3. Accessing member" << std::endl;
    
    const Resource& cref = Resource(80);  // Materialization happens here
    // Temporary materialized to xvalue, bound to reference
    
    // ============ COMMON PITFALLS ============
    std::cout << "\n=== Common Pitfalls ===" << std::endl;
    
    // 1. Returning local variable by reference
    /*
    int& bad_return() {
        int local = 42;
        return local;  // Dangling reference!
    }
    */
    
    // 2. Misunderstanding std::move
    std::string str = "hello";
    std::string moved = std::move(str);
    // str is now valid but unspecified state (not necessarily empty)
    
    // 3. Moving from const objects
    const Resource cr(90);
    // Resource r = std::move(cr);  // ERROR: cannot move from const
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Understand value categories for move semantics" << std::endl;
    std::cout << "2. Use std::move to convert lvalues to xvalues" << std::endl;
    std::cout << "3. Return by value (prvalue) for factory functions" << std::endl;
    std::cout << "4. Use const& for read-only parameters" << std::endl;
    std::cout << "5. Use && for sink parameters (taking ownership)" << std::endl;
    std::cout << "6. Leverage copy elision (don't overuse std::move)" << std::endl;
}

int main() {
    demonstrate_value_categories();
    return 0;
}