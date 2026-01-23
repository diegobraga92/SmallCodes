/*
   Go Control Flow - Comprehensive Example with Detailed Comments

   This file demonstrates Go's control flow constructs with practical examples.
   Go has simplified control flow compared to other languages - no while or do-while loops,
   but powerful for, switch, and defer statements.
*/

package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	fmt.Println("=== GO CONTROL FLOW DEMONSTRATION ===")
	fmt.Println()

	/*
	   SECTION 1: IF STATEMENTS

	   Go's if statements are similar to other languages but with some unique features:
	   - Parentheses are optional (but not recommended by style guide)
	   - Can include a short statement before the condition
	   - No ternary operator (condition ? a : b) in Go
	*/

	fmt.Println("=== 1. IF/ELSE STATEMENTS ===")

	// -----------------------------------------------------------------
	// Basic if statement
	// -----------------------------------------------------------------
	x := 10
	if x > 5 {
		fmt.Printf("1. Basic if: %d is greater than 5\n", x)
	}

	// -----------------------------------------------------------------
	// if-else statement
	// -----------------------------------------------------------------
	temperature := 25
	if temperature > 30 {
		fmt.Println("2. It's hot outside")
	} else {
		fmt.Println("2. Temperature is comfortable")
	}

	// -----------------------------------------------------------------
	// if-else if chain
	// -----------------------------------------------------------------
	score := 85
	if score >= 90 {
		fmt.Println("3. Grade: A")
	} else if score >= 80 {
		fmt.Println("3. Grade: B")
	} else if score >= 70 {
		fmt.Println("3. Grade: C")
	} else if score >= 60 {
		fmt.Println("3. Grade: D")
	} else {
		fmt.Println("3. Grade: F")
	}

	// -----------------------------------------------------------------
	// if with short statement (Go's unique feature)
	// -----------------------------------------------------------------
	/*
	   The short statement executes before evaluating the condition.
	   Variables declared in the short statement are only in scope for the if block.
	*/

	// Example 1: Checking map value
	userRoles := map[string]string{
		"alice": "admin",
		"bob":   "user",
	}

	if role, exists := userRoles["alice"]; exists {
		fmt.Printf("4. Alice has role: %s\n", role)
	} else {
		fmt.Println("4. User not found")
	}

	// role variable is NOT accessible here - only in if block
	// fmt.Println(role) // This would cause compile error

	// Example 2: Function call in condition
	if err := initializeSystem(); err != nil {
		fmt.Printf("5. System initialization error: %v\n", err)
	} else {
		fmt.Println("5. System initialized successfully")
	}

	// Example 3: Multiple statements with comma
	if file, err := os.Open("test.txt"); err != nil {
		fmt.Printf("6. Error opening file: %v\n", err)
	} else {
		// file is only accessible in this block
		fmt.Println("6. File opened successfully")
		file.Close()
	}

	// -----------------------------------------------------------------
	// Nested if statements
	// -----------------------------------------------------------------
	age := 25
	hasLicense := true

	if age >= 18 {
		if hasLicense {
			fmt.Println("7. Can drive a car")
		} else {
			fmt.Println("7. Old enough but needs license")
		}
	} else {
		fmt.Println("7. Too young to drive")
	}

	// -----------------------------------------------------------------
	// Compact style (avoiding else when possible)
	// -----------------------------------------------------------------
	// Go encourages "happy path" coding style
	if !isUserAuthenticated("alice", "wrongpass") {
		fmt.Println("8. Authentication failed")
		return // Early return instead of else block
	}
	fmt.Println("8. User authenticated")

	fmt.Println()

	/*
	   SECTION 2: SWITCH STATEMENTS

	   Go's switch is more powerful than in many languages:
	   - Can switch on values OR types
	   - No fallthrough by default (unlike C/Java)
	   - Can use expressions in cases
	   - Can have no expression (like if-else chain)
	*/

	fmt.Println("=== 2. SWITCH STATEMENTS ===")

	// -----------------------------------------------------------------
	// Basic switch on value
	// -----------------------------------------------------------------
	day := "Monday"

	switch day {
	case "Monday":
		fmt.Println("1. Start of work week")
	case "Tuesday", "Wednesday", "Thursday": // Multiple values
		fmt.Println("1. Midweek")
	case "Friday":
		fmt.Println("1. Almost weekend!")
	case "Saturday", "Sunday":
		fmt.Println("1. Weekend!")
	default:
		fmt.Println("1. Invalid day")
	}

	// -----------------------------------------------------------------
	// Switch with expression
	// -----------------------------------------------------------------
	hour := time.Now().Hour()

	switch {
	case hour < 12:
		fmt.Println("2. Good morning!")
	case hour < 18:
		fmt.Println("2. Good afternoon!")
	default:
		fmt.Println("2. Good evening!")
	}

	// More complex expressions
	num := 42
	switch {
	case num%2 == 0 && num%3 == 0:
		fmt.Println("3. Divisible by both 2 and 3")
	case num%2 == 0:
		fmt.Println("3. Divisible by 2")
	case num%3 == 0:
		fmt.Println("3. Divisible by 3")
	default:
		fmt.Println("3. Not divisible by 2 or 3")
	}

	// -----------------------------------------------------------------
	// Switch with short statement
	// -----------------------------------------------------------------
	switch os := runtimeOS(); os {
	case "darwin":
		fmt.Println("4. Running on macOS")
	case "linux":
		fmt.Println("4. Running on Linux")
	case "windows":
		fmt.Println("4. Running on Windows")
	default:
		fmt.Printf("4. Unknown OS: %s\n", os)
	}

	// -----------------------------------------------------------------
	// Fallthrough (explicit)
	// -----------------------------------------------------------------
	/*
	   In Go, cases don't fall through by default (safer!).
	   Use 'fallthrough' keyword explicitly if needed.
	*/

	value := 2
	switch value {
	case 1:
		fmt.Print("5. Value is 1 and ")
		fallthrough // Continue to next case
	case 2:
		fmt.Print("5. Value is 2 and ")
		fallthrough
	case 3:
		fmt.Println("5. Value is 3 or fell through")
	default:
		fmt.Println("5. Other value")
	}

	// -----------------------------------------------------------------
	// TYPE SWITCH (Go's unique feature)
	// -----------------------------------------------------------------
	/*
	   Type switches inspect the dynamic type of an interface value.
	   Syntax: switch v := i.(type) { ... }
	*/

	fmt.Println("\n=== 3. TYPE SWITCHES ===")

	// Function that accepts any type via interface{}
	printType := func(i interface{}) {
		switch v := i.(type) {
		case int:
			fmt.Printf("  Value %d is an int\n", v)
		case float64:
			fmt.Printf("  Value %.2f is a float64\n", v)
		case string:
			fmt.Printf("  Value \"%s\" is a string\n", v)
		case bool:
			fmt.Printf("  Value %v is a bool\n", v)
		case []int:
			fmt.Printf("  Value %v is a slice of int\n", v)
		default:
			fmt.Printf("  Unknown type: %T\n", v)
		}
	}

	// Test type switch with different values
	printType(42)
	printType(3.14159)
	printType("Hello Go")
	printType(true)
	printType([]int{1, 2, 3})
	printType(time.Now())

	// Type switch with custom types
	type Circle struct{ Radius float64 }
	type Square struct{ Side float64 }

	var shape interface{} = Circle{Radius: 5}

	switch s := shape.(type) {
	case Circle:
		fmt.Printf("  Shape is Circle with radius %.1f\n", s.Radius)
	case Square:
		fmt.Printf("  Shape is Square with side %.1f\n", s.Side)
	default:
		fmt.Println("  Unknown shape")
	}

	// Type switch with methods
	var writer interface{} = os.Stdout

	switch w := writer.(type) {
	case *os.File:
		fmt.Println("  Writer is a file")
		w.WriteString("Writing to file\n")
	case fmt.Stringer:
		fmt.Println("  Writer implements String()")
	default:
		fmt.Println("  Unknown writer type")
	}

	fmt.Println()

	/*
	   SECTION 3: FOR LOOPS

	   Go has only one loop construct: 'for'
	   It can be used in four ways:
	   1. Traditional C-style for loop
	   2. While-style loop (for condition)
	   3. Infinite loop (for {})
	   4. Range loop (for k, v := range collection)
	*/

	fmt.Println("=== 4. FOR LOOPS ===")

	// -----------------------------------------------------------------
	// Traditional C-style for loop
	// -----------------------------------------------------------------
	fmt.Println("1. Traditional for loop:")
	for i := 0; i < 5; i++ {
		fmt.Printf("  Iteration %d\n", i)
	}

	// Multiple variables
	fmt.Println("\n2. For loop with multiple variables:")
	for i, j := 0, 10; i < j; i, j = i+1, j-1 {
		fmt.Printf("  i=%d, j=%d\n", i, j)
	}

	// -----------------------------------------------------------------
	// While-style loop (Go doesn't have 'while' keyword)
	// -----------------------------------------------------------------
	fmt.Println("\n3. While-style loop (for condition):")
	counter := 0
	for counter < 3 {
		fmt.Printf("  Counter: %d\n", counter)
		counter++
	}

	// Simulating do-while loop
	fmt.Println("\n4. Simulating do-while loop:")
	attempts := 0
	for {
		attempts++
		fmt.Printf("  Attempt %d\n", attempts)
		if attempts >= 3 {
			break
		}
	}

	// -----------------------------------------------------------------
	// Infinite loop
	// -----------------------------------------------------------------
	fmt.Println("\n5. Infinite loop with break (simulated):")
	// Uncomment to see infinite loop
	/*
	   for {
	       fmt.Println("This would run forever")
	       time.Sleep(1 * time.Second)
	   }
	*/

	// Practical infinite loop example
	fmt.Println("  (Simulating server loop)")
	serverRunning := true
	requestCount := 0

	for serverRunning {
		requestCount++
		fmt.Printf("  Processing request #%d\n", requestCount)

		// Simulate some condition to stop
		if requestCount >= 3 {
			fmt.Println("  Shutting down server...")
			serverRunning = false
		}
	}

	// -----------------------------------------------------------------
	// RANGE LOOPS (for iterating collections)
	// -----------------------------------------------------------------
	fmt.Println("\n6. Range loops:")

	// Range over slice/array
	fruits := []string{"Apple", "Banana", "Cherry"}
	fmt.Println("  Iterating slice:")
	for index, fruit := range fruits {
		fmt.Printf("    Index %d: %s\n", index, fruit)
	}

	// Range over map
	scores := map[string]int{
		"Alice": 95,
		"Bob":   87,
		"Carol": 92,
	}
	fmt.Println("\n  Iterating map:")
	for name, score := range scores {
		fmt.Printf("    %s: %d\n", name, score)
	}

	// Range over string (gets runes, not bytes)
	fmt.Println("\n  Iterating string (runes):")
	for i, r := range "Hello, 世界" {
		fmt.Printf("    Position %d: %U = '%c'\n", i, r, r)
	}

	// Range over channel (covered in concurrency section)
	fmt.Println("\n7. Range with value only:")
	for _, fruit := range fruits {
		fmt.Printf("  Fruit: %s\n", fruit)
	}

	fmt.Println("\n8. Range with index only:")
	for i := range fruits {
		fmt.Printf("  Index: %d\n", i)
	}

	fmt.Println()

	/*
	   SECTION 4: BREAK, CONTINUE, GOTO

	   Go supports traditional flow control statements with some restrictions.
	*/

	fmt.Println("=== 5. BREAK, CONTINUE, and GOTO ===")

	// -----------------------------------------------------------------
	// BREAK statement
	// -----------------------------------------------------------------
	fmt.Println("1. Break statement:")

	// Basic break
	for i := 0; i < 10; i++ {
		if i == 5 {
			fmt.Println("  Breaking at i=5")
			break
		}
		fmt.Printf("  i=%d\n", i)
	}

	// Break with nested loops
	fmt.Println("\n2. Breaking nested loops:")
