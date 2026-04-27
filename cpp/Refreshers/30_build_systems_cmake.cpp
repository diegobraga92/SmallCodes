////////* BUILD SYSTEMS & CMAKE *////////

/*
 * MODERN BUILD SYSTEMS FOR C++ PROJECTS
 * 
 * Build systems automate the compilation, linking, and packaging of C++ projects.
 * CMake is the de facto standard for modern C++ projects due to its:
 *   - Cross-platform support (Windows, Linux, macOS)
 *   - Integration with IDEs (Visual Studio, CLion, VS Code)
 *   - Package management integration (Conan, vcpkg)
 *   - Modern target-based approach (transitive dependencies)
 */

// ============================================================================
// 1. BASIC CMAKE PROJECT STRUCTURE
// ============================================================================

/*
 * Typical C++ project structure:
 * 
 * my_project/
 * ├── CMakeLists.txt          # Root build configuration
 * ├── include/
 * │   └── mylib/
 * │       └── mylib.h         # Public headers
 * ├── src/
 * │   ├── CMakeLists.txt      # Library build config
 * │   └── mylib.cpp           # Implementation
 * ├── tests/
 * │   ├── CMakeLists.txt      # Test build config
 * │   └── test_mylib.cpp      # Unit tests
 * ├── examples/
 * │   ├── CMakeLists.txt      # Examples build config
 * │   └── example.cpp
 * └── build/                  # Build artifacts (gitignored)
 */

// ============================================================================
// ROOT CMakeLists.txt - Modern CMake 3.15+ best practices
// ============================================================================

/*
cmake_minimum_required(VERSION 3.15)

# Project declaration with version
project(MyProject 
    VERSION 1.0.0
    DESCRIPTION "A modern C++ library"
    LANGUAGES CXX
)

# Require C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)  # Disable compiler-specific extensions

# Build options
option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
option(BUILD_TESTING "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)

# Add subdirectories
add_subdirectory(src)

if(BUILD_TESTING)
    enable_testing()
    add_subdirectory(tests)
endif()

if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
*/

// ============================================================================
// src/CMakeLists.txt - Library target
// ============================================================================

/*
# Create library target (MODERN approach using target-based properties)
add_library(mylib
    mylib.cpp
    ${CMAKE_SOURCE_DIR}/include/mylib/mylib.h
)

# Alias for consistent naming (myproject::mylib)
add_library(myproject::mylib ALIAS mylib)

# Target include directories
# PUBLIC: Used by library AND consumers
# PRIVATE: Used only by library
# INTERFACE: Used only by consumers
target_include_directories(mylib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# Compiler warnings (best practice: enable ALL warnings)
target_compile_options(mylib
    PRIVATE
        $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
        $<$<CXX_COMPILER_ID:MSVC>:/W4>
)

# Link dependencies (transitive dependencies automatically propagated)
target_link_libraries(mylib
    PUBLIC
        # Public dependencies (consumers need these)
    PRIVATE
        # Private dependencies (only implementation needs these)
)
*/

// ============================================================================
// 2. BUILD CONFIGURATIONS (Debug, Release, RelWithDebInfo, MinSizeRel)
// ============================================================================

/*
 * Build types control optimization levels and debug information:
 * 
 * Debug:          No optimization, full debug info
 *                 Flags: -O0 -g
 *                 Use: Development, debugging
 * 
 * Release:        Full optimization, no debug info
 *                 Flags: -O3 -DNDEBUG
 *                 Use: Production
 * 
 * RelWithDebInfo: Optimized with debug info
 *                 Flags: -O2 -g -DNDEBUG
 *                 Use: Profiling production issues
 * 
 * MinSizeRel:     Optimize for size
 *                 Flags: -Os -DNDEBUG
 *                 Use: Embedded systems
 */

// Build commands:
// cmake -B build -DCMAKE_BUILD_TYPE=Debug
// cmake -B build -DCMAKE_BUILD_TYPE=Release
// cmake --build build --config Release

#include <iostream>

