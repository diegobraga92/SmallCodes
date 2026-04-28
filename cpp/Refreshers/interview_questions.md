# C++ Technical Interview Questions

> A comprehensive list of conversational technical interview questions covering modern C++ (C++11 through C++20) from junior to senior level. Based on the C++ refresher series covering 35 topics.

---

## 🟢 JUNIOR LEVEL — Fundamentals

### Basic Types & Variables

1. **What are the fundamental C++ data types and their typical sizes?**

   *Key points: char (1 byte), int (4 bytes), float (4 bytes), double (8 bytes), bool (1 byte). Sizes are platform-dependent but char is always 1 byte by definition.*

2. **What is the difference between `signed` and `unsigned` integers? What happens when you overflow each?**

   *Key points: Signed overflow is undefined behavior; unsigned overflow wraps around modulo 2^n. Signed can represent negative values; unsigned cannot.*

3. **What is the difference between `const`, `constexpr`, and `consteval`?**

   *Key points: const = runtime or compile-time constant; constexpr = compile-time constant (C++11, relaxed in C++14/17/20); consteval = must be evaluated at compile-time (C++20).*

4. **What is the difference between `enum` and `enum class`?**

   *Key points: enum class is strongly typed (no implicit int conversion), scoped (must use EnumName::Value), and can specify underlying type. Old enum pollutes surrounding namespace and implicitly converts to int.*

5. **What is the difference between `int`, `int32_t`, and `size_t`?**

   *Key points: int is platform-dependent (usually 4 bytes); int32_t is exactly 32 bits; size_t is unsigned and platform-dependent (result of sizeof).*

### Conditionals & Loops

6. **What is the difference between `break` and `continue` in loops?**

   *Key points: break exits the loop entirely; continue skips to the next iteration.*

7. **What is the ternary operator and when should you use it?**

   *Key points: `condition ? expr1 : expr2` — use for simple conditional assignments; avoid nesting for readability.*

8. **What is the difference between a `while` loop and a `do-while` loop?**

   *Key points: while checks condition before executing; do-while executes at least once before checking.*

9. **What is a range-based for loop and how does it work internally?**

   *Key points: `for (auto& elem : container)` — internally uses begin()/end() iterators. Available since C++11.*

10. **When would you use `goto` in modern C++?**

    *Key points: Rarely. Only acceptable for breaking out of deeply nested loops or in generated code. Prefer structured control flow, RAII, and exceptions.*

### Storage Classes & Operators

11. **What is the difference between stack and heap allocation?**

    *Key points: Stack is automatic (fast, limited size, LIFO); heap is manual (slower, larger, flexible lifetime). Prefer stack for small, short-lived objects.*

12. **What is the difference between `static` local, `static` global, and `static` class members?**

    *Key points: static local persists across function calls (initialized once); static global has internal linkage (file scope); static class member is shared across all instances.*

13. **What is `thread_local` storage?**

    *Key points: Each thread gets its own copy of the variable. Useful for thread-specific state without synchronization.*

14. **Explain operator precedence. What is the result of `2 + 3 * 4`?**

    *Key points: Multiplication before addition: 2 + 12 = 14. When in doubt, use parentheses.*

15. **What is short-circuit evaluation?**

    *Key points: In `a && b`, if `a` is false, `b` is not evaluated. In `a || b`, if `a` is true, `b` is not evaluated. Prevents unnecessary computation and enables safe null checks.*

### Functions

16. **What is the difference between pass-by-value, pass-by-reference, and pass-by-const-reference?**

    *Key points: By-value copies the parameter; by-reference can modify the original; by-const-reference is read-only and avoids copying. Use const-ref for large objects, by-value for small types.*

17. **What is function overloading and how does overload resolution work?**

    *Key points: Multiple functions with same name but different parameters. Resolution: exact match → promotion → standard conversion → user-defined conversion.*

18. **What are default arguments and what are the rules for using them?**

    *Key points: Parameters with default values must be trailing. Can't skip arguments in the middle. Declared in declaration (header), not definition.*

19. **What is an inline function? When does the compiler actually inline?**

    *Key points: Suggestion to compiler to insert code at call site. Compiler may ignore for large/recursive functions. Modern compilers auto-inline based on optimization settings.*

20. **What is a lambda expression? Explain capture clauses.**

    *Key points: Anonymous function object. `[capture](params) -> return_type { body }`. Captures: `[=]` by value, `[&]` by reference, `[x, &y]` specific, `[this]` capture this pointer.*

### Pointers & References

