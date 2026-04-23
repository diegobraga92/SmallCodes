/*
    TYPESCRIPT BASIC TYPES
    Covering: Primitives, arrays, tuples, enums, any, unknown, never, void
    
    TypeScript adds static typing to JavaScript for better tooling,
    error detection, and code maintainability.
*/

console.log("=== TypeScript Basic Types ===\n");

// ============================================================================
// 1. PRIMITIVE TYPES
// ============================================================================

/*
    PRIMITIVE TYPES:
    - number: all numbers (int, float)
    - string: text
    - boolean: true/false
    - null: intentional absence
    - undefined: uninitialized
    - symbol: unique identifier
    - bigint: large integers
*/

// Number type (includes int, float, hex, binary, octal)
let age: number = 30;
let price: number = 99.99;
let hex: number = 0xf00d;
let binary: number = 0b1010;
let octal: number = 0o744;

console.log("Numbers:", { age, price, hex, binary, octal });

// String type
let firstName: string = "Alice";
let lastName: string = 'Smith';
let fullName: string = `${firstName} ${lastName}`;

console.log("Strings:", { firstName, lastName, fullName });

// Boolean type
let isActive: boolean = true;
let isCompleted: boolean = false;

console.log("Booleans:", { isActive, isCompleted });

// Null and undefined
let nothing: null = null;
let notAssigned: undefined = undefined;

// Note: With strictNullChecks, null and undefined are separate types
// let value: number = null;  // Error in strict mode
// let value: number | null = null;  // OK

// Symbol type (ES6)
let sym1: symbol = Symbol("key");
let sym2: symbol = Symbol("key");
console.log("Symbols equal?", sym1 === sym2);  // false

// BigInt type (ES2020)
let bigNumber: bigint = 9007199254740991n;
console.log("BigInt:", bigNumber + 1n);


// ============================================================================
// 2. ARRAY TYPES
// ============================================================================

/*
    ARRAY TYPES:
    - Type[] syntax (preferred)
    - Array<Type> generic syntax
    - Can specify element types
    - Readonly arrays with readonly
*/

// Array with type annotation
let numbers: number[] = [1, 2, 3, 4, 5];
let names: string[] = ["Alice", "Bob", "Carol"];

// Generic array syntax
let scores: Array<number> = [90, 85, 95];
let cities: Array<string> = ["NYC", "LA", "Chicago"];

console.log("Arrays:", { numbers, names, scores, cities });

// Mixed type array (union)
let mixed: (number | string)[] = [1, "two", 3, "four"];

// Array of objects
interface User {
    name: string;
    age: number;
}

let users: User[] = [
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 }
];

// Readonly array (immutable)
let readonlyNumbers: readonly number[] = [1, 2, 3];
// readonlyNumbers.push(4);  // Error: push doesn't exist on readonly
// readonlyNumbers[0] = 10;  // Error: can't modify

// Multi-dimensional arrays
let matrix: number[][] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];


// ============================================================================
// 3. TUPLE TYPES
// ============================================================================

/*
    TUPLE TYPES:
    - Fixed-length array with specific types at each position
    - Order matters
    - Can have optional and rest elements
*/

// Basic tuple
let tuple: [string, number] = ["Alice", 30];
console.log("Tuple:", tuple);
console.log("Name:", tuple[0], "Age:", tuple[1]);

// Tuple with optional element
let optionalTuple: [string, number?] = ["Bob"];

// Tuple with rest elements
let restTuple: [string, ...number[]] = ["Alice", 1, 2, 3, 4];

// Named tuples (TypeScript 4.0+)
let namedTuple: [name: string, age: number] = ["Alice", 30];

// Readonly tuple
let readonlyTuple: readonly [string, number] = ["Alice", 30];
// readonlyTuple[0] = "Bob";  // Error: readonly

// Tuple destructuring
let [name, userAge] = tuple;
console.log("Destructured:", { name, userAge });


// ============================================================================
// 4. ENUM TYPES
// ============================================================================

/*
    ENUM TYPES:
    - Named constants
    - Numeric (default), String, or Heterogeneous
    - Reverse mapping for numeric enums
    - Const enums for performance
*/

