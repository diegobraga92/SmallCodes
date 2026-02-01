/*
================================================================================
GOLANG MEMORY MANAGEMENT & PERFORMANCE - JUNIOR TO SENIOR CONCEPTS
================================================================================
This comprehensive example demonstrates Go's memory management, performance
optimization techniques, and profiling tools.
*/

package main

import (
	"bytes"
	"fmt"
	"log"
	"math"
	"math/rand"
	"os"
	"runtime"
	"runtime/pprof"
	"sort"
	"sync"
	"time"
	"unsafe"
)

/*
-------------------------------------------------------------------------------
1. GARBAGE COLLECTOR BEHAVIOR
-------------------------------------------------------------------------------
Go uses a concurrent, tri-color mark-and-sweep GC with low latency goals.
Understanding GC behavior is key to performance optimization.
*/

// GC runs automatically based on heap growth and GOGC environment variable
// GOGC=100 (default) means GC runs when heap grows 100% since last GC

func demonstrateGCBehavior() {
	fmt.Println("\n=== Garbage Collector Behavior ===")

	// Force GC and get stats
	runtime.GC()

	var stats runtime.MemStats
	runtime.ReadMemStats(&stats)

	fmt.Printf("Heap in use: %v MB\n", stats.HeapInuse/1024/1024)
	fmt.Printf("Heap allocated: %v MB\n", stats.HeapAlloc/1024/1024)
	fmt.Printf("Total GC cycles: %d\n", stats.NumGC)
	fmt.Printf("Last GC pause: %v ms\n", float64(stats.PauseNs[(stats.NumGC+255)%256])/1e6)

	// Memory allocation patterns affect GC pressure
	createGCPressure()
}

func createGCPressure() {
	// Creating many short-lived objects increases GC frequency
	var slices [][]byte
	for i := 0; i < 10000; i++ {
		// Each iteration creates garbage
		data := make([]byte, 1024) // 1KB allocation
		_ = data
		// data becomes garbage immediately (no reference kept)
	}

	// Keeping references reduces immediate GC pressure but increases heap
	for i := 0; i < 1000; i++ {
		data := make([]byte, 10240) // 10KB allocation
		slices = append(slices, data)
	}
	// slices holds references, so memory isn't collected until function returns
	_ = slices
}

/*
-------------------------------------------------------------------------------
2. ALLOCATIONS & PROFILING
-------------------------------------------------------------------------------
Every allocation has a cost. Minimizing allocations is key to performance.
*/

type ExpensiveObject struct {
	ID    int
	Data  [1000]byte
	Links []*ExpensiveObject
}

func demonstrateAllocations() {
	fmt.Println("\n=== Memory Allocations ===")

	// Stack vs Heap allocation understanding
	allocOnStack()
	allocOnHeap()

	// Allocation patterns matter
	inefficientAllocations()
	efficientAllocations()
}

func allocOnStack() {
	// Small, short-lived variables typically stay on stack
	var x int = 42
	var arr [100]int
	_ = x
	_ = arr
	// These are automatically cleaned up when function returns
}

func allocOnHeap() {
	// These cause heap allocations:
	// 1. Variables that escape function scope
	obj := &ExpensiveObject{ID: 1} // Pointer escapes to heap
	globalReference := obj         // Bad practice - global reference

	// 2. Large allocations
	large := make([]byte, 1<<20) // 1MB allocation

	// 3. Variables referenced by closures that outlive function
	fn := func() {
		fmt.Println(obj.ID) // obj escapes through closure
	}
	go fn()

	_ = globalReference
	_ = large
}

func inefficientAllocations() {
	fmt.Println("Inefficient allocations pattern:")

	// BAD: Repeated allocation in loops
	var result []string
	for i := 0; i < 1000; i++ {
		// Each iteration allocates new string
		result = append(result, fmt.Sprintf("Number: %d", i))
	}

	// BAD: Unnecessary intermediate allocations
	var buffer bytes.Buffer
	for i := 0; i < 100; i++ {
		// Each WriteString might cause reallocation
		buffer.WriteString("data")
	}
	_ = result
}

