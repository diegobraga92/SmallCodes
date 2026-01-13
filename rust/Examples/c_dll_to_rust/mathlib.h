#pragma once

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

extern "C" {
    EXPORT int add(int a, int b);
    EXPORT int multiply(int a, int b);
}

// Build Linux: g++ -shared -fPIC mathlib.cpp -o libmathlib.so
// Build Windows: cl /LD mathlib.cpp /Fe:mathlib.dll
