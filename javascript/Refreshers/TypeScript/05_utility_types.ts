/**
 * TYPESCRIPT UTILITY TYPES
 * =========================
 * Comprehensive guide to built-in utility types
 * Partial, Required, Readonly, Pick, Omit, Record, and more
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT UTILITY TYPES");
console.log("=".repeat(80));

interface Todo {
    title: string;
    description: string;
    completed: boolean;
    createdAt: Date;
}

// ============================================================================
// 1. PARTIAL<T> - All properties optional
// ============================================================================

type PartialTodo = Partial<Todo>;
const todo1: PartialTodo = { title: "Learn TypeScript" };

// ============================================================================
// 2. REQUIRED<T> - All properties required
// ============================================================================

type RequiredTodo = Required<PartialTodo>;

// ============================================================================
// 3. READONLY<T> - All properties readonly
// ============================================================================

type ReadonlyTodo = Readonly<Todo>;
const todo2: ReadonlyTodo = {
    title: "Test",
    description: "Desc",
    completed: false,
    createdAt: new Date()
};
// todo2.title = "New";  // Error: readonly

// ============================================================================
// 4. RECORD<K, T> - Object type with keys K and values T
// ============================================================================

type TodoMap = Record<string, Todo>;
const todos: TodoMap = {
    "1": { title: "Task 1", description: "Desc", completed: false, createdAt: new Date() },
    "2": { title: "Task 2", description: "Desc", completed: true, createdAt: new Date() }
};

// ============================================================================
// 5. PICK<T, K> - Select properties from T
// ============================================================================

type TodoPreview = Pick<Todo, "title" | "completed">;
const preview: TodoPreview = { title: "Task", completed: false };

// ============================================================================
// 6. OMIT<T, K> - Remove properties from T
// ============================================================================

type TodoWithoutDates = Omit<Todo, "createdAt">;

// ============================================================================
// 7. EXCLUDE<T, U> - Exclude types from union
// ============================================================================

type T0 = Exclude<"a" | "b" | "c", "a">;  // "b" | "c"
type T1 = Exclude<string | number | boolean, boolean>;  // string | number

// ============================================================================
// 8. EXTRACT<T, U> - Extract types from union
// ============================================================================

type T2 = Extract<"a" | "b" | "c", "a" | "f">;  // "a"
type T3 = Extract<string | number | boolean, boolean>;  // boolean

// ============================================================================
// 9. NONNULLABLE<T> - Exclude null and undefined
// ============================================================================

type T4 = NonNullable<string | number | null | undefined>;  // string | number

// ============================================================================
// 10. RETURNTYPE<T> - Get function return type
// ============================================================================

function getTodo(): Todo {
    return { title: "Test", description: "Desc", completed: false, createdAt: new Date() };
}

type TodoReturnType = ReturnType<typeof getTodo>;  // Todo

// ============================================================================
// 11. PARAMETERS<T> - Get function parameter types as tuple
// ============================================================================

function createTodo(title: string, description: string): Todo {
    return { title, description, completed: false, createdAt: new Date() };
}

type CreateTodoParams = Parameters<typeof createTodo>;  // [string, string]

// ============================================================================
// 12. AWAITED<T> - Get type from Promise
// ============================================================================

type T5 = Awaited<Promise<string>>;  // string
type T6 = Awaited<Promise<Promise<number>>>;  // number

// ============================================================================
// KEY TAKEAWAYS
// ============================================================================

/**
 * UTILITY TYPE CHEAT SHEET:
 * 
 * Partial<T> - Make all properties optional
 * Required<T> - Make all properties required
 * Readonly<T> - Make all properties readonly
 * Record<K, T> - Object with keys K and values T
 * Pick<T, K> - Select specific properties
 * Omit<T, K> - Remove specific properties
 * Exclude<T, U> - Remove types from union
 * Extract<T, U> - Select types from union
 * NonNullable<T> - Remove null/undefined
 * ReturnType<T> - Get function return type
 * Parameters<T> - Get function parameters
 * Awaited<T> - Unwrap Promise type
 */

export {};
