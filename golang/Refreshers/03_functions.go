/*
   Go Functions - Comprehensive Example with Detailed Comments

   This file demonstrates Go's function capabilities including:
   - Function declarations and signatures
   - Multiple return values (Go's signature feature)
   - Named return values
   - Variadic functions
   - Anonymous functions and closures
   - Function types and first-class functions
*/

package main

import (
	"errors"
	"fmt"
	"math"
	"strings"
)

func main() {
	fmt.Println("=== GO FUNCTIONS DEMONSTRATION ===")
	fmt.Println()

	/*
	   SECTION 1: FUNCTION DECLARATIONS

	   Basic syntax: func functionName(parameters) returnType { ... }
	   Go functions can return multiple values, which is one of Go's most distinctive features.
	*/

	fmt.Println("=== 1. FUNCTION DECLARATIONS ===")

	// -----------------------------------------------------------------
	// Basic function with no parameters and no return value
	// -----------------------------------------------------------------
	fmt.Println("\n1. Basic function:")
	greet() // Calls the function defined below

	// -----------------------------------------------------------------
	// Function with parameters
	// -----------------------------------------------------------------
	fmt.Println("\n2. Function with parameters:")
	result := add(10, 20)
	fmt.Printf("   add(10, 20) = %d\n", result)

	// -----------------------------------------------------------------
	// Function with different parameter types
	// -----------------------------------------------------------------
	fmt.Println("\n3. Function with mixed parameters:")
	formatted := formatUser("Alice", 30, true)
	fmt.Printf("   formatUser(\"Alice\", 30, true) = %s\n", formatted)

	// -----------------------------------------------------------------
	// Function returning a value
	// -----------------------------------------------------------------
	fmt.Println("\n4. Function returning a computed value:")
	circleArea := calculateCircleArea(5.0)
	fmt.Printf("   calculateCircleArea(5.0) = %.2f\n", circleArea)

	// Function returning a boolean
	fmt.Println("\n5. Function returning boolean:")
	isEven := checkEven(42)
	fmt.Printf("   checkEven(42) = %v\n", isEven)

	fmt.Println()

	/*
	   SECTION 2: MULTIPLE RETURN VALUES

	   This is one of Go's most important features. Functions can return multiple values,
	   which is especially useful for returning both a result and an error.
	*/

	fmt.Println("=== 2. MULTIPLE RETURN VALUES ===")

	// -----------------------------------------------------------------
	// Basic multiple return values
	// -----------------------------------------------------------------
	fmt.Println("\n1. Basic multiple return values:")
	sum, product := calculateSumAndProduct(4, 5)
	fmt.Printf("   calculateSumAndProduct(4, 5) = sum: %d, product: %d\n", sum, product)

	// -----------------------------------------------------------------
	// Multiple return values with different types
	// -----------------------------------------------------------------
	fmt.Println("\n2. Multiple returns with different types:")
	length, uppercase := processString("hello")
	fmt.Printf("   processString(\"hello\") = length: %d, uppercase: \"%s\"\n", length, uppercase)

	// -----------------------------------------------------------------
	// Ignoring return values using blank identifier (_)
	// -----------------------------------------------------------------
	fmt.Println("\n3. Ignoring return values with _:")
	sumOnly, _ := calculateSumAndProduct(3, 7) // Ignore the product
	fmt.Printf("   calculateSumAndProduct(3, 7) ignoring product = sum: %d\n", sumOnly)

	// Ignoring all but one
	_, productOnly := calculateSumAndProduct(2, 8) // Ignore the sum
	fmt.Printf("   calculateSumAndProduct(2, 8) ignoring sum = product: %d\n", productOnly)

	// -----------------------------------------------------------------
	// The most common pattern: Result and error
	// -----------------------------------------------------------------
	fmt.Println("\n4. Result and error pattern (Go idiom):")

	// Successful operation
	value, err := divide(10.0, 2.0)
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   divide(10.0, 2.0) = %.2f\n", value)
	}

	// Error case
	value, err = divide(10.0, 0.0)
	if err != nil {
		fmt.Printf("   divide(10.0, 0.0) = Error: %v\n", err)
	}

	// -----------------------------------------------------------------
	// Returning three or more values
	// -----------------------------------------------------------------
	fmt.Println("\n5. Three return values:")
	min, max, avg := stats([]int{10, 20, 30, 40, 50})
	fmt.Printf("   stats([10,20,30,40,50]) = min: %d, max: %d, avg: %.1f\n", min, max, avg)

	// -----------------------------------------------------------------
	// Practical example: File operations
	// -----------------------------------------------------------------
	fmt.Println("\n6. Practical file operation pattern:")
	content, lines, err := readFileSimulation("data.txt")
	if err != nil {
		fmt.Printf("   Error reading file: %v\n", err)
	} else {
		fmt.Printf("   File content: \"%s\" (%d lines)\n", content, lines)
	}

	fmt.Println()

	/*
	   SECTION 3: NAMED RETURN VALUES

	   Go allows you to name return values, which:
	   1. Acts as documentation
	   2. Initializes the variables to zero values
	   3. Allows using 'naked return' (just 'return' without values)
	   4. Can be modified in defer statements
	*/

	fmt.Println("=== 3. NAMED RETURN VALUES ===")

	// -----------------------------------------------------------------
	// Basic named return values
	// -----------------------------------------------------------------
	fmt.Println("\n1. Basic named return values:")
	x, y := swap(5, 10)
	fmt.Printf("   swap(5, 10) = %d, %d\n", x, y)

	// -----------------------------------------------------------------
	// Named returns with initialization
	// -----------------------------------------------------------------
	fmt.Println("\n2. Named returns with initialization:")
	success, message := processWithDefaultMessage(true)
	fmt.Printf("   processWithDefaultMessage(true) = success: %v, message: \"%s\"\n", success, message)

	success, message = processWithDefaultMessage(false)
	fmt.Printf("   processWithDefaultMessage(false) = success: %v, message: \"%s\"\n", success, message)

	// -----------------------------------------------------------------
	// Naked return (using named returns without specifying values)
	// -----------------------------------------------------------------
	fmt.Println("\n3. Naked return (just 'return'):")
	total, count := calculateTotalAndCount(1, 2, 3, 4, 5)
	fmt.Printf("   calculateTotalAndCount(1,2,3,4,5) = total: %d, count: %d\n", total, count)

	// -----------------------------------------------------------------
	// Named returns in defer statements
	// -----------------------------------------------------------------
	fmt.Println("\n4. Named returns modified by defer:")
	result := namedReturnWithDefer(10)
	fmt.Printf("   namedReturnWithDefer(10) = %d\n", result)

	// -----------------------------------------------------------------
	// Practical example: Database operation
	// -----------------------------------------------------------------
	fmt.Println("\n5. Practical example with error handling:")
	user, err := getUserByID(123)
	if err != nil {
		fmt.Printf("   getUserByID(123) = Error: %v\n", err)
	} else {
		fmt.Printf("   getUserByID(123) = User: %+v\n", user)
	}

	user, err = getUserByID(999) // Non-existent user
	if err != nil {
		fmt.Printf("   getUserByID(999) = Error: %v\n", err)
	}

	fmt.Println()

	/*
	   SECTION 4: VARIADIC FUNCTIONS

	   Variadic functions can accept a variable number of arguments.
	   The ... syntax indicates that the function can be called with any number of arguments.
	   Inside the function, the parameter becomes a slice.
	*/

	fmt.Println("=== 4. VARIADIC FUNCTIONS ===")

	// -----------------------------------------------------------------
	// Basic variadic function
	// -----------------------------------------------------------------
	fmt.Println("\n1. Basic variadic function:")
	sum1 := sumVariadic(1, 2, 3)
	fmt.Printf("   sumVariadic(1, 2, 3) = %d\n", sum1)

	sum2 := sumVariadic(10, 20, 30, 40, 50)
	fmt.Printf("   sumVariadic(10, 20, 30, 40, 50) = %d\n", sum2)

	// Calling with no arguments
	sum3 := sumVariadic()
	fmt.Printf("   sumVariadic() = %d\n", sum3)

	// -----------------------------------------------------------------
	// Passing slice to variadic function using ...
	// -----------------------------------------------------------------
	fmt.Println("\n2. Passing slice to variadic function:")
	numbers := []int{1, 3, 5, 7, 9}
	sum4 := sumVariadic(numbers...)
	fmt.Printf("   numbers := []int{1,3,5,7,9}\n")
	fmt.Printf("   sumVariadic(numbers...) = %d\n", sum4)

	// -----------------------------------------------------------------
	// Variadic function with other parameters
	// -----------------------------------------------------------------
	fmt.Println("\n3. Variadic with other parameters:")
	total1 := sumWithPrefix("Subtotal:", 10, 20, 30)
	fmt.Printf("   %s\n", total1)

	total2 := sumWithPrefix("Total:", 1, 2, 3, 4, 5)
	fmt.Printf("   %s\n", total2)

	// -----------------------------------------------------------------
	// Mixed parameter types
	// -----------------------------------------------------------------
	fmt.Println("\n4. Variadic with mixed operations:")
	result1 := joinStringsWithSeparator(", ", "apple", "banana", "cherry")
	fmt.Printf("   joinStringsWithSeparator(\", \", \"apple\", \"banana\", \"cherry\") = \"%s\"\n", result1)

	// -----------------------------------------------------------------
	// Practical example: Logging function
	// -----------------------------------------------------------------
	fmt.Println("\n5. Practical logging example:")
	logMessage("INFO", "User login", "session started", "user=alice")

	// -----------------------------------------------------------------
	// Variadic function returning multiple values
	// -----------------------------------------------------------------
	fmt.Println("\n6. Variadic with multiple returns:")
	minVal, maxVal := findMinMax(42, 15, 87, 23, 56)
	fmt.Printf("   findMinMax(42, 15, 87, 23, 56) = min: %d, max: %d\n", minVal, maxVal)

	fmt.Println()

	/*
	   SECTION 5: ANONYMOUS FUNCTIONS & CLOSURES

	   In Go, functions are first-class citizens:
	   - They can be assigned to variables
	   - They can be passed as arguments to other functions
	   - They can be returned from functions
	   - They can capture variables from their surrounding scope (closures)
	*/

	fmt.Println("=== 5. ANONYMOUS FUNCTIONS & CLOSURES ===")

	// -----------------------------------------------------------------
	// Basic anonymous function
	// -----------------------------------------------------------------
	fmt.Println("\n1. Basic anonymous function:")

	// Assign anonymous function to a variable
	square := func(x int) int {
		return x * x
	}

	fmt.Printf("   square(5) = %d\n", square(5))
	fmt.Printf("   square(9) = %d\n", square(9))

	// Immediately invoked function expression (IIFE)
	fmt.Println("\n2. Immediately invoked function (IIFE):")
	func() {
		fmt.Println("   This function runs immediately!")
	}() // Parentheses invoke it immediately

	resultIIFE := func(x, y int) int {
		return x * y
	}(6, 7) // Invoked immediately with arguments

	fmt.Printf("   IIFE result: 6 * 7 = %d\n", resultIIFE)

	// -----------------------------------------------------------------
	// Passing functions as arguments
	// -----------------------------------------------------------------
	fmt.Println("\n3. Functions as arguments (higher-order functions):")

	// Define operation functions
	addFunc := func(a, b int) int { return a + b }
	multiplyFunc := func(a, b int) int { return a * b }

	// Apply operation
	resultAdd := applyOperation(10, 5, addFunc)
	resultMult := applyOperation(10, 5, multiplyFunc)

	fmt.Printf("   applyOperation(10, 5, add) = %d\n", resultAdd)
	fmt.Printf("   applyOperation(10, 5, multiply) = %d\n", resultMult)

	// Using anonymous function directly as argument
	resultSub := applyOperation(10, 5, func(a, b int) int {
		return a - b
	})
	fmt.Printf("   applyOperation(10, 5, subtract) = %d\n", resultSub)

	// -----------------------------------------------------------------
	// Returning functions from functions
	// -----------------------------------------------------------------
	fmt.Println("\n4. Returning functions from functions:")

	// Function that returns a greeting function
	greeter := createGreeter("Hello")
	fmt.Printf("   greeter(\"Alice\") = \"%s\"\n", greeter("Alice"))

	// Another greeter
	formalGreeter := createGreeter("Good day")
	fmt.Printf("   formalGreeter(\"Mr. Smith\") = \"%s\"\n", formalGreeter("Mr. Smith"))

	// -----------------------------------------------------------------
	// CLOSURES - Functions that capture surrounding variables
	// -----------------------------------------------------------------
	fmt.Println("\n5. Closures (capturing variables):")

	// Counter closure
	counter := createCounter()
	fmt.Printf("   counter() = %d\n", counter())
	fmt.Printf("   counter() = %d\n", counter())
	fmt.Printf("   counter() = %d\n", counter())

	// Each closure has its own state
	anotherCounter := createCounter()
	fmt.Printf("   anotherCounter() = %d\n", anotherCounter())
	fmt.Printf("   counter() = %d (still has its own state) = %d\n", counter(), counter())

	// -----------------------------------------------------------------
	// Practical closure: Accumulator/Adder
	// -----------------------------------------------------------------
	fmt.Println("\n6. Accumulator closure:")
	adder := createAdder()
	fmt.Printf("   adder(5) = %d\n", adder(5))
	fmt.Printf("   adder(10) = %d\n", adder(10))
	fmt.Printf("   adder(-3) = %d\n", adder(-3))

	// -----------------------------------------------------------------
	// Closure with parameters
	// -----------------------------------------------------------------
	fmt.Println("\n7. Closure with parameters:")
	multiplier := createMultiplier(2)
	fmt.Printf("   multiplier(5) = %d\n", multiplier(5))
	fmt.Printf("   multiplier(10) = %d\n", multiplier(10))

	triple := createMultiplier(3)
	fmt.Printf("   triple(7) = %d\n", triple(7))

	// -----------------------------------------------------------------
	// Closures in loops (common gotcha!)
	// -----------------------------------------------------------------
	fmt.Println("\n8. Closures in loops (the gotcha):")

	var funcs []func() int
	for i := 0; i < 3; i++ {
		// WRONG: All closures capture the same variable i
		funcs = append(funcs, func() int {
			return i // Captures i by reference
		})
	}

	fmt.Println("   WRONG way (all return 3):")
	for j, f := range funcs {
		fmt.Printf("     funcs[%d]() = %d\n", j, f())
	}

	// RIGHT way: Capture loop variable value
	var funcsCorrect []func() int
	for i := 0; i < 3; i++ {
		// Create a new variable for each iteration
		value := i
		funcsCorrect = append(funcsCorrect, func() int {
			return value // Captures value for this iteration
		})
	}

	fmt.Println("\n   RIGHT way (capture loop variable):")
	for j, f := range funcsCorrect {
		fmt.Printf("     funcsCorrect[%d]() = %d\n", j, f())
	}

	// -----------------------------------------------------------------
	// Practical use: Function generators
	// -----------------------------------------------------------------
	fmt.Println("\n9. Practical: Email validator generator:")

	validateCompanyEmail := createEmailValidator("company.com")
	fmt.Printf("   validateCompanyEmail(\"alice@company.com\") = %v\n",
		validateCompanyEmail("alice@company.com"))
	fmt.Printf("   validateCompanyEmail(\"bob@gmail.com\") = %v\n",
		validateCompanyEmail("bob@gmail.com"))

	// -----------------------------------------------------------------
	// Closures with structs (methods as closures)
	// -----------------------------------------------------------------
	fmt.Println("\n10. Methods as closures:")

	calc := Calculator{value: 100}
	// Method value (bound method)
	addFive := calc.Add
	fmt.Printf("   calc.Add(5) via closure = %d\n", addFive(5))

	// Method expression (unbound, takes receiver as first arg)
	addMethod := Calculator.Add
	resultMethod := addMethod(calc, 10)
	fmt.Printf("   Calculator.Add(calc, 10) = %d\n", resultMethod)

	fmt.Println()
	fmt.Println("=== END OF FUNCTIONS DEMONSTRATION ===")
}

