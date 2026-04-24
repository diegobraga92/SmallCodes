/**
 * TYPESCRIPT CLASSES
 * ===================
 * Classes with TypeScript types, access modifiers, abstract classes
 * Parameter properties, implements, generics
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT CLASSES");
console.log("=".repeat(80));

// ============================================================================
// 1. BASIC CLASSES WITH TYPES
// ============================================================================

console.log("\n=== Basic Classes ===");

class Person {
    name: string;
    age: number;
    
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
    
    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
}

const person = new Person("Alice", 30);
console.log(person.greet());


// ============================================================================
// 2. ACCESS MODIFIERS
// ============================================================================

console.log("\n=== Access Modifiers ===");

/**
 * Access modifiers:
 * - public: Accessible anywhere (default)
 * - private: Only accessible within class
 * - protected: Accessible in class and subclasses
 */

class BankAccount {
    public readonly accountNumber: string;  // Public and immutable
    private balance: number;                // Private
    protected ownerName: string;            // Protected
    
    constructor(accountNumber: string, initialBalance: number, ownerName: string) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.ownerName = ownerName;
    }
    
    public deposit(amount: number): void {
        if (amount > 0) {
            this.balance += amount;
        }
    }
    
    public getBalance(): number {
        return this.balance;
    }
    
    private log(message: string): void {
        console.log(`  [${this.accountNumber}] ${message}`);
    }
}

const account = new BankAccount("12345", 1000, "Alice");
account.deposit(500);
console.log("Balance:", account.getBalance());
// console.log(account.balance);  // Error: private
// account.log("test");  // Error: private


// ============================================================================
// 3. PARAMETER PROPERTIES (SHORTHAND)
// ============================================================================

console.log("\n=== Parameter Properties ===");

/**
 * Parameter properties = declare and initialize in constructor
 * Shorter syntax for common pattern
 */

// Without parameter properties
class User1 {
    name: string;
    email: string;
    
    constructor(name: string, email: string) {
        this.name = name;
        this.email = email;
    }
}

// With parameter properties (equivalent)
class User2 {
    constructor(
        public name: string,
        public email: string,
        private password: string
    ) {}
    
    validatePassword(input: string): boolean {
        return this.password === input;
    }
}

const user = new User2("Alice", "alice@example.com", "secret123");
console.log("User:", user.name, user.email);
// console.log(user.password);  // Error: private


// ============================================================================
// 4. READONLY MODIFIER
// ============================================================================

console.log("\n=== Readonly ===");

class Config {
    readonly apiUrl: string;
    readonly timeout: number;
    retries: number;
    
    constructor(apiUrl: string, timeout: number, retries: number) {
        this.apiUrl = apiUrl;
        this.timeout = timeout;
        this.retries = retries;
    }
    
    updateRetries(newRetries: number): void {
        this.retries = newRetries;  // OK
        // this.timeout = 5000;  // Error: readonly
    }
}

const config = new Config("https://api.example.com", 3000, 3);
// config.apiUrl = "new";  // Error: readonly
config.retries = 5;  // OK


// ============================================================================
// 5. GETTERS AND SETTERS
// ============================================================================

console.log("\n=== Getters and Setters ===");

class Temperature {
    private _celsius: number = 0;
    
    get celsius(): number {
        return this._celsius;
    }
    
    set celsius(value: number) {
        if (value < -273.15) {
            throw new Error("Temperature below absolute zero");
        }
        this._celsius = value;
    }
    
    get fahrenheit(): number {
        return this._celsius * 9/5 + 32;
    }
    
    set fahrenheit(value: number) {
        this.celsius = (value - 32) * 5/9;
    }
}

const temp = new Temperature();
temp.celsius = 25;
console.log("Temperature:", temp.celsius, "C =", temp.fahrenheit.toFixed(1), "F");

temp.fahrenheit = 77;
console.log("Temperature:", temp.celsius.toFixed(1), "C =", temp.fahrenheit, "F");


// ============================================================================
// 6. STATIC MEMBERS
// ============================================================================

console.log("\n=== Static Members ===");

class MathUtils {
    static PI: number = 3.14159;
    
    static add(a: number, b: number): number {
        return a + b;
    }
    
    static multiply(a: number, b: number): number {
        return a * b;
    }
    
    // Static block (TS 4.4+)
    static {
        console.log("  MathUtils initialized");
    }
}

// Call on class, not instance
console.log("Static add:", MathUtils.add(5, 3));
console.log("Static PI:", MathUtils.PI);


// ============================================================================
// 7. ABSTRACT CLASSES
// ============================================================================

console.log("\n=== Abstract Classes ===");

/**
 * Abstract classes:
 * - Cannot be instantiated directly
 * - Can have abstract methods (must be implemented by subclass)
 * - Can have concrete methods (inherited by subclass)
 */

abstract class Shape {
    constructor(public name: string) {}
    
    // Abstract method (no implementation)
    abstract area(): number;
    abstract perimeter(): number;
    
    // Concrete method
    describe(): string {
        return `${this.name} with area ${this.area().toFixed(2)}`;
    }
}

class Circle extends Shape {
    constructor(public radius: number) {
        super("Circle");
    }
    
