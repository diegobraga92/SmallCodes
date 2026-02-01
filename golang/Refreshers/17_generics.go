/*
GO GENERICS COMPREHENSIVE GUIDE (Go 1.18+)
This file demonstrates Go generics concepts with practical examples.
*/

package generics_examples

import (
	"context"
	"errors"
	"fmt"
	"log"
	"reflect"
	"sort"
	"strconv"
	"sync"
	"testing"
	"time"
)

// ============================================================================
// 1. TYPE PARAMETERS - Basic Syntax
// ============================================================================

// Generic function with type parameter T
func Identity[T any](value T) T {
	return value
}

// Multiple type parameters
func Pair[K, V any](key K, value V) (K, V) {
	return key, value
}

func TestBasicGenerics(t *testing.T) {
	// Type inference - compiler infers type from arguments
	intResult := Identity(42)
	if intResult != 42 {
		t.Errorf("Identity(42) = %v, want 42", intResult)
	}

	stringResult := Identity("hello")
	if stringResult != "hello" {
		t.Errorf(`Identity("hello") = %v, want "hello"`, stringResult)
	}

	// Explicit type specification (if needed)
	explicitResult := Identity[string]("world")
	if explicitResult != "world" {
		t.Errorf(`Identity[string]("world") = %v, want "world"`, explicitResult)
	}

	// Multiple type parameters
	key, value := Pair("name", "Alice")
	if key != "name" || value != "Alice" {
		t.Errorf("Pair returned (%v, %v), want (name, Alice)", key, value)
	}

	// Different types
	intKey, stringValue := Pair(123, "abc")
	if intKey != 123 || stringValue != "abc" {
		t.Errorf("Pair returned (%v, %v), want (123, abc)", intKey, stringValue)
	}
}

// ============================================================================
// 2. CONSTRAINTS - Restricting Type Parameters
// ============================================================================

// Before Go 1.18, we would use interfaces like fmt.Stringer
// Now we can use constraints

// Numeric constraint for types that support arithmetic
func Sum[T ~int | ~int8 | ~int16 | ~int32 | ~int64 | ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~float32 | ~float64](numbers []T) T {
	var total T
	for _, n := range numbers {
		total += n
	}
	return total
}

// Using predeclared constraints from "golang.org/x/exp/constraints"
// import "golang.org/x/exp/constraints"

// func Sum2[T constraints.Integer | constraints.Float](numbers []T) T {
//     var total T
//     for _, n := range numbers {
//         total += n
//     }
//     return total
// }

// Custom constraint
type Stringable interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 | ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~float32 | ~float64 | ~string
}

func ConvertToString[T Stringable](value T) string {
	return fmt.Sprintf("%v", value)
}

// Constraint with methods
type Processor[T any] interface {
	Process(input T) T
	Validate(input T) error
}

func RunPipeline[T any, P Processor[T]](processor P, inputs []T) ([]T, error) {
	results := make([]T, 0, len(inputs))
	for _, input := range inputs {
		if err := processor.Validate(input); err != nil {
			return nil, err
		}
		results = append(results, processor.Process(input))
	}
	return results, nil
}

// ============================================================================
// 3. COMPARABLE TYPES - Types that support == and !=
// ============================================================================

// Comparable constraint is built-in
func FindIndex[T comparable](slice []T, value T) int {
	for i, v := range slice {
		if v == value {
			return i
		}
	}
	return -1
}

// Using comparable for map keys
func CountOccurrences[T comparable](items []T) map[T]int {
	counts := make(map[T]int)
	for _, item := range items {
		counts[item]++
	}
	return counts
}

func RemoveDuplicates[T comparable](slice []T) []T {
	seen := make(map[T]bool)
	result := make([]T, 0, len(slice))

	for _, item := range slice {
		if !seen[item] {
			seen[item] = true
			result = append(result, item)
		}
	}
	return result
}

