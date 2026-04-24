/**
 * TYPESCRIPT BEST PRACTICES
 * ==========================
 * Coding standards, patterns, common pitfalls, and idiomatic TypeScript
 * Senior-level practices for writing maintainable TypeScript
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT BEST PRACTICES");
console.log("=".repeat(80));

// ============================================================================
// 1. ENABLE STRICT MODE
// ============================================================================

console.log("\n=== Strict Mode ===");

/**
 * ALWAYS enable strict mode in tsconfig.json
 * {
 *   "compilerOptions": {
 *     "strict": true
 *   }
 * }
 * 
 * This enables:
 * - noImplicitAny
 * - strictNullChecks
 * - strictFunctionTypes
 * - strictBindCallApply
 * - strictPropertyInitialization
 * - noImplicitThis
 * - alwaysStrict
 */

// BAD: Implicit any
function badAdd(a, b) {  // a, b are any
    return a + b;
}

// GOOD: Explicit types
function goodAdd(a: number, b: number): number {
    return a + b;
}

console.log("Always enable strict mode");


// ============================================================================
// 2. AVOID 'ANY' TYPE
// ============================================================================

console.log("\n=== Avoid 'any' ===");

/**
 * 'any' disables type checking
 * Use alternatives instead
 */

// BAD: Using any
function badProcess(data: any) {
    return data.value.toString();  // No type safety
}

// GOOD: Use unknown and narrow
function goodProcess(data: unknown): string {
    if (typeof data === "object" && data !== null && "value" in data) {
        const obj = data as { value: unknown };
        if (typeof obj.value === "number" || typeof obj.value === "string") {
            return obj.value.toString();
        }
    }
    throw new Error("Invalid data");
}

// GOOD: Use specific types
interface DataWithValue {
    value: string | number;
}

function betterProcess(data: DataWithValue): string {
    return data.value.toString();
}

console.log("Avoid any, use unknown or specific types");


// ============================================================================
// 3. INTERFACES VS TYPES
// ============================================================================

console.log("\n=== Interfaces vs Types ===");

/**
 * INTERFACE: For object shapes, public APIs, can be extended
 * TYPE: For unions, intersections, tuples, primitives
 */

// GOOD: Interface for object shapes
interface User {
    id: number;
    name: string;
    email: string;
}

// GOOD: Type for unions
type Status = "active" | "inactive" | "pending";

// GOOD: Type for complex unions
type Result<T> = 
    | { success: true; data: T }
    | { success: false; error: string };

// GOOD: Type for intersections
type WithTimestamps = { createdAt: Date; updatedAt: Date };
type UserWithTimestamps = User & WithTimestamps;

// GOOD: Interface for extensibility
interface Animal {
    name: string;
}

interface Dog extends Animal {
    breed: string;
}

console.log("Interfaces for objects, types for unions");


// ============================================================================
// 4. TYPE INFERENCE
// ============================================================================

console.log("\n=== Type Inference ===");

/**
 * Let TypeScript infer when obvious
 * Explicit types for function parameters and return types
 */

// GOOD: Let TypeScript infer
const numbers = [1, 2, 3, 4, 5];  // number[]
const user = { name: "Alice", age: 30 };  // { name: string; age: number }

// BAD: Redundant type annotation
const redundant: number[] = [1, 2, 3];  // Obvious from right side

// GOOD: Explicit function signatures
function calculateTotal(items: number[]): number {
    return items.reduce((sum, item) => sum + item, 0);
}

// GOOD: Explicit when needed
const userId: string | number = getUserId();  // Ambiguous without annotation

declare function getUserId(): string | number;

console.log("Infer when obvious, explicit for clarity");


// ============================================================================
// 5. READONLY AND IMMUTABILITY
// ============================================================================

console.log("\n=== Readonly and Immutability ===");

/**
 * Use readonly for immutability
 * Prevents accidental modifications
 */

// GOOD: Readonly properties
interface Config {
    readonly apiUrl: string;
    readonly timeout: number;
}

