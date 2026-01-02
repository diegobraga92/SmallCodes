////////* INCLUDES *////////

// ============ #INCLUDE DIRECTIVE ============

// File: constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

const double PI = 3.141592653589793;
const int MAX_BUFFER_SIZE = 1024;

#endif

// File: utilities.h
#ifndef UTILITIES_H
#define UTILITIES_H

#include <string>

void log_message(const std::string& message);
std::string trim(const std::string& str);

#endif

// File: utilities.cpp
#include "utilities.h"
#include <algorithm>
#include <cctype>

void log_message(const std::string& message) {
    // Implementation
}

std::string trim(const std::string& str) {
    // Implementation
    return str;
}

// File: main.cpp
#include <iostream>      // System header (angle brackets)
#include "constants.h"   // User header (quotes)
#include "utilities.h"   // Another user header

// Demonstrate different include scenarios
void demonstrate_includes() {
    std::cout << "============ #INCLUDE & HEADER GUARDS ============\n" << std::endl;
    
    // ============ #INCLUDE SYNTAX ============
    std::cout << "=== #include Syntax ===" << std::endl;
    std::cout << "Two forms:" << std::endl;
    std::cout << "1. #include <header>  - System headers" << std::endl;
    std::cout << "   • Searches in system include paths" << std::endl;
    std::cout << "   • Use for standard library, external libraries" << std::endl;
    
    std::cout << "\n2. #include \"header\" - User headers" << std::endl;
    std::cout << "   • Searches in current directory first" << std::endl;
    std::cout << "   • Then searches system paths" << std::endl;
    std::cout << "   • Use for your project's headers\n" << endl;
    
    // ============ HOW #INCLUDE WORKS ============
    std::cout << "=== How #include Works ===" << std::endl;
    std::cout << "1. Preprocessor finds the file" << std::endl;
    std::cout << "2. Copies entire file content" << std::endl;
    std::cout << "3. Replaces #include directive with file content" << std::endl;
    std::cout << "4. Process continues recursively\n" << endl;
    
    // ============ CIRCULAR DEPENDENCIES ============
    std::cout << "=== Circular Dependencies ===" << std::endl;
    std::cout << "Problem: A.h includes B.h, B.h includes A.h" << std::endl;
    std::cout << "Solution: Forward declarations\n" << std::endl;
    
    // Example of circular dependency and solution:
    // File: employee.h
    /*
    #ifndef EMPLOYEE_H
    #define EMPLOYEE_H
    
    #include "department.h"  // Problem: department.h includes employee.h
    
    class Employee {
        Department* dept;  // Use pointer or reference
    };
    
    #endif
    */
    
    // Solution: forward declaration in employee.h
    /*
    #ifndef EMPLOYEE_H
    #define EMPLOYEE_H
    
    class Department;  // Forward declaration instead of #include
    
    class Employee {
        Department* dept;  // Ok with forward declaration
    };
    
    #endif
    */
    
    // Then in employee.cpp:
    // #include "department.h"  // Include the full definition
    
    // ============ INCLUDE GUARDS ============
    std::cout << "=== Include Guards ===" << std::endl;
    std::cout << "Purpose: Prevent multiple inclusions of same header" << std::endl;
    
    std::cout << "\nTraditional include guard:" << std::endl;
    std::cout << "#ifndef UNIQUE_NAME_H" << std::endl;
    std::cout << "#define UNIQUE_NAME_H" << std::endl;
    std::cout << "// Header content" << std::endl;
    std::cout << "#endif // UNIQUE_NAME_H\n" << std::endl;
    
    std::cout << "How it works:" << std::endl;
    std::cout << "1. First inclusion: UNIQUE_NAME_H not defined" << std::endl;
    std::cout << "2. #define UNIQUE_NAME_H" << std::endl;
    std::cout << "3. Process header content" << std::endl;
    std::cout << "4. Subsequent inclusions: UNIQUE_NAME_H already defined" << std::endl;
    std::cout << "5. Skips entire header content\n" << std::endl;
    
    // ============ #PRAGMA ONCE ============
    std::cout << "=== #pragma once ===" << std::endl;
    std::cout << "Modern alternative to include guards" << std::endl;
    std::cout << "#pragma once" << std::endl;
    std::cout << "// Header content\n" << std::endl;
    
    std::cout << "Advantages:" << std::endl;
    std::cout << "• Shorter, less error-prone" << std::endl;
    std::cout << "• Compiler handles uniqueness" << std::endl;
    std::cout << "• May be faster for compiler\n" << std::endl;
    
    std::cout << "Disadvantages:" << std::cout;
    std::cout << "• Not standard C++ (but widely supported)" << std::cout;
    std::cout << "• Issues with symlinks/hardlinks" << std::endl;
    std::cout << "• Some build systems may copy headers\n" << std::endl;
    
    // ============ COMPARISON ============
    std::cout << "=== Include Guard vs #pragma once ===" << std::endl;
    
    std::cout << "Example header with both:" << std::endl;
    std::cout << "#pragma once" << std::endl;
    std::cout << "#ifndef MY_HEADER_H" << std::endl;
    std::cout << "#define MY_HEADER_H" << std::endl;
    std::cout << "// Content" << std::endl;
    std::cout << "#endif\n" << std::endl;
    
    std::cout << "Why use both?" << std::endl;
    std::cout << "1. #pragma once for compilers that support it" << std::endl;
    std::cout << "2. Include guards for portability" << std::endl;
    std::cout << "3. Defense in depth\n" << std::endl;
    
    // ============ COMMON PITFALLS ============
    std::cout << "=== Common Pitfalls ===" << std::endl;
    
    std::cout << "1. Misspelled guard name:" << std::endl;
    std::cout << "   // File: myclass.h" << std::endl;
    std::cout << "   #ifndef MY_CLASS_H  // Good" << std::endl;
    std::cout << "   #ifndef MYCLASS_H   // Bad if another file uses same" << std::endl;
    
    std::cout << "\n2. Forgetting #endif:" << std::endl;
    std::cout << "   // Compilation error or weird behavior" << std::endl;
    
    std::cout << "\n3. Nested headers without guards:" << std::endl;
    std::cout << "   // If A.h includes B.h, and B.h doesn't have guards..." << std::endl;
    
    std::cout << "\n4. Using reserved names:" << std::endl;
    std::cout << "   #ifndef _MYHEADER_H  // Underscore + capital is reserved" << std::endl;
    std::cout << "   #ifndef __HEADER_H   // Double underscore is reserved\n" << std::endl;
    
    // ============ MODERN PRACTICES ============
    std::cout << "=== Modern Practices ===" << std::endl;
    
    std::cout << "1. Use descriptive, unique guard names:" << std::endl;
    std::cout << "   PROJECT_PATH_FILE_H" << std::endl;
    std::cout << "   Example: MYPROJECT_SRC_UTILS_MATH_H" << std::endl;
    
    std::cout << "\n2. Consider #pragma once for new projects" << std::endl;
    
    std::cout << "\n3. Use forward declarations to reduce includes" << std::endl;
    
    std::cout << "\n4. Include what you use (IWYU principle)" << std::endl;
    std::cout << "   • Don't rely on transitive includes" << std::endl;
    std::cout << "   • Each file should include what it needs" << std::endl;
    
    std::cout << "\n5. Order includes consistently:" << std::endl;
    std::cout << "   1. Related header (for .cpp files)" << std::endl;
    std::cout << "   2. System headers" << std::endl;
    std::cout << "   3. Other library headers" << std::endl;
    std::cout << "   4. Project headers\n" << std::endl;
    
    // ============ EXAMPLE OF GOOD PRACTICE ============
    std::cout << "=== Example of Good Practice ===" << std::endl;
    
    std::cout << "// File: utils/string_utils.h" << std::endl;
    std::cout << "#pragma once" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "#include <string>" << std::endl;
    std::cout << "#include <vector>" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "// Forward declaration if only pointers/references needed" << std::endl;
    std::cout << "class SomeClass;" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "namespace utils {" << std::endl;
    std::cout << "    std::vector<std::string> split(const std::string& str, char delimiter);" << std::endl;
    std::cout << "    bool starts_with(const std::string& str, const std::string& prefix);" << std::endl;
    std::cout << "} // namespace utils\n" << std::endl;
}

