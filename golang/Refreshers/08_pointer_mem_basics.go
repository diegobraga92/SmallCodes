// ============================================
// GO POINTERS & MEMORY - COMPREHENSIVE GUIDE
// ============================================

package main

import (
	"fmt"
	"runtime"
	"unsafe"
)

// ============================================
// 1. POINTER SEMANTICS
// ============================================

// A pointer holds the memory address of a value.
// The zero value of a pointer is nil.
// & operator generates a pointer to its operand.
// * operator dereferences a pointer (accesses the underlying value).

func pointerSemantics() {
	fmt.Println("\n=== 1. Pointer Semantics ===")
	
	// Basic types
	x := 42
	var p *int        // Declare pointer to int
	p = &x           // p now points to x
	fmt.Printf("x = %d, p = %p, *p = %d\n", x, p, *p)
	
	// Modifying through pointer
	*p = 100
	fmt.Printf("After *p = 100: x = %d\n", x)
	
	// Pointer to struct
	type Person struct {
		Name string
		Age  int
	}
	
	john := Person{Name: "John", Age: 30}
	personPtr := &john
	personPtr.Age = 31 // Equivalent to (*personPtr).Age = 31
	fmt.Printf("John's age: %d\n", john.Age)
	
	// Pointer arithmetic is NOT allowed in Go (unlike C/C++)
	// p++ // Compile error: invalid operation
	
	// Comparing pointers
	var p1, p2 *int
	fmt.Printf("p1 == p2: %v (both nil)\n", p1 == p2)
	
	p1 = &x
	p2 = &x
	fmt.Printf("p1 == p2 (same address): %v\n", p1 == p2)
	
	y := 42
	p3 := &y
	fmt.Printf("p1 == p3 (different addresses): %v\n", p1 == p3)
	
	// Pointer to pointer (rarely needed, but possible)
	var pp **int = &p1
	fmt.Printf("Pointer to pointer: pp = %p, *pp = %p, **pp = %d\n", 
		pp, *pp, **pp)
}

// ============================================
// 2. PASSING BY VALUE VS REFERENCE
// ============================================

// Go is ALWAYS pass-by-value. However, when you pass a pointer,
// you're passing the pointer value (the memory address) by value.

// Passing by value (copy of the entire struct)
func modifyByValue(p Person) {
	p.Age += 10 // Modifies copy, not original
	fmt.Printf("Inside modifyByValue: Age = %d\n", p.Age)
}

// Passing by pointer (copy of the pointer)
func modifyByPointer(p *Person) {
	p.Age += 10 // Modifies original through pointer
	fmt.Printf("Inside modifyByPointer: Age = %d\n", p.Age)
}

// Passing slices (slice header is passed by value, but underlying array is shared)
func modifySlice(s []int) {
	if len(s) > 0 {
		s[0] = 999 // Modifies underlying array
	}
	// Appending may or may not affect original (depends on capacity)
	s = append(s, 100)
	fmt.Printf("Inside modifySlice: len=%d, cap=%d\n", len(s), cap(s))
}

func passByValueVsReference() {
	fmt.Println("\n=== 2. Passing by Value vs Reference ===")
	
	// Struct example
	person := Person{Name: "Alice", Age: 25}
	
	fmt.Printf("Before modifyByValue: Age = %d\n", person.Age)
	modifyByValue(person)
	fmt.Printf("After modifyByValue: Age = %d (unchanged)\n", person.Age)
	
	fmt.Printf("\nBefore modifyByPointer: Age = %d\n", person.Age)
	modifyByPointer(&person)
	fmt.Printf("After modifyByPointer: Age = %d (changed)\n", person.Age)
	
	// Slice example
	nums := make([]int, 3, 5)
	nums[0] = 1
	nums[1] = 2
	nums[2] = 3
	
	fmt.Printf("\nSlice before: %v, len=%d, cap=%d\n", nums, len(nums), cap(nums))
	modifySlice(nums)
	fmt.Printf("Slice after: %v, len=%d, cap=%d (first element changed!)\n", 
		nums, len(nums), cap(nums))
	
	// Map example (map is a pointer under the hood)
	m := map[string]int{"a": 1, "b": 2}
	fmt.Printf("\nMap before: %v\n", m)
	// No need to pass pointer - map is already a reference type
	m["a"] = 100
	fmt.Printf("Map after: %v\n", m)
	
	// When to use pointers:
	// 1. When you need to modify the original value
	// 2. For large structs to avoid copying costs
	// 3. When implementing methods that modify the receiver
	// 4. When a value can be nil (optional parameters)
	
	// When NOT to use pointers:
	// 1. Small values (ints, floats, bools)
	// 2. When immutability is desired
	// 3. Simple types that fit in registers
}

