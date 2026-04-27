/**
 * TYPESCRIPT ADVANCED TYPES
 * ==========================
 * Mapped types, conditional types, template literal types, infer keyword
 * Advanced type manipulation and type-level programming
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT ADVANCED TYPES");
console.log("=".repeat(80));

// ============================================================================
// 1. MAPPED TYPES
// ============================================================================

console.log("\n=== Mapped Types ===");

/**
 * MAPPED TYPES EXPLAINED:
 * =======================
 * 
 * Mapped types create new types by transforming properties of existing types.
 * They're TypeScript's way of applying transformations to type shapes.
 * 
 * SYNTAX BREAKDOWN:
 * type NewType<T> = { [P in keyof T]: TransformedType };
 * 
 * - [P in keyof T]: Iterates over each property name in T
 * - P: Property name (like a loop variable)
 * - keyof T: Gets all property names from T as a union
 * - TransformedType: New type for each property
 * 
 * MODIFIERS:
 * - ?: Makes property optional
 * - -?: Removes optional modifier (makes required)
 * - readonly: Makes property readonly
 * - -readonly: Removes readonly modifier (makes mutable)
 * 
 * WHEN TO USE:
 * ✓ Creating variations of existing types (readonly, optional, etc.)
 * ✓ Transforming API responses to client models
 * ✓ Building utility types
 * ✓ Type-safe property manipulation
 * 
 * WHEN NOT TO USE:
 * ✗ Simple property selection (use Pick/Omit instead)
 * ✗ When you need runtime logic (mapped types are compile-time only)
 * 
 * PERFORMANCE:
 * - Compile-time only (no runtime cost)
 * - Can slow compilation for very large types
 * - TypeScript compiler caches mapped types
 */

// Make all properties optional
type MyPartial<T> = {
    // [P in keyof T]: Iterate over each property name P in type T
    // ?: Add optional modifier to each property
    // T[P]: Keep the original property type
    [P in keyof T]?: T[P];
};

interface User {
    id: number;
    name: string;
    email: string;
}

type PartialUser = MyPartial<User>;
// Result: { id?: number; name?: string; email?: string; }
// EACH PROPERTY is now optional (can be present or undefined)

// Make all properties readonly
type MyReadonly<T> = {
    // readonly: Add readonly modifier to each property
    // Properties can only be set during initialization, not modified later
    readonly [P in keyof T]: T[P];
};

type ReadonlyUser = MyReadonly<User>;
// Result: { readonly id: number; readonly name: string; readonly email: string; }
// IMMUTABLE: Cannot change properties after creation

// Make all properties required
type MyRequired<T> = {
    // -?: Remove optional modifier from each property
    // This is the OPPOSITE of adding ?, it removes existing ?
    // Useful when starting with a type that has optional properties
    [P in keyof T]-?: T[P];
};
// USE CASE: Converting optional API response to required internal type

// Make all properties mutable (remove readonly)
type Mutable<T> = {
    // -readonly: Remove readonly modifier from each property
    // Allows modification of previously readonly properties
    // Useful when you need to modify immutable data structures
    -readonly [P in keyof T]: T[P];
};
// USE CASE: Creating draft versions of readonly types for editing

// Example usage
const user1: PartialUser = { name: "Alice" };  // OK - all optional
// We can omit id and email because ALL properties are optional

const user2: ReadonlyUser = { id: 1, name: "Bob", email: "bob@example.com" };
// user2.name = "Changed";  // Error: Cannot assign to 'name' because it is a read-only property
// TypeScript PREVENTS mutation at compile time

console.log("Mapped types:", { user1, user2 });

/**
 * KEY INSIGHTS:
 * 
 * 1. MAPPED TYPES ARE TRANSFORMATIONS:
 *    They don't copy types, they create NEW types by applying rules
 * 
 * 2. MODIFIERS CAN BE ADDED OR REMOVED:
 *    +? (add optional), -? (remove optional)
 *    +readonly (add readonly), -readonly (remove readonly)
 * 
 * 3. THEY'RE COMPOSABLE:
 *    type ReadonlyPartial<T> = Readonly<Partial<T>>;
 * 
 * 4. COMMON PATTERN:
 *    Most built-in utility types (Partial, Required, Readonly, Pick, Omit)
 *    are implemented using mapped types!
 */


