// ALIGNED DATA STRUCTURE

#include <cstddef>
#include <cstdlib>
#include <cassert>

// 32-byte alignment → suitable for AVX (256-bit)
// 16-byte would be enough for SSE
constexpr std::size_t ALIGN = 32;

// Allocate aligned memory helper
float* aligned_alloc_floats(std::size_t n) {
    void* p = std::aligned_alloc(ALIGN, n * sizeof(float));
    assert(p && "aligned_alloc failed");
    return static_cast<float*>(p);
}

// AUTO-VECTORIZABLE

// __restrict__ tells the compiler:
// These pointers do NOT alias → safe to vectorize
void add_arrays(float* __restrict__ a,
                const float* __restrict__ b,
                const float* __restrict__ c,
                std::size_t n)
{
    // Simple loop
    // - No branches
    // - Fixed stride
    // - Independent iterations
    for (std::size_t i = 0; i < n; ++i) {
        a[i] = b[i] + c[i];
    }
}

// AVOID Array of Structs
struct Particle {
    float x, y, z;
    float vx, vy, vz;
};

void update_bad(Particle* p, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) {
        p[i].x += p[i].vx;
    }
}


// GOOD: Struct of Arrays + SIMD
struct Particles {
    float* x;
    float* vx;
};

void update_good(Particles p, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) {
        p.x[i] += p.vx[i];
    }
}
