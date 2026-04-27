////////* CUSTOM ALLOCATORS & ADVANCED MEMORY MANAGEMENT *////////

/*
 * ADVANCED MEMORY MANAGEMENT IN C++
 * 
 * Standard allocator (malloc/new) is general-purpose but not always optimal:
 *   - Slow for many small allocations
 *   - Fragmentation over time
 *   - Cache-unfriendly
 * 
 * Custom allocators solve specific problems:
 *   - Pool allocators: Pre-allocate fixed-size blocks
 *   - Arena/Stack allocators: Allocate from contiguous buffer
 *   - PMR (C++17): Polymorphic Memory Resources
 * 
 * When to use:
 *   - Performance-critical code with many allocations
 *   - Real-time systems (need predictable timing)
 *   - Memory-constrained environments
 */

#include <iostream>
#include <vector>
#include <memory>
#include <chrono>
#include <list>
#include <memory_resource>  // C++17 PMR

// ============================================================================
// 1. STD::ALLOCATOR INTERFACE
// ============================================================================

/*
 * C++17 allocator requirements (minimal):
 *   - value_type: Type being allocated
 *   - allocate(n): Allocate memory for n objects
 *   - deallocate(p, n): Free memory at p
 * 
 * Optional (for optimization):
 *   - construct(p, args...): Construct object at p
 *   - destroy(p): Destroy object at p
 *   - Equality operators
 */

// Simple logging allocator (wraps std::allocator)
template<typename T>
class LoggingAllocator {
public:
    using value_type = T;
    
    LoggingAllocator() = default;
    
    template<typename U>
    LoggingAllocator(const LoggingAllocator<U>&) noexcept {}
    
    T* allocate(std::size_t n) {
        std::cout << "  [Allocator] Allocating " << n << " objects of size " 
                  << sizeof(T) << " = " << (n * sizeof(T)) << " bytes\n";
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    
    void deallocate(T* p, std::size_t n) noexcept {
        std::cout << "  [Allocator] Deallocating " << n << " objects\n";
        ::operator delete(p);
    }
    
    template<typename U>
    bool operator==(const LoggingAllocator<U>&) const noexcept { return true; }
    
    template<typename U>
    bool operator!=(const LoggingAllocator<U>&) const noexcept { return false; }
};

void demonstrate_allocator_interface() {
    std::cout << "=== ALLOCATOR INTERFACE ===\n\n";
    
    std::cout << "Creating vector with custom allocator:\n";
    std::vector<int, LoggingAllocator<int>> vec;
    
    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);
    
    std::cout << "\nVector contents: ";
    for (int n : vec) {
        std::cout << n << " ";
    }
    std::cout << "\n";
}

// ============================================================================
// 2. POOL ALLOCATOR (Fixed-size block allocation)
// ============================================================================

/*
 * Pool Allocator:
 *   - Pre-allocates many fixed-size blocks
 *   - Allocation: Pop from free list (O(1))
 *   - Deallocation: Push to free list (O(1))
 * 
 * Use cases:
 *   - Many allocations of same size (e.g., std::list nodes)
 *   - Avoid fragmentation
 *   - Predictable performance
 * 
 * Trade-offs:
 *   + Very fast allocation/deallocation
 *   + No fragmentation
 *   - Only for fixed size
 *   - Wastes memory if size varies
 */

template<typename T, std::size_t PoolSize = 1024>
class PoolAllocator {
private:
    struct Block {
        union {
            T data;              // When in use
            Block* next;         // When free
        };
    };
    
    Block* free_list = nullptr;
    std::vector<std::unique_ptr<Block[]>> pools;
    
    void allocate_pool() {
        auto pool = std::make_unique<Block[]>(PoolSize);
        
        // Link all blocks in free list
        for (std::size_t i = 0; i < PoolSize - 1; ++i) {
            pool[i].next = &pool[i + 1];
        }
        pool[PoolSize - 1].next = free_list;
        free_list = &pool[0];
        
        pools.push_back(std::move(pool));
    }
    
public:
    using value_type = T;
    
    PoolAllocator() {
        allocate_pool();
    }
    
    template<typename U>
    PoolAllocator(const PoolAllocator<U, PoolSize>&) noexcept {}
    
    T* allocate(std::size_t n) {
        if (n != 1) {
            throw std::bad_alloc();  // Pool only handles single objects
        }
        
        if (!free_list) {
            allocate_pool();
        }
        
        Block* block = free_list;
        free_list = free_list->next;
        return reinterpret_cast<T*>(block);
    }
    
