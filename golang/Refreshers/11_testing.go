/*
GO TESTING COMPREHENSIVE GUIDE
This file demonstrates essential Go testing concepts from fundamentals to advanced patterns.
Run tests with: go test -v ./...
*/

package testing_examples

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// ============================================================================
// 1. TESTING FUNDAMENTALS & TESTING PACKAGE
// ============================================================================

// Calculator is a simple struct to demonstrate testing
type Calculator struct{}

func (c Calculator) Add(a, b int) int {
	return a + b
}

func (c Calculator) Divide(a, b int) (int, error) {
	if b == 0 {
		return 0, fmt.Errorf("division by zero")
	}
	return a / b, nil
}

// TestAdd demonstrates basic testing with the testing package
func TestAdd(t *testing.T) {
	calc := Calculator{}
	result := calc.Add(2, 3)
	expected := 5

	// Use t.Error or t.Errorf for non-fatal failures
	if result != expected {
		t.Errorf("Add(2, 3) = %d; want %d", result, expected)
	}

	// t.Fatal or t.Fatalf stops test execution immediately
	if calc.Add(0, 0) != 0 {
		t.Fatal("Add(0, 0) should return 0")
	}
}

// TestDivideWithError demonstrates error testing
func TestDivideWithError(t *testing.T) {
	calc := Calculator{}

	// Test successful case
	result, err := calc.Divide(10, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if result != 5 {
		t.Errorf("Divide(10, 2) = %d; want 5", result)
	}

	// Test error case
	_, err = calc.Divide(10, 0)
	if err == nil {
		t.Error("expected error for division by zero")
	}
	if err != nil && !strings.Contains(err.Error(), "division by zero") {
		t.Errorf("unexpected error message: %v", err)
	}
}

// ============================================================================
// 2. TABLE-DRIVEN TESTS (Recommended pattern in Go)
// ============================================================================

func TestAddTableDriven(t *testing.T) {
	calc := Calculator{}

	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		{"positive numbers", 2, 3, 5},
		{"negative numbers", -1, -1, -2},
		{"mixed signs", -5, 10, 5},
		{"zero addition", 0, 0, 0},
		{"large numbers", 1000, 2000, 3000},
	}

	for _, tt := range tests {
		// Using t.Run() creates a subtest for each case (more on this later)
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Add(tt.a, tt.b)
			if result != tt.expected {
				t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
			}
		})
	}
}

// ============================================================================
// 3. SUBTESTS (For better test organization and selective execution)
// ============================================================================

func TestCalculatorSubtests(t *testing.T) {
	calc := Calculator{}

	t.Run("Addition", func(t *testing.T) {
		t.Run("Positive numbers", func(t *testing.T) {
			result := calc.Add(2, 3)
			if result != 5 {
				t.Errorf("got %d, want 5", result)
			}
		})

		t.Run("With zero", func(t *testing.T) {
			result := calc.Add(5, 0)
			if result != 5 {
				t.Errorf("got %d, want 5", result)
			}
		})
	})

	t.Run("Division", func(t *testing.T) {
		t.Run("Valid division", func(t *testing.T) {
			result, err := calc.Divide(10, 2)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if result != 5 {
				t.Errorf("got %d, want 5", result)
			}
		})

		t.Run("Division by zero", func(t *testing.T) {
			_, err := calc.Divide(10, 0)
			if err == nil {
				t.Error("expected error for division by zero")
			}
		})
	})

	// Subtests can be run individually:
	// go test -v -run "TestCalculatorSubtests/Addition"
	// go test -v -run "TestCalculatorSubtests/Division/Valid"
}

// ============================================================================
// 4. TEST COVERAGE
// ============================================================================

// Generate coverage report: go test -cover ./...
// Generate HTML coverage report: go test -coverprofile=coverage.out && go tool cover -html=coverage.out

// uncoveredFunction demonstrates uncovered code
func uncoveredFunction() bool {
	// This function won't be covered by tests
	return true
}

// ============================================================================
// 5. GOLDEN FILES (For testing complex outputs like JSON, HTML, etc.)
// ============================================================================

