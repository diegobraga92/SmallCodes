////////* COMPILATION MODEL *////////

// Let's trace through the complete compilation process with examples

// ============ PREPROCESSOR DIRECTIVES ============
// These are processed BEFORE actual compilation
// Common directives:
// #include, #define, #ifdef, #pragma, #error

// Example to demonstrate the full compilation chain:

// File: config.h
#ifndef CONFIG_H
#define CONFIG_H
#define MAX_SIZE 100
#define DEBUG_MODE
#endif

// File: math_utils.h
#ifndef MATH_UTILS_H
#define MATH_UTILS_H
int add(int a, int b);
int multiply(int a, int b);
#endif

// File: math_utils.cpp
#include "math_utils.h"
int add(int a, int b) {
    return a + b;
}
int multiply(int a, int b) {
    return a * b;
}

// File: main.cpp
#include "config.h"
#include "math_utils.h"
#include <iostream>

#ifdef DEBUG_MODE
    #define LOG(msg) std::cout << "DEBUG: " << msg << std::endl
#else
    #define LOG(msg)
#endif

int main() {
    LOG("Program started");
    std::cout << "MAX_SIZE: " << MAX_SIZE << std::endl;
    std::cout << "Add: " << add(10, 20) << std::endl;
    std::cout << "Multiply: " << multiply(5, 6) << std::endl;
    return 0;
}

# Compilation process step-by-step:

# Step 1: Preprocessing
# Expands all #include, #define, processes conditionals
g++ -E main.cpp -o main.ii  # Creates preprocessed output

# Step 2: Compilation (per translation unit)
# Each .cpp file is compiled separately to object file
g++ -c main.cpp -o main.o      # Compile main.cpp
g++ -c math_utils.cpp -o math_utils.o  # Compile math_utils.cpp

# Step 3: Linking
# Combines object files, resolves external references
g++ main.o math_utils.o -o program

# Or all steps at once:
g++ main.cpp math_utils.cpp -o program

#include <iostream>

// ============ COMPILATION STAGES DEMONSTRATION ============
void demonstrate_compilation_stages() {
    std::cout << "============ C++ COMPILATION MODEL ============\n" << std::endl;
    
    // ============ STAGE 1: PREPROCESSING ============
    std::cout << "=== Stage 1: Preprocessing ===" << std::endl;
    std::cout << "1. Processes all lines starting with #" << std::endl;
    std::cout << "2. Expands #include directives (file inclusion)" << std::endl;
    std::cout << "3. Handles #define macros (text substitution)" << std::endl;
    std::cout << "4. Processes conditional compilation (#ifdef, #ifndef)" << std::endl;
    std::cout << "5. Removes comments" << std::endl;
    std::cout << "6. Produces a single translation unit\n" << std::endl;
    
    // Example of what preprocessor does:
    #define SQUARE(x) ((x) * (x))  // Macro definition
    int result = SQUARE(5);  // Expands to: int result = ((5) * (5));
    
    // Conditional compilation
    #ifdef _WIN32
        std::cout << "Windows platform" << std::endl;
    #else
        std::cout << "Non-Windows platform" << std::endl;
    #endif
    
    // ============ STAGE 2: COMPILATION ============
    std::cout << "\n=== Stage 2: Compilation ===" << std::endl;
    std::cout << "1. Syntax and semantic analysis" << std::endl;
    std::cout << "2. Type checking" << std::endl;
    std::cout << "3. Template instantiation" << std::endl;
    std::cout << "4. Optimization" << std::endl;
    std::cout << "5. Generates object code (.obj/.o files)" << std::endl;
    std::cout << "6. Each .cpp file = one translation unit\n" << std::endl;
    
    // ============ STAGE 3: LINKING ============
    std::cout << "=== Stage 3: Linking ===" << std::endl;
    std::cout << "1. Combines multiple object files" << std::endl;
    std::cout << "2. Resolves external symbols (function/variable references)" << std::endl;
    std::cout << "3. Handles static vs dynamic linking" << std::endl;
    std::cout << "4. Creates executable or library\n" << std::endl;
    
    // Common linking errors:
    // - Undefined reference: declaration exists but no definition found
    // - Multiple definition: same symbol defined in multiple places
    // - Symbol not found: library not linked
    
    // ============ SEPARATE COMPILATION ============
    std::cout << "=== Separate Compilation ===" << std::endl;
    std::cout << "Why compile separately?" << std::endl;
    std::cout << "1. Faster builds: only recompile changed files" << std::endl;
    std::cout << "2. Modularity: independent development" << std::endl;
    std::cout << "3. Libraries: distribute compiled code\n" << std::endl;
    
    // Build tools handle this:
    // - Makefiles
    // - CMake
    // - Build systems (Bazel, Ninja)
}