// =====================================================================
// FUNCTION DEFINITIONS FOR SECTION 1
// =====================================================================

// Basic function with no parameters and no return value
func greet() {
	fmt.Println("   Hello from greet() function!")
}

// Function with parameters and return value
func add(a int, b int) int {
	return a + b
}

// When parameters share the same type, you can declare them like this
func formatUser(name string, age int, active bool) string {
	status := "inactive"
	if active {
		status = "active"
	}
	return fmt.Sprintf("%s (%d years old, %s)", name, age, status)
}

// Function with return value
func calculateCircleArea(radius float64) float64 {
	return math.Pi * radius * radius
}

// Function returning boolean
func checkEven(num int) bool {
	return num%2 == 0
}

// =====================================================================
// FUNCTION DEFINITIONS FOR SECTION 2
// =====================================================================

// Function returning multiple values
func calculateSumAndProduct(a, b int) (int, int) {
	return a + b, a * b
}

// Multiple returns with different types
func processString(s string) (int, string) {
	return len(s), strings.ToUpper(s)
}

// Most common Go pattern: value and error
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("division by zero")
	}
	return a / b, nil
}

// Returning three values
func stats(numbers []int) (min int, max int, avg float64) {
	if len(numbers) == 0 {
		return 0, 0, 0
	}

	min = numbers[0]
	max = numbers[0]
	total := 0

	for _, num := range numbers {
		if num < min {
			min = num
		}
		if num > max {
			max = num
		}
		total += num
	}

	avg = float64(total) / float64(len(numbers))
	return min, max, avg
}

