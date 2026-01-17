/*
   Comprehensive Go Example with Detailed Comments
   This file demonstrates fundamental Go concepts and language philosophy.

   Author: Go Developer
   Date: 2024
*/

// Package declaration: Every Go file starts with a package declaration.
// 'main' is a special package that creates an executable application.
package main

/*
   GO PHILOSOPHY & DESIGN GOALS (Demonstrated throughout this example):

   1. SIMPLICITY:
       - Minimal keywords (only 25)
       - No classes, inheritance, or generics (until recently, used sparingly)
       - Single binary output
       - Garbage collected but with value types for performance

   2. COMPOSITION OVER INHERITANCE:
       - Uses struct embedding instead of class inheritance
       - Interface implementation is implicit (duck typing)
       - Encourages small, focused types composed together

   3. CONCURRENCY AS FIRST-CLASS CITIZEN:
       - Built-in goroutines (lightweight threads)
       - Channels for communication between goroutines
       - select statement for multiplexing
       - "Do not communicate by sharing memory; share memory by communicating"
*/

// Import section: Import necessary packages
import (
	"fmt" // Formatting and printing
	// Mathematical operations
	"sync" // Synchronization primitives (WaitGroup, Mutex)
	"time" // Time-related functions
)

/*
   PROJECT STRUCTURE CONVENTIONS (Typical layout):

   myproject/
   ├── go.mod              // Module definition
   ├── go.sum              // Dependency checksums
   ├── cmd/                // Entry points for applications
   │   └── myapp/
   │       └── main.go     // This is where main() typically lives
   ├── internal/           // Private application code
   │   └── utils/          // Not importable by other modules
   ├── pkg/                // Library code exportable to others
   │   └── mylib/
   │       ├── types.go
   │       └── utils.go
   ├── api/                // API contracts (protobuf, OpenAPI)
   ├── web/                // Web-specific components
   ├── configs/            Configuration files
   ├── deployments/        Deployment configurations
   ├── scripts/            Build/install scripts
   └── README.md

   This structure scales from small to enterprise projects.
*/

/*
   VISIBILITY RULES:

   Exported identifiers (public): Start with UPPERCASE letter
   Unexported identifiers (private): Start with lowercase letter

   This applies to: variables, constants, functions, types, methods, and fields
*/

// Exported constant (accessible from other packages)
const MaxConnections = 100

// Unexported constant (only accessible within this package)
const defaultTimeout = 30 * time.Second

// Exported struct type
type Employee struct {
	// Exported field
	Name string

	// Unexported field (encapsulated)
	salary float64

	// Embedded struct (composition example)
	ContactInfo

	// Unexported embedded struct
	privateDetails privateData
}

// Unexported struct type
type privateData struct {
	ssn string
}

// Embedded struct for composition
type ContactInfo struct {
	Email string // Exported field
	phone string // Unexported field
}

/*
   PACKAGES AND IMPORTS:

   - Each directory is a single package
   - Package name should match directory name (except main)
   - Import paths can be:
       - Standard library: "fmt", "net/http"
       - Remote repositories: "github.com/user/repo"
       - Local relative paths: "./mypackage" or "../parentpackage"
   - Use blank identifier for side effects: _ "github.com/lib/pq"
   - Use alias for conflicting names: redis "github.com/go-redis/redis"
*/

// Exported function (starts with uppercase)
func NewEmployee(name string, salary float64) *Employee {
	return &Employee{
		Name:   name,
		salary: salary,
		ContactInfo: ContactInfo{
			Email: fmt.Sprintf("%s@company.com", name),
			phone: "555-0123",
		},
		privateDetails: privateData{
			ssn: "123-45-6789",
		},
	}
}

// Unexported function (only accessible within this package)
func calculateBonus(salary float64) float64 {
	return salary * 0.10
}

// Method with pointer receiver (can modify the struct)
func (e *Employee) SetSalary(newSalary float64) {
	if newSalary > 0 {
		e.salary = newSalary
	}
}

// Exported method
func (e *Employee) GetBonus() float64 {
	return calculateBonus(e.salary) // Can call unexported function
}

// Interface definition (implicit implementation)
type Worker interface {
	Work() string
}

// Employee implicitly implements Worker interface
func (e *Employee) Work() string {
	return fmt.Sprintf("%s is working hard", e.Name)
}

/*
   GO TOOLCHAIN OVERVIEW (Commands you'll use frequently):

   go build    - Compiles packages and dependencies, produces executable
   go run      - Compiles and runs Go program (convenience for development)
   go test     - Runs tests in current directory
   go mod      - Module maintenance (init, tidy, vendor)
   go get      - Adds dependencies to current module
   go install  - Compiles and installs packages to $GOPATH/bin
   go fmt      - Formats source code (always run this!)
   go vet      - Reports suspicious constructs
   go doc      - Shows documentation
*/

