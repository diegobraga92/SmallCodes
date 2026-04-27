/**
 * JAVASCRIPT ASYNCHRONOUS PROGRAMMING
 * =====================================
 * Comprehensive guide to async JavaScript
 * Callbacks, Promises, Async/Await
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT ASYNCHRONOUS PROGRAMMING");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. SYNCHRONOUS VS ASYNCHRONOUS
// ============================================================================

console.log("\n=== Synchronous vs Asynchronous ===");

/**
 * THE JAVASCRIPT EVENT LOOP EXPLAINED:
 * ====================================
 * 
 * JavaScript is SINGLE-THREADED but handles async operations efficiently
 * through the Event Loop mechanism.
 * 
 * KEY COMPONENTS:
 * 
 * 1. CALL STACK:
 *    - Execution context for function calls
 *    - LIFO (Last In, First Out)
 *    - Synchronous code executes here
 * 
 * 2. TASK QUEUE (MACRO-TASK QUEUE):
 *    - setTimeout, setInterval, I/O operations
 *    - Processed AFTER call stack is empty
 *    - One task per event loop iteration
 * 
 * 3. MICROTASK QUEUE:
 *    - Promises (.then, .catch, .finally)
 *    - process.nextTick (Node.js)
 *    - Processed BEFORE next task
 *    - ALL microtasks run before next task
 * 
 * EVENT LOOP PROCESS:
 * 1. Execute all synchronous code (call stack)
 * 2. Process ALL microtasks (promise callbacks)
 * 3. Take ONE task from task queue
 * 4. Repeat
 * 
 * PRIORITY: Sync Code > Microtasks > Tasks
 * 
 * WHY ASYNC?
 * - Prevents blocking (UI stays responsive)
 * - Enables concurrent operations (network, I/O)
 * - Better resource utilization
 */

// Synchronous (blocking) - executes line by line
console.log("1. First");   // Call stack: execute immediately
console.log("2. Second");  // Call stack: execute immediately
console.log("3. Third");   // Call stack: execute immediately
// Output order: 1, 2, 3 (predictable, synchronous)

// Asynchronous (non-blocking) - deferred execution
console.log("\nAsync example:");
console.log("1. Start");  // Call stack: execute immediately

// setTimeout schedules callback in TASK QUEUE
// Even with 0ms delay, it goes to the queue!
setTimeout(() => console.log("2. After 0ms"), 0);  // → Task Queue

console.log("3. End");    // Call stack: execute immediately

// OUTPUT ORDER: 1, 3, 2 (WHY?)
// 1. "1. Start" executes (sync)
// 2. setTimeout registers callback in task queue (async)
// 3. "3. End" executes (sync)
// 4. Call stack empty → event loop checks microtask queue (empty)
// 5. Event loop takes task from task queue → executes setTimeout callback
// 6. "2. After 0ms" executes

/**
 * MENTAL MODEL:
 * 
 * [Sync Code] executes first (call stack)
 *      ↓
 * [All Microtasks] execute next (promises)
 *      ↓
 * [One Task] executes (setTimeout, setInterval)
 *      ↓
 * [Repeat]
 */


// ============================================================================
// 2. CALLBACKS
// ============================================================================

console.log("\n=== Callbacks ===");

/**
 * Callback = function passed as argument to be executed later
 * Problem: Callback hell (pyramid of doom)
 */

// Simple callback
function fetchData(callback) {
    setTimeout(() => {
        callback("Data received");
    }, 100);
}

fetchData((data) => {
    console.log(data);
});

// Callback hell example
function step1(callback) {
    setTimeout(() => callback(null, "Step 1 done"), 100);
}

function step2(callback) {
    setTimeout(() => callback(null, "Step 2 done"), 100);
}

function step3(callback) {
    setTimeout(() => callback(null, "Step 3 done"), 100);
}

// Nested callbacks (hard to read and maintain)
step1((err, result1) => {
    if (err) return console.error(err);
    console.log(result1);
    
    step2((err, result2) => {
        if (err) return console.error(err);
        console.log(result2);
        
        step3((err, result3) => {
            if (err) return console.error(err);
            console.log(result3);
        });
    });
});


// ============================================================================
// 3. PROMISES
// ============================================================================

