/*
   Go Basic Syntax & Types - Comprehensive Example with Detailed Comments

   This file demonstrates Go's basic syntax, type system, and fundamental concepts.
   Each section includes practical examples with extensive explanations.
*/

package main

import (
	"fmt"
	"reflect"
	"strconv"
)

func main() {
	fmt.Println("=== GO BASIC SYNTAX & TYPES DEMONSTRATION ===")
	fmt.Println()

	/*
	   SECTION 1: VARIABLES

	   Go has two main ways to declare variables:
	   1. Using 'var' keyword (explicit declaration)
	   2. Using ':=' (short variable declaration - type inference)

	   Variables in Go:
	   - Must be used (unused variables cause compile error)
	   - Have block scope
	   - Can be declared at package or function level
	*/
	fmt.Println("=== 1. VARIABLE DECLARATIONS ===")

	// -----------------------------------------------------------------
	// METHOD 1: Using 'var' keyword (explicit declaration)
	// -----------------------------------------------------------------

	// Single variable declaration with explicit type
	var name string = "Alice"
	fmt.Printf("var name string = \"Alice\"\t\t// Result: %s\n", name)

	// Multiple variables of the same type
	var x, y int = 10, 20
	fmt.Printf("var x, y int = 10, 20\t\t\t// Result: x=%d, y=%d\n", x, y)

	// Multiple variables of different types
	var (
		age     int     = 30
		height  float64 = 5.8
		isAdmin bool    = true
	)
	fmt.Printf("var (age int = 30; height float64 = 5.8; isAdmin bool = true)\n")
	fmt.Printf("\t\t\t\t\t// Result: age=%d, height=%.1f, isAdmin=%v\n", age, height, isAdmin)

	// Declaration without initialization (gets zero value)
	var uninitializedInt int
	var uninitializedString string
	var uninitializedBool bool
	var uninitializedFloat float64
	fmt.Printf("var uninitializedInt int\t\t// Zero value: %d\n", uninitializedInt)
	fmt.Printf("var uninitializedString string\t\t// Zero value: \"%s\"\n", uninitializedString)
	fmt.Printf("var uninitializedBool bool\t\t// Zero value: %v\n", uninitializedBool)
	fmt.Printf("var uninitializedFloat float64\t\t// Zero value: %v\n", uninitializedFloat)

	// Type-only declaration (implicit zero values)
	var implicitZero int
	fmt.Printf("var implicitZero int\t\t\t// Implicitly: %d\n", implicitZero)

	fmt.Println()

	// -----------------------------------------------------------------
	// METHOD 2: Short variable declaration (:=)
	// -----------------------------------------------------------------

	fmt.Println("=== 2. SHORT VARIABLE DECLARATION (:=) ===")

	/*
	   ':=' declares and initializes variables with type inference.
	   It can only be used INSIDE functions (not at package level).

	   Rules:
	   - Must have at least one new variable on left side
	   - Type is inferred from the right-hand side
	   - Can declare multiple variables at once
	*/

	// Single variable with type inference
	greeting := "Hello, Go!"
	fmt.Printf("greeting := \"Hello, Go!\"\t\t// Type: %T, Value: %s\n", greeting, greeting)

	// Multiple variables
	a, b := 42, 3.14
	fmt.Printf("a, b := 42, 3.14\t\t\t// a: %T=%v, b: %T=%v\n", a, a, b, b)

	// Mixed types
	isReady, price := true, 99.99
	fmt.Printf("isReady, price := true, 99.99\t\t// isReady: %T=%v, price: %T=%.2f\n",
		isReady, isReady, price, price)

	// At least one must be new
	x, z := 100, 200 // x was declared earlier, but z is new - this is OK
	fmt.Printf("x, z := 100, 200\t\t\t// Reassign x=%d, new z=%d\n", x, z)

	// Can't use := if all variables already exist
	// x, y := 300, 400  // This would cause compile error: no new variables

	fmt.Println()

	/*
	   SECTION 2: CONSTANTS

	   Constants are immutable values that must be known at compile time.
	   Key features:
	   - Must be initialized at declaration
	   - Can only be basic types (numbers, strings, booleans)
	   - Use 'const' keyword
	   - Can use 'iota' for enumerated constants
	*/

	fmt.Println("=== 3. CONSTANTS (const) ===")

	// Basic constant declaration
	const Pi = 3.14159
	const MaxUsers = 1000
	const AppName = "MyGoApp"

	fmt.Printf("const Pi = 3.14159\t\t\t// %T: %.5f\n", Pi, Pi)
	fmt.Printf("const MaxUsers = 1000\t\t\t// %T: %d\n", MaxUsers, MaxUsers)
	fmt.Printf("const AppName = \"MyGoApp\"\t\t// %T: %s\n", AppName, AppName)

	// Typed constants
	const SecondsPerHour int = 3600
	const Gravity float64 = 9.81

	fmt.Printf("const SecondsPerHour int = 3600\t// Explicit type: %T\n", SecondsPerHour)
	fmt.Printf("const Gravity float64 = 9.81\t\t// Explicit type: %T\n", Gravity)

	// Multiple constants declaration
	const (
		StatusOK      = 200
		StatusCreated = 201
		StatusError   = 500
	)

	fmt.Printf("const (StatusOK=200, StatusCreated=201, StatusError=500)\n")
	fmt.Printf("\t\t\t\t\t// Values: %d, %d, %d\n", StatusOK, StatusCreated, StatusError)

	// Constant expressions (evaluated at compile time)
	const (
		MinutesPerHour     = 60
		SecondsPerMinute   = 60
		SecondsPerHourCalc = MinutesPerHour * SecondsPerMinute // Computed at compile time
	)

	fmt.Printf("SecondsPerHourCalc = 60*60\t\t// Computed constant: %d\n", SecondsPerHourCalc)

	fmt.Println()

	/*
	   IOTA - Special constant generator

	   iota:
	   - Starts at 0 in each const block
	   - Increments by 1 for each constant
	   - Resets to 0 in new const block
	   - Useful for creating enumerated constants
	*/

	fmt.Println("=== 4. IOTA (Enumerated Constants) ===")

	// Basic iota usage
	const (
		Sunday    = iota // 0
		Monday           // 1
		Tuesday          // 2
		Wednesday        // 3
		Thursday         // 4
		Friday           // 5
		Saturday         // 6
	)

	fmt.Printf("Days of week (iota): Sun=%d, Mon=%d, Tue=%d, ... Sat=%d\n",
		Sunday, Monday, Tuesday, Saturday)

	// iota with expressions
	const (
		_  = iota             // Skip 0
		KB = 1 << (10 * iota) // 1 << (10 * 1) = 1024
		MB = 1 << (10 * iota) // 1 << (10 * 2) = 1048576
		GB = 1 << (10 * iota) // 1 << (10 * 3) = 1073741824
		TB = 1 << (10 * iota) // 1 << (10 * 4) = 1099511627776
	)

	fmt.Printf("Memory sizes (iota with bit shifting):\n")
	fmt.Printf("  KB = %d bytes\n", KB)
	fmt.Printf("  MB = %d bytes\n", MB)
	fmt.Printf("  GB = %d bytes\n", GB)

	// iota resetting in new const block
	const (
		Zero = iota // 0 (resets from previous const block)
		One         // 1
		Two         // 2
	)

	fmt.Printf("New const block (iota resets): Zero=%d, One=%d, Two=%d\n", Zero, One, Two)

	// Complex iota example with multiple values
	const (
		Apple, Banana   = iota + 1, iota + 2 // Apple=1, Banana=2
		Cherry, Date                         // Cherry=2, Date=3
		Elderberry, Fig                      // Elderberry=3, Fig=4
	)

	fmt.Printf("Multiple iotas per line: Apple=%d, Banana=%d, Cherry=%d, Fig=%d\n",
		Apple, Banana, Cherry, Fig)

	fmt.Println()

	/*
	   SECTION 3: PRIMITIVE TYPES

	   Go has several built-in primitive types with specific sizes.
	   All types have default zero values when not initialized.
	*/

	fmt.Println("=== 5. PRIMITIVE TYPES ===")

	// -----------------------------------------------------------------
	// INTEGER TYPES (signed and unsigned)
	// -----------------------------------------------------------------
	fmt.Println("Integer Types:")

	// Signed integers
	var int8Var int8 = 127     // -128 to 127
	var int16Var int16 = 32767 // -32768 to 32767
	var int32Var int32 = 2147483647
	var int64Var int64 = 9223372036854775807

	// Unsigned integers
	var uint8Var uint8 = 255 // 0 to 255
	var uint16Var uint16 = 65535
	var uint32Var uint32 = 4294967295
	var uint64Var uint64 = 18446744073709551615

	// Platform-dependent (32 or 64 bits depending on architecture)
	var intVar int = 42
	var uintVar uint = 42

	// Byte is alias for uint8
	var byteVar byte = 255 // Same as uint8

	// Rune is alias for int32, represents Unicode code point
	var runeVar rune = 'A' // Single quotes for runes

	fmt.Printf("  int8: %d, int16: %d, int: %d\n", int8Var, int16Var, intVar)
	fmt.Printf("  uint8: %d, byte: %d, rune: %U (Unicode for %c)\n", uint8Var, byteVar, runeVar, runeVar)

	// -----------------------------------------------------------------
	// FLOATING-POINT TYPES
	// -----------------------------------------------------------------
	fmt.Println("\nFloating-Point Types:")

	var float32Var float32 = 3.1415927
	var float64Var float64 = 3.141592653589793

	// Scientific notation
	var avogadro float64 = 6.02214076e23
	var smallNumber float64 = 1.616255e-35 // Planck length in meters

	fmt.Printf("  float32: %.7f (less precision)\n", float32Var)
	fmt.Printf("  float64: %.15f (more precision)\n", float64Var)
	fmt.Printf("  Scientific: Avogadro = %.2e, Planck = %.2e\n", avogadro, smallNumber)

	// -----------------------------------------------------------------
	// BOOLEAN TYPE
	// -----------------------------------------------------------------
	fmt.Println("\nBoolean Type:")

	var trueVar bool = true
	var falseVar bool = false

	// Boolean operations
	andResult := true && false // AND
	orResult := true || false  // OR
	notResult := !true         // NOT

	fmt.Printf("  true: %v, false: %v\n", trueVar, falseVar)
	fmt.Printf("  true && false = %v (AND)\n", andResult)
	fmt.Printf("  true || false = %v (OR)\n", orResult)
	fmt.Printf("  !true = %v (NOT)\n", notResult)

	// -----------------------------------------------------------------
	// STRING TYPE
	// -----------------------------------------------------------------
	fmt.Println("\nString Type:")

	// String literals
	var str1 string = "Hello, World!"
	str2 := "Go strings are UTF-8 by default"

	// Raw string literals (backticks - preserve newlines and special chars)
	rawStr := `This is a raw string literal
    It can span multiple lines
    \n and \t are not interpreted here
    Backslashes: \\ and quotes: "`

	// String concatenation
	greetingStr := "Hello" + " " + "Go" + "!"

	// String indexing (returns bytes, not characters for multi-byte UTF-8)
	firstChar := str1[0] // byte at position 0

	// String length in bytes (not characters for UTF-8)
	byteLength := len(str1)

	fmt.Printf("  Regular string: %s\n", str1)
	fmt.Printf("  Concatenated: %s\n", greetingStr)
	fmt.Printf("  First byte of \"%s\": %d (ASCII for '%c')\n", str1, firstChar, firstChar)
	fmt.Printf("  Byte length of \"%s\": %d bytes\n", str1, byteLength)
	fmt.Printf("  Raw string demo (first line): %s\n", rawStr[:30])

	// Unicode/UTF-8 string example
	unicodeStr := "Hello, 世界!" // Contains Chinese characters
	fmt.Printf("  Unicode string: %s\n", unicodeStr)
	fmt.Printf("  Byte length of \"%s\": %d bytes\n", unicodeStr, len(unicodeStr))

	// Convert string to rune slice to count characters (not bytes)
	runeCount := len([]rune(unicodeStr))
	fmt.Printf("  Character count (runes): %d characters\n", runeCount)

	fmt.Println()

	/*
	   SECTION 4: ZERO VALUES

	   In Go, every type has a zero value (default value when not initialized).
	   This ensures variables always have a valid value.
	*/

	fmt.Println("=== 6. ZERO VALUES ===")

	// Declare variables without initialization
	var zeroInt int
	var zeroFloat float64
	var zeroBool bool
	var zeroString string
	var zeroSlice []int
	var zeroMap map[string]int
	var zeroPointer *int

	fmt.Printf("Zero values for primitive types:\n")
	fmt.Printf("  int:        %d\n", zeroInt)
	fmt.Printf("  float64:    %v\n", zeroFloat)
	fmt.Printf("  bool:       %v\n", zeroBool)
	fmt.Printf("  string:     \"%s\" (empty string)\n", zeroString)
	fmt.Printf("  slice:      %v (nil)\n", zeroSlice)
	fmt.Printf("  map:        %v (nil)\n", zeroMap)
	fmt.Printf("  pointer:    %v (nil)\n", zeroPointer)

	// Check if nil
	fmt.Printf("\nChecking nil values:\n")
	fmt.Printf("  zeroSlice == nil: %v\n", zeroSlice == nil)
	fmt.Printf("  zeroMap == nil: %v\n", zeroMap == nil)
	fmt.Printf("  zeroPointer == nil: %v\n", zeroPointer == nil)

	fmt.Println()

	/*
	   SECTION 5: TYPE INFERENCE

	   Go can infer types in several contexts:
	   1. With ':=' operator
	   2. In variable declarations without explicit type
	   3. In certain expressions
	*/

	fmt.Println("=== 7. TYPE INFERENCE ===")

	// Type inference with :=
	inferredInt := 42
	inferredFloat := 3.14
	inferredString := "Hello"
	inferredBool := true

	fmt.Printf("Type inference examples:\n")
	fmt.Printf("  42        => %T\n", inferredInt)
	fmt.Printf("  3.14      => %T\n", inferredFloat)
	fmt.Printf("  \"Hello\"   => %T\n", inferredString)
	fmt.Printf("  true      => %T\n", inferredBool)

	// Type inference in expressions
	mixedType := 10 + 3.14 // int + float64 => float64
	fmt.Printf("  10 + 3.14 => %T (value: %v)\n", mixedType, mixedType)

	// Constants with type inference
	const inferredConst = 100        // Untyped constant
	var varFromConst = inferredConst // Type inferred as int

	fmt.Printf("  const c = 100; var v = c => v is %T\n", varFromConst)

	// Using reflect package to examine types
	fmt.Printf("\nUsing reflect package:\n")
	fmt.Printf("  Type of 42:        %v\n", reflect.TypeOf(42))
	fmt.Printf("  Type of 3.14:      %v\n", reflect.TypeOf(3.14))
	fmt.Printf("  Type of 'A':       %v\n", reflect.TypeOf('A')) // rune
	fmt.Printf("  Type of \"text\":    %v\n", reflect.TypeOf("text"))
	fmt.Printf("  Type of true:      %v\n", reflect.TypeOf(true))

	fmt.Println()

	/*
	   SECTION 6: TYPE CONVERSIONS (EXPLICIT)

	   Go requires EXPLICIT type conversions - no implicit conversions.
	   This prevents bugs from unexpected type promotions.

	   Syntax: T(expression) where T is the target type
	*/

	fmt.Println("=== 8. TYPE CONVERSIONS (EXPLICIT ONLY) ===")

	// -----------------------------------------------------------------
	// Numeric Conversions
	// -----------------------------------------------------------------
	fmt.Println("Numeric Conversions:")

	var intValue int = 42
	var floatValue float64 = 3.14159

	// int to float64
	intToFloat := float64(intValue)
	fmt.Printf("  float64(%d) = %.1f\n", intValue, intToFloat)

	// float64 to int (truncates decimal)
	floatToInt := int(floatValue)
	fmt.Printf("  int(%.5f) = %d (truncated)\n", floatValue, floatToInt)

	// int to int8 (possible overflow!)
	bigInt := 300
	// int8Var := int8(bigInt)  // This would compile but overflow at runtime

	// Safe conversion with overflow check
	if bigInt >= -128 && bigInt <= 127 {
		safeInt8 := int8(bigInt)
		fmt.Printf("  Safe conversion: int8(%d) = %d\n", bigInt, safeInt8)
	} else {
		fmt.Printf("  Cannot convert %d to int8 (would overflow)\n", bigInt)
	}

	// Different int types
	var i32 int32 = 100
	var i64 int64 = 200

	int32To64 := int64(i32)
	int64To32 := int32(i64)

	fmt.Printf("  int32(%d) to int64: %d\n", i32, int32To64)
	fmt.Printf("  int64(%d) to int32: %d\n", i64, int64To32)

	// -----------------------------------------------------------------
	// String Conversions
	// -----------------------------------------------------------------
	fmt.Println("\nString Conversions:")

	// Integer to string (converts to digit characters, not number as string)
	asciiChar := string(65) // ASCII 65 = 'A'
	fmt.Printf("  string(65) = \"%s\" (ASCII character 'A')\n", asciiChar)

	// Correct way: convert number to string representation
	numStr := strconv.Itoa(123) // "123"
	fmt.Printf("  strconv.Itoa(123) = \"%s\"\n", numStr)

	// String to integer
	if parsedInt, err := strconv.Atoi("456"); err == nil {
		fmt.Printf("  strconv.Atoi(\"456\") = %d\n", parsedInt)
	}

	// Float to string
	floatStr := strconv.FormatFloat(3.14159, 'f', 2, 64) // 2 decimal places
	fmt.Printf("  strconv.FormatFloat(3.14159, 'f', 2, 64) = \"%s\"\n", floatStr)

	// String to float
	if parsedFloat, err := strconv.ParseFloat("2.718", 64); err == nil {
		fmt.Printf("  strconv.ParseFloat(\"2.718\", 64) = %.3f\n", parsedFloat)
	}

	// -----------------------------------------------------------------
	// Boolean Conversions
	// -----------------------------------------------------------------
	fmt.Println("\nBoolean Conversions:")

	// String to boolean
	if boolVal, err := strconv.ParseBool("true"); err == nil {
		fmt.Printf("  strconv.ParseBool(\"true\") = %v\n", boolVal)
	}

	if boolVal, err := strconv.ParseBool("false"); err == nil {
		fmt.Printf("  strconv.ParseBool(\"false\") = %v\n", boolVal)
	}

	// Boolean to string
	boolStr := strconv.FormatBool(true)
	fmt.Printf("  strconv.FormatBool(true) = \"%s\"\n", boolStr)

	// -----------------------------------------------------------------
	// Byte/Rune Conversions
	// -----------------------------------------------------------------
	fmt.Println("\nByte/Rune Conversions:")

	// String to byte slice
	str := "Hello"
	bytes := []byte(str)
	fmt.Printf("  []byte(\"%s\") = %v (byte slice)\n", str, bytes)

	// Byte slice to string
	byteSlice := []byte{72, 101, 108, 108, 111} // "Hello" in ASCII
	backToString := string(byteSlice)
	fmt.Printf("  string([]byte{72,101,108,108,111}) = \"%s\"\n", backToString)

	// Rune conversions (for Unicode)
	runes := []rune("Hello, 世界")
	fmt.Printf("  []rune(\"Hello, 世界\") = %v (Unicode code points)\n", runes)
	fmt.Printf("  Length in runes: %d\n", len(runes))

	// -----------------------------------------------------------------
	// Practical Conversion Examples
	// -----------------------------------------------------------------
	fmt.Println("\nPractical Conversion Examples:")

	// Example 1: Safe numeric operations
	var total int = 100
	var count int = 3

	// Need float for division
	average := float64(total) / float64(count)
	fmt.Printf("  Average of %d/%d = %.2f\n", total, count, average)

	// Example 2: String building with conversions
	score := 95
	maxScore := 100
	percentage := float64(score) / float64(maxScore) * 100

	message := fmt.Sprintf("Score: %d/%d (%.1f%%)", score, maxScore, percentage)
	fmt.Printf("  %s\n", message)

	// Example 3: Type assertion vs conversion
	var interfaceValue interface{} = 42

	// Type assertion (for interfaces, not type conversion)
	if intVal, ok := interfaceValue.(int); ok {
		fmt.Printf("  Type assertion: interface{} with int value: %d\n", intVal)
	}

	fmt.Println()
	fmt.Println("=== END OF DEMONSTRATION ===")

	/*
	   KEY TAKEAWAYS:

	   1. VARIABLES:
	      - Use 'var' for package-level or zero-value declarations
	      - Use ':=' for local variables with type inference
	      - Variables must be used

	   2. CONSTANTS:
	      - Use 'const' for immutable values
	      - Use 'iota' for enumerated constants
	      - Constants are evaluated at compile time

	   3. TYPES:
	      - Go has strong, static typing
	      - Primitive types have specific sizes
	      - Zero values ensure variables are always initialized

	   4. TYPE INFERENCE:
	      - ':=' operator infers type from right-hand side
	      - Constants can be untyped
	      - Minimizes boilerplate while maintaining type safety

	   5. TYPE CONVERSIONS:
	      - ALWAYS explicit in Go (T(value))
	      - Use strconv package for string conversions
	      - Beware of overflow in numeric conversions
	      - No implicit conversions prevent bugs
	*/
}
