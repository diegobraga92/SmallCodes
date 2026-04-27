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

/**
 * OBJECT CREATION METHODS - WHEN TO USE EACH:
 * ===========================================
 * 
 * 1. OBJECT LITERAL { } - USE 99% OF THE TIME
 *    - Simple, concise syntax
 *    - Best for single objects or data structures
 *    - Prototype: Object.prototype
 * 
 * 2. NEW OBJECT() - AVOID (UNNECESSARY)
 *    - Same as literal but more verbose
 *    - No advantage over { }
 * 
 * 3. OBJECT.CREATE(proto) - USE FOR SPECIFIC PROTOTYPES
 *    - When you need a specific prototype
 *    - Object.create(null) for dictionary without inherited properties
 *    - Useful for prototypal inheritance
 * 
 * 4. CONSTRUCTOR FUNCTION - USE FOR MULTIPLE INSTANCES (legacy)
 *    - When you need multiple objects with same structure
 *    - Prototypal inheritance
 *    - Modern alternative: ES6 classes
 */

// 1. Object literal (most common and recommended)
const person = {
    name: "Alice",
    age: 30,
    city: "New York"
};
// WHEN: Single object, data structure, configuration
// PROS: Simple, concise, easy to read
// CONS: Can't create multiple instances easily

// 2. Object constructor (verbose, avoid)
const person2 = new Object();
person2.name = "Bob";
person2.age = 25;
// WHEN: Never use this, literal is better
// CONS: More verbose than literal

// 3. Object.create() - for specific prototypes
const person3 = Object.create(null);  // No prototype at all!
person3.name = "Charlie";
// WHEN: Need object without inherited properties (true dictionary)
// PROS: Clean object, no pollution from Object.prototype
// CONS: Loses useful methods like hasOwnProperty()

// Example: true dictionary without prototype pollution
const dictionary = Object.create(null);
dictionary.toString = "my value";  // Won't conflict with Object.prototype.toString
console.log("Dictionary keys:", Object.keys(dictionary));  // ["toString"]

// 4. Constructor function (old way before ES6 classes)
function Person(name, age) {
    // Called with 'new', 'this' refers to new object
    this.name = name;
    this.age = age;
}
// Add methods to prototype (shared by all instances)
Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

const person4 = new Person("David", 35);
// WHEN: Need multiple objects with same structure (use ES6 classes instead)
// PROS: Memory efficient (methods on prototype)
// CONS: Verbose, ES6 classes are cleaner

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

/**
 * THE 'this' KEYWORD - FOUR BINDING RULES:
 * =========================================
 * 
 * 1. DEFAULT BINDING (standalone function):
 *    - In non-strict mode: 'this' refers to global object (window/globalThis)
 *    - In strict mode: 'this' is undefined
 * 
 * 2. IMPLICIT BINDING (method call):
 *    - 'this' refers to the object before the dot
 *    - obj.method() → 'this' is obj
 * 
 * 3. EXPLICIT BINDING (call/apply/bind):
 *    - Manually set 'this' using call(), apply(), or bind()
 *    - func.call(obj) → 'this' is obj
 * 
 * 4. NEW BINDING (constructor):
 *    - new Func() → 'this' is the new object being created
 * 
 * PRIORITY: new > explicit > implicit > default
 * 
 * ARROW FUNCTIONS:
 * - Don't have their own 'this'
 * - Inherit 'this' from enclosing lexical scope
 * - Cannot be used with call/apply/bind or as constructors
 */

const obj = {
    value: 42,
    
    // Regular method: 'this' determined at call time (implicit binding)
    regularMethod() {
        // 'this' refers to obj when called as obj.regularMethod()
        console.log("Regular method 'this':", this.value);
    },
    
    // Arrow function: 'this' captured from enclosing scope
    arrowMethod: () => {
        // Arrow functions DON'T have their own 'this'
        // 'this' here refers to the scope where 'obj' was defined (global scope)
        // In browser: 'this' would be window
        // In Node.js: 'this' would be the module exports
        console.log("Arrow method 'this':", this.value);  // undefined
    },
    
    // Nested function example
    nested() {
        // 'this' here is obj (implicit binding)
        const inner = () => {
            // Arrow function INHERITS 'this' from enclosing function
            // Since outer 'this' is obj, inner 'this' is also obj
            // This is why arrow functions are useful in callbacks!
            console.log("Nested arrow 'this':", this.value);
        };
        inner();
    }
};

