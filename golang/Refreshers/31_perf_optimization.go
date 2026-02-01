/*
GO PERFORMANCE & OPTIMIZATION
This comprehensive example demonstrates performance optimization techniques in Go
from junior to senior level, focusing on practical patterns and tool usage.
*/

package main

import (
	"bytes"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	_ "net/http/pprof" // Import pprof for profiling endpoints
	"os"
	"runtime"
	"runtime/debug"
	"runtime/pprof"
	"runtime/trace"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
	"unsafe"
)

/*
MEMORY MANAGEMENT & GC TUNING:
Go uses concurrent, tri-color mark-and-sweep garbage collector.
Key GC parameters (set via GODEBUG environment variable):
  - GOGC=100 (default): GC runs when heap grows 100% from live heap
  - GODEBUG=gctrace=1: Print GC events
  - GODEBUG=gcpacertrace=1: Print GC pacing events
*/

func main() {
	// Start pprof HTTP server for live profiling
	go func() {
		log.Println(http.ListenAndServe("localhost:6060", nil))
	}()

	// Demo various optimization techniques
	demoGCTuning()
	demoEfficientDataStructures()
	demoZeroAllocation()
	demoPoolUsage()
	demoCacheOptimizations()

	// Run memory-intensive operation
	runMemoryOptimizedTask()

	// Keep server running
	select {}
}

// ==================== GC TUNING AND MONITORING ====================

