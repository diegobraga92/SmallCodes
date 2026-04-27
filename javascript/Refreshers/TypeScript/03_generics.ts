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

/**
 * GENERIC CONSTRAINTS EXPLAINED:
 * ==============================
 * 
 * Generic constraints limit which types can be used with a generic type parameter.
 * 
 * SYNTAX:
 * <T extends SomeType>
 * 
 * "extends" MEANS: T must be assignable to SomeType
 * - T can be SomeType itself
 * - T can be a subtype of SomeType
 * - T must have AT LEAST the properties/methods of SomeType
 * 
 * WHY USE CONSTRAINTS?
 * 
 * 1. ACCESS SPECIFIC PROPERTIES/METHODS:
 *    Without constraint: Can't assume T has any properties
 *    With constraint: Can safely access guaranteed properties
 * 
 * 2. TYPE SAFETY:
 *    Prevents passing incompatible types
 *    Catches errors at compile time
 * 
 * 3. BETTER AUTOCOMPLETE:
 *    IDE knows what properties/methods are available
 * 
 * WHEN TO USE:
 * ✓ Need to access specific properties (e.g., .length, .id)
 * ✓ Require certain methods (e.g., .toString(), .map())
 * ✓ Ensure type compatibility
 * ✓ Type-safe property access (keyof pattern)
 * 
 * COMMON PATTERNS:
 * - extends object: Any object type
 * - extends string | number: Multiple type options
 * - extends keyof T: Must be a key of T
 * - extends new (...args: any[]) => any: Constructor types
 */

// Constrain to types with length property
interface HasLength {
    length: number;
}

function logLength<T extends HasLength>(arg: T): void {
    // WITHOUT constraint: T is any type, can't access .length
    // WITH constraint: T guaranteed to have .length property
    // TypeScript allows us to access arg.length safely
    console.log(`  Length: ${arg.length}`);
    
    // We can also return T, maintaining the original type
    // return arg; // Would return T, not just HasLength
}

// All these types have .length property:
logLength("hello");            // string has length ✓
logLength([1, 2, 3]);          // array has length ✓
logLength({ length: 10 });     // object with length ✓
// logLength(123);             // Error: number doesn't have length ✗
// logLength({ size: 10 });    // Error: 'size' is not 'length' ✗

/**
 * KEY INSIGHT:
 * The constraint doesn't change T to HasLength
 * T remains its original type (string, array, etc.)
 * But TypeScript ensures T has AT LEAST the length property
 */

// Constrain to object keys - POWERFUL PATTERN
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    // BREAKDOWN:
    // <T, K extends keyof T>
    //     ^^^^^^^^^^^^^^^
    //     K must be one of T's keys
    // 
    // keyof T = union of all property names in T
    // If T = { name: string; age: number }
    // Then keyof T = "name" | "age"
    // 
    // So K can ONLY be "name" or "age" (type-safe!)
    // 
    // T[K] = the TYPE of property K in T (indexed access type)
    // If K = "name", then T[K] = string
    // If K = "age", then T[K] = number
    
    return obj[key];
}

const person = { name: "Alice", age: 30 };

const name = getProperty(person, "name");  // Type: string (TypeScript infers!)
// How? T = { name: string; age: number }
//      K = "name"
//      T[K] = T["name"] = string

const age = getProperty(person, "age");    // Type: number
// How? T = { name: string; age: number }
//      K = "age"
//      T[K] = T["age"] = number

// const invalid = getProperty(person, "invalid");  // Error! 
// TypeScript error: "invalid" is not assignable to "name" | "age"
// This error is caught at COMPILE TIME!

console.log("Get property:", { name, age });

/**
 * WHY K extends keyof T IS POWERFUL:
 * 
 * 1. TYPE-SAFE PROPERTY ACCESS:
 *    Can't access non-existent properties
 * 
 * 2. AUTOCOMPLETE:
 *    IDE suggests valid keys only
 * 
 * 3. REFACTOR-SAFE:
 *    Rename property? TypeScript updates all usages
 * 
 * 4. PRESERVES EXACT TYPE:
 *    Return type is T[K], not string | number | ...
 *    Each key gets its specific type
 * 
 * COMMON USE CASES:
 * - Type-safe object property getters
 * - Form field accessors
 * - Configuration object readers
 * - Database column selectors
 * - Redux state selectors
 */


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


// ============================================================================
// 10. VARIANCE IN GENERICS (ADVANCED)
// ============================================================================

console.log("\n=== Variance ===");

/**
 * VARIANCE EXPLAINED:
 * ==================
 * 
 * Variance describes how subtyping between types relates to subtyping between
 * their generic versions. This is an ADVANCED concept but crucial for understanding
 * TypeScript's type system behavior.
 * 
 * THREE TYPES OF VARIANCE:
 * 
 * 1. COVARIANCE (Most Common):
 *    If Dog extends Animal, then Container<Dog> extends Container<Animal>
 *    Direction: Same as the type parameter
 *    Examples: Arrays, Promises, readonly properties
 * 
 * 2. CONTRAVARIANCE (Function Parameters):
 *    If Dog extends Animal, then Handler<Animal> extends Handler<Dog>
 *    Direction: OPPOSITE of the type parameter
 *    Examples: Function parameter types
 * 
 * 3. INVARIANCE (Mutable Structures):
 *    Dog extends Animal, but Container<Dog> does NOT extend Container<Animal>
 *    Direction: No relationship
 *    Examples: Mutable generic classes (with --strictFunctionTypes)
 * 
 * WHY THIS MATTERS:
 * Understanding variance prevents runtime errors and explains why
 * TypeScript rejects certain type assignments.
 */