// Practical file operation simulation
func readFileSimulation(filename string) (content string, lines int, err error) {
	if filename == "" {
		err = errors.New("filename cannot be empty")
		return
	}

	// Simulating reading a file
	if filename == "data.txt" {
		content = "Line 1\nLine 2\nLine 3"
		lines = 3
	} else {
		err = errors.New("file not found")
	}
	return
}

// =====================================================================
// FUNCTION DEFINITIONS FOR SECTION 3
// =====================================================================

// Named return values
func swap(a, b int) (x int, y int) {
	x = b
	y = a
	return // Naked return: returns x and y
}

// Named returns with initialization
func processWithDefaultMessage(success bool) (ok bool, msg string) {
	// ok and msg are automatically initialized to false and ""

	if success {
		ok = true
		msg = "Operation completed successfully"
	} else {
		msg = "Operation failed" // ok remains false
	}

	return // Naked return
}

// Naked return with named values
func calculateTotalAndCount(numbers ...int) (total int, count int) {
	for _, num := range numbers {
		total += num
		count++
	}
	return // Returns total and count
}

// Named return modified by defer
func namedReturnWithDefer(n int) (result int) {
	// result is initialized to 0

	defer func() {
		result *= 2 // This runs AFTER the return statement!
		fmt.Println("   (defer executed, doubling result)")
	}()

	result = n * 10
	return // Returns 100 for n=10 (10*10=100, then defer doubles to 200)
}