// IMPLICIT BINDING: 'this' is obj
obj.regularMethod();

// Arrow function: 'this' is from definition scope, not obj
obj.arrowMethod();

// Nested arrow inherits 'this'
obj.nested();

// COMMON PITFALL: Losing 'this' context
const standalone = obj.regularMethod;
// standalone();  // Error or undefined!
// WHY? When assigned to standalone, the function loses its connection to obj
// When called as standalone(), there's no object before the dot
// This falls back to DEFAULT BINDING (undefined in strict mode)

// FIX 1: Use bind() to permanently attach 'this'
const bound = obj.regularMethod.bind(obj);
bound();  // Works! 'this' is permanently set to obj

// FIX 2: Use an arrow function wrapper
const wrapper = () => obj.regularMethod();
wrapper();  // Works! Calls through obj

// EXPLICIT BINDING examples
function greet(greeting, punctuation) {
    console.log(`${greeting}, ${this.name}${punctuation}`);
}

const person = { name: "Alice" };

// call() - arguments passed individually
greet.call(person, "Hello", "!");  // 'this' is person

// apply() - arguments passed as array
greet.apply(person, ["Hi", "!!"]);  // 'this' is person

// bind() - creates new function with 'this' pre-set
const boundGreet = greet.bind(person);
boundGreet("Hey", "...");  // 'this' is always person


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
 * JAVASCRIPT PROTOTYPAL INHERITANCE EXPLAINED:
 * ============================================
 * 
 * KEY CONCEPTS:
 * 
 * 1. [[Prototype]] (internal property):
 *    - Every object has a hidden [[Prototype]] link to another object
 *    - Accessed via __proto__ (deprecated) or Object.getPrototypeOf()
 *    - Forms a chain: obj → prototype → prototype → ... → null
 * 
 * 2. Constructor.prototype:
 *    - When you create a function, it gets a .prototype property (an object)
 *    - Objects created with 'new Constructor()' have their [[Prototype]]
 *      linked to Constructor.prototype
 *    - IMPORTANT: Constructor.prototype !== Constructor's [[Prototype]]
 * 
 * 3. Prototype Chain Lookup:
 *    - When accessing obj.prop, JS first looks at obj's own properties
 *    - If not found, looks at obj.[[Prototype]]
 *    - Continues up the chain until found or reaching null
 * 
 * 4. The 'new' Keyword:
 *    - Creates a new empty object
 *    - Sets its [[Prototype]] to Constructor.prototype
 *    - Calls Constructor with 'this' = new object
 *    - Returns the new object (unless constructor returns an object)
 * 
 * MENTAL MODEL:
 * Constructor Function ──has──> .prototype (object)
 *                                    ↑
 *                                    │ [[Prototype]] link
 *                                    │
 * new Constructor() ──creates──> instance object
 */

// Constructor function and prototype
function Animal(name) {
    // When called with 'new':
    // 1. A new object is created
    // 2. Its [[Prototype]] is set to Animal.prototype
    // 3. 'this' refers to the new object
    // 4. Properties are added to the new object
    this.name = name;  // Instance property (on the object itself)
}

// Add method to prototype (shared by all instances)
// WHY put methods on prototype? Memory efficiency!
// If we put speak() inside the constructor, every instance
// would get its own copy of the function
Animal.prototype.speak = function() {
    console.log(`${this.name} makes a sound`);
};

const dog = new Animal("Dog");
// When we call dog.speak():
// 1. JS looks for 'speak' on dog object → not found
// 2. JS looks on dog.[[Prototype]] (Animal.prototype) → found!
// 3. Calls the method with 'this' = dog
dog.speak();

// Checking prototype relationships
console.log("Prototype:", Object.getPrototypeOf(dog) === Animal.prototype);  // true
console.log("Is instance?", dog instanceof Animal);  // true
// instanceof checks: is Animal.prototype anywhere in dog's prototype chain?

// THE PROTOTYPE CHAIN:
console.log("dog.__proto__:", dog.__proto__ === Animal.prototype);  // true
// dog.__proto__ is Animal.prototype (first link)

console.log("Animal.prototype.__proto__:", Animal.prototype.__proto__ === Object.prototype);  // true
// Animal.prototype is itself an object, so its [[Prototype]] is Object.prototype

console.log("Object.prototype.__proto__:", Object.prototype.__proto__);  // null
// Object.prototype is the top of the chain, its [[Prototype]] is null