func TestComparableTypes(t *testing.T) {
	// Works with any comparable type
	intIndex := FindIndex([]int{1, 2, 3, 4, 5}, 3)
	if intIndex != 2 {
		t.Errorf("FindIndex([]int{1,2,3,4,5}, 3) = %d, want 2", intIndex)
	}

	stringIndex := FindIndex([]string{"a", "b", "c"}, "b")
	if stringIndex != 1 {
		t.Errorf(`FindIndex([]string{"a","b","c"}, "b") = %d, want 1`, stringIndex)
	}

	// Count occurrences
	occurrences := CountOccurrences([]int{1, 2, 2, 3, 3, 3})
	if occurrences[2] != 2 || occurrences[3] != 3 {
		t.Errorf("CountOccurrences failed: %v", occurrences)
	}

	// Remove duplicates
	unique := RemoveDuplicates([]int{1, 2, 2, 3, 3, 3, 4})
	if len(unique) != 4 {
		t.Errorf("RemoveDuplicates failed: got %v", unique)
	}
}

// Complex example with structs (structs are comparable if all fields are comparable)
type Person struct {
	Name string
	Age  int
}

func TestComparableStructs(t *testing.T) {
	people := []Person{
		{"Alice", 30},
		{"Bob", 25},
		{"Alice", 30}, // Duplicate
		{"Charlie", 35},
	}

	uniquePeople := RemoveDuplicates(people)
	if len(uniquePeople) != 3 { // Should remove duplicate Alice
		t.Errorf("Expected 3 unique people, got %d", len(uniquePeople))
	}

	// Find person
	index := FindIndex(people, Person{"Bob", 25})
	if index != 1 {
		t.Errorf("FindIndex for Bob = %d, want 1", index)
	}
}

// ============================================================================
// 4. GENERIC FUNCTIONS
// ============================================================================

// Map function: applies function to each element
func Map[T, U any](slice []T, f func(T) U) []U {
	result := make([]U, len(slice))
	for i, v := range slice {
		result[i] = f(v)
	}
	return result
}

// Filter function: filters elements based on predicate
func Filter[T any](slice []T, f func(T) bool) []T {
	result := make([]T, 0, len(slice))
	for _, v := range slice {
		if f(v) {
			result = append(result, v)
		}
	}
	return result
}

// Reduce function: reduces slice to single value
func Reduce[T, U any](slice []T, initial U, f func(U, T) U) U {
	result := initial
	for _, v := range slice {
		result = f(result, v)
	}
	return result
}

// Contains function: checks if element exists
func Contains[T comparable](slice []T, value T) bool {
	for _, v := range slice {
		if v == value {
			return true
		}
	}
	return false
}

// Max function: finds maximum value (requires Ordered constraint)
func Max[T ~int | ~int8 | ~int16 | ~int32 | ~int64 | ~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 | ~float32 | ~float64](a, b T) T {
	if a > b {
		return a
	}
	return b
}

// Optional type (like Maybe/Option in other languages)
type Optional[T any] struct {
	value *T
}

func (o Optional[T]) IsPresent() bool {
	return o.value != nil
}

func (o Optional[T]) Get() (T, error) {
	if o.value == nil {
		var zero T
		return zero, errors.New("no value present")
	}
	return *o.value, nil
}

func (o Optional[T]) OrElse(defaultValue T) T {
	if o.value == nil {
		return defaultValue
	}
	return *o.value
}

func Some[T any](value T) Optional[T] {
	return Optional[T]{value: &value}
}

func None[T any]() Optional[T] {
	return Optional[T]{value: nil}
}