    void deallocate(T* p, std::size_t n) noexcept {
        if (n != 1) return;
        
        Block* block = reinterpret_cast<Block*>(p);
        block->next = free_list;
        free_list = block;
    }
    
    template<typename U>
    struct rebind {
        using other = PoolAllocator<U, PoolSize>;
    };
};

void demonstrate_pool_allocator() {
    std::cout << "\n=== POOL ALLOCATOR ===\n\n";
    
    // std::list makes many small allocations (perfect for pool!)
    using MyList = std::list<int, PoolAllocator<int, 1024>>;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    MyList list;
    for (int i = 0; i < 10000; ++i) {
        list.push_back(i);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "Inserted 10,000 elements with pool allocator\n";
    std::cout << "Time: " << duration.count() << " microseconds\n";
    std::cout << "\nPool allocator advantages:\n";
    std::cout << "  - O(1) allocation (pop from free list)\n";
    std::cout << "  - No fragmentation\n";
    std::cout << "  - Cache-friendly (adjacent blocks)\n";
}

// ============================================================================
// 3. ARENA/STACK ALLOCATOR (Bump allocator)
// ============================================================================

/*
 * Arena Allocator:
 *   - Allocates from contiguous buffer
 *   - Allocation: Bump pointer (O(1))
 *   - Deallocation: Usually all-at-once (reset)
 * 
 * Use cases:
 *   - Temporary allocations (scope-bound)
 *   - Parse tree, expression evaluation
 *   - Per-frame allocations (games)
 * 
 * Trade-offs:
 *   + Extremely fast allocation (just pointer bump)
 *   + Excellent cache locality
 *   - Can't free individual objects
 *   - Must know max size upfront
 */

class ArenaAllocator {
private:
    char* buffer;
    std::size_t size;
    std::size_t offset = 0;
    
public:
    ArenaAllocator(std::size_t size) : size(size) {
        buffer = new char[size];
    }
    
    ~ArenaAllocator() {
        delete[] buffer;
    }
    
    // Delete copy/move (arena is non-copyable)
    ArenaAllocator(const ArenaAllocator&) = delete;
    ArenaAllocator& operator=(const ArenaAllocator&) = delete;
    
    void* allocate(std::size_t bytes, std::size_t alignment = alignof(std::max_align_t)) {
        // Align offset
        std::size_t padding = (alignment - (offset % alignment)) % alignment;
        std::size_t aligned_offset = offset + padding;
        
        if (aligned_offset + bytes > size) {
            throw std::bad_alloc();
        }
        
        void* ptr = buffer + aligned_offset;
        offset = aligned_offset + bytes;
        return ptr;
    }
    
    // Arena doesn't support individual deallocation
    void deallocate(void*, std::size_t) noexcept {
        // No-op (all freed on reset())
    }
    
    // Reset arena (free all at once)
    void reset() noexcept {
        offset = 0;
    }
    
    std::size_t bytes_used() const noexcept {
        return offset;
    }
};

// Wrapper to use with STL containers
template<typename T>
class STLArenaAllocator {
private:
    ArenaAllocator* arena;
    
public:
    using value_type = T;
    
    STLArenaAllocator(ArenaAllocator& arena) : arena(&arena) {}
    
    template<typename U>
    STLArenaAllocator(const STLArenaAllocator<U>& other) noexcept 
        : arena(other.arena) {}
    
    T* allocate(std::size_t n) {
        return static_cast<T*>(arena->allocate(n * sizeof(T), alignof(T)));
    }
    
    void deallocate(T* p, std::size_t n) noexcept {
        arena->deallocate(p, n * sizeof(T));
    }
    
    template<typename U>
    bool operator==(const STLArenaAllocator<U>& other) const noexcept {
        return arena == other.arena;
    }
    
    template<typename U>
    bool operator!=(const STLArenaAllocator<U>& other) const noexcept {
        return arena != other.arena;
    }
    
    template<typename U>
    friend class STLArenaAllocator;
};

void demonstrate_arena_allocator() {
    std::cout << "\n=== ARENA ALLOCATOR ===\n\n";
    
    ArenaAllocator arena(1024 * 1024);  // 1 MB buffer
    
    std::cout << "Arena size: 1 MB\n\n";
    
    // Scope 1: Parse tree
    {
        std::vector<int, STLArenaAllocator<int>> vec(STLArenaAllocator<int>(arena));
        for (int i = 0; i < 100; ++i) {
            vec.push_back(i);
        }
        std::cout << "After vector: " << arena.bytes_used() << " bytes used\n";
    }
    
    // Scope 2: Temporary calculations (don't reset, keep allocating)
    {
        std::vector<double, STLArenaAllocator<double>> vec(STLArenaAllocator<double>(arena));
        for (int i = 0; i < 50; ++i) {
            vec.push_back(i * 3.14);
        }
        std::cout << "After second vector: " << arena.bytes_used() << " bytes used\n";
    }
    
    // Reset arena (free everything)
    arena.reset();
    std::cout << "\nAfter reset: " << arena.bytes_used() << " bytes used\n";
    
    std::cout << "\nArena advantages:\n";
    std::cout << "  - Fastest allocation (just pointer bump)\n";
    std::cout << "  - Perfect cache locality\n";
    std::cout << "  - Reset frees everything instantly\n";
    std::cout << "  - Ideal for scope-bound allocations\n";
}

// ============================================================================
// 4. PMR (Polymorphic Memory Resources) - C++17
// ============================================================================

/*
 * std::pmr (C++17):
 *   - Standard memory resource abstraction
 *   - Type-erased (same container type works with any allocator)
 *   - Composable (memory resources can wrap each other)
 * 
 * Key types:
 *   - std::pmr::memory_resource: Abstract base
 *   - std::pmr::new_delete_resource(): Default (malloc/free)
 *   - std::pmr::monotonic_buffer_resource: Arena-like
 *   - std::pmr::synchronized_pool_resource: Thread-safe pool
 *   - std::pmr::unsynchronized_pool_resource: Single-threaded pool
 */

void demonstrate_pmr() {
    std::cout << "\n=== PMR (Polymorphic Memory Resources) ===\n\n";
    
    // 1. Default resource (new/delete)
    std::cout << "1. Default resource:\n";
    {
        std::pmr::vector<int> vec;
        vec.push_back(1);
        vec.push_back(2);
        std::cout << "   Vector uses new/delete\n";
    }
    
    // 2. Monotonic buffer (arena-like)
    std::cout << "\n2. Monotonic buffer:\n";
    {
        char buffer[1024];
        std::pmr::monotonic_buffer_resource mbr(buffer, sizeof(buffer));
        
        std::pmr::vector<int> vec(&mbr);
        for (int i = 0; i < 10; ++i) {
            vec.push_back(i);
        }
        std::cout << "   Vector uses stack buffer\n";
        std::cout << "   Extremely fast, no heap allocations\n";
    }
    
    // 3. Pool resource
    std::cout << "\n3. Unsynchronized pool:\n";
    {
        std::pmr::unsynchronized_pool_resource pool;
        
        std::pmr::list<int> list(&pool);
        for (int i = 0; i < 100; ++i) {
            list.push_back(i);
        }
        std::cout << "   List uses pool for fast node allocation\n";
    }
    
    // 4. Composing resources
    std::cout << "\n4. Composing resources:\n";
    {
        char buffer[4096];
        std::pmr::monotonic_buffer_resource mbr(buffer, sizeof(buffer));
        std::pmr::unsynchronized_pool_resource pool(&mbr);  // Pool backed by arena!
        
        std::pmr::vector<int> vec(&pool);
        for (int i = 0; i < 50; ++i) {
            vec.push_back(i);
        }
        std::cout << "   Pool allocates from arena (no heap allocations!)\n";
    }
    
    std::cout << "\nPMR advantages:\n";
    std::cout << "  - Type-erased (same container type)\n";
    std::cout << "  - Composable resources\n";
    std::cout << "  - Standard interface\n";
}

// ============================================================================
// 5. MEMORY ALIGNMENT
// ============================================================================

/*
 * Alignment matters for:
 *   - Performance (aligned access is faster)
 *   - SIMD (AVX requires 32-byte alignment)
 *   - Cache lines (avoid false sharing)
 * 
 * C++11: alignas(N), alignof(T)
 * C++17: std::aligned_alloc, std::align
 */

void demonstrate_alignment() {
    std::cout << "\n=== MEMORY ALIGNMENT ===\n\n";
    
    // Check natural alignment
    std::cout << "Natural alignment:\n";
    std::cout << "  char: " << alignof(char) << " bytes\n";
    std::cout << "  int: " << alignof(int) << " bytes\n";
    std::cout << "  double: " << alignof(double) << " bytes\n";
    std::cout << "  void*: " << alignof(void*) << " bytes\n";
    
    // Custom alignment
    struct alignas(64) CacheLineAligned {  // 64-byte alignment (cache line)
        int data[16];
    };
    
    std::cout << "\nCustom alignment:\n";
    std::cout << "  CacheLineAligned: " << alignof(CacheLineAligned) << " bytes\n";
    
    // Over-aligned allocation
    void* ptr = std::aligned_alloc(64, 1024);
    std::cout << "\nAllocated 1024 bytes with 64-byte alignment\n";
    std::cout << "Address: " << ptr << " (divisible by 64)\n";
    std::free(ptr);
    
    std::cout << "\nAlignment is critical for:\n";
    std::cout << "  - SIMD (AVX requires 32-byte alignment)\n";
    std::cout << "  - Cache optimization (avoid false sharing)\n";
    std::cout << "  - Hardware requirements\n";
}

// ============================================================================
// 6. PERFORMANCE COMPARISON
// ============================================================================

void demonstrate_performance_comparison() {
    std::cout << "\n=== PERFORMANCE COMPARISON ===\n\n";
    
    constexpr int iterations = 100000;
    
    // 1. Default allocator (new/delete)
    {
        auto start = std::chrono::high_resolution_clock::now();
        
        std::list<int> list;
        for (int i = 0; i < iterations; ++i) {
            list.push_back(i);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Default allocator: " << duration.count() << " ms\n";
    }
    
    // 2. Pool allocator
    {
        auto start = std::chrono::high_resolution_clock::now();
        
        std::list<int, PoolAllocator<int>> list;
        for (int i = 0; i < iterations; ++i) {
            list.push_back(i);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Pool allocator:    " << duration.count() << " ms (";
        std::cout << "~2-3x faster)\n";
    }
    
    // 3. PMR pool
    {
        std::pmr::unsynchronized_pool_resource pool;
        
        auto start = std::chrono::high_resolution_clock::now();
        
        std::pmr::list<int> list(&pool);
        for (int i = 0; i < iterations; ++i) {
            list.push_back(i);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "PMR pool:          " << duration.count() << " ms\n";
    }
}

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

int main() {
    std::cout << "╔══════════════════════════════════════════════════════════╗\n";
    std::cout << "║    CUSTOM ALLOCATORS & MEMORY MANAGEMENT DEMONSTRATION   ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════╝\n\n";
    
    demonstrate_allocator_interface();
    demonstrate_pool_allocator();
    demonstrate_arena_allocator();
    demonstrate_pmr();
    demonstrate_alignment();
    demonstrate_performance_comparison();
    
    std::cout << "\n=== SUMMARY ===\n\n";
    std::cout << "Default allocator: General-purpose, malloc/free\n";
    std::cout << "Pool allocator: Fixed-size blocks, very fast\n";
    std::cout << "Arena allocator: Bump pointer, fastest, scope-bound\n";
    std::cout << "PMR: Standard abstraction, composable\n";
    
    return 0;
}

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/*
 * 1. WHY CUSTOM ALLOCATORS?
 *    - Performance: 2-10x faster for specific patterns
 *    - Predictability: Real-time systems
 *    - Control: Memory pooling, fragmentation
 * 
 * 2. ALLOCATOR TYPES:
 *    
 *    Pool Allocator:
 *      ✓ Fixed-size blocks
 *      ✓ O(1) alloc/dealloc
 *      ✓ No fragmentation
 *      ✗ Only one size
 *      Use: std::list, many same-size objects
 *    
 *    Arena Allocator:
 *      ✓ Fastest allocation (pointer bump)
 *      ✓ Perfect cache locality
 *      ✓ All-at-once deallocation
 *      ✗ Can't free individual objects
 *      Use: Scope-bound, parse trees, per-frame
 *    
 *    PMR (C++17):
 *      ✓ Standard interface
 *      ✓ Type-erased
 *      ✓ Composable
 *      ✓ monotonic_buffer, pool, new_delete
 *      Use: Flexible, modern codebases
 * 
 * 3. WHEN TO USE:
 *    - Many small allocations: Pool
 *    - Temporary/scope-bound: Arena
 *    - Need flexibility: PMR
 *    - Default works fine: Use default!
 * 
 * 4. BEST PRACTICES:
 *    - Profile first (don't optimize prematurely)
 *    - Use PMR for standard interface
 *    - Arena for scope-bound lifetimes
 *    - Pool for std::list, std::map
 * 
 * 5. ALIGNMENT:
 *    - Critical for SIMD, cache optimization
 *    - alignas(N) for custom alignment
 *    - std::aligned_alloc for over-alignment
 * 
 * 6. MEMORY DEBUGGING:
 *    - ASAN (AddressSanitizer): Catch leaks, use-after-free
 *    - Valgrind: Memory profiler
 *    - Custom tracking: Wrap allocators for debugging
 * 
 * Custom allocators are a senior-level optimization technique.
 * Use when profiling shows allocation is a bottleneck!
 */
