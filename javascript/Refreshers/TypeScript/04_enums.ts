/**
 * TYPESCRIPT ENUMS
 * =================
 * Numeric enums, string enums, const enums, computed enums
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT ENUMS");
console.log("=".repeat(80));

// ============================================================================
// 1. NUMERIC ENUMS
// ============================================================================

enum Direction {
    Up = 1,
    Down,
    Left,
    Right
}

console.log("Direction.Up:", Direction.Up);      // 1
console.log("Direction.Down:", Direction.Down);  // 2

// ============================================================================
// 2. STRING ENUMS
// ============================================================================

enum Status {
    Pending = "PENDING",
    InProgress = "IN_PROGRESS",
    Completed = "COMPLETED",
    Failed = "FAILED"
}

console.log("Status:", Status.Pending);

// ============================================================================
// 3. CONST ENUMS (compile-time only)
// ============================================================================

const enum LogLevel {
    Debug = 0,
    Info = 1,
    Warning = 2,
    Error = 3
}

// Inlined at compile time - more efficient
const level = LogLevel.Error;

// ============================================================================
// 4. HETEROGENEOUS ENUMS (mixed types - not recommended)
// ============================================================================

enum Mixed {
    No = 0,
    Yes = "YES"
}

// ============================================================================
// 5. REVERSE MAPPINGS (numeric enums only)
// ============================================================================

enum Color {
    Red = 1,
    Green,
    Blue
}

const colorName = Color[2];  // "Green"
console.log("Color name:", colorName);

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/**
 * 1. Numeric enums auto-increment
 * 2. String enums require explicit values
 * 3. Const enums are inlined (better performance)
 * 4. Reverse mapping available for numeric enums
 * 5. Prefer string enums for clarity
 * 6. Use const enums when possible for performance
 */

export {};