// ============================================================================
// 2. MAPPED TYPES WITH TRANSFORMATIONS
// ============================================================================

console.log("\n=== Mapped Type Transformations ===");

/**
 * KEY REMAPPING (TypeScript 4.1+):
 * =================================
 * 
 * Syntax: [P in keyof T as NewKeyType]: ValueType
 * 
 * The "as" clause allows you to:
 * - Rename properties
 * - Filter properties (using never)
 * - Transform property names
 * - Combine with template literal types
 * 
 * POWERFUL PATTERN:
 * You can compute NEW property names from OLD property names
 * This enables advanced type transformations like:
 * - Adding prefixes/suffixes
 * - Converting naming conventions
 * - Filtering by property type
 * - Creating derived types
 */

// Add 'get' prefix to all properties
type Getters<T> = {
    // KEY REMAPPING BREAKDOWN:
    // 1. [P in keyof T]: Iterate over property names
    // 2. as `get${Capitalize<string & P>}`: REMAP each key
    //    - `get${...}` : Template literal type for string manipulation
    //    - Capitalize<...>: Built-in utility to capitalize first letter
    //    - string & P: Ensure P is treated as string (intersection)
    // 3. () => T[P]: Transform to getter function type
    [P in keyof T as `get${Capitalize<string & P>}`]: () => T[P];
};

interface Person {
    name: string;
    age: number;
}

type PersonGetters = Getters<Person>;
// Result: { getName: () => string; getAge: () => number; }
// PROPERTIES ARE RENAMED: 'name' → 'getName', 'age' → 'getAge'
// TYPES ARE TRANSFORMED: T[P] → () => T[P] (value → getter function)

// Filter properties by type
type StringProperties<T> = {
    // CONDITIONAL KEY REMAPPING (filtering):
    // 1. T[P] extends string: Check if property type is string
    // 2. ? P : never: If yes, keep property name; if no, use 'never'
    // 3. never keys are EXCLUDED from the resulting type
    // 
    // This is TYPE-LEVEL FILTERING - removes properties at compile time
    [P in keyof T as T[P] extends string ? P : never]: T[P];
};

interface Mixed {
    name: string;
    age: number;
    email: string;
    active: boolean;
}

type OnlyStrings = StringProperties<Mixed>;
// Result: { name: string; email: string; }
// 'age' (number) and 'active' (boolean) are FILTERED OUT
// Only string properties remain

// Exclude certain properties
type OmitType<T, K extends keyof T> = {
    // PROPERTY EXCLUSION PATTERN:
    // 1. P extends K: Check if current property is in exclusion list K
    // 2. ? never : P: If yes, exclude (never); if no, keep property name
    // 
    // This is how Omit<T, K> utility type is implemented internally!
    [P in keyof T as P extends K ? never : P]: T[P];
};

type UserWithoutId = OmitType<User, "id">;
// Result: { name: string; email: string; }
// 'id' property is REMOVED from the type

/**
 * KEY REMAPPING PATTERNS:
 * 
 * 1. RENAME PATTERN:
 *    [P in keyof T as `prefix_${P}`]: T[P]
 * 
 * 2. FILTER PATTERN:
 *    [P in keyof T as Condition ? P : never]: T[P]
 * 
 * 3. TRANSFORM PATTERN:
 *    [P in keyof T as TransformKey<P>]: TransformValue<T[P]>
 * 
 * 4. COMBINE PATTERN:
 *    Can combine filtering + renaming + type transformation
 * 
 * COMMON USE CASES:
 * - API response → Client model transformation
 * - Database column names → TypeScript property names
 * - Event handlers (on + EventName pattern)
 * - Getters/setters generation
 * - Form validation schemas
 */


// ============================================================================
// 3. CONDITIONAL TYPES
// ============================================================================

console.log("\n=== Conditional Types ===");

