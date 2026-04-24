/**
 * JAVASCRIPT OBJECTS AND PROTOTYPES
 * ===================================
 * Comprehensive guide to objects in JavaScript
 * From basics to prototypal inheritance
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT OBJECTS AND PROTOTYPES");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. OBJECT BASICS
// ============================================================================

/**
 * Objects are collections of key-value pairs
 * - Keys are strings or Symbols
 * - Values can be any type
 * - Reference type (mutable)
 */

console.log("\n=== Creating Objects ===");

// Object literal (most common)
const person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

// Object constructor
const person2 = new Object();
person2.name = "Bob";
person2.age = 25;

// Object.create()
const person3 = Object.create(null);  // No prototype
person3.name = "Charlie";

// Constructor function (old way)
function Person(name, age) {
    this.name = name;
    this.age = age;
}
const person4 = new Person("David", 35);

console.log("Literal:", person);
console.log("Constructor:", person2);
console.log("Object.create:", person3);
console.log("Function constructor:", person4);


// ============================================================================
// 2. ACCESSING PROPERTIES
// ============================================================================

console.log("\n=== Accessing Properties ===");

const user = {
    firstName: "John",
    lastName: "Doe",
    age: 28,
    "full name": "John Doe"  // Key with space
};

// Dot notation
console.log("Dot notation:", user.firstName);

// Bracket notation
console.log("Bracket notation:", user["lastName"]);
console.log("Key with space:", user["full name"]);

// Dynamic property access
const prop = "age";
console.log("Dynamic:", user[prop]);

// Optional chaining (?.) - ES2020
const address = user.address?.street?.name;
console.log("Optional chaining:", address);  // undefined, no error


// ============================================================================
// 3. ADDING, MODIFYING, DELETING PROPERTIES
// ============================================================================

console.log("\n=== Modifying Objects ===");

const car = {
    brand: "Toyota",
    model: "Camry"
};

// Adding property
car.year = 2020;
car["color"] = "blue";
console.log("After adding:", car);

// Modifying property
car.model = "Corolla";
console.log("After modifying:", car);

// Deleting property
delete car.color;
console.log("After deleting:", car);

// Checking if property exists
console.log("Has 'brand':", "brand" in car);
console.log("Has 'color':", "color" in car);
console.log("Has 'brand' (own):", car.hasOwnProperty("brand"));


// ============================================================================
// 4. OBJECT METHODS
// ============================================================================

console.log("\n=== Object Methods ===");

const calculator = {
    value: 0,
    
    add(n) {
        this.value += n;
        return this;  // For chaining
    },
    
    subtract(n) {
        this.value -= n;
        return this;
    },
    
    multiply(n) {
        this.value *= n;
        return this;
    },
    
    reset() {
        this.value = 0;
        return this;
    },
    
    getValue() {
        return this.value;
    }
};

// Method chaining
const result = calculator
    .add(10)
    .multiply(2)
    .subtract(5)
    .getValue();
console.log("Chained result:", result);


// ============================================================================
// 5. THIS KEYWORD
// ============================================================================

console.log("\n=== 'this' Keyword ===");

const obj = {
    value: 42,
    
    regularMethod() {
        console.log("Regular method 'this':", this.value);
    },
    
    arrowMethod: () => {
        // Arrow functions don't have their own 'this'
        console.log("Arrow method 'this':", this.value);  // undefined
    },
    
    nested() {
        const inner = () => {
            // Arrow function inherits 'this' from outer function
            console.log("Nested arrow 'this':", this.value);
        };
        inner();
    }
};

obj.regularMethod();
obj.arrowMethod();
obj.nested();

// Losing 'this' context
const standalone = obj.regularMethod;
// standalone();  // Error or undefined - 'this' is lost

// Fixing with bind
const bound = obj.regularMethod.bind(obj);
bound();  // Works!


// ============================================================================
// 6. OBJECT DESTRUCTURING
// ============================================================================

console.log("\n=== Object Destructuring ===");

const employee = {
    empName: "Alice",
    empAge: 30,
    empCity: "Boston",
    empSalary: 75000
};

// Basic destructuring
const { empName, empAge } = employee;
console.log("Destructured:", empName, empAge);

// Renaming variables
const { empName: name, empAge: age } = employee;
console.log("Renamed:", name, age);

// Default values
const { empCity, empCountry = "USA" } = employee;
console.log("With defaults:", empCity, empCountry);

// Rest pattern
const { empName: n, ...rest } = employee;
console.log("Rest:", rest);

