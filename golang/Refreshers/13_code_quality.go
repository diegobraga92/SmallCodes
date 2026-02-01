/*
================================================================================
GOLANG CODE QUALITY & IDIOMS - JUNIOR TO SENIOR CONCEPTS
================================================================================
This comprehensive example demonstrates key Go idioms, best practices,
and concepts important for professional Go development.
*/

package main

import (
	// Standard library imports grouped together
	"context"
	"errors"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	// Third-party imports in separate group
	"golang.org/x/sync/errgroup"
)

/*
-------------------------------------------------------------------------------
1. GO FORMATTING (go fmt, goimports)
-------------------------------------------------------------------------------
Go enforces consistent formatting through gofmt. goimports additionally
organizes imports. Always format code before committing.
*/

// gofmt ensures consistent:
// - Indentation (tabs, not spaces)
// - Line length (auto-wrapping)
// - Brace positioning
// - Spacing around operators

// Example: Before gofmt might look messy:
// func messyFunc(x int,y int)int{return x+y}

// After gofmt (auto-corrected):
func cleanFunc(x int, y int) int {
	return x + y
}

/*
-------------------------------------------------------------------------------
2. IDIOMATIC NAMING CONVENTIONS
-------------------------------------------------------------------------------
Go has specific naming conventions that signal intent and scope.
*/

// Package names: lowercase, single-word, meaningful
// GOOD: 'strings', 'http', 'json'
// BAD: 'StringUtilities', 'HTTPLibrary'

// Exported identifiers: PascalCase (capital first letter)
type ExportedStruct struct {
	// Exported field
	PublicField string

	// Unexported field (lowercase)
	privateField int
}

// Unexported identifiers: camelCase
var localVariable = "internal use only"

// Acronyms: all caps (URL, HTTP, ID)
type APIHandler struct {
	BaseURL    string // GOOD
	HttpClient string // BAD (should be HTTPClient)
	UserId     string // BAD (should be UserID)
}

// Interfaces: -er suffix (if one method)
type Reader interface {
	Read(p []byte) (n int, err error)
}

// Multiple methods: descriptive name
type ReadWriteCloser interface {
	Reader
	Writer
	Closer
}

// Methods: verbs or descriptive names
func (s *ExportedStruct) Calculate() int {
	return len(s.PublicField) + s.privateField
}

// Booleans: "is", "has", "can" prefixes recommended
var isEnabled = true
var hasPermission = false
var canExecute = true

/*
-------------------------------------------------------------------------------
3. ERROR-FIRST RETURNS
-------------------------------------------------------------------------------
Go's idiomatic error handling pattern: return error as last value.
Always check errors, don't ignore them.
*/

