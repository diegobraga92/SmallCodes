/*
    Go Error Handling - Comprehensive Example with Detailed Comments
    
    This file demonstrates Go's error handling philosophy and patterns:
    - The error interface (Go's most important interface)
    - Creating and handling errors
    - Error wrapping for context
    - Sentinel errors and error checking
    - Panic/recover for exceptional cases
    - Best practices and common patterns
*/

package main

import (
    "errors"
    "fmt"
    "io"
    "os"
    "strconv"
    "strings"
    "time"
)

func main() {
    fmt.Println("=== GO ERROR HANDLING DEMONSTRATION ===")
    fmt.Println()

    /*
        SECTION 1: THE ERROR INTERFACE
        
        Go's error handling is based on a simple interface:
            type error interface {
                Error() string
            }
        
        Any type that implements Error() string is an error.
        Functions return errors as the last return value.
    */
    
    fmt.Println("=== 1. THE ERROR INTERFACE ===")
    
    // -----------------------------------------------------------------
    // Understanding the error interface
    // -----------------------------------------------------------------
    fmt.Println("\n1. Understanding the error Interface:")
    
    // error is a built-in interface type
    var err error // Can hold any value that implements Error() string
    
    // errors.New() returns a value that implements error interface
    err = errors.New("something went wrong")
    fmt.Printf("   Error value: %v\n", err)
    fmt.Printf("   Error string: %s\n", err.Error())
    fmt.Printf("   Type of error: %T\n", err)
    
    // Check if error is nil
    var nilErr error
    fmt.Printf("   nilErr == nil? %v\n", nilErr == nil)
    
    // -----------------------------------------------------------------
    // Custom error types
    // -----------------------------------------------------------------
    fmt.Println("\n2. Custom Error Types:")
    
    // Define a custom error type
    type ValidationError struct {
        Field   string
        Message string
        Value   interface{}
    }
    
    // Implement error interface
    func (e ValidationError) Error() string {
        return fmt.Sprintf("validation error on field '%s': %s (value: %v)", 
            e.Field, e.Message, e.Value)
    }
    
    // Create custom error
    customErr := ValidationError{
        Field:   "email",
        Message: "invalid format",
        Value:   "not-an-email",
    }
    
    fmt.Printf("   Custom error: %v\n", customErr)
    fmt.Printf("   Custom error string: %s\n", customErr.Error())
    
    // Custom errors can have additional methods
    func (e ValidationError) FieldName() string {
        return e.Field
    }
    
    fmt.Printf("   Error field name: %s\n", customErr.FieldName())
    
    fmt.Println()

    /*
        SECTION 2: CREATING ERRORS
        
        Go provides several ways to create errors.
        The most common are errors.New() and fmt.Errorf().
    */
    
    fmt.Println("=== 2. CREATING ERRORS ===")
    
    // -----------------------------------------------------------------
    // Using errors.New()
    // -----------------------------------------------------------------
    fmt.Println("\n1. Using errors.New():")
    
    // Simple, static error messages
    errNew := errors.New("file not found")
    fmt.Printf("   errors.New(\"file not found\"): %v\n", errNew)
    
    // Common pattern: package-level sentinel errors
    var (
        ErrNotFound   = errors.New("not found")
        ErrPermission = errors.New("permission denied")
        ErrTimeout    = errors.New("operation timed out")
    )
    
    fmt.Printf("   Sentinel error: %v\n", ErrNotFound)
    
    // -----------------------------------------------------------------
    // Using fmt.Errorf()
    // -----------------------------------------------------------------
    fmt.Println("\n2. Using fmt.Errorf():")
    
    // Error with dynamic content
    fileName := "config.json"
    lineNum := 42
    errFmt := fmt.Errorf("failed to parse %s at line %d", fileName, lineNum)
    fmt.Printf("   fmt.Errorf(): %v\n", errFmt)
    
    // Multiple error creation patterns in one function
    func createFile(filename string, size int) error {
        if filename == "" {
            return errors.New("filename cannot be empty")
        }
        if size < 0 {
            return fmt.Errorf("invalid size %d: must be positive", size)
        }
        if size > 1000000 {
            return fmt.Errorf("size %d too large (max: 1MB)", size)
        }
        return nil
    }
    
    // Test error creation
    err1 := createFile("", 100)
    err2 := createFile("test.txt", -50)
    err3 := createFile("large.txt", 2000000)
    
    fmt.Printf("   Empty filename: %v\n", err1)
    fmt.Printf("   Negative size: %v\n", err2)
    fmt.Printf("   Too large: %v\n", err3)
    
    // -----------------------------------------------------------------
    // Error wrapping with %w
    // -----------------------------------------------------------------
    fmt.Println("\n3. Error Wrapping with %w:")
    
    /*
        Error wrapping (introduced in Go 1.13) allows adding context 
        while preserving the original error for inspection.
        
        Use %w verb in fmt.Errorf to wrap an error.
    */
    
    func readConfigFile(path string) error {
        // Simulate a file reading error
        return fmt.Errorf("cannot read config: %w", io.EOF)
    }
    
    func loadConfiguration() error {
        err := readConfigFile("/etc/app/config.json")
        if err != nil {
            // Wrap with additional context
            return fmt.Errorf("failed to load configuration: %w", err)
        }
        return nil
    }
    
    configErr := loadConfiguration()
    fmt.Printf("   Wrapped error: %v\n", configErr)
    
    // Unwrap to get the original error
    fmt.Printf("   Unwrapped chain:\n")
    currentErr := configErr
    for i := 1; currentErr != nil; i++ {
        fmt.Printf("     Level %d: %v\n", i, currentErr)
        currentErr = errors.Unwrap(currentErr)
    }
    
    // Check for specific error in chain
    if errors.Is(configErr, io.EOF) {
        fmt.Printf("   Error chain contains io.EOF: true\n")
    }
    
    fmt.Println()

    /*
        SECTION 3: IDIOMATIC ERROR HANDLING
        
        Go's error handling philosophy:
        - Errors are values
        - Handle errors where they occur
        - Don't ignore errors
        - Return errors to caller when you can't handle them
    */
    
    fmt.Println("=== 3. IDIOMATIC ERROR HANDLING (if err != nil) ===")
    
    // -----------------------------------------------------------------
    // Basic error checking pattern
    // -----------------------------------------------------------------
    fmt.Println("\n1. Basic Error Checking Pattern:")
    
    func divide(a, b float64) (float64, error) {
        if b == 0 {
            return 0, errors.New("division by zero")
        }
        return a / b, nil
    }
    
    // The classic Go pattern
    result, err := divide(10, 2)
    if err != nil {
        fmt.Printf("   Error: %v\n", err)
    } else {
        fmt.Printf("   Result: %.2f\n", result)
    }
    
    // Error case
    result, err = divide(10, 0)
    if err != nil {
        fmt.Printf("   Expected error: %v\n", err)
    }
    
    // -----------------------------------------------------------------
    // Early return pattern
    // -----------------------------------------------------------------
    fmt.Println("\n2. Early Return Pattern (Happy Path):")
    
    func processUserData(userID string, data string) error {
        // Validate input
        if userID == "" {
            return errors.New("userID cannot be empty")
        }
        
        if data == "" {
            return errors.New("data cannot be empty")
        }
        
        // Process data
        if len(data) > 1000 {
            return fmt.Errorf("data too large: %d bytes", len(data))
        }
        
        // More processing...
        fmt.Printf("   Processing data for user %s\n", userID)
        
        return nil
    }
    
    err = processUserData("", "some data")
    if err != nil {
        fmt.Printf("   Error: %v\n", err)
    }
    
    // -----------------------------------------------------------------
    // Defer with error handling
    // -----------------------------------------------------------------
    fmt.Println("\n3. Defer with Error Handling:")
    
    func processFile(filename string) (err error) {
        // Defer for cleanup
        defer func() {
            if err != nil {
                fmt.Printf("   Cleanup after error: %v\n", err)
            }
        }()
        
        // Simulate file operations
        fmt.Printf("   Opening file: %s\n", filename)
        
        if filename == "missing.txt" {
            return fmt.Errorf("file not found: %s", filename)
        }
        
        fmt.Printf("   Processing file...\n")
        return nil
    }
    
    processFile("data.txt")
    processFile("missing.txt")
    
    // -----------------------------------------------------------------
    // Error handling in loops
    // -----------------------------------------------------------------
    fmt.Println("\n4. Error Handling in Loops:")
    
    func processItems(items []string) error {
        for i, item := range items {
            if item == "" {
                // Continue or break based on requirements
                return fmt.Errorf("empty item at index %d", i)
            }
            fmt.Printf("   Processing item %d: %s\n", i, item)
        }
        return nil
    }
    
    items := []string{"apple", "", "cherry"}
    err = processItems(items)
    if err != nil {
        fmt.Printf("   Loop error: %v\n", err)
    }
    
    // -----------------------------------------------------------------
    // Multiple error checks
    // -----------------------------------------------------------------
    fmt.Println("\n5. Multiple Sequential Operations:")
    
    func multiStepOperation() error {
        // Step 1
        if err := step1(); err != nil {
            return fmt.Errorf("step 1 failed: %w", err)
        }
        
        // Step 2
        if err := step2(); err != nil {
            return fmt.Errorf("step 2 failed: %w", err)
        }
        
        // Step 3
        if err := step3(); err != nil {
            return fmt.Errorf("step 3 failed: %w", err)
        }
        
        return nil
    }
    
    err = multiStepOperation()
    if err != nil {
        fmt.Printf("   Multi-step error: %v\n", err)
    }
    
    fmt.Println()

    /*
        SECTION 4: ERROR WRAPPING AND INSPECTION
        
        Go 1.13 introduced error wrapping and inspection utilities.
    */
    
    fmt.Println("=== 4. ERROR WRAPPING AND INSPECTION ===")
    
    // -----------------------------------------------------------------
    // Error wrapping with context
    // -----------------------------------------------------------------
    fmt.Println("\n1. Adding Context with Wrapping:")
    
    func connectToDatabase(host string, port int) error {
        if host == "" {
            return errors.New("host cannot be empty")
        }
        
        // Simulate connection error
        return fmt.Errorf("connection failed: host=%s, port=%d", host, port)
    }
    
    func initializeDatabase() error {
        err := connectToDatabase("localhost", 5432)
        if err != nil {
            // Wrap with additional context
            return fmt.Errorf("database initialization failed: %w", err)
        }
        return nil
    }
    
    func startApplication() error {
        err := initializeDatabase()
        if err != nil {
            // Wrap again
            return fmt.Errorf("application startup failed: %w", err)
        }
        return nil
    }
    
    appErr := startApplication()
    fmt.Printf("   Full error chain: %v\n", appErr)
    
    // -----------------------------------------------------------------
    // Unwrapping errors
    // -----------------------------------------------------------------
    fmt.Println("\n2. Unwrapping Errors:")
    
    // Manual unwrapping
    unwrapped := errors.Unwrap(appErr)
    fmt.Printf("   First unwrap: %v\n", unwrapped)
    
    unwrapped = errors.Unwrap(unwrapped)
    fmt.Printf("   Second unwrap: %v\n", unwrapped)
    
    // Full unwrap loop
    fmt.Println("\n   Complete unwrap chain:")
    currentErr = appErr
    for i := 1; currentErr != nil; i++ {
        indent := strings.Repeat("  ", i)
        fmt.Printf("%s%s\n", indent, currentErr)
        currentErr = errors.Unwrap(currentErr)
    }
    
    // -----------------------------------------------------------------
    // Checking error types with errors.Is()
    // -----------------------------------------------------------------
    fmt.Println("\n3. Checking Errors with errors.Is():")
    
    // Define sentinel errors
    var (
        ErrNetwork  = errors.New("network error")
        ErrAuth     = errors.New("authentication failed")
        ErrDatabase = errors.New("database error")
    )
    
    func makeRequest() error {
        // Simulate nested errors
        return fmt.Errorf("request failed: %w", 
            fmt.Errorf("connection lost: %w", ErrNetwork))
    }
    
    requestErr := makeRequest()
    
    // Check if error chain contains ErrNetwork
    if errors.Is(requestErr, ErrNetwork) {
        fmt.Printf("   Error is a network error\n")
    }
    
    // Check for specific error
    if errors.Is(requestErr, io.EOF) {
        fmt.Printf("   Error is EOF\n")
    } else {
        fmt.Printf("   Error is NOT EOF\n")
    }
    
    // -----------------------------------------------------------------
    // Type assertions with errors.As()
    // -----------------------------------------------------------------
    fmt.Println("\n4. Type Assertions with errors.As():")
    
    // Define custom error type
    type APIError struct {
        StatusCode int
        Message    string
        URL        string
    }
    
    func (e APIError) Error() string {
        return fmt.Sprintf("API error %d: %s (%s)", e.StatusCode, e.Message, e.URL)
    }
    
    func callAPI() error {
        // Simulate API error
        return fmt.Errorf("API call failed: %w", 
            APIError{StatusCode: 404, Message: "Not Found", URL: "/api/users"})
    }
    
    apiErr := callAPI()
    
    // Extract APIError from chain
    var apiError APIError
    if errors.As(apiErr, &apiError) {
        fmt.Printf("   Found APIError: Status=%d, URL=%s\n", 
            apiError.StatusCode, apiError.URL)
    }
    
    // Try with different type
    var validationErr ValidationError
    if errors.As(apiErr, &validationErr) {
        fmt.Printf("   Found ValidationError\n")
    } else {
        fmt.Printf("   No ValidationError in chain\n")
    }
    
    fmt.Println()

    /*
        SECTION 5: SENTINEL ERRORS
        
        Sentinel errors are predefined error values that can be compared
        using == operator or errors.Is().
    */
    
    fmt.Println("=== 5. SENTINEL ERRORS ===")
    
    // -----------------------------------------------------------------
    // Package-level sentinel errors
    // -----------------------------------------------------------------
    fmt.Println("\n1. Package-Level Sentinel Errors:")
    
    // Common pattern: export errors as package variables
    var (
        ErrUserNotFound    = errors.New("user not found")
        ErrInvalidPassword = errors.New("invalid password")
        ErrUserBanned      = errors.New("user is banned")
    )
    
    func authenticate(username, password string) error {
        if username != "admin" {
            return ErrUserNotFound
        }
        if password != "secret" {
            return ErrInvalidPassword
        }
        // Check if user is banned
        return nil
    }
    
    // Test authentication
    authErr := authenticate("user", "wrong")
    if authErr == ErrUserNotFound {
        fmt.Printf("   User not found\n")
    } else if authErr == ErrInvalidPassword {
        fmt.Printf("   Invalid password\n")
    }
    
    authErr = authenticate("admin", "wrong")
    if errors.Is(authErr, ErrInvalidPassword) {
        fmt.Printf("   Invalid password (using errors.Is)\n")
    }
    
    // -----------------------------------------------------------------
    // Sentinel errors with wrapping
    // -----------------------------------------------------------------
    fmt.Println("\n2. Sentinel Errors with Wrapping:")
    
    func getUserProfile(userID string) error {
        if userID == "999" {
            // Wrap sentinel error
            return fmt.Errorf("failed to get profile for %s: %w", 
                userID, ErrUserNotFound)
        }
        return nil
    }
    
    profileErr := getUserProfile("999")
    
    // Still works with errors.Is even when wrapped
    if errors.Is(profileErr, ErrUserNotFound) {
        fmt.Printf("   User not found (even when wrapped)\n")
    }
    
    fmt.Printf("   Full error: %v\n", profileErr)
    
    // -----------------------------------------------------------------
    // When to use sentinel errors
    // -----------------------------------------------------------------
    fmt.Println("\n3. When to Use Sentinel Errors:")
    
    fmt.Println("   Use sentinel errors when:")
    fmt.Println("   - Error is expected and should be handled specifically")
    fmt.Println("   - Error is part of your API contract")
    fmt.Println("   - Caller needs to check for specific error conditions")
    
    fmt.Println("\n   Example from standard library:")
    fmt.Println("   - io.EOF")
    fmt.Println("   - os.ErrNotExist")
    fmt.Println("   - os.ErrPermission")
    
    // Demonstrate with io.EOF
    fmt.Println("\n4. Example: Handling io.EOF:")
    
    func readStream() error {
        // Simulate reading until EOF
        return fmt.Errorf("read completed: %w", io.EOF)
    }
    
    streamErr := readStream()
    if errors.Is(streamErr, io.EOF) {
        fmt.Printf("   Reached end of stream (normal condition)\n")
    }
    
    fmt.Println()

    /*
        SECTION 6: PANIC, RECOVER AND DEFER
        
        Panic is for unrecoverable errors.
        Recover can catch panics in deferred functions.
        Use sparingly - prefer returning errors.
    */
    
    fmt.Println("=== 6. PANIC, RECOVER AND DEFER ===")
    
    // -----------------------------------------------------------------
    // Basic panic
    // -----------------------------------------------------------------
    fmt.Println("\n1. Basic Panic (commented out to keep program running):")
    
    // Uncomment to see panic
    /*
    func willPanic() {
        panic("something went terribly wrong")
    }
    */
    
    fmt.Println("   (Panic demonstration commented out)")
    
    // -----------------------------------------------------------------
    // Panic with recover
    // -----------------------------------------------------------------
    fmt.Println("\n2. Recovering from Panic:")
    
    func safeOperation() (err error) {
        // Defer with recover
        defer func() {
            if r := recover(); r != nil {
                // Convert panic to error
                err = fmt.Errorf("recovered from panic: %v", r)
                fmt.Printf("   Recovered in safeOperation: %v\n", r)
            }
        }()
        
        // This might panic
        riskyOperation()
        
        return nil
    }
    
    func riskyOperation() {
        // Simulate panic condition
        panic("risky operation failed")
    }
    
    // This won't crash the program
    err = safeOperation()
    if err != nil {
        fmt.Printf("   Operation failed: %v\n", err)
    }
    
    // -----------------------------------------------------------------
    // Nested panic and recover
    // -----------------------------------------------------------------
    fmt.Println("\n3. Nested Recover:")
    
    func outerFunction() {
        defer func() {
            if r := recover(); r != nil {
                fmt.Printf("   Outer recover: %v\n", r)
            }
        }()
        
        fmt.Println("   Starting outer function")
        innerFunction()
        fmt.Println("   Outer function completed (should not reach here)")
    }
    
    func innerFunction() {
        defer func() {
            fmt.Println("   Inner defer executing")
        }()
        
        panic("panic from inner function")
    }
    
    fmt.Println("   Calling outerFunction():")
    outerFunction()
    fmt.Println("   Program continues after recover")
    
    // -----------------------------------------------------------------
    // Re-panicking
    // -----------------------------------------------------------------
    fmt.Println("\n4. Re-panicking:")
    
    func handlePanic() {
        defer func() {
            if r := recover(); r != nil {
                fmt.Printf("   Caught panic: %v\n", r)
                // Re-panic after logging
                panic(fmt.Sprintf("re-panicking: %v", r))
            }
        }()
        
        panic("original panic")
    }
    
    // Uncomment to see re-panic
    /*
    func mainCaller() {
        defer func() {
            if r := recover(); r != nil {
                fmt.Printf("   Main recover: %v\n", r)
            }
        }()
        
        handlePanic()
    }
    
    mainCaller()
    */
    
    // -----------------------------------------------------------------
    // When to use panic/recover
    // -----------------------------------------------------------------
    fmt.Println("\n5. When to Use Panic/Recover:")
    
    fmt.Println("   Use panic for:")
    fmt.Println("   - Programming errors (bugs)")
    fmt.Println("   - Unrecoverable situations")
    fmt.Println("   - Initialization failures")
    
    fmt.Println("\n   Use recover for:")
    fmt.Println("   - Preventing crash in long-running servers")
    fmt.Println("   - Graceful shutdown on unrecoverable errors")
    fmt.Println("   - Converting panics to errors at API boundaries")
    
    // Practical example: HTTP server panic recovery
    fmt.Println("\n6. Practical Example: HTTP Handler Recovery:")
    
    func panicRecoveryHandler(handler func()) (err error) {
        defer func() {
            if r := recover(); r != nil {
                err = fmt.Errorf("handler panicked: %v", r)
            }
        }()
        
        handler()
        return nil
    }
    
    handler := func() {
        panic("handler panic")
    }
    
    err = panicRecoveryHandler(handler)
    if err != nil {
        fmt.Printf("   Handler error: %v\n", err)
    }
    
    fmt.Println()

    /*
        SECTION 7: ERROR BEST PRACTICES AND PATTERNS
    */
    
    fmt.Println("=== 7. ERROR BEST PRACTICES AND PATTERNS ===")
    
    // -----------------------------------------------------------------
    // Always handle errors
    // -----------------------------------------------------------------
    fmt.Println("\n1. Never Ignore Errors:")
    
    func badPattern() {
        // BAD: Ignoring error
        // fmt.Sprintf() // No error, but imagine it had one
        // os.Open("file.txt") // Error ignored!
    }
    
    func goodPattern() error {
        // GOOD: Check error
        file, err := os.Open("file.txt")
        if err != nil {
            return fmt.Errorf("failed to open file: %w", err)
        }
        defer file.Close()
        
        // Use file...
        return nil
    }
    
    fmt.Println("   Always check errors immediately")
    
    // -----------------------------------------------------------------
    // Add context when returning errors
    // -----------------------------------------------------------------
    fmt.Println("\n2. Add Context to Errors:")
    
    func readUserData(userID string) ([]byte, error) {
        filename := fmt.Sprintf("%s.json", userID)
        data, err := os.ReadFile(filename)
        if err != nil {
            // Add context about what we were trying to do
            return nil, fmt.Errorf("failed to read user data for %s: %w", 
                userID, err)
        }
        return data, nil
    }
    
    // -----------------------------------------------------------------
    // Use meaningful error messages
    // -----------------------------------------------------------------
    fmt.Println("\n3. Use Meaningful Error Messages:")
    
    // BAD: Vague error
    // return errors.New("error")
    
    // GOOD: Specific error
    // return fmt.Errorf("failed to parse JSON config: invalid character at position %d", pos)
    
    // EVEN BETTER: Include relevant values
    func validateAge(age int) error {
        if age < 0 {
            return fmt.Errorf("invalid age %d: must be non-negative", age)
        }
        if age > 150 {
            return fmt.Errorf("invalid age %d: maximum is 150", age)
        }
        return nil
    }
    
    fmt.Printf("   Good error: %v\n", validateAge(-5))
    fmt.Printf("   Good error: %v\n", validateAge(200))
    
    // -----------------------------------------------------------------
    // Create custom error types for complex errors
    // -----------------------------------------------------------------
    fmt.Println("\n4. Custom Error Types for Complex Cases:")
    
    type HTTPError struct {
        StatusCode int
        URL        string
        Method     string
        Err        error
    }
    
    func (e HTTPError) Error() string {
        return fmt.Sprintf("%s %s: %d %v", e.Method, e.URL, e.StatusCode, e.Err)
    }
    
    func (e HTTPError) Unwrap() error {
        return e.Err
    }
    
    // Create HTTP error
    httpErr := HTTPError{
        StatusCode: 500,
        URL:        "/api/users",
        Method:     "GET",
        Err:        errors.New("internal server error"),
    }
    
    fmt.Printf("   HTTP error: %v\n", httpErr)
    
    // -----------------------------------------------------------------
    // Error aggregation
    // -----------------------------------------------------------------
    fmt.Println("\n5. Error Aggregation:")
    
    type MultiError struct {
        Errors []error
    }
    
    func (e MultiError) Error() string {
        var msgs []string
        for _, err := range e.Errors {
            msgs = append(msgs, err.Error())
        }
        return strings.Join(msgs, "; ")
    }
    
    func validateUser(user map[string]string) error {
        var errs []error
        
        if name, ok := user["name"]; !ok || name == "" {
            errs = append(errs, errors.New("name is required"))
        }
        
        if email, ok := user["email"]; ok && !strings.Contains(email, "@") {
            errs = append(errs, fmt.Errorf("invalid email: %s", email))
        }
        
        if ageStr, ok := user["age"]; ok {
            if age, err := strconv.Atoi(ageStr); err != nil || age < 0 {
                errs = append(errs, fmt.Errorf("invalid age: %s", ageStr))
            }
        }
        
        if len(errs) > 0 {
            return MultiError{Errors: errs}
        }
        return nil
    }
    
    invalidUser := map[string]string{
        "name":  "",
        "email": "not-an-email",
        "age":   "-5",
    }
    
    validationErr := validateUser(invalidUser)
    if validationErr != nil {
        fmt.Printf("   Validation errors: %v\n", validationErr)
        
        // Check if it's a MultiError
        if multiErr, ok := validationErr.(MultiError); ok {
            fmt.Printf("   Number of errors: %d\n", len(multiErr.Errors))
        }
    }
    
    // -----------------------------------------------------------------
    // Logging vs returning errors
    // -----------------------------------------------------------------
    fmt.Println("\n6. Logging vs Returning Errors:")
    
    fmt.Println("   Rule of thumb:")
    fmt.Println("   - Log errors at the level where they're handled")
    fmt.Println("   - Return errors to the caller when you can't handle them")
    fmt.Println("   - Don't both log and return the same error (creates noise)")
    
    func processRequest() error {
        err := doSomething()
        if err != nil {
            // Log at the point of handling
            fmt.Printf("   [LOG] Failed to process request: %v\n", err)
            // Don't return the same error - we handled it
            return nil
        }
        return nil
    }
    
    func doSomething() error {
        return errors.New("something failed")
    }
    
    processRequest()
    
    // -----------------------------------------------------------------
    // Testing error conditions
    // -----------------------------------------------------------------
    fmt.Println("\n7. Testing Error Conditions:")
    
    fmt.Println("   Test helpers for errors:")
    
    func assertError(t testingT, err error, expected string) {
        if err == nil || err.Error() != expected {
            t.Errorf("expected error %q, got %v", expected, err)
        }
    }
    
    func assertNoError(t testingT, err error) {
        if err != nil {
            t.Errorf("unexpected error: %v", err)
        }
    }
    
    // Mock testing interface
    type testingT struct{}
    func (t testingT) Errorf(format string, args ...interface{}) {
        fmt.Printf("   TEST FAIL: "+format+"\n", args...)
    }
    
    var t testingT
    
    // Test error case
    err = validateAge(-1)
    assertError(t, err, "invalid age -1: must be non-negative")
    
    // Test success case
    err = validateAge(25)
    assertNoError(t, err)
    
    fmt.Println()
    fmt.Println("=== END OF ERROR HANDLING DEMONSTRATION ===")
    
    /*
        KEY TAKEAWAYS:
        
        1. ERROR INTERFACE:
           - error is just an interface: Error() string
           - Any type can be an error by implementing this method
        
        2. CREATING ERRORS:
           - errors.New() for simple static errors
           - fmt.Errorf() for formatted errors
           - Use %w for error wrapping (Go 1.13+)
        
        3. IDIOMATIC HANDLING:
           - if err != nil pattern
           - Handle errors where they occur
           - Return errors when you can't handle them
           - Don't ignore errors
        
        4. ERROR WRAPPING:
           - Add context with fmt.Errorf("... %w", err)
           - Use errors.Is() to check for specific errors in chain
           - Use errors.As() to extract error types from chain
        
        5. SENTINEL ERRORS:
           - Predefined error values for specific conditions
           - Check with == or errors.Is()
           - Useful for API contracts
        
        6. PANIC/RECOVER:
           - Panic for unrecoverable errors
           - Recover in deferred functions
           - Use sparingly - prefer error returns
           - Convert panics to errors at boundaries
        
        7. BEST PRACTICES:
           - Add context to errors
           - Create custom error types for complex cases
           - Never ignore errors
           - Test error conditions
           - Log at point of handling, not at every level
    */
}