func efficientAllocations() {
	fmt.Println("Efficient allocations pattern:")

	// GOOD: Pre-allocate when size is known
	result := make([]string, 0, 1000) // Pre-allocate capacity
	for i := 0; i < 1000; i++ {
		result = append(result, fmt.Sprintf("Number: %d", i))
	}

	// GOOD: Reuse buffers
	var buffer bytes.Buffer
	buffer.Grow(400) // Pre-allocate space for 100 * "data"
	for i := 0; i < 100; i++ {
		buffer.WriteString("data")
	}

	// GOOD: Use string.Builder for string concatenation
	var sb strings.Builder
	sb.Grow(1000) // Pre-allocate
	for i := 0; i < 100; i++ {
		sb.WriteString("data")
	}
	finalString := sb.String()
	_ = finalString
}

/*
-------------------------------------------------------------------------------
3. ESCAPE ANALYSIS IN PRACTICE
-------------------------------------------------------------------------------
Escape analysis determines whether variables stay on stack or escape to heap.
Use `go build -gcflags="-m"` to see escape analysis decisions.
*/

func escapeAnalysisExamples() {
	fmt.Println("\n=== Escape Analysis Examples ===")

	// Run with: go build -gcflags="-m -l" to see escapes

	// Case 1: Returning pointer causes escape
	ptr := createPointer()
	_ = ptr

	// Case 2: Interface method call causes escape
	var shape Shape = &Circle{radius: 5}
	_ = shape.Area()

	// Case 3: Storing in global variable causes escape
	storeInGlobal()

	// Case 4: Channel send causes escape
	ch := make(chan *Data, 1)
	sendToChannel(ch)

	// Case 5: Closure capture can cause escape
	createClosure()
}

// Example types for escape analysis
type Circle struct{ radius float64 }
type Shape interface{ Area() float64 }
type Data struct{ value int }

func (c *Circle) Area() float64 {
	return math.Pi * c.radius * c.radius
}

// This escapes to heap because pointer is returned
func createPointer() *int {
	x := 42
	return &x // x escapes to heap
}

// This does NOT escape (with optimizations)
func noEscape() int {
	x := 42
	return x // Value is copied, x stays on stack
}

func storeInGlobal() {
	data := &Data{value: 100}
	globalData = data // data escapes to heap
}

var globalData *Data

func sendToChannel(ch chan *Data) {
	d := &Data{value: 200}
	ch <- d // d escapes to heap
}

func createClosure() {
	x := 100
	fn := func() int {
		return x // x escapes to heap through closure
	}
	_ = fn
}

/*
-------------------------------------------------------------------------------
4. OBJECT POOLING (sync.Pool)
-------------------------------------------------------------------------------
sync.Pool reduces allocation pressure by reusing objects.
Ideal for frequently allocated/discarded objects.
*/

type BufferPool struct {
	pool sync.Pool
}

func NewBufferPool() *BufferPool {
	return &BufferPool{
		pool: sync.Pool{
			New: func() interface{} {
				// Called when pool is empty
				return &bytes.Buffer{}
			},
		},
	}
}

func (bp *BufferPool) Get() *bytes.Buffer {
	buf := bp.pool.Get().(*bytes.Buffer)
	buf.Reset() // Clear any existing data
	return buf
}

func (bp *BufferPool) Put(buf *bytes.Buffer) {
	// Only pool reasonable-sized buffers
	if buf.Cap() > 64*1024 { // Don't pool very large buffers
		return
	}
	bp.pool.Put(buf)
}