/**
 * CONDITIONAL TYPES EXPLAINED:
 * ============================
 * 
 * Syntax: T extends U ? X : Y
 * 
 * Like a ternary operator, but for TYPES:
 * - If type T is assignable to type U, result is X
 * - Otherwise, result is Y
 * 
 * KEY CONCEPTS:
 * 
 * 1. "extends" MEANS "is assignable to":
 *    - string extends string → true
 *    - "hello" extends string → true (literal extends base)
 *    - string extends "hello" → false (base does NOT extend literal)
 *    - number extends string → false (incompatible types)
 * 
 * 2. DISTRIBUTIVE CONDITIONAL TYPES:
 *    When T is a UNION type, TypeScript distributes the check:
 *    
 *    type Test<T> = T extends string ? true : false;
 *    type Result = Test<string | number>;
 *    
 *    TypeScript DISTRIBUTES:
 *    = (string extends string ? true : false) | (number extends string ? true : false)
 *    = true | false
 *    
 *    This behavior is POWERFUL but can be surprising!
 * 
 * 3. NON-DISTRIBUTIVE (wrapped in tuple):
 *    type Test<T> = [T] extends [string] ? true : false;
 *    type Result = Test<string | number>;  // false
 *    
 *    [string | number] extends [string] → false (union doesn't extend)
 * 
 * WHEN TO USE:
 * ✓ Type-level branching logic
 * ✓ Filtering union types
 * ✓ Extracting types from complex structures
 * ✓ Creating flexible utility types
 * 
 * COMMON PATTERNS:
 * - Exclude<T, U>: Remove types from union
 * - Extract<T, U>: Keep only matching types
 * - NonNullable<T>: Remove null/undefined
 * - ReturnType<T>: Extract function return type
 */

// Check if type is string
type IsString<T> = T extends string ? true : false;

// SIMPLE CHECKS:
type Test1 = IsString<string>;   // true (string extends string)
type Test2 = IsString<number>;   // false (number does NOT extend string)

// DISTRIBUTIVE BEHAVIOR WITH UNIONS:
type Test3 = IsString<string | number>;
// TypeScript distributes the conditional:
// = IsString<string> | IsString<number>
// = true | false
// = boolean (union of true and false)

// WHY DISTRIBUTIVE? Because T is a "naked type parameter"
// (not wrapped in array, tuple, or other type constructor)

// Check if type is array
type IsArray<T> = T extends any[] ? true : false;

type Test3 = IsArray<string[]>;  // true
type Test4 = IsArray<string>;    // false

// Extract type from array
type ArrayElement<T> = T extends (infer U)[] ? U : T;

type StringFromArray = ArrayElement<string[]>;  // string
type NumberFromArray = ArrayElement<number[]>;  // number
type NotAnArray = ArrayElement<boolean>;        // boolean

// Conditional based on property
type HasId<T> = T extends { id: any } ? true : false;

type Test5 = HasId<{ id: number; name: string }>;  // true
type Test6 = HasId<{ name: string }>;              // false


// ============================================================================
// 4. DISTRIBUTIVE CONDITIONAL TYPES
// ============================================================================

console.log("\n=== Distributive Conditional Types ===");

/**
 * When conditional type is applied to union type,
 * it distributes over union members
 */

type ToArray<T> = T extends any ? T[] : never;

type StringOrNumber = string | number;
type DistributedArray = ToArray<StringOrNumber>;
// Distributes to: string[] | number[]

// Extract types from union
type ExtractString<T> = T extends string ? T : never;

type OnlyStrings2 = ExtractString<string | number | boolean>;
// Result: string

// Remove null and undefined
type NonNullable<T> = T extends null | undefined ? never : T;

type Test7 = NonNullable<string | null | undefined>;  // string


// ============================================================================
// 5. INFER KEYWORD
// ============================================================================

console.log("\n=== Infer Keyword ===");

