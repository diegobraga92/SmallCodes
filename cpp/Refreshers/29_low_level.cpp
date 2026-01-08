/*
 * ADVANCED CPU AND MEMORY PERFORMANCE OPTIMIZATION DEMONSTRATION
 * 
 * This program demonstrates various CPU and memory optimization concepts
 * with detailed explanations for each technique.
 */

#include <iostream>
#include <vector>
#include <array>
#include <chrono>
#include <thread>
#include <algorithm>
#include <immintrin.h>  // For SIMD intrinsics (AVX, SSE)
#include <atomic>
#include <cstring>
#include <cmath>
#include <random>
#include <sys/mman.h>  // For memory alignment
#include <unistd.h>   // For sysconf
#include <memory>
#include <new>
#include <list>
#include <map>

// ============================================================================
// 1. BRANCH PREDICTION
// ============================================================================
/*
 * Branch Prediction: Modern CPUs predict which way branches will go to 
 * avoid pipeline stalls. Mispredictions cause ~10-20 cycle penalties.
 * Tips: Write predictable code, use __builtin_expect for GCC/Clang
 */
void demonstrate_branch_prediction() {
    std::cout << "\n=== 1. Branch Prediction Demo ===\n";
    
    // Create sorted and unsorted data
    const int size = 100000;
    std::vector<int> sorted_data(size);
    std::vector<int> unsorted_data(size);
    
    for (int i = 0; i < size; i++) {
        sorted_data[i] = i;
        unsorted_data[i] = rand() % 100;
    }
    
    // Warm up (avoid cold cache effects)
    volatile int warmup = 0;
    for (int i = 0; i < size; i++) {
        warmup += sorted_data[i];
    }
    
    // Test with sorted data (highly predictable branches)
    auto start = std::chrono::high_resolution_clock::now();
    int sum_sorted = 0;
    for (int i = 0; i < size; i++) {
        // This branch is highly predictable with sorted data
        if (sorted_data[i] < 50000) {
            sum_sorted += sorted_data[i];
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto sorted_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // Test with unsorted data (unpredictable branches)
    start = std::chrono::high_resolution_clock::now();
    int sum_unsorted = 0;
    for (int i = 0; i < size; i++) {
        // This branch is unpredictable with random data
        if (unsorted_data[i] < 50) {
            sum_unsorted += unsorted_data[i];
        }
    }
    end = std::chrono::high_resolution_clock::now();
    auto unsorted_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Sorted data time: " << sorted_time.count() << "μs\n";
    std::cout << "Unsorted data time: " << unsorted_time.count() << "μs\n";
    std::cout << "Branch prediction impact: " 
              << (double)unsorted_time.count() / sorted_time.count() 
              << "x slower with unpredictable branches\n";
    
    // Demonstrate branchless programming
    // Instead of: if (x > y) result = a; else result = b;
    // Use: result = (x > y) * a + (x <= y) * b;
    int x = 10, y = 20, a = 100, b = 200;
    int result_branch = (x > y) ? a : b;  // Uses branch
    int result_branchless = ((x > y) & a) | ((x <= y) & b);  // Branchless
    
    std::cout << "Branch result: " << result_branch << "\n";
    std::cout << "Branchless result: " << result_branchless << "\n";
}

// ============================================================================
// 2. CACHE LINE AWARENESS AND FALSE SHARING
// ============================================================================
/*
 * Cache Line: Smallest unit of memory transfer between CPU caches.
 * Typically 64 bytes on x86-64. False sharing occurs when two threads
 * modify different variables that happen to be on the same cache line.
 */
struct BadCacheAlignment {
    int thread1_counter;  // 4 bytes
    int thread2_counter;  // 4 bytes - SHARES CACHE LINE with thread1_counter!
    // Total: 8 bytes, fits in one 64-byte cache line
    // Cache line bouncing: Core 1 writes, invalidates Core 2's cache line
};

struct GoodCacheAlignment {
    alignas(64) int thread1_counter;  // Force to separate cache line
    char padding[60];                 // Explicit padding to ensure separation
    alignas(64) int thread2_counter;  // Force to separate cache line
    char padding2[60];                // More padding
};

void demonstrate_false_sharing() {
    std::cout << "\n=== 2. False Sharing Demo ===\n";
    
    const int iterations = 100000000;
    BadCacheAlignment bad;
    GoodCacheAlignment good;
    
    auto bad_start = std::chrono::high_resolution_clock::now();
    
    // Two threads modifying adjacent data on same cache line
    std::thread t1([&]() {
        for (int i = 0; i < iterations; i++) {
            bad.thread1_counter++;  // Core 1 modifies its cache line
        }
    });
    
    std::thread t2([&]() {
        for (int i = 0; i < iterations; i++) {
            bad.thread2_counter++;  // Core 2 modifies same cache line
            // Causes cache line bouncing between cores!
        }
    });
    
    t1.join();
    t2.join();
    auto bad_end = std::chrono::high_resolution_clock::now();
    
    auto good_start = std::chrono::high_resolution_clock::now();
    
    // Two threads modifying data on separate cache lines
    std::thread t3([&]() {
        for (int i = 0; i < iterations; i++) {
            good.thread1_counter++;  // Core 1 modifies its own cache line
        }
    });
    
    std::thread t4([&]() {
        for (int i = 0; i < iterations; i++) {
            good.thread2_counter++;  // Core 2 modifies different cache line
            // No bouncing between cores!
        }
    });
    
    t3.join();
    t4.join();
    auto good_end = std::chrono::high_resolution_clock::now();
    
    auto bad_time = std::chrono::duration_cast<std::chrono::milliseconds>(bad_end - bad_start);
    auto good_time = std::chrono::duration_cast<std::chrono::milliseconds>(good_end - good_start);
    
    std::cout << "With false sharing: " << bad_time.count() << "ms\n";
    std::cout << "Without false sharing: " << good_time.count() << "ms\n";
    std::cout << "Improvement: " << (double)bad_time.count() / good_time.count() << "x\n";
    
    // Detect cache line size
    std::cout << "Cache line size (detected): " << sysconf(_SC_LEVEL1_DCACHE_LINESIZE) << " bytes\n";
}

// ============================================================================
// 3. CACHE MISSES AND PREFETCHING
// ============================================================================
/*
 * Cache Miss Types:
 * - Compulsory (cold): First access to memory
 * - Capacity: Cache is too small for working set
 * - Conflict: Multiple memory locations map to same cache set
 * 
 * Prefetching: CPU or software attempts to load data into cache before it's needed
 */
void demonstrate_cache_effects() {
    std::cout << "\n=== 3. Cache Effects and Prefetching Demo ===\n";
    
    const int size = 64 * 1024 * 1024; // 64MB, larger than typical L3 cache
    int* data = new int[size];
    
    // Initialize with random access pattern
    for (int i = 0; i < size; i++) {
        data[i] = i;
    }
    
    // Test 1: Sequential access (good spatial locality, prefetcher works well)
    auto start = std::chrono::high_resolution_clock::now();
    int sum1 = 0;
    for (int i = 0; i < size; i++) {
        sum1 += data[i];  // Hardware prefetcher detects sequential pattern
    }
    auto mid = std::chrono::high_resolution_clock::now();
    
    // Test 2: Random access (poor locality, many cache misses)
    int sum2 = 0;
    std::vector<int> indices(size);
    for (int i = 0; i < size; i++) indices[i] = i;
    std::shuffle(indices.begin(), indices.end(), std::mt19937{std::random_device{}()});
    
    for (int i = 0; i < size; i++) {
        sum2 += data[indices[i]];  // Random access defeats prefetcher
    }
    auto end = std::chrono::high_resolution_clock::now();
    
    auto sequential_time = std::chrono::duration_cast<std::chrono::milliseconds>(mid - start);
    auto random_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - mid);
    
    std::cout << "Sequential access: " << sequential_time.count() << "ms\n";
    std::cout << "Random access: " << random_time.count() << "ms\n";
    std::cout << "Cache effect: " << (double)random_time.count() / sequential_time.count() 
              << "x slower with random access\n";
    
    // Demonstrate software prefetching
    const int prefetch_distance = 16; // How far ahead to prefetch
    start = std::chrono::high_resolution_clock::now();
    int sum3 = 0;
    for (int i = 0; i < size; i++) {
        if (i + prefetch_distance < size) {
            __builtin_prefetch(&data[i + prefetch_distance], 0, 1); // Prefetch for read
        }
        sum3 += data[i];
    }
    end = std::chrono::high_resolution_clock::now();
    auto prefetch_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "With software prefetching: " << prefetch_time.count() << "ms\n";
    
    delete[] data;
}

// ============================================================================
// 4. STRUCT PADDING, ALIGNING, AND PACKING
// ============================================================================
/*
 * Padding: Compiler adds unused bytes to align struct members for CPU
 * Alignment: Memory addresses should be multiples of data type size
 * Packing: Force compiler to not add padding (may cause performance penalty)
 */
#pragma pack(push, 1)  // Start packing - disable padding
struct PackedStruct {
    char a;     // 1 byte at offset 0
    int b;      // 4 bytes at offset 1 (UNALIGNED - SLOW!)
    double c;   // 8 bytes at offset 5 (UNALIGNED - SLOW!)
    char d;     // 1 byte at offset 13
    // Total with packing: 1 + 4 + 8 + 1 = 14 bytes
    // Without packing (alignment): 1 + 3(pad) + 4 + 8 + 1 + 7(pad) = 24 bytes
};
#pragma pack(pop)  // End packing

struct AlignedStruct {
    alignas(64) char a;     // Align to 64-byte boundary (cache line)
    alignas(16) int b;      // Align to 16-byte boundary (SSE/AVX)
    double c;
    char d;
};

// Reorder struct members for better packing
struct OptimizedStruct {
    double c;   // 8 bytes at offset 0
    int b;      // 4 bytes at offset 8
    char a;     // 1 byte at offset 12
    char d;     // 1 byte at offset 13
    // Total: 14 bytes with good alignment, only 2 bytes padding at end if in array
};

void demonstrate_struct_layout() {
    std::cout << "\n=== 4. Struct Layout Demo ===\n";
    
    PackedStruct packed;
    AlignedStruct aligned;
    struct NormalStruct {
        char a;    // 1 byte at offset 0
        // 3 bytes padding here for alignment
        int b;     // 4 bytes at offset 4
        double c;  // 8 bytes at offset 8
        char d;    // 1 byte at offset 16
        // 7 bytes padding here (array alignment)
    } normal;
    
    OptimizedStruct optimized;
    
    std::cout << "Sizeof PackedStruct: " << sizeof(PackedStruct) << " bytes\n";
    std::cout << "Sizeof NormalStruct: " << sizeof(NormalStruct) << " bytes\n";
    std::cout << "Sizeof AlignedStruct: " << sizeof(AlignedStruct) << " bytes\n";
    std::cout << "Sizeof OptimizedStruct: " << sizeof(OptimizedStruct) << " bytes\n";
    
    // Show memory layout
    std::cout << "\nMemory addresses:\n";
    std::cout << "NormalStruct.a: " << (void*)&normal.a << "\n";
    std::cout << "NormalStruct.b: " << (void*)&normal.b << " (4-byte aligned)\n";
    std::cout << "NormalStruct.c: " << (void*)&normal.c << " (8-byte aligned)\n";
    
    // Demonstrate performance difference
    const int iterations = 10000000;
    std::vector<PackedStruct> packed_vec(iterations);
    std::vector<NormalStruct> normal_vec(iterations);
    
    // Access patterns show performance differences
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; i++) {
        normal_vec[i].b = i;  // Aligned access - fast
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto normal_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; i++) {
        packed_vec[i].b = i;  // Unaligned access - slow (causes bus error on some CPUs)
    }
    end = std::chrono::high_resolution_clock::now();
    auto packed_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "\nNormal struct access time: " << normal_time.count() << "μs\n";
    std::cout << "Packed struct access time: " << packed_time.count() << "μs\n";
    std::cout << "Note: Packed may be slower due to unaligned memory access\n";
    std::cout << "Unaligned access penalty: 2-3x on modern CPUs, crash on older CPUs\n";
}

