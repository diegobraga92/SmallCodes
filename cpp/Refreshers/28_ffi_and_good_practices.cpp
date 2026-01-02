// API.hpp - Header file showing API changes
#pragma once
#include <string>
#include <vector>

// API Version 1.0 - Initial release
namespace MyLib {
    // Original class interface
    class DataProcessor {
    public:
        DataProcessor();
        
        // API v1.0 methods
        std::string process(const std::string& input);
        int calculate(int x, int y);
        
        // API BREAKING CHANGES:
        // 1. Changing return type (breaks source compatibility)
        // std::vector<char> process(const std::string& input); // BREAKING!
        
        // 2. Changing parameter types (breaks source compatibility)
        // int calculate(double x, double y); // BREAKING!
        
        // 3. Removing methods (breaks source compatibility)
        // (Don't remove existing methods)
        
        // 4. Changing method signatures (breaks source compatibility)
        // std::string process(const std::string& input, bool flag); // BREAKING!
    };
}

// API Version 1.1 - Backward compatible additions
namespace MyLib {
    // Same class with new methods (API compatible)
    class DataProcessor {
    public:
        DataProcessor();
        
        // Original methods remain unchanged
        std::string process(const std::string& input);
        int calculate(int x, int y);
        
        // NEW in v1.1 (API compatible)
        std::vector<int> batchProcess(const std::vector<std::string>& inputs);
        
        // Method overloading (API compatible)
        double calculate(double x, double y);
    };
}

// API Version 2.0 - Breaking changes
namespace MyLib {
    namespace v2 {  // New namespace for major version
        class DataProcessor {
        public:
            DataProcessor();
            
            // Breaking changes in new namespace
            std::vector<uint8_t> process(const std::string& input, Encoding encoding);
            double calculate(double x, double y, CalculationMode mode);
        };
    }
    
    // Keep v1.0 for backward compatibility
    namespace v1 = MyLib;  // Alias for v1 API
}

// Using API versioning
void demonstrateAPIUsage() {
    // Using v1.0 API
    MyLib::DataProcessor proc1;
    auto result1 = proc1.process("input");
    
    // Using v2.0 API (explicit)
    MyLib::v2::DataProcessor proc2;
    auto result2 = proc2.process("input", MyLib::v2::Encoding::UTF8);
    
    // API compatibility means source code using v1.0
    // should still compile with v2.0 headers (if using v1 namespace)
}



// ABI stability concerns - What breaks binary compatibility
class ABI_Examples {
    // ABI Version 1.0
    class Widget_v1 {
    private:
        int id;           // Offset 0
        std::string name; // Offset 8 (assuming 8-byte alignment)
        double value;     // Offset 40 (string size varies!)
    public:
        virtual void process();  // vtable entry 0
    };
    
    // ABI BREAKING CHANGES:
    
    // 1. Adding new data members changes object layout
    class Widget_v2_BROKEN {
    private:
        int id;
        std::string name;
        double value;
        bool enabled;  // NEW: Changes size and layout! (ABI BREAK)
    public:
        virtual void process();
    };
    
    // 2. Changing virtual function order
    class Widget_v3_BROKEN {
    private:
        int id;
        std::string name;
        double value;
    public:
        virtual void initialize();  // NEW at vtable[0] - BREAKS ABI!
        virtual void process();     // Now at vtable[1] - BREAKS ABI!
    };
    
    // 3. Adding virtual functions (if not at end)
    class Widget_v4_BROKEN {
    private:
        int id;
        std::string name;
        double value;
    public:
        virtual void process();
        virtual void cleanup();  // Adding virtual function BREAKS ABI
                                 // unless compiler uses thunks (not guaranteed)
    };
    
    // ABI SAFE CHANGES:
    
    // 1. Adding non-virtual functions (safe)
    class Widget_v5_SAFE {
    private:
        int id;
        std::string name;
        double value;
    public:
        virtual void process();
        // SAFE: Non-virtual functions don't affect ABI
        void newHelperFunction();
    };
    
    // 2. Adding static members (safe)
    class Widget_v6_SAFE {
    private:
        int id;
        std::string name;
        double value;
        static int instanceCount;  // SAFE: Static members not in object layout
    public:
        virtual void process();
    };
    
    // 3. Using PIMPL to hide implementation details
    class Widget_v7_SAFE {
    private:
        class Impl;  // Forward declaration
        std::unique_ptr<Impl> pImpl;  // Fixed size pointer
    public:
        Widget_v7_SAFE();
        ~Widget_v7_SAFE();
        virtual void process();
        // Can change Impl class without breaking ABI
    };
};

// Demonstrating ABI issues practically
void demonstrateABIIssues() {
    // Suppose library v1.0 creates this object
    Widget_v1* widget = createWidget();  // Returns Widget_v1*
    
    // If we upgrade to library v2.0 without recompiling:
    // widget->process();  // CRASH! Wrong vtable layout
    //                  // Or memory corruption due to size mismatch
}



// C ABI is simple and stable
// clib.h - C interface
#ifndef CLIB_H
#define CLIB_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// C has no name mangling - simple function names
// Function: calculate_sum
void* create_context(int initial_value);
int calculate_sum(void* context, int a, int b);
void destroy_context(void* context);

// Simple struct with explicit padding
#pragma pack(push, 1)  // No padding for network transmission
typedef struct {
    int32_t x;
    int32_t y;
    uint8_t flags;      // Explicit byte for flags
    uint8_t padding[3]; // Explicit padding for alignment
} Point;
#pragma pack(pop)

// C enums are just integers
typedef enum {
    MODE_A = 0,
    MODE_B = 1,
    MODE_C = 2
} OperationMode;

// Function pointer type - simple ABI
typedef int (*Callback)(int value, void* user_data);

// Register callback with user data
void register_callback(Callback cb, void* user_data);

#ifdef __cplusplus
}
#endif

#endif // CLIB_H

// clib.c - C implementation
#include "clib.h"

struct Context {
    int value;
    Callback cb;
    void* user_data;
};

void* create_context(int initial_value) {
    struct Context* ctx = malloc(sizeof(struct Context));
    ctx->value = initial_value;
    ctx->cb = NULL;
    ctx->user_data = NULL;
    return ctx;
}

int calculate_sum(void* context, int a, int b) {
    struct Context* ctx = (struct Context*)context;
    int result = a + b + ctx->value;
    
    // Call callback if registered
    if (ctx->cb) {
        result = ctx->cb(result, ctx->user_data);
    }
    
    return result;
}

void destroy_context(void* context) {
    free(context);
}

void register_callback(void* context, Callback cb, void* user_data) {
    struct Context* ctx = (struct Context*)context;
    ctx->cb = cb;
    ctx->user_data = user_data;
}



// C++ ABI is complex due to language features
// cpplib.h - C++ interface (complex ABI)
#pragma once
#include <string>
#include <vector>
#include <memory>

namespace CppLib {

// C++ name mangling example
// Function: calculate_sum<int, double> becomes something like:
// _ZN6CppLib13calculate_sumIidEEiT_T0_ (GCC/Itanium)
// ?calculate_sum@CppLib@@YAHHN@Z (MSVC)

class ComplexObject {
private:
    std::string name;
    std::vector<int> data;
    double* dynamic_array;
    
public:
    ComplexObject(const std::string& name);
    virtual ~ComplexObject();  // Virtual function - vtable
    
    // Virtual functions affect ABI
    virtual void process();
    virtual int calculate() const;
    
    // Template methods - instantiated at compile time
    template<typename T>
    T transform(T value) {
        return value * 2;  // Inline code in header
    }
    
    // Exception specifications affect ABI
    void riskyOperation() noexcept(false);
    
    // RTTI (Run-Time Type Information)
    virtual const char* typeName() const;
};

// Template classes - all code in headers
template<typename T>
class Container {
private:
    std::vector<T> items;
    
public:
    void add(const T& item) {
        items.push_back(item);
    }
    
    T& get(size_t index) {
        return items.at(index);
    }
    
    size_t size() const {
        return items.size();
    }
};

// Inline functions in headers
inline int helper_function(int x, int y) {
    return x * y + 42;
}

// C++ ABI issues:
// 1. Different compilers = different name mangling
// 2. Different stdlib implementations = different layouts
// 3. Virtual function order matters
// 4. Exception handling implementation differs
// 5. RTTI implementation differs

} // namespace CppLib

// cpplib.cpp - C++ implementation
#include "cpplib.h"
#include <typeinfo>

namespace CppLib {

ComplexObject::ComplexObject(const std::string& name) 
    : name(name), dynamic_array(new double[100]) {
    // Complex initialization
}

ComplexObject::~ComplexObject() {
    delete[] dynamic_array;
}

void ComplexObject::process() {
    // Implementation
}

int ComplexObject::calculate() const {
    return data.size() * 42;
}

void ComplexObject::riskyOperation() {
    throw std::runtime_error("This might fail");
}

const char* ComplexObject::typeName() const {
    return typeid(*this).name();  // RTTI usage
}

} // namespace CppLib

// Using C++ library from different compiler = ABI incompatibility
void demonstrateCppABIProblems() {
    // Compiled with GCC:
    // ComplexObject* obj = createObject();
    
    // Linked with MSVC-built library:
    // obj->process();  // CRASH! Different vtable layout
    //               // Different name mangling
    //               // Different exception handling
}


// header_only.hpp - Complete library in single header
#pragma once

// Use include guards for portability
#ifndef HEADER_ONLY_LIB_HPP
#define HEADER_ONLY_LIB_HPP

#include <vector>
#include <algorithm>
#include <numeric>
#include <type_traits>

namespace HeaderOnlyLib {

// All code is inline/template - no separate compilation needed

// Utility functions (marked inline)
template<typename T>
inline T clamp(T value, T min, T max) {
    return (value < min) ? min : (value > max) ? max : value;
}

// Template classes (all code in header)
template<typename T, size_t N>
class CircularBuffer {
private:
    T buffer[N];
    size_t head = 0;
    size_t tail = 0;
    size_t count = 0;
    
public:
    bool push(const T& item) {
        if (count == N) return false;
        buffer[tail] = item;
        tail = (tail + 1) % N;
        ++count;
        return true;
    }
    
    bool pop(T& item) {
        if (count == 0) return false;
        item = buffer[head];
        head = (head + 1) % N;
        --count;
        return true;
    }
    
    size_t size() const { return count; }
    bool empty() const { return count == 0; }
    bool full() const { return count == N; }
};

// CRTP (Curiously Recurring Template Pattern)
template<typename Derived>
class Singleton {
protected:
    Singleton() = default;
    ~Singleton() = default;
    
public:
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
    static Derived& instance() {
        static Derived instance;
        return instance;
    }
};

// Configuration manager using Singleton
class ConfigManager : public Singleton<ConfigManager> {
private:
    friend class Singleton<ConfigManager>;
    ConfigManager() {}  // Private constructor
    
    std::unordered_map<std::string, std::string> settings;
    
public:
    void set(const std::string& key, const std::string& value) {
        settings[key] = value;
    }
    
    std::string get(const std::string& key, 
                   const std::string& defaultValue = "") const {
        auto it = settings.find(key);
        return it != settings.end() ? it->second : defaultValue;
    }
};

// Constexpr functions (compile-time computation)
constexpr int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n - 1);
}

// Type traits and metaprogramming
template<typename T>
struct is_pointer_helper : std::false_type {};

template<typename T>
struct is_pointer_helper<T*> : std::true_type {};

template<typename T>
constexpr bool is_pointer = is_pointer_helper<T>::value;

} // namespace HeaderOnlyLib

#endif // HEADER_ONLY_LIB_HPP

// Usage example
void useHeaderOnlyLibrary() {
    // No linking required - just include
    using namespace HeaderOnlyLib;
    
    // Template instantiation happens at compile time
    CircularBuffer<int, 100> buffer;
    buffer.push(42);
    
    // Singleton usage
    ConfigManager::instance().set("timeout", "1000");
    
    // Constexpr computation at compile time
    constexpr int fact10 = factorial(10);  // Computed at compile time
    
    // Type trait usage
    static_assert(is_pointer<int*> == true, "Should be pointer");
    static_assert(is_pointer<int> == false, "Should not be pointer");
}

// Pros of header-only libraries:
// 1. No ABI issues (all code compiled with user's compiler)
// 2. Easy deployment (single header file)
// 3. Better optimization (inlining across translation units)
// 4. Template metaprogramming works naturally

// Cons:
// 1. Longer compile times (code compiled in every TU)
// 2. Larger binaries (code duplication)
// 3. No implementation hiding
// 4. Can't precompile


// compiled_lib.h - Header for compiled library
#pragma once

// Use dllexport/dllimport for Windows
#ifdef COMPILED_LIB_EXPORTS
    #define COMPILED_API __declspec(dllexport)
#else
    #define COMPILED_API __declspec(dllimport)
#endif

// Or use visibility attributes for GCC/Clang
#ifdef __GNUC__
    #define COMPILED_API __attribute__((visibility("default")))