func TestGenericFunctions(t *testing.T) {
	// Map
	numbers := []int{1, 2, 3, 4, 5}
	squared := Map(numbers, func(x int) int { return x * x })
	expectedSquared := []int{1, 4, 9, 16, 25}
	if !equal(squared, expectedSquared) {
		t.Errorf("Map failed: got %v, want %v", squared, expectedSquared)
	}

	// Map with type conversion
	strings := Map(numbers, func(x int) string { return strconv.Itoa(x) })
	expectedStrings := []string{"1", "2", "3", "4", "5"}
	if !equal(strings, expectedStrings) {
		t.Errorf("Map (type conversion) failed: got %v, want %v", strings, expectedStrings)
	}

	// Filter
	evens := Filter(numbers, func(x int) bool { return x%2 == 0 })
	expectedEvens := []int{2, 4}
	if !equal(evens, expectedEvens) {
		t.Errorf("Filter failed: got %v, want %v", evens, expectedEvens)
	}

	// Reduce
	sum := Reduce(numbers, 0, func(acc, x int) int { return acc + x })
	if sum != 15 {
		t.Errorf("Reduce failed: got %d, want 15", sum)
	}

	// Contains
	if !Contains(numbers, 3) {
		t.Error("Contains failed: should contain 3")
	}
	if Contains(numbers, 10) {
		t.Error("Contains failed: should not contain 10")
	}

	// Max
	if Max(10, 20) != 20 {
		t.Error("Max failed")
	}

	// Optional
	opt := Some(42)
	if !opt.IsPresent() {
		t.Error("Optional should be present")
	}
	value, err := opt.Get()
	if err != nil || value != 42 {
		t.Errorf("Optional.Get failed: %v, %v", value, err)
	}

	none := None[int]()
	if none.IsPresent() {
		t.Error("Optional should not be present")
	}
	if none.OrElse(100) != 100 {
		t.Error("Optional.OrElse failed")
	}
}

// Helper function for comparing slices
func equal[T comparable](a, b []T) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// ============================================================================
// 5. GENERIC DATA STRUCTURES
// ============================================================================

// Generic Stack
type Stack[T any] struct {
	items []T
}

func NewStack[T any]() *Stack[T] {
	return &Stack[T]{items: make([]T, 0)}
}

func (s *Stack[T]) Push(item T) {
	s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
	if len(s.items) == 0 {
		var zero T
		return zero, false
	}
	item := s.items[len(s.items)-1]
	s.items = s.items[:len(s.items)-1]
	return item, true
}

func (s *Stack[T]) Peek() (T, bool) {
	if len(s.items) == 0 {
		var zero T
		return zero, false
	}
	return s.items[len(s.items)-1], true
}

func (s *Stack[T]) Size() int {
	return len(s.items)
}

func (s *Stack[T]) IsEmpty() bool {
	return len(s.items) == 0
}

// Generic LinkedList Node
type Node[T any] struct {
	Value T
	Next  *Node[T]
}

type LinkedList[T any] struct {
	Head *Node[T]
}

func NewLinkedList[T any]() *LinkedList[T] {
	return &LinkedList[T]{}
}

func (l *LinkedList[T]) Append(value T) {
	newNode := &Node[T]{Value: value}
	if l.Head == nil {
		l.Head = newNode
		return
	}

	current := l.Head
	for current.Next != nil {
		current = current.Next
	}
	current.Next = newNode
}

func (l *LinkedList[T]) ToSlice() []T {
	var result []T
	current := l.Head
	for current != nil {
		result = append(result, current.Value)
		current = current.Next
	}
	return result
}

// Generic Binary Tree
type TreeNode[T any] struct {
	Value T
	Left  *TreeNode[T]
	Right *TreeNode[T]
}

type BinaryTree[T any] struct {
	Root *TreeNode[T]
}

func (t *BinaryTree[T]) InOrder() []T {
	var result []T
	t.inOrder(t.Root, &result)
	return result
}

func (t *BinaryTree[T]) inOrder(node *TreeNode[T], result *[]T) {
	if node == nil {
		return
	}
	t.inOrder(node.Left, result)
	*result = append(*result, node.Value)
	t.inOrder(node.Right, result)
}