// ============================================================================
// 15. MEMORY ORDERING AND ATOMIC OPERATIONS
// ============================================================================
/*
 * Memory Ordering: Controls how memory operations are ordered across threads
 * 
 * Memory Order Models:
 * - memory_order_seq_cst: Sequential consistency (default) - strongest
 * - memory_order_acq_rel: Acquire-release semantics
 * - memory_order_acquire: Load operation - prevents subsequent reads/writes from moving before
 * - memory_order_release: Store operation - prevents previous reads/writes from moving after
 * - memory_order_consume: Data dependency ordering (deprecated)
 * - memory_order_relaxed: No ordering guarantees, just atomicity
 * 
 * Happens-before relationship: Critical for correct concurrent code
 */
std::atomic<int> shared_data(0);
std::atomic<bool> ready(false);
int non_atomic_data = 0;

void producer_thread() {
    // Write data
    non_atomic_data = 42;
    
    // Release store: Ensures all previous writes are visible to consumer
    ready.store(true, std::memory_order_release);
    // Equivalent to: store with release fence
    // atomic_thread_fence(std::memory_order_release);
    // ready.store(true, std::memory_order_relaxed);
}

void consumer_thread() {
    // Acquire load: Wait until producer's writes are visible
    while (!ready.load(std::memory_order_acquire)) {
        // Spin wait
        std::this_thread::yield();
    }
    
    // Now we can safely read non_atomic_data
    // Due to acquire-release pairing, we see non_atomic_data = 42
    std::cout << "Consumed data: " << non_atomic_data << "\n";
}

