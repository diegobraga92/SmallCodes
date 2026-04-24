/**
 * TYPESCRIPT TYPE ANNOTATIONS
 * ============================
 * Comprehensive guide to type annotations in TypeScript
 * Variables, functions, parameters, return types
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT TYPE ANNOTATIONS");
console.log("=".repeat(80));

// ============================================================================
// 1. VARIABLE TYPE ANNOTATIONS
// ============================================================================

console.log("\n=== Variable Type Annotations ===");

// Basic type annotations
let myName: string = "Alice";
let myAge: number = 30;
let isActive: boolean = true;

// Type inference (TypeScript infers the type)
let inferredString = "Hello";  // TypeScript infers: string
let inferredNumber = 42;       // TypeScript infers: number

// Explicit is better when type can't be inferred
let myVariable: string;
myVariable = "assigned later";

// Multiple types with union
let value: string | number;
value = "text";
value = 123;

// Arrays
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];
let mixed: (string | number)[] = [1, "two", 3];

console.log("Basic types:", { myName, myAge, isActive });


// ============================================================================
// 2. FUNCTION PARAMETER ANNOTATIONS
// ============================================================================

console.log("\n=== Function Parameters ===");

// Parameter type annotations
function greet(name: string): void {
    console.log(`  Hello, ${name}!`);
}

greet("Alice");
// greet(123);  // Error: Argument of type 'number' is not assignable to parameter of type 'string'

// Multiple parameters
function add(a: number, b: number): number {
    return a + b;
}

console.log("Add:", add(5, 3));

// Optional parameters
function buildName(firstName: string, lastName?: string): string {
    if (lastName) {
        return `${firstName} ${lastName}`;
    }
    return firstName;
}

console.log("Name 1:", buildName("Alice"));
console.log("Name 2:", buildName("Alice", "Smith"));

// Default parameters
function greetWithDefault(name: string = "Guest"): string {
    return `Hello, ${name}!`;
}

console.log("Default:", greetWithDefault());
console.log("With arg:", greetWithDefault("Bob"));

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((acc, n) => acc + n, 0);
}

console.log("Sum:", sum(1, 2, 3, 4, 5));


// ============================================================================
// 3. FUNCTION RETURN TYPE ANNOTATIONS
// ============================================================================

console.log("\n=== Function Return Types ===");

// Explicit return type
function multiply(a: number, b: number): number {
    return a * b;
}

// Void return type (no return value)
function logMessage(message: string): void {
    console.log(` `, message);
}

logMessage("This function returns nothing");

// Never return type (function never returns)
function throwError(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {
        // Never returns
    }
}

// Promise return type
async function fetchData(): Promise<string> {
    return "data";
}

async function fetchNumber(): Promise<number> {
    return 42;
}


// ============================================================================
// 4. FUNCTION TYPE EXPRESSIONS
// ============================================================================

console.log("\n=== Function Type Expressions ===");

// Function type annotation
let myFunc: (a: number, b: number) => number;

myFunc = (x, y) => x + y;
console.log("Function type:", myFunc(3, 4));

// Type alias for function
type MathOperation = (a: number, b: number) => number;

const subtract: MathOperation = (a, b) => a - b;
const divide: MathOperation = (a, b) => a / b;

console.log("Subtract:", subtract(10, 3));
console.log("Divide:", divide(10, 2));

// Function with callback
function processArray(
    arr: number[],
    callback: (item: number) => number
): number[] {
    return arr.map(callback);
}

const doubled = processArray([1, 2, 3], x => x * 2);
console.log("Doubled:", doubled);


// ============================================================================
// 5. OBJECT TYPE ANNOTATIONS
// ============================================================================

console.log("\n=== Object Type Annotations ===");

// Inline object type
let user: { name: string; age: number; email?: string };

user = { name: "Alice", age: 30 };
user = { name: "Bob", age: 25, email: "bob@example.com" };

// Object with methods
let calculator: {
    add: (a: number, b: number) => number;
    subtract: (a: number, b: number) => number;
};

calculator = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b
};

console.log("Calculator add:", calculator.add(5, 3));

// Readonly properties
let readonlyUser: { readonly id: number; name: string };
readonlyUser = { id: 1, name: "Alice" };
// readonlyUser.id = 2;  // Error: Cannot assign to 'id' because it is a read-only property


// ============================================================================
// 6. ARRAY AND TUPLE TYPE ANNOTATIONS
// ============================================================================

console.log("\n=== Array and Tuple Types ===");

// Array types
let numberArray: number[] = [1, 2, 3];
let stringArray: string[] = ["a", "b", "c"];
let anyArray: any[] = [1, "two", true];

// Generic array type
let genericArray: Array<number> = [1, 2, 3];

// Tuple types (fixed length, fixed types)
let tuple: [string, number];
tuple = ["Alice", 30];
// tuple = [30, "Alice"];  // Error: Type 'number' is not assignable to type 'string'

// Tuple with optional elements
let optionalTuple: [string, number?];
optionalTuple = ["Alice"];
optionalTuple = ["Alice", 30];

// Tuple with rest elements
let restTuple: [string, ...number[]];
restTuple = ["Alice", 1, 2, 3, 4];

console.log("Tuple:", tuple);


// ============================================================================
// 7. UNION AND INTERSECTION TYPES
// ============================================================================

console.log("\n=== Union and Intersection Types ===");

// Union types (OR)
function printId(id: number | string): void {
    console.log(`  Your ID is: ${id}`);
}

printId(123);
printId("ABC");

// Type narrowing with unions
function processValue(value: string | number): string {
    if (typeof value === "string") {
        return value.toUpperCase();
    } else {
        return value.toFixed(2);
    }
}

console.log("Process string:", processValue("hello"));
console.log("Process number:", processValue(3.14159));

// Intersection types (AND)
type Person = { name: string; age: number };
type Employee = { employeeId: number; department: string };

type EmployeePerson = Person & Employee;

const employee: EmployeePerson = {
    name: "Alice",
    age: 30,
    employeeId: 12345,
    department: "Engineering"
};

console.log("Employee:", employee);


// ============================================================================
// 8. LITERAL TYPES
// ============================================================================

console.log("\n=== Literal Types ===");

// String literal types
let direction: "north" | "south" | "east" | "west";
direction = "north";
// direction = "up";  // Error: Type '"up"' is not assignable to type '"north" | "south" | "east" | "west"'

// Number literal types
let diceRoll: 1 | 2 | 3 | 4 | 5 | 6;
diceRoll = 3;

// Boolean literal types (less common)
let success: true;
success = true;
// success = false;  // Error

// Combining with unions
type Result = "success" | "error" | "pending";

function getStatus(): Result {
    return "success";
}

console.log("Status:", getStatus());


// ============================================================================
// 9. TYPE ASSERTIONS
// ============================================================================

console.log("\n=== Type Assertions ===");

// as syntax (preferred)
let someValue: unknown = "this is a string";
let strLength: number = (someValue as string).length;

// Angle-bracket syntax (not available in JSX)
let anotherValue: unknown = "another string";
let anotherLength: number = (<string>anotherValue).length;

// Non-null assertion (!)
function getElementById(id: string): HTMLElement | null {
    return document.getElementById(id);
}

// Tell TypeScript we know it's not null
// const element = getElementById("myId")!;

// Const assertions
let obj = { name: "Alice" } as const;
// obj.name = "Bob";  // Error: Cannot assign to 'name' because it is a read-only property

let arr = [1, 2, 3] as const;
// arr[0] = 99;  // Error: readonly

console.log("Type assertions:", { strLength, anotherLength });


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * TYPE ANNOTATION BEST PRACTICES:
 * 
 * 1. LET TYPESCRIPT INFER WHEN OBVIOUS:
 *    // Good
 *    let x = 5;  // inferred as number
 *    
 *    // Unnecessary
 *    let x: number = 5;
 * 
 * 2. ANNOTATE WHEN TYPE ISN'T CLEAR:
 *    // Good
 *    let result: number | null;
 *    
 *    // Bad (ambiguous)
 *    let result;
 * 
 * 3. ALWAYS ANNOTATE FUNCTION PARAMETERS:
 *    // Good
 *    function greet(name: string): void { }
 *    
 *    // Bad (parameters have implicit any)
 *    function greet(name) { }
 * 
 * 4. ANNOTATE FUNCTION RETURN TYPES:
 *    // Good - explicit
 *    function add(a: number, b: number): number {
 *        return a + b;
 *    }
 *    
 *    // Acceptable - inferred correctly
 *    function add(a: number, b: number) {
 *        return a + b;  // inferred as number
 *    }
 * 
 * 5. USE READONLY WHEN APPROPRIATE:
 *    interface Config {
 *        readonly apiUrl: string;
 *        readonly timeout: number;
 *    }
 * 
 * 6. AVOID ANY WHEN POSSIBLE:
 *    // Bad
 *    let value: any;
 *    
 *    // Good
 *    let value: unknown;  // Safer alternative
 * 
 * 7. USE UNION TYPES OVER ANY:
 *    // Bad
 *    function process(value: any) { }
 *    
 *    // Good
 *    function process(value: string | number) { }
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Annotate function parameters explicitly");
console.log("2. Let TypeScript infer types when obvious");
console.log("3. Use union types for multiple possible types");
console.log("4. Optional parameters with ? syntax");
console.log("5. Readonly prevents modification");
console.log("6. Tuple types for fixed-length arrays");
console.log("7. Type assertions with 'as' keyword");
console.log("8. Avoid 'any', prefer 'unknown'");
console.log("=".repeat(80));

export {};
