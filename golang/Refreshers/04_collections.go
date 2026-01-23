/*
   Go Collections - Comprehensive Example with Detailed Comments

   This file demonstrates Go's collection types with practical examples:
   - Arrays (fixed-size, value type)
   - Slices (dynamic-size, reference to underlying array)
   - Maps (hash maps, key-value stores)
   - Range loops for iteration

   Understanding slices is crucial for Go programming as they're used more often than arrays.
*/

package main

import (
	"fmt"
	"reflect"
	"sort"
	"strings"
)

func main() {
	fmt.Println("=== GO COLLECTIONS DEMONSTRATION ===")
	fmt.Println()

	/*
	   SECTION 1: ARRAYS

	   Arrays in Go:
	   - Fixed size (determined at compile time)
	   - Value type (copied when assigned or passed)
	   - Zero value is array of zero values
	   - Length is part of the type ([3]int ≠ [5]int)
	*/

	fmt.Println("=== 1. ARRAYS (Fixed Size) ===")

	// -----------------------------------------------------------------
	// Array declaration and initialization
	// -----------------------------------------------------------------
	fmt.Println("\n1. Array Declaration:")

	// Zero-valued array (all elements 0)
	var arr1 [5]int
	fmt.Printf("   var arr1 [5]int\t\t\t= %v\n", arr1)

	// Array literal with values
	arr2 := [3]int{10, 20, 30}
	fmt.Printf("   arr2 := [3]int{10, 20, 30}\t\t= %v\n", arr2)

	// Let compiler count elements
	arr3 := [...]int{1, 2, 3, 4, 5}
	fmt.Printf("   arr3 := [...]int{1, 2, 3, 4, 5}\t= %v (length: %d)\n", arr3, len(arr3))

	// Array with specific indices
	arr4 := [5]int{1: 100, 4: 500}
	fmt.Printf("   arr4 := [5]int{1:100, 4:500}\t= %v\n", arr4)

	// -----------------------------------------------------------------
	// Array operations
	// -----------------------------------------------------------------
	fmt.Println("\n2. Array Operations:")

	// Access and modify elements
	arr5 := [3]string{"apple", "banana", "cherry"}
	fmt.Printf("   arr5[0] = \"%s\"\n", arr5[0])

	arr5[1] = "blueberry"
	fmt.Printf("   After arr5[1] = \"blueberry\": %v\n", arr5)

	// Array length
	fmt.Printf("   len(arr5) = %d\n", len(arr5))

	// Iterate over array
	fmt.Print("   Iterating with for loop: ")
	for i := 0; i < len(arr5); i++ {
		fmt.Printf("%s ", arr5[i])
	}
	fmt.Println()

	// -----------------------------------------------------------------
	// Arrays are VALUE TYPES (important!)
	// -----------------------------------------------------------------
	fmt.Println("\n3. Arrays are Value Types:")

	original := [3]int{1, 2, 3}
	copy := original // Creates a complete copy!

	copy[0] = 99 // Modify the copy

	fmt.Printf("   original = %v\n", original)
	fmt.Printf("   copy     = %v (after modification)\n", copy)
	fmt.Printf("   original == copy? %v\n", original == copy)

	// -----------------------------------------------------------------
	// Multi-dimensional arrays
	// -----------------------------------------------------------------
	fmt.Println("\n4. Multi-dimensional Arrays:")

	var matrix [2][3]int
	matrix[0] = [3]int{1, 2, 3}
	matrix[1] = [3]int{4, 5, 6}

	fmt.Printf("   2x3 matrix: %v\n", matrix)
	fmt.Printf("   matrix[1][2] = %d\n", matrix[1][2])

	// Initialize in one line
	matrix2 := [2][2]int{{1, 2}, {3, 4}}
	fmt.Printf("   2x2 matrix: %v\n", matrix2)

	fmt.Println()

	/*
	   SECTION 2: SLICES

	   Slices are Go's dynamic array type and are used more frequently than arrays.
	   Key characteristics:
	   - Dynamic size (can grow and shrink)
	   - Reference type (points to underlying array)
	   - Zero value is nil
	   - Three components: pointer, length, capacity
	*/

	fmt.Println("=== 2. SLICES (Dynamic Arrays) ===")

	// -----------------------------------------------------------------
	// Slice declaration and initialization
	// -----------------------------------------------------------------
	fmt.Println("\n1. Slice Declaration:")

	// Zero-valued slice (nil)
	var slice1 []int
	fmt.Printf("   var slice1 []int\t\t\t= %v (nil? %v)\n", slice1, slice1 == nil)

	// Empty slice (not nil)
	slice2 := []int{}
	fmt.Printf("   slice2 := []int{}\t\t\t= %v (nil? %v)\n", slice2, slice2 == nil)

	// Slice literal
	slice3 := []int{10, 20, 30, 40, 50}
	fmt.Printf("   slice3 := []int{10,20,30,40,50}\t= %v\n", slice3)

	// Slice from array (slicing)
	arr := [5]int{1, 2, 3, 4, 5}
	slice4 := arr[1:4] // Elements 1, 2, 3 (1 inclusive, 4 exclusive)
	fmt.Printf("   arr := [5]int{1,2,3,4,5}\n")
	fmt.Printf("   slice4 := arr[1:4]\t\t\t= %v\n", slice4)

	// Using make() to create slice with specific capacity
	slice5 := make([]int, 3, 5) // length=3, capacity=5
	fmt.Printf("   slice5 := make([]int, 3, 5)\t= %v (len=%d, cap=%d)\n",
		slice5, len(slice5), cap(slice5))

	// -----------------------------------------------------------------
	// SLICE INTERNALS: Length vs Capacity
	// -----------------------------------------------------------------
	fmt.Println("\n2. Slice Internals (Length vs Capacity):")

	/*
	   A slice is a descriptor of an array segment.
	   It consists of:
	   - Pointer to underlying array element
	   - Length (number of elements in slice)
	   - Capacity (max elements from pointer to end of array)

	   Visual example:
	   Underlying array: [0,1,2,3,4,5,6,7,8,9]
	   Slice s := arr[2:5]

	   s points to arr[2]
	   len(s) = 3 (elements 2,3,4)
	   cap(s) = 8 (from arr[2] to arr[9])
	*/

	underlying := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	s := underlying[2:5]

	fmt.Printf("   underlying := [10]int{0,1,2,3,4,5,6,7,8,9}\n")
	fmt.Printf("   s := underlying[2:5]\n")
	fmt.Printf("   s = %v (len=%d, cap=%d)\n", s, len(s), cap(s))

	// Show what happens when we extend the slice
	s2 := s[:cap(s)] // Extend to full capacity
	fmt.Printf("   s2 := s[:cap(s)]\t\t\t= %v (len=%d, cap=%d)\n",
		s2, len(s2), cap(s2))

	// -----------------------------------------------------------------
	// Slice operations
	// -----------------------------------------------------------------
	fmt.Println("\n3. Slice Operations:")

	fruits := []string{"apple", "banana", "cherry", "date", "elderberry"}

	// Slicing operations
	fmt.Printf("   fruits = %v\n", fruits)
	fmt.Printf("   fruits[1:3] = %v\n", fruits[1:3]) // [banana, cherry]
	fmt.Printf("   fruits[:3] = %v\n", fruits[:3])   // [apple, banana, cherry]
	fmt.Printf("   fruits[2:] = %v\n", fruits[2:])   // [cherry, date, elderberry]
	fmt.Printf("   fruits[:] = %v (full slice)\n", fruits[:])

	// Length and capacity
	fmt.Printf("   len(fruits) = %d, cap(fruits) = %d\n", len(fruits), cap(fruits))

	// -----------------------------------------------------------------
	// APPEND BEHAVIOR
	// -----------------------------------------------------------------
	fmt.Println("\n4. Append Behavior:")

	/*
	   append() is how slices grow in Go.
	   Behavior depends on capacity:
	   1. If capacity available: add to existing array
	   2. If capacity full: allocate new larger array (usually 2x) and copy

	   The capacity growth strategy is implementation detail but typically:
	   - Small slices: double capacity
	   - Large slices: grow by 25%
	*/

	// Start with small slice
	numbers := make([]int, 0, 3) // len=0, cap=3
	fmt.Printf("   numbers := make([]int, 0, 3)\n")
	fmt.Printf("   Initial: len=%d, cap=%d, %v\n", len(numbers), cap(numbers), numbers)

	// Append within capacity
	numbers = append(numbers, 1)
	fmt.Printf("   append 1: len=%d, cap=%d, %v\n", len(numbers), cap(numbers), numbers)

	numbers = append(numbers, 2, 3)
	fmt.Printf("   append 2,3: len=%d, cap=%d, %v\n", len(numbers), cap(numbers), numbers)

	// Append beyond capacity - new allocation!
	oldCap := cap(numbers)
	numbers = append(numbers, 4)
	fmt.Printf("   append 4 (exceeds capacity):\n")
	fmt.Printf("     Old capacity: %d\n", oldCap)
	fmt.Printf("     New capacity: %d (usually doubled)\n", cap(numbers))
	fmt.Printf("     Slice: %v\n", numbers)

	// Show capacity growth pattern
	fmt.Println("\n   Capacity growth demonstration:")
	var growth []int
	for i := 0; i < 20; i++ {
		growth = append(growth, i)
		if i < 10 || i%5 == 0 {
			fmt.Printf("     Append %2d: len=%2d, cap=%2d\n", i, len(growth), cap(growth))
		}
	}

	// -----------------------------------------------------------------
	// COPYING SLICES (Important!)
	// -----------------------------------------------------------------
	fmt.Println("\n5. Copying Slices:")

	/*
	   Slices are reference types! Assigning creates a new reference, not a copy.
	   To actually copy data, use copy() function or append to nil slice.
	*/

	// WRONG way (just creates new reference)
	originalSlice := []int{1, 2, 3}
	referenceCopy := originalSlice

	referenceCopy[0] = 99
	fmt.Printf("   Original slice: %v\n", originalSlice)
	fmt.Printf("   Reference copy: %v (MODIFIED ORIGINAL!)\n", referenceCopy)

	// RIGHT way 1: Using copy() function
	originalSlice2 := []int{1, 2, 3}
	copy1 := make([]int, len(originalSlice2))
	copy(copy1, originalSlice2)

	copy1[0] = 99
	fmt.Printf("\n   Using copy() function:\n")
	fmt.Printf("   Original: %v\n", originalSlice2)
	fmt.Printf("   Copy:     %v (original unchanged)\n", copy1)

	// copy() returns number of elements copied
	src := []int{1, 2, 3, 4, 5}
	dst := make([]int, 3)
	copied := copy(dst, src)
	fmt.Printf("   copy(dst[cap=3], src[5]) = %d elements copied\n", copied)
	fmt.Printf("   dst = %v\n", dst)

	// RIGHT way 2: Using append to nil slice
	originalSlice3 := []int{10, 20, 30}
	copy2 := append([]int(nil), originalSlice3...)

	copy2[0] = 99
	fmt.Printf("\n   Using append to nil slice:\n")
	fmt.Printf("   Original: %v\n", originalSlice3)
	fmt.Printf("   Copy:     %v\n", copy2)

	// RIGHT way 3: Full slice expression [:]
	originalSlice4 := []int{100, 200, 300}
	copy3 := originalSlice4[:] // Still a reference!
	// Wait, this is also just a reference. Need to combine with copy.
	copy4 := make([]int, len(originalSlice4))
	copy(copy4, originalSlice4[:])

	fmt.Printf("\n   Important: s[:] creates new slice descriptor but same backing array!\n")

	// -----------------------------------------------------------------
	// Common slice patterns
	// -----------------------------------------------------------------
	fmt.Println("\n6. Common Slice Patterns:")

	// Remove element (preserving order)
	removeIndex := func(s []int, i int) []int {
		return append(s[:i], s[i+1:]...)
	}

	nums := []int{1, 2, 3, 4, 5}
	fmt.Printf("   Original: %v\n", nums)
	nums = removeIndex(nums, 2) // Remove element at index 2 (value 3)
	fmt.Printf("   After removing index 2: %v\n", nums)

	// Remove element (without preserving order, faster)
	removeFast := func(s []int, i int) []int {
		s[i] = s[len(s)-1]  // Move last element to position i
		return s[:len(s)-1] // Truncate slice
	}

	nums2 := []int{10, 20, 30, 40, 50}
	nums2 = removeFast(nums2, 1) // Remove index 1
	fmt.Printf("   Fast remove index 1: %v (order changed)\n", nums2)

	// Filter elements
	filterEven := func(s []int) []int {
		result := []int{}
		for _, v := range s {
			if v%2 == 0 {
				result = append(result, v)
			}
		}
		return result
	}

	mixed := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	evens := filterEven(mixed)
	fmt.Printf("   Filter even numbers from %v:\n", mixed)
	fmt.Printf("   Result: %v\n", evens)

	// Pre-allocate slice when size is known
	fmt.Println("\n7. Pre-allocation for Performance:")
	size := 10000
	preallocated := make([]int, 0, size) // Pre-allocate capacity
	for i := 0; i < size; i++ {
		preallocated = append(preallocated, i)
	}
	fmt.Printf("   Preallocated slice with cap=%d: final len=%d\n",
		size, len(preallocated))

	fmt.Println()

	/*
	   SECTION 3: MAPS (Hash Maps)

	   Maps are Go's built-in hash table implementation.
	   Key characteristics:
	   - Key-value pairs
	   - Reference type
	   - Zero value is nil (cannot add to nil map)
	   - Keys must be comparable (no slices, maps, or functions)
	*/

	fmt.Println("=== 3. MAPS (Hash Maps) ===")

	// -----------------------------------------------------------------
	// Map declaration and initialization
	// -----------------------------------------------------------------
	fmt.Println("\n1. Map Declaration:")

	// Zero-valued map (nil, cannot add entries)
	var nilMap map[string]int
	fmt.Printf("   var nilMap map[string]int\t\t= %v (nil? %v)\n",
		nilMap, nilMap == nil)

	// Empty map (using make)
	emptyMap := make(map[string]int)
	fmt.Printf("   emptyMap := make(map[string]int)\t= %v\n", emptyMap)

	// Map literal
	scores := map[string]int{
		"Alice": 95,
		"Bob":   87,
		"Carol": 92,
	}
	fmt.Printf("   scores := map[string]int{...}\t= %v\n", scores)

	// With computed keys
	computedMap := map[string]int{
		strings.ToLower("ALICE"): 100,
		"bob" + "by":             200,
	}
	fmt.Printf("   computedMap = %v\n", computedMap)

	// -----------------------------------------------------------------
	// Map operations
	// -----------------------------------------------------------------
	fmt.Println("\n2. Map Operations:")

	// Insert/Update
	scores["David"] = 88
	scores["Alice"] = 96 // Update existing
	fmt.Printf("   After insert/update: %v\n", scores)

	// Retrieve value
	aliceScore := scores["Alice"]
	fmt.Printf("   scores[\"Alice\"] = %d\n", aliceScore)

	// Check if key exists (two-value assignment)
	score, exists := scores["Eve"]
	fmt.Printf("   scores[\"Eve\"] returns: score=%d, exists=%v\n", score, exists)

	// Delete key
	delete(scores, "Bob")
	fmt.Printf("   After delete(scores, \"Bob\"): %v\n", scores)

	// Length of map
	fmt.Printf("   len(scores) = %d\n", len(scores))

	// -----------------------------------------------------------------
	// Map iteration is non-deterministic!
	// -----------------------------------------------------------------
	fmt.Println("\n3. Map Iteration (Order is Randomized):")

	colors := map[string]string{
		"red":    "#FF0000",
		"green":  "#00FF00",
		"blue":   "#0000FF",
		"yellow": "#FFFF00",
	}

	fmt.Println("   Iteration 1:")
	for key, value := range colors {
		fmt.Printf("     %s: %s\n", key, value)
	}

	fmt.Println("\n   Iteration 2 (different order):")
	for key, value := range colors {
		fmt.Printf("     %s: %s\n", key, value)
	}

	// For deterministic order, sort keys
	fmt.Println("\n   Deterministic order (sorted keys):")
	keys := make([]string, 0, len(colors))
	for k := range colors {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, k := range keys {
		fmt.Printf("     %s: %s\n", k, colors[k])
	}

	// -----------------------------------------------------------------
	// Map as set (using bool or struct{} as value)
	// -----------------------------------------------------------------
	fmt.Println("\n4. Map as Set:")

	// Using bool (more memory)
	set1 := make(map[string]bool)
	set1["apple"] = true
	set1["banana"] = true
	set1["apple"] = true // Duplicate doesn't matter

	fmt.Printf("   set1 = %v\n", set1)
	fmt.Printf("   Contains \"apple\"? %v\n", set1["apple"])

	// Using struct{} (zero memory for value)
	set2 := make(map[string]struct{})
	set2["apple"] = struct{}{}
	set2["banana"] = struct{}{}

	fmt.Printf("   set2 keys: ")
	for k := range set2 {
		fmt.Printf("%s ", k)
	}
	fmt.Println()

	// Check membership
	_, hasApple := set2["apple"]
	fmt.Printf("   set2 contains \"apple\"? %v\n", hasApple)

	// -----------------------------------------------------------------
	// Nested maps
	// -----------------------------------------------------------------
	fmt.Println("\n5. Nested Maps:")

	students := map[string]map[string]float64{
		"Alice": {
			"Math":    95.5,
			"Science": 88.0,
		},
		"Bob": {
			"Math":    78.0,
			"Science": 92.5,
		},
	}

	fmt.Printf("   students[\"Alice\"][\"Math\"] = %.1f\n",
		students["Alice"]["Math"])

	// Safely access nested map
	if bobSubjects, exists := students["Bob"]; exists {
		if mathScore, exists := bobSubjects["Math"]; exists {
			fmt.Printf("   Bob's Math score: %.1f\n", mathScore)
		}
	}

	// -----------------------------------------------------------------
	// Map comparison and copying
	// -----------------------------------------------------------------
	fmt.Println("\n6. Map Comparison and Copying:")

	// Maps cannot be compared with == (except to nil)
	mapA := map[string]int{"a": 1, "b": 2}
	mapB := map[string]int{"a": 1, "b": 2}

	// fmt.Println(mapA == mapB) // Compile error!

	// To compare, need to write custom function
	fmt.Printf("   mapA equals mapB? %v\n", reflect.DeepEqual(mapA, mapB))

	// Copying maps (must copy each element)
	originalMap := map[string]int{"x": 1, "y": 2, "z": 3}
	copiedMap := make(map[string]int, len(originalMap))

	for k, v := range originalMap {
		copiedMap[k] = v
	}

	copiedMap["x"] = 99 // Modify copy
	fmt.Printf("   Original map: %v\n", originalMap)
	fmt.Printf("   Copied map:   %v (original unchanged)\n", copiedMap)

	fmt.Println()

	/*
	   SECTION 4: ITERATING WITH RANGE

	   The range keyword provides elegant iteration over collections.
	   Works with: arrays, slices, maps, strings, and channels.
	*/

	fmt.Println("=== 4. ITERATING WITH RANGE ===")

	// -----------------------------------------------------------------
	// Range over arrays and slices
	// -----------------------------------------------------------------
	fmt.Println("\n1. Range over Arrays/Slices:")

	items := []string{"apple", "banana", "cherry"}

	fmt.Println("   Index and value:")
	for i, item := range items {
		fmt.Printf("     [%d] = %s\n", i, item)
	}

	fmt.Println("\n   Value only (ignore index):")
	for _, item := range items {
		fmt.Printf("     %s\n", item)
	}

	fmt.Println("\n   Index only (ignore value):")
	for i := range items {
		fmt.Printf("     Index: %d\n", i)
	}

	// -----------------------------------------------------------------
	// Range over maps
	// -----------------------------------------------------------------
	fmt.Println("\n2. Range over Maps:")

	population := map[string]int{
		"China":  1410,
		"India":  1380,
		"USA":    331,
		"Brazil": 213,
	}

	fmt.Println("   Key and value:")
	for country, pop := range population {
		fmt.Printf("     %s: %d million\n", country, pop)
	}

	fmt.Println("\n   Key only:")
	for country := range population {
		fmt.Printf("     Country: %s\n", country)
	}

	// -----------------------------------------------------------------
	// Range over strings (iterates runes, not bytes)
	// -----------------------------------------------------------------
	fmt.Println("\n3. Range over Strings:")

	greeting := "Hello, 世界"

	fmt.Println("   By index (bytes):")
	for i := 0; i < len(greeting); i++ {
		fmt.Printf("     [%d] = %c (byte %d)\n", i, greeting[i], greeting[i])
	}

	fmt.Println("\n   By range (runes/Unicode code points):")
	for i, r := range greeting {
		fmt.Printf("     [%d] = %U = '%c'\n", i, r, r)
	}

	// -----------------------------------------------------------------
	// Range copies values (important for large structs)
	// -----------------------------------------------------------------
	fmt.Println("\n4. Range Copies Values:")

	people := []struct {
		Name string
		Age  int
	}{
		{"Alice", 30},
		{"Bob", 25},
		{"Carol", 35},
	}

	fmt.Println("   Original values:")
	for i, p := range people {
		// p is a COPY of the slice element
		p.Age += 10 // Doesn't modify original
		fmt.Printf("     [%d] %+v (copy modified)\n", i, p)
	}

	fmt.Println("\n   After range loop (original unchanged):")
	for i, p := range people {
		fmt.Printf("     [%d] %+v\n", i, p)
	}

	// To modify original, use index
	fmt.Println("\n   Modifying original via index:")
	for i := range people {
		people[i].Age += 10 // Actually modifies original
	}

	for i, p := range people {
		fmt.Printf("     [%d] %+v\n", i, p)
	}

	// -----------------------------------------------------------------
	// Practical range examples
	// -----------------------------------------------------------------
	fmt.Println("\n5. Practical Range Examples:")

	// Sum elements
	numsRange := []int{10, 20, 30, 40, 50}
	sum := 0
	for _, n := range numsRange {
		sum += n
	}
	fmt.Printf("   Sum of %v = %d\n", numsRange, sum)

	// Find maximum
	max := numsRange[0]
	for _, n := range numsRange[1:] {
		if n > max {
			max = n
		}
	}
	fmt.Printf("   Max of %v = %d\n", numsRange, max)

	// Count occurrences
	words := []string{"apple", "banana", "apple", "cherry", "banana", "apple"}
	wordCount := make(map[string]int)
	for _, word := range words {
		wordCount[word]++
	}
	fmt.Printf("   Word counts: %v\n", wordCount)

	fmt.Println()
	fmt.Println("=== END OF COLLECTIONS DEMONSTRATION ===")
}

/*
   KEY TAKEAWAYS:

   1. ARRAYS:
      - Fixed size, value type
      - Length part of type ([3]int ≠ [4]int)
      - Copying creates complete duplicate
      - Use when size is known and fixed at compile time

   2. SLICES (MOST IMPORTANT):
      - Dynamic size, reference to backing array
      - Three components: pointer, length, capacity
      - append() handles growth automatically
      - Slicing creates new slice sharing same backing array
      - Use copy() for actual duplication
      - Pre-allocate with make() when size known for performance

   3. MAPS:
      - Hash table implementation
      - Reference type, nil map cannot be written to
      - Keys must be comparable (no slices/maps/functions)
      - Two-value assignment checks existence
      - Iteration order is randomized (intentionally)
      - Use struct{} for sets to save memory

   4. RANGE LOOPS:
      - Clean iteration over collections
      - Returns (index, value) for slices/arrays
      - Returns (key, value) for maps
      - Returns (index, rune) for strings
      - Value is COPY (watch for large structs)
      - Use index to modify original elements

   PERFORMANCE NOTES:
   - Slices: Pre-allocate with make() when size known
   - Maps: Pre-allocate with make(map[K]V, size) when size known
   - append(): May cause allocations when capacity exceeded
   - copy(): Use for slice duplication, not assignment
   - range: Copies values, use index for modification

   COMMON PITFALLS:
   1. Modifying slice while ranging over it (can cause unexpected behavior)
   2. Assuming map iteration order
   3. Using == to compare maps (use reflect.DeepEqual or custom function)
   4. Forgetting that slice assignment creates reference, not copy
   5. Trying to add to nil map (must use make() first)
*/
