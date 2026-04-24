/**
 * JAVASCRIPT ADVANCED PATTERNS AND CONCEPTS
 * ===========================================
 * Closures, IIFE, Currying, Memoization, Debounce/Throttle
 * Design patterns and advanced techniques
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT ADVANCED PATTERNS");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. CLOSURES
// ============================================================================

console.log("\n=== Closures ===");

/**
 * Closure = function that has access to variables from outer scope
 * Even after outer function has returned
 */

function makeCounter() {
    let count = 0;  // Private variable
    
    return {
        increment() {
            count++;
            return count;
        },
        decrement() {
            count--;
            return count;
        },
        getCount() {
            return count;
        }
    };
}

const counter = makeCounter();
console.log("Increment:", counter.increment());  // 1
console.log("Increment:", counter.increment());  // 2
console.log("Decrement:", counter.decrement());  // 1
console.log("Get:", counter.getCount());         // 1
// console.log(counter.count);  // undefined - private!

// Closure in loop (classic interview question)
console.log("\nClosure in loop:");
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log("  var:", i), 100);  // Prints 3, 3, 3
}

for (let j = 0; j < 3; j++) {
    setTimeout(() => console.log("  let:", j), 100);  // Prints 0, 1, 2
}

// Fix with IIFE
for (var k = 0; k < 3; k++) {
    (function(num) {
        setTimeout(() => console.log("  IIFE:", num), 100);  // Prints 0, 1, 2
    })(k);
}


// ============================================================================
// 2. IIFE (Immediately Invoked Function Expression)
// ============================================================================

console.log("\n=== IIFE ===");

/**
 * IIFE = Function that runs immediately after definition
 * Creates private scope
 */

// Basic IIFE
(function() {
    const private = "Can't access from outside";
    console.log("IIFE executed");
})();

// IIFE with return value
const result = (function() {
    return "Result from IIFE";
})();
console.log("IIFE result:", result);

// IIFE with parameters
(function(name) {
    console.log(`Hello, ${name}`);
})("Alice");

// Module pattern with IIFE
const Module = (function() {
    let privateVar = 0;
    
    function privateMethod() {
        return "Private";
    }
    
    return {
        publicMethod() {
            privateVar++;
            return `Public access: ${privateVar}`;
        }
    };
})();

console.log(Module.publicMethod());


// ============================================================================
// 3. CURRYING
// ============================================================================

console.log("\n=== Currying ===");

/**
 * Currying = Transform function with multiple arguments
 * into sequence of functions with single argument
 */

// Regular function
function add(a, b, c) {
    return a + b + c;
}

// Curried version
function curriedAdd(a) {
    return function(b) {
        return function(c) {
            return a + b + c;
        };
    };
}

console.log("Curried:", curriedAdd(1)(2)(3));  // 6

// With arrow functions
const curriedAdd2 = a => b => c => a + b + c;
console.log("Curried (arrow):", curriedAdd2(1)(2)(3));

// Practical example: Partial application
const add5 = curriedAdd(5);
const add5And3 = add5(3);
console.log("Partial:", add5And3(2));  // 10

// Generic curry function
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        } else {
            return function(...moreArgs) {
                return curried.apply(this, args.concat(moreArgs));
            };
        }
    };
}

const curriedSum = curry((a, b, c, d) => a + b + c + d);
console.log("Generic curry:", curriedSum(1)(2)(3)(4));  // 10
console.log("Generic curry:", curriedSum(1, 2)(3, 4));  // 10


// ============================================================================
// 4. MEMOIZATION
// ============================================================================

console.log("\n=== Memoization ===");

/**
 * Memoization = Cache results of expensive function calls
 */

// Without memoization
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// With memoization
function memoize(fn) {
    const cache = {};
    
    return function(...args) {
        const key = JSON.stringify(args);
        if (key in cache) {
            console.log(`  Cache hit for ${key}`);
            return cache[key];
        }
        console.log(`  Computing for ${key}`);
        const result = fn.apply(this, args);
        cache[key] = result;
        return result;
    };
}

const memoizedFib = memoize(fibonacci);
console.log("Fib(10):", memoizedFib(10));
console.log("Fib(10) again:", memoizedFib(10));  // From cache


// ============================================================================
// 5. DEBOUNCE AND THROTTLE
// ============================================================================

console.log("\n=== Debounce and Throttle ===");

/**
 * DEBOUNCE = Execute after delay, restart timer on new call
 * Use: Search input, window resize
 * 
 * THROTTLE = Execute at most once per time period
 * Use: Scroll events, button clicks
 */