console.log("\n=== Promises ===");

/**
 * PROMISES EXPLAINED:
 * ==================
 * 
 * Promise = object representing eventual completion/failure of async operation
 * 
 * THREE STATES (once settled, state never changes):
 * 
 * 1. PENDING:
 *    - Initial state
 *    - Operation not yet completed
 *    - Can transition to fulfilled or rejected
 * 
 * 2. FULFILLED:
 *    - Operation succeeded
 *    - Has a result value
 *    - Triggers .then() handlers
 *    - IMMUTABLE: Cannot change to rejected
 * 
 * 3. REJECTED:
 *    - Operation failed
 *    - Has a reason (error)
 *    - Triggers .catch() handlers
 *    - IMMUTABLE: Cannot change to fulfilled
 * 
 * KEY CONCEPTS:
 * 
 * - Promise callbacks (.then, .catch) go to MICROTASK QUEUE
 * - Microtasks run BEFORE next setTimeout/setInterval
 * - Promises execute IMMEDIATELY upon creation
 * - .then() always returns a new promise (enables chaining)
 * 
 * MICROTASK QUEUE BEHAVIOR:
 * Promise callbacks are PRIORITIZED over setTimeout:
 * 
 * console.log('1');
 * setTimeout(() => console.log('2'), 0);  // Task queue
 * Promise.resolve().then(() => console.log('3'));  // Microtask queue
 * console.log('4');
 * 
 * Output: 1, 4, 3, 2
 * WHY? Sync (1,4) → Microtasks (3) → Tasks (2)
 */

// Creating a promise
const promise1 = new Promise((resolve, reject) => {
    // IMPORTANT: This executor function runs IMMEDIATELY (synchronously)
    // It doesn't wait for setTimeout - just registers the callback
    
    setTimeout(() => {
        // This callback executes later (after 100ms)
        const success = true;
        
        if (success) {
            // resolve() changes state from pending → fulfilled
            // Triggers .then() handlers (via microtask queue)
            resolve("Promise fulfilled!");
        } else {
            // reject() changes state from pending → rejected
            // Triggers .catch() handlers (via microtask queue)
            reject("Promise rejected!");
        }
    }, 100);
    
    // Promise is now in "pending" state
});

// Consuming a promise
promise1
    .then(result => {
        // Executes when promise fulfilled
        // This callback is added to MICROTASK QUEUE
        console.log(result);
        
        // Returning a value wraps it in Promise.resolve()
        // This is why we can chain .then() calls
        return "Next step";
    })
    .then(result => {
        // Second .then() receives result from first
        // Chaining works because .then() returns a new promise
        console.log(result);
    })
    .catch(error => {
        // Catches rejections from ANY previous .then()
        // Acts like try-catch for promise chain
        console.error("Error:", error);
    })
    .finally(() => {
        // Runs regardless of fulfilled or rejected
        // No argument passed (doesn't know which state)
        // Useful for cleanup (closing connections, hiding loaders)
        console.log("Promise settled (fulfilled or rejected)");
    });

/**
 * PROMISE TIMING EXAMPLE:
 * 
 * console.log('A');
 * 
 * setTimeout(() => console.log('B'), 0);  // Task queue
 * 
 * Promise.resolve().then(() => console.log('C'));  // Microtask queue
 * 
 * console.log('D');
 * 
 * OUTPUT: A, D, C, B
 * 
 * EXECUTION ORDER:
 * 1. console.log('A') - sync, executes immediately
 * 2. setTimeout - registers in task queue
 * 3. Promise.resolve().then() - registers in microtask queue
 * 4. console.log('D') - sync, executes immediately
 * 5. Call stack empty → process all microtasks → 'C'
 * 6. Take one task from task queue → 'B'
 */


// ============================================================================
// 4. PROMISE CHAINING
// ============================================================================

console.log("\n=== Promise Chaining ===");

function asyncStep1() {
    return new Promise(resolve => {
        setTimeout(() => resolve("Step 1"), 100);
    });
}

function asyncStep2(previousResult) {
    return new Promise(resolve => {
        setTimeout(() => resolve(`${previousResult} -> Step 2`), 100);
    });
}