#else
    #define COMPILED_API
#endif

namespace CompiledLib {

// Forward declarations to hide implementation
class DataProcessorImpl;

// Public interface
class COMPILED_API DataProcessor {
private:
    DataProcessorImpl* pImpl;  // PIMPL pattern
    
public:
    DataProcessor();
    ~DataProcessor();
    
    // Non-copyable to avoid ABI issues with implicit members
    DataProcessor(const DataProcessor&) = delete;
    DataProcessor& operator=(const DataProcessor&) = delete;
    
    // Movable
    DataProcessor(DataProcessor&&) noexcept;
    DataProcessor& operator=(DataProcessor&&) noexcept;
    
    // Public API
    void processData(const std::vector<int>& input);
    std::vector<int> getResults() const;
    int calculate(int x, int y);
    
    // Factory function (C linkage for easier loading)
    static DataProcessor* create();
    static void destroy(DataProcessor* processor);
};

// C interface for maximum compatibility
extern "C" {
    COMPILED_API void* create_processor();
    COMPILED_API void process_data(void* processor, const int* data, size_t size);
    COMPILED_API void destroy_processor(void* processor);
}

} // namespace CompiledLib

// compiled_lib.cpp - Implementation
#include "compiled_lib.h"
#include <vector>
#include <algorithm>
#include <numeric>

// Private implementation class
class CompiledLib::DataProcessorImpl {
private:
    std::vector<int> buffer;
    int offset;
    
public:
    DataProcessorImpl() : offset(0) {}
    
    void process(const std::vector<int>& input) {
        buffer.resize(input.size());
        std::transform(input.begin(), input.end(), buffer.begin(),
                      [this](int x) { return x + offset; });
        offset += 10;
    }
    
    std::vector<int> getResults() const {
        return buffer;
    }
    
    int calculate(int x, int y) {
        return x * y + offset;
    }
};

// Public class implementation
CompiledLib::DataProcessor::DataProcessor() 
    : pImpl(new DataProcessorImpl()) {}

CompiledLib::DataProcessor::~DataProcessor() {
    delete pImpl;
}

CompiledLib::DataProcessor::DataProcessor(DataProcessor&& other) noexcept 
    : pImpl(other.pImpl) {
    other.pImpl = nullptr;
}

CompiledLib::DataProcessor& CompiledLib::DataProcessor::operator=(DataProcessor&& other) noexcept {
    if (this != &other) {
        delete pImpl;
        pImpl = other.pImpl;
        other.pImpl = nullptr;
    }
    return *this;
}

void CompiledLib::DataProcessor::processData(const std::vector<int>& input) {
    pImpl->process(input);
}

std::vector<int> CompiledLib::DataProcessor::getResults() const {
    return pImpl->getResults();
}

int CompiledLib::DataProcessor::calculate(int x, int y) {
    return pImpl->calculate(x, y);
}

CompiledLib::DataProcessor* CompiledLib::DataProcessor::create() {
    return new DataProcessor();
}

void CompiledLib::DataProcessor::destroy(DataProcessor* processor) {
    delete processor;
}

// C interface implementation
extern "C" {
    COMPILED_API void* create_processor() {
        return new CompiledLib::DataProcessor();
    }
    
    COMPILED_API void process_data(void* processor, const int* data, size_t size) {
        auto* proc = static_cast<CompiledLib::DataProcessor*>(processor);
        std::vector<int> vec(data, data + size);
        proc->processData(vec);
    }
    
    COMPILED_API void destroy_processor(void* processor) {
        delete static_cast<CompiledLib::DataProcessor*>(processor);
    }
}

// Building the library:
// Linux: g++ -fPIC -shared -o libcompiled.so compiled_lib.cpp -DCOMPILED_LIB_EXPORTS
// Windows: cl /LD compiled_lib.cpp /DCOMPILED_LIB_EXPORTS
// macOS: clang++ -dynamiclib -o libcompiled.dylib compiled_lib.cpp -DCOMPILED_LIB_EXPORTS

// Pros of compiled libraries:
// 1. Faster compilation (library precompiled)
// 2. Smaller binaries (code not duplicated)
// 3. Implementation hiding
// 4. Can use compiler-specific optimizations

// Cons:
// 1. ABI issues (must match compiler/version)
// 2. Deployment complexity (need to ship .so/.dll/.dylib)
// 3. Versioning complexity
// 4. Linker issues


// versioning.hpp - Comprehensive versioning strategies
#pragma once
#include <string>
#include <cstdint>
#include <type_traits>

// ===================== SEMANTIC VERSIONING =====================
struct SemanticVersion {
    uint32_t major;
    uint32_t minor;
    uint32_t patch;
    std::string prerelease;  // "alpha", "beta", "rc.1"
    std::string build;       // "build123", "githash"
    
    // Parse from string
    static SemanticVersion parse(const std::string& versionStr) {
        SemanticVersion version{0, 0, 0, "", ""};
        
        size_t plusPos = versionStr.find('+');
        size_t dashPos = versionStr.find('-');
        
        std::string core = versionStr;
        if (plusPos != std::string::npos) {
            version.build = versionStr.substr(plusPos + 1);
            core = versionStr.substr(0, plusPos);
        }
        if (dashPos != std::string::npos) {
            version.prerelease = core.substr(dashPos + 1);
            core = core.substr(0, dashPos);
        }
        
        // Parse MAJOR.MINOR.PATCH
        size_t dot1 = core.find('.');
        size_t dot2 = core.rfind('.');
        
        if (dot1 != std::string::npos && dot2 != std::string::npos && dot1 != dot2) {
            version.major = std::stoul(core.substr(0, dot1));
            version.minor = std::stoul(core.substr(dot1 + 1, dot2 - dot1 - 1));
            version.patch = std::stoul(core.substr(dot2 + 1));
        }
        
        return version;
    }
    
    // Convert to string
    std::string toString() const {
        std::string result = std::to_string(major) + "." +
                            std::to_string(minor) + "." +
                            std::to_string(patch);
        if (!prerelease.empty()) {
            result += "-" + prerelease;
        }
        if (!build.empty()) {
            result += "+" + build;
        }
        return result;
    }
    
    // Comparison operators
    bool operator==(const SemanticVersion& other) const {
        return major == other.major &&
               minor == other.minor &&
               patch == other.patch &&
               prerelease == other.prerelease;
    }
    
    bool operator<(const SemanticVersion& other) const {
        if (major != other.major) return major < other.major;
        if (minor != other.minor) return minor < other.minor;
        if (patch != other.patch) return patch < other.patch;
        
        // Pre-release comparison (simplified)
        return prerelease < other.prerelease;
    }
    
    bool isCompatibleWith(const SemanticVersion& other) const {
        // Same major version means backward compatible
        return major == other.major && *this >= other;
    }
};

// ===================== ABI VERSIONING (SONAME) =====================
class ABIVersioning {
public:
    // Linux/Unix: libfoo.so.MAJOR.MINOR.PATCH
    // MAJOR in SONAME (libfoo.so.1) - ABI breaking changes
    // MINOR.PATCH for compatible changes
    
    static std::string getSharedObjectName(const std::string& baseName,
                                          const SemanticVersion& version) {
        // libmylib.so.1.2.3
        return baseName + ".so." + 
               std::to_string(version.major) + "." +
               std::to_string(version.minor) + "." +
               std::to_string(version.patch);
    }
    
    static std::string getSONAME(const std::string& baseName,
                                uint32_t majorVersion) {
        // libmylib.so.1 (linker uses this)
        return baseName + ".so." + std::to_string(majorVersion);
    }
    
    static bool isABICompatible(uint32_t compiledWithMajor,
                               uint32_t runtimeMajor) {
        // Same major version means ABI compatible
        return compiledWithMajor == runtimeMajor;
    }
};

// ===================== NAMESPACE VERSIONING =====================
namespace MyLibrary {
    // Version 1.0 API
    namespace v1 {
        class Processor {
        public:
            virtual ~Processor() = default;
            virtual std::string process(const std::string& input) = 0;
        };
        
        Processor* createProcessor();
        void destroyProcessor(Processor*);
    }
    
    // Version 2.0 API (breaking changes)
    namespace v2 {
        class Processor {
        public:
            virtual ~Processor() = default;
            virtual std::vector<uint8_t> process(const std::vector<uint8_t>& input) = 0;
            virtual void configure(const std::string& options) = 0;
        };
        
        std::unique_ptr<Processor> createProcessor();  // Smart pointer in v2
    }
    
    // Version 3.0 API (C++20 features)
    namespace v3 {
        template<typename T>
        concept Processable = requires(T t) {
            { t.data() } -> std::convertible_to<const std::byte*>;
            { t.size() } -> std::convertible_to<size_t>;
        };
        
        class Processor {
        public:
            virtual ~Processor() = default;
            
            template<Processable T>
            auto process(const T& input) {
                return processImpl(input.data(), input.size());
            }
            
        private:
            virtual std::vector<std::byte> processImpl(const std::byte* data, size_t size) = 0;
        };
        
        std::unique_ptr<Processor> createProcessor();
    }
    
    // Current version alias
    namespace current = v3;
    
    // Compatibility layer
    namespace compatibility {
        // Adapter from v1 to v3
        class V1ToV3Adapter : public v1::Processor {
        private:
            std::unique_ptr<v3::Processor> v3Processor;
            
        public:
            V1ToV3Adapter() : v3Processor(v3::createProcessor()) {}
            
            std::string process(const std::string& input) override {
                std::vector<std::byte> bytes(input.begin(), input.end());
                auto result = v3Processor->process(bytes);
                return std::string(result.begin(), result.end());
            }
        };
    }
}

// ===================== API VERSION MACROS =====================
#define MYLIB_VERSION_MAJOR 2
#define MYLIB_VERSION_MINOR 1
#define MYLIB_VERSION_PATCH 3
#define MYLIB_VERSION_STRING "2.1.3"

// Compile-time version checks
#if MYLIB_VERSION_MAJOR < 2
    #error "This library requires version 2.0 or higher"
#endif

// Feature detection based on version
#if MYLIB_VERSION_MAJOR >= 2 && MYLIB_VERSION_MINOR >= 1
    #define MYLIB_HAS_FEATURE_X 1
#else
    #define MYLIB_HAS_FEATURE_X 0
#endif

// ===================== RUNTIME VERSION QUERIES =====================
extern "C" {
    // C interface for version queries
    const char* get_version_string();
    int get_version_major();
    int get_version_minor();
    int get_version_patch();
    
    // Check compatibility
    int check_compatibility(int required_major, int required_minor);
}