// Debounce
function debounce(func, delay) {
    let timeoutId;
    
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Usage
const searchAPI = (query) => console.log(`  Searching for: ${query}`);
const debouncedSearch = debounce(searchAPI, 500);

// Simulate rapid typing
debouncedSearch("a");
debouncedSearch("ab");
debouncedSearch("abc");  // Only this will execute after 500ms

// Throttle
function throttle(func, limit) {
    let inThrottle;
    
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Usage
const handleScroll = () => console.log("  Scroll event");
const throttledScroll = throttle(handleScroll, 1000);

// Simulating multiple scroll events
// Only first call executes, rest ignored until 1000ms


// ============================================================================
// 6. FUNCTION COMPOSITION
// ============================================================================

console.log("\n=== Function Composition ===");

/**
 * Composition = Combine multiple functions into one
 * Output of one becomes input of next
 */

const double = x => x * 2;
const increment = x => x + 1;
const square = x => x * x;

// Manual composition
const result1 = square(increment(double(3)));  // ((3 * 2) + 1)^2 = 49
console.log("Manual:", result1);

// Compose function (right to left)
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

const transform = compose(square, increment, double);
console.log("Compose:", transform(3));  // 49

// Pipe function (left to right)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const transform2 = pipe(double, increment, square);
console.log("Pipe:", transform2(3));  // 49


// ============================================================================
// 7. PARTIAL APPLICATION
// ============================================================================

console.log("\n=== Partial Application ===");

/**
 * Partial Application = Pre-fill some arguments
 */

function multiply(a, b, c) {
    return a * b * c;
}

// Using bind
const multiplyByTwo = multiply.bind(null, 2);
console.log("Partial (bind):", multiplyByTwo(3, 4));  // 24

// Custom partial function
function partial(fn, ...presetArgs) {
    return function(...laterArgs) {
        return fn(...presetArgs, ...laterArgs);
    };
}

const double2 = partial(multiply, 2);
console.log("Partial (custom):", double2(3, 4));  // 24


// ============================================================================
// 8. OBSERVER PATTERN
// ============================================================================

console.log("\n=== Observer Pattern ===");

/**
 * Observer = Object maintains list of dependents (observers)
 * Notifies them of state changes
 */

class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, listener) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(listener);
    }
    
    off(event, listenerToRemove) {
        if (!this.events[event]) return;
        
        this.events[event] = this.events[event].filter(
            listener => listener !== listenerToRemove
        );
    }
    
    emit(event, ...args) {
        if (!this.events[event]) return;
        
        this.events[event].forEach(listener => {
            listener(...args);
        });
    }
    
    once(event, listener) {
        const onceWrapper = (...args) => {
            listener(...args);
            this.off(event, onceWrapper);
        };
        this.on(event, onceWrapper);
    }
}

const emitter = new EventEmitter();

emitter.on("data", data => console.log("  Received:", data));
emitter.on("data", data => console.log("  Also received:", data));

emitter.emit("data", { value: 42 });


// ============================================================================
// 9. SINGLETON PATTERN
// ============================================================================

console.log("\n=== Singleton Pattern ===");

/**
 * Singleton = Only one instance of class exists
 */

class Singleton {
    constructor() {
        if (Singleton.instance) {
            return Singleton.instance;
        }
        Singleton.instance = this;
        this.data = [];
    }
    
    add(item) {
        this.data.push(item);
    }
    
    getAll() {
        return this.data;
    }
}

const s1 = new Singleton();
const s2 = new Singleton();

s1.add("item1");
s2.add("item2");

console.log("Same instance?", s1 === s2);
console.log("Data:", s1.getAll());  // ["item1", "item2"]


// ============================================================================
// 10. FACTORY PATTERN
// ============================================================================

console.log("\n=== Factory Pattern ===");

/**
 * Factory = Create objects without specifying exact class
 */

class Car {
    constructor(model) {
        this.type = "car";
        this.model = model;
    }
}

class Truck {
    constructor(model) {
        this.type = "truck";
        this.model = model;
    }
}

class VehicleFactory {
    static createVehicle(type, model) {
        switch (type) {
            case "car":
                return new Car(model);
            case "truck":
                return new Truck(model);
            default:
                throw new Error("Unknown vehicle type");
        }
    }
}

const car = VehicleFactory.createVehicle("car", "Sedan");
const truck = VehicleFactory.createVehicle("truck", "Pickup");

console.log("Car:", car);
console.log("Truck:", truck);


// ============================================================================
// 11. RECURSION PATTERNS
// ============================================================================

console.log("\n=== Recursion ===");

// Tail recursion (optimize with trampoline)
function factorial(n, acc = 1) {
    if (n <= 1) return acc;
    return factorial(n - 1, n * acc);
}

console.log("Factorial:", factorial(5));

// Tree traversal
const tree = {
    value: 1,
    children: [
        { value: 2, children: [{ value: 4, children: [] }] },
        { value: 3, children: [{ value: 5, children: [] }] }
    ]
};

function traverse(node) {
    console.log(" ", node.value);
    node.children.forEach(traverse);
}

console.log("Tree traversal:");
traverse(tree);


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Closures = functions remember outer scope");
console.log("2. IIFE = immediately invoked function for private scope");
console.log("3. Currying = transform f(a,b,c) to f(a)(b)(c)");
console.log("4. Memoization = cache expensive function results");
console.log("5. Debounce = delay execution until idle");
console.log("6. Throttle = limit execution rate");
console.log("7. Composition = combine functions");
console.log("8. Design patterns solve common problems");
console.log("=".repeat(80));
