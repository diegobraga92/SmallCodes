/**
 * TYPESCRIPT INTERFACES
 * ======================
 * Comprehensive guide to interfaces in TypeScript
 * Object shapes, optional properties, readonly, extending
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT INTERFACES");
console.log("=".repeat(80));

// ============================================================================
// 1. BASIC INTERFACES
// ============================================================================

console.log("\n=== Basic Interfaces ===");

// Define object shape
interface User {
    id: number;
    name: string;
    email: string;
}

const user: User = {
    id: 1,
    name: "Alice",
    email: "alice@example.com"
};

console.log("User:", user);

// Function parameter with interface
function printUser(user: User): void {
    console.log(`  ${user.name} (${user.email})`);
}

printUser(user);


// ============================================================================
// 2. OPTIONAL PROPERTIES
// ============================================================================

console.log("\n=== Optional Properties ===");

interface Product {
    id: number;
    name: string;
    description?: string;  // Optional
    price: number;
    inStock?: boolean;     // Optional
}

const product1: Product = {
    id: 1,
    name: "Laptop",
    price: 999.99
};

const product2: Product = {
    id: 2,
    name: "Mouse",
    description: "Wireless mouse",
    price: 29.99,
    inStock: true
};

console.log("Products:", { product1, product2 });


// ============================================================================
// 3. READONLY PROPERTIES
// ============================================================================

console.log("\n=== Readonly Properties ===");

interface Config {
    readonly apiUrl: string;
    readonly timeout: number;
    retries: number;  // Mutable
}

const config: Config = {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3
};

// config.apiUrl = "new url";  // Error: Cannot assign to 'apiUrl' because it is a read-only property
config.retries = 5;  // OK

console.log("Config:", config);


// ============================================================================
// 4. FUNCTION TYPES IN INTERFACES
// ============================================================================

console.log("\n=== Function Types ===");

interface Calculator {
    add(a: number, b: number): number;
    subtract(a: number, b: number): number;
    multiply(a: number, b: number): number;
    divide(a: number, b: number): number;
}

const calculator: Calculator = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b,
    multiply: (a, b) => a * b,
    divide: (a, b) => a / b
};

console.log("Calculator:", calculator.add(5, 3));

// Alternative syntax
interface SearchFunction {
    (query: string, limit: number): string[];
}

const search: SearchFunction = (query, limit) => {
    return [`Result 1 for ${query}`, `Result 2 for ${query}`].slice(0, limit);
};

console.log("Search:", search("typescript", 2));


// ============================================================================
// 5. INDEX SIGNATURES
// ============================================================================

console.log("\n=== Index Signatures ===");

// String index signature
interface StringDictionary {
    [key: string]: string;
}

const translations: StringDictionary = {
    hello: "hola",
    goodbye: "adiós",
    thanks: "gracias"
};

console.log("Translation:", translations["hello"]);

// Number index signature
interface NumberDictionary {
    [index: number]: string;
    length: number;  // OK
    // name: string;  // Error: Property 'name' of type 'string' is not assignable to string index type 'string'
}

// Mixed keys
interface MixedDictionary {
    [key: string]: number | string;
    count: number;  // OK
    name: string;   // OK
}


// ============================================================================
// 6. EXTENDING INTERFACES
// ============================================================================

console.log("\n=== Extending Interfaces ===");

interface Person {
    name: string;
    age: number;
}

interface Employee extends Person {
    employeeId: number;
    department: string;
}

const employee: Employee = {
    name: "Alice",
    age: 30,
    employeeId: 12345,
    department: "Engineering"
};

console.log("Employee:", employee);

// Multiple inheritance
interface Timestamped {
    createdAt: Date;
    updatedAt: Date;
}

interface Document extends Person, Timestamped {
    title: string;
}

const document: Document = {
    name: "Alice",
    age: 30,
    createdAt: new Date(),
    updatedAt: new Date(),
    title: "Report"
};

console.log("Document:", document.title);


// ============================================================================
// 7. INTERFACE VS TYPE ALIAS
// ============================================================================

console.log("\n=== Interface vs Type Alias ===");

// Interface
interface UserInterface {
    name: string;
    age: number;
}

// Type alias
type UserType = {
    name: string;
    age: number;
};

// Both work similarly for objects
const user1: UserInterface = { name: "Alice", age: 30 };
const user2: UserType = { name: "Bob", age: 25 };

/**
 * DIFFERENCES:
 * 
 * 1. DECLARATION MERGING (only interfaces):
 *    interface Window {
 *        title: string;
 *    }
 *    interface Window {
 *        ts: string;
 *    }
 *    // Merged: Window now has both properties
 * 
 * 2. EXTENDS (different syntax):
 *    interface Animal extends Mammal { }  // Interface
 *    type Animal = Mammal & { }           // Type
 * 
 * 3. TYPES CAN DO MORE:
 *    - Union types: type ID = string | number;
 *    - Mapped types: type Readonly<T> = { readonly [P in keyof T]: T[P] }
 *    - Conditional types
 * 
 * WHEN TO USE WHAT:
 * - Use INTERFACE for object shapes (especially public APIs)
 * - Use TYPE for unions, tuples, advanced types
 */


