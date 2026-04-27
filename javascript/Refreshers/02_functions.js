/*
    JAVASCRIPT FUNCTIONS
    Covering: Function declarations, expressions, arrow functions, parameters,
    closures, IIFE, higher-order functions, this binding
    
    Functions are first-class citizens in JavaScript - they can be assigned to
    variables, passed as arguments, and returned from other functions.
*/

console.log("=== JavaScript Functions ===\n");

// ============================================================================
// 1. FUNCTION DECLARATIONS
// ============================================================================

console.log("============ FUNCTION DECLARATIONS ============\n");

/*
    FUNCTION DECLARATION SYNTAX:
    function name(parameters) {
        // function body
        return value;
    }
    
    - Hoisted (can be called before declaration)
    - Named function
    - Creates function-scoped variable
*/

// Basic function
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet("Alice"));

// Function with multiple parameters
function add(a, b) {
    return a + b;
}

console.log("add(5, 3):", add(5, 3));

// Function with default parameters (ES6)
function greetWithDefault(name = "Guest") {
    return `Hello, ${name}!`;
}

console.log(greetWithDefault());          // "Hello, Guest!"
console.log(greetWithDefault("Bob"));     // "Hello, Bob!"

// Function with rest parameters (ES6)
function sum(...numbers) {
    return numbers.reduce((total, num) => total + num, 0);
}

console.log("sum(1, 2, 3, 4):", sum(1, 2, 3, 4));

// Function hoisting
console.log("Hoisted:", hoistedFunction());  // Works!

function hoistedFunction() {
    return "I'm hoisted!";
}


// ============================================================================
// 2. FUNCTION EXPRESSIONS
// ============================================================================

console.log("\n============ FUNCTION EXPRESSIONS ============\n");

/*
    FUNCTION EXPRESSION SYNTAX:
    const name = function(parameters) {
        // function body
        return value;
    };
    
    - NOT hoisted
    - Can be anonymous or named
    - Assigned to variable
*/

// Anonymous function expression
const multiply = function(a, b) {
    return a * b;
};

console.log("multiply(4, 5):", multiply(4, 5));

// Named function expression (useful for debugging/recursion)
const factorial = function fact(n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);  // Can reference itself by name
};

console.log("factorial(5):", factorial(5));

// Function expressions are NOT hoisted
// console.log(notHoisted());  // Error!
const notHoisted = function() {
    return "Not hoisted";
};


// ============================================================================
// 3. ARROW FUNCTIONS (ES6)
// ============================================================================

console.log("\n============ ARROW FUNCTIONS ============\n");

/**
 * ARROW FUNCTIONS EXPLAINED:
 * ==========================
 * 
 * SYNTAX:
 * const name = (parameters) => expression;
 * const name = (parameters) => { statements; return value; };
 * 
 * KEY DIFFERENCES FROM REGULAR FUNCTIONS:
 * 
 * 1. LEXICAL 'this':
 *    - Don't have their own 'this'
 *    - Inherit 'this' from enclosing scope
 *    - Perfect for callbacks (no .bind() needed!)
 * 
 * 2. CANNOT BE CONSTRUCTORS:
 *    - Can't use 'new' with arrow functions
 *    - No prototype property
 * 
 * 3. NO 'arguments' OBJECT:
 *    - Use rest parameters (...args) instead
 * 
 * 4. NO 'super' OR 'new.target':
 *    - Limitations in class methods
 * 
 * WHEN TO USE ARROW FUNCTIONS:
 * ✓ Callbacks (map, filter, setTimeout, etc.)
 * ✓ Short, simple functions
 * ✓ When you need lexical 'this'
 * ✓ Functional programming patterns
 * 
 * WHEN NOT TO USE:
 * ✗ Object methods (need dynamic 'this')
 * ✗ Constructors
 * ✗ When you need 'arguments' object
 * ✗ Event handlers that need 'this' = element
 */

// Basic arrow function - implicit return
const square = (x) => x * x;  // Returns x * x automatically
console.log("square(5):", square(5));

// Single parameter - parentheses optional
const double = x => x * 2;  // Shorter syntax
console.log("double(5):", double(5));

