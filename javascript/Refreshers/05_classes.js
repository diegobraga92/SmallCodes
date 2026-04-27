/**
 * JAVASCRIPT CLASSES AND INHERITANCE
 * ====================================
 * Comprehensive guide to ES6 classes
 * Syntactic sugar over prototypal inheritance
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT CLASSES AND INHERITANCE");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. CLASS BASICS
// ============================================================================

/**
 * ES6 CLASSES vs CONSTRUCTOR FUNCTIONS:
 * =====================================
 * 
 * Classes are "syntactic sugar" over constructor functions
 * - They use the same prototypal inheritance underneath
 * - Just a cleaner, more familiar syntax (especially for OOP devs)
 * - NOT a new inheritance model!
 * 
 * CONSTRUCTOR FUNCTION (old way):
 * function Person(name) {
 *     this.name = name;
 * }
 * Person.prototype.greet = function() {
 *     return `Hello, I'm ${this.name}`;
 * };
 * 
 * ES6 CLASS (new way):
 * class Person {
 *     constructor(name) {
 *         this.name = name;
 *     }
 *     greet() {
 *         return `Hello, I'm ${this.name}`;
 *     }
 * }
 * 
 * BOTH CREATE THE SAME PROTOTYPE CHAIN!
 * 
 * ADVANTAGES OF CLASSES:
 * ✓ Cleaner, more intuitive syntax
 * ✓ Easier to set up inheritance (extends/super)
 * ✓ Must use 'new' (throws error if forgotten)
 * ✓ Methods are non-enumerable by default
 * ✓ Easier to read and maintain
 * ✓ Better TypeScript integration
 * 
 * WHEN TO USE CLASSES:
 * - New code (ES6+)
 * - When you need inheritance
 * - Working with frameworks (React components, etc.)
 * - Team prefers OOP style
 * 
 * WHEN TO USE CONSTRUCTOR FUNCTIONS:
 * - Legacy code compatibility
 * - Very simple objects (consider factory functions instead)
 */

console.log("\n=== Basic Class ===");

class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        return `Hello, I'm ${this.name}`;
    }
    
    getAge() {
        return this.age;
    }
}

const person1 = new Person("Alice", 30);
console.log(person1.greet());
console.log("Age:", person1.getAge());

// Must use 'new' keyword
// const person2 = Person("Bob", 25);  // Error!


// ============================================================================
// 2. GETTERS AND SETTERS
// ============================================================================

console.log("\n=== Getters and Setters ===");

class Rectangle {
    constructor(width, height) {
        this._width = width;
        this._height = height;
    }
    
    // Getter
    get area() {
        return this._width * this._height;
    }
    
    get perimeter() {
        return 2 * (this._width + this._height);
    }
    
    // Setter with validation
    set width(value) {
        if (value <= 0) {
            throw new Error("Width must be positive");
        }
        this._width = value;
    }
    
    set height(value) {
        if (value <= 0) {
            throw new Error("Height must be positive");
        }
        this._height = value;
    }
    
    get width() {
        return this._width;
    }
    
    get height() {
        return this._height;
    }
}

const rect = new Rectangle(10, 5);
console.log("Area:", rect.area);  // Uses getter
console.log("Perimeter:", rect.perimeter);

rect.width = 20;  // Uses setter
console.log("New area:", rect.area);


// ============================================================================
// 3. STATIC METHODS AND PROPERTIES
// ============================================================================

console.log("\n=== Static Members ===");

class MathUtils {
    // Static method
    static add(a, b) {
        return a + b;
    }
    
    static multiply(a, b) {
        return a * b;
    }
    
    // Static property
    static PI = 3.14159;
    
    // Static block (ES2022)
    static {
        console.log("  MathUtils class initialized");
    }
}

// Call on class, not instance
console.log("Add:", MathUtils.add(5, 3));
console.log("PI:", MathUtils.PI);

// Can't call on instance
const utils = new MathUtils();
// console.log(utils.add(1, 2));  // Error!


// ============================================================================
// 4. CLASS INHERITANCE
// ============================================================================

console.log("\n=== Inheritance ===");

// Parent class
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        return `${this.name} makes a sound`;
    }
    
    sleep() {
        return `${this.name} is sleeping`;
    }
}

// Child class
class Dog extends Animal {
    constructor(name, breed) {
        super(name);  // Call parent constructor
        this.breed = breed;
    }
    
    // Override parent method
    speak() {
        return `${this.name} barks`;
    }
    