// ============================================
// 3. ESCAPE ANALYSIS (HIGH-LEVEL UNDERSTANDING)
// ============================================

// Escape analysis determines whether a variable can be allocated on the stack
// or must be allocated on the heap.
// Stack allocation is faster, heap allocation allows variables to outlive function scope.

//go:noinline (forces escape analysis to consider escape scenarios)
func escapeToHeap() *int {
	x := 42 // x escapes to heap because its address is returned
	return &x
}

//go:noinline
func stayOnStack() int {
	x := 42 // Stays on stack (address never taken or escapes)
	return x
}

//go:noinline
func interfaceEscape() interface{} {
	x := 100 // x escapes to heap (interfaces can store any value)
	return x
}

//go:noinline
func noEscape() {
	x := 42
	_ = x // No escape - address never taken
}

//go:noinline  
func closureEscape() func() int {
	x := 42 // x escapes to heap (captured by closure)
	return func() int {
		return x
	}
}

func escapeAnalysisDemo() {
	fmt.Println("\n=== 3. Escape Analysis ===")
	
	// These allocations may stay on stack (compiler dependent)
	a := stayOnStack()
	fmt.Printf("Stack value: %d\n", a)
	
	// This allocation escapes to heap
	b := escapeToHeap()
	fmt.Printf("Heap value: %d (address: %p)\n", *b, b)
	
	// Interface causes escape
	c := interfaceEscape()
	fmt.Printf("Interface value: %v\n", c)
	
	// Closure captures variable
	fn := closureEscape()
	fmt.Printf("Closure result: %d\n", fn())
	
	// Check memory stats
	var memStats runtime.MemStats
	runtime.ReadMemStats(&memStats)
	fmt.Printf("\nHeap allocations: %d\n", memStats.Mallocs)
	fmt.Printf("Heap objects: %d\n", memStats.HeapObjects)
	
	// Common escape triggers:
	// 1. Returning address of local variable
	// 2. Storing pointers in heap-allocated data (slices, maps, channels)
	// 3. Using interfaces (dynamic dispatch)
	// 4. Capturing variables in closures
	// 5. Exceeding stack size
}

// ============================================
// 4. STACK VS HEAP (CONCEPTUAL)
// ============================================

// Stack:
// - Fast allocation/deallocation (LIFO)
// - Limited size (~1MB default, can grow)
// - Automatic cleanup when function returns
// - Each goroutine has its own stack

// Heap:
// - Slower allocation (requires GC)
// - Larger available memory
// - Managed by garbage collector
// - Shared across goroutines

type LargeStruct struct {
	data [1024]byte // 1KB
	id   int
}

func stackAllocation() {
	// May allocate on stack if compiler can prove it doesn't escape
	var s LargeStruct
	s.id = 1
	_ = s
}

func heapAllocation() *LargeStruct {
	// Definitely allocates on heap (address escapes)
	s := &LargeStruct{id: 2}
	return s
}

func mixedAllocation() {
	// Some allocations escape, some don't
	s1 := LargeStruct{id: 1}  // Might be stack
	s2 := &LargeStruct{id: 2} // Might be heap if address escapes
	
	// Slice of pointers - elements may escape
	slice := make([]*LargeStruct, 0, 10)
	slice = append(slice, &s1) // &s1 may cause s1 to escape
	slice = append(slice, s2)
	
	_ = slice
}

func stackVsHeapDemo() {
	fmt.Println("\n=== 4. Stack vs Heap ===")
	
	// Show current goroutine stack size
	fmt.Printf("Default stack size per goroutine: ~%dKB\n", 1<<10)
	
	// Stack growth demonstration
	deepRecursion(0)
	
	// Heap allocation example
	heapStructs := make([]*LargeStruct, 0, 100)
	for i := 0; i < 100; i++ {
		s := &LargeStruct{id: i}
		heapStructs = append(heapStructs, s)
	}
	fmt.Printf("Allocated %d large structs on heap\n", len(heapStructs))
	
	// Forcing heap allocation with runtime.SetFinalizer
	obj := &LargeStruct{id: 999}
	runtime.SetFinalizer(obj, func(o *LargeStruct) {
		fmt.Printf("LargeStruct %d finalized by GC\n", o.id)
	})
	
	// Memory usage
	var memStats runtime.MemStats
	runtime.GC() // Request garbage collection
	runtime.ReadMemStats(&memStats)
	
	fmt.Printf("\nMemory Statistics:\n")
	fmt.Printf("  HeapAlloc: %v bytes\n", memStats.HeapAlloc)
	fmt.Printf("  StackInuse: %v bytes\n", memStats.StackInuse)
	fmt.Printf("  NextGC: %v bytes\n", memStats.NextGC)
}