outerLoop:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if i == 1 && j == 1 {
				fmt.Println("  Breaking to outer loop")
				break outerLoop // Breaks to labeled loop
			}
			fmt.Printf("  i=%d, j=%d\n", i, j)
		}
	}

	// Break in switch
	fmt.Println("\n3. Break in switch (exits switch, not loop):")
	for i := 0; i < 3; i++ {
		switch i {
		case 0:
			fmt.Println("  Case 0")
		case 1:
			fmt.Println("  Case 1 - breaking switch")
			break // Breaks switch, not the for loop
		case 2:
			fmt.Println("  Case 2")
		}
		fmt.Printf("  Loop iteration %d complete\n", i)
	}

	// -----------------------------------------------------------------
	// CONTINUE statement
	// -----------------------------------------------------------------
	fmt.Println("\n4. Continue statement:")

	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			continue // Skip even numbers
		}
		fmt.Printf("  Odd number: %d\n", i)
	}

	// Continue with label
	fmt.Println("\n5. Continue with label:")
outer:
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if j == 1 {
				fmt.Printf("  Skipping j=1 in iteration i=%d\n", i)
				continue outer
			}
			fmt.Printf("  i=%d, j=%d\n", i, j)
		}
	}

	// -----------------------------------------------------------------
	// GOTO statement (use sparingly!)
	// -----------------------------------------------------------------
	/*
	   Go has goto but it's rarely needed and should be used carefully.
	   Restrictions:
	   - Can't jump over variable declarations
	   - Can't jump into another block
	   - Can't jump outside functions
	*/

	fmt.Println("\n6. Goto statement (practical example):")

	// Practical goto example: error handling
	if err := processWithGoto(); err != nil {
		fmt.Printf("  Process failed: %v\n", err)
	}

	// Another example: breaking out of nested loops
	fmt.Println("\n7. Goto for complex control flow:")
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if i == 1 && j == 1 {
				fmt.Println("  Jumping to cleanup")
				goto cleanup
			}
			fmt.Printf("  Processing i=%d, j=%d\n", i, j)
		}
	}