/**
 * INFER KEYWORD EXPLAINED:
 * ========================
 * 
 * The "infer" keyword allows you to DECLARE a type variable within
 * a conditional type's extends clause, then use it in the true branch.
 * 
 * SYNTAX:
 * type MyType<T> = T extends SomePattern<infer U> ? U : never;
 *                                        ^^^^^^^     ^
 *                                        declare    use
 * 
 * HOW IT WORKS:
 * 1. TypeScript tries to match T against the pattern
 * 2. If it matches, it INFERS what U must be
 * 3. U becomes available in the true branch
 * 4. If no match, falls to false branch
 * 
 * THINK OF IT AS:
 * "If T matches this pattern, figure out what the unknown type U is,
 * then give me U"
 * 
 * COMMON PATTERNS:
 * 
 * 1. EXTRACT RETURN TYPE:
 *    T extends (...args: any[]) => infer R
 *    Match: function signature
 *    Infer: what the function returns (R)
 * 
 * 2. EXTRACT PARAMETERS:
 *    T extends (...args: infer P) => any
 *    Match: function signature
 *    Infer: what the parameters are (P as tuple)
 * 
 * 3. EXTRACT ARRAY ELEMENT:
 *    T extends (infer U)[]
 *    Match: array type
 *    Infer: what the element type is (U)
 * 
 * 4. EXTRACT PROMISE VALUE:
 *    T extends Promise<infer U>
 *    Match: Promise type
 *    Infer: what the Promise resolves to (U)
 * 
 * WHY SO POWERFUL?
 * - Extracts nested types without explicit type parameters
 * - Enables generic type introspection
 * - Foundation for many built-in utility types
 */

// Extract return type from function
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
//                                                   ^^^^^^^ 
//                                                   "If T is a function,
//                                                   infer its return type as R"

function getString(): string {
    return "hello";
}

function getNumber(): number {
    return 42;
}

type StringReturn = MyReturnType<typeof getString>;  // string
// TypeScript matches: (...args: any[]) => string
// Infers: R = string
// Returns: string

type NumberReturn = MyReturnType<typeof getNumber>;  // number
// TypeScript matches: (...args: any[]) => number
// Infers: R = number
// Returns: number

// Extract parameters from function
type MyParameters<T> = T extends (...args: infer P) => any ? P : never;
//                                        ^^^^^^^ 
//                                        "Infer the parameters tuple as P"

function add(a: number, b: number): number {
    return a + b;
}

type AddParams = MyParameters<typeof add>;  // [number, number]
// TypeScript matches: (a: number, b: number) => number
// Infers: P = [number, number] (as tuple!)
// Returns: [number, number]

// Extract array element type
type Unpacked<T> = 
    // Try first pattern: is it an array?
    T extends (infer U)[] ? U : 
    // Try second pattern: is it a Promise?
    T extends Promise<infer U> ? U : 
    // No match: return T unchanged
    T;

type Test8 = Unpacked<string[]>;          // string
// Matches first: string[] = (infer U)[]
// Infers: U = string
// Returns: string

type Test9 = Unpacked<Promise<number>>;   // number
// First fails, second matches: Promise<infer U>
// Infers: U = number
// Returns: number

type Test10 = Unpacked<boolean>;          // boolean
// Neither pattern matches
// Returns: T unchanged = boolean

/**
 * ADVANCED INFER PATTERNS:
 * 
 * 1. NESTED INFER:
 *    T extends Promise<infer U>[] ? U : never
 *    Extract: Array of Promises → what each Promise resolves to
 * 
 * 2. MULTIPLE INFER:
 *    T extends (a: infer A, b: infer B) => infer R ? [A, B, R] : never
 *    Extract: Multiple parts of function signature
 * 
 * 3. RECURSIVE INFER:
 *    type Flatten<T> = T extends (infer U)[] ? Flatten<U> : T
 *    Recursively unwrap nested arrays
 * 
 * LIMITATIONS:
 * - Can only use in conditional type extends clause
 * - Cannot infer from non-type positions
 * - Covariant inference position (output types)
 */


// ============================================================================
// 6. TEMPLATE LITERAL TYPES
// ============================================================================

console.log("\n=== Template Literal Types ===");