type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func FormatUserJSON(u User) (string, error) {
	data, err := json.MarshalIndent(u, "", "  ")
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// TestFormatUserJSONGolden uses golden files for comparison
func TestFormatUserJSONGolden(t *testing.T) {
	user := User{ID: 1, Name: "Alice", Age: 30}

	// Generate the output
	output, err := FormatUserJSON(user)
	if err != nil {
		t.Fatalf("failed to format user: %v", err)
	}

	// Define golden file path
	goldenPath := filepath.Join("testdata", "user.golden")

	// Update golden file (uncomment when you need to update expected output):
	// if *update {
	//     os.WriteFile(goldenPath, []byte(output), 0644)
	// }

	// Read expected output from golden file
	expected, err := os.ReadFile(goldenPath)
	if err != nil {
		t.Fatalf("failed to read golden file: %v", err)
	}

	// Compare
	if strings.TrimSpace(output) != strings.TrimSpace(string(expected)) {
		t.Errorf("output doesn't match golden file.\nGot:\n%s\nWant:\n%s", output, string(expected))
	}
}

// ============================================================================
// 6. BENCHMARKING AND PROFILING
// ============================================================================

// Fibonacci function for benchmarking
func Fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	return Fibonacci(n-1) + Fibonacci(n-2)
}

// BenchmarkFibonacci measures performance
func BenchmarkFibonacci(b *testing.B) {
	// Run the function b.N times
	for i := 0; i < b.N; i++ {
		Fibonacci(20) // Benchmark with n=20
	}
}

// BenchmarkFibonacciWithSetup demonstrates setup/teardown
func BenchmarkFibonacciWithSetup(b *testing.B) {
	// Setup (run once before benchmarks)
	// b.ResetTimer() // Use if setup takes significant time

	// Run benchmark
	for i := 0; i < b.N; i++ {
		Fibonacci(10)
	}

	// Teardown (if needed)
}

// Run benchmarks: go test -bench=. -benchmem
// Generate CPU profile: go test -bench=. -cpuprofile=cpu.prof
// Generate memory profile: go test -bench=. -memprofile=mem.prof
// Analyze with: go tool pprof cpu.prof

// ============================================================================
// 7. FUZZ TESTING (Go 1.18+)
// ============================================================================

// ReverseString for fuzz testing
func ReverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// FuzzReverse demonstrates fuzz testing
func FuzzReverse(f *testing.F) {
	// Add seed corpus (examples to start with)
	testcases := []string{"Hello", " ", "12345", "😀🎉"}
	for _, tc := range testcases {
		f.Add(tc)
	}

	// Fuzz function
	f.Fuzz(func(t *testing.T, original string) {
		reversed := ReverseString(original)
		doubleReversed := ReverseString(reversed)

		// Property: reversing twice returns original
		if original != doubleReversed {
			t.Errorf("Before: %q, after: %q", original, doubleReversed)
		}

		// Additional property: reversed string should have same rune count
		if len([]rune(original)) != len([]rune(reversed)) {
			t.Errorf("Length mismatch: original %d, reversed %d",
				len([]rune(original)), len([]rune(reversed)))
		}
	})
}

// Run fuzz test: go test -fuzz=FuzzReverse -fuzztime=30s

// ============================================================================
// 8. MOCKING AND TEST DOUBLES
// ============================================================================

// Interfaces enable mocking in Go
type DataStore interface {
	GetUser(id int) (*User, error)
	SaveUser(user *User) error
}

type RealDataStore struct {
	// Database connection, etc.
}

func (r *RealDataStore) GetUser(id int) (*User, error) {
	// Real database call
	return &User{ID: id, Name: "Real User"}, nil
}

func (r *RealDataStore) SaveUser(user *User) error {
	// Real database save
	return nil
}

// MockDataStore for testing
type MockDataStore struct {
	GetUserFunc  func(id int) (*User, error)
	SaveUserFunc func(user *User) error
	CallCount    map[string]int
}

func (m *MockDataStore) GetUser(id int) (*User, error) {
	m.CallCount["GetUser"]++
	if m.GetUserFunc != nil {
		return m.GetUserFunc(id)
	}
	return &User{ID: id, Name: "Mock User"}, nil
}

func (m *MockDataStore) SaveUser(user *User) error {
	m.CallCount["SaveUser"]++
	if m.SaveUserFunc != nil {
		return m.SaveUserFunc(user)
	}
	return nil
}

func NewMockDataStore() *MockDataStore {
	return &MockDataStore{
		CallCount: make(map[string]int),
	}
}

// UserService depends on DataStore interface
type UserService struct {
	store DataStore
}