func demoGCTuning() {
	// Print current GC settings
	fmt.Printf("GOGC=%s\n", os.Getenv("GOGC"))
	fmt.Printf("GOMAXPROCS=%d\n", runtime.GOMAXPROCS(0))

	// Set GC percentage (lower = more frequent GC, less memory usage)
	// Set via environment: GOGC=50 or debug.SetGCPercent()
	debug.SetGCPercent(100) // Default value

	// Force GC (for testing/demo only - don't do in production!)
	runtime.GC()

	// Read memory stats
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("Alloc = %v MiB", bToMb(m.Alloc))
	fmt.Printf("\tTotalAlloc = %v MiB", bToMb(m.TotalAlloc))
	fmt.Printf("\tSys = %v MiB", bToMb(m.Sys))
	fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func bToMb(b uint64) uint64 {
	return b / 1024 / 1024
}

// ==================== PROFILING WITH PPTOF ====================

// CPU Profiling example
func startCPUProfile() {
	f, err := os.Create("cpu.prof")
	if err != nil {
		log.Fatal("could not create CPU profile: ", err)
	}
	defer f.Close()

	if err := pprof.StartCPUProfile(f); err != nil {
		log.Fatal("could not start CPU profile: ", err)
	}

	// Stop after 30 seconds
	time.AfterFunc(30*time.Second, pprof.StopCPUProfile)
}

// Memory profiling example
func writeMemoryProfile() {
	f, err := os.Create("mem.prof")
	if err != nil {
		log.Fatal("could not create memory profile: ", err)
	}
	defer f.Close()

	runtime.GC() // Get up-to-date statistics
	if err := pprof.WriteHeapProfile(f); err != nil {
		log.Fatal("could not write memory profile: ", err)
	}
}

// ==================== EFFICIENT DATA STRUCTURES ====================

func demoEfficientDataStructures() {
	// 1. Slice vs Linked List
	// For most use cases, slices are more cache-efficient
	demoSliceVsLinkedList()

	// 2. Map optimizations
	demoMapOptimizations()

	// 3. Struct layout for cache locality
	demoStructLayout()

	// 4. String building
	demoStringBuilding()
}

func demoSliceVsLinkedList() {
	// Slice (contiguous memory, good for iteration)
	data := make([]int, 0, 1000) // Pre-allocate capacity
	for i := 0; i < 1000; i++ {
		data = append(data, i)
	}

	// Iteration is cache-friendly
	sum := 0
	for _, v := range data {
		sum += v
	}

	// Linked List (better for frequent inserts/deletes in middle)
	type Node struct {
		value int
		next  *Node
	}

	// But in Go, slices are almost always better due to:
	// - Better cache locality
	// - Less allocation overhead
	// - Simpler code
}

func demoMapOptimizations() {
	// 1. Pre-allocate map size when known
	m := make(map[string]int, 1000) // Pre-allocates space for ~1000 entries
	for i := 0; i < 1000; i++ {
		m[strconv.Itoa(i)] = i
	}

	// 2. Use int keys instead of strings when possible
	intMap := make(map[int]string, 1000)

	// 3. Consider using slice+linear search for small maps (<10 entries)
	// Maps have overhead: 8 bytes per key + 8 bytes per value + overhead
	smallData := []struct {
		key   string
		value int
	}{
		{"a", 1},
		{"b", 2},
		{"c", 3},
	}

	// Linear search for small collections can be faster
	findValue := func(key string) (int, bool) {
		for _, item := range smallData {
			if item.key == key {
				return item.value, true
			}
		}
		return 0, false
	}
	_ = findValue

	// 4. Use sync.Map for read-heavy, write-rarely scenarios
	var syncMap sync.Map
	syncMap.Store("key", "value")
	if val, ok := syncMap.Load("key"); ok {
		fmt.Println("Found:", val)
	}
}

func demoStructLayout() {
	// POOR: Struct with padding (wastes memory)
	type PoorStruct struct {
		a bool    // 1 byte + 7 bytes padding
		b int64   // 8 bytes
		c bool    // 1 byte + 7 bytes padding
		d float64 // 8 bytes
		e bool    // 1 byte + 7 bytes padding
	}
	// Total: 40 bytes (only 18 bytes of data!)

	// BETTER: Reorder fields to minimize padding
	type BetterStruct struct {
		b int64   // 8 bytes
		d float64 // 8 bytes
		a bool    // 1 byte
		c bool    // 1 byte
		e bool    // 1 byte
		// 5 bytes padding (to align to 8 bytes)
	}
	// Total: 24 bytes (same data!)

	fmt.Printf("PoorStruct size: %d bytes\n", unsafe.Sizeof(PoorStruct{}))
	fmt.Printf("BetterStruct size: %d bytes\n", unsafe.Sizeof(BetterStruct{}))

	// For arrays of structs, this makes huge difference
	poorArray := make([]PoorStruct, 1000)
	betterArray := make([]BetterStruct, 1000)
	fmt.Printf("Poor array: %d bytes\n", unsafe.Sizeof(poorArray[0])*1000)
	fmt.Printf("Better array: %d bytes\n", unsafe.Sizeof(betterArray[0])*1000)
}

func demoStringBuilding() {
	// INEFFICIENT: Creates many temporary strings
	var result string
	for i := 0; i < 1000; i++ {
		result += strconv.Itoa(i) // New allocation each iteration!
	}

	// EFFICIENT: Use strings.Builder
	var builder strings.Builder
	builder.Grow(4096) // Pre-allocate estimated size
	for i := 0; i < 1000; i++ {
		builder.WriteString(strconv.Itoa(i))
	}
	result = builder.String()

	// ALTERNATIVE: Use bytes.Buffer
	var buf bytes.Buffer
	buf.Grow(4096)
	for i := 0; i < 1000; i++ {
		buf.WriteString(strconv.Itoa(i))
	}
	result = buf.String()
}

// ==================== ZERO-ALLOCATION TECHNIQUES ====================

func demoZeroAllocation() {
	// 1. Reuse buffers
	reuseBuffer()

	// 2. Stack allocation vs heap allocation
	stackVsHeap()

	// 3. Avoid interface conversions
	avoidInterfaceConversions()

	// 4. Use sync.Pool for frequently allocated objects
	useSyncPool()
}

func reuseBuffer() {
	// Instead of creating new buffers, reuse them
	buf := make([]byte, 0, 1024)

	process := func() {
		buf = buf[:0] // Reset slice length, keep capacity
		buf = append(buf, "data "...)
		// Process buf...
		_ = string(buf)
	}

	for i := 0; i < 1000; i++ {
		process()
	}
}

func stackVsHeap() {
	// Go compiler uses escape analysis to allocate on stack when possible
	// Stack allocation is much faster than heap allocation

	// This will likely stay on stack (no escape)
	stayOnStack()

	// This will escape to heap (returned pointer)
	_ = escapeToHeap()
}

func stayOnStack() int {
	x := 42 // Allocated on stack
	return x
}

func escapeToHeap() *int {
	x := 42 // Escapes to heap (address returned)
	return &x
}

func avoidInterfaceConversions() {
	// Interface conversions cause allocations

	// Allocation happens here (interface{} conversion)
	var iface interface{} = "hello"
	str := iface.(string)
	_ = str

	// Type switches also cause allocations
	switch v := iface.(type) {
	case string:
		_ = v
	case int:
		_ = v
	}

	// Alternative: Use generics (Go 1.18+) to avoid interface allocations
	printGeneric("hello")
	printGeneric(42)
}

func printGeneric[T any](value T) {
	// No interface allocation
	fmt.Println(value)
}

// ==================== SYNC.POOL FOR OBJECT REUSE ====================

var bufferPool = sync.Pool{
	New: func() interface{} {
		return &bytes.Buffer{}
	},
}

func getBuffer() *bytes.Buffer {
	return bufferPool.Get().(*bytes.Buffer)
}

func putBuffer(buf *bytes.Buffer) {
	buf.Reset()
	bufferPool.Put(buf)
}

func demoPoolUsage() {
	// Get buffer from pool
	buf := getBuffer()
	defer putBuffer(buf) // Important: defer return to pool

	// Use buffer
	buf.WriteString("Hello, ")
	buf.WriteString("World!")

	result := buf.String()
	_ = result
}

// ==================== CACHE OPTIMIZATIONS ====================

func demoCacheOptimizations() {
	// 1. CPU Cache Line awareness (typically 64 bytes)
	type CacheLine struct {
		data [64]byte // Fits in one cache line
	}

	// 2. False sharing prevention
	type PaddedCounter struct {
		value int64
		_     [56]byte // Padding to fill cache line (64 - 8 = 56)
	}

	// 3. Slice of pointers vs slice of values
	// Slice of values is more cache-friendly
	values := make([]int, 1000)    // Contiguous memory
	pointers := make([]*int, 1000) // Pointers to scattered memory

	// Initialize
	for i := range values {
		values[i] = i
		pointers[i] = &values[i]
	}

	// Iterating values is faster (better cache locality)
	sum := 0
	for _, v := range values {
		sum += v
	}
	_ = sum
}

// ==================== ADVANCED MEMORY OPTIMIZATIONS ====================

func runMemoryOptimizedTask() {
	// Simulate memory-intensive processing
	data := generateLargeDataset(1_000_000)

	// Process with different optimization techniques
	processWithOptimizations(data)

	// Compare approaches
	benchmarkApproaches()
}

func generateLargeDataset(n int) []int {
	data := make([]int, n)
	for i := range data {
		data[i] = rand.Intn(1000)
	}
	return data
}

func processWithOptimizations(data []int) {
	// Approach 1: Naive (creates many allocations)
	_ = processNaive(data)

	// Approach 2: Optimized (minimal allocations)
	_ = processOptimized(data)

	// Approach 3: Parallel processing
	_ = processParallel(data)
}

func processNaive(data []int) []string {
	// Inefficient: Creates new string for each element
	result := make([]string, len(data))
	for i, v := range data {
		result[i] = fmt.Sprintf("Value: %d", v) // Allocation!
	}
	return result
}

func processOptimized(data []int) []string {
	// Optimized: Pre-allocate, use strings.Builder
	result := make([]string, len(data))

	// Reusable buffer
	var buf strings.Builder
	buf.Grow(20) // Estimate average string length

	for i, v := range data {
		buf.Reset()
		buf.WriteString("Value: ")
		buf.WriteString(strconv.Itoa(v))
		result[i] = buf.String()
	}
	return result
}

func processParallel(data []int) []string {
	// Parallel processing with worker pools
	numWorkers := runtime.GOMAXPROCS(0)
	chunkSize := len(data) / numWorkers

	var wg sync.WaitGroup
	results := make([]string, len(data))

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()

			start := workerID * chunkSize
			end := start + chunkSize
			if workerID == numWorkers-1 {
				end = len(data)
			}

			// Process chunk
			var buf strings.Builder
			for i := start; i < end; i++ {
				buf.Reset()
				buf.WriteString("Value: ")
				buf.WriteString(strconv.Itoa(data[i]))
				results[i] = buf.String()
			}
		}(w)
	}

	wg.Wait()
	return results
}