// Generic Cache with expiration
type Cache[K comparable, V any] struct {
	data     map[K]cacheEntry[V]
	capacity int
	mu       sync.RWMutex
}

type cacheEntry[V any] struct {
	value      V
	expiration time.Time
}

func NewCache[K comparable, V any](capacity int) *Cache[K, V] {
	return &Cache[K, V]{
		data:     make(map[K]cacheEntry[V]),
		capacity: capacity,
	}
}

func (c *Cache[K, V]) Set(key K, value V, ttl time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()

	// Evict if at capacity
	if len(c.data) >= c.capacity && len(c.data) > 0 {
		// Simple eviction: remove first key (could implement LRU)
		for k := range c.data {
			delete(c.data, k)
			break
		}
	}

	c.data[key] = cacheEntry[V]{
		value:      value,
		expiration: time.Now().Add(ttl),
	}
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
	c.mu.RLock()
	entry, found := c.data[key]
	c.mu.RUnlock()

	if !found {
		var zero V
		return zero, false
	}

	// Check expiration
	if time.Now().After(entry.expiration) {
		c.mu.Lock()
		delete(c.data, key)
		c.mu.Unlock()
		var zero V
		return zero, false
	}

	return entry.value, true
}

func TestGenericDataStructures(t *testing.T) {
	// Test Stack
	stack := NewStack[int]()
	stack.Push(1)
	stack.Push(2)
	stack.Push(3)

	if stack.Size() != 3 {
		t.Errorf("Stack size = %d, want 3", stack.Size())
	}

	top, ok := stack.Peek()
	if !ok || top != 3 {
		t.Errorf("Stack.Peek = %d, want 3", top)
	}

	popped, ok := stack.Pop()
	if !ok || popped != 3 {
		t.Errorf("Stack.Pop = %d, want 3", popped)
	}

	// Test LinkedList
	list := NewLinkedList[string]()
	list.Append("a")
	list.Append("b")
	list.Append("c")

	slice := list.ToSlice()
	expected := []string{"a", "b", "c"}
	if !equal(slice, expected) {
		t.Errorf("LinkedList.ToSlice = %v, want %v", slice, expected)
	}

	// Test Cache
	cache := NewCache[string, int](2)
	cache.Set("a", 1, time.Minute)
	cache.Set("b", 2, time.Minute)

	val, found := cache.Get("a")
	if !found || val != 1 {
		t.Errorf("Cache.Get('a') = %d, want 1", val)
	}

	// Should evict when capacity exceeded
	cache.Set("c", 3, time.Minute)
	_, found = cache.Get("a")
	if found {
		t.Error("Cache should have evicted 'a'")
	}
}

// ============================================================================
// 6. GENERIC METHODS ON STRUCTS
// ============================================================================

// Generic receiver methods (cannot have additional type parameters)
type Container[T any] struct {
	items []T
}

func (c *Container[T]) Add(item T) {
	c.items = append(c.items, item)
}

func (c *Container[T]) Get(index int) T {
	return c.items[index]
}

func (c *Container[T]) Map(f func(T) T) *Container[T] {
	result := &Container[T]{items: make([]T, len(c.items))}
	for i, item := range c.items {
		result.items[i] = f(item)
	}
	return result
}

// Note: You can't define new type parameters on methods
// WRONG: func (c *Container) Transform[U any](f func(T) U) *Container[U]
// This must be a regular function:

func Transform[T, U any](c *Container[T], f func(T) U) *Container[U] {
	result := &Container[U]{items: make([]U, len(c.items))}
	for i, item := range c.items {
		result.items[i] = f(item)
	}
	return result
}

// ============================================================================
// 7. GENERIC INTERFACES
// ============================================================================

// Generic interface
type Repository[T any] interface {
	Get(id string) (T, error)
	Save(entity T) error
	Delete(id string) error
	List() ([]T, error)
}

