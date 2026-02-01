// ============================================
// GO INTERFACES & COMPOSITION - COMPREHENSIVE GUIDE
// ============================================

package main

import (
	"fmt"
	"reflect"
)

// ============================================
// 1. INTERFACES AS CONTRACTS
// ============================================

// Interfaces define behavior contracts - they specify WHAT an object can do,
// not HOW it does it. This enables polymorphism and loose coupling.

// Writer interface defines a contract for writing data
type Writer interface {
	Write([]byte) (int, error)
}

// Reader interface defines a contract for reading data
type Reader interface {
	Read([]byte) (int, error)
}

// ReadWriter interface composes two interfaces (more on composition later)
type ReadWriter interface {
	Reader
	Writer
}

// ============================================
// 2. IMPLICIT INTERFACE IMPLEMENTATION
// ============================================

// In Go, interfaces are implemented implicitly. A type implements an interface
// simply by having methods with matching signatures. No explicit declaration needed.

// File implements Writer implicitly by having Write method
type File struct {
	name string
}

func (f File) Write(data []byte) (int, error) {
	fmt.Printf("Writing %d bytes to file: %s\n", len(data), f.name)
	return len(data), nil
}

// MemoryBuffer also implements Writer implicitly
type MemoryBuffer struct {
	buffer []byte
}

func (m *MemoryBuffer) Write(data []byte) (int, error) {
	m.buffer = append(m.buffer, data...)
	return len(data), nil
}

// This demonstrates the power of implicit implementation - both File and
// MemoryBuffer satisfy the Writer interface without declaring it explicitly.

// ============================================
// 3. INTERFACE SATISFACTION
// ============================================

// A type satisfies an interface if it implements ALL methods in the interface.
// Interface satisfaction is checked at compile time.

type Closer interface {
	Close() error
}

type ReadCloser interface {
	Reader
	Closer
}

// NetworkConnection satisfies ReadCloser by implementing both Read and Close
type NetworkConnection struct {
	open bool
}

func (nc *NetworkConnection) Read(data []byte) (int, error) {
	if !nc.open {
		return 0, fmt.Errorf("connection closed")
	}
	// Simulate reading
	return copy(data, []byte("data")), nil
}

func (nc *NetworkConnection) Close() error {
	nc.open = false
	return nil
}

// ============================================
// 4. INTERFACE VS CONCRETE TYPES
// ============================================

// Concrete types define both data representation AND behavior
// Interfaces define ONLY behavior

// Concrete type with specific implementation
type ConcreteLogger struct {
	prefix string
}

func (cl ConcreteLogger) Log(msg string) {
	fmt.Printf("[%s] %s\n", cl.prefix, msg)
}

// Interface for logging abstraction
type Logger interface {
	Log(string)
}

// Function accepting interface - more flexible
func logMessage(logger Logger, msg string) {
	logger.Log(msg)
}

// Function accepting concrete type - less flexible
func logWithConcrete(logger ConcreteLogger, msg string) {
	logger.Log(msg)
}

// ============================================
// 5. EMPTY INTERFACE (interface{}) vs any
// ============================================

// Empty interface accepts any type (since all types implement at least zero methods)
// 'any' is a type alias for interface{} (introduced in Go 1.18)

func processValue(v interface{}) {
	fmt.Printf("Value: %v, Type: %T\n", v, v)
}

func processAny(v any) {
	fmt.Printf("Value: %v, Type: %T\n", v, v)
}

// Type switches with empty interface
func describe(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Integer: %d\n", v)
	case string:
		fmt.Printf("String: %s\n", v)
	default:
		fmt.Printf("Unknown type: %T\n", v)
	}
}

// ============================================
// 6. TYPE ASSERTIONS
// ============================================

// Type assertions provide access to an interface value's underlying concrete value