// ==================== CUSTOM ALLOCATOR PATTERN ====================

// Arena allocator pattern for batch processing
type Arena struct {
	buf   []byte
	index int
}

func NewArena(size int) *Arena {
	return &Arena{
		buf: make([]byte, size),
	}
}

func (a *Arena) Alloc(size int) []byte {
	if a.index+size > len(a.buf) {
		// Fallback to regular allocation
		return make([]byte, size)
	}

	slice := a.buf[a.index : a.index+size]
	a.index += size
	return slice
}

func (a *Arena) Reset() {
	a.index = 0
}

func benchmarkApproaches() {
	// Simple benchmark comparison
	data := generateLargeDataset(10000)

	// Time naive approach
	start := time.Now()
	_ = processNaive(data)
	naiveTime := time.Since(start)

	// Time optimized approach
	start = time.Now()
	_ = processOptimized(data)
	optimizedTime := time.Since(start)

	fmt.Printf("Naive: %v\n", naiveTime)
	fmt.Printf("Optimized: %v\n", optimizedTime)
	fmt.Printf("Speedup: %.2fx\n", float64(naiveTime)/float64(optimizedTime))
}

// ==================== TRACING AND OBSERVABILITY ====================

// Enable execution tracing
func startTracing() {
	f, err := os.Create("trace.out")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	if err := trace.Start(f); err != nil {
		log.Fatal(err)
	}

	// Stop after some time
	time.AfterFunc(5*time.Second, func() {
		trace.Stop()
		fmt.Println("Trace written to trace.out")
		fmt.Println("Analyze with: go tool trace trace.out")
	})
}