void demonstrate_memory_ordering() {
    std::cout << "\n=== 15. Memory Ordering Demo ===\n";
    
    // Demonstrate different memory ordering semantics
    std::atomic<int> x(0), y(0);
    int r1 = 0, r2 = 0;
    
    // Thread 1
    std::thread t1([&]() {
        x.store(1, std::memory_order_relaxed);  // Can be reordered
        y.store(1, std::memory_order_release);  // Creates release fence
    });
    
    // Thread 2
    std::thread t2([&]() {
        r1 = y.load(std::memory_order_acquire);  // Acquire load
        r2 = x.load(std::memory_order_relaxed);
    });
    
    t1.join();
    t2.join();
    
    std::cout << "With acquire-release: r1=" << r1 << ", r2=" << r2 << "\n";
    std::cout << "Important: If r1==1, then r2 must also be 1 due to happens-before\n";
    
    // Demonstrate sequential consistency (strongest, but slowest)
    std::atomic<int> seq_cst_var(0);
    
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1000000; i++) {
        seq_cst_var.store(i, std::memory_order_seq_cst);  // Full memory fence
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto seq_cst_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 1000000; i++) {
        seq_cst_var.store(i, std::memory_order_relaxed);  // No ordering guarantees
    }
    end = std::chrono::high_resolution_clock::now();
    auto relaxed_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "\nPerformance comparison:\n";
    std::cout << "Sequential consistency: " << seq_cst_time.count() << "μs\n";
    std::cout << "Relaxed ordering: " << relaxed_time.count() << "μs\n";
    std::cout << "Speedup: " << (double)seq_cst_time.count() / relaxed_time.count() << "x\n";
    
    // Demonstrate the classic Peterson's algorithm with memory ordering
    std::cout << "\nPeterson's Lock with proper memory ordering:\n";
    
    std::atomic<bool> flag[2] = {false, false};
    std::atomic<int> turn(0);
    
    auto lock = [&](int id) {
        int other = 1 - id;
        flag[id].store(true, std::memory_order_relaxed);
        turn.store(other, std::memory_order_relaxed);
        
        // Critical: This fence creates the necessary ordering
        std::atomic_thread_fence(std::memory_order_seq_cst);
        
        // Wait while other thread wants to enter and it's their turn
        while (flag[other].load(std::memory_order_relaxed) && 
               turn.load(std::memory_order_relaxed) == other) {
            std::this_thread::yield();
        }
    };
    
    auto unlock = [&](int id) {
        flag[id].store(false, std::memory_order_relaxed);
    };
    
    // Test the lock
    int shared_counter = 0;
    std::thread thread_a([&]() {
        lock(0);
        shared_counter++;
        unlock(0);
    });
    
    std::thread thread_b([&]() {
        lock(1);
        shared_counter++;
        unlock(1);
    });
    
    thread_a.join();
    thread_b.join();
    
    std::cout << "Shared counter after Peterson's lock: " << shared_counter << "\n";
}