func (s *UserService) GetAndUpdateUser(id int, newName string) error {
	user, err := s.store.GetUser(id)
	if err != nil {
		return err
	}

	user.Name = newName
	return s.store.SaveUser(user)
}

// TestUserServiceWithMock demonstrates mocking
func TestUserServiceWithMock(t *testing.T) {
	mockStore := NewMockDataStore()
	service := UserService{store: mockStore}

	// Set up mock behavior
	expectedUser := &User{ID: 1, Name: "Test User"}
	mockStore.GetUserFunc = func(id int) (*User, error) {
		if id != 1 {
			return nil, fmt.Errorf("user not found")
		}
		return expectedUser, nil
	}

	mockStore.SaveUserFunc = func(user *User) error {
		if user.Name != "Updated Name" {
			return fmt.Errorf("unexpected name: %s", user.Name)
		}
		return nil
	}

	// Test the service
	err := service.GetAndUpdateUser(1, "Updated Name")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	// Verify mock was called correctly
	if mockStore.CallCount["GetUser"] != 1 {
		t.Errorf("GetUser called %d times, expected 1", mockStore.CallCount["GetUser"])
	}
	if mockStore.CallCount["SaveUser"] != 1 {
		t.Errorf("SaveUser called %d times, expected 1", mockStore.CallCount["SaveUser"])
	}
}

// ============================================================================
// 9. HTTP TESTING WITH MOCK SERVER
// ============================================================================

// HTTPClient interface for mocking HTTP calls
type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

type APIClient struct {
	Client  HTTPClient
	BaseURL string
}

func (c *APIClient) FetchData() (string, error) {
	req, err := http.NewRequest("GET", c.BaseURL+"/data", nil)
	if err != nil {
		return "", err
	}

	resp, err := c.Client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}

// TestAPIClientWithMock demonstrates HTTP mocking
func TestAPIClientWithMock(t *testing.T) {
	// Create a mock HTTP client
	mockClient := &MockHTTPClient{
		Response: &http.Response{
			StatusCode: 200,
			Body:       io.NopCloser(bytes.NewBufferString(`{"data": "test"}`)),
		},
	}

	client := &APIClient{
		Client:  mockClient,
		BaseURL: "http://api.example.com",
	}

	data, err := client.FetchData()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	expected := `{"data": "test"}`
	if data != expected {
		t.Errorf("got %s, want %s", data, expected)
	}
}

type MockHTTPClient struct {
	Response *http.Response
	Error    error
}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
	if m.Error != nil {
		return nil, m.Error
	}
	return m.Response, nil
}

// ============================================================================
// 10. TEST HELPERS AND CLEANUP
// ============================================================================

// TestHelper demonstrates test helpers and cleanup
func TestHelper(t *testing.T) {
	// Setup temporary file
	tmpFile, err := os.CreateTemp("", "test-*.txt")
	if err != nil {
		t.Fatal(err)
	}

	// Cleanup function (always runs even if test fails)
	t.Cleanup(func() {
		tmpFile.Close()
		os.Remove(tmpFile.Name())
		t.Log("Cleaned up temporary file")
	})

	// Write test data
	content := "test data"
	_, err = tmpFile.WriteString(content)
	if err != nil {
		t.Fatal(err)
	}

	// Reset file pointer
	_, err = tmpFile.Seek(0, 0)
	if err != nil {
		t.Fatal(err)
	}

	// Read and verify
	readContent, err := io.ReadAll(tmpFile)
	if err != nil {
		t.Fatal(err)
	}

	if string(readContent) != content {
		t.Errorf("got %s, want %s", readContent, content)
	}
}

// Helper function (won't fail test directly)
func readTestFile(t *testing.T, path string) string {
	t.Helper() // Marks this as a helper function
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("failed to read file: %v", err)
	}
	return string(data)
}

// ============================================================================
// 11. TEST MAIN FOR SETUP/TEARDOWN
// ============================================================================

// TestMain provides global setup/teardown
func TestMain(m *testing.M) {
	// Global setup
	fmt.Println("Setting up test environment...")

	// Create test directory
	err := os.MkdirAll("testdata", 0755)
	if err != nil {
		fmt.Printf("Failed to create testdata: %v\n", err)
		os.Exit(1)
	}

	// Run tests
	exitCode := m.Run()

	// Global teardown
	fmt.Println("Tearing down test environment...")

	// Exit with test result code
	os.Exit(exitCode)
}

