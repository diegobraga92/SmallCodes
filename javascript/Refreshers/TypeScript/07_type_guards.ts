/**
 * TYPESCRIPT TYPE GUARDS AND NARROWING
 * ======================================
 * typeof, instanceof, custom type guards, discriminated unions
 * Type narrowing techniques for safer code
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT TYPE GUARDS AND NARROWING");
console.log("=".repeat(80));

// ============================================================================
// 1. TYPEOF TYPE GUARDS
// ============================================================================

console.log("\n=== typeof Type Guards ===");

/**
 * typeof operator narrows type based on JavaScript type check
 * Works for: string, number, boolean, symbol, undefined, object, function
 */

function processValue(value: string | number): string {
    if (typeof value === "string") {
        // TypeScript knows value is string here
        return value.toUpperCase();
    } else {
        // TypeScript knows value is number here
        return value.toFixed(2);
    }
}

console.log("String:", processValue("hello"));
console.log("Number:", processValue(3.14159));

// Multiple type checks
function describe(value: string | number | boolean): string {
    if (typeof value === "string") {
        return `String: ${value.length} characters`;
    } else if (typeof value === "number") {
        return `Number: ${value.toFixed(2)}`;
    } else {
        return `Boolean: ${value}`;
    }
}

console.log(describe("test"));
console.log(describe(42));
console.log(describe(true));


// ============================================================================
// 2. INSTANCEOF TYPE GUARDS
// ============================================================================

console.log("\n=== instanceof Type Guards ===");

/**
 * instanceof checks if object is instance of class
 */

class Dog {
    bark(): void {
        console.log("  Woof!");
    }
}

class Cat {
    meow(): void {
        console.log("  Meow!");
    }
}

function makeSound(animal: Dog | Cat): void {
    if (animal instanceof Dog) {
        // TypeScript knows animal is Dog
        animal.bark();
    } else {
        // TypeScript knows animal is Cat
        animal.meow();
    }
}

makeSound(new Dog());
makeSound(new Cat());

// With Error handling
function handleError(error: Error | string): void {
    if (error instanceof Error) {
        console.log("  Error:", error.message);
        console.log("  Stack:", error.stack?.split('\n')[0]);
    } else {
        console.log("  String error:", error);
    }
}

handleError(new Error("Something went wrong"));
handleError("Simple error message");


// ============================================================================
// 3. CUSTOM TYPE GUARDS (TYPE PREDICATES)
// ============================================================================

console.log("\n=== Custom Type Guards ===");

/**
 * Custom type guards use 'is' keyword: parameterName is Type
 * Return boolean, TypeScript narrows type based on result
 */

interface Fish {
    swim(): void;
}

interface Bird {
    fly(): void;
}

// Type predicate function
function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}

function movePet(pet: Fish | Bird): void {
    if (isFish(pet)) {
        // TypeScript knows pet is Fish
        pet.swim();
    } else {
        // TypeScript knows pet is Bird
        pet.fly();
    }
}

const fish: Fish = { swim: () => console.log("  Swimming...") };
const bird: Bird = { fly: () => console.log("  Flying...") };

movePet(fish);
movePet(bird);

// Type guard for null/undefined
function isDefined<T>(value: T | null | undefined): value is T {
    return value !== null && value !== undefined;
}

const maybeNumber: number | null = Math.random() > 0.5 ? 42 : null;

if (isDefined(maybeNumber)) {
    // TypeScript knows maybeNumber is number
    console.log("Defined:", maybeNumber.toFixed(2));
}

// Array filter with type guard
const mixed: (string | number)[] = [1, "two", 3, "four", 5];

function isString(value: string | number): value is string {
    return typeof value === "string";
}

const strings: string[] = mixed.filter(isString);  // Type is string[]
console.log("Strings only:", strings);


// ============================================================================
// 4. IN OPERATOR NARROWING
// ============================================================================

console.log("\n=== 'in' Operator ===");

/**
 * 'in' operator checks if property exists in object
 */

interface Car {
    drive(): void;
    wheels: number;
}

interface Boat {
    sail(): void;
    hull: string;
}

function operate(vehicle: Car | Boat): void {
    if ("drive" in vehicle) {
        // TypeScript knows vehicle is Car
        console.log(`  Car with ${vehicle.wheels} wheels`);
        vehicle.drive();
    } else {
        // TypeScript knows vehicle is Boat
        console.log(`  Boat with ${vehicle.hull} hull`);
        vehicle.sail();
    }
}

const car: Car = { drive: () => console.log("    Driving..."), wheels: 4 };
const boat: Boat = { sail: () => console.log("    Sailing..."), hull: "aluminum" };

operate(car);
operate(boat);


// ============================================================================
// 5. DISCRIMINATED UNIONS (TAGGED UNIONS)
// ============================================================================

console.log("\n=== Discriminated Unions ===");

/**
 * Discriminated union = union type with common literal property
 * Common property (discriminant) used to narrow type
 */

interface Success {
    kind: "success";  // Discriminant
    data: string;
}

interface Error {
    kind: "error";  // Discriminant
    message: string;
}

interface Loading {
    kind: "loading";  // Discriminant
}

type Result = Success | Error | Loading;

function handleResult(result: Result): void {
    // TypeScript narrows based on 'kind'
    switch (result.kind) {
        case "success":
            console.log("  Success:", result.data);
            break;
        case "error":
            console.log("  Error:", result.message);
            break;
        case "loading":
            console.log("  Loading...");
            break;
        default:
            // Exhaustiveness check
            const _exhaustive: never = result;
            return _exhaustive;
    }
}