func demonstrateObjectPooling() {
	fmt.Println("\n=== Object Pooling with sync.Pool ===")

	pool := NewBufferPool()

	// Simulate heavy buffer usage
	start := time.Now()
	var wg sync.WaitGroup

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()

			buf := pool.Get()
			defer pool.Put(buf) // Return to pool when done

			// Use buffer
			fmt.Fprintf(buf, "Goroutine %d: ", id)
			for j := 0; j < 100; j++ {
				buf.WriteString("data ")
			}
			// In real code, do something with buf.String()
		}(i)
	}

	wg.Wait()
	fmt.Printf("Pooled operations took: %v\n", time.Since(start))
}

// More sophisticated pooling example
type Connection struct {
	ID     int
	InUse  bool
	Socket int // Simulated
}

type ConnectionPool struct {
	pool      sync.Pool
	created   int
	maxSize   int
	mu        sync.Mutex
	available []*Connection
}

func NewConnectionPool(maxSize int) *ConnectionPool {
	return &ConnectionPool{
		pool: sync.Pool{
			New: func() interface{} {
				return &Connection{}
			},
		},
		maxSize: maxSize,
	}
}

func (cp *ConnectionPool) Get() *Connection {
	cp.mu.Lock()
	// Try to get from available slice first
	if len(cp.available) > 0 {
		conn := cp.available[len(cp.available)-1]
		cp.available = cp.available[:len(cp.available)-1]
		cp.mu.Unlock()
		conn.InUse = true
		return conn
	}
	cp.mu.Unlock()

	// Get from sync.Pool or create new
	conn := cp.pool.Get().(*Connection)
	if conn.ID == 0 { // New connection
		cp.mu.Lock()
		cp.created++
		conn.ID = cp.created
		cp.mu.Unlock()
	}
	conn.InUse = true
	return conn
}

func (cp *ConnectionPool) Put(conn *Connection) {
	if conn == nil {
		return
	}
	conn.InUse = false
	
	cp.mu.Lock()
	defer cp.mu.Unlock()
	
	// Only pool if we're under max size
	if len(cp.available) < cp.maxSize {
		cp.available = append(cp.available, conn)
	} else {
		// Return to sync.Pool
		cp.pool.Put(conn)
	}
}

/*
-------------------------------------------------------------------------------
5. CPU & MEMORY PROFILING (pprof)
-------------------------------------------------------------------------------
Go's built-in profiling tools for performance analysis.
*/

func startCPUProfile() (*os.File, error) {
	f, err := os.Create("cpu.prof")
	if err != nil {
		return nil, err
	}
	if err := pprof.StartCPUProfile(f); err != nil {
		f.Close()
		return nil, err
	}
	return f, nil
}

func stopCPUProfile(f *os.File) {
	pprof.StopCPUProfile()
	f.Close()
}

func writeHeapProfile() error {
	f, err := os.Create("heap.prof")
	if err != nil {
		return err
	}
	defer f.Close()
	return pprof.WriteHeapProfile(f)
}

func demonstrateProfiling() {
	fmt.Println("\n=== CPU & Memory Profiling ===")

	// Start CPU profiling
	profFile, err := startCPUProfile()
	if err != nil {
		log.Fatal("Could not start CPU profile: ", err)
	}
	defer stopCPUProfile(profFile)

	// Run workload to profile
	runProfiledWorkload()

	// Write heap profile
	if err := writeHeapProfile(); err != nil {
		log.Fatal("Could not write heap profile: ", err)
	}

	fmt.Println("Profiles written to cpu.prof and heap.prof")
	fmt.Println("Analyze with: go tool pprof cpu.prof")
	fmt.Println("Or: go tool pprof -http=:8080 cpu.prof")
}

func runProfiledWorkload() {
	// Simulate CPU-intensive work
	for i := 0; i < 1000000; i++ {
		_ = math.Sqrt(float64(i))
		_ = math.Sin(float64(i))
	}

	// Simulate memory allocation
	var data [][]byte
	for i := 0; i < 10000; i++ {
		data = append(data, make([]byte, 1024))
	}
	_ = data
}