func processWriter(w Writer) {
	// Safe type assertion with ok idiom
	if file, ok := w.(File); ok {
		fmt.Printf("Underlying type is File: %s\n", file.name)
	} else if buf, ok := w.(*MemoryBuffer); ok {
		fmt.Printf("Underlying type is *MemoryBuffer, length: %d\n", len(buf.buffer))
	} else {
		fmt.Println("Unknown Writer implementation")
	}

	// Panic if assertion fails (unsafe - use with caution or when certain)
	// file := w.(File) // Would panic if w is not File
}

// Type assertion with switch
func printType(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Println("Integer:", v)
	case string:
		fmt.Println("String:", v)
	case Writer:
		fmt.Println("Writer interface")
		v.Write([]byte("test"))
	default:
		fmt.Println("Unknown type")
	}
}

// ============================================
// 7. COMPOSITION VS INHERITANCE
// ============================================

// Go favors composition over inheritance (which doesn't exist in Go).
// Composition: Building complex types by combining simpler types.

// Base structs
type Person struct {
	Name string
	Age  int
}

func (p Person) Introduce() {
	fmt.Printf("Hi, I'm %s, %d years old\n", p.Name, p.Age)
}

type Employee struct {
	Person  // Embedded struct (composition)
	Company string
	Salary  float64
}

// Employee automatically gets Person's methods (promoted methods)
// This is NOT inheritance - it's embedding/composition

// Interface composition
type Worker interface {
	Work() string
}

type Eater interface {
	Eat() string
}

type WorkerEater interface {
	Worker
	Eater
}

type Chef struct{}

func (c Chef) Work() string { return "Cooking..." }
func (c Chef) Eat() string  { return "Tasting food..." }

// ============================================
// 8. EMBEDDING STRUCTS AND INTERFACES
// ============================================

// Embedding enables type composition and method promotion

// Base struct
type Address struct {
	Street  string
	City    string
	Country string
}

func (a Address) FullAddress() string {
	return fmt.Sprintf("%s, %s, %s", a.Street, a.City, a.Country)
}

// Embedding struct
type Customer struct {
	ID      string
	Address // Embedded - methods are promoted
}

// Customer now has access to Address fields and methods directly
// customer.Street instead of customer.Address.Street
// customer.FullAddress() instead of customer.Address.FullAddress()

// Embedding interface
type ReadSeeker interface {
	Reader
	Seek(offset int64, whence int) (int64, error)
}

// BufferedReadSeeker embeds ReadSeeker interface
// This means any type that implements ReadSeeker can be assigned to BufferedReadSeeker
type BufferedReadSeeker struct {
	ReadSeeker // Embedded interface
	buffer     []byte
}

// ============================================
// ADVANCED PATTERNS AND BEST PRACTICES
// ============================================

// 1. Interface Segregation Principle
// Prefer smaller, focused interfaces over large ones

type WriterOnly interface {
	Write([]byte) (int, error)
}

type ReaderOnly interface {
	Read([]byte) (int, error)
}

// Instead of one large ReadWriteCloser interface for all scenarios

// 2. Accept interfaces, return concrete types
func NewFileWriter(name string) *File {
	return &File{name: name}
}

// 3. Interface guards (compile-time verification)
var _ Writer = (*File)(nil)         // Verify File implements Writer
var _ Writer = (*MemoryBuffer)(nil) // Verify MemoryBuffer implements Writer

// 4. Functional options pattern with interfaces
type ServerOption interface {
	apply(*Server)
}

type Server struct {
	host string
	port int
}

// 5. Runtime interface inspection
func inspectInterface(i interface{}) {
	v := reflect.ValueOf(i)
	t := v.Type()

	fmt.Printf("Interface has %d methods:\n", t.NumMethod())
	for i := 0; i < t.NumMethod(); i++ {
		method := t.Method(i)
		fmt.Printf("  %s\n", method.Name)
	}
}

// ============================================
// PRACTICAL EXAMPLE: PLUGIN ARCHITECTURE
// ============================================

// Plugin interface for extensible architecture
type Plugin interface {
	Name() string
	Initialize() error
	Execute(params map[string]interface{}) (interface{}, error)
	Cleanup() error
}