// ============================================================================
// 12. PARALLEL TESTING
// ============================================================================

func TestParallel1(t *testing.T) {
	t.Parallel() // Run in parallel with other tests
	time.Sleep(100 * time.Millisecond)
	// Test code...
}

func TestParallel2(t *testing.T) {
	t.Parallel() // Run in parallel with other tests
	time.Sleep(100 * time.Millisecond)
	// Test code...
}

// ============================================================================
// 13. USEFUL GO TEST FLAGS AND COMMANDS
// ============================================================================

/*
COMMON GO TEST COMMANDS:

# Basic testing
go test ./...                          # Test all packages
go test -v ./...                       # Verbose output
go test -run TestAdd ./...             # Run specific test
go test -run "TestAdd.*" ./...         # Run tests matching pattern

# Coverage
go test -cover ./...                   # Show coverage percentage
go test -coverprofile=coverage.out     # Generate coverage file
go tool cover -html=coverage.out       # View coverage in browser
go test -covermode=atomic ./...        # For concurrent code

# Benchmarking
go test -bench=. ./...                 # Run all benchmarks
go test -bench=Fibonacci ./...         # Run specific benchmark
go test -bench=. -benchmem ./...       # Show memory allocations
go test -bench=. -count=5 ./...        # Run each benchmark 5 times

# Profiling
go test -bench=. -cpuprofile=cpu.prof
go test -bench=. -memprofile=mem.prof
go test -bench=. -blockprofile=block.prof
go tool pprof cpu.prof                 # Analyze profile

# Fuzzing
go test -fuzz=FuzzReverse -fuzztime=30s
go test -fuzz=. -fuzzminimizetime=30s

# Other useful flags
go test -timeout=30s ./...            # Set timeout
go test -short ./...                  # Skip long tests
go test -failfast ./...               # Stop on first failure
go test -list .                       # List tests without running
go test -json ./...                   # JSON output for CI/CD
go test -race ./...                   # Race detector

# Test organization
go test ./pkg/...                     # Test specific package
go test ./internal/...                # Test internal packages
go test -tags=integration ./...       # Run integration tests

# Golden files update pattern
var update = flag.Bool("update", false, "update golden files")
go test -update ./...                 # Update golden files
*/

// ============================================================================
// 14. INTEGRATION TEST EXAMPLE
// ============================================================================

// Integration test (often in separate file with build tag)
// //go:build integration
// // +build integration

func TestIntegrationWithDatabase(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	// Real database setup and tests...
	t.Log("Running integration test")
}

// ============================================================================
// 15. TESTING PRIVATE FUNCTIONS
// ============================================================================

// privateFunc is not exported (lowercase)
func privateFunc(input string) string {
	return "processed: " + input
}

// Test private functions in the same package
func TestPrivateFunc(t *testing.T) {
	result := privateFunc("test")
	expected := "processed: test"
	if result != expected {
		t.Errorf("got %s, want %s", result, expected)
	}
}

// ============================================================================
// 16. RACE CONDITION TESTING
// ============================================================================

var counter int

func incrementCounter() {
	counter++
}

func TestRaceCondition(t *testing.T) {
	// Run with: go test -race ./...
	for i := 0; i < 1000; i++ {
		go incrementCounter()
	}
	// Race detector will catch issues if present
}

// ============================================================================
// 17. EXAMPLE TESTS (Documentation + Testing)
// ============================================================================

func ExampleAdd() {
	calc := Calculator{}
	sum := calc.Add(3, 4)
	fmt.Println(sum)
	// Output: 7
}

// ============================================================================
// BEST PRACTICES SUMMARY
// ============================================================================

/*
1. Use table-driven tests for multiple test cases
2. Name tests clearly: Test[Function]_[Scenario]
3. Use t.Helper() for helper functions
4. Test both success and error cases
5. Use t.Cleanup() for resource cleanup
6. Run tests with -race flag in CI
7. Aim for high test coverage but focus on critical paths
8. Mock interfaces, not concrete implementations
9. Use subtests for better organization and selective running
10. Keep tests fast and independent
11. Use golden files for complex output verification
12. Leverage fuzz testing for finding edge cases
13. Benchmark performance-critical code
14. Separate unit, integration, and e2e tests
*/

// This file can be tested with: go test -v -cover -race ./...