// HTTP profiling endpoint (for web servers)
/*
import _ "net/http/pprof"

func startProfilingServer() {
	go func() {
		log.Println(http.ListenAndServe("localhost:6060", nil))
	}()
	// Then visit:
	// http://localhost:6060/debug/pprof/
	// http://localhost:6060/debug/pprof/heap
	// http://localhost:6060/debug/pprof/profile?seconds=30
}
*/

/*
-------------------------------------------------------------------------------
6. BENCHMARK-DRIVEN OPTIMIZATION
-------------------------------------------------------------------------------
Use Go's built-in benchmarking to measure and optimize performance.
*/

// Fibonacci examples for benchmarking
func fibRecursive(n int) int {
	if n <= 1 {
		return n
	}
	return fibRecursive(n-1) + fibRecursive(n-2)
}

func fibIterative(n int) int {
	if n <= 1 {
		return n
	}
	a, b := 0, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}

var fibMemo = sync.Map{}

func fibMemoized(n int) int {
	if n <= 1 {
		return n
	}
	if val, ok := fibMemo.Load(n); ok {
		return val.(int)
	}
	val := fibMemoized(n-1) + fibMemoized(n-2)
	fibMemo.Store(n, val)
	return val
}

// String concatenation benchmarks
func concatStringsSlow(strs []string) string {
	var result string
	for _, s := range strs {
		result += s
	}
	return result
}

func concatStringsBuilder(strs []string) string {
	var builder strings.Builder
	builder.Grow(len(strs) * 10) // Estimate size
	for _, s := range strs {
		builder.WriteString(s)
	}
	return builder.String()
}

// Sorting optimization example
type Person struct {
	Name string
	Age  int
}

func sortPeopleSlow(people []Person) {
	sort.Slice(people, func(i, j int) bool {
		return people[i].Age < people[j].Age
	})
}

// Pre-allocate and reuse to avoid closure allocation
var peopleSorter = func(people []Person) func(i, j int) bool {
	return func(i, j int) bool {
		return people[i].Age < people[j].Age
	}
}

func sortPeopleOptimized(people []Person) {
	sort.Slice(people, peopleSorter(people))
}

/*
-------------------------------------------------------------------------------
ADVANCED MEMORY OPTIMIZATION TECHNIQUES
-------------------------------------------------------------------------------
*/

// 1. Reducing Pointer Indirection
type CompactUser struct {
	// Group bools together to reduce padding
	Active, Verified, Premium bool
	ID                       int32
	Score                    float32
	// Use small int types when appropriate
	Age uint8
}

// Compare with inefficient version
type InefficientUser struct {
	ID       *int      // Unnecessary pointer
	Name     *string   // Unnecessary pointer
	Active   *bool     // Unnecessary pointer
	Metadata *struct { // Unnecessary nested struct
		Created time.Time
		Updated time.Time
	}
}

// 2. Slice Reuse Pattern
type SliceReuser struct {
	pool [][]byte
}

func (sr *SliceReuser) Get(size int) []byte {
	if len(sr.pool) > 0 {
		b := sr.pool[len(sr.pool)-1]
		sr.pool = sr.pool[:len(sr.pool)-1]
		if cap(b) >= size {
			return b[:size]
		}
	}
	return make([]byte, size)
}

func (sr *SliceReuser) Put(b []byte) {
	// Clear slice but keep capacity
	b = b[:0]
	sr.pool = append(sr.pool, b)
}

// 3. Arena-style Allocation (Advanced)
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
		return make([]byte, size) // Fallback
	}
	slice := a.buf[a.index : a.index+size]
	a.index += size
	return slice
}

func (a *Arena) Reset() {
	a.index = 0
	// Optionally zero the memory for security
	// for i := range a.buf {
	//     a.buf[i] = 0
	// }
}

// 4. Memory-mapped I/O Simulation
type MemoryMappedCache struct {
	data []byte
	mu   sync.RWMutex
}