function asyncStep3(previousResult) {
    return new Promise(resolve => {
        setTimeout(() => resolve(`${previousResult} -> Step 3`), 100);
    });
}

// Clean chaining (solves callback hell)
asyncStep1()
    .then(result1 => {
        console.log(result1);
        return asyncStep2(result1);
    })
    .then(result2 => {
        console.log(result2);
        return asyncStep3(result2);
    })
    .then(result3 => {
        console.log("Final:", result3);
    })
    .catch(error => {
        console.error("Error in chain:", error);
    });


// ============================================================================
// 5. PROMISE STATIC METHODS
// ============================================================================

console.log("\n=== Promise Static Methods ===");

/**
 * PROMISE COMBINATORS - WHEN TO USE EACH:
 * =======================================
 * 
 * 1. PROMISE.ALL([...])
 *    - Waits for ALL promises to fulfill
 *    - REJECTS if ANY promise rejects (fail-fast)
 *    - Returns: array of results in same order
 *    - USE WHEN: All operations must succeed
 *    - EXAMPLE: Fetching multiple required resources
 * 
 * 2. PROMISE.ALLSETTLED([...])
 *    - Waits for ALL promises to settle (fulfill or reject)
 *    - NEVER rejects
 *    - Returns: array of {status, value/reason} objects
 *    - USE WHEN: Want results regardless of individual failures
 *    - EXAMPLE: Running tests, batch operations with partial success
 * 
 * 3. PROMISE.RACE([...])
 *    - Returns first promise to SETTLE (fulfill OR reject)
 *    - Result/error from fastest promise
 *    - USE WHEN: Need fastest response, timeouts
 *    - EXAMPLE: Timeout mechanism, fastest server wins
 * 
 * 4. PROMISE.ANY([...])
 *    - Returns first promise to FULFILL
 *    - IGNORES rejections (continues until one succeeds)
 *    - Rejects only if ALL reject (AggregateError)
 *    - USE WHEN: Need any one success, fallback servers
 *    - EXAMPLE: Multiple CDNs, mirror servers
 */

const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.resolve(3);
const pReject = Promise.reject("Error!");

// PROMISE.ALL() - Wait for all (rejects if any rejects)
Promise.all([p1, p2, p3])
    .then(results => {
        // All succeeded: get array of results
        // Order matches input order (not completion order!)
        console.log("Promise.all:", results);  // [1, 2, 3]
    });

// Promise.all() with rejection - FAILS FAST
Promise.all([p1, pReject, p3])
    .then(results => {
        console.log("Won't reach here");
    })
    .catch(error => {
        // If ANY promise rejects, entire Promise.all rejects
        // Returns the FIRST rejection reason
        // NOTE: Other promises may still resolve, but results are ignored
        console.log("Promise.all rejected:", error);
    });

// PROMISE.ALLSETTLED() - Wait for all (never rejects)
Promise.allSettled([p1, pReject, p3])
    .then(results => {
        // Always resolves with status of each promise
        // Perfect for when you want all results, even failures
        console.log("Promise.allSettled:", results);
        // [
        //   { status: 'fulfilled', value: 1 },
        //   { status: 'rejected', reason: 'Error!' },
        //   { status: 'fulfilled', value: 3 }
        // ]
        
        // Filter successful results:
        const successful = results
            .filter(r => r.status === 'fulfilled')
            .map(r => r.value);
    });

// PROMISE.RACE() - First to settle (fulfill or reject)
const slow = new Promise(resolve => setTimeout(() => resolve("slow"), 200));
const fast = new Promise(resolve => setTimeout(() => resolve("fast"), 50));

Promise.race([slow, fast])
    .then(result => {
        // Fastest promise wins (fulfill or reject)
        console.log("Promise.race:", result);  // "fast"
        
        // USE CASE: Timeout pattern
        // const timeout = new Promise((_, reject) => 
        //     setTimeout(() => reject('Timeout!'), 5000));
        // Promise.race([fetchData(), timeout])
    });

// PROMISE.ANY() - First to fulfill (ignores rejections)
const p4 = Promise.reject("Error 1");
const p5 = new Promise(resolve => setTimeout(() => resolve("Success"), 100));
const p6 = Promise.reject("Error 2");