// Nested destructuring
const company = {
    name: "TechCorp",
    location: {
        city: "San Francisco",
        state: "CA"
    }
};
const { location: { city, state } } = company;
console.log("Nested:", city, state);


// ============================================================================
// 7. OBJECT SPREAD OPERATOR
// ============================================================================

console.log("\n=== Spread Operator ===");

const defaults = { theme: "light", language: "en" };
const userSettings = { language: "es", notifications: true };

// Merging objects (later properties override earlier)
const settings = { ...defaults, ...userSettings };
console.log("Merged:", settings);

// Shallow copy
const original = { a: 1, b: 2 };
const copy = { ...original };
console.log("Copy:", copy);

// Adding properties
const enhanced = { ...original, c: 3, d: 4 };
console.log("Enhanced:", enhanced);


// ============================================================================
// 8. OBJECT METHODS (STATIC)
// ============================================================================

console.log("\n=== Object Static Methods ===");

const obj2 = {
    name: "Test",
    age: 25,
    city: "NYC"
};

// Object.keys() - Returns array of keys
console.log("Keys:", Object.keys(obj2));

// Object.values() - Returns array of values
console.log("Values:", Object.values(obj2));

// Object.entries() - Returns array of [key, value] pairs
console.log("Entries:", Object.entries(obj2));

// Object.fromEntries() - Creates object from entries
const entries = [["a", 1], ["b", 2]];
const fromEntries = Object.fromEntries(entries);
console.log("From entries:", fromEntries);

// Object.assign() - Copy/merge objects (mutates target)
const target = { a: 1 };
const source1 = { b: 2 };
const source2 = { c: 3 };
Object.assign(target, source1, source2);
console.log("Assigned:", target);

// Object.freeze() - Prevent modifications
const frozen = Object.freeze({ value: 42 });
// frozen.value = 100;  // Silently fails (or throws in strict mode)
console.log("Frozen:", frozen);

// Object.seal() - Prevent adding/removing properties
const sealed = Object.seal({ value: 42 });
sealed.value = 100;  // Can modify existing
// sealed.newProp = 1;  // Can't add new
console.log("Sealed:", sealed);

// Object.isFrozen(), Object.isSealed()
console.log("Is frozen?", Object.isFrozen(frozen));
console.log("Is sealed?", Object.isSealed(sealed));


// ============================================================================
// 9. PROPERTY DESCRIPTORS
// ============================================================================

console.log("\n=== Property Descriptors ===");

const obj3 = {};

// Define property with descriptor
Object.defineProperty(obj3, "name", {
    value: "Test",
    writable: false,      // Can't change value
    enumerable: true,     // Shows in for...in
    configurable: false   // Can't delete or reconfigure
});

console.log("Object:", obj3);
// obj3.name = "New";  // Fails silently or throws
console.log("After trying to modify:", obj3.name);

// Get property descriptor
const descriptor = Object.getOwnPropertyDescriptor(obj3, "name");
console.log("Descriptor:", descriptor);

// Define multiple properties
Object.defineProperties(obj3, {
    age: {
        value: 25,
        writable: true,
        enumerable: true
    },
    hidden: {
        value: "secret",
        enumerable: false  // Won't show in Object.keys()
    }
});

console.log("Keys:", Object.keys(obj3));  // Only 'name' and 'age'
console.log("All properties:", Object.getOwnPropertyNames(obj3));


// ============================================================================
// 10. GETTERS AND SETTERS
// ============================================================================

console.log("\n=== Getters and Setters ===");

const account = {
    _balance: 1000,  // Convention: underscore for "private"
    
    get balance() {
        return this._balance;
    },
    
    set balance(amount) {
        if (amount < 0) {
            throw new Error("Balance cannot be negative");
        }
        this._balance = amount;
    },
    
    deposit(amount) {
        this.balance = this._balance + amount;
    },
    
    withdraw(amount) {
        this.balance = this._balance - amount;
    }
};

console.log("Balance:", account.balance);  // Uses getter
account.deposit(500);
console.log("After deposit:", account.balance);
account.withdraw(200);
console.log("After withdrawal:", account.balance);


// ============================================================================
// 11. PROTOTYPES
// ============================================================================

console.log("\n=== Prototypes ===");

/**
 * Every object has an internal [[Prototype]] property
 * - Accessed via __proto__ or Object.getPrototypeOf()
 * - Forms the prototype chain
 * - Used for inheritance
 */

// Constructor function and prototype
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    console.log(`${this.name} makes a sound`);
};

const dog = new Animal("Dog");
dog.speak();

// Checking prototype
console.log("Prototype:", Object.getPrototypeOf(dog) === Animal.prototype);
console.log("Is instance?", dog instanceof Animal);