    // New method
    fetch() {
        return `${this.name} fetches the ball`;
    }
}

const dog = new Dog("Rex", "Golden Retriever");
console.log(dog.speak());  // Overridden
console.log(dog.sleep());  // Inherited
console.log(dog.fetch());  // New method
console.log("Breed:", dog.breed);


// ============================================================================
// 5. SUPER KEYWORD
// ============================================================================

console.log("\n=== Super Keyword ===");

class Vehicle {
    constructor(type) {
        this.type = type;
    }
    
    describe() {
        return `This is a ${this.type}`;
    }
}

class Car extends Vehicle {
    constructor(brand, model) {
        super("car");  // Call parent constructor
        this.brand = brand;
        this.model = model;
    }
    
    describe() {
        // Call parent method
        const baseDescription = super.describe();
        return `${baseDescription} - ${this.brand} ${this.model}`;
    }
}

const car = new Car("Toyota", "Camry");
console.log(car.describe());


// ============================================================================
// 6. PRIVATE FIELDS (ES2022)
// ============================================================================

console.log("\n=== Private Fields ===");

class BankAccount {
    // Private field (# prefix)
    #balance = 0;
    #accountNumber;
    
    constructor(accountNumber, initialBalance = 0) {
        this.#accountNumber = accountNumber;
        this.#balance = initialBalance;
    }
    
    deposit(amount) {
        if (amount > 0) {
            this.#balance += amount;
            return true;
        }
        return false;
    }
    
    withdraw(amount) {
        if (amount > 0 && amount <= this.#balance) {
            this.#balance -= amount;
            return true;
        }
        return false;
    }
    
    getBalance() {
        return this.#balance;
    }
    
    // Private method
    #validateTransaction(amount) {
        return amount > 0 && amount <= this.#balance;
    }
}

const account = new BankAccount("12345", 1000);
account.deposit(500);
console.log("Balance:", account.getBalance());
// console.log(account.#balance);  // SyntaxError! Can't access private


// ============================================================================
// 7. STATIC PRIVATE FIELDS
// ============================================================================

console.log("\n=== Static Private Fields ===");

class Counter {
    static #count = 0;
    
    static increment() {
        this.#count++;
    }
    
    static getCount() {
        return this.#count;
    }
    
    static reset() {
        this.#count = 0;
    }
}

Counter.increment();
Counter.increment();
console.log("Count:", Counter.getCount());


// ============================================================================
// 8. CLASS EXPRESSIONS
// ============================================================================

console.log("\n=== Class Expressions ===");

// Named class expression
const MyClass = class NamedClass {
    constructor(value) {
        this.value = value;
    }
    
    getValue() {
        return this.value;
    }
};

const instance = new MyClass(42);
console.log("Value:", instance.getValue());

// Anonymous class expression
const AnotherClass = class {
    constructor(data) {
        this.data = data;
    }
};


// ============================================================================
// 9. INSTANCEOF AND CLASS CHECKING
// ============================================================================

console.log("\n=== Instance Checking ===");

class Parent {}
class Child extends Parent {}

const child = new Child();

console.log("child instanceof Child:", child instanceof Child);
console.log("child instanceof Parent:", child instanceof Parent);
console.log("child instanceof Object:", child instanceof Object);

// Check constructor
console.log("constructor:", child.constructor === Child);
console.log("constructor.name:", child.constructor.name);


// ============================================================================
// 10. MIXINS (COMPOSITION)
// ============================================================================

console.log("\n=== Mixins ===");

// Mixin pattern (since JS doesn't support multiple inheritance)
const CanEat = {
    eat(food) {
        return `${this.name} is eating ${food}`;
    }
};

const CanWalk = {
    walk() {
        return `${this.name} is walking`;
    }
};

const CanSwim = {
    swim() {
        return `${this.name} is swimming`;
    }
};

class Human {
    constructor(name) {
        this.name = name;
    }
}

// Apply mixins
Object.assign(Human.prototype, CanEat, CanWalk, CanSwim);

const human = new Human("John");
console.log(human.eat("pizza"));
console.log(human.walk());
console.log(human.swim());


// ============================================================================
// 11. ABSTRACT CLASS PATTERN
// ============================================================================

console.log("\n=== Abstract Class Pattern ===");

// JavaScript doesn't have abstract classes, but we can simulate them
class AbstractShape {
    constructor() {
        if (new.target === AbstractShape) {
            throw new Error("Cannot instantiate abstract class");
        }
    }
    