// Basic error-first pattern
func divide(a, b float64) (float64, error) {
	if b == 0 {
		// Return zero value and meaningful error
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

// For functions that only return an error
func validateInput(input string) error {
	if len(input) == 0 {
		return errors.New("input cannot be empty")
	}
	if len(input) > 100 {
		return fmt.Errorf("input too long: %d characters", len(input))
	}
	return nil
}

// Named return values for documentation (use sparingly)
func processFile(path string) (content []byte, err error) {
	// Defer can modify named return values
	defer func() {
		if err != nil {
			err = fmt.Errorf("processFile %q: %w", path, err)
		}
	}()

	content, err = os.ReadFile(path)
	if err != nil {
		return nil, err // Return zero value for content
	}

	// Success case
	return content, nil
}

// Sentinel errors for specific error conditions
var (
	ErrNotFound     = errors.New("not found")
	ErrInvalidInput = errors.New("invalid input")
)

func findUser(id string) (*User, error) {
	if id == "" {
		return nil, ErrInvalidInput
	}
	// ... lookup logic
	return nil, ErrNotFound
}

// Error wrapping with fmt.Errorf %w
func complexOperation() error {
	if err := step1(); err != nil {
		return fmt.Errorf("step1 failed: %w", err)
	}
	if err := step2(); err != nil {
		return fmt.Errorf("step2 failed: %w", err)
	}
	return nil
}

// Custom error types for structured error data
type ValidationError struct {
	Field   string
	Message string
	Code    int
}

func (e ValidationError) Error() string {
	return fmt.Sprintf("validation error on %s: %s", e.Field, e.Message)
}

// Using errors.Is and errors.As for error inspection
func handleError(err error) {
	if errors.Is(err, ErrNotFound) {
		fmt.Println("Resource not found")
	}

	var valErr ValidationError
	if errors.As(err, &valErr) {
		fmt.Printf("Field %s invalid: %s\n", valErr.Field, valErr.Message)
	}
}

/*
-------------------------------------------------------------------------------
4. AVOIDING UNNECESSARY ABSTRACTIONS
-------------------------------------------------------------------------------
Go values simplicity and clarity over premature abstraction.
*/

// BAD: Over-abstracted with unnecessary interfaces
type StringProcessorInterface interface {
	Process(string) string
	Validate(string) bool
}

type AdvancedStringProcessor struct{}

// GOOD: Simple function when that's all you need
func toUpper(s string) string {
	return strings.ToUpper(s)
}

// BAD: Premature interface for single implementation
type UserStore interface {
	GetUser(id string) (*User, error)
	SaveUser(user *User) error
}

// Wait until you have at least 2 implementations before creating interface
type DBUserStore struct{}

func (d *DBUserStore) GetUser(id string) (*User, error) {
	// Database implementation
	return &User{}, nil
}

// Later, when you need a mock/test implementation:
type MockUserStore struct{}

func (m *MockUserStore) GetUser(id string) (*User, error) {
	// Mock implementation
	return &User{ID: id}, nil
}

// Only then define interface where it's used
type UserRepository interface {
	GetUser(id string) (*User, error)
}

// BAD: Unnecessary factory pattern
func NewComplexFactory(config Config) *ComplexService {
	return &ComplexService{config: config}
}

// GOOD: Simple constructor
func NewService(config Config) *Service {
	return &Service{config: config}
}

// Favor concrete types until interface is needed
type Service struct {
	config Config
}

// BAD: Over-engineered with generics too early
type Container[T any] struct {
	items []T
}

// GOOD: Use specific types first, generalize only when needed
type StringContainer struct {
	items []string
}

/*
-------------------------------------------------------------------------------
5. EFFECTIVE GO PRINCIPLES
-------------------------------------------------------------------------------
Principles from the official "Effective Go" guide.
*/

// -------------------- Simplicity & Readability --------------------
// Clear, readable code is prioritized over clever code.

// GOOD: Obvious logic
func calculateTotal(items []Item) float64 {
	var total float64
	for _, item := range items {
		total += item.Price
	}
	return total
}

// BAD: "Clever" but obscure
func calc(items []Item) (t float64) {
	for _, i := range items {
		t += i.Price
	}
	return
}

// -------------------- Zero Values --------------------
// Use zero values effectively. They're meaningful in Go.
type Server struct {
	Host     string
	Port     int        // 0 is meaningful (invalid port)
	Timeout  time.Duration // 0 means no timeout
	Shutdown chan struct{}
}

func NewServer() *Server {
	return &Server{
		// Host: "" - zero value is fine
		// Port: 0 - will need to be set
		Shutdown: make(chan struct{}), // Channels need initialization
	}
}

// -------------------- Composition Over Inheritance --------------------
// Go doesn't have inheritance; use embedding and interfaces.

type Person struct {
	Name string
	Age  int
}

// Embedding, not inheritance
type Employee struct {
	Person  // Embedded type gets Person's fields/methods
	EmployeeID string
	Department string
}

func (p Person) Greet() string {
	return fmt.Sprintf("Hello, I'm %s", p.Name)
}

// Employee automatically gets Greet() method but can override it
func (e Employee) Greet() string {
	return fmt.Sprintf("Hello, I'm %s from %s", e.Name, e.Department)
}

// -------------------- Functional Options Pattern --------------------
// Clean way to handle optional parameters.

type ServerConfig struct {
	Host    string
	Port    int
	Timeout time.Duration
	Debug   bool
}

type Option func(*ServerConfig)

func WithHost(host string) Option {
	return func(c *ServerConfig) {
		c.Host = host
	}
}

func WithPort(port int) Option {
	return func(c *ServerConfig) {
		c.Port = port
	}
}

func WithTimeout(timeout time.Duration) Option {
	return func(c *ServerConfig) {
		c.Timeout = timeout
	}
}

func NewServerConfig(opts ...Option) *ServerConfig {
	config := &ServerConfig{
		Host:    "localhost", // Sensible defaults
		Port:    8080,
		Timeout: 30 * time.Second,
		Debug:   false,
	}

	for _, opt := range opts {
		opt(config)
	}

	return config
}

// Usage: clean and readable
func setupServer() {
	// Default config
	cfg1 := NewServerConfig()

	// Custom config
	cfg2 := NewServerConfig(
		WithHost("example.com"),
		WithPort(9000),
		WithTimeout(60*time.Second),
	)

	_ = cfg1
	_ = cfg2
}

// -------------------- Context Pattern --------------------
// Use context for cancellation, timeouts, and request-scoped values.

func longRunningOperation(ctx context.Context, data string) (string, error) {
	// Check if context is already cancelled
	if err := ctx.Err(); err != nil {
		return "", err
	}

	// Simulate work with cancellation support
	select {
	case <-time.After(2 * time.Second):
		return "result: " + data, nil
	case <-ctx.Done():
		return "", ctx.Err() // Handle cancellation gracefully
	}
}

func processWithTimeout() {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel() // Always call cancel to release resources

	result, err := longRunningOperation(ctx, "test")
	if err != nil {
		fmt.Printf("Operation failed: %v\n", err)
		return
	}
	fmt.Println(result)
}

// -------------------- Concurrency Patterns --------------------
// Goroutines, channels, and synchronization.

func processConcurrently(data []string) []string {
	results := make(chan string, len(data))
	var wg sync.WaitGroup

	for _, item := range data {
		wg.Add(1)
		go func(s string) {
			defer wg.Done()
			// Process item
			results <- strings.ToUpper(s)
		}(item)
	}

	// Close channel when all goroutines complete
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect results
	var output []string
	for result := range results {
		output = append(output, result)
	}

	return output
}

// Using errgroup for concurrent operations with error handling
func fetchMultipleURLs(urls []string) ([]string, error) {
	var g errgroup.Group
	results := make([]string, len(urls))

	for i, url := range urls {
		i, url := i, url // Capture loop variables
		g.Go(func() error {
			resp, err := http.Get(url)
			if err != nil {
				return fmt.Errorf("failed to fetch %s: %w", url, err)
			}
			defer resp.Body.Close()
			// Process response
			results[i] = fmt.Sprintf("Fetched %s", url)
			return nil
		})
	}

	if err := g.Wait(); err != nil {
		return nil, err
	}
	return results, nil
}

// -------------------- Receiver Types --------------------
// Choose pointer vs value receivers carefully.

type Counter struct {
	value int
}

// Pointer receiver: when method needs to modify receiver
func (c *Counter) Increment() {
	c.value++
}

// Pointer receiver: when struct is large to avoid copying
func (c *Counter) Value() int {
	return c.value
}

// Value receiver: when method doesn't modify receiver and struct is small
type Point struct {
	X, Y int
}

func (p Point) DistanceToOrigin() float64 {
	return math.Sqrt(float64(p.X*p.X + p.Y*p.Y))
}

// -------------------- Defer for Cleanup --------------------
// Use defer for resource cleanup, but be mindful in loops.

func processFileSafely(path string) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close() // Always close the file

	// Multiple defers execute in LIFO order
	defer fmt.Println("File processing complete")

	// Process file
	return nil
}

// BAD: defer in loop can cause resource exhaustion
func processFilesBad(files []string) {
	for _, file := range files {
		f, err := os.Open(file)
		if err != nil {
			continue
		}
		defer f.Close() // All files stay open until function returns!
		// Process file
	}
}

// GOOD: Use helper function or manual cleanup in loops
func processFilesGood(files []string) error {
	for _, file := range files {
		if err := processSingleFile(file); err != nil {
			return err
		}
	}
	return nil
}

func processSingleFile(path string) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close() // Closed when helper function returns

	// Process file
	return nil
}