// User struct for demonstration
type User struct {
	ID   int
	Name string
}

// Practical example with named returns
func getUserByID(id int) (user User, err error) {
	// user and err are initialized to zero values

	defer func() {
		// Log the operation
		if err == nil {
			fmt.Printf("   (Successfully retrieved user %d)\n", id)
		} else {
			fmt.Printf("   (Failed to retrieve user %d: %v)\n", id, err)
		}
	}()

	// Simulate database lookup
	if id == 123 {
		user = User{ID: 123, Name: "Alice"}
		return // Success
	}

	err = fmt.Errorf("user with ID %d not found", id)
	return // Error case
}

// =====================================================================
// FUNCTION DEFINITIONS FOR SECTION 4
// =====================================================================

// Basic variadic function
func sumVariadic(numbers ...int) int {
	total := 0
	for _, num := range numbers {
		total += num
	}
	return total
}

// Variadic function with other parameters
func sumWithPrefix(prefix string, numbers ...int) string {
	total := 0
	for _, num := range numbers {
		total += num
	}
	return fmt.Sprintf("%s %d", prefix, total)
}

// Variadic with string parameters
func joinStringsWithSeparator(sep string, strings ...string) string {
	return strings.Join(strings, sep)
}

// Practical logging function
func logMessage(level string, messages ...string) {
	timestamp := "2024-01-15 10:30:00" // In real code, use time.Now()
	fullMessage := strings.Join(messages, " - ")
	fmt.Printf("   [%s] %s: %s\n", timestamp, level, fullMessage)
}