/*
   CONCURRENCY EXAMPLES:
   Demonstrating Go's built-in concurrency primitives
*/

// Exported function demonstrating goroutines
func RunConcurrentExample() {
	fmt.Println("\n=== Concurrency Example ===")

	// WaitGroup ensures main goroutine waits for others
	var wg sync.WaitGroup

	// Channel for communication between goroutines
	results := make(chan string, 3)

	// Launch 3 goroutines
	for i := 1; i <= 3; i++ {
		wg.Add(1) // Increment WaitGroup counter

		// Goroutine (lightweight thread)
		go func(id int) {
			defer wg.Done() // Decrement counter when done

			// Simulate work
			time.Sleep(time.Duration(id*100) * time.Millisecond)

			// Send result through channel
			results <- fmt.Sprintf("Worker %d completed", id)
		}(i)
	}

	// Close channel when all goroutines are done
	go func() {
		wg.Wait()
		close(results)
	}()

	// Receive results from channel
	for result := range results {
		fmt.Println(result)
	}

	// Buffered channel example
	fmt.Println("\n=== Buffered Channel Example ===")
	messages := make(chan string, 2)
	messages <- "Hello"
	messages <- "World"
	// messages <- "Third" // This would block because buffer is full

	fmt.Println(<-messages)
	fmt.Println(<-messages)
}

/*
SIMPLICITY IN ERROR HANDLING:
Go uses multiple return values for errors (no exceptions)
*/
func Divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("cannot divide by zero")
	}
	return a / b, nil
}

/*
DEFER STATEMENT:
Ensures resources are cleaned up regardless of execution path
*/
func FileProcessor() {
	fmt.Println("\n=== Defer Example ===")

	// Simulating file operations
	fmt.Println("Opening file...")

	// Defer statements execute in LIFO order
	defer fmt.Println("4. Fourth cleanup")
	defer fmt.Println("3. Third cleanup")
	defer fmt.Println("2. Closing file...")

	fmt.Println("1. Processing file...")

	// Even if panic occurs, deferred functions run
	// defer func() {
	//     if r := recover(); r != nil {
	//         fmt.Println("Recovered from panic:", r)
	//     }
	// }()
}

// main function - Entry point of the executable
func main() {
	fmt.Println("=== Go Language Basics Demonstration ===")

	// VARIABLE DECLARATIONS (showing different styles)
	var explicitVar string = "explicit" // Explicit type
	inferredVar := "inferred"           // Type inference

	// Multiple declarations
	var (
		name   = "Alice"
		age    = 30
		height float64
	)

	height = 5.8

	fmt.Printf("Variables: %s, %s, %s, %d, %.1f\n",
		explicitVar, inferredVar, name, age, height)

	// Create employee using constructor
	emp := NewEmployee("John Doe", 75000)

	// Access exported fields
	fmt.Printf("\nEmployee: %s\n", emp.Name)
	fmt.Printf("Email: %s\n", emp.Email) // From embedded struct

	// Call methods
	fmt.Printf("Work status: %s\n", emp.Work())
	fmt.Printf("Bonus: $%.2f\n", emp.GetBonus())

	// Error handling example
	result, err := Divide(10, 2)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Division result: %.2f\n", result)
	}

	// Try division by zero
	_, err = Divide(10, 0)
	if err != nil {
		fmt.Printf("Expected error: %v\n", err)
	}

	// Demonstrate composition
	fmt.Println("\n=== Composition Example ===")
	emp.SetSalary(80000)
	fmt.Printf("Updated bonus: $%.2f\n", emp.GetBonus())

	// Run concurrency example
	RunConcurrentExample()

	// Defer example
	FileProcessor()

	// Demonstrate interface usage
	var worker Worker = emp
	fmt.Printf("\nInterface call: %s\n", worker.Work())

	// Type switch example
	fmt.Println("\n=== Type Assertion ===")
	describeType(emp)
	describeType(42)
	describeType("Hello")

	fmt.Println("\n=== Program Complete ===")
}

// Helper function demonstrating type switches
func describeType(i interface{}) {
	switch v := i.(type) {
	case *Employee:
		fmt.Printf("It's an Employee: %s\n", v.Name)
	case int:
		fmt.Printf("It's an integer: %d\n", v)
	case string:
		fmt.Printf("It's a string: %s\n", v)
	default:
		fmt.Printf("Unknown type: %T\n", v)
	}
}

/*
   HOW TO USE THIS PROGRAM:

   1. Save as main.go
   2. Initialize module: go mod init example.com/demo
   3. Run: go run main.go
   4. Build: go build -o demoapp
   5. Test: go test ./... (if you add *_test.go files)

   Key takeaways:
   - Simple, readable code
   - Composition over inheritance
   - Explicit error handling
   - Built-in concurrency
   - Fast compilation
   - Single binary deployment
*/