/**
 * TEMPLATE LITERAL TYPES EXPLAINED:
 * ==================================
 * 
 * Template literal types use the same syntax as JavaScript template
 * literals, but they operate at the TYPE LEVEL (compile time).
 * 
 * SYNTAX:
 * type MyType = `${A}${B}${C}`;
 * 
 * KEY BEHAVIORS:
 * 
 * 1. STRING INTERPOLATION AT TYPE LEVEL:
 *    Combines literal strings with types to create new string literal types
 * 
 * 2. UNION DISTRIBUTION:
 *    When you use a union type in ${}, TypeScript creates a CARTESIAN PRODUCT
 *    type A = "x" | "y";
 *    type B = "1" | "2";
 *    type C = `${A}${B}`;  // "x1" | "x2" | "y1" | "y2"
 * 
 * 3. WORKS WITH INTRINSIC STRING UTILITIES:
 *    - Capitalize<T>: First letter uppercase
 *    - Uncapitalize<T>: First letter lowercase
 *    - Uppercase<T>: All letters uppercase
 *    - Lowercase<T>: All letters lowercase
 * 
 * WHEN TO USE:
 * ✓ Type-safe string patterns (URLs, CSS classes, event names)
 * ✓ API route typing
 * ✓ Database column names from types
 * ✓ Event handler naming conventions
 * ✓ CSS-in-JS type safety
 * 
 * LIMITATIONS:
 * - Can create HUGE union types (performance impact)
 * - Only works with string literal types, not arbitrary strings
 * - No regex patterns or complex string manipulation
 * 
 * PERFORMANCE CONSIDERATION:
 * Multiple unions multiply quickly:
 * type A = "a" | "b";
 * type B = "1" | "2";
 * type C = "x" | "y";
 * type D = `${A}${B}${C}`;  // 2 × 2 × 2 = 8 combinations
 * 
 * With 4 unions of 5 options each: 5^4 = 625 string literal types!
 */

// Basic template literal type
type Greeting = `Hello ${string}`;
// This matches ANY string that starts with "Hello "
// string in ${} acts as a wildcard for any string

const greeting1: Greeting = "Hello Alice";       // ✓ Valid
const greeting2: Greeting = "Hello Bob";         // ✓ Valid
const greeting3: Greeting = "Hello 123";         // ✓ Valid
// const greeting4: Greeting = "Hi Alice";       // ✗ Error: doesn't start with "Hello "
// const greeting5: Greeting = "hello Alice";    // ✗ Error: wrong case

// With unions - DISTRIBUTION
type Direction = "top" | "right" | "bottom" | "left";
type Margin = `margin${Capitalize<Direction>}`;
// TypeScript distributes over the union:
// = `margin${Capitalize<"top">}` | `margin${Capitalize<"right">}` | ...
// = "marginTop" | "marginRight" | "marginBottom" | "marginLeft"
// 
// This creates 4 EXACT string literal types
// You can ONLY assign these exact strings

// Multiple unions - CARTESIAN PRODUCT
type HTTPMethod = "GET" | "POST";
type Endpoint = "users" | "posts";
type APIRoute = `${HTTPMethod} /${Endpoint}`;
// Cartesian product of unions:
// = ("GET" | "POST") × ("users" | "posts")
// = "GET /users" | "GET /posts" | "POST /users" | "POST /posts"
// 
// Result: 2 × 2 = 4 possible combinations
// Type-safe API routes!

const validRoute1: APIRoute = "GET /users";      // ✓ Valid
const validRoute2: APIRoute = "POST /posts";     // ✓ Valid
// const invalidRoute: APIRoute = "DELETE /users"; // ✗ Error: not in union
// const typo: APIRoute = "GET /user";            // ✗ Error: typo caught at compile time

// Event handler types - REAL-WORLD PATTERN
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// Result: "onClick" | "onFocus" | "onBlur"
// 
// Common in React, Vue, Angular for prop types:
// interface ButtonProps {
//     onClick?: () => void;
//     onFocus?: () => void;
//     onBlur?: () => void;
// }