21. **What is the difference between a pointer and a reference?**

    *Key points: References must be initialized, cannot be null, cannot be reassigned, don't need dereferencing syntax. Pointers can be null, can be reassigned, need `*` to dereference.*

22. **What is a null pointer and how should you represent it in modern C++?**

    *Key points: Use `nullptr` (C++11) instead of `NULL` or `0`. nullptr is type-safe (std::nullptr_t) and doesn't cause overload ambiguity.*

23. **Explain the difference between `const int*`, `int* const`, and `const int* const`.**

    *Key points: `const int*` = pointer to const int (can't modify data); `int* const` = const pointer to int (can't change pointer); `const int* const` = const pointer to const int (neither can change).*

24. **What is pointer arithmetic? Give an example.**

    *Key points: Adding N to a pointer advances by N * sizeof(element). `arr + 5` points to the 6th element. Only valid within array bounds.*

25. **What is a dangling pointer and how do you avoid it?**

    *Key points: Pointer to freed memory. Avoid by setting to nullptr after delete, using smart pointers, and ensuring proper object lifetimes.*

### Compilation Model

26. **What are the stages of C++ compilation?**

    *Key points: 1) Preprocessing (#include, #define expansion), 2) Compilation (syntax analysis, code generation → .o/.obj), 3) Linking (combine object files, resolve symbols → executable).*

27. **What is a translation unit?**

    *Key points: A source file (.cpp) after preprocessing (all #includes expanded). Each TU is compiled independently into an object file.*

28. **What is the One Definition Rule (ODR)?**

    *Key points: Each non-inline function/variable must have exactly one definition in the entire program. Multiple declarations are allowed. Violations cause linker errors.*

29. **What is the difference between a declaration and a definition?**

    *Key points: Declaration introduces a name (no memory allocated); definition provides the implementation (memory allocated). `extern int x;` vs `int x = 42;`.*

30. **What is the difference between `#include <header>` and `#include "header"`?**

    *Key points: Angle brackets search system include paths; quotes search current directory first, then system paths.*

### Namespaces

31. **What is a namespace and why is it useful?**

    *Key points: Prevents name collisions. Groups related declarations. Can be nested. Can have aliases (`namespace ns = long::name;`).*

32. **What is the difference between a `using` declaration and a `using` directive?**

    *Key points: `using std::cout;` brings one name into scope; `using namespace std;` brings entire namespace. Never put `using namespace` in headers.*

33. **What is an anonymous namespace?**

    *Key points: `namespace { ... }` gives internal linkage to its contents (equivalent to static). Used for file-local declarations.*

### Value Categories

34. **What are the C++ value categories? Explain lvalues, prvalues, and xvalues.**

    *Key points: lvalue = has identity, can't be moved from; prvalue = no identity, can be moved from (temporaries, literals); xvalue = has identity, can be moved from (std::move result).*

35. **What is `std::move` and what does it actually do?**

    *Key points: `std::move(x)` casts x to an rvalue reference. It doesn't move anything — it enables move semantics by making the value eligible for moving.*

36. **What is copy elision and when is it guaranteed (C++17)?**

    *Key points: Compiler optimization that eliminates copy/move constructors. C++17 guarantees elision when returning a prvalue or initializing from a prvalue.*

### Containers

37. **Compare `std::vector`, `std::list`, and `std::deque` in terms of performance.**

    *Key points: vector: O(1) random access, O(n) insert/remove middle; list: O(n) access, O(1) insert/remove anywhere; deque: O(1) access, O(1) push/pop at both ends.*

38. **When would you use `std::map` vs `std::unordered_map`?**

    *Key points: map: ordered, O(log n), needs operator<; unordered_map: unordered, O(1) average, needs std::hash. Use map when ordering matters or stable performance needed.*

39. **What is a `std::set` and how is it different from `std::vector`?**

    *Key points: set stores unique, sorted elements. No duplicates. O(log n) insert/find. Vector allows duplicates, unsorted, O(n) find.*

40. **What is the difference between `std::array` and C-style arrays?**

    *Key points: std::array has STL interface (size(), begin(), end()), doesn't decay to pointer, supports algorithms, bounds-checked at() method.*

41. **What is `std::string_view` and when should you use it?**

    *Key points: Non-owning view of a string (pointer + size). No allocation. Use for read-only string parameters. Must ensure viewed string outlives the view.*

### Iterators & Algorithms

42. **What are the iterator categories in C++?**

    *Key points: Input (read once), Output (write once), Forward (read/write forward), Bidirectional (forward + backward), Random Access (jump to any position), Contiguous (C++20, adjacent memory).*

43. **What is the difference between `std::find` and `std::binary_search`?**

    *Key points: find is O(n) linear search; binary_search is O(log n) but requires sorted range.*

44. **What is `std::sort` and what algorithm does it use?**

    *Key points: Introsort (quicksort + heapsort + insertion sort). O(n log n) average. Requires random access iterators.*

45. **What is the difference between `std::sort` and `std::stable_sort`?**

    *Key points: stable_sort preserves relative order of equal elements. Uses mergesort. May be slower but guarantees stability.*

---

## 🟡 MID-LEVEL — Intermediate

### Move Semantics & Perfect Forwarding

46. **Explain the Rule of Five. When must you implement it?**

    *Key points: If you define any of: destructor, copy constructor, copy assignment, move constructor, move assignment — you should probably define all five. Applies when class manages a resource.*

47. **What is perfect forwarding and how does `std::forward` work?**

    *Key points: Preserves value category (lvalue/rvalue) when forwarding arguments through template functions. Uses reference collapsing rules: T&& + lvalue = T&, T&& + rvalue = T&&.*

48. **What is a forwarding reference (universal reference)?**

    *Key points: `T&&` where T is a deduced template parameter. Can bind to both lvalues and rvalues. Not the same as rvalue reference `int&&`.*

49. **What is the copy-and-swap idiom?**

    *Key points: Implement copy assignment by taking parameter by value (copy), then swapping with `*this`. Provides strong exception guarantee and handles self-assignment.*

### Modern C++ (C++11/14/17/20)

50. **What is `auto` and when should you use it?**

    *Key points: Type deduction from initializer. Use when type is obvious from context (iterators, lambdas, complex types). Don't use when type is important for readability.*

51. **What is `decltype` and how is it different from `auto`?**

    *Key points: decltype deduces the exact type of an expression (including references). auto strips references and const. `decltype(auto)` preserves exact type.*

52. **What are structured bindings (C++17)?**

    *Key points: `auto [a, b, c] = tuple;` — decomposes tuples, pairs, arrays, and structs into named variables. Works with maps: `for (const auto& [key, value] : map)`.*

53. **What is `std::optional` and when would you use it?**

    *Key points: Represents a value that may or may not be present. Use for optional return values instead of sentinel values or out-parameters.*

54. **What is `std::variant` and how is it different from a union?**

    *Key points: Type-safe union. Stores one of several types. Access with std::visit or std::get_if. No undefined behavior from reading wrong member.*

55. **What is `std::any`?**

    *Key points: Type-safe container for single values of any type. Uses type erasure. Access with std::any_cast. Has runtime overhead.*

56. **What are the C++17 parallel algorithms?**

    *Key points: Execution policies: `std::execution::seq` (sequential), `std::execution::par` (parallel), `std::execution::par_unseq` (parallel + vectorized). Apply to most STL algorithms.*

57. **What is `std::span` (C++20)?**

    *Key points: Non-owning view over contiguous sequence. Like string_view but for any type. Zero overhead. Bounds information always available.*

58. **What are C++20 coroutines? Explain `co_await`, `co_yield`, `co_return`.**

    *Key points: Functions that can be suspended and resumed. co_await suspends until operation completes; co_yield yields a value; co_return completes the coroutine.*

59. **What is the spaceship operator `<=>` (C++20)?**

    *Key points: Three-way comparison. Returns std::strong_ordering, std::weak_ordering, or std::partial_ordering. `auto operator<=>(const T&) const = default;` generates all comparison operators.*

### Templates

60. **What is the difference between a function template and a template function?**

    *Key points: Function template is the pattern; template function is the instantiation. The template generates functions when instantiated with specific types.*

61. **What is template specialization? When would you use it?**

    *Key points: Provide a different implementation for a specific type. Full specialization: `template<> class MyClass<int> {}`. Partial specialization: `template<typename T> class MyClass<T*> {}`.*

62. **What are variadic templates?**

    *Key points: Templates that accept a variable number of arguments. `template<typename... Args>`. Use with fold expressions (C++17) for concise operations.*

63. **What is SFINAE?**

    *Key points: Substitution Failure Is Not An Error. When template substitution fails, the compiler doesn't error — it just removes that overload from consideration. Used with std::enable_if.*

64. **What are concepts (C++20)?**

    *Key points: Named constraints on template parameters. `template<Integral T>`. Better than SFINAE: clearer syntax, better error messages, composable.*

### Smart Pointers

65. **Compare `std::unique_ptr`, `std::shared_ptr`, and `std::weak_ptr`.**

    *Key points: unique_ptr: exclusive ownership, zero overhead; shared_ptr: shared ownership, atomic reference counting; weak_ptr: non-owning observer, breaks cycles.*

66. **When would you use `std::make_unique` vs `new`?**

    *Key points: Always prefer make_unique. Exception-safe (no gap between allocation and ownership), avoids explicit new, more concise.*

67. **What is the `std::enable_shared_from_this` pattern?**

    *Key points: Allows a class to safely create shared_ptr to itself (shared_from_this()). Requires class to inherit from enable_shared_from_this and be owned by a shared_ptr.*

68. **What is a custom deleter and when would you need one?**

    *Key points: Custom cleanup logic when smart pointer destroys object. Examples: closing files, freeing C resources, returning objects to a pool.*

### Threading & Concurrency

69. **What is the difference between `std::thread` and `std::jthread` (C++20)?**

    *Key points: jthread automatically joins on destruction (RAII). Supports cooperative cancellation via std::stop_token. No need to manually call join().*

70. **What is a data race and how do you prevent it?**

    *Key points: Two threads accessing same memory, at least one write, no synchronization. Prevent with mutexes, atomics, or thread-local storage.*

71. **What is the difference between `std::mutex`, `std::recursive_mutex`, and `std::shared_mutex`?**

    *Key points: mutex: standard, non-recursive; recursive_mutex: same thread can lock multiple times; shared_mutex: multiple readers or one writer.*

72. **What is `std::lock_guard` vs `std::unique_lock` vs `std::scoped_lock`?**

    *Key points: lock_guard: simple RAII, can't unlock early; unique_lock: flexible, can unlock/lock, supports deferred locking; scoped_lock (C++17): locks multiple mutexes atomically.*

73. **What is a condition variable and how do you use it?**

    *Key points: Allows threads to wait for a condition. Used with unique_lock and a predicate to handle spurious wakeups. `cv.wait(lock, predicate)`.*

74. **What is the difference between `std::async` with `std::launch::async` vs `std::launch::deferred`?**

    *Key points: async runs in a new thread immediately; deferred runs lazily when get() is called (in the calling thread). Default policy may choose either.*

75. **What is a thread pool and why would you use one?**

    *Key points: Fixed set of worker threads + task queue. Avoids thread creation overhead. Better for many short-lived tasks. Work stealing improves load balancing.*

### Async & Futures

76. **What is the difference between `std::future` and `std::shared_future`?**

    *Key points: future: move-only, get() can only be called once; shared_future: copyable, get() can be called multiple times by multiple threads.*

77. **What is `std::promise` and how does it relate to `std::future`?**

    *Key points: Promise/future pair for thread communication. Producer sets value on promise; consumer gets value from future. One-shot channel.*

78. **What is `std::packaged_task`?**

    *Key points: Wraps a callable to produce a future. Can be passed to a thread or invoked directly. Useful for creating tasks that produce results.*

### Classes & OOP

79. **What is the difference between a class and a struct in C++?**

    *Key points: Only difference: class members are private by default; struct members are public by default. Convention: struct for POD data, class for objects with invariants.*

80. **What is the `this` pointer?**

    *Key points: Pointer to the current object instance. Available in non-static member functions. Used to disambiguate member variables from parameters, or for method chaining.*

81. **What is the difference between public, protected, and private inheritance?**

    *Key points: Public: is-a relationship (most common); Protected: public members become protected in derived; Private: implementation inheritance (base becomes private).*

82. **What is a virtual function and how does it work internally?**

    *Key points: Function that can be overridden in derived classes. Uses vtable (virtual table) and vptr (virtual pointer). Runtime dispatch based on actual object type.*

83. **What is a pure virtual function and an abstract class?**

    *Key points: `virtual void func() = 0;` — no implementation in base class. Class with at least one pure virtual function is abstract and cannot be instantiated.*

84. **What is the difference between early binding and late binding?**

    *Key points: Early binding (compile-time): non-virtual functions, function overloading. Late binding (runtime): virtual functions, resolved via vtable at runtime.*

85. **What is the diamond problem and how does virtual inheritance solve it?**

    *Key points: Two classes derive from same base, then a class derives from both. Creates two base subobjects. Virtual inheritance (`virtual public Base`) ensures single shared base subobject.*

### Advanced OOP

86. **What is a friend function/class? When would you use it?**

    *Key points: Grants access to private members. Use for operator overloading (<<, >>), tightly coupled classes (iterator-container), factory functions.*

87. **What is a nested class? What are its access rules?**

    *Key points: Class defined inside another class. Has access to enclosing class's private members (if enclosing class grants friendship). Enclosing class doesn't have special access to nested class's private members.*

88. **What is the CRTP (Curiously Recurring Template Pattern)?**

    *Key points: `class Derived : public Base<Derived>`. Enables static polymorphism (no vtable). Used for mixins, object counting, singleton pattern.*

89. **What is type erasure? How does `std::function` implement it?**

    *Key points: Hides concrete type behind a common interface. std::function uses a small buffer optimization (SBO) for small callables, heap allocation for large ones, with virtual dispatch.*

90. **What is the PIMPL idiom and what are its benefits?**

    *Key points: Pointer to Implementation. Hides implementation details in .cpp file. Benefits: compilation firewall (faster builds), ABI stability, implementation hiding.*

### SOLID Principles

91. **Explain the Single Responsibility Principle.**

    *Key points: A class should have only one reason to change. Each class should have a single, well-defined responsibility. Leads to smaller, more focused, testable classes.*

92. **Explain the Open/Closed Principle.**

    *Key points: Classes should be open for extension but closed for modification. Use inheritance, composition, and polymorphism to add behavior without changing existing code.*

93. **Explain the Liskov Substitution Principle.**

    *Key points: Derived classes must be substitutable for their base classes. Subclass should not strengthen preconditions or weaken postconditions. Square-Rectangle problem is a classic violation.*

94. **Explain the Interface Segregation Principle.**

    *Key points: Clients should not depend on interfaces they don't use. Prefer many small, focused interfaces over one large, monolithic interface.*

95. **Explain the Dependency Inversion Principle.**

    *Key points: High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details; details should depend on abstractions.*

---

## 🔴 UPPER-MID TO SENIOR LEVEL

### Design Patterns

96. **Explain the Factory pattern and its variants (Simple Factory, Factory Method, Abstract Factory).**

    *Key points: Simple Factory: static method creating objects; Factory Method: virtual method in base class; Abstract Factory: interface for creating families of related objects.*

97. **Explain the Singleton pattern. What are its problems and modern alternatives?**

    *Key points: Ensures single instance. Problems: global state, hidden dependencies, testing difficulty. Modern alternatives: dependency injection, monostate pattern. Meyers' singleton (static local) is thread-safe in C++11+.*

98. **Explain the Observer pattern. How would you implement it in modern C++?**

    *Key points: Subject notifies observers of state changes. Modern C++: use std::function for slots, Signal/Slot pattern, or event bus with type-erased handlers.*

99. **Explain the Strategy pattern.**

    *Key points: Defines family of algorithms, encapsulates each, makes them interchangeable. Use std::function or polymorphic interfaces. Example: sorting algorithms, payment methods.*

100. **Explain the Command pattern and how it enables undo/redo.**

     *Key points: Encapsulates request as object. Each command has execute() and undo(). Store in stacks for undo/redo. Used in text editors, transaction systems.*

101. **Explain the Visitor pattern.**

     *Key points: Separates algorithm from object structure. New operations without modifying classes. Double dispatch. Modern C++: std::visit with variant for simpler cases.*

102. **Explain the Adapter pattern.**

     *Key points: Converts one interface to another. Object adapter (composition) vs class adapter (inheritance). Used for integrating legacy code or third-party libraries.*

103. **Explain the Decorator pattern.**

     *Key points: Adds behavior to objects dynamically. Wraps object with same interface. Examples: stream compression/encryption, beverage condiments.*

104. **Explain the Facade pattern.**

     *Key points: Provides simplified interface to complex subsystem. Reduces coupling between client and subsystem. Example: computer startup (CPU, memory, hard drive).*

105. **Explain the Proxy pattern.**

     *Key points: Provides surrogate/placeholder for another object. Types: virtual (lazy loading), protection (access control), remote (network), cache, logging.*

### Exceptions & Error Handling

106. **What are the exception safety guarantees?**

     *Key points: No-throw (operations always succeed); Strong (commit or rollback — state unchanged on failure); Basic (no leaks, valid state); No guarantee (may leak/corrupt).*

107. **What is stack unwinding?**

     *Key points: When exception is thrown, destructors of local objects are called as stack frames are exited. Ensures RAII cleanup. Destructors must not throw.*

108. **When should you NOT use exceptions?**

     *Key points: Real-time systems (unpredictable timing), destructors (must not throw), high-frequency code (overhead), expected failures (use optional/expected), cross-language boundaries.*

109. **What is the difference between `std::exception` and custom exception classes?**

     *Key points: std::exception provides what() virtual method. Custom exceptions can carry additional context (error codes, SQL state, etc.). Should derive from std::exception.*

### Testing

110. **What are the different types of tests in C++?**

     *Key points: Unit tests (individual components), Integration tests (component interaction), Performance tests (benchmarks), Property-based tests (invariants with random inputs), Fuzzing (crash detection with malformed inputs).*

111. **What is a mock and how do you use it in testing?**

     *Key points: Simulated object that mimics real dependency. Used with dependency injection. Google Mock provides EXPECT_CALL, MOCK_METHOD. Verify interactions and return predefined values.*

112. **What is property-based testing?**

     *Key points: Test properties/invariants with randomly generated inputs. Finds edge cases that example-based tests miss. Libraries: RapidCheck (C++), Hypothesis (Python).*

### Performance Optimization

113. **What is branch prediction and how does it affect performance?**

     *Key points: CPU predicts which branch will be taken. Mispredictions cause pipeline stalls (~10-20 cycles). Sort data before processing to make branches predictable. Use branchless programming when possible.*

114. **What is false sharing and how do you prevent it?**

     *Key points: Threads modify different variables on same cache line, causing unnecessary cache invalidations. Prevent with alignment (alignas(64)) and padding.*

115. **What is cache locality and why does it matter?**

     *Key points: Accessing nearby memory is faster (cache hits). Sequential access is prefetched by hardware. Random access causes cache misses (100x slower). Prefer contiguous containers (vector) over linked structures.*

116. **What is LTO (Link-Time Optimization)?**

     *Key points: Optimizes across translation units at link time. Enables inlining across files, dead code elimination. 10-20% performance gain. Longer compilation, more memory.*

117. **What is the difference between `-O2` and `-O3` optimization levels?**

     *Key points: -O3 enables more aggressive optimizations (function inlining, loop unrolling, vectorization). May increase binary size. Sometimes slower due to code bloat.*

### Low-Level & System Programming

118. **What is memory-mapped I/O and when would you use it?**

     *Key points: Maps file or device memory into process address space. Zero-copy I/O. Efficient for large files, shared memory between processes, device drivers.*

119. **What is the difference between `fork()` and `exec()`?**

     *Key points: fork() creates a copy of the current process; exec() replaces current process image with a new program. Combined: fork then exec to run a new program in a child process.*

120. **What is a signal and how do you handle it safely?**

     *Key points: Asynchronous notification sent to process. Signal handlers must be async-signal-safe (only use write(), not printf/malloc). Use sigaction() over signal(). Set volatile sig_atomic_t flags.*

121. **What is the difference between a pipe, a FIFO, and a Unix domain socket?**

     *Key points: Pipe: parent-child communication only; FIFO (named pipe): unrelated processes on same machine; Unix domain socket: bidirectional, stream/datagram, most flexible.*

### FFI & Cross-Language Interoperability

122. **What is the C++ ABI and why is it a problem for library distribution?**

     *Key points: C++ ABI includes name mangling, vtable layout, exception handling, RTTI. Differs between compilers and versions. Solution: extern "C" for stable ABI, or header-only libraries.*

123. **What is `extern "C"` and when do you need it?**

     *Key points: Disables C++ name mangling. Needed for C-compatible interfaces, shared libraries used by other languages, and callbacks passed to C libraries.*

124. **What is the PIMPL idiom and how does it help with ABI stability?**

     *Key points: Hides implementation behind a pointer. Changes to implementation don't change class layout. Enables adding features without breaking binary compatibility.*

### Build Systems & Tooling

125. **What is CMake and why is it the de facto standard for C++ projects?**

     *Key points: Cross-platform build system generator. Target-based (modern CMake 3.15+). Handles dependencies, testing, installation. Integrates with IDEs and package managers.*

126. **What is the difference between static and dynamic libraries?**

     *Key points: Static (.a/.lib): code copied into executable, no runtime dependencies, larger binary. Dynamic (.so/.dll/.dylib): loaded at runtime, smaller binary, can be updated independently.*

127. **What are sanitizers and how do you use them?**

     *Key points: Runtime instrumentation tools: AddressSanitizer (memory errors), UndefinedBehaviorSanitizer (UB), ThreadSanitizer (data races), MemorySanitizer (uninitialized reads). Compile with -fsanitize=flag.*

### Advanced Memory Management

128. **What is a custom allocator and when would you write one?**

     *Key points: Override default memory allocation. Types: pool (fixed-size blocks), arena (bump pointer), stack (LIFO). Use when profiling shows allocation is a bottleneck.*

129. **What is PMR (Polymorphic Memory Resources) in C++17?**

     *Key points: Standard allocator abstraction. Types: monotonic_buffer_resource (arena), synchronized_pool_resource, unsynchronized_pool_resource. Composable and type-erased.*

130. **What is memory alignment and why does it matter?**

     *Key points: Memory addresses should be multiples of data type size. Misaligned access is slower (or crashes on some architectures). Critical for SIMD (AVX requires 32-byte alignment).*

### Advanced Templates & Metaprogramming

131. **What is template metaprogramming?**

     *Key points: Using templates to perform computations at compile-time. Examples: compile-time factorial, type lists, SFINAE-based dispatch. Zero runtime cost.*

132. **What are type traits and how do you use them?**

     *Key points: Compile-time type queries: is_integral, is_pointer, is_same, etc. Type transformations: remove_const, add_pointer, decay. Use _v for values, _t for types.*

133. **What is `std::enable_if` and how does it work?**

     *Key points: Conditionally enables/disables template overloads. If condition is true, provides a typedef (type). If false, substitution fails (SFINAE). Modern alternative: concepts (C++20).*

134. **What are fold expressions (C++17)?**

     *Key points: Apply binary operator over parameter pack. `(args + ...)` = sum of all args. `(cout << ... << args)` = print all args. Unary right fold, unary left fold, binary folds.*

### Ranges & Views (C++20)

135. **What are C++20 ranges and how do they differ from traditional STL algorithms?**

     *Key points: Work on ranges (containers/views) instead of iterator pairs. Pipeable syntax: `data | filter | transform | take`. Lazy evaluation — no intermediate containers.*

136. **What is a view and how is it different from a container?**

     *Key points: View is non-owning, O(1) copy, lazy. Container owns data, eager. Views compose without allocation. Example: `numbers | filter(even) | transform(square) | take(5)`.*

### Concurrency (Advanced)

137. **What is a lock-free data structure?**

     *Key points: Uses atomic operations (CAS) instead of locks. No thread can block another. Progress guarantee: lock-free (system-wide progress) or wait-free (per-thread progress).*

138. **What is the ABA problem in lock-free programming?**

     *Key points: Thread reads A, another changes A→B→A, first thread's CAS succeeds but data changed. Solution: tagged pointers (ABA counter), hazard pointers, RCU.*

139. **What is memory ordering and why is it important?**

     *Key points: Controls visibility of writes across threads. Options: relaxed (atomicity only), acquire/release (synchronization), seq_cst (total order). Wrong ordering causes data races.*

140. **What is double-checked locking and how do you implement it correctly?**

     *Key points: Check without lock (fast path), then with lock (slow path). Must use atomic with acquire/release ordering. C++11+ makes this safe with std::atomic and memory ordering.*

---

## 💡 BONUS: Behavioral & Problem-Solving Questions

141. **Describe a time you had to debug a difficult concurrency bug. What tools and techniques did you use?**

     *Key points: ThreadSanitizer, AddressSanitizer, GDB with thread debugging, logging with thread IDs, reducing to minimal reproducer, code review for missing synchronization.*

142. **How would you design a thread-safe producer-consumer queue?**

     *Key points: Mutex + condition variable, or lock-free ring buffer. Handle spurious wakeups with predicate. Support graceful shutdown. Consider bounded vs unbounded.*

143. **How would you optimize a C++ application that's CPU-bound?**

     *Key points: Profile first (perf, VTune). Improve algorithms, reduce allocations, improve cache locality, add parallelism, use SIMD, enable LTO/PGO.*

144. **How would you optimize a C++ application that's memory-bound?**

     *Key points: Reduce allocations (reserve, pool allocators), improve data locality (SoA vs AoS), use memory-mapped files, compress data, use smaller types.*

145. **How would you modernize a legacy C++98 codebase?**

     *Key points: Incremental approach. Start with compiler upgrade and -Wall. Add C++11 features: auto, nullptr, range-for. Move to smart pointers. Add move semantics. Enable C++14/17 features gradually. Use clang-tidy for automated refactoring. Add unit tests before refactoring.*

146. **What are the trade-offs between using exceptions and error codes for error handling?**

     *Key points: Exceptions: cleaner code, can't be ignored, but have overhead and make control flow complex. Error codes: explicit, no overhead, but verbose and easy to ignore. Hybrid approaches exist (Expected<T> pattern).*

147. **How would you design a plugin system in C++?**

     *Key points: Define a stable ABI interface (abstract base class with virtual functions). Use dynamic loading (dlopen/LoadLibrary). Version the interface. Use factory functions. Consider dependency injection for plugin services.*

148. **Explain the concept of type erasure and how it's implemented in C++.**

     *Key points: Type erasure hides concrete types behind a common interface. Examples: std::function, std::any, std::variant. Implementation: base class with virtual functions + template-derived wrapper class.*

149. **How do you implement a thread-safe singleton in modern C++?**

     *Key points: Use function-local static (guaranteed thread-safe in C++11): static T& instance() { static T t; return t; }. Or use std::call_once with std::once_flag. Avoid double-checked locking.*

150. **What is the SBO (Small Buffer Optimization) and where is it used in the standard library?**

     *Key points: SBO stores small objects inline without heap allocation. Used in std::string (SSO), std::function, std::any. Improves performance for small objects by avoiding dynamic memory allocation.*

---

## 💡 BONUS: Behavioral & System Design Questions

151. **Describe a time you debugged a difficult memory corruption issue. What tools and techniques did you use?**

     *Key points: AddressSanitizer, Valgrind, core dumps, GDB, careful code review, binary search on commits, adding assertions, custom allocators with guard pages.*

152. **How would you design a high-performance logging library?**

     *Key points: Asynchronous logging (producer-consumer queue), multiple severity levels, format strings, configurable sinks (file, console, network), rotation policies, minimal overhead in hot paths, structured logging support.*

153. **Explain how you would implement a custom memory allocator.**

     *Key points: Pool allocator (fixed-size blocks), arena allocator (linear allocation + reset), stack allocator, free-list allocator. Consider alignment, fragmentation, thread safety, and deallocation strategy.*

154. **How would you approach reducing compile times in a large C++ project?**

     *Key points: Precompiled headers, forward declarations, reduce header dependencies, use PIMPL idiom, unity builds, modules (C++20), faster linker (lld/mold), parallel compilation, ccache/distcc.*

155. **What considerations go into choosing between runtime polymorphism (virtual functions) and compile-time polymorphism (templates)?**

     *Key points: Virtual functions: runtime flexibility, binary interface stability, but indirection cost. Templates: zero overhead, type safety at compile time, but code bloat, longer compile times, harder to debug. Use templates for performance-critical generic code, virtual for runtime-pluggable components.*

156. **How would you design a cross-platform networking library in C++?**

     *Key points: Abstract OS-specific APIs behind a common interface (Socket, ServerSocket). Use RAII for resource management. Support both sync and async I/O. Consider using proactor/reactor patterns. Abstract address resolution, protocol selection, and error handling.*

157. **Explain how you would implement a lock-free data structure.**

     *Key points: Use std::atomic with compare_exchange_weak/strong. Understand memory ordering (acquire/release/seq_cst). Handle the ABA problem. Start simple (lock-free stack with Treiber stack). Test thoroughly — lock-free is hard to get right.*

158. **How would you profile and optimize a CPU-bound C++ application?**

     *Key points: Use perf/Linux perf, VTune, or similar profilers. Identify hot spots. Optimize algorithms first, then micro-optimizations: cache locality, branch prediction, SIMD, loop unrolling, avoid virtual calls in hot paths, use PMR allocators.*

159. **What strategies would you use to ensure exception safety in a complex codebase?**

     *Key points: Follow RAII religiously. Use the basic/strong/nothrow guarantees. Avoid throwing destructors. Use scope guards (finally pattern). Test exception paths. Use noexcept where appropriate. Consider using std::optional or Expected<T> for expected failures.*

160. **How would you design a C++ API that is both performant and user-friendly?**

     *Key points: Provide both value and reference semantics. Use type-safe interfaces. Minimize header dependencies. Document preconditions and exception guarantees. Provide move operations. Consider ranges/views for composability. Follow the principle of least surprise.*

---

*Generated from the C++ Refreshers series covering 29 topics: basic types, control flow, storage/operators, functions, pointers, compilation, namespaces, value categories, containers, move semantics, modern C++, templates, smart pointers, threading, async, classes, OOP, SOLID, POSIX APIs, Windows APIs, system calls, networking/IPC, advanced templates, exceptions, testing, design patterns, performance optimization, FFI/best practices, and low-level programming.*