void demonstrate_build_configs() {
    std::cout << "=== BUILD CONFIGURATIONS ===\n\n";
    
    // NDEBUG is defined in Release builds
    #ifdef NDEBUG
        std::cout << "Running in RELEASE mode\n";
        std::cout << "Assertions disabled, optimizations enabled\n";
    #else
        std::cout << "Running in DEBUG mode\n";
        std::cout << "Assertions enabled, no optimizations\n";
    #endif
    
    // Debug-only code
    #ifndef NDEBUG
        std::cout << "Debug-specific logging enabled\n";
    #endif
}

// ============================================================================
// 3. SANITIZERS (AddressSanitizer, ThreadSanitizer, UndefinedBehaviorSanitizer)
// ============================================================================

/*
 * Sanitizers are runtime instrumentation tools that detect bugs:
 * 
 * AddressSanitizer (ASAN):
 *   - Detects: Memory leaks, use-after-free, buffer overflows
 *   - Flags: -fsanitize=address -fno-omit-frame-pointer
 *   - Overhead: ~2x slowdown
 * 
 * ThreadSanitizer (TSAN):
 *   - Detects: Data races, deadlocks
 *   - Flags: -fsanitize=thread
 *   - Overhead: 5-15x slowdown
 *   - Note: Cannot combine with ASAN
 * 
 * UndefinedBehaviorSanitizer (UBSAN):
 *   - Detects: Integer overflow, null dereference, misaligned access
 *   - Flags: -fsanitize=undefined
 *   - Overhead: Minimal
 */

// CMakeLists.txt for sanitizers:
/*
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
option(ENABLE_TSAN "Enable ThreadSanitizer" OFF)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" OFF)

if(ENABLE_ASAN)
    target_compile_options(mylib PRIVATE -fsanitize=address -fno-omit-frame-pointer)
    target_link_options(mylib PRIVATE -fsanitize=address)
endif()

if(ENABLE_TSAN)
    target_compile_options(mylib PRIVATE -fsanitize=thread)
    target_link_options(mylib PRIVATE -fsanitize=thread)
endif()

if(ENABLE_UBSAN)
    target_compile_options(mylib PRIVATE -fsanitize=undefined)
    target_link_options(mylib PRIVATE -fsanitize=undefined)
endif()
*/

// Build with sanitizers:
// cmake -B build -DENABLE_ASAN=ON
// cmake --build build
// ./build/myapp  # Will report any memory errors

#include <memory>
#include <vector>

void demonstrate_sanitizer_detection() {
    std::cout << "\n=== SANITIZER EXAMPLES ===\n\n";
    
    // Example 1: ASAN would catch this (commented out to avoid crash)
    // int* ptr = new int(42);
    // delete ptr;
    // *ptr = 100;  // Use-after-free - ASAN detects!
    
    // Example 2: ASAN would catch this
    // std::vector<int> vec{1, 2, 3};
    // int x = vec[10];  // Buffer overflow - ASAN detects!
    
    // Example 3: UBSAN would catch this
    // int x = INT_MAX;
    // int y = x + 1;  // Integer overflow - UBSAN detects!
    
    std::cout << "Safe code - no sanitizer issues\n";
}

// ============================================================================
// 4. LINK-TIME OPTIMIZATION (LTO/IPO)
// ============================================================================

/*
 * Link-Time Optimization (LTO), also called Interprocedural Optimization (IPO):
 * 
 * What it does:
 *   - Optimizes across translation units at link time
 *   - Inlines functions across files
 *   - Removes dead code globally
 *   - Optimizes virtual function calls
 * 
 * When to use:
 *   - Production builds for maximum performance
 *   - When binary size matters
 * 
 * Trade-offs:
 *   - Pros: 10-20% performance improvement, smaller binaries
 *   - Cons: Much slower compilation, high memory usage
 */

// CMakeLists.txt for LTO:
/*
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT error)

if(ipo_supported)
    message(STATUS "LTO/IPO enabled")
    set_property(TARGET mylib PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
    message(STATUS "LTO/IPO not supported: ${error}")
endif()
*/

// Example: LTO can inline this across translation units
namespace lto_example {
    inline int add(int a, int b) {
        return a + b;
    }
    
