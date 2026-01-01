////////* POINTERS & REFERENCES *////////

#include <iostream>
#include <memory>
#include <vector>

void demonstrate_pointers_references() {
    std::cout << "============ POINTERS & REFERENCES ============\n" << std::endl;
    
    // ============ RAW POINTERS ============
    std::cout << "=== Raw Pointers ===" << std::endl;
    
    int value = 42;
    int* ptr = &value;  // & gets address
    
    std::cout << "value: " << value << std::endl;
    std::cout << "address of value: " << &value << std::endl;
    std::cout << "ptr: " << ptr << " (stores address)" << std::endl;
    std::cout << "*ptr: " << *ptr << " (dereference - gets value)" << std::endl;
    
    // Modifying through pointer
    *ptr = 100;
    std::cout << "After *ptr = 100, value: " << value << std::endl;
    
    // Null pointer (pre-C++11)
    int* null_ptr1 = 0;
    int* null_ptr2 = NULL;  // C-style (avoid in C++)
    
    // nullptr (C++11) - type-safe null pointer
    int* null_ptr3 = nullptr;
    std::cout << "nullptr: " << null_ptr3 << "\n" << std::endl;
    
    // ============ REFERENCES ============
    std::cout << "=== References ===" << std::endl;
    
    int x = 10;
    int& ref = x;  // Must be initialized, cannot be reassigned
    
    std::cout << "x: " << x << std::endl;
    std::cout << "ref: " << ref << std::endl;
    std::cout << "&x: " << &x << ", &ref: " << &ref 
              << " (same address!)" << std::endl;
    
    ref = 20;  // Modifies x
    std::cout << "After ref = 20, x: " << x << std::endl;
    
    // Reference vs pointer differences:
    // 1. References must be initialized
    // 2. References cannot be null
    // 3. References cannot be reassigned
    // 4. References don't need dereferencing syntax
    // 5. References are safer (no null dereference bugs)
    
    // Reference to const
    const int& const_ref = x;
    // const_ref = 30;  // ERROR: cannot modify through const reference
    
    // ============ POINTER ARITHMETIC ============
    std::cout << "\n=== Pointer Arithmetic ===" << std::endl;
    
    int arr[5] = {10, 20, 30, 40, 50};
    int* arr_ptr = arr;  // Array name decays to pointer to first element
    
    std::cout << "Array: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    
    std::cout << "arr_ptr points to: " << *arr_ptr << std::endl;
    
    // Pointer arithmetic
    arr_ptr++;  // Move to next element (adds sizeof(int) bytes)
    std::cout << "After arr_ptr++, points to: " << *arr_ptr << " (20)" << std::endl;
    
    arr_ptr += 2;  // Move forward 2 elements
    std::cout << "After arr_ptr += 2, points to: " << *arr_ptr << " (40)" << std::endl;
    
    arr_ptr--;  // Move back 1 element
    std::cout << "After arr_ptr--, points to: " << *arr_ptr << " (30)" << std::endl;
    
    // Difference between pointers
    int* ptr1 = &arr[0];
    int* ptr2 = &arr[3];
    ptrdiff_t diff = ptr2 - ptr1;  // Number of elements between
    std::cout << "ptr2 - ptr1 = " << diff << " elements" << std::endl;
    
    // Array indexing using pointer arithmetic
    std::cout << "arr_ptr[1] = " << arr_ptr[1] << " (same as *(arr_ptr + 1))" << std::endl;
    std::cout << "1[arr_ptr] = " << 1[arr_ptr] << " (weird but valid!)\n" << std::endl;
    
    // ============ VOID POINTERS ============
    std::cout << "=== void Pointers ===" << std::endl;
    
    void* void_ptr = &x;  // Can point to any type
    // *void_ptr = 30;  // ERROR: cannot dereference void*
    
    // Must cast back to original type
    int* int_ptr = static_cast<int*>(void_ptr);
    *int_ptr = 30;
    std::cout << "After modifying through void_ptr, x: " << x << std::endl;
    
    // Use cases: generic functions, C compatibility
    // Avoid in modern C++ (use templates instead)
    
    // ============ POINTER TO POINTER ============
    std::cout << "\n=== Pointer to Pointer ===" << std::endl;
    
    int var = 100;
    int* p = &var;
    int** pp = &p;  // Pointer to pointer to int
    
    std::cout << "var: " << var << std::endl;
    std::cout << "*p: " << *p << std::endl;
    std::cout << "**pp: " << **pp << std::endl;
    
    // Modifying through multiple indirection
    **pp = 200;
    std::cout << "After **pp = 200, var: " << var << std::endl;
    
    // Common use: modifying pointer arguments in functions
    auto allocate = [](int** ptr) {
        *ptr = new int(999);  // Allocate and make ptr point to it
    };
    
    int* dynamic_ptr = nullptr;
    allocate(&dynamic_ptr);
    std::cout << "Allocated value: " << *dynamic_ptr << std::endl;
    delete dynamic_ptr;
    
    // ============ CONST WITH POINTERS/REFERENCES ============
    std::cout << "\n=== const with Pointers/References ===" << std::endl;
    
    int y = 10;
    const int* ptr_to_const = &y;     // Pointer to const int
    int* const const_ptr = &y;        // Const pointer to int
    const int* const const_ptr_to_const = &y;  // Const pointer to const int
    
    // ptr_to_const: can change pointer, cannot change data
    ptr_to_const = nullptr;  // OK
    // *ptr_to_const = 20;   // ERROR
    
    // const_ptr: cannot change pointer, can change data
    // const_ptr = nullptr;  // ERROR
    *const_ptr = 20;        // OK
    
    // const_ptr_to_const: cannot change either
    // const_ptr_to_const = nullptr;  // ERROR
    // *const_ptr_to_const = 30;      // ERROR
    
    // Read pointer declarations right-to-left:
    // const int* ptr → ptr is a pointer to const int
    // int const* ptr → same as above
    // int* const ptr → ptr is a const pointer to int
    
    // ============ POINTERS TO FUNCTIONS ============
    std::cout << "\n=== Pointers to Functions ===" << std::endl;
    
    int (*func_ptr)(int, int) = &add;
    std::cout << "Function pointer: " << func_ptr(10, 20) << std::endl;
    
    // Array of function pointers
    int (*operations[])(int, int) = {add, multiply};
    std::cout << "operations[0](5, 6): " << operations[0](5, 6) << std::endl;
    std::cout << "operations[1](5, 6): " << operations[1](5, 6) << "\n" << std::endl;
    
    // ============ COMMON POINTER PITFALLS ============
    std::cout << "=== Common Pointer Pitfalls ===" << std::endl;
    
    // 1. Dangling pointers
    int* dangling = new int(100);
    delete dangling;  // Memory freed
    // *dangling = 200;  // UNDEFINED BEHAVIOR - dangling pointer!
    dangling = nullptr;  // Always set to nullptr after delete
    
    // 2. Memory leaks
    int* leak = new int(100);
    // Forgot to delete - MEMORY LEAK!
    delete leak;  // Good
    
    // 3. Uninitialized pointers
    int* uninitialized;  // Contains garbage address
    // *uninitialized = 10;  // UNDEFINED BEHAVIOR
    
    // 4. Buffer overflows
    int small_array[3] = {1, 2, 3};
    int* overflow = small_array;
    // overflow[10] = 100;  // Buffer overflow - UNDEFINED BEHAVIOR
    
    // 5. Null dereference
    int* null_deref = nullptr;
    // *null_deref = 10;  // CRASH - null pointer dereference
    
    // ============ SMART POINTERS (MODERN C++) ============
    std::cout << "\n=== Smart Pointers (Modern C++) ===" << std::endl;
    
    // std::unique_ptr - exclusive ownership
    std::unique_ptr<int> uptr = std::make_unique<int>(100);
    std::cout << "unique_ptr: " << *uptr << std::endl;
    // Automatically deleted when out of scope
    
    // std::shared_ptr - shared ownership
    std::shared_ptr<int> sptr1 = std::make_shared<int>(200);
    std::shared_ptr<int> sptr2 = sptr1;  // Share ownership
    std::cout << "shared_ptr use_count: " << sptr1.use_count() << std::endl;
    
    // std::weak_ptr - non-owning reference
    std::weak_ptr<int> wptr = sptr1;
    if (auto locked = wptr.lock()) {  // Convert to shared_ptr if still exists
        std::cout << "weak_ptr locked: " << *locked << std::endl;
    }
    
    std::cout << "\nPrefer smart pointers over raw pointers!" << std::endl;
    std::cout << "- unique_ptr: exclusive ownership" << std::endl;
    std::cout << "- shared_ptr: shared ownership" << std::endl;
    std::cout << "- weak_ptr: non-owning observers" << std::endl;
}