// GOOD: Readonly arrays
function processItems(items: readonly number[]): number {
    // items.push(1);  // Error: Cannot push to readonly array
    return items.reduce((sum, item) => sum + item, 0);
}

// GOOD: Readonly tuples
type Point = readonly [number, number];

// GOOD: Const assertions
const routes = {
    home: "/",
    about: "/about",
    contact: "/contact"
} as const;

// routes is readonly, values are literal types
type Route = typeof routes[keyof typeof routes];  // "/" | "/about" | "/contact"

console.log("Use readonly for immutability");


// ============================================================================
// 6. DISCRIMINATED UNIONS
// ============================================================================

console.log("\n=== Discriminated Unions ===");

/**
 * Discriminated unions better than optional properties
 * Type-safe state management
 */

// BAD: Optional properties
interface BadState {
    loading?: boolean;
    data?: string;
    error?: string;
}

// Can have invalid states: { loading: true, data: "value", error: "error" }

// GOOD: Discriminated union
type GoodState = 
    | { status: "loading" }
    | { status: "success"; data: string }
    | { status: "error"; error: string };

function handleState(state: GoodState): void {
    switch (state.status) {
        case "loading":
            console.log("  Loading...");
            break;
        case "success":
            console.log("  Data:", state.data);
            break;
        case "error":
            console.log("  Error:", state.error);
            break;
    }
}

handleState({ status: "loading" });
handleState({ status: "success", data: "result" });

console.log("Use discriminated unions for states");


// ============================================================================
// 7. GENERICS FOR REUSABILITY
// ============================================================================

console.log("\n=== Generics ===");

/**
 * Use generics for type-safe, reusable code
 */

// GOOD: Generic function
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const person = { name: "Alice", age: 30 };
const name = getProperty(person, "name");  // Type: string
const age = getProperty(person, "age");    // Type: number

// GOOD: Generic class
class Cache<T> {
    private data = new Map<string, T>();
    
    set(key: string, value: T): void {
        this.data.set(key, value);
    }
    
    get(key: string): T | undefined {
        return this.data.get(key);
    }
}

const stringCache = new Cache<string>();
stringCache.set("key", "value");

// GOOD: Generic constraints
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

console.log("Use generics for type-safe reusability");


// ============================================================================
// 8. NEVER USE @ts-ignore
// ============================================================================

console.log("\n=== Don't Ignore Errors ===");

/**
 * Fix errors instead of suppressing them
 * If necessary, use @ts-expect-error with comment
 */

// BAD: Hiding errors
// @ts-ignore
const result = dangerousOperation();

// GOOD: Fix the issue
declare function dangerousOperation(): unknown;
const result2 = dangerousOperation();
if (typeof result2 === "string") {
    console.log("  Result:", result2);
}

// ACCEPTABLE: Temporary with explanation
// @ts-expect-error - TODO: Fix after library update
const temporaryFix = oldLibraryFunction();

declare function oldLibraryFunction(): any;

console.log("Fix errors, don't suppress them");


// ============================================================================
// 9. UTILITY TYPES
// ============================================================================

console.log("\n=== Utility Types ===");

/**
 * Use built-in utility types
 * Don't reinvent the wheel
 */

interface Product {
    id: number;
    name: string;
    price: number;
    description: string;
}

// GOOD: Use Partial for optional updates
function updateProduct(id: number, updates: Partial<Product>): void {
    console.log("  Updating product", id, "with", updates);
}

updateProduct(1, { price: 99.99 });  // Only price needed

// GOOD: Use Pick for subsets
type ProductSummary = Pick<Product, "id" | "name">;

// GOOD: Use Omit to exclude properties
type ProductWithoutId = Omit<Product, "id">;

// GOOD: Use Required for all required
type RequiredProduct = Required<Partial<Product>>;

// GOOD: Use Readonly
type ImmutableProduct = Readonly<Product>;

console.log("Leverage utility types");


// ============================================================================
// 10. ORGANIZE TYPES
// ============================================================================

console.log("\n=== Organize Types ===");

/**
 * Organize types logically
 * Separate type files for large projects
 */

// GOOD: types/user.ts
export interface User {
    id: string;
    name: string;
    email: string;
}

