#pragma once

#ifdef _WIN32
#define IMPORT __declspec(dllimport)
#else
#define IMPORT
#endif

extern "C" {
    IMPORT int add(int a, int b);
    IMPORT int multiply(int a, int b);
}

// g++ main.cpp -L. -lrustlib -o app