// ============================================================================
// 16. CUSTOM ALLOCATORS
// ============================================================================
/*
 * Custom Allocators: Override default memory allocation behavior
 * 
 * Why use custom allocators:
 * 1. Improve performance (avoid malloc/free overhead)
 * 2. Reduce fragmentation
 * 3. Memory pooling for specific types
 * 4. Arena/Stack allocation
 * 5. Alignment guarantees
 * 6. Debugging and profiling
 * 
 * Types of allocators:
 * - Linear/Stack allocator
 * - Pool allocator
 * - Free list allocator
 * - Buddy allocator
 * - Slab allocator
 */

// Simple linear (arena) allocator
class LinearAllocator {
private:
    char* memory;
    char* current;
    size_t size;
    size_t used;
    
public:
    LinearAllocator(size_t total_size) {
        memory = static_cast<char*>(malloc(total_size));
        current = memory;
        size = total_size;
        used = 0;
    }
    
    ~LinearAllocator() {
        free(memory);
    }
    
    void* allocate(size_t bytes, size_t alignment = alignof(std::max_align_t)) {
        // Calculate aligned address
        uintptr_t addr = reinterpret_cast<uintptr_t>(current);
        uintptr_t aligned_addr = (addr + alignment - 1) & ~(alignment - 1);
        size_t padding = aligned_addr - addr;
        
        if (used + bytes + padding > size) {
            throw std::bad_alloc();
        }
        
        current = reinterpret_cast<char*>(aligned_addr) + bytes;
        used += bytes + padding;
        
        return reinterpret_cast<void*>(aligned_addr);
    }
    