// Generic interface with type constraint
type NumericRepository[T ~int | ~float64] interface {
	GetSum() T
	GetAverage() T
	Add(value T)
}

// Implementing generic interface with concrete type
type UserRepository struct {
	users map[string]User
}

func (r *UserRepository) Get(id string) (User, error) {
	user, ok := r.users[id]
	if !ok {
		return User{}, errors.New("not found")
	}
	return user, nil
}

func (r *UserRepository) Save(user User) error {
	r.users[user.ID] = user
	return nil
}

func (r *UserRepository) Delete(id string) error {
	delete(r.users, id)
	return nil
}

func (r *UserRepository) List() ([]User, error) {
	users := make([]User, 0, len(r.users))
	for _, user := range r.users {
		users = append(users, user)
	}
	return users, nil
}

// Generic service using generic interface
type Service[T any] struct {
	repo Repository[T]
}

func (s *Service[T]) ProcessAll() error {
	items, err := s.repo.List()
	if err != nil {
		return err
	}

	// Process items...
	for _, item := range items {
		_ = item // Process each item
	}
	return nil
}

// ============================================================================
// 8. TYPE SETS AND INTERFACE CONSTRAINTS
// ============================================================================

// Type sets in interfaces (Go 1.18+)
type Number interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
		~float32 | ~float64
}

// Interface with both type set and methods
type OrderedNumber interface {
	Number
	comparable
}

// Complex constraint example
type Processable interface {
	~int | ~string
	Process() string
}

// Cannot mix type sets and methods on the same type parameter
// This is a compile-time error:
// func ProcessItems[T Processable](items []T) {}
// Because the underlying type int/string doesn't have Process() method

// Correct approach: separate constraints
type Processor2[T any] interface {
	Process() T
}

func ProcessItems[T any, P Processor2[T]](items []P) []T {
	result := make([]T, len(items))
	for i, item := range items {
		result[i] = item.Process()
	}
	return result
}

// ============================================================================
// 9. REAL-WORLD EXAMPLES
// ============================================================================

// Database Pagination
type PaginatedResponse[T any] struct {
	Data       []T `json:"data"`
	Page       int `json:"page"`
	PageSize   int `json:"page_size"`
	TotalCount int `json:"total_count"`
	TotalPages int `json:"total_pages"`
}

func Paginate[T any](items []T, page, pageSize int) PaginatedResponse[T] {
	if page < 1 {
		page = 1
	}
	if pageSize < 1 {
		pageSize = 10
	}

	start := (page - 1) * pageSize
	end := start + pageSize

	if start > len(items) {
		start = len(items)
	}
	if end > len(items) {
		end = len(items)
	}

	return PaginatedResponse[T]{
		Data:       items[start:end],
		Page:       page,
		PageSize:   pageSize,
		TotalCount: len(items),
		TotalPages: (len(items) + pageSize - 1) / pageSize,
	}
}

// API Response Wrapper
type APIResponse[T any] struct {
	Success bool   `json:"success"`
	Message string `json:"message,omitempty"`
	Data    T      `json:"data,omitempty"`
	Error   string `json:"error,omitempty"`
}

func SuccessResponse[T any](data T) APIResponse[T] {
	return APIResponse[T]{
		Success: true,
		Data:    data,
	}
}

func ErrorResponse[T any](message string) APIResponse[T] {
	return APIResponse[T]{
		Success: false,
		Error:   message,
	}
}

// Sort with custom comparator
func SortBy[T any](slice []T, less func(a, b T) bool) {
	sort.Slice(slice, func(i, j int) bool {
		return less(slice[i], slice[j])
	})
}

// Concurrent Map Access Pattern
type ConcurrentMap[K comparable, V any] struct {
	data map[K]V
	mu   sync.RWMutex
}

func (m *ConcurrentMap[K, V]) Update(key K, updater func(V) V) {
	m.mu.Lock()
	defer m.mu.Unlock()

	current := m.data[key]
	m.data[key] = updater(current)
}

