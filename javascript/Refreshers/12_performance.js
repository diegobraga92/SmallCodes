/**
 * JAVASCRIPT PERFORMANCE OPTIMIZATION
 * =====================================
 * Memory management, performance tips, profiling
 * Web Vitals, optimization techniques
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT PERFORMANCE OPTIMIZATION");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. MEMORY MANAGEMENT
// ============================================================================

console.log("\n=== Memory Management ===");

/**
 * GARBAGE COLLECTION:
 * - Automatic in JavaScript
 * - Mark-and-sweep algorithm
 * - Collects unreachable objects
 * 
 * MEMORY LEAKS:
 * - Global variables
 * - Forgotten timers/callbacks
 * - Closures holding references
 * - Detached DOM nodes
 */

// Memory leak example - Global variable
// BAD
// myGlobal = "This leaks to global scope";

// GOOD
let myVariable = "This is scoped";

// Memory leak example - Forgotten timer
// BAD
setInterval(() => {
    const data = fetchData();  // Keeps running forever
}, 1000);

// GOOD
const intervalId = setInterval(() => {
    const data = fetchData();
}, 1000);
// Clear when no longer needed
// clearInterval(intervalId);

// Memory leak example - Closure holding reference
function createLeak() {
    const largeArray = new Array(1000000).fill('data');
    
    return function() {
        return largeArray.length;  // Keeps largeArray in memory
    };
}

// GOOD - Release reference
function noLeak() {
    const largeArray = new Array(1000000).fill('data');
    const length = largeArray.length;
    
    return function() {
        return length;  // Only keeps length, not array
    };
}


// ============================================================================
// 2. PERFORMANCE MEASUREMENT
// ============================================================================

console.log("\n=== Performance Measurement ===");

// performance.now() - High precision timestamp
const start = performance.now();

// Some operation
for (let i = 0; i < 1000000; i++) {}

const end = performance.now();
console.log(`Operation took ${(end - start).toFixed(2)}ms`);

// console.time / console.timeEnd
console.time("Loop");
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("Loop");

// performance.mark / performance.measure
performance.mark("start");

// Some operation
for (let i = 0; i < 1000000; i++) {}

performance.mark("end");
performance.measure("operation", "start", "end");

const measure = performance.getEntriesByName("operation")[0];
console.log(`Measured: ${measure.duration.toFixed(2)}ms`);


// ============================================================================
// 3. OPTIMIZATION TECHNIQUES
// ============================================================================

console.log("\n=== Optimization Techniques ===");

// 1. AVOID UNNECESSARY WORK
// BAD
function processAll(items) {
    return items.map(item => expensiveOperation(item));
}

// GOOD - Only process what's needed
function processNeeded(items, limit) {
    return items.slice(0, limit).map(item => expensiveOperation(item));
}

function expensiveOperation(item) {
    return item * 2;
}

// 2. CACHE COMPUTATIONS
const fibonacci = (() => {
    const cache = new Map();
    
    return function fib(n) {
        if (n <= 1) return n;
        if (cache.has(n)) return cache.get(n);
        
        const result = fib(n - 1) + fib(n - 2);
        cache.set(n, result);
        return result;
    };
})();

console.time("Fib with cache");
console.log("Fib(40):", fibonacci(40));
console.timeEnd("Fib with cache");

// 3. USE APPROPRIATE DATA STRUCTURES
// BAD - Array for lookups
const arr = [1, 2, 3, 4, 5, /* ... thousands */];
const exists = arr.includes(3);  // O(n)

// GOOD - Set for lookups
const set = new Set([1, 2, 3, 4, 5, /* ... thousands */]);
const exists2 = set.has(3);  // O(1)

// 4. AVOID REPEATED DOM ACCESS
// BAD
function updateDOM() {
    for (let i = 0; i < 100; i++) {
        document.getElementById('list').innerHTML += `<li>${i}</li>`;  // Reflow each time!
    }
}

// GOOD - Batch DOM operations
function updateDOMBetter() {
    const fragment = document.createDocumentFragment();
    for (let i = 0; i < 100; i++) {
        const li = document.createElement('li');
        li.textContent = i;
        fragment.appendChild(li);
    }
    document.getElementById('list').appendChild(fragment);  // Single reflow
}

// 5. USE EVENT DELEGATION
// BAD - Add listener to each item
// items.forEach(item => {
//     item.addEventListener('click', handleClick);
// });

// GOOD - Single listener on parent
// parent.addEventListener('click', (e) => {
//     if (e.target.matches('.item')) {
//         handleClick(e);
//     }
// });


// ============================================================================
// 4. LOOP OPTIMIZATION
// ============================================================================

console.log("\n=== Loop Optimization ===");

const largeArray = Array.from({ length: 1000000 }, (_, i) => i);

// Traditional for loop (fastest)
console.time("for");
let sum1 = 0;
for (let i = 0; i < largeArray.length; i++) {
    sum1 += largeArray[i];
}
console.timeEnd("for");

// forEach (slower)
console.time("forEach");
let sum2 = 0;
largeArray.forEach(n => sum2 += n);
console.timeEnd("forEach");

// reduce (slowest but most functional)
console.time("reduce");
const sum3 = largeArray.reduce((acc, n) => acc + n, 0);
console.timeEnd("reduce");

// Cache array length
console.time("cached length");
let sum4 = 0;
for (let i = 0, len = largeArray.length; i < len; i++) {
    sum4 += largeArray[i];
}
console.timeEnd("cached length");


// ============================================================================
// 5. STRING OPTIMIZATION
// ============================================================================

console.log("\n=== String Optimization ===");

// BAD - String concatenation in loop
console.time("concat");
let str1 = "";
for (let i = 0; i < 10000; i++) {
    str1 += "a";  // Creates new string each time
}
console.timeEnd("concat");