// CSS properties - DESIGN SYSTEM TYPING
type Size = "sm" | "md" | "lg";
type Color = "primary" | "secondary";
type ClassName = `${Size}-${Color}`;
// Cartesian product:
// = ("sm" | "md" | "lg") × ("primary" | "secondary")
// = "sm-primary" | "sm-secondary" | "md-primary" | 
//   "md-secondary" | "lg-primary" | "lg-secondary"
// 
// Result: 3 × 2 = 6 type-safe CSS class names
// Typos are caught at compile time!

const cssClass: ClassName = "md-primary";        // ✓ Valid
// const typo: ClassName = "medium-primary";     // ✗ Error: not in union
// const invalid: ClassName = "sm-tertiary";     // ✗ Error: tertiary not defined

console.log("CSS class:", cssClass);

/**
 * ADVANCED PATTERNS:
 * 
 * 1. NESTED TEMPLATE LITERALS:
 *    type Deep = `${A}-${`${B}-${C}`}`;
 * 
 * 2. CONDITIONAL IN TEMPLATES:
 *    type Prefixed<T> = T extends string ? `prefix-${T}` : never;
 * 
 * 3. RECURSIVE PATTERNS:
 *    type Path<T> = T extends object 
 *        ? { [K in keyof T]: `${K}` | `${K}.${Path<T[K]>}` }[keyof T]
 *        : never;
 *    // Creates dot-notation paths for nested objects
 * 
 * REAL-WORLD USE CASES:
 * - Type-safe URL routing in frameworks
 * - CSS-in-JS type safety (styled-components, emotion)
 * - Database query builders (Prisma, TypeORM)
 * - GraphQL query type generation
 * - Event system typing
 */


// ============================================================================
// 7. INTRINSIC STRING MANIPULATION TYPES
// ============================================================================

console.log("\n=== String Manipulation Types ===");

/**
 * Built-in string manipulation types:
 * - Uppercase<S>
 * - Lowercase<S>
 * - Capitalize<S>
 * - Uncapitalize<S>
 */

type Loud = Uppercase<"hello">;        // "HELLO"
type Quiet = Lowercase<"HELLO">;       // "hello"
type Cap = Capitalize<"hello">;        // "Hello"
type Uncap = Uncapitalize<"Hello">;    // "hello"

// Practical example: generate property names
type PropName = "firstName" | "lastName";
type PropGetter = `get${Capitalize<PropName>}`;
// "getFirstName" | "getLastName"

type PropSetter = `set${Capitalize<PropName>}`;
// "setFirstName" | "setLastName"


// ============================================================================
// 8. RECURSIVE TYPES
// ============================================================================

console.log("\n=== Recursive Types ===");

/**
 * Types can reference themselves
 * Useful for tree structures, nested data
 */

// JSON type
type JSONValue = 
    | string
    | number
    | boolean
    | null
    | JSONValue[]
    | { [key: string]: JSONValue };

const json: JSONValue = {
    name: "Alice",
    age: 30,
    tags: ["developer", "typescript"],
    metadata: {
        created: "2024-01-01",
        nested: {
            deep: true
        }
    }
};

// Tree structure
interface TreeNode<T> {
    value: T;
    children?: TreeNode<T>[];
}

const tree: TreeNode<number> = {
    value: 1,
    children: [
        { value: 2 },
        { 
            value: 3,
            children: [
                { value: 4 }
            ]
        }
    ]
};

console.log("Tree:", tree);


// ============================================================================
// 9. ADVANCED UTILITY TYPE IMPLEMENTATIONS
// ============================================================================

console.log("\n=== Advanced Utility Types ===");

// DeepReadonly - make nested objects readonly
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

interface NestedUser {
    name: string;
    address: {
        street: string;
        city: string;
    };
}

type DeepReadonlyUser = DeepReadonly<NestedUser>;

// DeepPartial - make nested objects optional
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Flatten intersection types
type Flatten<T> = { [K in keyof T]: T[K] };

type A = { a: number };
type B = { b: string };
type Flattened = Flatten<A & B>;  // { a: number; b: string }