cleanup:
	fmt.Println("  Performing cleanup operations")

	fmt.Println()

	/*
	   SECTION 5: DEFER STATEMENT

	   Defer is one of Go's most unique and useful features.
	   It schedules a function call to run AFTER the surrounding function returns.

	   Key characteristics:
	   - Deferred calls execute in LIFO (Last In, First Out) order
	   - Arguments are evaluated immediately, but function executes later
	   - Used for cleanup (closing files, unlocking mutexes, etc.)
	   - Can modify named return values
	*/

	fmt.Println("=== 6. DEFER STATEMENT ===")

	// -----------------------------------------------------------------
	// Basic defer
	// -----------------------------------------------------------------
	fmt.Println("1. Basic defer examples:")

	deferExample1()

	// -----------------------------------------------------------------
	// Multiple defers (LIFO order)
	// -----------------------------------------------------------------
	fmt.Println("\n2. Multiple defers (LIFO order):")

	fmt.Println("  Starting function...")
	defer fmt.Println("  Defer 1: First registered, last executed")
	defer fmt.Println("  Defer 2: Second registered")
	defer fmt.Println("  Defer 3: Last registered, first executed")
	fmt.Println("  End of function")

	// -----------------------------------------------------------------
	// Defer with arguments evaluation
	// -----------------------------------------------------------------
	fmt.Println("\n3. Defer argument evaluation:")

	value := "initial"
	defer fmt.Printf("  Deferred print: %s\n", value)
	value = "modified"
	fmt.Printf("  Immediate print: %s\n", value)

	// To capture current value, use closure
	fmt.Println("\n4. Defer with closure:")
	for i := 0; i < 3; i++ {
		defer func() {
			fmt.Printf("  Closure: i=%d\n", i) // Captures i by reference
		}()
	}

	fmt.Println("\n5. Defer with parameter capture:")
	for i := 0; i < 3; i++ {
		defer func(n int) {
			fmt.Printf("  Captured: n=%d\n", n) // Captures value at defer time
		}(i)
	}

	// -----------------------------------------------------------------
	// Practical defer patterns
	// -----------------------------------------------------------------
	fmt.Println("\n6. Practical defer patterns:")

	// Pattern 1: Resource cleanup
	fmt.Println("  Opening resource...")
	resource := "file.txt"
	defer func() {
		fmt.Printf("  Closing resource: %s\n", resource)
	}()
	fmt.Println("  Using resource...")

	// Pattern 2: Timing a function
	defer timeTrack(time.Now(), "exampleFunction")

	// Pattern 3: Recover from panic
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("  Recovered from panic: %v\n", r)
		}
	}()

	// Uncomment to test panic recovery
	// panic("test panic")

	// -----------------------------------------------------------------
	// Defer with named return values
	// -----------------------------------------------------------------
	fmt.Println("\n7. Defer modifying return values:")

	result := namedReturnExample()
	fmt.Printf("  Function returned: %d\n", result)

	result2 := deferWithError()
	fmt.Printf("  Function with error returned: %v\n", result2)

	// -----------------------------------------------------------------
	// Common defer pitfalls
	// -----------------------------------------------------------------
	fmt.Println("\n8. Defer pitfalls to avoid:")

	// Pitfall 1: Defer in loop
	fmt.Println("  Processing items...")
	for _, item := range []string{"A", "B", "C"} {
		// Resource opened in loop - deferred cleanup happens at END of function
		// defer fmt.Printf("  Cleaning up: %s\n", item)
		// Better: Use immediate cleanup or separate function
		processItem(item)
	}

	fmt.Println()
	fmt.Println("=== END OF CONTROL FLOW DEMONSTRATION ===")
}

