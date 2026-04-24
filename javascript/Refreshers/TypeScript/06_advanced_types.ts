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
 * Mapped types transform properties of existing types
 * Syntax: { [P in K]: T }
 */

// Make all properties optional
type MyPartial<T> = {
    [P in keyof T]?: T[P];
};

interface User {
    id: number;
    name: string;
    email: string;
}

type PartialUser = MyPartial<User>;
// { id?: number; name?: string; email?: string; }

// Make all properties readonly
type MyReadonly<T> = {
    readonly [P in keyof T]: T[P];
};

type ReadonlyUser = MyReadonly<User>;
// { readonly id: number; readonly name: string; readonly email: string; }

// Make all properties required
type MyRequired<T> = {
    [P in keyof T]-?: T[P];  // -? removes optional modifier
};

// Make all properties mutable (remove readonly)
type Mutable<T> = {
    -readonly [P in keyof T]: T[P];  // -readonly removes readonly
};

// Example usage
const user1: PartialUser = { name: "Alice" };  // OK - all optional
const user2: ReadonlyUser = { id: 1, name: "Bob", email: "bob@example.com" };
// user2.name = "Changed";  // Error: readonly

console.log("Mapped types:", { user1, user2 });


// ============================================================================
// 2. MAPPED TYPES WITH TRANSFORMATIONS
// ============================================================================

console.log("\n=== Mapped Type Transformations ===");

// Add 'get' prefix to all properties
type Getters<T> = {
    [P in keyof T as `get${Capitalize<string & P>}`]: () => T[P];
};

interface Person {
    name: string;
    age: number;
}

type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number; }

// Filter properties by type
type StringProperties<T> = {
    [P in keyof T as T[P] extends string ? P : never]: T[P];
};

interface Mixed {
    name: string;
    age: number;
    email: string;
    active: boolean;
}

type OnlyStrings = StringProperties<Mixed>;
// { name: string; email: string; }

// Exclude certain properties
type OmitType<T, K extends keyof T> = {
    [P in keyof T as P extends K ? never : P]: T[P];
};

type UserWithoutId = OmitType<User, "id">;
// { name: string; email: string; }


// ============================================================================
// 3. CONDITIONAL TYPES
// ============================================================================

console.log("\n=== Conditional Types ===");

/**
 * Conditional types: T extends U ? X : Y
 * Choose type based on condition
 */

// Check if type is string
type IsString<T> = T extends string ? true : false;

type Test1 = IsString<string>;   // true
type Test2 = IsString<number>;   // false

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
 * infer = declare type variable within conditional type
 * Extract types from complex type expressions
 */

// Extract return type from function
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function getString(): string {
    return "hello";
}

function getNumber(): number {
    return 42;
}

type StringReturn = MyReturnType<typeof getString>;  // string
type NumberReturn = MyReturnType<typeof getNumber>;  // number

// Extract parameters from function
type MyParameters<T> = T extends (...args: infer P) => any ? P : never;

function add(a: number, b: number): number {
    return a + b;
}

type AddParams = MyParameters<typeof add>;  // [number, number]

// Extract array element type
type Unpacked<T> = T extends (infer U)[] ? U : 
                   T extends Promise<infer U> ? U : 
                   T;

type Test8 = Unpacked<string[]>;          // string
type Test9 = Unpacked<Promise<number>>;   // number
type Test10 = Unpacked<boolean>;          // boolean


// ============================================================================
// 6. TEMPLATE LITERAL TYPES
// ============================================================================

console.log("\n=== Template Literal Types ===");

/**
 * Template literal types = string manipulation at type level
 */

// Basic template literal type
type Greeting = `Hello ${string}`;
const greeting1: Greeting = "Hello Alice";
const greeting2: Greeting = "Hello Bob";
// const greeting3: Greeting = "Hi Alice";  // Error

// With unions
type Direction = "top" | "right" | "bottom" | "left";
type Margin = `margin${Capitalize<Direction>}`;
// "marginTop" | "marginRight" | "marginBottom" | "marginLeft"

// Multiple unions (Cartesian product)
type HTTPMethod = "GET" | "POST";
type Endpoint = "users" | "posts";
type APIRoute = `${HTTPMethod} /${Endpoint}`;
// "GET /users" | "GET /posts" | "POST /users" | "POST /posts"

// Event handler types
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

// CSS properties
type Size = "sm" | "md" | "lg";
type Color = "primary" | "secondary";
type ClassName = `${Size}-${Color}`;
// "sm-primary" | "sm-secondary" | "md-primary" | "md-secondary" | ...

const cssClass: ClassName = "md-primary";
console.log("CSS class:", cssClass);


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