Promise.any([p4, p5, p6])
    .then(result => {
        // Returns first SUCCESSFUL result
        // Rejections are ignored until all reject
        console.log("Promise.any:", result);  // "Success"
        
        // USE CASE: Fastest successful server
        // Promise.any([
        //     fetch('https://api1.com/data'),
        //     fetch('https://api2.com/data'),
        //     fetch('https://api3.com/data')
        // ])
    });

/**
 * QUICK DECISION GUIDE:
 * 
 * Need all to succeed? → Promise.all()
 * Want all results (even failures)? → Promise.allSettled()
 * Need fastest (success or fail)? → Promise.race()
 * Need first success (ignore fails)? → Promise.any()
 */


// ============================================================================
// 6. ASYNC/AWAIT
// ============================================================================

console.log("\n=== Async/Await ===");

/**
 * ASYNC/AWAIT EXPLAINED:
 * =====================
 * 
 * KEY CONCEPTS:
 * 
 * 1. ASYNC KEYWORD:
 *    - Makes a function return a Promise
 *    - return value; → Promise.resolve(value)
 *    - throw error; → Promise.reject(error)
 *    - Enables use of 'await' inside the function
 * 
 * 2. AWAIT KEYWORD:
 *    - Can ONLY be used inside async functions
 *    - Pauses function execution until promise settles
 *    - Returns the resolved value (or throws if rejected)
 *    - Does NOT block other code (just pauses this function)
 * 
 * 3. HOW IT WORKS:
 *    - await suspends the async function
 *    - Returns control to caller (non-blocking!)
 *    - Resumes when promise settles
 *    - Rest of async function goes to microtask queue
 * 
 * COMMON PITFALLS:
 * 
 * 1. Forgetting await (returns promise instead of value)
 * 2. Sequential awaits when parallel is possible
 * 3. Not handling errors (unhandled promise rejection)
 * 4. Using await in non-async function
 * 5. Blocking loops with await (use Promise.all instead)
 */

// Async function - always returns a Promise
async function fetchUserData() {
    // Whatever you return is automatically wrapped in Promise.resolve()
    return "User data";  
    
    // These are equivalent:
    // return "User data";
    // return Promise.resolve("User data");
}

// Calling async function returns a Promise
fetchUserData().then(data => console.log(data));

// IMPORTANT: async function returning non-promise value
async function example1() {
    return 42;  // Still returns Promise.resolve(42)
}
// Must use .then() or await to get the value:
example1().then(value => console.log(value));  // 42

// Await - pauses execution, returns resolved value
async function processData() {
    try {
        // Each await PAUSES this function until promise settles
        // Other code continues running (non-blocking)
        
        const step1Result = await asyncStep1();
        // Function paused here until asyncStep1() resolves
        // Once resolved, step1Result gets the value
        console.log("Await step 1:", step1Result);
        
        // This wait is SEQUENTIAL - only starts after step1 completes
        const step2Result = await asyncStep2(step1Result);
        console.log("Await step 2:", step2Result);
        
        const step3Result = await asyncStep3(step2Result);
        console.log("Await step 3:", step3Result);
        
        // Returning from async function wraps in Promise
        return step3Result;
    } catch (error) {
        // try-catch works with await!
        // If any promise rejects, catch block executes
        console.error("Error in processData:", error);
        
        // Re-throwing makes the returned promise reject
        throw error;
    }
}

// Calling async function
processData()
    .then(result => console.log("Final:", result))
    .catch(err => console.error("Caught:", err));

/**
 * PITFALL #1: Forgetting await
 */
async function mistake1() {
    // WRONG: Forgot await - result is a Promise, not the value!
    const data = fetchUserData();
    console.log(data);  // Promise { 'User data' } ❌
    
    // RIGHT: Use await to get the value
    const correctData = await fetchUserData();
    console.log(correctData);  // 'User data' ✓
}

/**
 * PITFALL #2: Sequential when parallel is possible
 * (see section 8 for detailed explanation)
 */


// ============================================================================
// 7. ERROR HANDLING WITH ASYNC/AWAIT
// ============================================================================

console.log("\n=== Error Handling ===");

async function riskyOperation() {
    throw new Error("Something went wrong!");
}