// No parameters - parentheses required
const getRandom = () => Math.random();
console.log("random:", getRandom());

// Multiple parameters - parentheses required
const divide = (a, b) => a / b;
console.log("divide(10, 2):", divide(10, 2));

// Multiple statements - braces and explicit return required
const processNumber = (n) => {
    const doubled = n * 2;
    const squared = doubled * doubled;
    return squared;  // Must explicitly return
};
console.log("processNumber(3):", processNumber(3));

// Returning object literal - MUST wrap in parentheses
const createPerson = (name, age) => ({ name, age });
// Why? Without (), the { } looks like function body, not object!
// WRONG: const createPerson = (name, age) => { name, age };  // Syntax error
console.log("createPerson:", createPerson("Alice", 30));

// Arrow functions shine with array methods
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);        // Concise!
const evens = numbers.filter(n => n % 2 === 0); // Readable!
console.log("doubled:", doubled);
console.log("evens:", evens);

/**
 * LEXICAL 'this' - THE KILLER FEATURE:
 * 
 * PROBLEM WITH REGULAR FUNCTIONS:
 * const obj = {
 *     value: 42,
 *     method() {
 *         setTimeout(function() {
 *             console.log(this.value);  // undefined! 'this' is wrong
 *         }, 100);
 *     }
 * };
 * 
 * OLD SOLUTION (bind):
 * method() {
 *     setTimeout(function() {
 *         console.log(this.value);
 *     }.bind(this), 100);  // Verbose!
 * }
 * 
 * ARROW FUNCTION SOLUTION:
 * method() {
 *     setTimeout(() => {
 *         console.log(this.value);  // Works! 'this' from enclosing scope
 *     }, 100);
 * }
 */


// ============================================================================
// 4. PARAMETERS AND ARGUMENTS
// ============================================================================

console.log("\n============ PARAMETERS AND ARGUMENTS ============\n");

// Default parameters
function power(base, exponent = 2) {
    return base ** exponent;
}

console.log("power(5):", power(5));        // 25 (uses default)
console.log("power(5, 3):", power(5, 3));  // 125

// Rest parameters (collect remaining arguments)
function multiply(multiplier, ...numbers) {
    return numbers.map(n => n * multiplier);
}

console.log("multiply(2, 1, 2, 3):", multiply(2, 1, 2, 3));

// Arguments object (traditional functions only, not arrow functions)
function traditionalSum() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

console.log("traditionalSum(1, 2, 3, 4):", traditionalSum(1, 2, 3, 4));

// Destructuring parameters
function printUser({ name, age, city = "Unknown" }) {
    console.log(`${name}, ${age} years old, from ${city}`);
}

printUser({ name: "Alice", age: 30, city: "NYC" });
printUser({ name: "Bob", age: 25 });  // city defaults to "Unknown"

// Array destructuring in parameters
function getFirstTwo([first, second]) {
    return { first, second };
}

console.log("getFirstTwo:", getFirstTwo([10, 20, 30]));


// ============================================================================
// 5. RETURN VALUES
// ============================================================================

console.log("\n============ RETURN VALUES ============\n");

/*
    - Functions without explicit return return 'undefined'
    - return statement exits function immediately
    - Can return any type (primitive or object)
*/

// Explicit return
function explicitReturn() {
    return 42;
}

// Implicit return (undefined)
function implicitReturn() {
    console.log("No return statement");
}

console.log("explicit:", explicitReturn());    // 42
console.log("implicit:", implicitReturn());     // undefined

// Early return (guard clauses)
function processInput(value) {
    if (!value) {
        return "No value provided";
    }
    
    if (typeof value !== "number") {
        return "Value must be a number";
    }
    
    return value * 2;
}

console.log("processInput(''):", processInput(""));
console.log("processInput('text'):", processInput("text"));
console.log("processInput(5):", processInput(5));

// Returning multiple values (using object/array)
function getMinMax(arr) {
    return {
        min: Math.min(...arr),
        max: Math.max(...arr)
    };
}

const result = getMinMax([1, 5, 3, 9, 2]);
console.log("min/max:", result);


// ============================================================================
// 6. CLOSURES
// ============================================================================