export type UserId = string;

export interface UserCredentials {
    email: string;
    password: string;
}

// GOOD: types/product.ts
export interface Product2 {
    id: string;
    name: string;
    price: number;
}

// GOOD: types/index.ts (barrel export)
// export * from './user';
// export * from './product';

console.log("Organize types in separate files");


// ============================================================================
// 11. FUNCTION OVERLOADS
// ============================================================================

console.log("\n=== Function Overloads ===");

/**
 * Use function overloads for different call signatures
 */

// GOOD: Function overloads
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;
function format(value: string | number | Date): string {
    if (typeof value === "string") {
        return value.toUpperCase();
    } else if (typeof value === "number") {
        return value.toFixed(2);
    } else {
        return value.toISOString();
    }
}

console.log("String:", format("hello"));
console.log("Number:", format(42.5));
console.log("Date:", format(new Date()));


// ============================================================================
// 12. AVOID ENUMS (PREFER UNION TYPES)
// ============================================================================

console.log("\n=== Enums vs Union Types ===");

/**
 * Union types are more flexible and tree-shakeable
 */

// OKAY: Enum
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT"
}

// BETTER: Union type with const object
const DIRECTION = {
    Up: "UP",
    Down: "DOWN",
    Left: "LEFT",
    Right: "RIGHT"
} as const;

type Direction2 = typeof DIRECTION[keyof typeof DIRECTION];

function move(direction: Direction2): void {
    console.log("  Moving:", direction);
}

move(DIRECTION.Up);

console.log("Prefer union types over enums");


// ============================================================================
// 13. NAMING CONVENTIONS
// ============================================================================

console.log("\n=== Naming Conventions ===");

/**
 * Consistent naming conventions
 */

// GOOD: PascalCase for types, interfaces, classes
interface UserAccount {}
type AccountStatus = "active" | "suspended";
class DatabaseConnection {}

// GOOD: camelCase for variables, functions
const userName = "Alice";
function getUserById(id: string) {}

// GOOD: UPPER_SNAKE_CASE for constants
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = "https://api.example.com";

// GOOD: Prefix interfaces with 'I' only if needed
// Prefer: interface User {} (no prefix)
// Sometimes: interface IUser {} (when conflicting with class)

// GOOD: Generic type parameters
// Single letter for simple: <T>, <K, V>
// Descriptive for complex: <TData, TError>

console.log("Follow naming conventions");


// ============================================================================
// 14. ERROR HANDLING
// ============================================================================

console.log("\n=== Error Handling ===");

/**
 * Type-safe error handling
 */

// GOOD: Custom error types
class ValidationError extends Error {
    constructor(public field: string, message: string) {
        super(message);
        this.name = "ValidationError";
    }
}

class NotFoundError extends Error {
    constructor(public resource: string, public id: string) {
        super(`${resource} with id ${id} not found`);
        this.name = "NotFoundError";
    }
}

// GOOD: Result type pattern
type Result<T, E = Error> = 
    | { ok: true; value: T }
    | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
    if (b === 0) {
        return { ok: false, error: "Division by zero" };
    }
    return { ok: true, value: a / b };
}

const divResult = divide(10, 2);
if (divResult.ok) {
    console.log("Result:", divResult.value);
} else {
    console.log("Error:", divResult.error);
}

console.log("Type-safe error handling");


// ============================================================================
// 15. ASYNC/AWAIT PATTERNS
// ============================================================================

console.log("\n=== Async/Await Patterns ===");

/**
 * Type-safe async code
 */

// GOOD: Explicit Promise return type
async function fetchUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
}

// GOOD: Error handling
async function fetchUserSafe(id: string): Promise<Result<User, Error>> {
    try {
        const user = await fetchUser(id);
        return { ok: true, value: user };
    } catch (error) {
        return { ok: false, error: error as Error };
    }
}

// GOOD: Parallel requests
async function fetchMultipleUsers(ids: string[]): Promise<User[]> {
    const promises = ids.map(id => fetchUser(id));
    return Promise.all(promises);
}