// GOOD - Array join
console.time("join");
const arr2 = [];
for (let i = 0; i < 10000; i++) {
    arr2.push("a");
}
const str2 = arr2.join("");
console.timeEnd("join");

// BETTER - Template literals for small concatenations
const name = "Alice";
const greeting = `Hello, ${name}!`;  // Fast for few operations


// ============================================================================
// 6. OBJECT OPTIMIZATION
// ============================================================================

console.log("\n=== Object Optimization ===");

// Use object pooling for frequently created objects
class ObjectPool {
    constructor(createFn, resetFn) {
        this.createFn = createFn;
        this.resetFn = resetFn;
        this.pool = [];
    }
    
    acquire() {
        return this.pool.length > 0
            ? this.pool.pop()
            : this.createFn();
    }
    
    release(obj) {
        this.resetFn(obj);
        this.pool.push(obj);
    }
}

const vectorPool = new ObjectPool(
    () => ({ x: 0, y: 0 }),
    (v) => { v.x = 0; v.y = 0; }
);

// Use Map for dynamic keys
// BAD
const obj = {};
for (let i = 0; i < 1000; i++) {
    obj[`key${i}`] = i;
}

// GOOD - Map is optimized for frequent additions/deletions
const map = new Map();
for (let i = 0; i < 1000; i++) {
    map.set(`key${i}`, i);
}


// ============================================================================
// 7. WEB VITALS (BROWSER ONLY)
// ============================================================================

console.log("\n=== Web Vitals ===");

/**
 * CORE WEB VITALS:
 * 
 * 1. LCP (Largest Contentful Paint)
 *    - Measures loading performance
 *    - Should occur within 2.5s
 * 
 * 2. FID (First Input Delay)
 *    - Measures interactivity
 *    - Should be < 100ms
 * 
 * 3. CLS (Cumulative Layout Shift)
 *    - Measures visual stability
 *    - Should be < 0.1
 * 
 * MONITORING:
 * const observer = new PerformanceObserver((list) => {
 *     for (const entry of list.getEntries()) {
 *         console.log(entry);
 *     }
 * });
 * observer.observe({ entryTypes: ['largest-contentful-paint'] });
 */


// ============================================================================
// 8. DEBOUNCE/THROTTLE FOR PERFORMANCE
// ============================================================================

console.log("\n=== Debounce/Throttle ===");

// Debounce - Wait for pause
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Throttle - Limit frequency
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

// Usage for scroll events
// const handleScroll = throttle(() => {
//     console.log("Scroll position:", window.scrollY);
// }, 100);
// window.addEventListener('scroll', handleScroll);


// ============================================================================
// 9. LAZY LOADING
// ============================================================================

console.log("\n=== Lazy Loading ===");

/**
 * LAZY LOADING STRATEGIES:
 * 
 * 1. Code Splitting:
 *    const Component = React.lazy(() => import('./Component'));
 * 
 * 2. Image Lazy Loading:
 *    <img loading="lazy" src="image.jpg" />
 * 
 * 3. Intersection Observer:
 *    const observer = new IntersectionObserver((entries) => {
 *        entries.forEach(entry => {
 *            if (entry.isIntersecting) {
 *                loadContent(entry.target);
 *            }
 *        });
 *    });
 * 
 * 4. Virtual Scrolling:
 *    Only render visible items in long lists
 */


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * PERFORMANCE BEST PRACTICES:
 * 
 * 1. MINIMIZE WORK:
 *    ✓ Avoid unnecessary loops
 *    ✓ Cache computed values
 *    ✓ Use appropriate data structures
 *    ✓ Lazy load when possible
 * 
 * 2. EFFICIENT ALGORITHMS:
 *    ✓ Choose O(1) or O(log n) over O(n²)
 *    ✓ Use binary search instead of linear
 *    ✓ Hash tables for lookups
 * 
 * 3. DOM OPTIMIZATION:
 *    ✓ Batch DOM operations
 *    ✓ Use DocumentFragment
 *    ✓ Event delegation
 *    ✓ Minimize reflows/repaints
 * 
 * 4. MEMORY MANAGEMENT:
 *    ✓ Avoid memory leaks
 *    ✓ Clear timers/listeners
 *    ✓ Release references
 *    ✓ Use WeakMap/WeakSet for caches
 * 
 * 5. ASYNC OPERATIONS:
 *    ✓ Use Web Workers for heavy computation
 *    ✓ Debounce/throttle events
 *    ✓ requestAnimationFrame for animations
 *    ✓ Async/await for clarity
 * 
 * 6. BUNDLE OPTIMIZATION:
 *    ✓ Code splitting
 *    ✓ Tree shaking
 *    ✓ Minification
 *    ✓ Compression (gzip/brotli)
 * 
 * 7. RESOURCE LOADING:
 *    ✓ Lazy load images/modules
 *    ✓ Preload critical resources
 *    ✓ Use CDN
 *    ✓ Cache assets
 * 
 * 8. PROFILING:
 *    ✓ Chrome DevTools Performance tab
 *    ✓ Memory profiler
 *    ✓ Lighthouse audits
 *    ✓ Performance API
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Measure before optimizing (don't guess!)");
console.log("2. Use appropriate data structures (Set, Map, etc.)");
console.log("3. Cache expensive computations");
console.log("4. Batch DOM operations");
console.log("5. Use event delegation");
console.log("6. Debounce/throttle frequent events");
console.log("7. Lazy load heavy resources");
console.log("8. Avoid memory leaks (clear timers, release references)");
console.log("9. Profile with DevTools");
console.log("10. Optimize for Core Web Vitals (LCP, FID, CLS)");
console.log("=".repeat(80));