// Variadic function returning multiple values
func findMinMax(numbers ...int) (min int, max int) {
	if len(numbers) == 0 {
		return 0, 0
	}

	min = numbers[0]
	max = numbers[0]

	for _, num := range numbers {
		if num < min {
			min = num
		}
		if num > max {
			max = num
		}
	}
	return
}

// =====================================================================
// FUNCTION DEFINITIONS FOR SECTION 5
// =====================================================================

// Higher-order function: takes a function as parameter
func applyOperation(a, b int, operation func(int, int) int) int {
	return operation(a, b)
}

// Function that returns a function
func createGreeter(greeting string) func(string) string {
	// Returns a closure that captures 'greeting'
	return func(name string) string {
		return fmt.Sprintf("%s, %s!", greeting, name)
	}
}

// Classic counter closure
func createCounter() func() int {
	count := 0 // This variable is captured by the closure
	return func() int {
		count++
		return count
	}
}

// Accumulator closure
func createAdder() func(int) int {
	total := 0
	return func(x int) int {
		total += x
		return total
	}
}

// Closure with parameter captured at creation
func createMultiplier(factor int) func(int) int {
	return func(x int) int {
		return x * factor
	}
}

// Email validator generator
func createEmailValidator(domain string) func(string) bool {
	return func(email string) bool {
		return strings.HasSuffix(email, "@"+domain)
	}
}