    // "Abstract" method (must be overridden)
    area() {
        throw new Error("Method 'area()' must be implemented");
    }
}

class Circle extends AbstractShape {
    constructor(radius) {
        super();
        this.radius = radius;
    }
    
    area() {
        return Math.PI * this.radius ** 2;
    }
}

const circle = new Circle(5);
console.log("Circle area:", circle.area().toFixed(2));

// const shape = new AbstractShape();  // Error!


// ============================================================================
// 12. METHOD CHAINING
// ============================================================================

console.log("\n=== Method Chaining ===");

class Calculator {
    constructor() {
        this.value = 0;
    }
    
    add(n) {
        this.value += n;
        return this;  // Return this for chaining
    }
    
    subtract(n) {
        this.value -= n;
        return this;
    }
    
    multiply(n) {
        this.value *= n;
        return this;
    }
    
    divide(n) {
        this.value /= n;
        return this;
    }
    
    getValue() {
        return this.value;
    }
}

const calc = new Calculator();
const result = calc
    .add(10)
    .multiply(2)
    .subtract(5)
    .divide(3)
    .getValue();

console.log("Chained result:", result);


// ============================================================================
// 13. CLASS VS CONSTRUCTOR FUNCTION
// ============================================================================

console.log("\n=== Class vs Constructor Function ===");

// Constructor function (old way)
function OldPerson(name, age) {
    this.name = name;
    this.age = age;
}

OldPerson.prototype.greet = function() {
    return `Hi, I'm ${this.name}`;
};

// Class (new way)
class NewPerson {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        return `Hi, I'm ${this.name}`;
    }
}

// Both work the same way
const oldPerson = new OldPerson("Alice", 30);
const newPerson = new NewPerson("Bob", 25);

console.log(oldPerson.greet());
console.log(newPerson.greet());

// Classes are NOT hoisted
// const early = new MyLaterClass();  // Error!
// class MyLaterClass {}


// ============================================================================
// 14. COMMON PATTERNS
// ============================================================================

console.log("\n=== Common Patterns ===");

// Singleton pattern
class Singleton {
    static #instance;
    
    constructor() {
        if (Singleton.#instance) {
            return Singleton.#instance;
        }
        Singleton.#instance = this;
    }
    
    static getInstance() {
        if (!Singleton.#instance) {
            Singleton.#instance = new Singleton();
        }
        return Singleton.#instance;
    }
}

const s1 = new Singleton();
const s2 = new Singleton();
console.log("Same instance?", s1 === s2);

// Factory pattern
class ShapeFactory {
    static createShape(type, ...args) {
        switch (type) {
            case "circle":
                return new Circle(...args);
            case "rectangle":
                return new Rectangle(...args);
            default:
                throw new Error("Unknown shape type");
        }
    }
}


// ============================================================================
// 15. COMMON PITFALLS
// ============================================================================

console.log("\n=== Common Pitfalls ===");

// 1. Forgetting 'new' keyword
class MyClass1 {
    constructor() {
        console.log("  Constructor called");
    }
}
// const instance1 = MyClass1();  // TypeError!
const instance2 = new MyClass1();  // Correct

// 2. 'this' binding in callbacks
class Button {
    constructor(label) {
        this.label = label;
    }
    
    click() {
        console.log(`  Button ${this.label} clicked`);
    }
    
    // Wrong way
    wrongSetup() {
        setTimeout(this.click, 100);  // 'this' will be lost
    }
    
    // Right way 1: Arrow function
    rightSetup1() {
        setTimeout(() => this.click(), 100);
    }
    
    // Right way 2: Bind
    rightSetup2() {
        setTimeout(this.click.bind(this), 100);
    }
}

const btn = new Button("Submit");
btn.rightSetup1();

// 3. Calling super() before accessing 'this'
class Base {}
class Derived extends Base {
    constructor() {
        // this.value = 1;  // Error! Must call super() first
        super();
        this.value = 1;  // Correct
    }
}


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Classes are syntactic sugar over prototypes");
console.log("2. Must use 'new' keyword to instantiate");
console.log("3. Use 'extends' for inheritance, 'super' to call parent");
console.log("4. Private fields start with # (ES2022)");
console.log("5. Static methods/properties belong to class, not instances");
console.log("6. Getters/setters for computed or validated properties");
console.log("7. Return 'this' from methods for chaining");
console.log("8. Be careful with 'this' binding in callbacks");
console.log("=".repeat(80));