// -------------------- Package Organization --------------------
// Organize code by responsibility, not by type.

// BAD: Controller package with only interfaces
// package controller
// type UserController interface{}
// type ProductController interface{}

// GOOD: Organize by domain/feature
// package user
// type Repository interface{}
// type Service struct{}
// type Handler struct{}

// -------------------- Testing --------------------
// Write testable code with clear interfaces.

// Service with dependencies that can be mocked
type UserService struct {
	repo UserRepository
}

func (s *UserService) GetUserByID(id string) (*User, error) {
	return s.repo.GetUser(id)
}

// In test file:
type mockRepository struct{}

func (m *mockRepository) GetUser(id string) (*User, error) {
	return &User{ID: id, Name: "Test User"}, nil
}

/*
-------------------------------------------------------------------------------
PRACTICAL EXAMPLES
-------------------------------------------------------------------------------
*/

// Example struct used throughout
type User struct {
	ID   string
	Name string
}

// sync package example
var sync.WaitGroup

// http package example
var http.Get

// math package example
var math.Sqrt

func main() {
	fmt.Println("Go Code Quality & Idioms Examples")
	fmt.Println("==================================")

	// Error handling example
	result, err := divide(10, 2)
	if err != nil {
		log.Printf("Division failed: %v", err)
	} else {
		fmt.Printf("10 / 2 = %.1f\n", result)
	}

	// Context example
	processWithTimeout()

	// Functional options example
	config := NewServerConfig(WithPort(9090), WithHost("api.example.com"))
	fmt.Printf("Server config: %+v\n", config)

	// Concurrent processing example
	data := []string{"a", "b", "c", "d"}
	results := processConcurrently(data)
	fmt.Printf("Concurrent results: %v\n", results)

	// Error wrapping and inspection
	err = complexOperation()
	if err != nil {
		fmt.Printf("Wrapped error: %v\n", err)
		handleError(err)
	}
}

/*
-------------------------------------------------------------------------------
KEY TAKEAWAYS:
-------------------------------------------------------------------------------
1. Always run gofmt/goimports before committing
2. Follow naming conventions - they convey meaning
3. Handle ALL errors - never ignore them
4. Keep it simple - avoid unnecessary abstractions
5. Use composition, not inheritance
6. Leverage zero values - they're meaningful
7. Use context for cancellation and timeouts
8. Write concurrent code safely with goroutines and channels
9. Make packages focused and cohesive
10. Write clear, readable code over clever code
*/

// Additional note: Use `go vet` and `staticcheck` for deeper code analysis
// Use `golangci-lint` for comprehensive linting in CI/CD pipelines