// Numeric enum (default starts at 0)
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right    // 3
}

let dir: Direction = Direction.Up;
console.log("Direction:", dir);  // 0
console.log("Reverse mapping:", Direction[0]);  // "Up"

// Numeric enum with custom values
enum Status {
    Active = 1,
    Inactive = 2,
    Pending = 3
}

// String enum
enum Color {
    Red = "RED",
    Green = "GREEN",
    Blue = "BLUE"
}

let color: Color = Color.Red;
console.log("Color:", color);  // "RED"

// Heterogeneous enum (not recommended)
enum Mixed {
    No = 0,
    Yes = "YES"
}

// Const enum (inlined at compile time for performance)
const enum HttpStatus {
    OK = 200,
    NotFound = 404,
    ServerError = 500
}

let status: HttpStatus = HttpStatus.OK;


// ============================================================================
// 5. ANY TYPE
// ============================================================================

/*
    ANY TYPE:
    - Opts out of type checking
    - Can assign any value
    - Can call any method
    - Use sparingly (defeats TypeScript purpose)
    - Useful for migration from JavaScript
*/

let anything: any = 42;
anything = "string";
anything = true;
anything = { key: "value" };

// Can call any method (no compile-time checking!)
anything.foo();      // No error (fails at runtime)
anything.bar.baz();  // No error (fails at runtime)

// Any array
let anyArray: any[] = [1, "two", true, { key: "value" }];

// Avoid any when possible, use unknown instead


// ============================================================================
// 6. UNKNOWN TYPE
// ============================================================================

/*
    UNKNOWN TYPE:
    - Type-safe alternative to any
    - Requires type checking before use
    - Can't access properties without narrowing
    - Preferred over any
*/

let unknownValue: unknown = 42;
unknownValue = "string";
unknownValue = true;

// Must narrow type before use
// let num: number = unknownValue;  // Error: can't assign unknown to number

// Type guard required
if (typeof unknownValue === "number") {
    let num: number = unknownValue;  // OK: narrowed to number
}

// Type assertion (use carefully!)
let str: string = unknownValue as string;

// instanceof check
class Person {
    name: string = "";
}

let unknownPerson: unknown = new Person();

if (unknownPerson instanceof Person) {
    console.log(unknownPerson.name);  // OK: narrowed to Person
}


// ============================================================================
// 7. VOID TYPE
// ============================================================================

/*
    VOID TYPE:
    - Absence of any type
    - Used for functions that don't return a value
    - Variables of type void can only be undefined or null
*/

// Function returning void
function logMessage(message: string): void {
    console.log(message);
    // No return statement
}

// Function returning void explicitly
function doNothing(): void {
    return;  // OK: return without value
    // return 42;  // Error: can't return value from void function
}

// Void variable (rarely used)
let voidValue: void = undefined;
// voidValue = null;  // Only if strictNullChecks is false


// ============================================================================
// 8. NEVER TYPE
// ============================================================================

/*
    NEVER TYPE:
    - Represents values that never occur
    - Functions that never return (throw error, infinite loop)
    - Unreachable code
    - Bottom type (assignable to everything, nothing assignable to it)
*/

// Function that never returns (throws)
function throwError(message: string): never {
    throw new Error(message);
}

// Function that never returns (infinite loop)
function infiniteLoop(): never {
    while (true) {
        // Never exits
    }
}

// Exhaustive checking with never
type Shape = Circle | Square;

interface Circle {
    kind: "circle";
    radius: number;
}

interface Square {
    kind: "square";
    sideLength: number;
}

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "square":
            return shape.sideLength ** 2;
        default:
            // This ensures all cases are handled
            const _exhaustive: never = shape;
            throw new Error(`Unhandled shape: ${_exhaustive}`);
    }
}


// ============================================================================
// 9. OBJECT TYPES
// ============================================================================

/*
    OBJECT TYPES:
    - object (lowercase): non-primitive type
    - Object (uppercase): rarely used
    - {} (empty object): any non-null value
    - Prefer interfaces or type aliases
*/