func NewMemoryMappedCache(size int) *MemoryMappedCache {
	// Simulate memory mapping
	data := make([]byte, size)
	return &MemoryMappedCache{data: data}
}

func (mmc *MemoryMappedCache) Read(offset, size int) ([]byte, bool) {
	mmc.mu.RLock()
	defer mmc.mu.RUnlock()
	
	if offset+size > len(mmc.data) {
		return nil, false
	}
	// Return slice into existing data (no copy)
	return mmc.data[offset : offset+size], true
}

/*
-------------------------------------------------------------------------------
PERFORMANCE MONITORING IN PRODUCTION
-------------------------------------------------------------------------------
*/

type PerformanceMonitor struct {
	allocations uint64
	mu          sync.Mutex
	startTime   time.Time
}

func NewPerformanceMonitor() *PerformanceMonitor {
	pm := &PerformanceMonitor{
		startTime: time.Now(),
	}
	// Sample memory stats periodically
	go pm.monitor()
	return pm
}

func (pm *PerformanceMonitor) monitor() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	
	for range ticker.C {
		var stats runtime.MemStats
		runtime.ReadMemStats(&stats)
		
		pm.mu.Lock()
		pm.allocations = stats.Mallocs
		pm.mu.Unlock()
		
		// Log or alert on thresholds
		if stats.HeapInuse > 100*1024*1024 { // 100MB
			log.Printf("High memory usage: %v MB", stats.HeapInuse/1024/1024)
		}
	}
}

func (pm *PerformanceMonitor) GetAllocationCount() uint64 {
	pm.mu.Lock()
	defer pm.mu.Unlock()
	return pm.allocations
}

/*
-------------------------------------------------------------------------------
PRACTICAL EXAMPLE: HIGH-PERFORMANCE CACHE
-------------------------------------------------------------------------------
*/

type CacheEntry struct {
	value      interface{}
	expiration time.Time
	size       int
}

type HighPerfCache struct {
	entries    map[string]*CacheEntry
	mu         sync.RWMutex
	maxMemory  int
	usedMemory int
	pool       sync.Pool
}

func NewHighPerfCache(maxMemoryMB int) *HighPerfCache {
	return &HighPerfCache{
		entries:   make(map[string]*CacheEntry),
		maxMemory: maxMemoryMB * 1024 * 1024,
		pool: sync.Pool{
			New: func() interface{} {
				return &CacheEntry{}
			},
		},
	}
}

func (c *HighPerfCache) Get(key string) (interface{}, bool) {
	c.mu.RLock()
	entry, exists := c.entries[key]
	c.mu.RUnlock()
	
	if !exists {
		return nil, false
	}
	
	if time.Now().After(entry.expiration) {
		c.Delete(key)
		return nil, false
	}
	
	return entry.value, true
}

func (c *HighPerfCache) Set(key string, value interface{}, ttl time.Duration, size int) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	// Reuse entry from pool
	entry := c.pool.Get().(*CacheEntry)
	entry.value = value
	entry.expiration = time.Now().Add(ttl)
	entry.size = size
	
	// Evict if necessary
	if c.usedMemory+size > c.maxMemory {
		c.evictSome()
	}
	
	// Update memory usage
	if oldEntry, exists := c.entries[key]; exists {
		c.usedMemory -= oldEntry.size
	}
	
	c.entries[key] = entry
	c.usedMemory += size
}

func (c *HighPerfCache) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	
	if entry, exists := c.entries[key]; exists {
		c.usedMemory -= entry.size
		// Return to pool
		entry.value = nil
		c.pool.Put(entry)
		delete(c.entries, key)
	}
}

func (c *HighPerfCache) evictSome() {
	// Simple eviction: remove expired entries first
	now := time.Now()
	for key, entry := range c.entries {
		if now.After(entry.expiration) {
			c.Delete(key)
		}
	}
	
	// If still over limit, remove random entries
	if c.usedMemory > c.maxMemory {
		for key := range c.entries {
			if c.usedMemory <= c.maxMemory {
				break
			}
			c.Delete(key)
		}
	}
}

