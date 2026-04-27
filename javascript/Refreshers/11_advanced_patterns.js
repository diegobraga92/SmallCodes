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
 * CLOSURES EXPLAINED:
 * ==================
 * 
 * DEFINITION:
 * A closure is a function that has access to variables from an outer function
 * even after the outer function has returned.
 * 
 * HOW IT WORKS:
 * - Inner function "closes over" (captures) outer function's variables
 * - Variables are kept alive in memory as long as closure exists
 * - Each closure gets its own copy of the outer variables
 * 
 * WHEN CREATED:
 * - Every time a function is created inside another function
 * - Arrow functions, regular functions, methods - all can form closures
 * 
 * USE CASES:
 * ✓ Data privacy (private variables)
 * ✓ Factory functions (creating similar objects)
 * ✓ Event handlers (accessing component state)
 * ✓ Callbacks (remembering context)
 * 
 * MEMORY IMPLICATIONS:
 * - Closures keep variables in memory (potential memory leak)
 * - Each closure instance has separate memory
 * - Only captured variables are retained (not entire scope)
 * 
 * TRADE-OFFS:
 * PROS: Data privacy, state management, elegant code
 * CONS: Memory overhead, harder to debug, can cause leaks
 */

function makeCounter() {
    // This variable is in the outer function's scope
    let count = 0;  // Private variable - not accessible from outside
    
    // Return object with methods that close over 'count'
    return {
        increment() {
            // This function forms a closure over 'count'
            // Even after makeCounter returns, 'count' stays alive
            count++;
            return count;
        },
        decrement() {
            // Another closure over the same 'count'
            count--;
            return count;
        },
        getCount() {
            // Yet another closure over 'count'
            return count;
        }
    };
}

const counter = makeCounter();
// makeCounter() has returned, but 'count' is still alive!
console.log("Increment:", counter.increment());  // 1
console.log("Increment:", counter.increment());  // 2
console.log("Decrement:", counter.decrement());  // 1
console.log("Get:", counter.getCount());         // 1

// IMPORTANT: Can't access 'count' directly (data privacy!)
console.log(counter.count);  // undefined - private!

// Each call to makeCounter() creates a NEW closure with NEW variables
const counter2 = makeCounter();
console.log("Counter2:", counter2.increment());  // 1 (independent!)

// CLOSURE IN LOOP - CLASSIC INTERVIEW QUESTION
console.log("\nClosure in loop:");

// PROBLEM: var is function-scoped, not block-scoped
for (var i = 0; i < 3; i++) {
    // setTimeout callback closes over 'i'
    // By the time callback executes, loop has finished and i = 3
    setTimeout(() => console.log("  var:", i), 100);  // Prints 3, 3, 3 ❌
}
// WHY? All callbacks share the SAME 'i', which is 3 after loop ends

// SOLUTION 1: Use 'let' (block-scoped)
for (let j = 0; j < 3; j++) {
    // Each iteration creates a NEW 'j' in separate block scope
    // Callback closes over its iteration's 'j'
    setTimeout(() => console.log("  let:", j), 100);  // Prints 0, 1, 2 ✓
}

// SOLUTION 2: IIFE (old way, before 'let')
for (var k = 0; k < 3; k++) {
    // IIFE creates new scope for each iteration
    // Passes current 'k' value as 'num' parameter
    (function(num) {
        // Callback closes over 'num' (frozen at this iteration's value)
        setTimeout(() => console.log("  IIFE:", num), 100);  // Prints 0, 1, 2 ✓
    })(k);
}

