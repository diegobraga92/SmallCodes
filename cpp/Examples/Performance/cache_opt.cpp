#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <cstdint>
#include <chrono>

constexpr std::size_t CACHE_LINE = 64;
constexpr int ITERATIONS = 1'000'000;

/* ============================================================
   SECTION 1: FALSE SHARING (BAD EXAMPLE)
   ============================================================ */

// Two counters in the same cache line → false sharing
struct StatsBad {
    uint64_t sent;
    uint64_t received;
};

StatsBad stats_bad{0, 0};

void sender_bad() {
    for (int i = 0; i < ITERATIONS; ++i) {
        stats_bad.sent++;
    }
}

void receiver_bad() {
    for (int i = 0; i < ITERATIONS; ++i) {
        stats_bad.received++;
    }
}

/* ============================================================
   SECTION 2: FALSE SHARING FIX (CACHE-LINE SEPARATION)
   ============================================================ */

struct alignas(CACHE_LINE) StatsGood {
    uint64_t sent;
    char pad1[CACHE_LINE - sizeof(uint64_t)];

    uint64_t received;
    char pad2[CACHE_LINE - sizeof(uint64_t)];
};

StatsGood stats_good{};

void sender_good() {
    for (int i = 0; i < ITERATIONS; ++i) {
        stats_good.sent++;
    }
}

void receiver_good() {
    for (int i = 0; i < ITERATIONS; ++i) {
        stats_good.received++;
    }
}

/* ============================================================
   SECTION 3: AoS vs SoA (CACHE LOCALITY)
   ============================================================ */

constexpr int N = 1024;

// Array of Structures (AoS) — cache-inefficient for partial access
struct ParticleAoS {
    float x, y, z;
    float vx, vy, vz;
};

std::vector<ParticleAoS> particles_aos(N);

// Structure of Arrays (SoA) — cache-friendly
struct ParticlesSoA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;

    ParticlesSoA(int n)
        : x(n), y(n), z(n), vx(n), vy(n), vz(n) {}
};

ParticlesSoA particles_soa(N);

void update_aos() {
    for (int i = 0; i < N; ++i) {
        particles_aos[i].x += particles_aos[i].vx;
    }
}

void update_soa() {
    for (int i = 0; i < N; ++i) {
        particles_soa.x[i] += particles_soa.vx[i];
    }
}

/* ============================================================
   SECTION 4: PER-THREAD DATA (BEST PRACTICE)
   ============================================================ */

// Each thread owns its own cache line → no contention
struct alignas(CACHE_LINE) ThreadStats {
    uint64_t count = 0;
};

void worker(ThreadStats& stats) {
    for (int i = 0; i < ITERATIONS; ++i) {
        stats.count++;
    }
}

/* ============================================================
   SECTION 5: ATOMICS & FALSE SHARING
   ============================================================ */

// Bad: atomics share cache line
struct AtomicBad {
    std::atomic<uint64_t> a;
    std::atomic<uint64_t> b;
};

// Good: atomics separated by cache lines
struct AtomicGood {
    alignas(CACHE_LINE) std::atomic<uint64_t> a;
    alignas(CACHE_LINE) std::atomic<uint64_t> b;
};

/* ============================================================
   SECTION 6: MAIN DEMO
   ============================================================ */

int main() {
    std::cout << "=== FALSE SHARING (BAD) ===\n";
    {
        std::thread t1(sender_bad);
        std::thread t2(receiver_bad);
        t1.join();
        t2.join();
        std::cout << "sent=" << stats_bad.sent
                  << " received=" << stats_bad.received << "\n";
    }

    std::cout << "\n=== FALSE SHARING FIXED ===\n";
    {
        std::thread t1(sender_good);
        std::thread t2(receiver_good);
        t1.join();
        t2.join();
        std::cout << "sent=" << stats_good.sent
                  << " received=" << stats_good.received << "\n";
    }

    std::cout << "\n=== AoS vs SoA UPDATE ===\n";
    update_aos();
    update_soa();
    std::cout << "AoS x[0]=" << particles_aos[0].x
              << " SoA x[0]=" << particles_soa.x[0] << "\n";

    std::cout << "\n=== PER-THREAD STATS ===\n";
    ThreadStats s1, s2;
    std::thread w1(worker, std::ref(s1));
    std::thread w2(worker, std::ref(s2));
    w1.join();
    w2.join();
    std::cout << "Total = " << (s1.count + s2.count) << "\n";

    std::cout << "\n=== ATOMIC FALSE SHARING NOTE ===\n";
    std::cout << "AtomicBad shares cache line → contention\n";
    std::cout << "AtomicGood separates cache lines → scalable\n";
}