var traceStarted bool

func traceStart(f *os.File) error {
	traceStarted = true
	return nil
}

func traceStop() {
	traceStarted = false
}

// ==================== CONCURRENCY OPTIMIZATIONS ====================

// Lock-free patterns using atomic operations
type AtomicCounter struct {
	value int64
}

func (c *AtomicCounter) Add(delta int64) int64 {
	return atomic.AddInt64(&c.value, delta)
}

func (c *AtomicCounter) Load() int64 {
	return atomic.LoadInt64(&c.value)
}

// Channel optimizations
func demoChannelOptimizations() {
	// 1. Buffered channels reduce contention
	ch := make(chan int, 100) // Buffer reduces goroutine blocking

	// 2. Batch processing through channels
	batchCh := make(chan []int, 10)

	// Producer
	go func() {
		batch := make([]int, 0, 100)
		for i := 0; i < 1000; i++ {
			batch = append(batch, i)
			if len(batch) == 100 {
				batchCh <- batch
				batch = make([]int, 0, 100)
			}
		}
		if len(batch) > 0 {
			batchCh <- batch
		}
		close(batchCh)
	}()

	// Consumer
	go func() {
		for batch := range batchCh {
			// Process batch
			_ = batch
		}
	}()
}

// ==================== REAL-WORLD OPTIMIZATION EXAMPLE ====================

// High-performance HTTP handler with optimizations
type OptimizedHandler struct {
	// Reusable buffers in pool
	bufPool sync.Pool

	// Cache for frequently accessed data
	cache      map[string]cacheEntry
	cacheMutex sync.RWMutex

	// Atomic counters for stats
	requestCount AtomicCounter
}

type cacheEntry struct {
	data    []byte
	expires time.Time
}

func NewOptimizedHandler() *OptimizedHandler {
	return &OptimizedHandler{
		bufPool: sync.Pool{
			New: func() interface{} {
				return bytes.NewBuffer(make([]byte, 0, 4096))
			},
		},
		cache: make(map[string]cacheEntry),
	}
}

func (h *OptimizedHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	h.requestCount.Add(1)

	// Get buffer from pool
	buf := h.bufPool.Get().(*bytes.Buffer)
	defer h.bufPool.Put(buf)
	buf.Reset()

	// Check cache first
	key := r.URL.Path
	if entry, ok := h.getFromCache(key); ok {
		w.Write(entry.data)
		return
	}

	// Generate response
	h.generateResponse(buf, r)

	// Cache the response
	data := make([]byte, buf.Len())
	copy(data, buf.Bytes())
	h.setCache(key, data, 5*time.Minute)

	// Write response
	w.Write(data)
}