int main() {
    demonstrate_compilation_stages();
    return 0;
}


////////* TRANSLATION UNITS *////////

// ============ PROJECT STRUCTURE EXAMPLE ============

// File: point.h - HEADER FILE (declarations only)
#ifndef POINT_H
#define POINT_H

#include <iostream>

class Point {
private:
    double x, y;
    
public:
    // Constructor declaration
    Point(double x = 0, double y = 0);
    
    // Method declarations
    double getX() const;
    double getY() const;
    void setX(double x);
    void setY(double y);
    void move(double dx, double dy);
    
    // Friend function declaration
    friend std::ostream& operator<<(std::ostream& os, const Point& p);
};

// Inline function can be in header (small functions)
inline double distance(const Point& p1, const Point& p2);

#endif // POINT_H

// File: point.cpp - SOURCE FILE (definitions)
#include "point.h"
#include <cmath>

// Constructor definition
Point::Point(double x, double y) : x(x), y(y) {}

// Method definitions
double Point::getX() const { return x; }
double Point::getY() const { return y; }
void Point::setX(double x) { this->x = x; }
void Point::setY(double y) { this->y = y; }
void Point::move(double dx, double dy) { x += dx; y += dy; }

// Friend function definition
std::ostream& operator<<(std::ostream& os, const Point& p) {
    os << "Point(" << p.x << ", " << p.y << ")";
    return os;
}

// Inline function definition (must be in header, but shown here for demo)
// Actually defined in point.h

// File: geometry.h - Another header
#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "point.h"

class Rectangle {
private:
    Point topLeft;
    double width, height;
    
public:
    Rectangle(const Point& tl, double w, double h);
    double area() const;
    double perimeter() const;
};

#endif // GEOMETRY_H

// File: geometry.cpp
#include "geometry.h"

Rectangle::Rectangle(const Point& tl, double w, double h) 
    : topLeft(tl), width(w), height(h) {}

double Rectangle::area() const {
    return width * height;
}

double Rectangle::perimeter() const {
    return 2 * (width + height);
}

// File: main.cpp
#include "point.h"
#include "geometry.h"
#include <iostream>

// Function prototype (declaration)
void demonstrate_translation_units();

int main() {
    demonstrate_translation_units();
    return 0;
}

#include <iostream>
#include <string>