console.log("Type-safe async/await");


// ============================================================================
// 16. COMMON PITFALLS TO AVOID
// ============================================================================

console.log("\n=== Common Pitfalls ===");

/**
 * Common TypeScript mistakes
 */

// PITFALL 1: Type assertions without checking
// BAD
const element = document.getElementById("myId") as HTMLButtonElement;
// element.click();  // Might fail if not a button

// GOOD
const element2 = document.getElementById("myId");
if (element2 instanceof HTMLButtonElement) {
    element2.click();
}

// PITFALL 2: Ignoring null/undefined
// BAD
function badLength(str?: string): number {
    return str.length;  // Error if str is undefined
}

// GOOD
function goodLength(str?: string): number {
    return str?.length ?? 0;
}

// PITFALL 3: Modifying readonly arrays
// BAD
function badSort(arr: readonly number[]): number[] {
    // arr.sort();  // Error: Cannot modify readonly array
    return arr.slice().sort();  // Good: Create copy first
}

// PITFALL 4: Not narrowing unknown
// BAD
function badParse(data: unknown) {
    return data.value;  // Error: data is unknown
}

// GOOD
function goodParse(data: unknown) {
    if (typeof data === "object" && data !== null && "value" in data) {
        return (data as { value: unknown }).value;
    }
}

console.log("Avoid common pitfalls");


// ============================================================================
// 17. TESTING PATTERNS
// ============================================================================

console.log("\n=== Testing Patterns ===");

/**
 * Type-safe testing
 */

// GOOD: Type test functions
type Expect<T extends true> = T;
type Equal<X, Y> = 
    (<T>() => T extends X ? 1 : 2) extends
    (<T>() => T extends Y ? 1 : 2) ? true : false;

// Test utility types
type Test1 = Expect<Equal<Pick<User, "name">, { name: string }>>;

// GOOD: Mock with correct types
interface ApiClient {
    getUser(id: string): Promise<User>;
}

const mockApiClient: ApiClient = {
    getUser: async (id: string) => ({ id: "1", name: "Mock User", email: "mock@example.com" })
};

console.log("Type-safe testing");


// ============================================================================
// 18. BEST PRACTICES SUMMARY
// ============================================================================

/**
 * TYPESCRIPT BEST PRACTICES SUMMARY:
 * 
 * 1. ENABLE STRICT MODE
 *    Always use "strict": true
 * 
 * 2. AVOID ANY
 *    Use unknown, specific types, or generics
 * 
 * 3. INTERFACES VS TYPES
 *    Interfaces for objects, types for unions
 * 
 * 4. TYPE INFERENCE
 *    Infer when obvious, explicit for signatures
 * 
 * 5. READONLY
 *    Immutability prevents bugs
 * 
 * 6. DISCRIMINATED UNIONS
 *    Better than optional properties
 * 
 * 7. GENERICS
 *    Reusable, type-safe code
 * 
 * 8. DON'T IGNORE ERRORS
 *    Fix issues, don't suppress
 * 
 * 9. UTILITY TYPES
 *    Leverage built-in types
 * 
 * 10. ORGANIZE TYPES
 *     Separate files, logical grouping
 * 
 * 11. NAMING CONVENTIONS
 *     Consistent naming
 * 
 * 12. ERROR HANDLING
 *     Type-safe errors
 * 
 * 13. AVOID ENUMS
 *     Prefer union types
 * 
 * 14. TEST YOUR TYPES
 *     Verify type behavior
 * 
 * 15. DOCUMENT COMPLEX TYPES
 *     JSDoc comments
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Enable strict mode always");
console.log("2. Avoid any - use unknown or specific types");
console.log("3. Interfaces for objects, types for unions");
console.log("4. Infer types when obvious");
console.log("5. Use readonly for immutability");
console.log("6. Discriminated unions > optional properties");
console.log("7. Leverage generics for reusability");
console.log("8. Never ignore TypeScript errors");
console.log("9. Use utility types (Partial, Pick, Omit)");
console.log("10. Organize types, follow conventions, test thoroughly");
console.log("=".repeat(80));

export {};
