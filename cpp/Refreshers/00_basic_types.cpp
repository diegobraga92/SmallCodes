////////* BASIC TYPES *////////

#include <iostream>
#include <limits>
#include <typeinfo>  // For type identification
#include <iomanip>   // For output formatting

int main() {
    // ========== INTEGER TYPES ==========
    int myInt = 42;  // Most common integer type, typically 4 bytes (32 bits)
    
    // Integer sizes can be explicitly specified
    short myShort = 32767;      // At least 16 bits, often -32,768 to 32,767
    long myLong = 2147483647L;  // At least 32 bits (L suffix for long literal)
    long long myLongLong = 9223372036854775807LL;  // At least 64 bits
    
    std::cout << "int: " << myInt << " (size: " << sizeof(myInt) << " bytes)" << std::endl;
    std::cout << "short max: " << std::numeric_limits<short>::max() << std::endl;
    
    // ========== FLOATING-POINT TYPES ==========
    float myFloat = 3.14159f;      // Single precision, 4 bytes (f suffix required for float)
    double myDouble = 3.141592653589793;  // Double precision, 8 bytes (default for literals)
    long double myLongDouble = 3.14159265358979323846L;  // Extended precision
    
    // Floating-point precision demonstration
    std::cout << std::setprecision(10);  // Set output precision
    std::cout << "float: " << myFloat << std::endl;     // May lose precision
    std::cout << "double: " << myDouble << std::endl;   // More precise
    std::cout << "Size of double: " << sizeof(double) << " bytes" << std::endl;
    
    // ========== CHARACTER TYPES ==========
    char myChar = 'A';         // Single character, 1 byte
    signed char mySignedChar = -128;  // Can hold negative values
    unsigned char myUnsignedChar = 255;  // Only positive (0-255)
    
    // Characters are actually integers
    std::cout << "char 'A' as int: " << static_cast<int>(myChar) << std::endl;
    std::cout << "char 'A' + 1: " << static_cast<char>(myChar + 1) << std::endl;
    
    // Wide characters for international text
    wchar_t myWideChar = L'Ω';      // Wide character (size depends on platform)
    char16_t utf16Char = u'€';      // UTF-16 character (C++11)
    char32_t utf32Char = U'😊';     // UTF-32 character (C++11)
    
    // ========== BOOLEAN TYPE ==========
    bool myBool = true;        // Can be true or false
    bool anotherBool = false;
    
    // Booleans are stored as integers (0 = false, non-zero = true)
    std::cout << "true as int: " << static_cast<int>(myBool) << std::endl;
    std::cout << "false as int: " << static_cast<int>(anotherBool) << std::endl;
    
    // Boolean operations
    bool result = (10 > 5) && (3 != 4);  // true && true = true
    std::cout << "(10 > 5) && (3 != 4) = " << std::boolalpha << result << std::endl;
    
    // ========== TYPE IDENTIFICATION ==========
    std::cout << "\nType identification:" << std::endl;
    std::cout << "Type of myInt: " << typeid(myInt).name() << std::endl;
    std::cout << "Type of myDouble: " << typeid(myDouble).name() << std::endl;
    
    return 0;
}

////////* TYPE MODIFIERS *////////

#include <iostream>
#include <typeinfo>  // For type identification
#include <type_traits>  // For type traits