void demonstrate_translation_units() {
    std::cout << "============ TRANSLATION UNITS & HEADERS ============\n" << std::endl;
    
    // ============ TRANSLATION UNIT ============
    std::cout << "=== Translation Unit ===" << std::endl;
    std::cout << "Definition: A source file (.cpp) after preprocessing" << std::endl;
    std::cout << "Includes all #included headers" << std::endl;
    std::cout << "Compiled independently into object file\n" << std::endl;
    
    std::cout << "Key characteristics:" << std::endl;
    std::cout << "1. Contains exactly one main() function (for executables)" << std::endl;
    std::cout << "2. Has internal linkage (static) or external linkage" << std::endl;
    std::cout << "3. Can include multiple headers\n" << std::endl;
    
    // ============ HEADER FILES (.h, .hpp, .hxx) ============
    std::cout << "=== Header Files (.h/.hpp) ===" << std::endl;
    std::cout << "Purpose: Declarations only (no definitions)" << std::endl;
    std::cout << std::endl;
    std::cout << "What goes in headers:" << std::endl;
    std::cout << "✓ Class declarations" << std::endl;
    std::cout << "✓ Function prototypes" << std::endl;
    std::cout << "✓ Extern variable declarations" << std::endl;
    std::cout << "✓ Template definitions (must be in headers)" << std::endl;
    std::cout << "✓ Inline function definitions" << std::endl;
    std::cout << "✓ Type definitions (typedef, using)" << std::endl;
    std::cout << "✓ Constant declarations (extern const)\n" << std::endl;
    
    std::cout << "What should NOT go in headers:" << std::endl;
    std::cout << "✗ Function definitions (except inline/templates)" << std::endl;
    std::cout << "✗ Variable definitions (except constexpr/static const)" << std::endl;
    std::cout << "✗ Main function\n" << std::endl;
    
    // ============ SOURCE FILES (.cpp, .cc, .cxx) ============
    std::cout << "=== Source Files (.cpp/.cc) ===" << std::endl;
    std::cout << "Purpose: Definitions" << std::endl;
    std::cout << std::endl;
    std::cout << "What goes in source files:" << std::endl;
    std::cout << "✓ Function definitions" << std::endl;
    std::cout << "✓ Global/static variable definitions" << std::endl;
    std::cout << "✓ Static member definitions" << std::endl;
    std::cout << "✓ Main function\n" << std::endl;
    
    // ============ ONE DEFINITION RULE (ODR) ============
    std::cout << "=== One Definition Rule (ODR) ===" << std::endl;
    std::cout << "For non-inline functions/global variables:" << std::endl;
    std::cout << "1. Can have multiple declarations" << std::endl;
    std::cout << "2. Must have exactly ONE definition in entire program" << std::endl;
    std::cout << "3. Violation causes linker error (multiple definitions)\n" << std::endl;
    
    std::cout << "Exceptions to ODR (can have multiple definitions):" << std::endl;
    std::cout << "1. Inline functions" << std::endl;
    std::cout << "2. Class definitions (in each translation unit that uses them)" << std::endl;
    std::cout << "3. Templates (instantiated in each TU)" << std::endl;
    std::cout << "4. Const variables with internal linkage\n" << std::endl;
    
    // ============ DECLARATION vs DEFINITION ============
    std::cout << "=== Declaration vs Definition ===" << std::endl;
    
    // Declaration examples
    extern int global_var;      // Declaration (no memory allocated)
    void function(int x);       // Function prototype
    class MyClass;              // Forward declaration
    
    // Definition examples
    int global_var = 42;        // Definition (memory allocated)
    void function(int x) {      // Function definition
        std::cout << x << std::endl;
    }
    
    // ============ LINKAGE ============
    std::cout << "\n=== Linkage Types ===" << std::endl;
    
    // External linkage (can be accessed from other TUs)
    extern int external_var;          // Declaration
    void external_function();         // Declaration
    
    // Internal linkage (only within this TU)
    static int internal_var = 100;    // Definition with internal linkage
    static void internal_function() { // Internal linkage function
        std::cout << "Internal" << std::endl;
    }
    
    // No linkage (local variables)
    auto no_linkage_example = []() {
        int local_var = 10;  // No linkage
    };
    
    // ============ INLINE FUNCTIONS IN HEADERS ============
    std::cout << "\n=== Inline Functions in Headers ===" << std::endl;
    std::cout << "Why inline functions can be in headers:" << std::endl;
    std::cout << "1. inline suggests to compiler: insert code at call site" << std::endl;
    std::cout << "2. Multiple definitions allowed across TUs" << std::endl;
    std::cout << "3. All definitions must be identical" << std::endl;
    std::cout << "4. Compiler chooses one for out-of-line calls\n" << std::endl;
    
    // ============ TEMPLATES MUST BE IN HEADERS ============
    std::cout << "=== Templates Must Be in Headers ===" << std::endl;
    std::cout << "Reason: Templates are instantiated at compile time" << std::endl;
    std::cout << "Each TU needs full template definition" << std::endl;
    std::cout << "Exception: explicit instantiation in .cpp file\n" << std::endl;
    
    // ============ BEST PRACTICES ============
    std::cout << "=== Best Practices ===" << std::endl;
    std::cout << "1. Keep headers minimal (declare only what's needed)" << std::endl;
    std::cout << "2. Use forward declarations when possible" << std::endl;
    std::cout << "3. One class per header (usually)" << std::endl;
    std::cout << "4. Use include guards or #pragma once" << std::endl;
    std::cout << "5. Don't include unnecessary headers" << std::endl;
    std::cout << "6. Use source files for implementation details" << std::endl;
}

// Example of things that cause ODR violations:

// In header.h (if included in multiple .cpp files):
// int global;  // VIOLATION: multiple definitions if header included multiple times
// void func() {}  // VIOLATION: multiple definitions

// Correct in header.h:
// extern int global;  // Declaration only
// inline void func() {}  // inline allows multiple definitions
// const int MAX = 100;  // Internal linkage in C++ (ok)

int main() {
    demonstrate_translation_units();
    return 0;
}