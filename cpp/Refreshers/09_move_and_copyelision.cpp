#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <tuple>
#include <memory>
#include <coroutine>  // C++20
#include <compare>    // C++20

// ============ 1. MOVE SEMANTICS ============

class Resource {
    std::string name;
    int* data;
    size_t size;
    
public:
    // Constructor
    Resource(const std::string& n, size_t sz) 
        : name(n), size(sz), data(new int[sz]) {
        std::cout << "Resource '" << name << "' constructed" << std::endl;
    }
    
    // Copy constructor (deep copy)
    Resource(const Resource& other) 
        : name(other.name + " (copy)"), size(other.size), data(new int[other.size]) {
        std::copy(other.data, other.data + other.size, data);
        std::cout << "Resource '" << name << "' copy constructed" << std::endl;
    }
    
    // Copy assignment
    Resource& operator=(const Resource& other) {
        if (this != &other) {
            delete[] data;
            name = other.name + " (copy assigned)";
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
            std::cout << "Resource '" << name << "' copy assigned" << std::endl;
        }
        return *this;
    }
    
    // Move constructor (C++11) - steals resources
    Resource(Resource&& other) noexcept
        : name(std::move(other.name)), size(other.size), data(other.data) {
        other.data = nullptr;
        other.size = 0;
        std::cout << "Resource '" << name << "' move constructed" << std::endl;
    }
    
    // Move assignment
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            delete[] data;
            name = std::move(other.name);
            size = other.size;
            data = other.data;
            other.data = nullptr;
            other.size = 0;
            std::cout << "Resource '" << name << "' move assigned" << std::endl;
        }
        return *this;
    }
    
    // Destructor
    ~Resource() {
        delete[] data;
        std::cout << "Resource '" << name << "' destroyed" << std::endl;
    }
    
    void print() const {
        std::cout << "Resource '" << name << "' size: " << size << std::endl;
    }
};

void demonstrate_move_semantics() {
    std::cout << "============ MOVE SEMANTICS ============\n" << std::endl;
    
    // ============ Rvalue References ============
    std::cout << "=== Rvalue References (&&) ===" << std::endl;
    
    int x = 10;
    int& lref = x;      // lvalue reference
    // int&& rref = x;  // ERROR: cannot bind rvalue ref to lvalue
    int&& rref = 20;    // OK: 20 is rvalue (temporary)
    int&& rref2 = std::move(x);  // OK: std::move converts lvalue to rvalue
    
    std::cout << "x = " << x << std::endl;
    std::cout << "lref = " << lref << std::endl;
    std::cout << "rref = " << rref << std::endl;
    std::cout << "rref2 = " << rref2 << std::endl;
    
    // ============ std::move ============
    std::cout << "\n=== std::move ===" << std::endl;
    std::cout << "Converts lvalue to rvalue reference (allows moving)" << std::endl;
    
    Resource res1("Resource1", 100);
    Resource res2("Resource2", 200);
    
    std::cout << "\nBefore move:" << std::endl;
    res1.print();
    res2.print();
    
    // Move construction
    Resource res3 = std::move(res1);  // Calls move constructor
    
    std::cout << "\nAfter move construction:" << std::endl;
    res1.print();  // res1 is now empty (moved-from state)
    res3.print();  // res3 now owns res1's resources
    
    // Move assignment
    res2 = std::move(res3);  // Calls move assignment
    
    std::cout << "\nAfter move assignment:" << std::endl;
    res2.print();  // res2 now owns the resources
    res3.print();  // res3 is now empty
    
    // ============ When Move Happens Automatically ============
    std::cout << "\n=== Automatic Moves ===" << std::endl;
    
    // Returning local variable
    auto create_resource = []() -> Resource {
        Resource temp("Temporary", 50);
        return temp;  // May be moved or copy-elided
    };
    
    Resource res4 = create_resource();  // Move or copy elision
    
    // Temporary objects are rvalues
    std::vector<Resource> resources;
    resources.push_back(Resource("Temp", 10));  // Move constructor called
    
    // ============ Rule of Five ============
    std::cout << "\n=== Rule of Five ===" << std::endl;
    std::cout << "If you define any of:" << std::endl;
    std::cout << "1. Destructor" << std::endl;
    std::cout << "2. Copy constructor" << std::endl;
    std::cout << "3. Copy assignment" << std::endl;
    std::cout << "4. Move constructor" << std::endl;
    std::cout << "5. Move assignment" << std::endl;
    std::cout << "You should probably define all five.\n" << std::endl;
    
    // ============ noexcept for Moves ============
    std::cout << "=== noexcept Moves ===" << std::endl;
    std::cout << "Move operations should be marked noexcept when possible" << std::endl;
    std::cout << "Standard library containers use noexcept moves for optimization\n" << std::endl;
}

// ============ 2. PERFECT FORWARDING ============

// Universal/forwarding reference: T&& where T is template parameter
template<typename T>
void forward_example(T&& arg) {
    // arg is forwarding reference (can bind to lvalue or rvalue)
    process(std::forward<T>(arg));  // Preserves value category
}

void process(int& x) {
    std::cout << "process(int&): lvalue " << x << std::endl;
}

void process(int&& x) {
    std::cout << "process(int&&): rvalue " << x << std::endl;
}