func (h *OptimizedHandler) getFromCache(key string) ([]byte, bool) {
	h.cacheMutex.RLock()
	defer h.cacheMutex.RUnlock()

	entry, ok := h.cache[key]
	if !ok || time.Now().After(entry.expires) {
		return nil, false
	}
	return entry.data, true
}

func (h *OptimizedHandler) setCache(key string, data []byte, ttl time.Duration) {
	h.cacheMutex.Lock()
	defer h.cacheMutex.Unlock()

	h.cache[key] = cacheEntry{
		data:    data,
		expires: time.Now().Add(ttl),
	}
}

func (h *OptimizedHandler) generateResponse(buf *bytes.Buffer, r *http.Request) {
	// Efficient string building
	buf.WriteString(`{"status":"ok","path":"`)
	buf.WriteString(r.URL.Path)
	buf.WriteString(`","count":`)
	buf.WriteString(strconv.FormatInt(h.requestCount.Load(), 10))
	buf.WriteString(`}`)
}

// ==================== PROFILING ENDPOINTS ====================

// Add profiling endpoints to your HTTP server
func addProfilingEndpoints(mux *http.ServeMux) {
	// Already have pprof from net/http/pprof import

	// Custom profiling endpoint
	mux.HandleFunc("/debug/memory", func(w http.ResponseWriter, r *http.Request) {
		var m runtime.MemStats
		runtime.ReadMemStats(&m)

		fmt.Fprintf(w, "Alloc: %v MB\n", m.Alloc/1024/1024)
		fmt.Fprintf(w, "TotalAlloc: %v MB\n", m.TotalAlloc/1024/1024)
		fmt.Fprintf(w, "Sys: %v MB\n", m.Sys/1024/1024)
		fmt.Fprintf(w, "NumGC: %v\n", m.NumGC)
		fmt.Fprintf(w, "GCSys: %v MB\n", m.GCSys/1024/1024)
		fmt.Fprintf(w, "HeapAlloc: %v MB\n", m.HeapAlloc/1024/1024)
		fmt.Fprintf(w, "HeapSys: %v MB\n", m.HeapSys/1024/1024)
	})
}

// ==================== OPTIMIZATION CHECKLIST ====================

/*
PERFORMANCE OPTIMIZATION CHECKLIST:

1. MEASURE FIRST:
   - Use pprof to identify bottlenecks
   - Benchmark before and after optimizations
   - Use go test -bench . -benchmem

2. MEMORY OPTIMIZATIONS:
   [✓] Minimize allocations
   [✓] Reuse buffers with sync.Pool
   [✓] Use appropriate data structures
   [✓] Optimize struct layout
   [✓] Consider arena allocation patterns

3. CPU OPTIMIZATIONS:
   [✓] Reduce interface conversions
   [✓] Use generics for type safety without allocations
   [✓] Optimize loops and conditionals
   [✓] Use CPU cache-friendly data access patterns

4. CONCURRENCY OPTIMIZATIONS:
   [✓] Use appropriate synchronization primitives
   [✓] Consider lock-free patterns for hot paths
   [✓] Batch operations to reduce contention
   [✓] Use worker pools for task processing

5. GC TUNING:
   [✓] Set appropriate GOGC value
   [✓] Reduce pointer-rich data structures
   [✓] Consider manual memory management for critical paths

6. PRODUCTION MONITORING:
   [✓] Enable pprof endpoints
   [✓] Add metrics for key operations
   [✓] Set up alerts for memory leaks
   [✓] Regularly review GC and memory stats

REMEMBER: Premature optimization is the root of all evil.
Always profile and measure before optimizing!
*/

// Example benchmark test (would be in *_test.go file)
/*
func BenchmarkProcessOptimized(b *testing.B) {
	data := generateLargeDataset(10000)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		_ = processOptimized(data)
	}
}

func BenchmarkProcessNaive(b *testing.B) {
	data := generateLargeDataset(10000)
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		_ = processNaive(data)
	}
}
*/

// Helper function to analyze escape analysis
// Build with: go build -gcflags="-m -m" main.go
func analyzeEscapes() {
	data := make([]int, 100)

	// Does this escape to heap?
	processData(data)
}

func processData(data []int) []int {
	// Return slice - does it cause escape?
	result := make([]int, len(data))
	copy(result, data)
	return result
}