    // Without LTO: This is a function call
    // With LTO: Compiler can inline this even if called from another .cpp file
    int compute(int x) {
        return add(x, 10) * 2;
    }
}

void demonstrate_lto() {
    std::cout << "\n=== LINK-TIME OPTIMIZATION ===\n\n";
    
    int result = lto_example::compute(5);
    std::cout << "LTO example result: " << result << "\n";
    
    std::cout << "Build with LTO:\n";
    std::cout << "  cmake -B build -DCMAKE_BUILD_TYPE=Release\n";
    std::cout << "  cmake --build build\n";
    std::cout << "Compare binary size and performance with/without LTO\n";
}

// ============================================================================
// 5. PACKAGE MANAGERS (Conan, vcpkg)
// ============================================================================

/*
 * Package managers automate dependency management:
 * 
 * CONAN:
 *   - Python-based, flexible
 *   - Binary packages (precompiled)
 *   - Custom remotes
 * 
 * VCPKG:
 *   - Microsoft-backed
 *   - Source-based (compiles on your machine)
 *   - CMake integration
 */

// ============================================================================
// CONAN EXAMPLE
// ============================================================================

/*
 * conanfile.txt:
 * 
 * [requires]
 * fmt/9.1.0
 * spdlog/1.11.0
 * boost/1.81.0
 * 
 * [generators]
 * CMakeDeps
 * CMakeToolchain
 * 
 * [options]
 * boost:shared=False
 */

// CMakeLists.txt with Conan:
/*
cmake_minimum_required(VERSION 3.15)
project(MyProject)

# Include Conan-generated files
include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)

find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)

add_executable(myapp main.cpp)
target_link_libraries(myapp PRIVATE fmt::fmt spdlog::spdlog)
*/

// Build with Conan:
// conan install . --output-folder=build --build=missing
// cmake -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
// cmake --build build

// ============================================================================
// VCPKG EXAMPLE
// ============================================================================

/*
 * Install dependencies:
 * vcpkg install fmt spdlog boost
 * 
 * CMakeLists.txt remains standard:
 * find_package(fmt CONFIG REQUIRED)
 * find_package(spdlog CONFIG REQUIRED)
 * target_link_libraries(myapp PRIVATE fmt::fmt spdlog::spdlog)
 * 
 * Build with vcpkg:
 * cmake -B build -DCMAKE_TOOLCHAIN_FILE=[vcpkg-root]/scripts/buildsystems/vcpkg.cmake
 * cmake --build build
 */

#include <string>

void demonstrate_package_managers() {
    std::cout << "\n=== PACKAGE MANAGERS ===\n\n";
    
    std::cout << "CONAN:\n";
    std::cout << "  1. Create conanfile.txt with dependencies\n";
    std::cout << "  2. conan install . --build=missing\n";
    std::cout << "  3. CMake finds dependencies automatically\n\n";
    
    std::cout << "VCPKG:\n";
    std::cout << "  1. vcpkg install <package>\n";
    std::cout << "  2. Pass toolchain file to CMake\n";
    std::cout << "  3. find_package() works out of the box\n";
}

// ============================================================================
// 6. CROSS-COMPILATION & TOOLCHAINS
// ============================================================================

/*
 * Cross-compilation builds binaries for a different platform:
 * 
 * Common scenarios:
 *   - Build for ARM on x86 (embedded systems)
 *   - Build for Android/iOS
 *   - Build for different OS (Linux -> Windows)
 * 
 * Toolchain file specifies:
 *   - Compiler paths
 *   - Sysroot (target system libraries)
 *   - Compiler flags
 *   - Target system characteristics
 */

// Example toolchain file (arm-toolchain.cmake):
/*
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# Cross-compiler paths
set(CMAKE_C_COMPILER /usr/bin/arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabihf-g++)

# Sysroot (target system root)
set(CMAKE_SYSROOT /usr/arm-linux-gnueabihf)

# Search paths
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# Optional: Add target-specific flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=armv7-a")
*/

// Build with toolchain:
// cmake -B build -DCMAKE_TOOLCHAIN_FILE=arm-toolchain.cmake
// cmake --build build