// Try-catch
async function handleErrors1() {
    try {
        const result = await riskyOperation();
        console.log(result);
    } catch (error) {
        console.error("Caught error:", error.message);
    }
}

handleErrors1();

// .catch() on async function call
async function handleErrors2() {
    const result = await riskyOperation();
    return result;
}

handleErrors2().catch(error => {
    console.error("Caught via .catch():", error.message);
});


// ============================================================================
// 8. PARALLEL VS SEQUENTIAL EXECUTION
// ============================================================================

console.log("\n=== Parallel vs Sequential ===");

/**
 * CRITICAL ASYNC/AWAIT PERFORMANCE CONCEPT:
 * =========================================
 * 
 * SEQUENTIAL:
 * - Operations run one after another
 * - Each await blocks the next operation
 * - Total time = sum of all operations
 * - USE WHEN: Operations depend on each other
 * 
 * PARALLEL:
 * - Operations start simultaneously
 * - All awaits happen at once (via Promise.all)
 * - Total time = slowest operation
 * - USE WHEN: Operations are independent
 * 
 * EXAMPLE:
 * 3 API calls, each takes 100ms:
 * - Sequential: 100 + 100 + 100 = 300ms ❌
 * - Parallel: max(100, 100, 100) = 100ms ✓
 * 
 * THIS IS ONE OF THE MOST COMMON PERFORMANCE MISTAKES!
 */

function delay(ms, value) {
    return new Promise(resolve => setTimeout(() => resolve(value), ms));
}

// Sequential (slow) - awaits happen one by one
async function sequential() {
    console.time("Sequential");
    
    // SLOW: Each await waits for previous to finish
    const result1 = await delay(100, "First");   // Wait 100ms
    const result2 = await delay(100, "Second");  // Wait another 100ms
    const result3 = await delay(100, "Third");   // Wait another 100ms
    // Total: ~300ms
    
    console.timeEnd("Sequential");  // ~300ms
    return [result1, result2, result3];
}

// Parallel (fast) - all operations start immediately
async function parallel() {
    console.time("Parallel");
    
    // FAST: Start all promises immediately (don't await yet!)
    // All three delays start at the same time
    const [result1, result2, result3] = await Promise.all([
        delay(100, "First"),   // Starts immediately
        delay(100, "Second"),  // Starts immediately
        delay(100, "Third")    // Starts immediately
    ]);
    // Wait for ALL to complete (whichever is slowest)
    // Total: ~100ms (they overlap!)
    
    console.timeEnd("Parallel");  // ~100ms
    return [result1, result2, result3];
}

// WHEN TO USE SEQUENTIAL:
// - Operations depend on each other
async function sequentialExample() {
    const userId = await getUserId();        // Need this first
    const userData = await getUser(userId);  // Depends on userId
    const orders = await getOrders(userData.id);  // Depends on userData
    return orders;
}

// WHEN TO USE PARALLEL:
// - Operations are independent
async function parallelExample() {
    // These don't depend on each other - run simultaneously!
    const [users, products, categories] = await Promise.all([
        fetchUsers(),
        fetchProducts(),
        fetchCategories()
    ]);
    return { users, products, categories };
}

// HYBRID: Mix sequential and parallel
async function hybridExample() {
    // Step 1: Get user (sequential, must happen first)
    const user = await getUser();
    
    // Step 2: Fetch user's data in parallel (all need user.id)
    const [profile, orders, preferences] = await Promise.all([
        fetchProfile(user.id),      // Start all three
        fetchOrders(user.id),        // at the same time
        fetchPreferences(user.id)
    ]);
    
    return { user, profile, orders, preferences };
}

sequential().then(results => console.log("Sequential results:", results));
parallel().then(results => console.log("Parallel results:", results));


// ============================================================================
// 9. ASYNC ITERATION
// ============================================================================

console.log("\n=== Async Iteration ===");

// Async generator
async function* asyncGenerator() {
    yield await delay(50, 1);
    yield await delay(50, 2);
    yield await delay(50, 3);
}

// Consume with for await...of
async function consumeAsyncIterator() {
    for await (const value of asyncGenerator()) {
        console.log("Async value:", value);
    }
}

consumeAsyncIterator();


// ============================================================================
// 10. PROMISIFICATION
// ============================================================================