// Helper functions for demonstrations

func initializeSystem() error {
	return nil // Simulating success
}

func isUserAuthenticated(username, password string) bool {
	return username == "alice" && password == "secret"
}

func runtimeOS() string {
	// Simplified - in real code use runtime.GOOS
	return "linux"
}

func processWithGoto() error {
	// Simulating a function that needs cleanup at multiple points

	// Allocate resource
	resource := "database connection"
	fmt.Println("  Allocated:", resource)

	// First check
	if err := step1(); err != nil {
		goto cleanup
	}

	// Second check
	if err := step2(); err != nil {
		goto cleanup
	}

	// Success path
	fmt.Println("  All steps completed successfully")
	return nil

cleanup:
	fmt.Println("  Cleaning up:", resource)
	return fmt.Errorf("operation failed")
}

func step1() error {
	return nil // Simulating success
}

func step2() error {
	return fmt.Errorf("step2 failed") // Simulating failure
}

func deferExample1() {
	fmt.Println("  Before defer")
	defer fmt.Println("  Deferred statement executed")
	fmt.Println("  After defer, before return")
}

func timeTrack(start time.Time, name string) {
	elapsed := time.Since(start)
	fmt.Printf("  %s took %v\n", name, elapsed)
}

func namedReturnExample() (result int) {
	defer func() {
		result *= 2 // Modifies named return value
		fmt.Println("  Defer doubled the result")
	}()

	result = 21
	return // Returns 42
}