// ============================================================================
// 10. ADVANCED PATTERNS AND TRICKS
// ============================================================================

// Type switching with generics (limited - you can't type switch on T)
func TypeName[T any](value T) string {
	switch any(value).(type) {
	case int:
		return "int"
	case string:
		return "string"
	case bool:
		return "bool"
	default:
		return "unknown"
	}
}

// Generic constructor pattern
func NewWithOptions[T any](options ...func(*T)) *T {
	var item T
	for _, option := range options {
		option(&item)
	}
	return &item
}

// Using ~ for underlying types
type ID string
type UserID ID
type ProductID ID

func ValidateID[T ~string](id T) bool {
	return len(id) > 0
}

// Generic middleware pattern
type Handler[T any] func(ctx context.Context, req T) (interface{}, error)

func Middleware[T any](next Handler[T]) Handler[T] {
	return func(ctx context.Context, req T) (interface{}, error) {
		// Pre-processing
		log.Printf("Processing request: %v", req)

		// Call next handler
		resp, err := next(ctx, req)

		// Post-processing
		if err != nil {
			log.Printf("Handler error: %v", err)
		}

		return resp, err
	}
}

// ============================================================================
// 11. WHEN NOT TO USE GENERICS
// ============================================================================

// 1. When interface{} (any) is sufficient and simpler
// Bad: Overly generic for simple case
func BadGenericPrint[T any](value T) {
	fmt.Println(value)
}

// Good: Use any if you just need to accept any type
func GoodPrint(value any) {
	fmt.Println(value)
}

// 2. When performance is critical and type-specific implementation is faster
// Bad: Generic numeric function that boxes values
func BadGenericAdd[T ~int | ~float64](a, b T) T {
	return a + b
}

// Good: Multiple specific functions (no boxing, inlining possible)
func AddInt(a, b int) int {
	return a + b
}

func AddFloat(a, b float64) float64 {
	return a + b
}

// 3. When code becomes harder to read
// Bad: Deeply nested generics with complex constraints
type BadComplexGeneric[A any, B comparable, C ~int | ~string] struct {
	field1 A
	field2 map[B]C
}

// 4. When you need runtime type information
// Generics don't provide runtime type information
func BadRuntimeType[T any]() string {
	// Can't get type name at runtime
	return "unknown"
}

// 5. When working with reflection
// Reflection with generics is more complex
func BadReflection[T any](value T) {
	// Type information is lost
	_ = reflect.TypeOf(value)
}

// 6. When implementing io.Reader/Writer patterns
// These are better with concrete types or interfaces

// ============================================================================
// 12. COMMON PITFALLS AND SOLUTIONS
// ============================================================================

// Pitfall 1: Cannot use generic type in method signatures
type Processor3[T any] struct{}

// WRONG: Can't have method with its own type parameter
// func (p *Processor3[T]) Process[U any](input U) U { return input }

// Solution: Make it a regular function
func ProcessGeneric[T, U any](p *Processor3[T], input U) U {
	return input
}

// Pitfall 2: Type inference fails with nested calls
func Wrap[T any](value T) T {
	return value
}

func TestTypeInferencePitfall(t *testing.T) {
	// This works:
	result1 := Wrap(42)
	_ = result1

	// This might not infer correctly:
	// result2 := Wrap(Wrap(42)) // Go 1.18 had issues with this

	// Solution: Be explicit
	result2 := Wrap[int](Wrap(42))
	_ = result2
}

// Pitfall 3: Generic methods on non-generic types
type NonGeneric struct{}

// WRONG: Can't add type parameters to methods
// func (n NonGeneric) GenericMethod[T any](value T) T { return value }

// Solution: Use a function
func GenericMethod[T any](n NonGeneric, value T) T {
	return value
}

// Pitfall 4: Cannot instantiate with non-comparable types
type NonComparable struct {
	Data []int
}