void demonstrate_perfect_forwarding() {
    std::cout << "============ PERFECT FORWARDING ============\n" << std::endl;
    
    // ============ Universal References ============
    std::cout << "=== Universal/Forwarding References ===" << std::endl;
    std::cout << "T&& in template context where T is deduced\n" << std::endl;
    
    int x = 42;
    const int y = 100;
    
    // Template function with forwarding reference
    auto log_value = [](auto&& val) {
        std::cout << "Value: " << val << std::endl;
        // val is forwarding reference
    };
    
    log_value(x);      // lvalue - T = int&
    log_value(123);    // rvalue - T = int
    log_value(y);      // const lvalue - T = const int&
    
    // ============ std::forward ============
    std::cout << "\n=== std::forward ===" << std::endl;
    std::cout << "Preserves value category (lvalue/rvalue) when forwarding\n" << std::endl;
    
    std::cout << "Calling forward_example:" << std::endl;
    forward_example(x);      // Calls process(int&)
    forward_example(123);    // Calls process(int&&)
    
    // ============ Perfect Forwarding in Practice ============
    std::cout << "\n=== Perfect Forwarding in Practice ===" << std::endl;
    
    // emplace_back uses perfect forwarding
    std::vector<Resource> resources;
    
    // Construct Resource in-place with arguments
    resources.emplace_back("Emplaced", 500);  // No copy or move!
    
    // ============ Variadic Templates with Perfect Forwarding ============
    std::cout << "\n=== Variadic Perfect Forwarding ===" << std::endl;
    
    template<typename... Args>
    auto make_resource(Args&&... args) {
        return Resource(std::forward<Args>(args)...);
    }
    
    auto res = make_resource("Perfect", 1000);
    
    // ============ Reference Collapsing ============
    std::cout << "\n=== Reference Collapsing Rules ===" << std::endl;
    std::cout << "T& &  → T&" << std::endl;
    std::cout << "T& && → T&" << std::endl;
    std::cout << "T&& & → T&" << std::endl;
    std::cout << "T&& && → T&&\n" << std::endl;
}

// ============ COPY ELISION & RVO ============

struct BigObject {
    std::vector<int> data;
    
    BigObject() {
        std::cout << "Default constructor" << std::endl;
    }
    
    BigObject(const BigObject& other) {
        std::cout << "Copy constructor" << std::endl;
        data = other.data;
    }
    
    BigObject(BigObject&& other) noexcept {
        std::cout << "Move constructor" << std::endl;
        data = std::move(other.data);
    }
};

BigObject create_object() {
    BigObject obj;
    obj.data.resize(1000);
    return obj;  // May use RVO/NRVO
}

BigObject create_object_conditional(bool flag) {
    BigObject obj1, obj2;
    obj1.data.resize(100);
    obj2.data.resize(200);
    
    if (flag) {
        return obj1;  // NRVO may not apply
    } else {
        return obj2;  // Two return paths
    }
}

void demonstrate_copy_elision() {
    std::cout << "============ COPY ELISION & RVO ============\n" << std::endl;
    
    // ============ Return Value Optimization (RVO) ============
    std::cout << "=== Return Value Optimization (RVO) ===" << std::endl;
    std::cout << "Elides copy when returning temporary\n" << std::endl;
    
    std::cout << "Creating object with RVO:" << std::endl;
    BigObject obj1 = create_object();  // No copy/move - constructed directly
    
    // ============ Named Return Value Optimization (NRVO) ============
    std::cout << "\n=== Named RVO (NRVO) ===" << std::endl;
    std::cout << "Elides copy when returning named local variable\n" << std::endl;
    
    std::cout << "Creating object with possible NRVO:" << std::endl;
    auto obj2 = create_object_conditional(true);  // May or may not elide
    
    // ============ Guaranteed Copy Elision (C++17) ============
    std::cout << "\n=== Guaranteed Copy Elision (C++17) ===" << std::endl;
    std::cout << "Copy elision is mandatory in some cases\n" << std::endl;
    
    // C++17 guarantees no copy/move here:
    BigObject obj3 = BigObject();  // Direct initialization
    
    // Also for prvalues in function arguments
    auto consume = [](BigObject obj) {
        return obj;
    };
    
    std::cout << "\nPassing prvalue to function:" << std::endl;
    auto obj4 = consume(BigObject());  // Direct construction in parameter
    
    // ============ When Elision Happens ============
    std::cout << "\n=== When Copy Elision Happens ===" << std::endl;
    
    std::cout << "1. Returning temporary object (RVO)" << std::endl;
    std::cout << "2. Returning named local variable (NRVO)" << std::endl;
    std::cout << "3. Throwing and catching by value" << std::endl;
    std::cout << "4. Initialization with temporary (C++17 mandatory)" << std::endl;
    
    // ============ Best Practices ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. Don't write return std::move(local_var)" << std::endl;
    std::cout << "   • Interferes with RVO/NRVO" << std::endl;
    std::cout << "   • Forces move even when copy could be elided" << std::endl;
    
    std::cout << "\n2. Write factory functions that return by value" << std::endl;
    std::cout << "   • Let compiler optimize" << std::endl;
    std::cout << "   • Simpler interface" << std::endl;
    
    std::cout << "\n3. Trust the compiler for C++17 and later" << std::endl;
    std::cout << "   • Copy elision is guaranteed in many cases" << std::endl;
    
    // ============ Example: Bad Pattern ============
    std::cout << "\n=== Bad Pattern (Avoid This) ===" << std::endl;
    
    /*
    BigObject bad_factory() {
        BigObject obj;
        // ... setup ...
        return std::move(obj);  // BAD! Prevents RVO
    }
    */
    
    // ============ Example: Good Pattern ============
    std::cout << "\n=== Good Pattern ===" << std::endl;
    
    /*
    BigObject good_factory() {
        BigObject obj;
        // ... setup ...
        return obj;  // GOOD! Allows RVO/NRVO
    }
    */
}

int main() {
    demonstrate_move_semantics();
    demonstrate_perfect_forwarding();
    demonstrate_copy_elision();
    
    return 0;
}