// Struct with method
type Calculator struct {
	value int
}

// Method on Calculator
func (c Calculator) Add(x int) int {
	return c.value + x
}

/*
   KEY TAKEAWAYS:

   1. FUNCTION DECLARATIONS:
      - Use clear, descriptive names
      - Parameters come before return types
      - Type comes after variable name

   2. MULTIPLE RETURN VALUES:
      - Go's signature feature
      - Perfect for returning result + error
      - Use blank identifier (_) to ignore values
      - Makes error handling explicit and clear

   3. NAMED RETURN VALUES:
      - Acts as documentation
      - Initialized to zero values
      - Enable naked returns (use sparingly)
      - Can be modified by defer statements

   4. VARIADIC FUNCTIONS:
      - Use ... syntax before type
      - Becomes slice inside function
      - Can pass slice using ... operator
      - Useful for utility functions

   5. ANONYMOUS FUNCTIONS & CLOSURES:
      - Functions are first-class citizens
      - Can assign to variables, pass as args, return from functions
      - Closures capture variables from surrounding scope
      - Watch out for loop variable capture gotcha
      - Powerful for creating function factories and decorators

   BEST PRACTICES:
   - Keep functions small and focused (single responsibility)
   - Use multiple returns for operations that can fail
   - Name return values for documentation in complex functions
   - Use closures judiciously (they can make code harder to understand)
   - Consider function signatures part of API design
*/