func deepRecursion(depth int) {
	if depth >= 1000 {
		// Stack growth happens automatically when needed
		return
	}
	// Each call uses stack space
	deepRecursion(depth + 1)
}

// ============================================
// 5. PRACTICAL PATTERNS & BEST PRACTICES
// ============================================

// Pointer receiver methods
type Counter struct {
	value int
}

// Value receiver (works on copy)
func (c Counter) IncrementByValue() Counter {
	c.value++
	return c
}

// Pointer receiver (modifies original)
func (c *Counter) IncrementByPointer() {
	c.value++
}

func (c Counter) Value() int {
	return c.value
}

// Returning pointers from factory functions
func NewCounter(initial int) *Counter {
	return &Counter{value: initial}
}

// Nil pointer safety
func safeDereference(p *Counter) {
	if p != nil {
		fmt.Printf("Counter value: %d\n", p.value)
	} else {
		fmt.Println("Counter is nil")
	}
}

// Pointer vs value semantics for methods
// Rule of thumb: If a method modifies the receiver, use pointer receiver.
// If it doesn't modify, use value receiver.

func practicalPatterns() {
	fmt.Println("\n=== 5. Practical Patterns ===")
	
	// Pointer receiver pattern
	counter1 := Counter{value: 0}
	counter1.IncrementByValue()
	fmt.Printf("After value receiver: %d (unchanged)\n", counter1.Value())
	
	counter1.IncrementByPointer()
	fmt.Printf("After pointer receiver: %d (changed)\n", counter1.Value())
	
	// Factory function returning pointer
	counter2 := NewCounter(10)
	fmt.Printf("Factory-created counter: %d\n", counter2.Value())
	
	// Nil pointer safety
	var nilCounter *Counter
	safeDereference(nilCounter)
	
	// Pointer to array vs slice
	arr := [3]int{1, 2, 3}
	slice := []int{1, 2, 3}
	
	arrPtr := &arr
	slicePtr := &slice
	
	// Arrays: need pointer to modify elements in another function
	// Slices: already reference types, but pointer can be useful for resizing
	
	fmt.Printf("\nArray pointer: %p, Slice pointer: %p\n", arrPtr, slicePtr)
	
	// Performance consideration
	type BigData struct {
		data [10000]int
	}
	
	// Passing by value copies 10000 ints
	// Passing by pointer copies 1 pointer (8 bytes on 64-bit)
	
	// Use benchmarks to decide!
}

// ============================================
// 6. ADVANCED TOPICS
// ============================================

// unsafe.Pointer for low-level operations (use with caution!)
func unsafeOperations() {
	fmt.Println("\n=== 6. Advanced Topics ===")
	
	// Regular pointer (type-safe)
	x := 42
	p := &x
	
	// unsafe.Pointer can convert between pointer types
	unsafePtr := unsafe.Pointer(p)
	
	// Convert back to different pointer type (dangerous!)
	intPtr := (*int)(unsafePtr)
	fmt.Printf("Original: %d, Unsafe round-trip: %d\n", x, *intPtr)
	
	// Size and alignment
	fmt.Printf("Size of int: %d bytes\n", unsafe.Sizeof(x))
	fmt.Printf("Alignment of int: %d bytes\n", unsafe.Alignof(x))
	
	// Warning: unsafe breaks type safety and memory safety guarantees!
	// Only use in performance-critical, low-level code.
}

// Memory layout demonstration
type MemoryLayout struct {
	a bool    // 1 byte (+7 padding)
	b int64   // 8 bytes
	c int32   // 4 bytes (+4 padding on 64-bit systems)
	d int16   // 2 bytes (+6 padding)
}