// Get function names from object
type FunctionPropertyNames<T> = {
    [K in keyof T]: T[K] extends Function ? K : never;
}[keyof T];

interface MyObject {
    name: string;
    age: number;
    greet(): void;
    calculate(): number;
}

type Functions = FunctionPropertyNames<MyObject>;  // "greet" | "calculate"


// ============================================================================
// 10. TYPE CHALLENGES (INTERVIEW LEVEL)
// ============================================================================

console.log("\n=== Type Challenges ===");

// Challenge 1: Get readonly keys
type ReadonlyKeys<T> = {
    [P in keyof T]-?: (<F>() => F extends { [Q in P]: T[P] } ? 1 : 2) extends
                      (<F>() => F extends { -readonly [Q in P]: T[P] } ? 1 : 2)
                      ? never : P;
}[keyof T];

// Challenge 2: Get optional keys
type OptionalKeys<T> = {
    [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

// Challenge 3: Deep merge
type Merge<T, U> = {
    [K in keyof T | keyof U]: K extends keyof U
        ? U[K]
        : K extends keyof T
        ? T[K]
        : never;
};

// Challenge 4: Tuple to union
type TupleToUnion<T extends any[]> = T[number];

type Colors = ["red", "green", "blue"];
type ColorUnion = TupleToUnion<Colors>;  // "red" | "green" | "blue"


// ============================================================================
// 11. PRACTICAL EXAMPLES
// ============================================================================

console.log("\n=== Practical Examples ===");

// Type-safe event emitter
type EventMap = {
    login: { userId: number; timestamp: Date };
    logout: { userId: number };
    error: { message: string; code: number };
};

class TypedEventEmitter<T extends Record<string, any>> {
    private listeners: { [K in keyof T]?: Array<(data: T[K]) => void> } = {};
    
    on<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event]!.push(listener);
    }
    
    emit<K extends keyof T>(event: K, data: T[K]): void {
        const eventListeners = this.listeners[event];
        if (eventListeners) {
            eventListeners.forEach(listener => listener(data));
        }
    }
}

const emitter = new TypedEventEmitter<EventMap>();

emitter.on("login", (data) => {
    console.log("  User logged in:", data.userId);  // data is typed!
});

emitter.emit("login", { userId: 123, timestamp: new Date() });
// emitter.emit("login", { userId: 123 });  // Error: missing timestamp

// Type-safe API client
type APIEndpoints = {
    "/users": { method: "GET"; response: User[] };
    "/users/:id": { method: "GET"; response: User };
    "/users": { method: "POST"; body: Omit<User, "id">; response: User };
};

// Type-safe builder pattern
class QueryBuilder<T> {
    private filters: Array<(item: T) => boolean> = [];
    
    where<K extends keyof T>(key: K, value: T[K]): this {
        this.filters.push(item => item[key] === value);
        return this;
    }
    
    execute(items: T[]): T[] {
        return items.filter(item => 
            this.filters.every(filter => filter(item))
        );
    }
}

const users: User[] = [
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" }
];

const query = new QueryBuilder<User>()
    .where("name", "Alice")
    .execute(users);

console.log("Query result:", query);


// ============================================================================
// 12. RECURSIVE CONDITIONAL TYPES
// ============================================================================

console.log("\n=== Recursive Types ===");

// Deep readonly (recursive)
type DeepReadonly<T> = {
    readonly [P in keyof T]: T[P] extends object 
        ? T[P] extends Function
            ? T[P]
            : DeepReadonly<T[P]>
        : T[P];
};

interface NestedData {
    name: string;
    metadata: {
        tags: string[];
        info: {
            created: Date;
        };
    };
}

type DeepReadonlyData = DeepReadonly<NestedData>;
// All nested properties are readonly

// Deep partial (recursive)
type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object 
        ? DeepPartial<T[P]> 
        : T[P];
};

type DeepPartialData = DeepPartial<NestedData>;
// All nested properties are optional