console.log("\n============ CLOSURES ============\n");

/*
    CLOSURE:
    A function that has access to variables from its outer (enclosing) scope,
    even after the outer function has returned.
    
    Closures enable:
    - Data privacy
    - Factory functions
    - Callback functions
    - Partial application
*/

// Basic closure
function outer() {
    const outerVar = "I'm from outer function";
    
    function inner() {
        console.log(outerVar);  // Accesses outer scope
    }
    
    return inner;
}

const closureFunc = outer();
closureFunc();  // Still has access to outerVar!

// Counter with closure (data privacy)
function createCounter() {
    let count = 0;  // Private variable
    
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

const counter = createCounter();
console.log("count:", counter.increment());  // 1
console.log("count:", counter.increment());  // 2
console.log("count:", counter.decrement());  // 1
console.log("get:", counter.getCount());     // 1
// console.log(counter.count);  // undefined (private!)

// Factory function with closure
function createGreeter(greeting) {
    return (name) => `${greeting}, ${name}!`;
}

const sayHello = createGreeter("Hello");
const sayHi = createGreeter("Hi");

console.log(sayHello("Alice"));  // "Hello, Alice!"
console.log(sayHi("Bob"));       // "Hi, Bob!"


// ============================================================================
// 7. IMMEDIATELY INVOKED FUNCTION EXPRESSIONS (IIFE)
// ============================================================================

console.log("\n============ IIFE ============\n");

/*
    IIFE:
    Function that runs immediately after it's defined
    Used for:
    - Creating private scope
    - Avoiding global namespace pollution
    - Module pattern (before ES6 modules)
*/

// Basic IIFE
(function() {
    console.log("IIFE executed!");
})();

// IIFE with parameters
(function(name) {
    console.log(`Hello from IIFE, ${name}!`);
})("Alice");

// IIFE returning value
const result2 = (function() {
    const privateVar = 42;
    return privateVar * 2;
})();

console.log("IIFE result:", result2);

// Arrow function IIFE
(() => {
    console.log("Arrow IIFE!");
})();

// Module pattern with IIFE
const calculator = (function() {
    // Private variables and functions
    let memory = 0;
    
    function add(a, b) {
        return a + b;
    }
    
    // Public API
    return {
        add: add,
        addToMemory: (value) => memory += value,
        getMemory: () => memory
    };
})();

console.log("calculator.add(5, 3):", calculator.add(5, 3));
calculator.addToMemory(10);
console.log("memory:", calculator.getMemory());


// ============================================================================
// 8. HIGHER-ORDER FUNCTIONS
// ============================================================================

console.log("\n============ HIGHER-ORDER FUNCTIONS ============\n");

/*
    HIGHER-ORDER FUNCTION:
    A function that:
    - Takes one or more functions as arguments, OR
    - Returns a function as its result
*/

// Function that takes a function as argument
function repeat(n, action) {
    for (let i = 0; i < n; i++) {
        action(i);
    }
}

repeat(3, (i) => console.log(`Iteration ${i}`));

// Function that returns a function
function multiplier(factor) {
    return (number) => number * factor;
}

const double2 = multiplier(2);
const triple = multiplier(3);

console.log("double(5):", double2(5));    // 10
console.log("triple(5):", triple(5));     // 15

// Composition
const compose = (f, g) => (x) => f(g(x));

const addOne = x => x + 1;
const square2 = x => x * x;

const addOneThenSquare = compose(square2, addOne);
console.log("compose result:", addOneThenSquare(5));  // 36 ((5+1)^2)


// ============================================================================
// 9. 'THIS' BINDING
// ============================================================================

console.log("\n============ 'THIS' BINDING ============\n");

/*
    'this' value depends on how function is called:
    1. Method: this = object
    2. Function: this = global (undefined in strict mode)
    3. Arrow function: this = lexical (from outer scope)
    4. Constructor: this = new instance
    5. call/apply/bind: this = explicitly set
*/

const person = {
    name: "Alice",
    greet: function() {
        console.log(`Hello, I'm ${this.name}`);
    },
    greetArrow: () => {
        // Arrow function: 'this' from outer scope (not person!)
        console.log(`Arrow this:`, this);
    }
};

person.greet();  // "Hello, I'm Alice" (this = person)
person.greetArrow();  // 'this' is NOT person!

// Losing 'this' context
const greetFunc = person.greet;
// greetFunc();  // Error or undefined (this is not person)

// Binding 'this'
const boundGreet = person.greet.bind(person);
boundGreet();  // Works! 'this' is bound to person

// call and apply
function introduce(age, city) {
    console.log(`I'm ${this.name}, ${age} years old, from ${city}`);
}

const user = { name: "Bob" };

introduce.call(user, 25, "NYC");           // call: individual arguments
introduce.apply(user, [25, "NYC"]);        // apply: array of arguments

// Arrow functions inherit 'this' from outer scope
const obj = {
    name: "Test",
    traditional: function() {
        setTimeout(function() {
            // console.log(this.name);  // undefined (this is not obj)
        }, 0);
    },
    arrow: function() {
        setTimeout(() => {
            console.log(`Arrow preserves this: ${this.name}`);  // Works!
        }, 0);
    }
};

obj.arrow();


// ============================================================================
// 10. CALLBACK FUNCTIONS
// ============================================================================

console.log("\n============ CALLBACK FUNCTIONS ============\n");

/*
    CALLBACK:
    A function passed as an argument to another function
    Called by that function at an appropriate time
*/

// Simple callback
function processData(data, callback) {
    const result = data * 2;
    callback(result);
}

processData(5, (result) => {
    console.log("Callback result:", result);
});

// Array methods use callbacks
const arr = [1, 2, 3, 4, 5];

arr.forEach((num, index) => {
    console.log(`Index ${index}: ${num}`);
});

const mapped = arr.map(num => num * 2);
console.log("mapped:", mapped);


// ============================================================================
// 11. FUNCTION CURRYING
// ============================================================================

console.log("\n============ CURRYING ============\n");

/*
    CURRYING:
    Transforming a function with multiple arguments
    into a sequence of functions with single arguments
*/

// Regular function
function addRegular(a, b, c) {
    return a + b + c;
}

// Curried function
function addCurried(a) {
    return function(b) {
        return function(c) {
            return a + b + c;
        };
    };
}

console.log("curried:", addCurried(1)(2)(3));  // 6

// Arrow function currying
const addArrow = a => b => c => a + b + c;
console.log("arrow curried:", addArrow(1)(2)(3));

// Practical use: partial application
const add5 = addCurried(5);
const add5And10 = add5(10);
console.log("partial application:", add5And10(15));  // 30


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

console.log("\n============ BEST PRACTICES ============\n");

/*
    FUNCTION BEST PRACTICES:
    
    1. Use arrow functions for callbacks and short functions
    2. Use function declarations for top-level functions
    3. Keep functions small and focused (single responsibility)
    4. Use descriptive names (verbs for functions)
    5. Avoid side effects when possible (pure functions)
    6. Use default parameters instead of manual checks
    7. Use rest parameters instead of arguments object
    8. Return early to avoid deep nesting
    9. Use arrow functions to preserve 'this' in callbacks
    10. Prefer composition over complex nested logic
*/

// Good: Pure function (no side effects)
function addPure(a, b) {
    return a + b;
}

// Bad: Side effects
let total = 0;
function addWithSideEffect(a) {
    total += a;  // Modifies external state
    return total;
}

// Good: Single responsibility
function validateEmail(email) {
    return email.includes("@");
}

function sendEmail(email) {
    if (!validateEmail(email)) {
        return false;
    }
    // Send email logic
    return true;
}

// Good: Descriptive names
function calculateTotalPrice(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}


console.log("\n=== Functions Complete ===");

/*
    KEY TAKEAWAYS:
    
    1. Function declarations are hoisted, expressions are not
    2. Arrow functions have lexical 'this' binding
    3. Closures provide data privacy and state persistence
    4. Higher-order functions enable functional programming
    5. Use const/let for function expressions
    6. Default, rest, and destructuring parameters for flexibility
    7. 'this' binding depends on how function is called
    8. Currying enables partial application
    9. Keep functions pure and focused
    10. Use descriptive names and early returns
*/