func (ml *MemoryLayout) PrintLayout() {
	fmt.Printf("\nMemoryLayout size: %d bytes\n", unsafe.Sizeof(*ml))
	fmt.Printf("Field offsets:\n")
	fmt.Printf("  a (bool):   %d\n", unsafe.Offsetof(ml.a))
	fmt.Printf("  b (int64):  %d\n", unsafe.Offsetof(ml.b))
	fmt.Printf("  c (int32):  %d\n", unsafe.Offsetof(ml.c))
	fmt.Printf("  d (int16):  %d\n", unsafe.Offsetof(ml.d))
}

// ============================================
// 7. COMMON GOTCHAS & ANTIPATTERNS
// ============================================

func commonGotchas() {
	fmt.Println("\n=== 7. Common Gotchas ===")
	
	// 1. Returning pointer to local variable IS allowed (escape analysis)
	//    But modifying after return is dangerous
	func() {
		p := escapeToHeap()
		fmt.Printf("Gotcha 1 - Valid: %d\n", *p) // OK - x still reachable
	}()
	
	// 2. Pointer to loop variable
	var pointers []*int
	for i := 0; i < 3; i++ {
		pointers = append(pointers, &i) // WRONG! All point to same i
	}
	fmt.Printf("Gotcha 2 - Loop pointers: %v %v %v\n", 
		*pointers[0], *pointers[1], *pointers[2])
	
	// Correct way
	pointers = nil
	for i := 0; i < 3; i++ {
		val := i // New variable each iteration
		pointers = append(pointers, &val)
	}
	fmt.Printf("Fixed loop pointers: %v %v %v\n", 
		*pointers[0], *pointers[1], *pointers[2])
	
	// 3. Nil pointer dereference
	var nilPtr *int
	// fmt.Printf("%d\n", *nilPtr) // PANIC: nil pointer dereference
	
	// 4. Pointer to interface (rarely needed)
	var w io.Writer
	// pw := &w // Pointer to interface (usually unnecessary)
	
	// 5. Modifying slice header vs underlying array
	slice := []int{1, 2, 3}
	modifySliceHeader(slice)
	fmt.Printf("Gotcha 5 - Slice after header mod: %v\n", slice)
}

func modifySliceHeader(s []int) {
	s = s[:1] // Only modifies local copy of slice header
}

// ============================================
// MAIN DEMONSTRATION
// ============================================

import (
	"io"
)

func main() {
	fmt.Println("=== GO POINTERS & MEMORY MANAGEMENT ===")
	
	// Run all demonstrations
	pointerSemantics()
	passByValueVsReference()
	escapeAnalysisDemo()
	stackVsHeapDemo()
	practicalPatterns()
	unsafeOperations()
	commonGotchas()
	
	// Memory layout example
	ml := MemoryLayout{}
	ml.PrintLayout()
	
	fmt.Println("\n=== END OF DEMONSTRATION ===")
	
	// Force GC to see finalizer in action
	runtime.GC()
	runtime.Gosched() // Give GC time to run
}

// ============================================
// KEY TAKEAWAYS FOR DEVELOPERS:
// ============================================

// JUNIOR DEVELOPERS:
// 1. Use & to get address, * to dereference
// 2. Go is always pass-by-value (even pointers are passed by value)
// 3. Pointer receivers modify the original, value receivers work on copies
// 4. Check for nil before dereferencing
// 5. Slices and maps are reference-like (but still passed by value)

// MID-LEVEL DEVELOPERS:
// 1. Understand escape analysis basics
// 2. Know when to use pointers vs values (performance vs safety)
// 3. Use factory functions that return pointers
// 4. Be careful with pointers in loops
// 5. Understand slice/map/channel internals (they're not "references")

// SENIOR DEVELOPERS:
// 1. Profile memory allocations and escape analysis
// 2. Use -gcflags="-m" to see escape analysis decisions
// 3. Understand stack vs heap trade-offs
// 4. Know when to use unsafe.Pointer (rarely!)
// 5. Design APIs with clear ownership semantics
// 6. Consider cache locality and pointer chasing

// PERFORMANCE TIPS:
// 1. Small, short-lived objects should stay on stack
// 2. Avoid unnecessary pointers (pointer chasing is slow)
// 3. Preallocate slices/maps when size is known
// 4. Reuse objects with sync.Pool when appropriate
// 5. Value semantics often enable better compiler optimizations

// SAFETY TIPS:
// 1. Always validate pointers before use
// 2. Use the "ok" idiom with type assertions
// 3. Set pointers to nil after use when appropriate
// 4. Be careful with cgo and foreign pointers
// 5. Use race detector for concurrent pointer access