// PluginManager uses composition to manage plugins
type PluginManager struct {
	plugins map[string]Plugin
}

func (pm *PluginManager) Register(p Plugin) {
	pm.plugins[p.Name()] = p
}

func (pm *PluginManager) ExecutePlugin(name string, params map[string]interface{}) (interface{}, error) {
	if plugin, exists := pm.plugins[name]; exists {
		return plugin.Execute(params)
	}
	return nil, fmt.Errorf("plugin %s not found", name)
}

// ============================================
// MAIN FUNCTION - DEMONSTRATION
// ============================================

func main() {
	fmt.Println("=== Interfaces & Composition Demo ===\n")

	// 1. Interface as contract
	fmt.Println("1. Interface as Contract:")
	file := File{name: "data.txt"}
	var writer Writer = file
	writer.Write([]byte("Hello"))

	// 2. Implicit implementation
	fmt.Println("\n2. Implicit Implementation:")
	buffer := &MemoryBuffer{}
	writer = buffer
	writer.Write([]byte("World"))

	// 3. Type assertions
	fmt.Println("\n3. Type Assertions:")
	processWriter(file)
	processWriter(buffer)

	// 4. Empty interface
	fmt.Println("\n4. Empty Interface:")
	processValue(42)
	processValue("hello")
	processAny(3.14)
	describe(123)
	describe("test")

	// 5. Composition
	fmt.Println("\n5. Composition vs Inheritance:")
	emp := Employee{
		Person:  Person{Name: "John", Age: 30},
		Company: "TechCorp",
		Salary:  50000,
	}
	emp.Introduce() // Promoted method from Person
	fmt.Printf("Works at: %s\n", emp.Company)

	// 6. Embedding
	fmt.Println("\n6. Struct Embedding:")
	customer := Customer{
		ID: "C001",
		Address: Address{
			Street:  "123 Main St",
			City:    "Boston",
			Country: "USA",
		},
	}
	fmt.Printf("Customer address: %s\n", customer.FullAddress()) // Promoted method
	fmt.Printf("Street: %s\n", customer.Street)                  // Promoted field

	// 7. Interface composition
	fmt.Println("\n7. Interface Composition:")
	var we WorkerEater = Chef{}
	fmt.Println("Work:", we.Work())
	fmt.Println("Eat:", we.Eat())

	// 8. Plugin architecture example
	fmt.Println("\n8. Plugin Architecture Example:")
	pm := &PluginManager{plugins: make(map[string]Plugin)}
	// In real scenario, register actual plugins
	fmt.Printf("Plugin manager initialized with %d plugins\n", len(pm.plugins))

	fmt.Println("\n=== End Demo ===")
}

// ============================================
// KEY TAKEAWAYS FOR DEVELOPERS:
// ============================================

// JUNIOR DEVELOPERS:
// 1. Interfaces define WHAT a type can do (methods)
// 2. Types implement interfaces implicitly
// 3. Use empty interface (interface{}) for generic functions
// 4. Prefer composition with embedding over complex hierarchies

// MID-LEVEL DEVELOPERS:
// 1. Design small, focused interfaces (ISP)
// 2. Accept interfaces, return concrete types
// 3. Understand interface nil values (interface can be nil, or can hold nil concrete value)
// 4. Use type switches for type-specific behavior

// SENIOR DEVELOPERS:
// 1. Design interfaces for testability and dependency injection
// 2. Use interface composition for complex behaviors
// 3. Consider performance implications of interface method calls
// 4. Implement compile-time checks with interface guards
// 5. Design for extensibility through interface-based plugins
// 6. Understand interface internals (itab, data pointer)

// COMMON PITFALLS:
// 1. Overusing empty interface (loses type safety)
// 2. Creating overly large interfaces
// 3. Forgetting that interface values can be nil
// 4. Confusing embedding with inheritance
// 5. Not handling type assertion failures properly