// Prototype chain
console.log("dog.__proto__:", dog.__proto__ === Animal.prototype);
console.log("Animal.prototype.__proto__:", Animal.prototype.__proto__ === Object.prototype);
console.log("Object.prototype.__proto__:", Object.prototype.__proto__);  // null


// ============================================================================
// 12. PROTOTYPAL INHERITANCE
// ============================================================================

console.log("\n=== Prototypal Inheritance ===");

// Parent constructor
function Vehicle(type) {
    this.type = type;
}

Vehicle.prototype.describe = function() {
    return `This is a ${this.type}`;
};

// Child constructor
function Car(brand, model) {
    Vehicle.call(this, "car");  // Call parent constructor
    this.brand = brand;
    this.model = model;
}

// Set up inheritance
Car.prototype = Object.create(Vehicle.prototype);
Car.prototype.constructor = Car;

// Add child methods
Car.prototype.getInfo = function() {
    return `${this.brand} ${this.model}`;
};

const myCar = new Car("Toyota", "Camry");
console.log("Info:", myCar.getInfo());
console.log("Describe:", myCar.describe());  // Inherited
console.log("Is Vehicle?", myCar instanceof Vehicle);


// ============================================================================
// 13. OBJECT ITERATION
// ============================================================================

console.log("\n=== Object Iteration ===");

const person5 = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

// for...in (includes inherited enumerable properties)
console.log("for...in:");
for (let key in person5) {
    if (person5.hasOwnProperty(key)) {  // Only own properties
        console.log(`  ${key}: ${person5[key]}`);
    }
}

// Object.keys() + forEach
console.log("Object.keys + forEach:");
Object.keys(person5).forEach(key => {
    console.log(`  ${key}: ${person5[key]}`);
});

// Object.entries() + for...of
console.log("Object.entries + for...of:");
for (const [key, value] of Object.entries(person5)) {
    console.log(`  ${key}: ${value}`);
}


// ============================================================================
// 14. ADVANCED PATTERNS
// ============================================================================

console.log("\n=== Advanced Patterns ===");

// Computed property names
const propName = "dynamicKey";
const obj4 = {
    [propName]: "value",
    [`${propName}2`]: "value2"
};
console.log("Computed properties:", obj4);

// Property shorthand
const x = 10, y = 20;
const point = { x, y };  // Same as { x: x, y: y }
console.log("Shorthand:", point);

// Method shorthand
const obj5 = {
    // Old way: method: function() { }
    // New way:
    method() {
        return "result";
    }
};

// Symbols as keys (for truly private properties)
const privateKey = Symbol("private");
const obj6 = {
    publicProp: "visible",
    [privateKey]: "hidden"
};
console.log("Public:", obj6.publicProp);
console.log("Symbol:", obj6[privateKey]);
console.log("Keys (no symbol):", Object.keys(obj6));
console.log("Symbols:", Object.getOwnPropertySymbols(obj6));


// ============================================================================
// 15. COMMON PITFALLS
// ============================================================================

console.log("\n=== Common Pitfalls ===");

// 1. Objects are reference types
const obj7 = { value: 1 };
const ref = obj7;
ref.value = 2;
console.log("Original changed:", obj7.value);  // 2

// 2. Shallow copy only copies first level
const nested = { a: 1, b: { c: 2 } };
const shallowCopy = { ...nested };
shallowCopy.b.c = 99;
console.log("Original nested changed:", nested.b.c);  // 99

// 3. this binding can be lost
const obj8 = {
    value: 42,
    getValue() { return this.value; }
};
const getValueStandalone = obj8.getValue;
// console.log(getValueStandalone());  // undefined or error

// 4. for...in includes inherited properties
function Parent() {}
Parent.prototype.inherited = "yes";
const child = new Parent();
child.own = "yes";

for (let key in child) {
    console.log(key);  // Shows both 'own' and 'inherited'
}

// Use hasOwnProperty() to filter
for (let key in child) {
    if (child.hasOwnProperty(key)) {
        console.log("Own:", key);
    }
}


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Objects are reference types (mutable)");
console.log("2. Use dot notation for known properties, bracket for dynamic");
console.log("3. Understand 'this' binding (use arrow functions or bind)");
console.log("4. Spread operator creates shallow copies");
console.log("5. Prototypes enable inheritance");
console.log("6. Use Object.freeze() to make immutable");
console.log("7. Getters/setters for computed properties");
console.log("8. hasOwnProperty() to check own properties");
console.log("=".repeat(80));