console.log("\n=== Promisification ===");

// Convert callback-based function to promise-based
function callbackFunction(value, callback) {
    setTimeout(() => {
        callback(null, value * 2);
    }, 100);
}

// Promisify utility
function promisify(fn) {
    return function(...args) {
        return new Promise((resolve, reject) => {
            fn(...args, (err, result) => {
                if (err) reject(err);
                else resolve(result);
            });
        });
    };
}

const promisifiedFunction = promisify(callbackFunction);

promisifiedFunction(5).then(result => {
    console.log("Promisified result:", result);
});


// ============================================================================
// 11. REAL-WORLD PATTERNS
// ============================================================================

console.log("\n=== Real-World Patterns ===");

// API call simulation
async function fetchFromAPI(url) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (url) {
                resolve({ data: `Response from ${url}` });
            } else {
                reject(new Error("URL is required"));
            }
        }, 100);
    });
}

// Retry logic
async function fetchWithRetry(url, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetchFromAPI(url);
            return response;
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            console.log(`Retry ${i + 1}/${maxRetries}`);
            await delay(1000 * (i + 1));  // Exponential backoff
        }
    }
}

// Timeout wrapper
async function withTimeout(promise, ms) {
    const timeout = new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Timeout")), ms)
    );
    return Promise.race([promise, timeout]);
}

// Rate limiting
class RateLimiter {
    constructor(maxConcurrent) {
        this.maxConcurrent = maxConcurrent;
        this.running = 0;
        this.queue = [];
    }
    
    async run(fn) {
        while (this.running >= this.maxConcurrent) {
            await new Promise(resolve => this.queue.push(resolve));
        }
        
        this.running++;
        try {
            return await fn();
        } finally {
            this.running--;
            const resolve = this.queue.shift();
            if (resolve) resolve();
        }
    }
}

const limiter = new RateLimiter(2);  // Max 2 concurrent

async function testRateLimiter() {
    const tasks = Array.from({ length: 5 }, (_, i) =>
        limiter.run(async () => {
            console.log(`Task ${i} started`);
            await delay(100);
            console.log(`Task ${i} completed`);
            return i;
        })
    );
    
    const results = await Promise.all(tasks);
    console.log("All tasks completed:", results);
}

testRateLimiter();


// ============================================================================
// 12. COMMON PITFALLS
// ============================================================================

console.log("\n=== Common Pitfalls ===");

// 1. Forgetting to await
async function forgotAwait() {
    const promise = delay(100, "result");
    console.log(promise);  // Promise object, not the result!
    
    const result = await delay(100, "result");
    console.log(result);  // "result"
}

// 2. Sequential when parallel is better
async function unnecessarySequential() {
    // Slow - tasks are independent but run sequentially
    const user = await fetchFromAPI("/user");
    const posts = await fetchFromAPI("/posts");
    const comments = await fetchFromAPI("/comments");
    
    // Fast - run in parallel
    const [user2, posts2, comments2] = await Promise.all([
        fetchFromAPI("/user"),
        fetchFromAPI("/posts"),
        fetchFromAPI("/comments")
    ]);
}

// 3. Not handling errors
async function unhandledError() {
    await riskyOperation();  // Unhandled promise rejection!
}
// unhandledError();  // Causes warning

// 4. Using async without await
async function unnecessaryAsync() {
    return "value";  // No await, async is unnecessary
}

// 5. await in loop (usually wrong)
async function awaitInLoop() {
    const ids = [1, 2, 3, 4, 5];
    
    // Sequential (slow)
    for (const id of ids) {
        await fetchFromAPI(`/item/${id}`);
    }
    
    // Parallel (fast)
    await Promise.all(ids.map(id => fetchFromAPI(`/item/${id}`)));
}


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Promises solve callback hell");
console.log("2. async/await makes async code look synchronous");
console.log("3. async functions always return promises");
console.log("4. Always handle errors (try-catch or .catch())");
console.log("5. Use Promise.all() for parallel execution");
console.log("6. Use Promise.allSettled() when you need all results");
console.log("7. Don't await in loops unless sequential needed");
console.log("8. Use Promise.race() for timeout patterns");
console.log("=".repeat(80));
