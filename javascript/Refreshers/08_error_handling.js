/**
 * JAVASCRIPT ERROR HANDLING
 * ===========================
 * Comprehensive guide to error handling in JavaScript
 * Try-catch, custom errors, async errors
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT ERROR HANDLING");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. TRY-CATCH BASICS
// ============================================================================

console.log("\n=== Try-Catch Basics ===");

try {
    // Code that might throw an error
    const result = riskyOperation();
    console.log(result);
} catch (error) {
    // Handle the error
    console.log("Error caught:", error.message);
} finally {
    // Always executes (cleanup code)
    console.log("Finally block executed");
}

function riskyOperation() {
    throw new Error("Something went wrong!");
}


// ============================================================================
// 2. ERROR TYPES
// ============================================================================

console.log("\n=== Error Types ===");

// Built-in Error types
try {
    JSON.parse("invalid json");
} catch (error) {
    console.log("SyntaxError:", error.name, "-", error.message);
}

try {
    const obj = null;
    obj.property;
} catch (error) {
    console.log("TypeError:", error.name, "-", error.message);
}

try {
    nonExistentFunction();
} catch (error) {
    console.log("ReferenceError:", error.name, "-", error.message);
}

try {
    const arr = [1, 2, 3];
    arr.length = -1;
} catch (error) {
    console.log("RangeError:", error.name, "-", error.message);
}

// Error object properties
try {
    throw new Error("Test error");
} catch (error) {
    console.log("\nError properties:");
    console.log("  name:", error.name);
    console.log("  message:", error.message);
    console.log("  stack:", error.stack.split('\n')[0]);
}


// ============================================================================
// 3. CUSTOM ERRORS
// ============================================================================

console.log("\n=== Custom Errors ===");

class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

class NetworkError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.name = "NetworkError";
        this.statusCode = statusCode;
    }
}

function validateUser(user) {
    if (!user.name) {
        throw new ValidationError("Name is required");
    }
    if (!user.email) {
        throw new ValidationError("Email is required");
    }
    return true;
}

try {
    validateUser({ name: "Alice" });
} catch (error) {
    if (error instanceof ValidationError) {
        console.log("Validation failed:", error.message);
    } else {
        console.log("Unexpected error:", error);
    }
}


// ============================================================================
// 4. ERROR HANDLING IN ASYNC CODE
// ============================================================================

console.log("\n=== Async Error Handling ===");

// Promises - use .catch()
function asyncOperation() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            reject(new Error("Async error"));
        }, 100);
    });
}

asyncOperation()
    .then(result => console.log(result))
    .catch(error => console.log("Promise error:", error.message));

// Async/await - use try-catch
async function handleAsync() {
    try {
        const result = await asyncOperation();
        console.log(result);
    } catch (error) {
        console.log("Async/await error:", error.message);
    }
}

handleAsync();


// ============================================================================
// 5. ERROR HANDLING PATTERNS
// ============================================================================

console.log("\n=== Error Handling Patterns ===");

// Pattern 1: Early return
function processData(data) {
    if (!data) {
        throw new Error("Data is required");
    }
    if (typeof data !== 'object') {
        throw new Error("Data must be an object");
    }
    
    // Process data
    return data;
}

// Pattern 2: Error codes/results
function divide(a, b) {
    if (b === 0) {
        return { success: false, error: "Division by zero" };
    }
    return { success: true, value: a / b };
}

const result1 = divide(10, 2);
if (result1.success) {
    console.log("Division result:", result1.value);
} else {
    console.log("Division error:", result1.error);
}

// Pattern 3: Null/undefined returns
function findUser(id) {
    if (id < 0) return null;
    return { id, name: "User" };
}

const user = findUser(1);
if (user) {
    console.log("Found user:", user.name);
}


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Use try-catch for error handling");
console.log("2. Create custom error classes for specific cases");
console.log("3. Always handle async errors (.catch() or try-catch)");
console.log("4. Use finally for cleanup code");
console.log("5. Check error types with instanceof");
console.log("6. Provide meaningful error messages");
console.log("7. Don't catch errors you can't handle");
console.log("=".repeat(80));