// Path type (get nested property paths)
type PathsToStringProps<T> = T extends string 
    ? []
    : {
        [K in Extract<keyof T, string>]: [K, ...PathsToStringProps<T[K]>];
    }[Extract<keyof T, string>];

// Flatten union
type FlattenUnion<T> = T extends any ? T : never;


// ============================================================================
// 13. VARIANCE ANNOTATIONS (TS 4.7+)
// ============================================================================

console.log("\n=== Variance Annotations ===");

/**
 * in = contravariant (input position)
 * out = covariant (output position)
 */

// Covariant (out)
interface Producer<out T> {
    produce(): T;
}

// Contravariant (in)
interface Consumer<in T> {
    consume(value: T): void;
}

// Invariant (both)
interface Box<T> {
    value: T;
}


// ============================================================================
// 14. SATISFIES OPERATOR (TS 4.9+)
// ============================================================================

console.log("\n=== Satisfies Operator ===");

/**
 * satisfies = check type without widening
 * Preserves literal types
 */

type Color = "red" | "green" | "blue" | { r: number; g: number; b: number };

// Without satisfies - type is Color (union)
const color1: Color = "red";
// color1.toUpperCase();  // Error: Property doesn't exist on Color

// With satisfies - type is "red" (literal)
const color2 = "red" satisfies Color;
color2.toUpperCase();  // OK - TypeScript knows it's a string

// More complex example
type Route = { path: string; component: any };
type Routes = Record<string, Route>;

const routes = {
    home: { path: "/", component: "HomeComponent" },
    about: { path: "/about", component: "AboutComponent" }
} satisfies Routes;

// TypeScript knows exact keys
routes.home.path;  // OK
// routes.unknown.path;  // Error: Property 'unknown' does not exist


// ============================================================================
// 15. TYPE PREDICATES WITH GENERICS
// ============================================================================

console.log("\n=== Type Predicates ===");

// Generic type guard
function isType<T>(value: unknown, check: (val: any) => boolean): value is T {
    return check(value);
}

interface Dog {
    bark(): void;
}

interface Cat {
    meow(): void;
}

function isDog(animal: Dog | Cat): animal is Dog {
    return (animal as Dog).bark !== undefined;
}

const animal: Dog | Cat = { bark: () => console.log("Woof!") } as Dog;

if (isDog(animal)) {
    animal.bark();  // TypeScript knows it's Dog
}


// ============================================================================
// 16. BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * ADVANCED TYPES BEST PRACTICES:
 * 
 * 1. USE MAPPED TYPES FOR TRANSFORMATIONS
 *    Instead of repeating properties
 * 
 * 2. CONDITIONAL TYPES FOR FLEXIBILITY
 *    Create types that adapt to inputs
 * 
 * 3. INFER FOR TYPE EXTRACTION
 *    Extract types from complex structures
 * 
 * 4. TEMPLATE LITERALS FOR STRING TYPES
 *    Type-safe string manipulation
 * 
 * 5. DON'T OVER-ENGINEER
 *    Complex types can hurt maintainability
 *    Balance type safety with readability
 * 
 * 6. DOCUMENT COMPLEX TYPES
 *    Add comments explaining what type does
 * 
 * 7. TEST YOUR TYPES
 *    Use type assertions to verify behavior
 *    type _Test = Expect<Equal<MyType, ExpectedType>>;
 * 
 * 8. USE SATISFIES FOR LITERAL PRESERVATION
 *    Better than type assertion
 * 
 * 9. RECURSIVE TYPES WITH CARE
 *    Can be slow to compile
 *    May hit recursion limits
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Mapped types transform object properties");
console.log("2. Conditional types: T extends U ? X : Y");
console.log("3. infer keyword extracts types from patterns");
console.log("4. Template literal types for string manipulation");
console.log("5. Distributive conditional types over unions");
console.log("6. Recursive types for nested structures");
console.log("7. satisfies preserves literal types");
console.log("8. Variance annotations (in/out) for type safety");
console.log("9. Type-level programming is powerful but use judiciously");
console.log("10. Balance type safety with maintainability");
console.log("=".repeat(80));

export {};
