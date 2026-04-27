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

/**
 * PERFORMANCE OPTIMIZATION PRINCIPLES:
 * ===================================
 * 
 * GOLDEN RULE: "Premature optimization is the root of all evil"
 * - Donald Knuth
 * 
 * BEFORE OPTIMIZING:
 * 1. MEASURE: Use profiler to find actual bottlenecks
 * 2. IDENTIFY: What's actually slow? (guesses are often wrong)
 * 3. OPTIMIZE: Fix the bottleneck, not random code
 * 4. VERIFY: Measure again to confirm improvement
 * 
 * OPTIMIZATION PRIORITIES:
 * 1. Algorithm/Data Structure (biggest impact)
 * 2. Reduce work (skip unnecessary operations)
 * 3. Batch operations (reduce overhead)
 * 4. Micro-optimizations (usually not worth it)
 * 
 * WHEN TO OPTIMIZE:
 * ✓ User-facing performance issues (slow UI, lag)
 * ✓ Profiler shows clear bottleneck
 * ✓ Operations on large datasets (1000s+ items)
 * ✓ Frequently called functions (hot paths)
 * 
 * WHEN NOT TO OPTIMIZE:
 * ✗ Code that runs once
 * ✗ Without profiling first
 * ✗ At the cost of readability (unless proven necessary)
 * ✗ Small datasets (<100 items) - won't notice difference
 * 
 * TRADE-OFFS:
 * Optimized code is often:
 * - Less readable
 * - Harder to maintain
 * - More bug-prone
 * - Only faster for large scale
 * 
 * BALANCE: Optimize hot paths, keep rest readable
 */

// 1. AVOID UNNECESSARY WORK
// BAD - Process everything, even if not needed
function processAll(items) {
    // If items has 1,000,000 elements but we only need 10...
    // This wastes 99.999% of CPU time!
    return items.map(item => expensiveOperation(item));
}

// GOOD - Only process what's needed
function processNeeded(items, limit) {
    // Slice first to reduce work by 99.999%!
    // This is "algorithmic optimization" - best kind
    return items.slice(0, limit).map(item => expensiveOperation(item));
}

function expensiveOperation(item) {
    return item * 2;
}

/**
 * LESSON: Skip work when possible
 * - Early returns
 * - Lazy evaluation
 * - Pagination (don't load all data)
 * - Virtual scrolling (only render visible items)
 */

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
/**
 * DATA STRUCTURE PERFORMANCE:
 * ==========================
 * 
 * ARRAY:
 * - Access by index: O(1) ✓
 * - Search (includes, find): O(n) ❌
 * - Insert/delete at end: O(1) ✓
 * - Insert/delete at start: O(n) ❌
 * - Use for: Ordered lists, iteration
 * 
 * SET:
 * - Add/has/delete: O(1) ✓
 * - No duplicates (enforced)
 * - No order guarantee (though insertion order maintained)
 * - Use for: Unique values, lookups, membership tests
 * 
 * MAP:
 * - get/set/has/delete: O(1) ✓
 * - Keys can be any type (not just strings)
 * - Maintains insertion order
 * - Use for: Key-value pairs, caching, counting
 * 
 * OBJECT:
 * - Access: O(1) ✓
 * - Keys are strings/symbols only
 * - Prototype pollution risk
 * - Use for: Simple data structures, JSON
 * 
 * CHOOSING THE RIGHT STRUCTURE:
 * Need lookups? → Set/Map (O(1)) instead of Array (O(n))
 * Need order? → Array/Map (ordered) instead of Object (not guaranteed)
 * Need counting? → Map (any keys) instead of Object (string keys)
 */

// BAD - Array for membership tests
const users = [1, 2, 3, 4, 5, /* ... thousands */];
const exists = users.includes(3);  // O(n) - scans entire array!
// With 10,000 items: ~10,000 comparisons

// GOOD - Set for membership tests  
const userSet = new Set([1, 2, 3, 4, 5, /* ... thousands */]);
const exists2 = userSet.has(3);  // O(1) - hash lookup!
// With 10,000 items: ~1 comparison

/**
 * PERFORMANCE IMPACT:
 * Array with 10,000 items:
 * - includes(): ~0.1ms per lookup
 * - 1,000 lookups = 100ms ❌
 * 
 * Set with 10,000 items:
 * - has(): ~0.001ms per lookup
 * - 1,000 lookups = 1ms ✓
 * 
 * 100x FASTER just by choosing right data structure!
 */

// 4. AVOID REPEATED DOM ACCESS
/**
 * DOM PERFORMANCE BOTTLENECKS:
 * ===========================
 * 
 * WHY DOM IS SLOW:
 * - Bridge between JavaScript and rendering engine
 * - Each modification triggers reflow/repaint
 * - Browser recalculates layout (expensive!)
 * 
 * REFLOW (Layout):
 * - When: Size, position, structure changes
 * - Cost: Very expensive (recalculates entire layout)
 * - Triggered by: innerHTML, appendChild, style changes
 * 
 * REPAINT:
 * - When: Visual changes (color, visibility)
 * - Cost: Moderate (redraws pixels)
 * - Triggered by: background, color, opacity changes
 * 
 * OPTIMIZATION STRATEGIES:
 * 1. Batch DOM updates (minimize reflows)
 * 2. Use DocumentFragment (off-screen assembly)
 * 3. Cache DOM queries
 * 4. Use CSS classes instead of inline styles
 * 5. Virtual DOM (React, Vue) for complex UIs
 */