// COVARIANCE EXAMPLE: Arrays are covariant

class Animal {
    name: string = "animal";
}

class Dog extends Animal {
    bark(): void { console.log("Woof!"); }
}

class Cat extends Animal {
    meow(): void { console.log("Meow!"); }
}

// Arrays are COVARIANT (in readonly positions):
// Dog[] is assignable to Animal[] (when reading)
const dogs: Dog[] = [new Dog()];
const animals: Animal[] = dogs;  // ✓ OK (covariant)
// We can treat Dog[] as Animal[] for READING

// BUT this is dangerous for WRITING:
// animals.push(new Cat());  // TypeScript allows but causes runtime error!
// dogs[0].bark();  // Runtime error: bark doesn't exist on Cat

/**
 * IMPORTANT: TypeScript allows this because arrays are covariant
 * For sound typing, arrays should be invariant, but TypeScript
 * chose convenience over perfect soundness
 * 
 * SAFE ALTERNATIVE: Use readonly
 */
const readonlyDogs: readonly Dog[] = [new Dog()];
const readonlyAnimals: readonly Animal[] = readonlyDogs;  // ✓ Safe
// readonlyAnimals.push(new Cat());  // ✗ Error: push doesn't exist on readonly array


// CONTRAVARIANCE EXAMPLE: Function parameters are contravariant

type AnimalHandler = (animal: Animal) => void;
type DogHandler = (dog: Dog) => void;

const handleAnimal: AnimalHandler = (animal: Animal) => {
    console.log(animal.name);  // Works for any Animal
};

const handleDog: DogHandler = (dog: Dog) => {
    console.log(dog.name);
    dog.bark();  // Dog-specific operation
};

// CONTRAVARIANCE: Handler<Animal> extends Handler<Dog>
// A function that handles ANY Animal can handle Dogs specifically
const dogHandler1: DogHandler = handleAnimal;  // ✓ OK (contravariant)
// WHY? handleAnimal works for all Animals, so it works for Dogs too

// const animalHandler: AnimalHandler = handleDog;  // ✗ Error!
// WHY? handleDog expects Dog-specific operations (bark)
// But AnimalHandler might be called with Cats (no bark method)

/**
 * MENTAL MODEL FOR FUNCTION CONTRAVARIANCE:
 * 
 * A function is SAFE TO USE as a substitute if it accepts
 * MORE GENERAL parameters (Animal vs Dog)
 * 
 * Think: "Can I pass this handler to code expecting DogHandler?"
 * - handleAnimal: YES (works with Dogs and more)
 * - handleDog: NO (only works with Dogs, fails for other Animals)
 */


// INVARIANCE EXAMPLE: Mutable generic classes

class Box<T> {
    constructor(public value: T) {}
    
    getValue(): T {
        return this.value;
    }
    
    setValue(value: T): void {
        this.value = value;
    }
}

const dogBox: Box<Dog> = new Box(new Dog());
// const animalBox: Box<Animal> = dogBox;  // Error with --strictFunctionTypes
// 
// WHY? Box is INVARIANT because it's both:
// - Covariant in getValue() (returns T)
// - Contravariant in setValue(value: T) (accepts T)
// 
// If assignment were allowed:
// animalBox.setValue(new Cat());  // Would put Cat in Box<Dog>!
// dogBox.getValue().bark();  // Runtime error!

/**
 * PRACTICAL GUIDELINES:
 * 
 * 1. READONLY STRUCTURES → COVARIANT (SAFE):
 *    readonly T[], Promise<T>, ReadonlyArray<T>
 * 
 * 2. FUNCTION PARAMETERS → CONTRAVARIANT (SAFE):
 *    (t: T) => void
 * 
 * 3. MUTABLE STRUCTURES → INVARIANT (SAFEST):
 *    class Box<T> with get/set methods
 * 
 * 4. ENABLE --strictFunctionTypes:
 *    Enables proper contravariance checking
 *    Part of --strict mode
 * 
 * 5. USE READONLY WHEN POSSIBLE:
 *    Covariant types are easier to work with
 *    readonly T[] instead of T[] when you don't need mutation
 * 
 * SUMMARY:
 * - Covariance: Type parameter and generic vary together (arrays, promises)
 * - Contravariance: Type parameter and generic vary oppositely (function params)
 * - Invariance: No variance (mutable structures)
 */

console.log("Variance examples complete");


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
console.log("9. Variance: covariant (arrays), contravariant (function params), invariant (mutable)");
console.log("=".repeat(80));

export {};