void demonstrate_cross_compilation() {
    std::cout << "\n=== CROSS-COMPILATION ===\n\n";
    
    #ifdef __arm__
        std::cout << "Running on ARM architecture\n";
    #elif defined(__x86_64__) || defined(_M_X64)
        std::cout << "Running on x86_64 architecture\n";
    #elif defined(__i386__) || defined(_M_IX86)
        std::cout << "Running on x86 architecture\n";
    #elif defined(__aarch64__)
        std::cout << "Running on ARM64 architecture\n";
    #else
        std::cout << "Running on unknown architecture\n";
    #endif
    
    std::cout << "\nCross-compile for ARM:\n";
    std::cout << "  cmake -B build -DCMAKE_TOOLCHAIN_FILE=arm-toolchain.cmake\n";
}

// ============================================================================
// 7. MODERN CMAKE BEST PRACTICES SUMMARY
// ============================================================================

/*
 * DO:
 *   ✓ Use target-based approach (target_link_libraries, target_include_directories)
 *   ✓ Use generator expressions ($<BUILD_INTERFACE:...>)
 *   ✓ Create ALIAS targets (myproject::mylib)
 *   ✓ Set CMAKE_CXX_STANDARD per target
 *   ✓ Use PUBLIC/PRIVATE/INTERFACE correctly
 *   ✓ Enable warnings (-Wall -Wextra)
 *   ✓ Use modern package managers (Conan/vcpkg)
 * 
 * DON'T:
 *   ✗ Use file(GLOB) for source files (breaks incremental builds)
 *   ✗ Modify CMAKE_CXX_FLAGS directly (use target_compile_options)
 *   ✗ Use include_directories() (use target_include_directories)
 *   ✗ Use link_directories() (use target_link_libraries with full paths)
 *   ✗ Hardcode paths (use variables and find_package)
 */

// Modern target-based approach:
/*
add_library(mylib src/mylib.cpp)
target_compile_features(mylib PUBLIC cxx_std_20)
target_compile_options(mylib PRIVATE -Wall -Wextra)
target_include_directories(mylib PUBLIC include)
target_link_libraries(mylib PUBLIC fmt::fmt PRIVATE internal_helper)
*/

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

int main() {
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║      MODERN BUILD SYSTEMS & CMAKE DEMONSTRATION          ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n\n";
    
    demonstrate_build_configs();
    demonstrate_sanitizer_detection();
    demonstrate_lto();
    demonstrate_package_managers();
    demonstrate_cross_compilation();
    
    std::cout << "\n=== CMAKE WORKFLOW SUMMARY ===\n\n";
    std::cout << "1. Configure:  cmake -B build -DCMAKE_BUILD_TYPE=Release\n";
    std::cout << "2. Build:      cmake --build build --parallel\n";
    std::cout << "3. Test:       ctest --test-dir build\n";
    std::cout << "4. Install:    cmake --install build --prefix /usr/local\n";
    
    return 0;
}

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/*
 * 1. MODERN CMAKE (3.15+):
 *    - Use target-based approach for better dependency management
 *    - Generator expressions for build/install differences
 *    - Transitive dependencies propagate automatically
 * 
 * 2. BUILD CONFIGURATIONS:
 *    - Debug: Development (-O0 -g)
 *    - Release: Production (-O3 -DNDEBUG)
 *    - Use sanitizers in CI/CD to catch bugs early
 * 
 * 3. OPTIMIZATION:
 *    - LTO/IPO: 10-20% performance gain, enable for releases
 *    - Profile-guided optimization (PGO): Collect runtime data
 *    - Compile-time options affect runtime performance significantly
 * 
 * 4. PACKAGE MANAGEMENT:
 *    - Conan: Binary packages, flexible, Python ecosystem
 *    - vcpkg: Source-based, Microsoft-backed, simple integration
 *    - Don't manage dependencies manually
 * 
 * 5. TOOLCHAINS:
 *    - Required for cross-compilation
 *    - Specify compiler, sysroot, flags
 *    - Essential for embedded/mobile development
 * 
 * Senior engineers must understand the entire build pipeline, not just code!
 */