/*
-------------------------------------------------------------------------------
MAIN DEMONSTRATION FUNCTION
-------------------------------------------------------------------------------
*/

func main() {
	fmt.Println("=== Go Memory Management & Performance ===")
	
	// Show GC behavior
	demonstrateGCBehavior()
	
	// Show allocation patterns
	demonstrateAllocations()
	
	// Show escape analysis concepts
	escapeAnalysisExamples()
	
	// Demonstrate object pooling
	demonstrateObjectPooling()
	
	// Run profiling example (commented to avoid file creation)
	// demonstrateProfiling()
	
	// Show performance monitor
	monitor := NewPerformanceMonitor()
	_ = monitor
	
	// Demonstrate cache
	cache := NewHighPerfCache(10) // 10MB cache
	cache.Set("key1", "value1", 5*time.Minute, 100)
	val, found := cache.Get("key1")
	if found {
		fmt.Printf("Cache hit: %v\n", val)
	}
	
	// Memory stats
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	fmt.Printf("\n=== Final Memory Stats ===\n")
	fmt.Printf("Alloc = %v MiB\n", m.Alloc/1024/1024)
	fmt.Printf("TotalAlloc = %v MiB\n", m.TotalAlloc/1024/1024)
	fmt.Printf("Sys = %v MiB\n", m.Sys/1024/1024)
	fmt.Printf("NumGC = %v\n", m.NumGC)
	
	// Force final GC for clean measurement
	runtime.GC()
	time.Sleep(100 * time.Millisecond)
	
	fmt.Println("\n=== Performance Tips Summary ===")
	printPerformanceTips()
}

func printPerformanceTips() {
	tips := []string{
		"1. Pre-allocate slices/maps when size is known",
		"2. Use sync.Pool for frequently allocated objects",
		"3. Avoid unnecessary heap allocations (check escape analysis)",
		"4. Reuse buffers and objects when possible",
		"5. Use strings.Builder for string concatenation",
		"6. Profile before optimizing - use pprof",
		"7. Write benchmarks for performance-critical code",
		"8. Consider data locality and cache lines",
		"9. Use appropriate data types (int32 vs int64)",
		"10. Monitor GC pauses in production",
	}
	
	for _, tip := range tips {
		fmt.Println(tip)
	}
}

// Helper function for strings.Builder
var strings.Builder

/*
-------------------------------------------------------------------------------
BENCHMARKS (Normally in _test.go files)
-------------------------------------------------------------------------------
Example benchmark file content:

func BenchmarkFibRecursive(b *testing.B) {
	for i := 0; i < b.N; i++ {
		fibRecursive(20)
	}
}

func BenchmarkFibIterative(b *testing.B) {
	for i := 0; i < b.N; i++ {
		fibIterative(20)
	}
}

func BenchmarkConcatStringsSlow(b *testing.B) {
	strs := make([]string, 1000)
	for i := range strs {
		strs[i] = "test"
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		concatStringsSlow(strs)
	}
}

func BenchmarkConcatStringsBuilder(b *testing.B) {
	strs := make([]string, 1000)
	for i := range strs {
		strs[i] = "test"
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		concatStringsBuilder(strs)
	}
}

Run with: go test -bench=. -benchmem
*/

/*
-------------------------------------------------------------------------------
KEY TAKEAWAYS:
-------------------------------------------------------------------------------
1. Go's GC is concurrent but allocations still have cost
2. Minimize heap allocations through escape analysis awareness
3. Use sync.Pool for objects with high allocation rates
4. Always profile before optimizing (pprof is your friend)
5. Write benchmarks to validate performance improvements
6. Memory layout matters - consider data structure design
7. Reuse buffers and objects to reduce GC pressure
8. Pre-allocate slices and maps when size is known
9. Monitor production performance with runtime metrics
10. Balance optimization with code readability
*/