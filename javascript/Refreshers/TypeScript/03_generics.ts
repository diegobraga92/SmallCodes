/**
 * TYPESCRIPT GENERICS
 * ====================
 * Comprehensive guide to generics in TypeScript
 * Generic functions, classes, constraints, utility types
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT GENERICS");
console.log("=".repeat(80));

// ============================================================================
// 1. BASIC GENERICS
// ============================================================================

console.log("\n=== Basic Generics ===");

// Generic function
function identity<T>(arg: T): T {
    return arg;
}

// Usage
const num = identity<number>(42);
const str = identity<string>("hello");
const bool = identity<boolean>(true);

// Type inference (TypeScript infers T)
const inferred = identity("auto");  // T is string

console.log("Identity:", { num, str, bool, inferred });

// Generic function with array
function firstElement<T>(arr: T[]): T | undefined {
    return arr[0];
}

console.log("First number:", firstElement([1, 2, 3]));
console.log("First string:", firstElement(["a", "b", "c"]));


// ============================================================================
// 2. GENERIC CONSTRAINTS
// ============================================================================

console.log("\n=== Generic Constraints ===");

// Constrain to types with length property
interface HasLength {
    length: number;
}

function logLength<T extends HasLength>(arg: T): void {
    console.log(`  Length: ${arg.length}`);
}

logLength("hello");  // string has length
logLength([1, 2, 3]);  // array has length
logLength({ length: 10 });  // object with length
// logLength(123);  // Error: number doesn't have length

// Constrain to object keys
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const person = { name: "Alice", age: 30 };
const name = getProperty(person, "name");  // Type: string
const age = getProperty(person, "age");    // Type: number
// const invalid = getProperty(person, "invalid");  // Error

console.log("Get property:", { name, age });


// ============================================================================
// 3. GENERIC CLASSES
// ============================================================================

console.log("\n=== Generic Classes ===");

class Box<T> {
    private value: T;
    
    constructor(value: T) {
        this.value = value;
    }
    
    getValue(): T {
        return this.value;
    }
    
    setValue(value: T): void {
        this.value = value;
    }
}

const numberBox = new Box<number>(42);
const stringBox = new Box<string>("hello");

console.log("Number box:", numberBox.getValue());
console.log("String box:", stringBox.getValue());

// Generic class with multiple type parameters
class Pair<K, V> {
    constructor(public key: K, public value: V) {}
    
    getKey(): K {
        return this.key;
    }
    
    getValue(): V {
        return this.value;
    }
}

const pair = new Pair<string, number>("age", 30);
console.log("Pair:", pair.getKey(), "=", pair.getValue());


// ============================================================================
// 4. GENERIC INTERFACES
// ============================================================================

console.log("\n=== Generic Interfaces ===");

interface Repository<T> {
    getById(id: number): T | undefined;
    getAll(): T[];
    create(item: T): T;
    update(item: T): T;
    delete(id: number): boolean;
}

interface User {
    id: number;
    name: string;
}

class UserRepository implements Repository<User> {
    private users: User[] = [];
    
    getById(id: number): User | undefined {
        return this.users.find(u => u.id === id);
    }
    
    getAll(): User[] {
        return this.users;
    }
    
    create(user: User): User {
        this.users.push(user);
        return user;
    }
    
    update(user: User): User {
        const index = this.users.findIndex(u => u.id === user.id);
        if (index !== -1) {
            this.users[index] = user;
        }
        return user;
    }
    
    delete(id: number): boolean {
        const index = this.users.findIndex(u => u.id === id);
        if (index !== -1) {
            this.users.splice(index, 1);
            return true;
        }
        return false;
    }
}

const userRepo = new UserRepository();
userRepo.create({ id: 1, name: "Alice" });
console.log("Users:", userRepo.getAll());


// ============================================================================
// 5. GENERIC TYPE ALIASES
// ============================================================================

console.log("\n=== Generic Type Aliases ===");

type Result<T> = {
    success: boolean;
    data?: T;
    error?: string;
};

function divide(a: number, b: number): Result<number> {
    if (b === 0) {
        return { success: false, error: "Division by zero" };
    }
    return { success: true, data: a / b };
}

const result1 = divide(10, 2);
const result2 = divide(10, 0);

console.log("Result 1:", result1);
console.log("Result 2:", result2);

// Generic array type
type StringArray = Array<string>;
type NumberArray = Array<number>;
type ObjectWithArray<T> = {
    items: Array<T>;
};


// ============================================================================
// 6. DEFAULT GENERIC PARAMETERS
// ============================================================================

console.log("\n=== Default Generic Parameters ===");

interface ApiResponse<T = any> {
    data: T;
    status: number;
    message: string;
}

// Can use without specifying type (defaults to any)
const response1: ApiResponse = {
    data: "anything",
    status: 200,
    message: "OK"
};

// Or specify type
const response2: ApiResponse<User> = {
    data: { id: 1, name: "Alice" },
    status: 200,
    message: "OK"
};

console.log("Responses:", { response1, response2 });


// ============================================================================
// 7. GENERIC CONSTRAINTS WITH TYPES
// ============================================================================

console.log("\n=== Generic Constraints ===");

// Constraint to specific type
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
    return { ...obj1, ...obj2 };
}

const merged = merge({ name: "Alice" }, { age: 30 });
console.log("Merged:", merged);  // Type: { name: string } & { age: number }

// Constraint with multiple bounds
interface Lengthwise {
    length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
    console.log(`  Length: ${arg.length}`);
    return arg;
}

loggingIdentity("hello");
loggingIdentity([1, 2, 3]);
loggingIdentity({ length: 10, value: 3 });


// ============================================================================
// 8. CONDITIONAL TYPES WITH GENERICS
// ============================================================================

console.log("\n=== Conditional Types ===");

// Extract array element type
type ArrayElement<T> = T extends (infer U)[] ? U : never;

type StringArrayElement = ArrayElement<string[]>;  // string
type NumberArrayElement = ArrayElement<number[]>;  // number
type NotArray = ArrayElement<string>;              // never

// Conditional type example
type IsString<T> = T extends string ? true : false;

type Test1 = IsString<string>;   // true
type Test2 = IsString<number>;   // false


// ============================================================================
// 9. MAPPED TYPES WITH GENERICS
// ============================================================================

console.log("\n=== Mapped Types ===");

// Make all properties optional
type Partial<T> = {
    [P in keyof T]?: T[P];
};

interface Todo {
    title: string;
    description: string;
    completed: boolean;
}

type PartialTodo = Partial<Todo>;  // All properties optional

// Make all properties readonly
type Readonly<T> = {
    readonly [P in keyof T]: T[P];
};

type ReadonlyTodo = Readonly<Todo>;  // All properties readonly

// Pick specific properties
type Pick<T, K extends keyof T> = {
    [P in K]: T[P];
};

type TodoPreview = Pick<Todo, "title" | "completed">;


// ============================================================================
// 10. UTILITY TYPES
// ============================================================================

console.log("\n=== Utility Types ===");

/**
 * BUILT-IN UTILITY TYPES:
 * 
 * Partial<T> - Make all properties optional
 * Required<T> - Make all properties required
 * Readonly<T> - Make all properties readonly
 * Record<K, T> - Object with keys K and values T
 * Pick<T, K> - Pick properties K from T
 * Omit<T, K> - Omit properties K from T
 * Exclude<T, U> - Exclude types from union
 * Extract<T, U> - Extract types from union
 * NonNullable<T> - Exclude null and undefined
 * ReturnType<T> - Get function return type
 * Parameters<T> - Get function parameter types
 */

interface Product {
    id: number;
    name: string;
    price: number;
    description: string;
}

// Partial - all optional
type PartialProduct = Partial<Product>;

// Required - all required
type RequiredProduct = Required<PartialProduct>;

// Readonly - all readonly
type ReadonlyProduct = Readonly<Product>;

// Record - create object type
type ProductMap = Record<number, Product>;

// Pick - select properties
type ProductSummary = Pick<Product, "id" | "name">;

// Omit - exclude properties
type ProductWithoutDescription = Omit<Product, "description">;

// Example usage
const summary: ProductSummary = { id: 1, name: "Laptop" };
console.log("Product summary:", summary);


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Generics enable reusable, type-safe code");
console.log("2. Use <T> syntax for generic type parameter");
console.log("3. Constrain generics with 'extends'");
console.log("4. Generic functions, classes, interfaces, type aliases");
console.log("5. keyof gets object keys as type");
console.log("6. Mapped types transform object types");
console.log("7. Conditional types for type logic");
console.log("8. Utility types (Partial, Pick, Omit, etc.)");
console.log("=".repeat(80));

export {};