// Helper function for pointer demo
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    demonstrate_pointers_references();
    return 0;
}


////////* NULLPTR *////////

#include <iostream>
#include <type_traits>
#include <cstddef>  // For NULL definition

// Function overloads to demonstrate the difference
void foo(int) {
    std::cout << "foo(int) called" << std::endl;
}

void foo(int*) {
    std::cout << "foo(int*) called" << std::endl;
}

void bar(std::nullptr_t) {
    std::cout << "bar(nullptr_t) called" << std::endl;
}

template<typename T>
void process(T* ptr) {
    if (ptr == nullptr) {
        std::cout << "Pointer is null" << std::endl;
    } else {
        std::cout << "Pointer is not null" << std::endl;
    }
}

void demonstrate_nullptr() {
    std::cout << "============ nullptr vs NULL ============\n" << std::endl;
    
    // ============ HISTORICAL BACKGROUND ============
    std::cout << "=== Historical Background ===" << std::endl;
    
    // NULL in C (usually #define NULL 0 or (void*)0)
    // NULL in C++ (usually #define NULL 0)
    
    // Problems with NULL:
    // 1. It's an integer literal 0
    // 2. Can cause function overload ambiguity
    // 3. Not type-safe
    
    // ============ NULL IN C++ ============
    std::cout << "\n=== NULL in C++ ===" << std::endl;
    
    int* ptr1 = NULL;  // Actually assigns 0
    std::cout << "NULL is usually defined as: " << NULL << std::endl;
    
    // NULL is an integer, not a pointer type
    std::cout << "Type of NULL: " << typeid(NULL).name() << std::endl;
    std::cout << "Type of 0: " << typeid(0).name() << std::endl;
    std::cout << "Are they same? " << std::is_same<decltype(NULL), decltype(0)>::value << std::endl;
    
    // Function overload problem with NULL
    foo(0);      // Calls foo(int)
    // foo(NULL); // May be ambiguous or call foo(int) - depends on compiler!
    
    // ============ nullptr (C++11) ============
    std::cout << "\n=== nullptr (C++11) ===" << std::endl;
    
    // nullptr is a keyword and prvalue of type std::nullptr_t
    int* ptr2 = nullptr;
    double* ptr3 = nullptr;
    std::nullptr_t null_value = nullptr;
    
    std::cout << "nullptr is of type: " << typeid(nullptr).name() << std::endl;
    std::cout << "std::nullptr_t is: " << typeid(std::nullptr_t).name() << std::endl;
    
    // nullptr solves the overload problem
    foo(nullptr);  // Unambiguously calls foo(int*)
    
    // Can be used in templates
    process<int>(nullptr);  // T deduced as int
    
    // ============ TYPE SAFETY ============
    std::cout << "\n=== Type Safety ===" << std::endl;
    
    // nullptr is not convertible to integer types
    // int x = nullptr;  // ERROR: cannot convert nullptr to int
    
    // But it is convertible to bool
    if (nullptr) {
        std::cout << "This won't print" << std::endl;
    } else {
        std::cout << "nullptr converts to false in boolean context" << std::endl;
    }
    
    // nullptr is comparable with all pointer types
    if (ptr2 == nullptr) {
        std::cout << "Pointer is null" << std::endl;
    }
    
    // ============ TEMPLATE METAPROGRAMMING ============
    std::cout << "\n=== Template Metaprogramming ===" << std::endl;
    
    // std::nullptr_t is a distinct type
    bar(nullptr);  // Calls bar(nullptr_t)
    
    // Can overload on nullptr_t
    template<typename T>
    void check(T t) {
        if constexpr (std::is_same_v<T, std::nullptr_t>) {
            std::cout << "Got nullptr_t" << std::endl;
        } else if constexpr (std::is_pointer_v<T>) {
            std::cout << "Got pointer type" << std::endl;
        } else {
            std::cout << "Got something else" << std::endl;
        }
    }
    
    check(nullptr);
    check(ptr2);
    check(0);
    
    // ============ PRACTICAL EXAMPLES ============
    std::cout << "\n=== Practical Examples ===" << std::endl;
    
    // 1. Initializing pointers
    int* dynamic_ptr = nullptr;  // Good practice
    // vs
    int* old_style = 0;          // Old style
    int* problematic = NULL;     // Problematic
    
    // 2. Checking for null
    if (dynamic_ptr == nullptr) {  // Clear intent
        dynamic_ptr = new int(42);
    }
    
    // 3. Returning null from functions
    auto find_value = [](const std::vector<int>& vec, int target) -> int* {
        for (auto& val : vec) {
            if (val == target) {
                return &val;
            }
        }
        return nullptr;  // Clear null pointer return
    };
    
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int* found = find_value(numbers, 3);
    if (found != nullptr) {
        std::cout << "Found value: " << *found << std::endl;
    }
    
    // 4. Default arguments
    void allocate_resource(int size, void* hint = nullptr) {
        // hint is optional
    }
    
    // ============ COMPARISON WITH NULL ============
    std::cout << "\n=== Comparison with NULL ===" << std::endl;
    
    int* p1 = nullptr;
    int* p2 = NULL;
    int* p3 = 0;
    
    // All compare equal
    std::cout << "nullptr == NULL: " << (p1 == p2) << std::endl;
    std::cout << "nullptr == 0: " << (p1 == p3) << std::endl;
    
    // But they are different in overload resolution
    std::cout << "\nOverload resolution difference:" << std::endl;
    // foo(NULL);    // Might call foo(int) or be ambiguous
    foo(nullptr);  // Always calls foo(int*)
    
    // ============ ADVANCED USAGE ============
    std::cout << "\n=== Advanced Usage ===" << std::endl;
    
    // nullptr with auto
    auto ptr_auto = nullptr;  // Type is std::nullptr_t
    std::cout << "auto ptr = nullptr; type is: " 
              << typeid(decltype(ptr_auto)).name() << std::endl;
    
    // Use with perfect forwarding
    template<typename T>
    void forward_example(T&& arg) {
        // arg can be nullptr
    }
    
    forward_example(nullptr);
    
    // nullptr in switch (with caution)
    int* choice = nullptr;
    // switch(choice) {  // ERROR: pointer in switch
    //     case nullptr:  // ERROR
    //         break;
    // }
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    std::cout << "1. ALWAYS use nullptr instead of NULL or 0" << std::endl;
    std::cout << "2. Initialize pointers to nullptr" << std::endl;
    std::cout << "3. Check for null with 'if (ptr == nullptr)'" << std::endl;
    std::cout << "4. Return nullptr from functions that can fail" << std::endl;
    std::cout << "5. Use nullptr in templates for type safety" << std::endl;
    std::cout << "6. nullptr works with all pointer types (including member pointers)" << std::endl;
    std::cout << "7. nullptr is a keyword, not a macro" << std::endl;
    
    // ============ C++17: nodiscard with nullptr ============
    std::cout << "\n=== C++17 [[nodiscard]] ===" << std::endl;
    
    [[nodiscard]] int* allocate_memory(int size) {
        return new int[size];
    }
    
    // Compiler warning if return value ignored
    allocate_memory(100);  // Warning: ignoring return value
    
    // But this is OK:
    int* memory = allocate_memory(100);
    delete[] memory;
    
    // nullptr can be returned from [[nodiscard]] functions
    [[nodiscard]] int* find_or_null() {
        return nullptr;  // OK
    }
}

int main() {
    demonstrate_nullptr();
    return 0;
}