    void reset() {
        current = memory;
        used = 0;
    }
    
    size_t get_used() const { return used; }
    size_t get_size() const { return size; }
};

// Pool allocator for fixed-size objects
template<typename T, size_t PoolSize = 1024>
class PoolAllocator {
private:
    union Node {
        T data;
        Node* next;
    };
    
    Node* free_list;
    std::vector<Node*> blocks;
    
public:
    PoolAllocator() : free_list(nullptr) {
        // Allocate first block
        allocate_block();
    }
    
    ~PoolAllocator() {
        for (auto block : blocks) {
            ::operator delete(block);
        }
    }
    
    void* allocate() {
        if (!free_list) {
            allocate_block();
        }
        
        Node* node = free_list;
        free_list = free_list->next;
        return reinterpret_cast<void*>(node);
    }
    
    void deallocate(void* ptr) {
        Node* node = static_cast<Node*>(ptr);
        node->next = free_list;
        free_list = node;
    }
    
private:
    void allocate_block() {
        Node* block = static_cast<Node*>(::operator new(sizeof(Node) * PoolSize));
        blocks.push_back(block);
        
        // Build free list
        for (size_t i = 0; i < PoolSize - 1; i++) {
            block[i].next = &block[i + 1];
        }
        block[PoolSize - 1].next = nullptr;
        
        free_list = block;
    }
};

// Custom STL allocator using our pool
template<typename T>
class CustomAllocator {
private:
    static PoolAllocator<T, 1024> pool;
    
public:
    using value_type = T;
    
    CustomAllocator() = default;
    
    template<typename U>
    CustomAllocator(const CustomAllocator<U>&) {}
    
    T* allocate(size_t n) {
        if (n != 1) {
            // Fall back to standard allocator for arrays
            return static_cast<T*>(::operator new(n * sizeof(T)));
        }
        return static_cast<T*>(pool.allocate());
    }
    
    void deallocate(T* p, size_t n) {
        if (n == 1) {
            pool.deallocate(p);
        } else {
            ::operator delete(p);
        }
    }
    
    template<typename U>
    bool operator==(const CustomAllocator<U>&) const { return true; }
    
    template<typename U>
    bool operator!=(const CustomAllocator<U>&) const { return false; }
};