// Helper functions for demonstration

func step1() error {
    return nil
}

func step2() error {
    return errors.New("step2 failed")
}

func step3() error {
    return nil
}

/*
    COMMON PATTERNS:
    
    1. Error Chaining:
        func topLevel() error {
            err := middleLevel()
            if err != nil {
                return fmt.Errorf("top level failed: %w", err)
            }
            return nil
        }
    
    2. Error Aggregation:
        type MultiError []error
        // Aggregate multiple errors
    
    3. Retry Pattern:
        func withRetry(attempts int, fn func() error) error {
            for i := 0; i < attempts; i++ {
                err := fn()
                if err == nil {
                    return nil
                }
                // Check if error is retryable
                if !isRetryable(err) {
                    return err
                }
                time.Sleep(backoff(i))
            }
            return fmt.Errorf("failed after %d attempts", attempts)
        }
    
    4. Error Classification:
        func classifyError(err error) string {
            if errors.Is(err, io.EOF) {
                return "end_of_stream"
            }
            if errors.Is(err, os.ErrNotExist) {
                return "not_found"
            }
            return "unknown"
        }
    
    5. Temporary Errors:
        type temporary interface {
            Temporary() bool
        }
        
        func isTemporary(err error) bool {
            if te, ok := err.(temporary); ok {
                return te.Temporary()
            }
            return false
        }
*/