// BAD - 100 reflows/repaints!
function updateDOM() {
    for (let i = 0; i < 100; i++) {
        // Each iteration:
        // 1. Gets element from DOM (slow)
        // 2. Parses HTML string
        // 3. Triggers reflow (browser recalculates layout)
        // 4. Triggers repaint (browser redraws)
        document.getElementById('list').innerHTML += `<li>${i}</li>`;
    }
}
// Result: 100 reflows = 100ms+ (visible lag!)

// GOOD - Single reflow/repaint
function updateDOMBetter() {
    // DocumentFragment: off-screen DOM container
    // Changes don't trigger reflow until attached
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < 100; i++) {
        const li = document.createElement('li');
        li.textContent = i;
        // Adding to fragment (no reflow - it's off-screen)
        fragment.appendChild(li);
    }
    
    // Single reflow when attaching to DOM
    document.getElementById('list').appendChild(fragment);
}
// Result: 1 reflow = ~1ms (smooth!)

/**
 * DOM OPTIMIZATION CHECKLIST:
 * ✓ Batch DOM updates
 * ✓ Use DocumentFragment for multiple elements
 * ✓ Cache querySelector results
 * ✓ Avoid layout thrashing (read then write in batches)
 * ✓ Use CSS transitions instead of JavaScript animation
 * ✓ Debounce/throttle scroll/resize handlers
 */

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

/**
 * LOOP PERFORMANCE COMPARISON:
 * ============================
 * 
 * PERFORMANCE RANKING (1M items):
 * 1. for loop (cached length): ~5ms ✓✓✓
 * 2. for loop: ~7ms ✓✓
 * 3. forEach: ~20ms ✓
 * 4. reduce: ~30ms ✓
 * 5. map/filter/find: ~40ms+ (worst for simple iteration)
 * 
 * WHY THE DIFFERENCES?
 * 
 * FOR LOOP:
 * - Direct array access
 * - No function call overhead
 * - Compiler can optimize heavily
 * - USE WHEN: Maximum performance needed
 * 
 * FOREACH:
 * - Function call per iteration (overhead)
 * - Can't break/continue
 * - Cleaner syntax
 * - USE WHEN: Readability > micro-optimization
 * 
 * REDUCE:
 * - Function call + accumulator management
 * - Most overhead
 * - Functional style
 * - USE WHEN: Complex aggregations, functional style preferred
 * 
 * WHEN DOES IT MATTER?
 * 
 * SMALL ARRAYS (<1000 items):
 * - Difference: <1ms
 * - VERDICT: Use readable code (forEach, reduce) ✓
 * 
 * LARGE ARRAYS (100k+ items):
 * - Difference: 10ms+
 * - VERDICT: Consider for loop if performance critical
 * 
 * HOT PATHS (called frequently):
 * - Even small difference compounds
 * - VERDICT: Profile and optimize if bottleneck
 * 
 * RULE OF THUMB:
 * Write for readability first, optimize if profiler shows bottleneck
 */

const largeArray = Array.from({ length: 1000000 }, (_, i) => i);

// Traditional for loop (fastest)
console.time("for");
let sum1 = 0;
for (let i = 0; i < largeArray.length; i++) {
    // Direct array access: fastest possible
    // No function calls, minimal overhead
    sum1 += largeArray[i];
}
console.timeEnd("for");  // ~7ms

// forEach (slower due to function call overhead)
console.time("forEach");
let sum2 = 0;
largeArray.forEach(n => sum2 += n);
// Each iteration: function call overhead
// Arrow function executed 1M times
console.timeEnd("forEach");  // ~20ms

// reduce (slowest but most functional)
console.time("reduce");
const sum3 = largeArray.reduce((acc, n) => acc + n, 0);
// Function call + accumulator management
// Good for readability, not raw speed
console.timeEnd("reduce");  // ~30ms

// Cache array length (micro-optimization)
console.time("cached length");
let sum4 = 0;
for (let i = 0, len = largeArray.length; i < len; i++) {
    // Avoids .length lookup on each iteration
    // Modern engines optimize this anyway
    // Usually not worth the decreased readability
    sum4 += largeArray[i];
}
console.timeEnd("cached length");  // ~5ms

/**
 * PRACTICAL ADVICE:
 * 
 * DEFAULT CHOICE:
 * Use forEach/map/reduce for readability
 * 
 * WHEN TO SWITCH TO FOR LOOP:
 * ✓ Profiler shows loop is bottleneck
 * ✓ Processing 100k+ items
 * ✓ Called in hot path (many times per second)
 * ✓ Need early break/continue
 * 
 * MICRO-OPTIMIZATIONS (caching length, etc.):
 * ✗ Modern engines already optimize
 * ✗ Decreases readability
 * ✗ Measure first - likely not worth it
 */


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