func TestNonComparable(t *testing.T) {
	// This won't compile because NonComparable contains a slice
	// index := FindIndex([]NonComparable{{}}, NonComparable{})

	// Solution: Use a custom comparison function
	items := []NonComparable{{Data: []int{1, 2}}}
	findIndexWithFunc(items, func(item NonComparable) bool {
		return len(item.Data) == 2
	})
}

func findIndexWithFunc[T any](slice []T, predicate func(T) bool) int {
	for i, v := range slice {
		if predicate(v) {
			return i
		}
	}
	return -1
}

// ============================================================================
// 13. BEST PRACTICES
// ============================================================================

/*
1. Start without generics - add them when you need type safety for multiple types
2. Use descriptive type parameter names (T for any type, K/V for key/value, E for element)
3. Keep constraints minimal - use `any` when you don't need operations
4. Consider performance - generics may not inline as well as concrete functions
5. Write comprehensive tests for generic functions with different types
6. Document constraints and expectations
7. Avoid deeply nested generics - they hurt readability
8. Use type aliases (~) for underlying type constraints
9. Prefer interfaces over generics for behavior abstraction
10. Remember: Generics are compile-time - no runtime type information
*/

// ============================================================================
// 14. PERFORMANCE CONSIDERATIONS
// ============================================================================

// Generic functions are monomorphized at compile time
// Each unique type instantiation creates a new function

func BenchmarkGenericVsConcrete(b *testing.B) {
	ints := make([]int, 1000)
	floats := make([]float64, 1000)

	// Benchmark generic function
	b.Run("Generic", func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			_ = Sum(ints)
			_ = Sum(floats)
		}
	})

	// Benchmark concrete functions
	b.Run("Concrete", func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			_ = sumInts(ints)
			_ = sumFloats(floats)
		}
	})
}

func sumInts(nums []int) int {
	var total int
	for _, n := range nums {
		total += n
	}
	return total
}

func sumFloats(nums []float64) float64 {
	var total float64
	for _, n := range nums {
		total += n
	}
	return total
}

// ============================================================================
// 15. TESTING GENERIC CODE
// ============================================================================

// Test helper for generic functions
func testSum[T ~int | ~float64](t *testing.T) {
	tests := []struct {
		name     string
		input    []T
		expected T
	}{
		{"empty", []T{}, 0},
		{"single", []T{5}, 5},
		{"multiple", []T{1, 2, 3, 4}, 10},
		{"negative", []T{-1, -2, -3}, -6},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Sum(tt.input)
			if result != tt.expected {
				t.Errorf("Sum(%v) = %v, want %v", tt.input, result, tt.expected)
			}
		})
	}
}

func TestSumInt(t *testing.T) {
	testSum[int](t)
}

func TestSumFloat64(t *testing.T) {
	testSum[float64](t)
}

// ============================================================================
// 16. REAL-WORLD USE CASES WHERE GENERICS EXCEL
// ============================================================================

// 1. Collection utilities (Map, Filter, Reduce)
// 2. Data structures (Stack, Queue, Tree, Cache)
// 3. Repository pattern with different entity types
// 4. API response wrappers
// 5. Math/statistics libraries
// 6. Validation libraries
// 7. Configuration loading
// 8. Pipeline/processing patterns

// Example: Generic validation
type Validator[T any] interface {
	Validate(value T) error
}

type StringValidator struct {
	MinLength int
	MaxLength int
}

func (v StringValidator) Validate(value string) error {
	if len(value) < v.MinLength {
		return fmt.Errorf("too short: min %d", v.MinLength)
	}
	if len(value) > v.MaxLength {
		return fmt.Errorf("too long: max %d", v.MaxLength)
	}
	return nil
}

func ValidateAll[T any](value T, validators ...Validator[T]) error {
	for _, validator := range validators {
		if err := validator.Validate(value); err != nil {
			return err
		}
	}
	return nil
}