template<typename T>
PoolAllocator<T, 1024> CustomAllocator<T>::pool;

// Stack allocator (like alloca but safer)
class StackAllocator {
private:
    static constexpr size_t STACK_SIZE = 1024 * 1024; // 1MB
    alignas(64) char stack[STACK_SIZE];
    char* top;
    
public:
    StackAllocator() : top(stack) {}
    
    void* allocate(size_t size, size_t alignment = alignof(std::max_align_t)) {
        uintptr_t addr = reinterpret_cast<uintptr_t>(top);
        uintptr_t aligned_addr = (addr + alignment - 1) & ~(alignment - 1);
        size_t padding = aligned_addr - addr;
        
        if (aligned_addr + size > reinterpret_cast<uintptr_t>(stack + STACK_SIZE)) {
            throw std::bad_alloc();
        }
        
        top = reinterpret_cast<char*>(aligned_addr + size);
        return reinterpret_cast<void*>(aligned_addr);
    }
    
    void reset() {
        top = stack;
    }
    
    template<typename T, typename... Args>
    T* allocate_object(Args&&... args) {
        void* mem = allocate(sizeof(T), alignof(T));
        return new (mem) T(std::forward<Args>(args)...);
    }
};

// Demonstrate alignment-aware allocator
class AlignedAllocator {
public:
    static void* allocate_aligned(size_t size, size_t alignment) {
        // Using POSIX memalign
        void* ptr = nullptr;
        if (posix_memalign(&ptr, alignment, size) != 0) {
            throw std::bad_alloc();
        }
        return ptr;
    }
    
    static void free_aligned(void* ptr) {
        free(ptr);
    }
};