// ============================================================================
// 8. IMPLEMENTING INTERFACES WITH CLASSES
// ============================================================================

console.log("\n=== Implementing Interfaces ===");

interface Animal {
    name: string;
    makeSound(): void;
}

class Dog implements Animal {
    name: string;
    
    constructor(name: string) {
        this.name = name;
    }
    
    makeSound(): void {
        console.log(`  ${this.name} says: Woof!`);
    }
}

class Cat implements Animal {
    name: string;
    
    constructor(name: string) {
        this.name = name;
    }
    
    makeSound(): void {
        console.log(`  ${this.name} says: Meow!`);
    }
}

const dog = new Dog("Rex");
const cat = new Cat("Whiskers");

dog.makeSound();
cat.makeSound();


// ============================================================================
// 9. GENERIC INTERFACES
// ============================================================================

console.log("\n=== Generic Interfaces ===");

interface Box<T> {
    value: T;
    getValue(): T;
}

const numberBox: Box<number> = {
    value: 42,
    getValue() {
        return this.value;
    }
};

const stringBox: Box<string> = {
    value: "Hello",
    getValue() {
        return this.value;
    }
};

console.log("Number box:", numberBox.getValue());
console.log("String box:", stringBox.getValue());

// Multiple type parameters
interface Pair<K, V> {
    key: K;
    value: V;
}

const pair: Pair<string, number> = {
    key: "age",
    value: 30
};

console.log("Pair:", pair);


// ============================================================================
// 10. HYBRID TYPES
// ============================================================================

console.log("\n=== Hybrid Types ===");

// Interface that is both callable and has properties
interface Counter {
    (start: number): string;
    interval: number;
    reset(): void;
}

function getCounter(): Counter {
    let counter = (function(start: number) {
        return `Count: ${start}`;
    }) as Counter;
    
    counter.interval = 1000;
    counter.reset = function() {
        console.log("  Counter reset");
    };
    
    return counter;
}

const myCounter = getCounter();
console.log(myCounter(10));
console.log("Interval:", myCounter.interval);
myCounter.reset();


// ============================================================================
// 11. BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * INTERFACE BEST PRACTICES:
 * 
 * 1. PREFER INTERFACES FOR OBJECT SHAPES:
 *    // Good
 *    interface User {
 *        name: string;
 *        email: string;
 *    }
 *    
 *    // Use type for unions/intersections
 *    type ID = string | number;
 * 
 * 2. USE OPTIONAL PROPERTIES WISELY:
 *    // Good
 *    interface Config {
 *        host: string;
 *        port?: number;  // Has sensible default
 *    }
 * 
 * 3. USE READONLY FOR IMMUTABILITY:
 *    interface User {
 *        readonly id: number;
 *        name: string;
 *    }
 * 
 * 4. EXTEND WHEN RELATED:
 *    interface Employee extends Person {
 *        employeeId: number;
 *    }
 * 
 * 5. GENERIC INTERFACES FOR REUSABILITY:
 *    interface Response<T> {
 *        data: T;
 *        status: number;
 *    }
 * 
 * 6. DOCUMENT PUBLIC INTERFACES:
 *    /**
 *     * Represents a user in the system
 *     * /
 *    interface User {
 *        /** Unique identifier * /
 *        id: number;
 *        /** Full name * /
 *        name: string;
 *    }
 * 
 * 7. AVOID EMPTY INTERFACES:
 *    // Bad
 *    interface Empty { }
 *    
 *    // Good - use unknown or Record<string, unknown>
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Interfaces define object shapes");
console.log("2. Use ? for optional properties");
console.log("3. Use readonly to prevent modification");
console.log("4. Extend interfaces for inheritance");
console.log("5. Implement interfaces with classes");
console.log("6. Generic interfaces for reusability");
console.log("7. Index signatures for dynamic keys");
console.log("8. Prefer interfaces over type aliases for objects");
console.log("=".repeat(80));

export {};