/**
 * MEMORY LEAK WARNING:
 * 
 * // BAD: Closure keeping large object in memory
 * function createHandler() {
 *     const largeData = new Array(1000000).fill('x');
 *     
 *     return function() {
 *         console.log(largeData.length);  // Keeps entire array in memory!
 *     };
 * }
 * 
 * // GOOD: Only keep what you need
 * function createHandler() {
 *     const largeData = new Array(1000000).fill('x');
 *     const length = largeData.length;  // Extract value
 *     
 *     return function() {
 *         console.log(length);  // Only keeps number, not entire array
 *     };
 * }
 */


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
 * MEMOIZATION EXPLAINED:
 * =====================
 * 
 * CONCEPT:
 * Cache results of expensive function calls to avoid recalculation
 * 
 * HOW IT WORKS:
 * 1. Check if result for these arguments exists in cache
 * 2. If yes: return cached result (fast!)
 * 3. If no: compute result, store in cache, return result
 * 
 * WHEN TO USE:
 * ✓ Pure functions (same input → same output)
 * ✓ Expensive calculations (fibonacci, factorials, complex algorithms)
 * ✓ API calls with same parameters
 * ✓ Recursive functions (massive speedup!)
 * 
 * WHEN NOT TO USE:
 * ✗ Functions with side effects
 * ✗ Functions that return different results for same input
 * ✗ Rarely-called functions (cache overhead not worth it)
 * ✗ Functions with many unique argument combinations (memory waste)
 * 
 * TRADE-OFFS:
 * PROS: Massive performance gains for repeated calls
 * CONS: Memory usage (cache grows), only works for pure functions
 * 
 * PERFORMANCE COMPARISON:
 * fibonacci(40) without memoization: ~1-2 seconds (2^40 operations)
 * fibonacci(40) with memoization: <1ms (40 operations + cache hits)
 */

// Without memoization - EXPONENTIALLY SLOW
function fibonacci(n) {
    if (n <= 1) return n;
    // Each call spawns 2 more calls → 2^n time complexity!
    return fibonacci(n - 1) + fibonacci(n - 2);
}
// fibonacci(40) would take ~1 second, fibonacci(50) would take minutes!

// With memoization - LINEAR TIME
function memoize(fn) {
    const cache = {};  // Store results here
    
    return function(...args) {
        // Create cache key from arguments
        const key = JSON.stringify(args);
        
        // Check cache first
        if (key in cache) {
            console.log(`  Cache hit for ${key}`);
            return cache[key];  // Return instantly!
        }
        
        // Not in cache: compute result
        console.log(`  Computing for ${key}`);
        const result = fn.apply(this, args);
        
        // Store in cache for next time
        cache[key] = result;
        return result;
    };
}

const memoizedFib = memoize(fibonacci);

// First call: computes and caches
console.log("Fib(10):", memoizedFib(10));

// Second call: instant from cache
console.log("Fib(10) again:", memoizedFib(10));  // From cache

/**
 * MEMOIZATION PITFALLS:
 * 
 * 1. CACHE GROWS UNBOUNDED
 *    Solution: Add cache size limit or TTL (time-to-live)
 * 
 * 2. REFERENCE TYPES AS ARGUMENTS
 *    Objects/arrays: JSON.stringify might not create unique keys
 *    Solution: Use better serialization or WeakMap
 * 
 * 3. MEMORY LEAKS
 *    Cache never clears, grows forever
 *    Solution: Implement cache eviction strategy (LRU, LFU)
 * 
 * ADVANCED MEMOIZATION (with cache limit):
 * function memoizeWithLimit(fn, maxSize = 100) {
 *     const cache = new Map();
 *     return function(...args) {
 *         const key = JSON.stringify(args);
 *         if (cache.has(key)) return cache.get(key);
 *         
 *         const result = fn(...args);
 *         cache.set(key, result);
 *         
 *         if (cache.size > maxSize) {
 *             const firstKey = cache.keys().next().value;
 *             cache.delete(firstKey);  // Remove oldest
 *         }
 *         return result;
 *     };
 * }
 */


// ============================================================================
// 5. DEBOUNCE AND THROTTLE
// ============================================================================

console.log("\n=== Debounce and Throttle ===");