void demonstrate_custom_allocators() {
    std::cout << "\n=== 16. Custom Allocators Demo ===\n";
    
    // Test linear allocator (fast allocation, but can't free individually)
    {
        std::cout << "\n1. Linear Allocator (Arena):\n";
        LinearAllocator arena(1024 * 1024); // 1MB arena
        
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 100000; i++) {
            int* p = static_cast<int*>(arena.allocate(sizeof(int), alignof(int)));
            *p = i;
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto arena_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        std::cout << "Arena allocation time: " << arena_time.count() << "μs\n";
        std::cout << "Memory used: " << arena.get_used() << " bytes\n";
        
        // Reset and reuse
        arena.reset();
        std::cout << "After reset: " << arena.get_used() << " bytes used\n";
    }
    
    // Test pool allocator (fast allocation/deallocation of fixed-size objects)
    {
        std::cout << "\n2. Pool Allocator:\n";
        PoolAllocator<int, 1000> pool;
        
        std::vector<int*, CustomAllocator<int*>> pointers;
        
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 1000; i++) {
            int* p = static_cast<int*>(pool.allocate());
            *p = i;
            pointers.push_back(p);
        }
        auto mid = std::chrono::high_resolution_clock::now();
        
        // Deallocate
        for (auto p : pointers) {
            pool.deallocate(p);
        }
        auto end = std::chrono::high_resolution_clock::now();
        
        auto alloc_time = std::chrono::duration_cast<std::chrono::microseconds>(mid - start);
        auto dealloc_time = std::chrono::duration_cast<std::chrono::microseconds>(end - mid);
        
        std::cout << "Pool allocation time: " << alloc_time.count() << "μs\n";
        std::cout << "Pool deallocation time: " << dealloc_time.count() << "μs\n";
    }
    
    // Compare with standard allocator
    {
        std::cout << "\n3. Standard vs Custom Allocator Performance:\n";
        
        const int iterations = 10000;
        
        // Standard vector
        auto start = std::chrono::high_resolution_clock::now();
        std::vector<int> std_vec;
        std_vec.reserve(iterations);
        for (int i = 0; i < iterations; i++) {
            std_vec.push_back(i);
        }
        auto end = std::chrono::high_resolution_clock::now();
        auto std_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        // Vector with custom allocator
        start = std::chrono::high_resolution_clock::now();
        std::vector<int, CustomAllocator<int>> custom_vec;
        custom_vec.reserve(iterations);
        for (int i = 0; i < iterations; i++) {
            custom_vec.push_back(i);
        }
        end = std::chrono::high_resolution_clock::now();
        auto custom_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        std::cout << "Standard allocator time: " << std_time.count() << "μs\n";
        std::cout << "Custom allocator time: " << custom_time.count() << "μs\n";
        std::cout << "Improvement: " << (double)std_time.count() / custom_time.count() << "x\n";
    }
    
    // Demonstrate stack allocator
    {
        std::cout << "\n4. Stack Allocator:\n";
        StackAllocator stack_alloc;
        
        // Allocate various types with proper alignment
        int* int_ptr = stack_alloc.allocate_object<int>(42);
        double* double_ptr = stack_alloc.allocate_object<double>(3.14159);
        
        std::cout << "Stack allocated int: " << *int_ptr << "\n";
        std::cout << "Stack allocated double: " << *double_ptr << "\n";
        
        // Can't individually free, but reset everything
        stack_alloc.reset();
    }
    
    // Demonstrate aligned allocation for SIMD
    {
        std::cout << "\n5. Aligned Allocation for SIMD:\n";
        
        // Allocate memory aligned to 32 bytes for AVX
        const size_t alignment = 32;
        const size_t num_elements = 1024;
        const size_t size = num_elements * sizeof(float);
        
        float* aligned_mem = static_cast<float*>(AlignedAllocator::allocate_aligned(size, alignment));
        
        std::cout << "Memory address: " << aligned_mem << "\n";
        std::cout << "Address is 32-byte aligned: " 
                  << ((reinterpret_cast<uintptr_t>(aligned_mem) % alignment) == 0) << "\n";
        
        // Use with SIMD
        #ifdef __AVX__
        __m256 avx_vec = _mm256_load_ps(aligned_mem);
        #endif
        
        AlignedAllocator::free_aligned(aligned_mem);
    }
    
    // Demonstrate memory pool for specific type
    {
        std::cout << "\n6. Memory Pool for Specific Type:\n";
        
        struct ExpensiveObject {
            std::array<double, 100> data;
            int id;
            
            ExpensiveObject(int i) : id(i) {
                // Simulate expensive construction
                for (auto& d : data) d = i * 3.14159;
            }
            
            ~ExpensiveObject() {
                // Simulate expensive destruction
            }
        };
        
        // Custom allocator for ExpensiveObject
        using ObjectAllocator = CustomAllocator<ExpensiveObject>;
        std::vector<ExpensiveObject, ObjectAllocator> objects;
        
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < 1000; i++) {
            objects.emplace_back(i);  // Uses custom allocator
        }
        auto end = std::chrono::high_resolution_clock::now();
        
        auto pool_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Pool allocation for expensive objects: " << pool_time.count() << "μs\n";
    }
}

// ============================================================================
// 5. HAZARDS AND STALLS
// ============================================================================
void demonstrate_data_hazards() {
    std::cout << "\n=== 5. Data Hazards Demo ===\n";
    
    // RAW (Read After Write) hazard example
    int a = 10, b = 20, c = 30;
    
    // Original code with hazards
    a = b + c;    // Write to a
    b = a + 5;    // Read from a (RAW hazard - depends on previous instruction)
    c = b * 2;    // Read from b (another RAW hazard)
    
    // Reordered to reduce stalls (if dependencies allow)
    int temp1 = b + c;
    int temp2 = temp1 + 5;
    a = temp1;
    b = temp2;
    c = temp2 * 2;
    
    std::cout << "After hazard resolution: a=" << a << ", b=" << b << ", c=" << c << "\n";
}

// ============================================================================
// MAIN FUNCTION
// ============================================================================
int main() {
    std::cout << "CPU and Memory Performance Optimization Demonstrations\n";
    std::cout << "=====================================================\n";
    
    // Run demonstrations
    demonstrate_branch_prediction();
    demonstrate_false_sharing();
    demonstrate_cache_effects();
    demonstrate_struct_layout();
    demonstrate_data_hazards();
    demonstrate_memory_ordering();
    demonstrate_custom_allocators();
    
    std::cout << "\n=====================================================\n";
    std::cout << "All demonstrations completed.\n";
    
    return 0;
}