void demonstrate_data_types() {
    std::cout << "============ DATA TYPES & VARIABLES ============\n" << std::endl;
    
    // ============ PRIMITIVE TYPES ============
    std::cout << "=== Primitive Types ===" << std::endl;
    
    // Fundamental types
    bool boolean = true;          // 1 byte, true/false
    char character = 'A';         // 1 byte, ASCII character
    int integer = 42;             // Usually 4 bytes
    float floating = 3.14f;       // 4 bytes, single precision
    double dbl = 3.1415926535;    // 8 bytes, double precision
    
    std::cout << "bool: " << boolean << " (size: " << sizeof(bool) << " byte)" << std::endl;
    std::cout << "char: " << character << " (size: " << sizeof(char) << " byte)" << std::endl;
    std::cout << "int: " << integer << " (size: " << sizeof(int) << " bytes)" << std::endl;
    std::cout << "float: " << floating << " (size: " << sizeof(float) << " bytes)" << std::endl;
    std::cout << "double: " << dbl << " (size: " << sizeof(double) << " bytes)\n" << std::endl;
    
    // ============ TYPE MODIFIERS ============
    std::cout << "=== Type Modifiers ===" << std::endl;
    
    // Signed/unsigned modifiers
    signed int s_int = -100;      // Can be negative (default for int)
    unsigned int u_int = 100;     // Only non-negative
    
    // Size modifiers
    short small = 32000;          // At least 16 bits
    long large = 1000000L;        // At least 32 bits
    long long huge = 10000000000LL; // At least 64 bits
    
    // Floating-point precision
    long double extra_precise = 3.1415926535897932385L;
    
    std::cout << "short: " << sizeof(short) << " bytes" << std::endl;
    std::cout << "long: " << sizeof(long) << " bytes" << std::endl;
    std::cout << "long long: " << sizeof(long long) << " bytes" << std::endl;
    std::cout << "long double: " << sizeof(long double) << " bytes\n" << std::endl;
    
    // ============ AUTO TYPE DEDUCTION (C++11) ============
    std::cout << "=== auto (C++11) ===" << std::endl;
    
    // auto deduces type from initializer
    auto x = 42;           // int
    auto y = 3.14;         // double
    auto z = 3.14f;        // float
    auto c = 'A';          // char
    auto b = true;         // bool
    
    std::cout << "auto x = 42: " << typeid(x).name() << std::endl;
    std::cout << "auto y = 3.14: " << typeid(y).name() << std::endl;
    
    // auto with references and pointers
    int value = 100;
    auto& ref = value;      // int&
    auto ptr = &value;      // int*
    auto* ptr2 = &value;    // int* (explicit pointer)
    
    // auto in range-based for loops
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    std::cout << "\nRange-based for with auto:" << std::endl;
    for (auto num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    // auto with complex types
    auto vec = std::vector<int>{10, 20, 30};  // No need to specify type twice
    
    // CAUTION: auto strips references and const qualifiers!
    const int const_val = 42;
    auto deduced = const_val;  // int, NOT const int!
    deduced = 100;  // This works
    
    // To preserve const, use const auto
    const auto const_deduced = const_val;  // const int
    
    // ============ DECLTYPE (C++11) ============
    std::cout << "\n=== decltype (C++11) ===" << std::endl;
    
    // decltype deduces the exact type of an expression
    int i = 10;
    const int& ref_i = i;
    
    decltype(i) a;           // int
    decltype(ref_i) b = i;   // const int& (must be initialized)
    decltype((i)) c = i;     // int& (note double parentheses!)
    
    std::cout << "decltype(i): " << typeid(decltype(i)).name() << std::endl;
    std::cout << "decltype(ref_i): " << typeid(decltype(ref_i)).name() << std::endl;
    std::cout << "decltype((i)): " << typeid(decltype((i))).name() << std::endl;
    
    // Practical use: template metaprogramming
    template<typename T, typename U>
    auto add(T t, U u) -> decltype(t + u) {  // Trailing return type
        return t + u;
    }
    
    // decltype(auto) (C++14) - combines auto and decltype behavior
    int val = 42;
    const int& cref = val;
    
    auto a1 = cref;           // int (strips const and reference)
    decltype(auto) a2 = cref; // const int& (preserves exact type)
    
    // Useful for perfect forwarding in templates
    template<typename T>
    decltype(auto) forward_example(T&& t) {
        return std::forward<T>(t);
    }
    
    // ============ VARIABLE DECLARATION ============
    std::cout << "\n=== Variable Declaration Styles ===" << std::endl;
    
    // Copy initialization
    int copy_init = 10;
    
    // Direct initialization
    int direct_init(20);
    
    // Brace initialization (C++11) - PREFERRED
    int brace_init{30};           // No narrowing conversions allowed
    int brace_init2 = {40};       // Alternative syntax
    
    // Brace initialization prevents narrowing
    // int narrow{3.14};  // ERROR: narrowing conversion
    int narrow(3.14);     // OK: truncates to 3 (but dangerous!)
    
    std::cout << "Brace initialization is safer - prevents narrowing!" << std::endl;
}

// ============ GLOBAL VS LOCAL VARIABLES ============
int global_var = 100;  // Global variable (avoid when possible)

int main() {
    demonstrate_data_types();
    
    // ============ VARIABLE SCOPE ============
    std::cout << "\n=== Variable Scope ===" << std::endl;
    
    int local_var = 50;  // Local to main()
    
    {
        int block_var = 25;  // Local to this block
        local_var = 75;      // Can modify enclosing scope variable
        // global_var accessible here
    }
    // block_var not accessible here - out of scope
    
    // ============ STATIC LOCAL VARIABLES ============
    std::cout << "\n=== Static Local Variables ===" << std::endl;
    
    for (int i = 0; i < 5; ++i) {
        static int static_counter = 0;  // Initialized only once!
        int regular_counter = 0;
        
        ++static_counter;
        ++regular_counter;
        
        std::cout << "static: " << static_counter 
                  << ", regular: " << regular_counter << std::endl;
    }
    
    return 0;
}

////////* SIZES & PLATFORM DEPENDENCY *////////

#include <iostream>
#include <cstdint>  // For fixed-width integer types

int main() {
    // ========== PLATFORM-DEPENDENT SIZES ==========
    std::cout << "=== Platform-Dependent Type Sizes ===" << std::endl;
    std::cout << "sizeof(char): " << sizeof(char) << " (ALWAYS 1 byte by definition)" << std::endl;
    std::cout << "sizeof(short): " << sizeof(short) << " bytes" << std::endl;
    std::cout << "sizeof(int): " << sizeof(int) << " bytes" << std::endl;
    std::cout << "sizeof(long): " << sizeof(long) << " bytes" << std::endl;
    std::cout << "sizeof(long long): " << sizeof(long long) << " bytes" << std::endl;
    std::cout << "sizeof(float): " << sizeof(float) << " bytes" << std::endl;
    std::cout << "sizeof(double): " << sizeof(double) << " bytes" << std::endl;
    std::cout << "sizeof(bool): " << sizeof(bool) << " bytes" << std::endl;
    std::cout << "sizeof(void*): " << sizeof(void*) << " bytes (pointer size)" << std::endl;
    
    // ========== FIXED-WIDTH INTEGER TYPES (C++11) ==========
    // These provide consistent sizes across platforms
    std::cout << "\n=== Fixed-Width Integers (from <cstdint>) ===" << std::endl;
    std::cout << "sizeof(int8_t): " << sizeof(int8_t) << " bytes (exactly 8 bits)" << std::endl;
    std::cout << "sizeof(int16_t): " << sizeof(int16_t) << " bytes (exactly 16 bits)" << std::endl;
    std::cout << "sizeof(int32_t): " << sizeof(int32_t) << " bytes (exactly 32 bits)" << std::endl;
    std::cout << "sizeof(int64_t): " << sizeof(int64_t) << " bytes (exactly 64 bits)" << std::endl;
    
    // ========== MIN/MAX VALUES ==========
    // These vary by platform for standard types
    std::cout << "\n=== Value Ranges ===" << std::endl;
    std::cout << "char range: " << int(std::numeric_limits<char>::min()) 
              << " to " << int(std::numeric_limits<char>::max()) << std::endl;
    std::cout << "unsigned char range: 0 to " 
              << int(std::numeric_limits<unsigned char>::max()) << std::endl;
    
    // ========== PLATFORM-SPECIFIC ISSUES ==========
    // Example: What happens when we exceed type limits?
    unsigned int maxUint = std::numeric_limits<unsigned int>::max();
    std::cout << "\nMax unsigned int: " << maxUint << std::endl;
    maxUint += 1;  // Overflow - wraps around to 0
    std::cout << "After overflow (max + 1): " << maxUint << std::endl;
    
    // ========== ENDIANNESS ==========
    // Different platforms store multi-byte values differently
    int testValue = 0x12345678;
    unsigned char* bytes = reinterpret_cast<unsigned char*>(&testValue);
    
    std::cout << "\nEndianness test (value 0x12345678 in memory):" << std::endl;
    for(size_t i = 0; i < sizeof(testValue); ++i) {
        std::cout << "Byte " << i << ": 0x" << std::hex << (int)bytes[i] << std::dec << std::endl;
    }
    // On little-endian (x86): 78 56 34 12
    // On big-endian: 12 34 56 78
    
    return 0;
}


////////* SIGNING *////////

#include <iostream>
#include <bitset>  // For binary representation

void demonstrate_signed_unsigned() {
    std::cout << "============ SIGNED vs UNSIGNED ============\n" << std::endl;
    
    // ============ SIGNED INTEGERS ============
    // Can represent positive, negative, and zero
    signed int s_int = -100;  // 'signed' keyword is optional for int
    int another_signed = -42;  // Default is signed
    
    std::cout << "Signed int: " << s_int << std::endl;
    std::cout << "Range: " << std::numeric_limits<signed int>::min() 
              << " to " << std::numeric_limits<signed int>::max() << std::endl;

    // ============ UNSIGNED INTEGERS ============
    // Can only represent zero and positive numbers
    unsigned int u_int = 100;
    unsigned int max_uint = std::numeric_limits<unsigned int>::max();
    
    std::cout << "\nUnsigned int: " << u_int << std::endl;
    std::cout << "Range: 0 to " << max_uint << std::endl;

    // ============ CRITICAL DIFFERENCES ============
    std::cout << "\n=== Critical Behaviors ===" << std::endl;
    
    // 1. UNDERFLOW/OVERFLOW BEHAVIOR
    unsigned int u_min = 0;
    u_min--;  // Underflow - wraps around to max value
    std::cout << "Unsigned 0 - 1 = " << u_min << " (wrap-around!)" << std::endl;
    
    signed int s_min = -2147483648;  // Near minimum
    s_min--;  // Signed overflow is UNDEFINED BEHAVIOR
    std::cout << "Signed underflow: UNDEFINED BEHAVIOR" << std::endl;

    // 2. COMPARISON PITFALLS
    int signed_value = -1;
    unsigned int unsigned_value = 100;
    
    // Dangerous comparison: signed gets converted to unsigned!
    if (signed_value < unsigned_value) {
        std::cout << "\n-1 < 100? You'd think so, but..." << std::endl;
    }
    
    // What actually happens:
    std::cout << "-1 as unsigned: " << (unsigned int)signed_value 
              << " (that's " << std::hex << (unsigned int)signed_value 
              << " in hex)" << std::dec << std::endl;
    
    // 3. BIT REPRESENTATION
    signed char s_char = -5;
    unsigned char u_char = 251;  // Same bit pattern as -5 in signed char
    
    std::cout << "\nSame bits, different interpretation:" << std::endl;
    std::cout << "signed char -5:   bits = " 
              << std::bitset<8>(*reinterpret_cast<unsigned char*>(&s_char)) << std::endl;
    std::cout << "unsigned char 251: bits = " 
              << std::bitset<8>(u_char) << std::endl;

    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    // Use unsigned for:
    // 1. Bit manipulation
    unsigned int flags = 0x0F;  // Hexadecimal for bit flags
    
    // 2. Array indices and sizes (size_t is unsigned)
    size_t array_size = 100;  // size_t is platform-dependent unsigned type
    
    // 3. When you truly need the full positive range
    unsigned int pixel_value = 255;  // RGB values 0-255
    
    // Use signed for:
    // 1. General arithmetic (avoids unexpected conversions)
    // 2. Values that could be negative
    
    // ============ TYPE ALIASES ============
    // Fixed-width integers (C++11)
    std::int8_t fixed_signed;    // Exactly 8 bits signed
    std::uint32_t fixed_unsigned; // Exactly 32 bits unsigned
    std::cout << "\nFixed width types ensure portability" << std::endl;
}

int main() {
    demonstrate_signed_unsigned();
    return 0;
}


////////* ENUMS *////////

#include <iostream>
#include <type_traits>

// ============ OLD-STYLE ENUM (C++98) ============
namespace OldStyle {
    // Traditional enum - unscoped, pollutes surrounding namespace
    enum Color {
        RED,    // 0
        GREEN,  // 1
        BLUE    // 2
        // Values automatically assigned starting from 0
    };
    
    // Can specify values explicitly
    enum HttpStatus {
        OK = 200,
        CREATED = 201,
        BAD_REQUEST = 400,
        NOT_FOUND = 404,
        SERVER_ERROR = 500
    };
    
    // Problem: names are in the surrounding scope
    enum TrafficLight {
        RED,    // ERROR: RED already defined in Color!
        YELLOW, // Would be 1
        GREEN   // ERROR: GREEN already defined!
    };
}

// ============ ENUM WITH EXPLICIT SCOPE ============
namespace Workaround {
    // Old workaround: put enums in namespaces or prefix names
    enum Color {
        COLOR_RED,
        COLOR_GREEN,
        COLOR_BLUE
    };
    
    enum TrafficLight {
        LIGHT_RED,
        LIGHT_YELLOW,
        LIGHT_GREEN
    };
}

// ============ ENUM CLASS (C++11) ============
namespace Modern {
    // Strongly typed, scoped enumeration
    enum class Color {
        RED,    // Modern::Color::RED
        GREEN,  // Modern::Color::GREEN
        BLUE    // Modern::Color::BLUE
    };
    
    // No naming conflicts!
    enum class TrafficLight {
        RED,    // Modern::TrafficLight::RED
        YELLOW, // Modern::TrafficLight::YELLOW
        GREEN   // Modern::TrafficLight::GREEN
    };
    
    // Can specify underlying type (default is int)
    enum class Byte : unsigned char {
        ZERO = 0,
        MAX = 255
    };
    
    // Can specify values explicitly
    enum class Permission : uint8_t {
        READ = 0b0001,   // Binary literals (C++14)
        WRITE = 0b0010,
        EXECUTE = 0b0100,
        ALL = READ | WRITE | EXECUTE
    };
}

void demonstrate_enums() {
    std::cout << "============ ENUM vs ENUM CLASS ============\n" << std::endl;
    
    // ============ OLD-STYLE ENUM USAGE ============
    std::cout << "=== Old-style enum (C++98) ===" << std::endl;
    
    OldStyle::Color old_color = OldStyle::RED;  // No scope resolution needed
    std::cout << "Old color: " << old_color << std::endl;  // Prints as integer
    
    // Problems with old enums:
    // 1. Implicit conversion to int
    int color_value = old_color;  // No error - implicit conversion
    std::cout << "Color as int: " << color_value << std::endl;
    
    // 2. Can compare with ints
    if (old_color == 0) {  // RED is 0
        std::cout << "Color is RED (compared to 0)" << std::endl;
    }
    
    // 3. Names pollute namespace (see above compilation errors)
    
    // ============ ENUM CLASS USAGE ============
    std::cout << "\n=== enum class (C++11) ===" << std::endl;
    
    Modern::Color modern_color = Modern::Color::RED;
    Modern::TrafficLight light = Modern::TrafficLight::RED;  // No conflict!
    
    // Benefits of enum class:
    // 1. Strongly typed - no implicit conversion to int
    // int modern_value = modern_color;  // ERROR: no implicit conversion
    
    // Must use static_cast for conversion
    int modern_value = static_cast<int>(modern_color);
    std::cout << "Modern color as int (explicit cast): " << modern_value << std::endl;
    
    // 2. Scope resolution required
    std::cout << "Cannot print directly: " 
              << static_cast<int>(modern_color) << std::endl;  // Must cast
    
    // 3. No accidental comparisons with ints
    // if (modern_color == 0) { }  // ERROR: no comparison with int
    
    // Must compare with same enum type
    if (modern_color == Modern::Color::RED) {
        std::cout << "Color is Modern::Color::RED" << std::endl;
    }
    
    // ============ TYPE SAFETY DEMONSTRATION ============
    std::cout << "\n=== Type Safety Example ===" << std::endl;
    
    // Dangerous with old enums
    OldStyle::Color c1 = OldStyle::RED;
    OldStyle::HttpStatus s1 = OldStyle::OK;
    
    // Compiles but semantically wrong!
    if (c1 == s1) {  // Comparing colors with HTTP statuses!
        std::cout << "RED == OK (200) ? This makes no sense but compiles!" << std::endl;
    }
    
    // Safe with enum class
    Modern::Color c2 = Modern::Color::RED;
    // Modern::Permission p2 = Modern::Permission::READ;
    
    // if (c2 == p2) { }  // ERROR: different enum classes
    
    // ============ UNDERLYING TYPE CONTROL ============
    std::cout << "\n=== Underlying Type Control ===" << std::endl;
    
    Modern::Byte b = Modern::Byte::MAX;
    std::cout << "Size of Byte enum: " << sizeof(Modern::Byte) << " bytes" << std::endl;
    std::cout << "Size of Color enum: " << sizeof(Modern::Color) << " bytes" << std::endl;
    
    // Check underlying type with type traits
    std::cout << "Byte underlying type is unsigned char: "
              << std::is_same_v<std::underlying_type_t<Modern::Byte>, unsigned char>
              << std::endl;
    
    // ============ BIT FLAGS WITH ENUM CLASS ============
    std::cout << "\n=== Bit Flags Example ===" << std::endl;
    
    using Modern::Permission;
    Permission user_perms = Permission::READ;
    
    // Add permissions
    user_perms = static_cast<Permission>(
        static_cast<uint8_t>(user_perms) | 
        static_cast<uint8_t>(Permission::WRITE)
    );
    
    // Check permission
    bool can_write = (static_cast<uint8_t>(user_perms) & 
                     static_cast<uint8_t>(Permission::WRITE)) != 0;
    
    std::cout << "User can write: " << std::boolalpha << can_write << std::endl;
    
    // More readable with helper functions
    auto add_permission = [](Permission& perms, Permission p) {
        perms = static_cast<Permission>(
            static_cast<uint8_t>(perms) | static_cast<uint8_t>(p)
        );
    };
    
    auto has_permission = [](Permission perms, Permission p) -> bool {
        return (static_cast<uint8_t>(perms) & static_cast<uint8_t>(p)) != 0;
    };
    
    Permission admin_perms = Permission::READ;
    add_permission(admin_perms, Permission::WRITE);
    add_permission(admin_perms, Permission::EXECUTE);
    
    std::cout << "Admin has all permissions: " 
              << has_permission(admin_perms, Permission::ALL) << std::endl;
    
    // ============ ITERATING OVER ENUMS ============
    std::cout << "\n=== Iterating Over Enum Values ===" << std::endl;
    
    // Enums don't have built-in iteration, but we can create arrays
    constexpr Modern::Color all_colors[] = {
        Modern::Color::RED,
        Modern::Color::GREEN,
        Modern::Color::BLUE
    };
    
    std::cout << "All colors: ";
    for (auto color : all_colors) {
        std::cout << static_cast<int>(color) << " ";
    }
    std::cout << std::endl;
    
    // ============ ENUM BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    
    // ALWAYS prefer enum class over old enum
    // Reasons:
    // 1. Type safety
    // 2. No namespace pollution
    // 3. Clear scope resolution
    // 4. Can specify underlying type
    
    // Only use old enum for:
    // 1. Legacy code maintenance
    // 2. C interoperability
    // 3. When you NEED implicit conversion to int
    
    // Consider using enum class even for bit flags
    // (use helper functions for bit operations)
}

// ============ ADVANCED ENUM TECHNIQUES ============
namespace Advanced {
    // Enum with methods using operator overloading
    enum class FileMode {
        READ = 1,
        WRITE = 2,
        APPEND = 4,
        BINARY = 8
    };
    
    // Overload operators for enum class
    inline FileMode operator|(FileMode a, FileMode b) {
        return static_cast<FileMode>(
            static_cast<int>(a) | static_cast<int>(b)
        );
    }
    
    inline FileMode operator&(FileMode a, FileMode b) {
        return static_cast<FileMode>(
            static_cast<int>(a) & static_cast<int>(b)
        );
    }
    
    inline FileMode& operator|=(FileMode& a, FileMode b) {
        a = a | b;
        return a;
    }
    
    inline bool operator!(FileMode a) {
        return static_cast<int>(a) == 0;
    }
}

void demonstrate_advanced_enums() {
    std::cout << "\n=== Advanced Enum Techniques ===" << std::endl;
    
    using Advanced::FileMode;
    
    FileMode mode = FileMode::READ | FileMode::WRITE;
    
    if (static_cast<int>(mode & FileMode::WRITE) != 0) {
        std::cout << "File opened in write mode" << std::endl;
    }
    
    mode |= FileMode::BINARY;
    std::cout << "Added binary mode" << std::endl;
}

int main() {
    demonstrate_enums();
    demonstrate_advanced_enums();
    return 0;
}