    area(): number {
        return Math.PI * this.radius ** 2;
    }
    
    perimeter(): number {
        return 2 * Math.PI * this.radius;
    }
}

class Rectangle extends Shape {
    constructor(public width: number, public height: number) {
        super("Rectangle");
    }
    
    area(): number {
        return this.width * this.height;
    }
    
    perimeter(): number {
        return 2 * (this.width + this.height);
    }
}

const circle = new Circle(5);
const rectangle = new Rectangle(4, 6);

console.log(circle.describe());
console.log(rectangle.describe());

// const shape = new Shape("Test");  // Error: Cannot create instance of abstract class


// ============================================================================
// 8. IMPLEMENTING INTERFACES
// ============================================================================

console.log("\n=== Implementing Interfaces ===");

interface Drawable {
    draw(): void;
}

interface Movable {
    move(x: number, y: number): void;
}

// Implement single interface
class Point implements Drawable {
    constructor(public x: number, public y: number) {}
    
    draw(): void {
        console.log(`  Drawing point at (${this.x}, ${this.y})`);
    }
}

// Implement multiple interfaces
class Sprite implements Drawable, Movable {
    constructor(public x: number, public y: number) {}
    
    draw(): void {
        console.log(`  Drawing sprite at (${this.x}, ${this.y})`);
    }
    
    move(x: number, y: number): void {
        this.x = x;
        this.y = y;
    }
}

const sprite = new Sprite(0, 0);
sprite.draw();
sprite.move(10, 20);
sprite.draw();


// ============================================================================
// 9. GENERIC CLASSES
// ============================================================================

console.log("\n=== Generic Classes ===");

class Stack<T> {
    private items: T[] = [];
    
    push(item: T): void {
        this.items.push(item);
    }
    
    pop(): T | undefined {
        return this.items.pop();
    }
    
    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }
    
    size(): number {
        return this.items.length;
    }
    
    isEmpty(): boolean {
        return this.items.length === 0;
    }
}

const numberStack = new Stack<number>();
numberStack.push(1);
numberStack.push(2);
numberStack.push(3);
console.log("Stack size:", numberStack.size());
console.log("Popped:", numberStack.pop());

const stringStack = new Stack<string>();
stringStack.push("a");
stringStack.push("b");
console.log("String stack peek:", stringStack.peek());


// ============================================================================
// 10. PRIVATE FIELDS (ECMAScript #)
// ============================================================================

console.log("\n=== Private Fields (#) ===");

/**
 * # private fields (JavaScript feature)
 * - Truly private (not accessible via bracket notation)
 * - Different from TypeScript private
 */

class Counter {
    #count: number = 0;  // ECMAScript private
    
    increment(): void {
        this.#count++;
    }
    
    getCount(): number {
        return this.#count;
    }
}

const counter = new Counter();
counter.increment();
console.log("Count:", counter.getCount());
// console.log(counter.#count);  // Syntax error!


// ============================================================================
// 11. THIS TYPES
// ============================================================================

console.log("\n=== This Types ===");

class Calculator {
    constructor(public value: number = 0) {}
    
    add(n: number): this {
        this.value += n;
        return this;
    }
    
    multiply(n: number): this {
        this.value *= n;
        return this;
    }
    
    getValue(): number {
        return this.value;
    }
}

// Method chaining
const result = new Calculator()
    .add(10)
    .multiply(2)
    .add(5)
    .getValue();

console.log("Chained result:", result);

// this type allows inheritance to return correct type
class ScientificCalculator extends Calculator {
    square(): this {
        this.value = this.value ** 2;
        return this;
    }
}

const sciCalc = new ScientificCalculator()
    .add(3)
    .square()  // Returns ScientificCalculator
    .multiply(2)
    .getValue();

console.log("Scientific calc:", sciCalc);


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

/**
 * CLASS BEST PRACTICES:
 * 
 * 1. USE PUBLIC, PRIVATE, PROTECTED APPROPRIATELY
 *    Mark intention clearly
 * 
 * 2. PREFER READONLY FOR IMMUTABLE PROPERTIES
 *    Prevents accidental modification
 * 
 * 3. USE PARAMETER PROPERTIES
 *    Reduces boilerplate
 * 
 * 4. IMPLEMENT INTERFACES
 *    Clear contracts
 * 
 * 5. ABSTRACT CLASSES FOR SHARED BEHAVIOR
 *    Code reuse with type safety
 * 
 * 6. GENERIC CLASSES FOR REUSABILITY
 *    Type-safe containers
 * 
 * 7. USE GETTERS/SETTERS FOR COMPUTED/VALIDATED PROPERTIES
 *    Encapsulation
 * 
 * 8. RETURN 'THIS' FOR CHAINING
 *    Fluent interfaces
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Access modifiers: public, private, protected");
console.log("2. readonly prevents modification after initialization");
console.log("3. Parameter properties reduce boilerplate");
console.log("4. Abstract classes enforce implementation");
console.log("5. implements for interface contracts");
console.log("6. Generic classes for type-safe containers");
console.log("7. Getters/setters for encapsulation");
console.log("8. Static members belong to class");
console.log("9. # for ECMAScript private fields");
console.log("10. this type enables proper method chaining");
console.log("=".repeat(80));

export {};