// object type (non-primitive)
let obj1: object = { key: "value" };
let obj2: object = [1, 2, 3];
let obj3: object = () => {};
// let obj4: object = 42;  // Error: number is primitive

// Object type (rarely used)
let obj5: Object = { key: "value" };
let obj6: Object = "string";  // OK but not useful

// Better: Use interfaces or type aliases
interface UserObject {
    name: string;
    age: number;
}

let user1: UserObject = { name: "Alice", age: 30 };


// ============================================================================
// 10. TYPE ASSERTIONS
// ============================================================================

/*
    TYPE ASSERTIONS:
    - Tell compiler to treat value as specific type
    - as keyword or <Type> syntax
    - No runtime checking (compile-time only)
    - Use sparingly
*/

// as keyword (preferred)
let someValue: unknown = "hello";
let strLength: number = (someValue as string).length;

// <Type> syntax (not usable in JSX)
let strLength2: number = (<string>someValue).length;

// Non-null assertion (!)
function getElement(id: string): HTMLElement | null {
    return document.getElementById(id);
}

// Tell TypeScript we're sure it's not null
let element: HTMLElement = getElement("myId")!;

// Const assertion (as const)
let obj = { x: 10, y: 20 } as const;
// obj.x = 20;  // Error: readonly

let arr = [1, 2, 3] as const;
// arr.push(4);  // Error: readonly


// ============================================================================
// 11. TYPE INFERENCE
// ============================================================================

/*
    TYPE INFERENCE:
    - TypeScript automatically infers types
    - Based on value assigned
    - Reduces need for explicit annotations
    - Best of both worlds: safety + conciseness
*/

// Inferred types
let inferredNumber = 42;           // number
let inferredString = "hello";      // string
let inferredBoolean = true;        // boolean
let inferredArray = [1, 2, 3];     // number[]
let inferredTuple = [1, "two"];    // (number | string)[]

// Function return type inferred
function add(a: number, b: number) {
    return a + b;  // return type: number (inferred)
}

// Contextual typing
window.onmousedown = function(mouseEvent) {
    // mouseEvent type inferred from context
    console.log(mouseEvent.button);
};


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

/*
    TYPE SYSTEM BEST PRACTICES:
    
    1. Enable strict mode (strict: true in tsconfig.json)
    2. Avoid any, use unknown instead
    3. Prefer interfaces for object shapes
    4. Use const assertions for literals
    5. Let TypeScript infer types when obvious
    6. Use union types over enums when possible
    7. Use readonly for immutable data
    8. Type guard before using unknown
    9. Use never for exhaustive checking
    10. Prefer named tuples for clarity
*/

// Good: Let TypeScript infer
const count = 0;  // Type inferred as 0 (literal type)

// Good: Use unknown instead of any
function processValue(value: unknown) {
    if (typeof value === "string") {
        return value.toUpperCase();
    }
    return value;
}

// Good: Readonly for immutability
interface Config {
    readonly apiUrl: string;
    readonly timeout: number;
}

const config: Config = {
    apiUrl: "https://api.example.com",
    timeout: 5000
};

// config.apiUrl = "new";  // Error: readonly

// Good: Const assertion for literals
const API_ENDPOINTS = {
    users: "/api/users",
    posts: "/api/posts"
} as const;

// API_ENDPOINTS.users = "new";  // Error: readonly


console.log("\n=== TypeScript Basic Types Complete ===");

/*
    KEY TAKEAWAYS:
    
    1. Primitives: number, string, boolean, null, undefined, symbol, bigint
    2. Arrays: Type[] or Array<Type>, readonly for immutability
    3. Tuples: Fixed-length arrays with specific types
    4. Enums: Named constants (numeric, string, const)
    5. any: Opts out of type checking (avoid)
    6. unknown: Type-safe alternative to any (prefer)
    7. void: Functions that don't return value
    8. never: Values that never occur
    9. Type assertions: as keyword or <Type> syntax
    10. Type inference: Let TypeScript infer when obvious
    11. Enable strict mode for maximum type safety
    12. Use readonly for immutable data structures
*/

// Export for use in other files
export {};