handleResult({ kind: "success", data: "User loaded" });
handleResult({ kind: "error", message: "Network error" });
handleResult({ kind: "loading" });

// Practical example: API response types
interface ApiSuccess<T> {
    status: "success";
    data: T;
}

interface ApiError {
    status: "error";
    error: string;
    code: number;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

function processApiResponse<T>(response: ApiResponse<T>): void {
    if (response.status === "success") {
        console.log("  Data:", response.data);
    } else {
        console.log("  Error:", response.error, `(${response.code})`);
    }
}


// ============================================================================
// 6. TRUTHINESS NARROWING
// ============================================================================

console.log("\n=== Truthiness Narrowing ===");

/**
 * TypeScript narrows types based on truthiness checks
 */

function printLength(str: string | null | undefined): void {
    if (str) {
        // TypeScript knows str is string (not null/undefined)
        console.log("  Length:", str.length);
    } else {
        console.log("  No string provided");
    }
}

printLength("hello");
printLength(null);

// Filtering out null/undefined from arrays
function processItems(items: (string | null)[]): void {
    // Filter with type guard
    const validItems: string[] = items.filter((item): item is string => {
        return item !== null;
    });
    
    console.log("  Valid items:", validItems);
}

processItems(["a", null, "b", "c", null]);


// ============================================================================
// 7. EQUALITY NARROWING
// ============================================================================

console.log("\n=== Equality Narrowing ===");

/**
 * === and !== comparisons narrow types
 */

function example(x: string | number, y: string | boolean): void {
    if (x === y) {
        // Both must be string (only common type)
        console.log("  Both strings:", x.toUpperCase(), y.toUpperCase());
    } else {
        console.log("  Different types:", x, y);
    }
}

example("hello", "world");
example(42, true);


// ============================================================================
// 8. ASSERTION FUNCTIONS
// ============================================================================

console.log("\n=== Assertion Functions ===");

/**
 * Assertion functions use 'asserts' keyword
 * Throw error if condition false, narrow type if true
 */

function assert(condition: boolean, message?: string): asserts condition {
    if (!condition) {
        throw new Error(message || "Assertion failed");
    }
}

function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== "string") {
        throw new Error("Value is not a string");
    }
}

function processUnknown(value: unknown): void {
    assertIsString(value);
    // After assertion, TypeScript knows value is string
    console.log("  Uppercase:", value.toUpperCase());
}

try {
    processUnknown("hello");
    processUnknown(123);  // Will throw
} catch (e) {
    console.log("  Caught error:", (e as Error).message);
}


// ============================================================================
// 9. NEVER TYPE FOR EXHAUSTIVENESS
// ============================================================================

console.log("\n=== Exhaustiveness Checking ===");

/**
 * never type ensures all cases are handled
 */

type Shape = 
    | { kind: "circle"; radius: number }
    | { kind: "square"; size: number }
    | { kind: "rectangle"; width: number; height: number };

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "square":
            return shape.size ** 2;
        case "rectangle":
            return shape.width * shape.height;
        default:
            // If we add a new shape type and forget to handle it,
            // TypeScript will error here
            const _exhaustive: never = shape;
            throw new Error(`Unhandled shape: ${_exhaustive}`);
    }
}

const circle: Shape = { kind: "circle", radius: 5 };
console.log("Circle area:", getArea(circle).toFixed(2));


// ============================================================================
// 10. CONTROL FLOW ANALYSIS
// ============================================================================

console.log("\n=== Control Flow Analysis ===");

/**
 * TypeScript tracks type through control flow
 */

function example2(x: string | number | null): void {
    // x is string | number | null
    
    if (x === null) {
        // x is null
        console.log("  Null");
        return;
    }
    
    // x is string | number (null eliminated)
    
    if (typeof x === "string") {
        // x is string
        console.log("  String:", x.toUpperCase());
        return;
    }
    
    // x is number (string eliminated)
    console.log("  Number:", x.toFixed(2));
}

example2(null);
example2("hello");
example2(42);


// ============================================================================
// 11. BEST PRACTICES
// ============================================================================

/**
 * TYPE GUARD BEST PRACTICES:
 * 
 * 1. PREFER DISCRIMINATED UNIONS
 *    Cleaner than multiple type guards
 * 
 * 2. USE TYPEOF FOR PRIMITIVES
 *    Simple and fast
 * 
 * 3. USE INSTANCEOF FOR CLASSES
 *    Works with inheritance
 * 
 * 4. CUSTOM TYPE GUARDS FOR INTERFACES
 *    Can't use instanceof with interfaces
 * 
 * 5. ASSERTION FUNCTIONS FOR VALIDATION
 *    Throw early if invalid
 * 
 * 6. EXHAUSTIVENESS CHECKS WITH NEVER
 *    Catch unhandled cases at compile time
 * 
 * 7. AVOID TYPE ASSERTIONS
 *    Use type guards instead of 'as'
 * 
 * 8. KEEP TYPE GUARDS SIMPLE
 *    Complex logic makes types harder to track
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. typeof for primitive type checks");
console.log("2. instanceof for class instance checks");
console.log("3. Custom type guards with 'is' keyword");
console.log("4. 'in' operator for property existence");
console.log("5. Discriminated unions with literal types");
console.log("6. Assertion functions with 'asserts'");
console.log("7. never type for exhaustiveness checking");
console.log("8. Control flow analysis tracks types");
console.log("9. Truthiness narrowing removes null/undefined");
console.log("10. Type guards make code safer and clearer");
console.log("=".repeat(80));

export {};