/**
 * FULL CHAIN VISUALIZATION:
 * 
 * dog object
 *   ↓ [[Prototype]]
 * Animal.prototype (has 'speak' method)
 *   ↓ [[Prototype]]
 * Object.prototype (has 'toString', 'hasOwnProperty', etc.)
 *   ↓ [[Prototype]]
 * null (end of chain)
 * 
 * Property lookup walks up this chain!
 */

// IMPORTANT DISTINCTION: .prototype vs [[Prototype]]
// Animal.prototype: The object that instances will inherit from
// dog.[[Prototype]]: The actual prototype link (points to Animal.prototype)

// Own properties vs inherited properties
console.log("dog.hasOwnProperty('name'):", dog.hasOwnProperty('name'));  // true
console.log("dog.hasOwnProperty('speak'):", dog.hasOwnProperty('speak'));  // false
// 'name' is on dog, 'speak' is on Animal.prototype


// ============================================================================
// 12. PROTOTYPAL INHERITANCE
// ============================================================================

console.log("\n=== Prototypal Inheritance ===");

/**
 * SETTING UP INHERITANCE IN JAVASCRIPT:
 * =====================================
 * 
 * GOAL: Make Car inherit from Vehicle
 * 
 * STEPS:
 * 1. Call parent constructor (for instance properties)
 * 2. Link prototypes (for inherited methods)
 * 3. Fix constructor property
 * 
 * WHY THIS WORKS:
 * - Vehicle.call(this, ...) sets up instance properties
 * - Object.create(Vehicle.prototype) creates a new object with
 *   Vehicle.prototype as its [[Prototype]]
 * - This creates the chain: Car.prototype → Vehicle.prototype → Object.prototype
 * 
 * COMMON MISTAKE: Car.prototype = Vehicle.prototype
 * - This makes them the SAME object (not a chain!)
 * - Adding methods to Car.prototype would add them to Vehicle.prototype too
 * 
 * MODERN ALTERNATIVE: Use ES6 classes (cleaner syntax, same mechanism)
 */

// Parent constructor
function Vehicle(type) {
    // Instance properties (unique to each object)
    this.type = type;
}

// Parent methods (shared via prototype)
Vehicle.prototype.describe = function() {
    return `This is a ${this.type}`;
};

// Child constructor
function Car(brand, model) {
    // STEP 1: Call parent constructor to inherit instance properties
    // Vehicle.call(this, "car") is equivalent to:
    // - Setting 'this' to the new Car instance
    // - Running Vehicle's code: this.type = "car"
    // - This ensures Car instances get Vehicle's properties
    Vehicle.call(this, "car");  
    
    // Add Car-specific instance properties
    this.brand = brand;
    this.model = model;
}

// STEP 2: Set up prototype chain for method inheritance
// WRONG: Car.prototype = Vehicle.prototype (makes them same object!)
// WRONG: Car.prototype = new Vehicle() (calls constructor unnecessarily)
// RIGHT: Car.prototype = Object.create(Vehicle.prototype)
Car.prototype = Object.create(Vehicle.prototype);

// STEP 3: Fix constructor property
// After Object.create(), Car.prototype.constructor points to Vehicle
// We need to fix it to point back to Car
Car.prototype.constructor = Car;

// Add child-specific methods
// These go on Car.prototype, NOT Vehicle.prototype
Car.prototype.getInfo = function() {
    return `${this.brand} ${this.model}`;
};

const myCar = new Car("Toyota", "Camry");

// getInfo is on Car.prototype (found immediately)
console.log("Info:", myCar.getInfo());

// describe is on Vehicle.prototype (found via prototype chain)
// Lookup: myCar → Car.prototype → Vehicle.prototype → found!
console.log("Describe:", myCar.describe());

// instanceof walks the prototype chain
console.log("Is Car?", myCar instanceof Car);  // true
console.log("Is Vehicle?", myCar instanceof Vehicle);  // true
console.log("Is Object?", myCar instanceof Object);  // true

/**
 * PROTOTYPE CHAIN FOR myCar:
 * 
 * myCar
 *   ↓ [[Prototype]]
 * Car.prototype (has getInfo)
 *   ↓ [[Prototype]]
 * Vehicle.prototype (has describe)
 *   ↓ [[Prototype]]
 * Object.prototype
 *   ↓ [[Prototype]]
 * null
 * 
 * WHEN TO USE:
 * - Use prototypal inheritance when you need classical inheritance patterns
 * - Consider composition over inheritance for most cases
 * - Modern code: use ES6 classes (they do this internally)
 */


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