func deferWithError() (err error) {
	defer func() {
		if err != nil {
			fmt.Println("  Defer detected an error")
		}
	}()

	// Simulate operation that might fail
	err = fmt.Errorf("simulated error")
	return
}

func processItem(item string) {
	// Simulating immediate cleanup instead of defer in loop
	fmt.Printf("  Processing item: %s\n", item)
	// Cleanup happens here, not deferred
	fmt.Printf("  Cleaned up: %s\n", item)
}

/*
   KEY TAKEAWAYS:

   1. IF STATEMENTS:
      - Can include short statements: if x := f(); x < limit { ... }
      - Variables in short statements are block-scoped
      - No parentheses required (but consistent style is key)

   2. SWITCH STATEMENTS:
      - No fallthrough by default (safer code)
      - Can switch on values, expressions, or types
      - Type switches are powerful for interface values
      - Can use as a cleaner if-else chain

   3. FOR LOOPS (ONLY LOOP IN GO):
      - Four variations: C-style, while-style, infinite, range
      - Range loops work with slices, maps, strings, channels
      - No while or do-while keywords (use for instead)

   4. FLOW CONTROL:
      - break: exit loop or switch
      - continue: skip to next iteration
      - goto: available but use judiciously (mostly for error handling)
      - Labels allow breaking/continuing outer loops

   5. DEFER (UNIQUE GO FEATURE):
      - Executes when surrounding function returns
      - LIFO order for multiple defers
      - Arguments evaluated at defer time
      - Essential for resource cleanup
      - Can modify named return values
      - Use for unlocking mutexes, closing files, recovering panics

   BEST PRACTICES:
   - Use if with short statements for concise error handling
   - Prefer switch over long if-else chains
   - Use range loops for iterating collections
   - Use defer for all cleanup operations
   - Avoid goto except for centralized error handling
   - Keep control flow simple and readable
*/