int main() {
    demonstrate_includes();
    return 0;
}


////////* NAMESPACE *////////

#include <iostream>
#include <string>
#include <vector>

// ============ BASIC NAMESPACE USAGE ============

// Global namespace (unnamed)
int global_var = 100;

// User-defined namespace
namespace MyLibrary {
    int version = 1;
    
    void print_version() {
        std::cout << "Library version: " << version << std::endl;
    }
    
    // Nested namespace (C++17 allows nicer syntax)
    namespace Math {
        const double PI = 3.14159;
        
        double circle_area(double radius) {
            return PI * radius * radius;
        }
    }
    
    // Inline namespace (C++11)
    inline namespace v1 {
        void api_function() {
            std::cout << "API v1" << std::endl;
        }
    }
    
    namespace v2 {
        void api_function() {
            std::cout << "API v2" << std::endl;
        }
    }
}

// Anonymous namespace (internal linkage)
namespace {
    int internal_counter = 0;  // Only accessible in this translation unit
    
    void internal_function() {
        std::cout << "Internal function" << std::endl;
    }
}

// Namespace alias
namespace ML = MyLibrary;
namespace MLM = MyLibrary::Math;

void demonstrate_namespaces() {
    std::cout << "============ NAMESPACES ============\n" << std::endl;
    
    // ============ ACCESSING NAMESPACE MEMBERS ============
    std::cout << "=== Accessing Namespace Members ===" << std::endl;
    
    // 1. Fully qualified name
    MyLibrary::print_version();
    std::cout << "PI: " << MyLibrary::Math::PI << std::endl;
    
    // 2. Using declaration (brings single name into scope)
    using MyLibrary::version;
    std::cout << "Version (using declaration): " << version << std::endl;
    
    // 3. Using directive (brings entire namespace into scope)
    using namespace MyLibrary::Math;
    std::cout << "PI (using directive): " << PI << std::endl;
    std::cout << "Area: " << circle_area(2.0) << std::endl;
    
    // ============ NAMESPACE BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    std::cout << "1. Use namespaces to avoid name collisions" << std::endl;
    std::cout << "2. Never put 'using namespace' in headers" << std::endl;
    std::cout << "3. Prefer fully qualified names in headers" << std::endl;
    std::cout << "4. Use anonymous namespaces for internal linkage" << std::endl;
    std::cout << "5. Use inline namespaces for versioning\n" << std::endl;
    
    // ============ NAMESPACE USAGE EXAMPLES ============
    std::cout << "=== Practical Examples ===" << std::endl;
    
    // Example 1: Library design
    namespace Graphics {
        namespace Shapes {
            class Circle { /* ... */ };
            class Rectangle { /* ... */ };
        }
        
        namespace Rendering {
            void render(const Shapes::Circle& c) { /* ... */ }
        }
    }
    
    // Using the library
    Graphics::Shapes::Circle c;
    Graphics::Rendering::render(c);
    
    // Example 2: Versioning with inline namespaces
    std::cout << "\n=== Versioning with Inline Namespaces ===" << std::endl;
    
    MyLibrary::api_function();  // Calls v1 (inline namespace is default)
    MyLibrary::v2::api_function();  // Explicitly call v2
    
    // Example 3: Namespace for implementation details
    namespace MyLibrary {
        namespace detail {  // Convention: detail for internal implementation
            class Implementation {
                // Hidden implementation details
            };
        }
        
        // Public interface uses implementation
        class PublicClass {
        private:
            detail::Implementation impl;
        };
    }
    
    // ============ NAMESPACES AND ADL ============
    std::cout << "\n=== Argument-Dependent Lookup (ADL) ===" << std::endl;
    
    namespace Custom {
        class Widget {
        public:
            int value;
        };
        
        // Operator in same namespace as Widget
        std::ostream& operator<<(std::ostream& os, const Widget& w) {
            return os << "Widget(" << w.value << ")";
        }
    }
    
    Custom::Widget w{42};
    std::cout << w << std::endl;  // ADL finds operator<< in Custom namespace
    
    // ============ NAMESPACE STD ============
    std::cout << "\n=== The std Namespace ===" << std::endl;
    
    // Why not to do 'using namespace std;'
    vector<int> bad;  // ERROR without 'using namespace std;'
    std::vector<int> good;  // Correct
    
    // Exception: implementation files with limited scope
    {
        using namespace std;
        vector<int> local_vec;  // OK in limited scope
    }
    
    // ============ NAMESPACE IN HEADERS ============
    std::cout << "\n=== Namespaces in Headers ===" << std::endl;
    
    std::cout << "Good header example:" << std::endl;
    std::cout << "// mylib.h" << std::endl;
    std::cout << "#pragma once" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "#include <string>" << std::endl;
    std::cout << "" << std::endl;
    std::cout << "namespace mylib {" << std::endl;
    std::cout << "    class MyClass {" << std::endl;
    std::cout << "    public:" << std::endl;
    std::cout << "        void do_something(const std::string& input);" << std::endl;
    std::cout << "    };" << std::endl;
    std::cout << "} // namespace mylib\n" << std::endl;
}

// ============ NAMESPACE DEFINITIONS CAN BE SPLIT ============
namespace MyLibrary {
    // Can add more members later
    std::string get_name() {
        return "MyLibrary";
    }
}

// ============ NAMESPACE WITH TEMPLATES ============
namespace TemplateExample {
    template<typename T>
    class Container {
    public:
        void add(const T& item) { /* ... */ }
    };
    
    template<typename T>
    T max(T a, T b) {
        return (a > b) ? a : b;
    }
}

int main() {
    demonstrate_namespaces();
    
    // Demonstrate inline namespace behavior
    using namespace MyLibrary;
    api_function();  // Calls v1 (inline)
    
    return 0;
}