// ===================== VERSIONED SYMBOLS =====================
// Using GNU extension for versioned symbols
#ifdef __GNUC__
    #define EXPORT_SYMBOL_VERSION(return_type, name, version_string) \
        extern "C" return_type name ## _ ## version_string() __attribute__((alias(#name))); \
        __asm__(".symver " #name "_" #version_string ", " #name "@" version_string)
#else
    #define EXPORT_SYMBOL_VERSION(return_type, name, version_string)
#endif

// Example of versioned symbols
extern "C" {
    void process_data_v1(int* data, int size);
    void process_data_v2(int* data, int size, int options);
}

// In implementation:
// EXPORT_SYMBOL_VERSION(void, process_data, "VERSION_1.0");
// EXPORT_SYMBOL_VERSION(void, process_data, "VERSION_2.0");

// ===================== DEPRECATION WARNINGS =====================
#if defined(__GNUC__) || defined(__clang__)
    #define DEPRECATED(msg) __attribute__((deprecated(msg)))
#elif defined(_MSC_VER)
    #define DEPRECATED(msg) __declspec(deprecated(msg))
#else
    #define DEPRECATED(msg)
#endif

class VersionedAPI {
public:
    // Old API - deprecated
    DEPRECATED("Use newProcess() instead")
    void oldProcess();
    
    // New API
    void newProcess();
    
    // Version-specific implementation
#if MYLIB_VERSION_MAJOR >= 2
    void featureOnlyInV2();
#endif
};

// ===================== VERSIONED DATA STRUCTURES =====================
#pragma pack(push, 1)
struct MessageHeader {
    uint32_t version;  // Protocol version
    uint32_t size;     // Message size
    uint32_t type;     // Message type
    uint32_t checksum; // Data integrity
};

// Version 1.0 message format
struct MessageV1 {
    MessageHeader header;
    char data[256];  // Fixed size
};

// Version 2.0 message format (extended)
struct MessageV2 {
    MessageHeader header;
    uint32_t flags;      // New in v2
    uint64_t timestamp;  // New in v2
    char data[];         // Flexible array member
};
#pragma pack(pop)

class MessageProcessor {
public:
    static void* parseMessage(const void* data, size_t size) {
        const MessageHeader* header = static_cast<const MessageHeader*>(data);
        
        switch (header->version) {
            case 1:
                return parseV1Message(data, size);
            case 2:
                return parseV2Message(data, size);
            default:
                throw std::runtime_error("Unsupported message version");
        }
    }
    
private:
    static void* parseV1Message(const void* data, size_t size) {
        if (size < sizeof(MessageV1)) {
            throw std::runtime_error("Message too small for v1");
        }
        // Parse v1 message
        return nullptr;
    }
    
    static void* parseV2Message(const void* data, size_t size) {
        const MessageV2* msg = static_cast<const MessageV2*>(data);
        if (size < sizeof(MessageV2)) {
            throw std::runtime_error("Message too small for v2");
        }
        // Parse v2 message
        return nullptr;
    }
};

// ===================== BUILD VERSION INTEGRATION =====================
// Generated by build system
#ifndef BUILD_VERSION
    #define BUILD_VERSION "custom"
#endif

#ifndef BUILD_TIMESTAMP
    #define BUILD_TIMESTAMP __DATE__ " " __TIME__
#endif

#ifndef GIT_COMMIT_HASH
    #define GIT_COMMIT_HASH "unknown"
#endif

struct BuildInfo {
    static const char* version() { return MYLIB_VERSION_STRING; }
    static const char* buildVersion() { return BUILD_VERSION; }
    static const char* buildTimestamp() { return BUILD_TIMESTAMP; }
    static const char* gitCommit() { return GIT_COMMIT_HASH; }
    
    static void printInfo() {
        std::cout << "Library Version: " << version() << "\n"
                  << "Build Version: " << buildVersion() << "\n"
                  << "Build Time: " << buildTimestamp() << "\n"
                  << "Git Commit: " << gitCommit() << "\n";
    }
};

// ===================== VERSION POLICY ENFORCEMENT =====================
class VersionPolicy {
public:
    // Check if current version satisfies requirement
    static bool satisfies(const std::string& requirement) {
        // Supports: ">=2.0.0", "<3.0.0", "^2.1.0", "~2.1.0"
        auto current = SemanticVersion::parse(MYLIB_VERSION_STRING);
        auto req = parseRequirement(requirement);
        
        return checkRequirement(current, req);
    }
    
    // Enforce version requirement at runtime
    static void enforce(const std::string& requirement) {
        if (!satisfies(requirement)) {
            throw std::runtime_error(
                "Version requirement not satisfied: " + requirement +
                " (current: " + MYLIB_VERSION_STRING + ")"
            );
        }
    }
    
private:
    struct VersionRequirement {
        enum class Op { EQ, NE, GT, GE, LT, LE, TILDE, CARET } op;
        SemanticVersion version;
    };
    
    static VersionRequirement parseRequirement(const std::string& req) {
        // Simplified parser
        // Real implementation would use proper parsing
        return VersionRequirement{VersionRequirement::Op::GE, 
                                 SemanticVersion::parse("2.0.0")};
    }
    
    static bool checkRequirement(const SemanticVersion& current,
                                const VersionRequirement& req) {
        switch (req.op) {
            case VersionRequirement::Op::GE:
                return !(current < req.version);
            // Handle other operators
            default:
                return true;
        }
    }
};

// Usage example
void demonstrateVersioning() {
    // Semantic versioning
    auto version = SemanticVersion::parse("2.1.3-beta+build123");
    std::cout << "Version: " << version.toString() << "\n";
    
    // Namespace versioning
    {
        using namespace MyLibrary::v2;
        auto processor = createProcessor();
        processor->configure("options");
    }
    
    // Runtime version check
    if (check_compatibility(2, 0)) {
        std::cout << "Compatible with 2.0+\n";
    }
    
    // Version policy
    VersionPolicy::enforce(">=2.0.0 <3.0.0");
    
    // Build info
    BuildInfo::printInfo();
}



// versioning.hpp - Comprehensive versioning strategies
#pragma once
#include <string>
#include <cstdint>
#include <type_traits>

// ===================== SEMANTIC VERSIONING =====================
struct SemanticVersion {
    uint32_t major;
    uint32_t minor;
    uint32_t patch;
    std::string prerelease;  // "alpha", "beta", "rc.1"
    std::string build;       // "build123", "githash"
    
    // Parse from string
    static SemanticVersion parse(const std::string& versionStr) {
        SemanticVersion version{0, 0, 0, "", ""};
        
        size_t plusPos = versionStr.find('+');
        size_t dashPos = versionStr.find('-');
        
        std::string core = versionStr;
        if (plusPos != std::string::npos) {
            version.build = versionStr.substr(plusPos + 1);
            core = versionStr.substr(0, plusPos);
        }
        if (dashPos != std::string::npos) {
            version.prerelease = core.substr(dashPos + 1);
            core = core.substr(0, dashPos);
        }
        
        // Parse MAJOR.MINOR.PATCH
        size_t dot1 = core.find('.');
        size_t dot2 = core.rfind('.');
        
        if (dot1 != std::string::npos && dot2 != std::string::npos && dot1 != dot2) {
            version.major = std::stoul(core.substr(0, dot1));
            version.minor = std::stoul(core.substr(dot1 + 1, dot2 - dot1 - 1));
            version.patch = std::stoul(core.substr(dot2 + 1));
        }
        
        return version;
    }
    
    // Convert to string
    std::string toString() const {
        std::string result = std::to_string(major) + "." +
                            std::to_string(minor) + "." +
                            std::to_string(patch);
        if (!prerelease.empty()) {
            result += "-" + prerelease;
        }
        if (!build.empty()) {
            result += "+" + build;
        }
        return result;
    }
    
    // Comparison operators
    bool operator==(const SemanticVersion& other) const {
        return major == other.major &&
               minor == other.minor &&
               patch == other.patch &&
               prerelease == other.prerelease;
    }
    
    bool operator<(const SemanticVersion& other) const {
        if (major != other.major) return major < other.major;
        if (minor != other.minor) return minor < other.minor;
        if (patch != other.patch) return patch < other.patch;
        
        // Pre-release comparison (simplified)
        return prerelease < other.prerelease;
    }
    
    bool isCompatibleWith(const SemanticVersion& other) const {
        // Same major version means backward compatible
        return major == other.major && *this >= other;
    }
};

// ===================== ABI VERSIONING (SONAME) =====================
class ABIVersioning {
public:
    // Linux/Unix: libfoo.so.MAJOR.MINOR.PATCH
    // MAJOR in SONAME (libfoo.so.1) - ABI breaking changes
    // MINOR.PATCH for compatible changes
    
    static std::string getSharedObjectName(const std::string& baseName,
                                          const SemanticVersion& version) {
        // libmylib.so.1.2.3
        return baseName + ".so." + 
               std::to_string(version.major) + "." +
               std::to_string(version.minor) + "." +
               std::to_string(version.patch);
    }
    
    static std::string getSONAME(const std::string& baseName,
                                uint32_t majorVersion) {
        // libmylib.so.1 (linker uses this)
        return baseName + ".so." + std::to_string(majorVersion);
    }
    
    static bool isABICompatible(uint32_t compiledWithMajor,
                               uint32_t runtimeMajor) {
        // Same major version means ABI compatible
        return compiledWithMajor == runtimeMajor;
    }
};

// ===================== NAMESPACE VERSIONING =====================
namespace MyLibrary {
    // Version 1.0 API
    namespace v1 {
        class Processor {
        public:
            virtual ~Processor() = default;
            virtual std::string process(const std::string& input) = 0;
        };
        
        Processor* createProcessor();
        void destroyProcessor(Processor*);
    }
    
    // Version 2.0 API (breaking changes)
    namespace v2 {
        class Processor {
        public:
            virtual ~Processor() = default;
            virtual std::vector<uint8_t> process(const std::vector<uint8_t>& input) = 0;
            virtual void configure(const std::string& options) = 0;
        };
        
        std::unique_ptr<Processor> createProcessor();  // Smart pointer in v2
    }
    
    // Version 3.0 API (C++20 features)
    namespace v3 {
        template<typename T>
        concept Processable = requires(T t) {
            { t.data() } -> std::convertible_to<const std::byte*>;
            { t.size() } -> std::convertible_to<size_t>;
        };
        
        class Processor {
        public:
            virtual ~Processor() = default;
            
            template<Processable T>
            auto process(const T& input) {
                return processImpl(input.data(), input.size());
            }
            
        private:
            virtual std::vector<std::byte> processImpl(const std::byte* data, size_t size) = 0;
        };
        
        std::unique_ptr<Processor> createProcessor();
    }
    
    // Current version alias
    namespace current = v3;
    
    // Compatibility layer
    namespace compatibility {
        // Adapter from v1 to v3
        class V1ToV3Adapter : public v1::Processor {
        private:
            std::unique_ptr<v3::Processor> v3Processor;
            
        public:
            V1ToV3Adapter() : v3Processor(v3::createProcessor()) {}
            
            std::string process(const std::string& input) override {
                std::vector<std::byte> bytes(input.begin(), input.end());
                auto result = v3Processor->process(bytes);
                return std::string(result.begin(), result.end());
            }
        };
    }
}

// ===================== API VERSION MACROS =====================
#define MYLIB_VERSION_MAJOR 2
#define MYLIB_VERSION_MINOR 1
#define MYLIB_VERSION_PATCH 3
#define MYLIB_VERSION_STRING "2.1.3"

// Compile-time version checks
#if MYLIB_VERSION_MAJOR < 2
    #error "This library requires version 2.0 or higher"
#endif

// Feature detection based on version
#if MYLIB_VERSION_MAJOR >= 2 && MYLIB_VERSION_MINOR >= 1
    #define MYLIB_HAS_FEATURE_X 1
#else
    #define MYLIB_HAS_FEATURE_X 0
#endif

// ===================== RUNTIME VERSION QUERIES =====================
extern "C" {
    // C interface for version queries
    const char* get_version_string();
    int get_version_major();
    int get_version_minor();
    int get_version_patch();
    
    // Check compatibility
    int check_compatibility(int required_major, int required_minor);
}

// ===================== VERSIONED SYMBOLS =====================
// Using GNU extension for versioned symbols
#ifdef __GNUC__
    #define EXPORT_SYMBOL_VERSION(return_type, name, version_string) \
        extern "C" return_type name ## _ ## version_string() __attribute__((alias(#name))); \
        __asm__(".symver " #name "_" #version_string ", " #name "@" version_string)
#else
    #define EXPORT_SYMBOL_VERSION(return_type, name, version_string)
#endif

// Example of versioned symbols
extern "C" {
    void process_data_v1(int* data, int size);
    void process_data_v2(int* data, int size, int options);
}

// In implementation:
// EXPORT_SYMBOL_VERSION(void, process_data, "VERSION_1.0");
// EXPORT_SYMBOL_VERSION(void, process_data, "VERSION_2.0");

// ===================== DEPRECATION WARNINGS =====================
#if defined(__GNUC__) || defined(__clang__)
    #define DEPRECATED(msg) __attribute__((deprecated(msg)))
#elif defined(_MSC_VER)
    #define DEPRECATED(msg) __declspec(deprecated(msg))
#else
    #define DEPRECATED(msg)
#endif

class VersionedAPI {
public:
    // Old API - deprecated
    DEPRECATED("Use newProcess() instead")
    void oldProcess();
    
    // New API
    void newProcess();
    
    // Version-specific implementation
#if MYLIB_VERSION_MAJOR >= 2
    void featureOnlyInV2();
#endif
};

// ===================== VERSIONED DATA STRUCTURES =====================
#pragma pack(push, 1)
struct MessageHeader {
    uint32_t version;  // Protocol version
    uint32_t size;     // Message size
    uint32_t type;     // Message type
    uint32_t checksum; // Data integrity
};

// Version 1.0 message format
struct MessageV1 {
    MessageHeader header;
    char data[256];  // Fixed size
};

// Version 2.0 message format (extended)
struct MessageV2 {
    MessageHeader header;
    uint32_t flags;      // New in v2
    uint64_t timestamp;  // New in v2
    char data[];         // Flexible array member
};
#pragma pack(pop)

class MessageProcessor {
public:
    static void* parseMessage(const void* data, size_t size) {
        const MessageHeader* header = static_cast<const MessageHeader*>(data);
        
        switch (header->version) {
            case 1:
                return parseV1Message(data, size);
            case 2:
                return parseV2Message(data, size);
            default:
                throw std::runtime_error("Unsupported message version");
        }
    }
    
private:
    static void* parseV1Message(const void* data, size_t size) {
        if (size < sizeof(MessageV1)) {
            throw std::runtime_error("Message too small for v1");
        }
        // Parse v1 message
        return nullptr;
    }
    
    static void* parseV2Message(const void* data, size_t size) {
        const MessageV2* msg = static_cast<const MessageV2*>(data);
        if (size < sizeof(MessageV2)) {
            throw std::runtime_error("Message too small for v2");
        }
        // Parse v2 message
        return nullptr;
    }
};

// ===================== BUILD VERSION INTEGRATION =====================
// Generated by build system
#ifndef BUILD_VERSION
    #define BUILD_VERSION "custom"
#endif

#ifndef BUILD_TIMESTAMP
    #define BUILD_TIMESTAMP __DATE__ " " __TIME__
#endif

#ifndef GIT_COMMIT_HASH
    #define GIT_COMMIT_HASH "unknown"
#endif

struct BuildInfo {
    static const char* version() { return MYLIB_VERSION_STRING; }
    static const char* buildVersion() { return BUILD_VERSION; }
    static const char* buildTimestamp() { return BUILD_TIMESTAMP; }
    static const char* gitCommit() { return GIT_COMMIT_HASH; }
    
    static void printInfo() {
        std::cout << "Library Version: " << version() << "\n"
                  << "Build Version: " << buildVersion() << "\n"
                  << "Build Time: " << buildTimestamp() << "\n"
                  << "Git Commit: " << gitCommit() << "\n";
    }
};

// ===================== VERSION POLICY ENFORCEMENT =====================
class VersionPolicy {
public:
    // Check if current version satisfies requirement
    static bool satisfies(const std::string& requirement) {
        // Supports: ">=2.0.0", "<3.0.0", "^2.1.0", "~2.1.0"
        auto current = SemanticVersion::parse(MYLIB_VERSION_STRING);
        auto req = parseRequirement(requirement);
        
        return checkRequirement(current, req);
    }
    
    // Enforce version requirement at runtime
    static void enforce(const std::string& requirement) {
        if (!satisfies(requirement)) {
            throw std::runtime_error(
                "Version requirement not satisfied: " + requirement +
                " (current: " + MYLIB_VERSION_STRING + ")"
            );
        }
    }
    
private:
    struct VersionRequirement {
        enum class Op { EQ, NE, GT, GE, LT, LE, TILDE, CARET } op;
        SemanticVersion version;
    };
    
    static VersionRequirement parseRequirement(const std::string& req) {
        // Simplified parser
        // Real implementation would use proper parsing
        return VersionRequirement{VersionRequirement::Op::GE, 
                                 SemanticVersion::parse("2.0.0")};
    }
    
    static bool checkRequirement(const SemanticVersion& current,
                                const VersionRequirement& req) {
        switch (req.op) {
            case VersionRequirement::Op::GE:
                return !(current < req.version);
            // Handle other operators
            default:
                return true;
        }
    }
};

// Usage example
void demonstrateVersioning() {
    // Semantic versioning
    auto version = SemanticVersion::parse("2.1.3-beta+build123");
    std::cout << "Version: " << version.toString() << "\n";
    
    // Namespace versioning
    {
        using namespace MyLibrary::v2;
        auto processor = createProcessor();
        processor->configure("options");
    }
    
    // Runtime version check
    if (check_compatibility(2, 0)) {
        std::cout << "Compatible with 2.0+\n";
    }
    
    // Version policy
    VersionPolicy::enforce(">=2.0.0 <3.0.0");
    
    // Build info
    BuildInfo::printInfo();
}



// compiler_sanitizers.md
/*
Compiler Flags & Sanitizers Guide

COMPILER FLAGS:

GCC/Clang:
  - Basic:
    -g                  # Debug symbols
    -O0, -O1, -O2, -O3  # Optimization levels
    -Os                 # Optimize for size
    -Og                 # Optimize for debugging
    
  - Warnings:
    -Wall              # Most warnings
    -Wextra            # Extra warnings
    -Werror            # Treat warnings as errors
    -Wpedantic         # Strict ISO C++ compliance
    -Wshadow           # Warn on shadowed variables
    -Wconversion       # Warn on implicit conversions
    -Wsign-conversion  # Warn on signed/unsigned conversions
    
  - Language:
    -std=c++20         # C++ standard version
    -fno-exceptions    # Disable exceptions
    -fno-rtti          # Disable RTTI
    -fPIC              # Position Independent Code (shared libs)
    
  - Debugging:
    -ggdb3             # Enhanced debug info for GDB
    -fno-omit-frame-pointer  # Better stack traces
    
  - Performance:
    -march=native      # Optimize for current CPU
    -mtune=native      # Tune for current CPU
    -flto              # Link Time Optimization
    -fprofile-generate/-fprofile-use  # Profile Guided Optimization

MSVC:
  /DEBUG              # Debug symbols
  /Od, /O1, /O2, /Ox  # Optimization
  /W4                 # Warning level 4
  /WX                 # Treat warnings as errors
  /std:c++20          # C++ standard
  /MD, /MT            # Runtime library linking

SANITIZERS (GCC/Clang):

  Address Sanitizer (ASAN):
    -fsanitize=address
    -fno-omit-frame-pointer
    Detects:
      - Buffer overflows
      - Use-after-free
      - Memory leaks
      - Stack/buffer overflow

  Undefined Behavior Sanitizer (UBSAN):
    -fsanitize=undefined
    -fsanitize=integer
    -fsanitize=nullability
    Detects:
      - Integer overflow
      - Null pointer dereference
      - Misaligned pointers
      - Out-of-bounds array access

  Thread Sanitizer (TSAN):
    -fsanitize=thread
    Detects:
      - Data races
      - Deadlocks
      - Thread safety violations

  Memory Sanitizer (MSAN):
    -fsanitize=memory
    Detects:
      - Uninitialized memory reads

  Leak Sanitizer (LSAN):
    -fsanitize=leak
    Detects:
      - Memory leaks

EXAMPLE BUILD SCRIPTS:

  Debug with sanitizers:
    g++ -std=c++20 -g -O0 -Wall -Wextra -Werror \
        -fsanitize=address,undefined \
        -fno-omit-frame-pointer \
        -o program program.cpp

  Release with optimizations:
    g++ -std=c++20 -O3 -march=native -flto \
        -DNDEBUG -o program program.cpp

  Shared library:
    g++ -std=c++20 -fPIC -shared \
        -o libexample.so example.cpp
*/

// sanitizer_example.cpp - Demonstrating sanitizer usage
#include <iostream>
#include <cstring>
#include <thread>
#include <vector>
#include <memory>

// ===================== ADDRESS SANITIZER DETECTIONS =====================
void demonstrateASan() {
    // Buffer overflow
    int buffer[10];
    buffer[15] = 42;  // ASAN: stack-buffer-overflow
    
    // Use-after-free
    int* ptr = new int(100);
    delete ptr;
    *ptr = 200;  // ASAN: heap-use-after-free
    
    // Memory leak
    int* leaked = new int[100];  // ASAN: detected memory leak
    // Forgot to delete
}

// ===================== UNDEFINED BEHAVIOR SANITIZER =====================
void demonstrateUBSan() {
    // Integer overflow
    int max_int = INT_MAX;
    int overflow = max_int + 1;  // UBSAN: signed-integer-overflow
    
    // Null pointer dereference
    int* null_ptr = nullptr;
    // *null_ptr = 42;  // UBSAN: null-pointer-dereference
    
    // Shift overflow
    int shift = 1 << 32;  // UBSAN: shift-out-of-bounds
    
    // Division by zero
    int x = 10;
    int y = 0;
    // int z = x / y;  // UBSAN: division-by-zero
    
    // Misaligned pointer
    char data[10];
    int* misaligned = reinterpret_cast<int*>(&data[1]);
    // *misaligned = 42;  // UBSAN: misaligned-pointer-use
}

// ===================== THREAD SANITIZER =====================
std::atomic<int> shared_data{0};
int unsafe_shared = 0;

void thread_func1() {
    for (int i = 0; i < 10000; ++i) {
        shared_data.fetch_add(1, std::memory_order_relaxed);
        unsafe_shared++;  // TSAN: data race!
    }
}

void thread_func2() {
    for (int i = 0; i < 10000; ++i) {
        shared_data.fetch_add(1, std::memory_order_relaxed);
        unsafe_shared++;  // TSAN: data race!
    }
}

void demonstrateTSan() {
    std::thread t1(thread_func1);
    std::thread t2(thread_func2);
    
    t1.join();
    t2.join();
    
    std::cout << "Safe counter: " << shared_data.load() << "\n";
    std::cout << "Unsafe counter: " << unsafe_shared << "\n";
}

// ===================== MEMORY SANITIZER =====================
void demonstrateMSan() {
    // Uninitialized memory
    int uninitialized;
    if (uninitialized > 0) {  // MSAN: use-of-uninitialized-value
        std::cout << "Uninitialized is positive\n";
    }
    
    // Uninitialized heap memory
    int* heap_array = new int[10];
    int sum = 0;
    for (int i = 0; i < 10; ++i) {
        sum += heap_array[i];  // MSAN: use-of-uninitialized-value
    }
    delete[] heap_array;
}

// ===================== LEAK SANITIZER =====================
void demonstrateLSan() {
    // Memory leak
    int* leaked = new int(42);  // LSAN: detected memory leak
    // Forgot to delete
    
    // Indirect leak
    struct Node {
        int data;
        Node* next;
    };
    
    Node* head = new Node{1, nullptr};
    head->next = new Node{2, nullptr};  // LSAN: indirect leak
    // Only delete head, not head->next
    delete head;
}

// ===================== COMPILER-SPECIFIC BEHAVIOR =====================
#ifdef __GNUC__
    #define GCC_VERSION (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__)
#endif

void demonstrateCompilerSpecific() {
    // Compiler-specific behavior
#if defined(__GNUC__) && !defined(__clang__)
    std::cout << "Compiled with GCC " << __VERSION__ << "\n";
    
    // GCC extensions
    int array[10];
    int size = sizeof(array) / sizeof(array[0]);  // Portable
    int gcc_size = sizeof(array) / sizeof(*array);  // Also portable
    
    // GCC attributes
    __attribute__((unused)) int unused_var = 42;
    
#elif defined(__clang__)
    std::cout << "Compiled with Clang " << __clang_version__ << "\n";
    
    // Clang attributes
    [[clang::unused]] int unused_var = 42;
    
#elif defined(_MSC_VER)
    std::cout << "Compiled with MSVC " << _MSC_VER << "\n";
    
    // MSVC pragmas
    #pragma warning(push)
    #pragma warning(disable: 4100)  // Unreferenced parameter
    void unused_param(int param) {}
    #pragma warning(pop)
#endif
    
    // Standard alignment
    alignas(64) int aligned_data[100];  // 64-byte alignment for cache lines
    
    // Likely/unlikely hints
    int value = rand() % 100;
    if (value > 90) [[unlikely]] {
        std::cout << "Rare condition\n";
    }
}

// ===================== BUILD CONFIGURATIONS =====================
class BuildConfiguration {
public:
    static void printConfiguration() {
        std::cout << "Build Configuration:\n";
        
        // Compiler identification
#ifdef __GNUC__
        std::cout << "  Compiler: GCC " << __VERSION__ << "\n";
#endif
#ifdef __clang__
        std::cout << "  Compiler: Clang " << __clang_version__ << "\n";
#endif
#ifdef _MSC_VER
        std::cout << "  Compiler: MSVC " << _MSC_VER << "\n";
#endif
        
        // C++ standard
        std::cout << "  C++ Standard: ";
#if __cplusplus == 202002L
        std::cout << "C++20\n";
#elif __cplusplus == 201703L
        std::cout << "C++17\n";
#elif __cplusplus == 201402L
        std::cout << "C++14\n";
#elif __cplusplus == 201103L
        std::cout << "C++11\n";
#else
        std::cout << "Pre-C++11\n";
#endif
        
        // Build type
#ifdef NDEBUG
        std::cout << "  Build Type: Release\n";
#else
        std::cout << "  Build Type: Debug\n";
#endif
        
        // Optimization level
#ifdef __OPTIMIZE__
        std::cout << "  Optimization: Enabled\n";
#else
        std::cout << "  Optimization: Disabled\n";
#endif
        
        // Sanitizers
#ifdef __SANITIZE_ADDRESS__
        std::cout << "  Address Sanitizer: Enabled\n";
#endif
#ifdef __SANITIZE_UNDEFINED__
        std::cout << "  Undefined Behavior Sanitizer: Enabled\n";
#endif
#ifdef __SANITIZE_THREAD__
        std::cout << "  Thread Sanitizer: Enabled\n";
#endif
    }
};

// ===================== SECURE COMPILATION FLAGS =====================
/*
Secure compilation recommendations:

1. Stack Protection:
   -fstack-protector-strong    # Strong stack protection
   -fstack-clash-protection    # Stack clash protection

2. Security Hardening:
   -D_FORTIFY_SOURCE=2         # Buffer overflow detection
   -fPIE -pie                  # Position Independent Executable
   -Wl,-z,now                  # Full RELRO
   -Wl,-z,relro                # Partial RELRO

3. Control Flow Integrity:
   -fcf-protection=full        # Control flow protection (x86)
   -fsanitize=safe-stack       # Safe stack (Clang)

4. Hardening for production:
   g++ -std=c++20 -O2 -DNDEBUG \
       -fstack-protector-strong \
       -fPIE -pie \
       -Wl,-z,now,-z,relro \
       -D_FORTIFY_SOURCE=2 \
       -o secure_app app.cpp
*/

// ===================== CROSS-COMPILATION =====================
/*
Cross-compilation example for ARM:

  # ARM 32-bit (Raspberry Pi)
  arm-linux-gnueabihf-g++ -std=c++20 -march=armv7-a \
      -mfpu=neon -mfloat-abi=hard \
      -o arm_app app.cpp

  # ARM 64-bit
  aarch64-linux-gnu-g++ -std=c++20 \
      -o aarch64_app app.cpp

  # Windows from Linux (MinGW)
  x86_64-w64-mingw32-g++ -std=c++20 \
      -o windows_app.exe app.cpp
*/

// ===================== EXAMPLE CMAKELISTS.TXT =====================
/*
# Example CMakeLists.txt with sanitizers

cmake_minimum_required(VERSION 3.15)
project(SanitizerExample)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Default build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()

# Compiler warnings
add_compile_options(
    -Wall
    -Wextra
    -Werror
    -Wpedantic
    -Wshadow
    -Wconversion
)

# Build configurations
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    # Debug options
    add_compile_options(-g -O0)
    
    # Sanitizers (optional)
    option(ENABLE_SANITIZERS "Enable sanitizers" ON)
    if(ENABLE_SANITIZERS)
        add_compile_options(
            -fsanitize=address,undefined
            -fno-omit-frame-pointer
        )
        add_link_options(
            -fsanitize=address,undefined
        )
    endif()
    
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Release options
    add_compile_options(-O3 -DNDEBUG)
    
    # Security hardening
    add_compile_options(
        -fstack-protector-strong
        -D_FORTIFY_SOURCE=2
    )
    add_link_options(
        -Wl,-z,now,-z,relro
    )
endif()

add_executable(sanitizer_example sanitizer_example.cpp)
*/

int main() {
    std::cout << "=== Compiler Flags & Sanitizers Example ===\n\n";
    
    BuildConfiguration::printConfiguration();
    
    std::cout << "\nDemonstrating sanitizers (compile with appropriate flags):\n";
    
    // Uncomment to demonstrate specific sanitizers
    // demonstrateASan();
    // demonstrateUBSan();
    // demonstrateTSan();  // Requires -fsanitize=thread
    // demonstrateMSan();  // Requires -fsanitize=memory
    // demonstrateLSan();  // Requires -fsanitize=leak
    
    demonstrateCompilerSpecific();
    
    return 0;
}



// linkers_toolchains.md
/*
Linkers & Toolchains Explained

LINKERS:

  Purpose:
    - Combine object files (.o, .obj)
    - Resolve symbols (functions, variables)
    - Relocate code (adjust addresses)
    - Create executable or library

  Types:
    1. Static Linker (ld, link.exe)
        - Combines object files into executable/library
        - Resolves all symbols at link time
        - Produces: .exe, .a (static lib), .so/.dll (dynamic lib)
    
    2. Dynamic Linker (ld.so, dyld)
        - Loads shared libraries at runtime
        - Resolves symbols on demand
        - Performs relocation at load time

  Linker Scripts (ld):
    - Control memory layout
    - Define sections (.text, .data, .bss)
    - Set entry point
    - Control symbol visibility

TOOLCHAINS:

  Components:
    1. Compiler (gcc, clang, cl.exe)
    2. Assembler (as, ml64.exe)
    3. Linker (ld, link.exe)
    4. Archiver (ar, lib.exe)
    5. Debugger (gdb, lldb, windbg)
    6. Standard Library (libc, libc++)
    7. Runtime Library (crt0, vcruntime)

  Popular Toolchains:
    
    Linux:
      - GCC + GNU Binutils + glibc
        gcc, g++, as, ld, ar, gdb
        
      - Clang + LLVM + libc++
        clang, clang++, lld, lldb
        
    Windows:
      - Microsoft Visual C++ (MSVC)
        cl.exe, link.exe, lib.exe
        
      - MinGW-w64 (GNU on Windows)
        x86_64-w64-mingw32-g++
        
      - Clang for Windows
        clang-cl (MSVC-compatible)
        
    macOS:
      - Apple Clang + LLVM + libc++
        clang++, lldb
        
      - Homebrew GCC
        gcc-11, g++-11

  Cross-Compilation:
    - Target different platform from host
    - Example: Build for ARM on x86
    - Requires target-specific toolchain
    
LIBRARY TYPES:

  Static Libraries (.a, .lib):
    - Code copied into executable
    - No runtime dependencies
    - Larger binaries
    - Faster startup
    
  Dynamic Libraries (.so, .dll, .dylib):
    - Shared code loaded at runtime
    - Smaller binaries
    - Can be updated independently
    - Slightly slower startup
    
  Comparison:
    +-------------------+-------------------+------------------+
    | Aspect            | Static            | Dynamic          |
    +-------------------+-------------------+------------------+
    | Binary Size       | Larger            | Smaller          |
    | Startup Time      | Faster            | Slight overhead  |
    | Updates           | Rebuild needed    | Swap library     |
    | ABI Concerns      | None              | Critical         |
    | Memory Usage      | Higher (per app)  | Shared           |
    | Deployment        | Easy              | Requires libs    |
    +-------------------+-------------------+------------------+

SYMBOL VISIBILITY:

  - Default: All symbols visible (can cause conflicts)
  - Hidden: Symbols not exported from shared library
  - Use -fvisibility=hidden and export selectively
  
VERSIONING:

  - Shared objects: libfoo.so.MAJOR.MINOR.PATCH
  - SONAME: libfoo.so.MAJOR (embedded in library)
  - Symbol versioning: @@VERSION in symbol table
*/

// linker_example.cpp - Demonstrating linking concepts
#include <iostream>
#include <vector>
#include <memory>

// ===================== STATIC vs DYNAMIC LINKING =====================

// Static library would contain these functions
namespace StaticMath {
    int add(int a, int b) {
        return a + b;
    }
    
    int multiply(int a, int b) {
        return a * b;
    }
}

// Shared library interface
#ifdef BUILD_SHARED_LIB
    #ifdef _WIN32
        #define SHARED_API __declspec(dllexport)
    #else
        #define SHARED_API __attribute__((visibility("default")))
    #endif
#else
    #define SHARED_API
#endif

extern "C" {
    SHARED_API int shared_add(int a, int b);
    SHARED_API int shared_multiply(int a, int b);
}

// ===================== SYMBOL VISIBILITY =====================

// Default visibility (exported from shared library)
__attribute__((visibility("default")))
void exported_function() {
    std::cout << "This function is exported\n";
}

// Hidden visibility (not exported)
__attribute__((visibility("hidden")))
void internal_function() {
    std::cout << "This function is internal\n";
}

// Selective export using macros
#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
    #define IMPORT __declspec(dllimport)
#else
    #define EXPORT __attribute__((visibility("default")))
    #define IMPORT
#endif

#ifdef BUILD_SHARED_LIB
    #define API EXPORT
#else
    #define API IMPORT
#endif

class API PublicClass {
public:
    void publicMethod();
    
private:
    void privateMethod();  // Not exported
};

// ===================== LINKER SECTIONS =====================

// Place data in specific sections
__attribute__((section(".custom_data")))
int custom_variable = 42;

__attribute__((section(".custom_code")))
void custom_function() {
    std::cout << "Function in custom section\n";
}

// Constructor/destructor priorities
__attribute__((constructor(101)))  // Early initialization
void early_init() {
    std::cout << "Early initialization\n";
}

__attribute__((destructor(101)))  // Late cleanup
void late_cleanup() {
    std::cout << "Late cleanup\n";
}

// ===================== WEAK SYMBOLS =====================

// Weak symbol (can be overridden)
__attribute__((weak))
void weak_function() {
    std::cout << "Default weak implementation\n";
}

// Strong symbol (overrides weak)
void weak_function() {
    std::cout << "Strong implementation overrides weak\n";
}

// ===================== LINK-TIME OPTIMIZATION =====================

// Functions that benefit from LTO
__attribute__((always_inline))
inline int heavily_inlined(int x) {
    return x * x + 2 * x + 1;
}

// External function that linker can optimize
int external_calculation(int x);

// ===================== RUNTIME LIBRARY LINKING =====================

#ifdef _WIN32
    // Windows runtime linking
    // /MD: Dynamic runtime (msvcrt.dll)
    // /MT: Static runtime
#else
    // Linux/Mac: Usually dynamic linking to libc, libstdc++, libc++
#endif

// ===================== EXAMPLE BUILD SCRIPTS =====================

/*
Building static library:

  g++ -c math.cpp -o math.o
  ar rcs libmath.a math.o
  
  # Using the static library
  g++ main.cpp -L. -lmath -o program
  
Building shared library:

  # Linux/Mac
  g++ -fPIC -shared -o libmath.so math.cpp
  
  # Windows
  cl /LD math.cpp /link /OUT:math.dll
  
  # Using shared library
  g++ main.cpp -L. -lmath -o program
  
  # Runtime: export LD_LIBRARY_PATH=. (Linux)
  # Or copy .dll to executable directory (Windows)
*/

// ===================== DYNAMIC LOADING =====================
#include <dlfcn.h>  // Linux/Mac
// #include <windows.h>  // Windows

class DynamicLibrary {
private:
#ifdef _WIN32
    HMODULE handle;
#else
    void* handle;
#endif
    
public:
    DynamicLibrary(const std::string& library_path) {
#ifdef _WIN32
        handle = LoadLibraryA(library_path.c_str());
#else
        handle = dlopen(library_path.c_str(), RTLD_LAZY);
#endif
        if (!handle) {
            throw std::runtime_error("Failed to load library");
        }
    }
    
    ~DynamicLibrary() {
        if (handle) {
#ifdef _WIN32
            FreeLibrary(handle);
#else
            dlclose(handle);
#endif
        }
    }
    
    template<typename Func>
    Func get_function(const std::string& name) {
#ifdef _WIN32
        return reinterpret_cast<Func>(GetProcAddress(handle, name.c_str()));
#else
        return reinterpret_cast<Func>(dlsym(handle, name.c_str()));
#endif
    }
};

void demonstrate_dynamic_loading() {
    try {
        DynamicLibrary lib("./libmath.so");  // or .dll
        
        using AddFunc = int(*)(int, int);
        AddFunc add = lib.get_function<AddFunc>("add");
        
        if (add) {
            int result = add(10, 20);
            std::cout << "Dynamic call result: " << result << "\n";
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
}

// ===================== TOOLCHAIN DETECTION =====================
void detect_toolchain() {
    std::cout << "Toolchain Information:\n";
    
    // Compiler
#if defined(__GNUC__) && !defined(__clang__)
    std::cout << "  Compiler: GCC " << __VERSION__ << "\n";
#elif defined(__clang__)
    std::cout << "  Compiler: Clang " << __clang_version__ << "\n";
#elif defined(_MSC_VER)
    std::cout << "  Compiler: MSVC " << _MSC_VER << "\n";
#endif
    
    // Standard Library
#ifdef _LIBCPP_VERSION
    std::cout << "  Stdlib: libc++ " << _LIBCPP_VERSION << "\n";
#elif defined(__GLIBCXX__)
    std::cout << "  Stdlib: libstdc++ " << __GLIBCXX__ << "\n";
#elif defined(_CPPLIB_VER)
    std::cout << "  Stdlib: MSVC STL " << _CPPLIB_VER << "\n";
#endif
    
    // Platform
#ifdef __linux__
    std::cout << "  Platform: Linux\n";
#elif defined(_WIN32)
    std::cout << "  Platform: Windows\n";
#elif defined(__APPLE__)
    std::cout << "  Platform: macOS\n";
#endif
    
    // Architecture
#ifdef __x86_64__
    std::cout << "  Arch: x86-64\n";
#elif defined(__i386__)
    std::cout << "  Arch: x86\n";
#elif defined(__aarch64__)
    std::cout << "  Arch: ARM64\n";
#elif defined(__arm__)
    std::cout << "  Arch: ARM\n";
#endif
    
    // Endianness
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
    std::cout << "  Endian: Little\n";
#elif __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
    std::cout << "  Endian: Big\n";
#endif
}

// ===================== CROSS-COMPILATION EXAMPLE =====================
/*
Cross-compilation setup:

  # Install cross-compiler
  sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
  
  # Build for ARM64
  aarch64-linux-gnu-g++ -std=c++20 \
      -o program-arm64 program.cpp
      
  # Check file type
  file program-arm64
  # program-arm64: ELF 64-bit LSB executable, ARM aarch64, version 1
*/

// ===================== LINKER SCRIPT EXAMPLE =====================
/*
Example linker script (linker.ld):

  ENTRY(_start)           /* Entry point */
  
  SECTIONS {
      . = 0x10000;       /* Load address */
      
      .text : {
          *(.text)       /* Code */
          *(.text.*)
      }
      
      .rodata : {
          *(.rodata)     /* Read-only data */
          *(.rodata.*)
      }
      
      .data : {
          *(.data)       /* Initialized data */
          *(.data.*)
      }
      
      .bss : {
          *(.bss)        /* Zero-initialized data */
          *(.bss.*)
          *(COMMON)
      }
      
      /DISCARD/ : {
          *(.comment)
          *(.note.*)
      }
  }
  
Usage:
  ld -T linker.ld -o program *.o
*/

// ===================== SYMBOL VERSIONING =====================
/*
Symbol versioning in shared libraries:

  # Version script (libfoo.map)
  LIBFOO_1.0 {
      global:
          foo;
          bar;
      local:
          *;
  };
  
  LIBFOO_2.0 {
      global:
          foo_v2;
  } LIBFOO_1.0;
  
Building:
  g++ -shared -Wl,--version-script=libfoo.map \
      -o libfoo.so foo.cpp
*/

// ===================== MEMORY LAYOUT =====================
void show_memory_layout() {
    std::cout << "\nMemory Layout Example:\n";
    
    // Text segment (code)
    std::cout << "Code address: " << (void*)show_memory_layout << "\n";
    
    // Data segment
    static int static_var = 42;
    std::cout << "Static variable: " << &static_var << "\n";
    
    // Heap
    int* heap_var = new int(100);
    std::cout << "Heap variable: " << heap_var << "\n";
    delete heap_var;
    
    // Stack
    int stack_var = 200;
    std::cout << "Stack variable: " << &stack_var << "\n";
    
    // Environment variables
    extern char** environ;
    std::cout << "Environment: " << (void*)environ << "\n";
}

// ===================== RELOCATION EXAMPLE =====================
/*
Relocation types:

  - R_X86_64_PC32: PC-relative 32-bit
  - R_X86_64_64: Absolute 64-bit
  - R_X86_64_GOTPCRELX: GOT-relative
  
View relocations:
  objdump -R program     # Dynamic relocations
  readelf -r program     # ELF relocations
*/

int main() {
    std::cout << "=== Linkers & Toolchains Example ===\n\n";
    
    detect_toolchain();
    
    // Static linking example
    std::cout << "\nStatic Math: " 
              << StaticMath::add(10, 20) << "\n";
    
    // Symbol visibility
    exported_function();
    internal_function();
    
    // Weak symbols
    weak_function();
    
    // Linker sections
    custom_function();
    std::cout << "Custom variable: " << custom_variable << "\n";
    
    // Dynamic loading
    demonstrate_dynamic_loading();
    
    // Memory layout
    show_memory_layout();
    
    return 0;
}



// ffi_example.cpp - Foreign Function Interface examples
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cstring>

// ===================== C ABI FOR FFI =====================
// C interface is stable and simple for FFI

// C-compatible types only
extern "C" {
    
    // Simple data types
    struct Point {
        double x;
        double y;
    };
    
    struct Rect {
        Point top_left;
        Point bottom_right;
    };
    
    // Opaque pointer for C++ objects
    typedef void* ImageHandle;
    
    // Function pointer types
    typedef void (*ProgressCallback)(int percent, void* user_data);
    typedef void (*ErrorCallback)(const char* message, void* user_data);
    
    // Simple functions with C linkage
    ImageHandle create_image(int width, int height);
    void destroy_image(ImageHandle handle);
    
    // Functions with callbacks
    void process_image(ImageHandle handle,
                      ProgressCallback progress_cb,
                      ErrorCallback error_cb,
                      void* user_data);
    
    // Functions returning simple types
    int get_image_width(ImageHandle handle);
    int get_image_height(ImageHandle handle);
    
    // Functions with struct parameters
    Rect get_image_bounds(ImageHandle handle);
    void set_image_bounds(ImageHandle handle, Rect bounds);
    
    // Memory management functions
    void* allocate_buffer(size_t size);
    void free_buffer(void* buffer);
    
    // String handling (caller must free)
    char* get_image_info(ImageHandle handle);
    void free_string(char* str);
}

// ===================== C++ IMPLEMENTATION =====================
class Image {
private:
    int width;
    int height;
    std::vector<uint8_t> data;
    Rect bounds;
    
public:
    Image(int w, int h) : width(w), height(h), data(w * h * 4) {
        bounds.top_left = {0.0, 0.0};
        bounds.bottom_right = {static_cast<double>(w), 
                              static_cast<double>(h)};
    }
    
    int getWidth() const { return width; }
    int getHeight() const { return height; }
    Rect getBounds() const { return bounds; }
    void setBounds(Rect b) { bounds = b; }
    
    std::string getInfo() const {
        return "Image " + std::to_string(width) + "x" + 
               std::to_string(height);
    }
    
    void process(std::function<void(int)> progress,
                std::function<void(const std::string&)> error) {
        // Simulate processing
        for (int i = 0; i <= 100; i += 10) {
            if (progress) progress(i);
            // Simulate work
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    }
};

// C wrapper implementations
extern "C" {
    
    ImageHandle create_image(int width, int height) {
        try {
            return new Image(width, height);
        } catch (...) {
            return nullptr;
        }
    }
    
    void destroy_image(ImageHandle handle) {
        delete static_cast<Image*>(handle);
    }
    
    void process_image(ImageHandle handle,
                      ProgressCallback progress_cb,
                      ErrorCallback error_cb,
                      void* user_data) {
        Image* img = static_cast<Image*>(handle);
        if (!img) {
            if (error_cb) {
                error_cb("Invalid image handle", user_data);
            }
            return;
        }
        
        try {
            img->process(
                [progress_cb, user_data](int percent) {
                    if (progress_cb) {
                        progress_cb(percent, user_data);
                    }
                },
                [error_cb, user_data](const std::string& msg) {
                    if (error_cb) {
                        error_cb(msg.c_str(), user_data);
                    }
                }
            );
        } catch (const std::exception& e) {
            if (error_cb) {
                error_cb(e.what(), user_data);
            }
        }
    }
    
    int get_image_width(ImageHandle handle) {
        Image* img = static_cast<Image*>(handle);
        return img ? img->getWidth() : -1;
    }
    
    int get_image_height(ImageHandle handle) {
        Image* img = static_cast<Image*>(handle);
        return img ? img->getHeight() : -1;
    }
    
    Rect get_image_bounds(ImageHandle handle) {
        Image* img = static_cast<Image*>(handle);
        static Rect empty = {{0.0, 0.0}, {0.0, 0.0}};
        return img ? img->getBounds() : empty;
    }
    
    void set_image_bounds(ImageHandle handle, Rect bounds) {
        Image* img = static_cast<Image*>(handle);
        if (img) {
            img->setBounds(bounds);
        }
    }
    
    char* get_image_info(ImageHandle handle) {
        Image* img = static_cast<Image*>(handle);
        if (!img) return nullptr;
        
        std::string info = img->getInfo();
        char* cstr = static_cast<char*>(malloc(info.size() + 1));
        if (cstr) {
            std::strcpy(cstr, info.c_str());
        }
        return cstr;
    }
    
    void free_string(char* str) {
        free(str);
    }
    
    void* allocate_buffer(size_t size) {
        return malloc(size);
    }
    
    void free_buffer(void* buffer) {
        free(buffer);
    }
}

// ===================== RUST INTERFACE =====================
/*
Rust side (lib.rs):
  
  #[repr(C)]
  pub struct Point {
      pub x: f64,
      pub y: f64,
  }
  
  #[repr(C)]
  pub struct Rect {
      pub top_left: Point,
      pub bottom_right: Point,
  }
  
  extern "C" {
      pub fn create_image(width: i32, height: i32) -> *mut c_void;
      pub fn destroy_image(handle: *mut c_void);
      pub fn get_image_width(handle: *mut c_void) -> i32;
  }
  
  // Safe Rust wrapper
  pub struct Image {
      handle: *mut c_void,
  }
  
  impl Image {
      pub fn new(width: i32, height: i32) -> Option<Self> {
          let handle = unsafe { create_image(width, height) };
          if handle.is_null() {
              None
          } else {
              Some(Image { handle })
          }
      }
      
      pub fn width(&self) -> i32 {
          unsafe { get_image_width(self.handle) }
      }
  }
  
  impl Drop for Image {
      fn drop(&mut self) {
          unsafe { destroy_image(self.handle) }
      }
  }
*/

// ===================== PYTHON INTERFACE =====================
/*
Using ctypes (Python):

  import ctypes
  import platform
  
  if platform.system() == "Windows":
      lib = ctypes.CDLL("./image_lib.dll")
  else:
      lib = ctypes.CDLL("./libimage_lib.so")
  
  # Define types
  class Point(ctypes.Structure):
      _fields_ = [("x", ctypes.c_double),
                  ("y", ctypes.c_double)]
  
  class Rect(ctypes.Structure):
      _fields_ = [("top_left", Point),
                  ("bottom_right", Point)]
  
  # Set up function prototypes
  lib.create_image.argtypes = [ctypes.c_int, ctypes.c_int]
  lib.create_image.restype = ctypes.c_void_p
  
  lib.destroy_image.argtypes = [ctypes.c_void_p]
  
  lib.get_image_width.argtypes = [ctypes.c_void_p]
  lib.get_image_width.restype = ctypes.c_int
  
  # Usage
  image = lib.create_image(800, 600)
  width = lib.get_image_width(image)
  lib.destroy_image(image)
*/

// ===================== C# INTERFACE (P/INVOKE) =====================
/*
C# side:
  
  using System;
  using System.Runtime.InteropServices;
  
  namespace ImageLibrary {
      [StructLayout(LayoutKind.Sequential)]
      public struct Point {
          public double x;
          public double y;
      }
      
      [StructLayout(LayoutKind.Sequential)]
      public struct Rect {
          public Point top_left;
          public Point bottom_right;
      }
      
      public class ImageLib {
          [DllImport("image_lib.dll", CallingConvention = CallingConvention.Cdecl)]
          public static extern IntPtr create_image(int width, int height);
          
          [DllImport("image_lib.dll", CallingConvention = CallingConvention.Cdecl)]
          public static extern void destroy_image(IntPtr handle);
          
          [DllImport("image_lib.dll", CallingConvention = CallingConvention.Cdecl)]
          public static extern int get_image_width(IntPtr handle);
          
          // Callback delegates
          [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
          public delegate void ProgressCallback(int percent, IntPtr userData);
          
          [DllImport("image_lib.dll", CallingConvention = CallingConvention.Cdecl)]
          public static extern void process_image(
              IntPtr handle,
              ProgressCallback progress_cb,
              ErrorCallback error_cb,
              IntPtr user_data);
      }
      
      // Safe wrapper
      public class Image : IDisposable {
          private IntPtr handle;
          private bool disposed = false;
          
          public Image(int width, int height) {
              handle = ImageLib.create_image(width, height);
              if (handle == IntPtr.Zero) {
                  throw new Exception("Failed to create image");
              }
          }
          
          public int Width {
              get { return ImageLib.get_image_width(handle); }
          }
          
          public void Process(Action<int> progress, Action<string> error) {
              // Marshal callbacks
              // ...
          }
          
          public void Dispose() {
              Dispose(true);
              GC.SuppressFinalize(this);
          }
          
          protected virtual void Dispose(bool disposing) {
              if (!disposed) {
                  if (handle != IntPtr.Zero) {
                      ImageLib.destroy_image(handle);
                      handle = IntPtr.Zero;
                  }
                  disposed = true;
              }
          }
          
          ~Image() {
              Dispose(false);
          }
      }
  }
*/

// ===================== JAVASCRIPT/WASM INTERFACE =====================
/*
WebAssembly with Emscripten:

  // C++ compiled to WebAssembly
  // emcc -O2 -lembind -o image_lib.js image_lib.cpp
  
  JavaScript side:
    
    import Module from './image_lib.js';
    
    await Module.ready;
    
    class Point {
      constructor(x, y) {
        this.x = x;
        this.y = y;
      }
    }
    
    class Rect {
      constructor(top_left, bottom_right) {
        this.top_left = top_left;
        this.bottom_right = bottom_right;
      }
    }
    
    // Embind automatically generates bindings
    const Image = Module.Image;
    
    const img = new Image(800, 600);
    console.log(`Width: ${img.getWidth()}`);
    img.delete();  // Manual memory management
*/

// ===================== SWIG INTERFACE GENERATOR =====================
/*
SWIG interface file (image_lib.i):
  
  %module image_lib
  
  %{
  #include "image_lib.h"
  %}
  
  // Map C++ exceptions to target language exceptions
  %exception {
      try {
          $action
      } catch (const std::exception& e) {
          SWIG_exception(SWIG_RuntimeError, e.what());
      }
  }
  
  // Include header
  %include "image_lib.h"
  
  // Special handling for callbacks
  %typemap(in) void* {
      // Convert target language function to C callback
  }
  
Building:
  swig -c++ -python image_lib.i
  g++ -fPIC -c image_lib_wrap.cxx -I/usr/include/python3.8
  g++ -shared image_lib_wrap.o -o _image_lib.so
*/

// ===================== PYTHON EXTENSION MODULE =====================
/*
Using Python C API directly:

  #include <Python.h>
  #include "image_lib.h"
  
  static PyObject* py_create_image(PyObject* self, PyObject* args) {
      int width, height;
      if (!PyArg_ParseTuple(args, "ii", &width, &height)) {
          return NULL;
      }
      
      ImageHandle handle = create_image(width, height);
      if (!handle) {
          PyErr_SetString(PyExc_RuntimeError, "Failed to create image");
          return NULL;
      }
      
      return PyCapsule_New(handle, "ImageHandle", NULL);
  }
  
  static PyObject* py_get_image_width(PyObject* self, PyObject* args) {
      PyObject* capsule;
      if (!PyArg_ParseTuple(args, "O", &capsule)) {
          return NULL;
      }
      
      ImageHandle handle = (ImageHandle)PyCapsule_GetPointer(capsule, "ImageHandle");
      if (!handle) {
          return NULL;
      }
      
      int width = get_image_width(handle);
      return PyLong_FromLong(width);
  }
  
  static PyMethodDef ImageLibMethods[] = {
      {"create_image", py_create_image, METH_VARARGS, "Create an image"},
      {"get_image_width", py_get_image_width, METH_VARARGS, "Get image width"},
      {NULL, NULL, 0, NULL}
  };
  
  static struct PyModuleDef imagelibmodule = {
      PyModuleDef_HEAD_INIT,
      "image_lib",
      "Image processing library",
      -1,
      ImageLibMethods
  };
  
  PyMODINIT_FUNC PyInit_image_lib(void) {
      return PyModule_Create(&imagelibmodule);
  }
*/

// ===================== JNI (JAVA NATIVE INTERFACE) =====================
/*
Java JNI interface:

  C++ side (image_lib_jni.cpp):
    
    #include <jni.h>
    #include "image_lib.h"
    
    extern "C" {
        JNIEXPORT jlong JNICALL
        Java_com_example_ImageLib_createImage(JNIEnv* env, jclass clazz,
                                             jint width, jint height) {
            return reinterpret_cast<jlong>(create_image(width, height));
        }
        
        JNIEXPORT void JNICALL
        Java_com_example_ImageLib_destroyImage(JNIEnv* env, jclass clazz,
                                              jlong handle) {
            destroy_image(reinterpret_cast<ImageHandle>(handle));
        }
        
        JNIEXPORT jint JNICALL
        Java_com_example_ImageLib_getImageWidth(JNIEnv* env, jclass clazz,
                                               jlong handle) {
            return get_image_width(reinterpret_cast<ImageHandle>(handle));
        }
    }
  
  Java side:
    
    package com.example;
    
    public class ImageLib {
        static {
            System.loadLibrary("image_lib");
        }
        
        private native long createImage(int width, int height);
        private native void destroyImage(long handle);
        private native int getImageWidth(long handle);
        
        public class Image implements AutoCloseable {
            private long handle;
            
            public Image(int width, int height) {
                handle = createImage(width, height);
                if (handle == 0) {
                    throw new RuntimeException("Failed to create image");
                }
            }
            
            public int getWidth() {
                return getImageWidth(handle);
            }
            
            @Override
            public void close() {
                if (handle != 0) {
                    destroyImage(handle);
                    handle = 0;
                }
            }
            
            @Override
            protected void finalize() throws Throwable {
                close();
                super.finalize();
            }
        }
    }
*/

// ===================== GO CGO INTERFACE =====================
/*
Go cgo interface:

  // image_lib.go
  package main
  
  /*
  #cgo CFLAGS: -I.
  #cgo LDFLAGS: -L. -limage_lib
  #include "image_lib.h"
  */
  import "C"
  import "unsafe"
  
  type Point struct {
      X float64
      Y float64
  }
  
  type Rect struct {
      TopLeft Point
      BottomRight Point
  }
  
  type Image struct {
      handle unsafe.Pointer
  }
  
  func NewImage(width, height int) (*Image, error) {
      handle := C.create_image(C.int(width), C.int(height))
      if handle == nil {
          return nil, errors.New("failed to create image")
      }
      return &Image{handle: handle}, nil
  }
  
  func (img *Image) Width() int {
      return int(C.get_image_width(img.handle))
  }
  
  func (img *Image) Close() {
      if img.handle != nil {
          C.destroy_image(img.handle)
          img.handle = nil
      }
  }
  
  // Callback wrapper
  //export goProgressCallback
  func goProgressCallback(percent C.int, userData unsafe.Pointer) {
      // Convert to Go callback
  }
*/

// ===================== FFI BEST PRACTICES =====================
class FFIBestPractices {
public:
    // 1. Use C ABI (extern "C")
    static void rule1() {
        std::cout << "1. Always use extern \"C\" for FFI functions\n";
    }
    
    // 2. Use simple, fixed-size types
    static void rule2() {
        std::cout << "2. Use simple types: int, double, char*, void*\n";
        std::cout << "   Avoid: std::string, std::vector, smart pointers\n";
    }
    
    // 3. Provide explicit memory management
    static void rule3() {
        std::cout << "3. Provide create/destroy functions\n";
        std::cout << "   Document ownership semantics\n";
    }
    
    // 4. Use opaque pointers
    static void rule4() {
        std::cout << "4. Use void* or opaque structs for objects\n";
        std::cout << "   Hide C++ implementation details\n";
    }
    
    // 5. Provide C callbacks for async operations
    static void rule5() {
        std::cout << "5. Use C callbacks for async operations\n";
        std::cout << "   Include user_data parameter\n";
    }
    
    // 6. Handle exceptions at boundary
    static void rule6() {
        std::cout << "6. Catch C++ exceptions at FFI boundary\n";
        std::cout << "   Convert to error codes or callbacks\n";
    }
    
    // 7. Version your API
    static void rule7() {
        std::cout << "7. Version your FFI API\n";
        std::cout << "   Use function prefixes or version structs\n";
    }
    
    // 8. Provide comprehensive documentation
    static void rule8() {
        std::cout << "8. Document thread safety, memory ownership,\n";
        std::cout << "   error handling, and lifecycle\n";
    }
};

// ===================== FFI TESTING =====================
void test_ffi_interface() {
    std::cout << "Testing FFI interface...\n";
    
    // Create image
    ImageHandle img = create_image(800, 600);
    if (!img) {
        std::cerr << "Failed to create image\n";
        return;
    }
    
    // Get properties
    int width = get_image_width(img);
    int height = get_image_height(img);
    std::cout << "Image size: " << width << "x" << height << "\n";
    
    // Get bounds
    Rect bounds = get_image_bounds(img);
    std::cout << "Bounds: (" << bounds.top_left.x << "," << bounds.top_left.y
              << ") to (" << bounds.bottom_right.x << "," 
              << bounds.bottom_right.y << ")\n";
    
    // Get info string
    char* info = get_image_info(img);
    if (info) {
        std::cout << "Info: " << info << "\n";
        free_string(info);
    }
    
    // Process with callbacks
    process_image(
        img,
        [](int percent, void* user_data) {
            std::cout << "Progress: " << percent << "%\n";
        },
        [](const char* message, void* user_data) {
            std::cerr << "Error: " << message << "\n";
        },
        nullptr  // user_data
    );
    
    // Cleanup
    destroy_image(img);
}

// ===================== PERFORMANCE CONSIDERATIONS =====================
void ffi_performance_considerations() {
    std::cout << "\nFFI Performance Considerations:\n";
    
    std::cout << "1. Marshalling overhead\n";
    std::cout << "   - Converting between language representations\n";
    std::cout << "   - Solution: Use simple types, minimize crossings\n";
    
    std::cout << "2. Memory copying\n";
    std::cout << "   - Data may be copied across boundaries\n";
    std::cout << "   - Solution: Use shared memory or zero-copy\n";
    
    std::cout << "3. Thread safety\n";
    std::cout << "   - FFI calls may need synchronization\n";
    std::cout << "   - Document thread safety guarantees\n";
    
    std::cout << "4. Error handling overhead\n";
    std::cout << "   - Converting between error representations\n";
    std::cout << "   - Use efficient error codes for common cases\n";
}

int main() {
    std::cout << "=== Foreign Function Interface (FFI) Example ===\n\n";
    
    FFIBestPractices::rule1();
    FFIBestPractices::rule2();
    FFIBestPractices::rule3();
    FFIBestPractices::rule4();
    FFIBestPractices::rule5();
    FFIBestPractices::rule6();
    FFIBestPractices::rule7();
    FFIBestPractices::rule8();
    
    std::cout << "\n";
    test_ffi_interface();
    
    ffi_performance_considerations();
    
    return 0;
}




// binary_compatibility.cpp - Binary compatibility issues and solutions
#include <iostream>
#include <memory>
#include <vector>
#include <cstddef>

// ===================== STRUCT LAYOUT CHANGES =====================

// Version 1.0
struct Data_v1 {
    int id;           // offset 0
    float value;      // offset 4
    // Total size: 8 bytes (assuming 4-byte alignment)
};

// Version 1.1 - BAD: Adding field changes layout
struct Data_v1_1_BAD {
    int id;           // offset 0
    float value;      // offset 4
    bool enabled;     // offset 8 - NEW FIELD!
    // Total size: 12 bytes (with padding)
    // BREAKS BINARY COMPATIBILITY!
    // Old code expects 8 bytes, new struct is 12 bytes
};

// Version 1.1 - GOOD: Add field at end with versioning
struct Data_v1_1_GOOD {
    int id;
    float value;
    // Version 1.0 ends here
    // New in version 1.1:
    bool enabled;     // Added at the end
    char reserved[7]; // Reserved for future expansion
    // Total size: 16 bytes (8-byte aligned)
    // Old code can still use first 8 bytes
};

// Version 1.2 - Using versioned layout
class Data {
private:
    struct Version1_0 {
        int id;
        float value;
    };
    
    struct Version1_1 : Version1_0 {
        bool enabled;
        char reserved[7];
    };
    
    std::aligned_storage<16, 8>::type storage;
    int version;
    
public:
    Data(int ver = 1) : version(ver) {
        if (version == 1) {
            new (&storage) Version1_0{0, 0.0f};
        } else {
            new (&storage) Version1_1{0, 0.0f, false, {}};
        }
    }
    
    int getId() const {
        if (version == 1) {
            return reinterpret_cast<const Version1_0*>(&storage)->id;
        } else {
            return reinterpret_cast<const Version1_1*>(&storage)->id;
        }
    }
    
    // ... other accessors
};

// ===================== VIRTUAL FUNCTION CHANGES =====================

// Base class v1.0
class Base_v1 {
public:
    virtual ~Base_v1() = default;
    virtual void process() { /* vtable[0] */ }
    virtual int calculate() { return 42; }  // vtable[1]
};

// Derived class v1.1 - BAD: Adding virtual function
class Derived_v1_1_BAD : public Base_v1 {
public:
    virtual void newMethod() { /* vtable[2] - BREAKS ABI! */ }
    // Adding virtual function changes vtable layout
    // Old code expects calculate() at vtable[1], now it's at [2]
};

// Solution 1: Don't add virtual functions to existing classes
// Solution 2: Use composition instead of inheritance
// Solution 3: Create new interface

// Versioned interface approach
class IBase_v1 {
public:
    virtual ~IBase_v1() = default;
    virtual void process() = 0;
    virtual int calculate() = 0;
};

class IBase_v2 : public IBase_v1 {
public:
    virtual void newMethod() = 0;  // New in v2
};

// Factory with version detection
std::unique_ptr<IBase_v1> createBase(int version) {
    if (version == 1) {
        return std::make_unique<Base_v1_Impl>();
    } else {
        return std::make_unique<Base_v2_Impl>();
    }
}

// ===================== INLINE FUNCTION CHANGES =====================

// Header file v1.0
inline int helper_function(int x, int y) {
    return x + y;  // Inlined into calling code
}

// Header file v1.1 - BAD: Changing inline function
inline int helper_function(int x, int y) {
    return x * y;  // BREAKS BINARY COMPATIBILITY!
    // Old compiled code uses x+y, new code uses x*y
    // Mixing leads to incorrect results
}

// Solution: Never change inline functions
// Option 1: Create new function
inline int helper_function_v2(int x, int y) {
    return x * y;  // New name
}

// Option 2: Use compile-time selection
template<int Version = 1>
inline int helper_function_versioned(int x, int y) {
    if constexpr (Version == 1) {
        return x + y;
    } else {
        return x * y;
    }
}

// ===================== STANDARD LIBRARY VERSION ISSUES =====================

void std_library_issues() {
    // Different libstdc++ versions have different ABIs
    std::string s1 = "hello";
    
    // libstdc++ 5 vs 6 have different string implementations
    // GCC 5: COW (Copy-On-Write) string
    // GCC 6+: SSO (Small String Optimization)
    
    // Solution: Use same compiler/stdlib version
    // Or stick to C ABI for library interfaces
    
    // Vector<bool> is especially problematic
    std::vector<bool> bits;
    // Different implementations may pack bits differently
    
    // Avoid in public APIs
}

// ===================== COMPILER FLAG DIFFERENCES =====================

void compiler_flag_issues() {
    // Different compiler flags affect ABI:
    
    // 1. Exception handling
    // -fno-exceptions changes function signatures
    
    // 2. RTTI
    // -fno-rtti affects typeid and dynamic_cast
    
    // 3. Optimization levels
    // Different -O levels can change inlining decisions
    
    // 4. Debug vs Release
    // -g adds debug info but doesn't affect ABI
    // -DNDEBUG changes assert behavior
    
    // 5. Structure packing
    // #pragma pack changes struct layout
    
    // Solution: Document required compiler flags
    // Or use C ABI for library boundaries
}

// ===================== NAME MANGLING DIFFERENCES =====================

void name_mangling_issues() {
    // Different compilers = different name mangling
    
    // GCC/Clang (Itanium ABI):
    // _ZN3foo3barEv -> foo::bar()
    
    // MSVC:
    // ?bar@foo@@YAXXZ -> foo::bar()
    
    // Solution for libraries:
    // 1. Use C linkage (extern "C")
    // 2. Use same compiler for all components
    // 3. Use COM interfaces on Windows
}

// ===================== TEMPLATE INSTANTIATIONS =====================

template<typename T>
class Container {
private:
    T* data;
    size_t size;
    
public:
    Container(size_t n) : data(new T[n]), size(n) {}
    ~Container() { delete[] data; }
    
    T& operator[](size_t idx) { return data[idx]; }
    size_t getSize() const { return size; }
};

// Template instantiation issues:
// - Each translation unit instantiates templates
// - Different compiler versions may generate different code
// - Debug vs Release may instantiate differently

// Solution:
// 1. Explicit template instantiation in one translation unit
// 2. Header-only library (consistent instantiation)
// 3. Avoid templates in public API

// Explicit instantiation
template class Container<int>;    // In .cpp file
template class Container<double>; // In .cpp file

// ===================== RUN-TIME TYPE INFORMATION =====================

class RTTI_Example {
public:
    virtual ~RTTI_Example() = default;
    
    // RTTI adds type_info structures
    // Different compilers implement type_info differently
    
    virtual const char* getName() const {
        return typeid(*this).name();  // Compiler-specific
    }
};

// Issues:
// - typeid() may return different strings
// - dynamic_cast may work differently
// - -fno-rtti breaks this code

// Solution for libraries:
// - Avoid RTTI in public interfaces
// - Use virtual functions for type identification
// - Or use explicit type IDs

class TypeSafeBase {
public:
    virtual ~TypeSafeBase() = default;
    
    enum class TypeId {
        BASE,
        DERIVED1,
        DERIVED2
    };
    
    virtual TypeId getTypeId() const = 0;
    
    template<typename T>
    T* as() {
        if (getTypeId() == T::STATIC_TYPE_ID) {
            return static_cast<T*>(this);
        }
        return nullptr;
    }
};

// ===================== EXCEPTION HANDLING ABI =====================

void exception_handling_issues() {
    // Exception handling implementation varies:
    
    // 1. Itanium ABI (GCC/Clang on Unix)
    //    - Uses unwind tables
    //    - Zero-cost exceptions (when no exceptions)
    
    // 2. MSVC ABI (Windows)
    //    - Structured Exception Handling (SEH)
    //    - Different exception object layout
    
    // 3. SjLj exceptions (older GCC)
    //    - setjmp/longjmp based
    
    // Issues:
    // - Cannot throw exceptions across library boundaries
    // - Different unwinding mechanisms
    
    // Solution:
    // 1. Catch exceptions at library boundary
    // 2. Convert to error codes
    // 3. Use same compiler for all components
    // 4. Disable exceptions (-fno-exceptions) for libraries
}

// ===================== MEMORY ALLOCATOR MISMATCH =====================

void allocator_mismatch() {
    // Different parts of program may use different allocators
    
    // Issue: Memory allocated by one allocator,
    // freed by another
    
    // Common scenarios:
    // 1. Different runtime libraries (debug vs release)
    // 2. Custom allocators
    // 3. Different heaps (DLL vs executable)
    
    // Windows DLL memory issues:
    // void* mem = malloc(size);  // In DLL
    // free(mem);                 // In EXE - CRASH!
    
    // Solution:
    // 1. Provide allocation/deallocation functions
    // 2. Use same runtime library
    // 3. Use shared allocator
}

class SafeAllocator {
public:
    static void* allocate(size_t size) {
        return getInstance().alloc(size);
    }
    
    static void deallocate(void* ptr) {
        getInstance().free(ptr);
    }
    
private:
    virtual void* alloc(size_t size) = 0;
    virtual void free(void* ptr) = 0;
    
    static SafeAllocator& getInstance() {
        static SafeAllocatorImpl instance;
        return instance;
    }
};

// ===================== THREAD LOCAL STORAGE =====================

thread_local int tls_var = 42;

void tls_issues() {
    // TLS implementation varies:
    
    // 1. Compiler-specific TLS models
    //    - global-dynamic
    //    - local-dynamic
    //    - initial-exec
    //    - local-exec
    
    // 2. Different on Windows vs Unix
    
    // 3. DLL vs executable TLS
    
    // Issues:
    // - TLS may not work across library boundaries
    // - Different initialization order
    
    // Solution:
    // - Avoid TLS in library interfaces
    // - Use platform-specific TLS APIs if needed
    // - Use thread-safe singletons instead
}

// ===================== FLOATING POINT CONSISTENCY =====================

void floating_point_issues() {
    // Floating point behavior varies:
    
    // 1. Precision control
    //    - -ffast-math changes semantics
    //    - Different FPU modes
    
    // 2. Denormal handling
    //    - FTZ (Flush To Zero)
    //    - DAZ (Denormals Are Zero)
    
    // 3. SSE vs x87 FPU
    //    - Different precision
    //    - Different rounding
    
    // 4. Strict vs relaxed floating point
    
    // Issues:
    // - Different results with same inputs
    // - NaN/Inf handling differences
    
    // Solution:
    // 1. Use consistent compiler flags
    // 2. Avoid -ffast-math in libraries
    // 3. Document FP requirements
    // 4. Use fixed-point for critical calculations
}

// ===================== DEBUG VS RELEASE ABI =====================

#ifdef NDEBUG
    // Release build
    #define ASSERT(expr) ((void)0)
#else
    // Debug build
    #define ASSERT(expr) \
        if (!(expr)) { \
            std::cerr << "Assertion failed: " #expr; \
            std::terminate(); \
        }
#endif

void debug_release_issues() {
    // Issues between debug and release:
    
    // 1. Different struct padding
    //    - Debug may add padding for debugging
    
    // 2. Different inlining decisions
    //    - Debug: less inlining
    //    - Release: aggressive inlining
    
    // 3. Iterator debugging
    //    - Debug iterators have extra checks
    
    // 4. STL container debugging
    //    - Extra fields for bounds checking
    
    // Solution:
    // - Use same build type for all components
    // - Or design API to be build-type agnostic
    // - Avoid debug-only features in public API
}

// ===================== ABI DETECTION AND VERSIONING =====================

namespace ABI {
    struct Version {
        int compiler_major;
        int compiler_minor;
        int stdlib_version;
        int abi_version;
        
        bool operator==(const Version& other) const {
            return compiler_major == other.compiler_major &&
                   compiler_minor == other.compiler_minor &&
                   stdlib_version == other.stdlib_version &&
                   abi_version == other.abi_version;
        }
    };
    
    Version getCurrentVersion() {
        return Version{
#ifdef __GNUC__
            __GNUC__,
            __GNUC_MINOR__,
#else
            0, 0,
#endif
#ifdef _GLIBCXX_RELEASE
            _GLIBCXX_RELEASE,
#else
            0,
#endif
            1  // ABI version
        };
    }
    
    bool checkCompatibility(const Version& required) {
        Version current = getCurrentVersion();
        
        // Basic compatibility check
        if (current.compiler_major != required.compiler_major) {
            return false;
        }
        
        // stdlib compatibility
        if (current.stdlib_version < required.stdlib_version) {
            return false;
        }
        
        return true;
    }
}

// ===================== ABI SAFE DESIGN PATTERNS =====================

// Pattern 1: PIMPL (Pointer to Implementation)
class ABISafeClass {
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
    
public:
    ABISafeClass();
    ~ABISafeClass();
    
    // Non-copyable, non-movable in public interface
    ABISafeClass(const ABISafeClass&) = delete;
    ABISafeClass& operator=(const ABISafeClass&) = delete;
    
    // Public API - stable
    void stableMethod();
    int calculate(int x, int y);
};

// Pattern 2: C interface wrapper
extern "C" {
    void* create_abisafe();
    void destroy_abisafe(void* obj);
    void abisafe_method(void* obj);
    int abisafe_calculate(void* obj, int x, int y);
}

// Pattern 3: Versioned interfaces
class IStableInterface {
public:
    virtual ~IStableInterface() = default;
    
    virtual void method1() = 0;
    virtual int method2() = 0;
    
    // Factory with version check
    static std::unique_ptr<IStableInterface> create(int version);
};

// Pattern 4: Message-based interface
#pragma pack(push, 1)
struct Message {
    uint32_t version;
    uint32_t type;
    uint32_t size;
    char data[];  // Flexible array member
};
#pragma pack(pop)

class MessageProcessor {
public:
    static void* processMessage(const Message* msg) {
        switch (msg->version) {
            case 1:
                return processV1(msg);
            case 2:
                return processV2(msg);
            default:
                return nullptr;
        }
    }
    
private:
    static void* processV1(const Message* msg) {
        // Process version 1 message
        return nullptr;
    }
    
    static void* processV2(const Message* msg) {
        // Process version 2 message
        return nullptr;
    }
};

// ===================== ABI TESTING =====================

void test_abi_compatibility() {
    std::cout << "Testing ABI compatibility...\n";
    
    // Test 1: Size checks
    static_assert(sizeof(Data_v1) == 8, "Data_v1 size changed!");
    static_assert(offsetof(Data_v1, value) == 4, "Data_v1 layout changed!");
    
    // Test 2: Type traits
    static_assert(std::is_standard_layout<Data_v1>::value,
                  "Data_v1 must be standard layout");
    
    // Test 3: ABI version check
    ABI::Version required{9, 3, 9, 1};  // GCC 9.3, libstdc++ 9, ABI v1
    bool compatible = ABI::checkCompatibility(required);
    
    if (!compatible) {
        std::cerr << "ABI incompatible!\n";
        std::cerr << "Required: GCC " << required.compiler_major 
                  << "." << required.compiler_minor << "\n";
    }
    
    // Test 4: Ensure no RTTI in public interface
    // (Can't be enforced at compile time, but can be documented)
    
    std::cout << "ABI tests passed.\n";
}

// ===================== BUILD SYSTEM INTEGRATION =====================
/*
CMake example for ABI-safe library:

  cmake_minimum_required(VERSION 3.15)
  project(ABISafeLib)
  
  # ABI compatibility settings
  set(CMAKE_CXX_VISIBILITY_PRESET hidden)
  set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)
  
  # Strict compiler flags
  add_compile_options(
      -Wall -Wextra -Werror
      -Wno-psabi  # Disable ABI warnings
  )
  
  # ABI version definition
  add_definitions(-DLIB_ABI_VERSION=1)
  
  # Library target
  add_library(abisafe SHARED src/abisafe.cpp)
  set_target_properties(abisafe PROPERTIES
      VERSION 1.0.0
      SOVERSION 1
      CXX_VISIBILITY_PRESET hidden
  )
  
  # Export only C interface
  target_include_directories(abisafe PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include>
  )
  
  # Install with versioned library name
  install(TARGETS abisafe
      LIBRARY DESTINATION lib
      ARCHIVE DESTINATION lib
      RUNTIME DESTINATION bin
  )
*/

int main() {
    std::cout << "=== Binary Compatibility Issues ===\n\n";
    
    std::cout << "Common binary compatibility issues:\n";
    std::cout << "1. Struct layout changes\n";
    std::cout << "2. Virtual function additions\n";
    std::cout << "3. Inline function changes\n";
    std::cout << "4. Standard library version mismatches\n";
    std::cout << "5. Compiler flag differences\n";
    std::cout << "6. Name mangling differences\n";
    std::cout << "7. Template instantiation differences\n";
    std::cout << "8. RTTI implementation differences\n";
    std::cout << "9. Exception handling ABI\n";
    std::cout << "10. Memory allocator mismatches\n";
    
    std::cout << "\nBest practices:\n";
    std::cout << "- Use PIMPL pattern\n";
    std::cout << "- Provide C interface\n";
    std::cout << "- Version your API\n";
    std::cout << "- Never change existing functions\n";
    std::cout << "- Use same compiler chain\n";
    std::cout << "- Document ABI requirements\n";
    
    test_abi_compatibility();
    
    return 0;
}