/**
 * DEBOUNCE vs THROTTLE - WHEN TO USE EACH:
 * ========================================
 * 
 * DEBOUNCE:
 * - Delays execution until activity stops
 * - Resets timer on each new call
 * - Only executes AFTER user stops triggering
 * 
 * VISUALIZATION:
 * Events:  | | | | |     |      (user types/moves)
 * Debounce:          [300ms]→ ✓  (only runs after pause)
 * 
 * USE WHEN:
 * ✓ Search input (wait until user stops typing)
 * ✓ Window resize (wait until user finishes resizing)
 * ✓ Form validation (validate after user finishes typing)
 * ✓ Auto-save (save after user stops editing)
 * 
 * THROTTLE:
 * - Executes at regular intervals
 * - Ignores calls during cooldown period
 * - Guarantees execution at consistent rate
 * 
 * VISUALIZATION:
 * Events:  | | | | | | | | | | (continuous events)
 * Throttle: ✓   [300ms]   ✓   [300ms]   ✓  (every 300ms)
 * 
 * USE WHEN:
 * ✓ Scroll events (update position every Xms, not every scroll)
 * ✓ Mouse move tracking (sample position, not every pixel)
 * ✓ Button clicks (prevent spam clicking)
 * ✓ API rate limiting (max N requests per second)
 * 
 * KEY DIFFERENCE:
 * Debounce: "Wait until they stop"
 * Throttle: "Do it regularly, not constantly"
 * 
 * PERFORMANCE IMPACT:
 * Without:  1000 events = 1000 function calls = 💀
 * Debounce: 1000 events = 1 call (after stop) = ✓
 * Throttle: 1000 events = ~10 calls (every 100ms) = ✓
 */

// DEBOUNCE IMPLEMENTATION
function debounce(func, delay) {
    let timeoutId;  // Stores the timer
    
    return function(...args) {
        // Clear previous timer (restart the countdown!)
        clearTimeout(timeoutId);
        
        // Start new timer
        timeoutId = setTimeout(() => {
            // Execute after delay (if no new calls interrupt)
            func.apply(this, args);
        }, delay);
        
        // KEY BEHAVIOR: Each call resets the timer
        // Function only executes after 'delay' ms of silence
    };
}

// REAL-WORLD EXAMPLE: Search input
const searchAPI = (query) => console.log(`  Searching for: ${query}`);
const debouncedSearch = debounce(searchAPI, 500);

// Simulate rapid typing (user types "abc")
debouncedSearch("a");    // Timer starts (500ms)
debouncedSearch("ab");   // Timer resets (500ms)
debouncedSearch("abc");  // Timer resets (500ms)
// After 500ms of no calls: searchAPI("abc") executes
// Result: Only 1 API call instead of 3!

/**
 * WHY THIS MATTERS:
 * Without debounce:
 * - User types "javascript" (10 characters)
 * - 10 API calls fired
 * - Server overload, wasted bandwidth
 * 
 * With debounce (300ms):
 * - User types "javascript" (10 characters)
 * - 1 API call fired (after they stop typing)
 * - Efficient, better UX
 */

// THROTTLE IMPLEMENTATION
function throttle(func, limit) {
    let inThrottle;  // Flag to track cooldown
    
    return function(...args) {
        if (!inThrottle) {
            // Not in cooldown: execute immediately
            func.apply(this, args);
            
            // Start cooldown period
            inThrottle = true;
            
            // Reset flag after 'limit' ms
            setTimeout(() => inThrottle = false, limit);
            
            // KEY BEHAVIOR: Executes immediately, then cooldown
            // Subsequent calls during cooldown are ignored
        }
        // Calls during cooldown are silently dropped
    };
}

// REAL-WORLD EXAMPLE: Scroll tracking
const trackScroll = () => console.log(`  Scroll position: ${window.scrollY}`);
const throttledScroll = throttle(trackScroll, 100);

// User scrolls continuously
// window.addEventListener('scroll', throttledScroll);
// Without throttle: fires 100+ times per second
// With throttle (100ms): fires 10 times per second

/**
 * ADVANCED DEBOUNCE (with leading/trailing options):
 * 
 * function debounceAdvanced(func, delay, options = {}) {
 *     let timeoutId;
 *     const { leading = false, trailing = true } = options;
 *     let lastArgs;
 *     
 *     return function(...args) {
 *         lastArgs = args;
 *         
 *         if (leading && !timeoutId) {
 *             func.apply(this, args);  // Execute immediately
 *         }
 *         
 *         clearTimeout(timeoutId);
 *         timeoutId = setTimeout(() => {
 *             if (trailing) {
 *                 func.apply(this, lastArgs);  // Execute after delay
 *             }
 *             timeoutId = null;
 *         }, delay);
 *     };
 * }
 * 
 * USE CASES:
 * - leading: true → Execute first call immediately, debounce rest
 * - trailing: true → Execute after delay (default behavior)
 * - both: Execute first call AND after delay
 */

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
