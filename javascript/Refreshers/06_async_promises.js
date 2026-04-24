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

// Synchronous (blocking)
console.log("1. First");
console.log("2. Second");
console.log("3. Third");

// Asynchronous (non-blocking)
console.log("\nAsync example:");
console.log("1. Start");
setTimeout(() => console.log("2. After 0ms"), 0);
console.log("3. End");
// Output: 1, 3, 2 (setTimeout goes to event queue)


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
 * Promise = object representing eventual completion/failure of async operation
 * States:
 * - Pending: Initial state
 * - Fulfilled: Operation succeeded
 * - Rejected: Operation failed
 */

// Creating a promise
const promise1 = new Promise((resolve, reject) => {
    setTimeout(() => {
        const success = true;
        if (success) {
            resolve("Promise fulfilled!");
        } else {
            reject("Promise rejected!");
        }
    }, 100);
});

// Consuming a promise
promise1
    .then(result => {
        console.log(result);
        return "Next step";
    })
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.error("Error:", error);
    })
    .finally(() => {
        console.log("Promise settled (fulfilled or rejected)");
    });


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

const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.resolve(3);
const pReject = Promise.reject("Error!");

// Promise.all() - Wait for all (rejects if any rejects)
Promise.all([p1, p2, p3])
    .then(results => {
        console.log("Promise.all:", results);  // [1, 2, 3]
    });

// Promise.all() with rejection
Promise.all([p1, pReject, p3])
    .then(results => {
        console.log("Won't reach here");
    })
    .catch(error => {
        console.log("Promise.all rejected:", error);
    });

// Promise.allSettled() - Wait for all (never rejects)
Promise.allSettled([p1, pReject, p3])
    .then(results => {
        console.log("Promise.allSettled:", results);
        // [
        //   { status: 'fulfilled', value: 1 },
        //   { status: 'rejected', reason: 'Error!' },
        //   { status: 'fulfilled', value: 3 }
        // ]
    });

// Promise.race() - First to settle (fulfill or reject)
const slow = new Promise(resolve => setTimeout(() => resolve("slow"), 200));
const fast = new Promise(resolve => setTimeout(() => resolve("fast"), 50));

Promise.race([slow, fast])
    .then(result => {
        console.log("Promise.race:", result);  // "fast"
    });

// Promise.any() - First to fulfill (ignores rejections)
const p4 = Promise.reject("Error 1");
const p5 = new Promise(resolve => setTimeout(() => resolve("Success"), 100));
const p6 = Promise.reject("Error 2");

Promise.any([p4, p5, p6])
    .then(result => {
        console.log("Promise.any:", result);  // "Success"
    });


// ============================================================================
// 6. ASYNC/AWAIT
// ============================================================================

console.log("\n=== Async/Await ===");

/**
 * async/await = syntactic sugar for promises
 * - async function always returns a promise
 * - await pauses execution until promise settles
 * - Makes async code look synchronous
 */

// Async function
async function fetchUserData() {
    return "User data";  // Automatically wrapped in Promise.resolve()
}

fetchUserData().then(data => console.log(data));

// Await
async function processData() {
    try {
        const step1Result = await asyncStep1();
        console.log("Await step 1:", step1Result);
        
        const step2Result = await asyncStep2(step1Result);
        console.log("Await step 2:", step2Result);
        
        const step3Result = await asyncStep3(step2Result);
        console.log("Await step 3:", step3Result);
        
        return step3Result;
    } catch (error) {
        console.error("Error in processData:", error);
        throw error;
    }
}

processData();


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

function delay(ms, value) {
    return new Promise(resolve => setTimeout(() => resolve(value), ms));
}

// Sequential (slow)
async function sequential() {
    console.time("Sequential");
    const result1 = await delay(100, "First");
    const result2 = await delay(100, "Second");
    const result3 = await delay(100, "Third");
    console.timeEnd("Sequential");  // ~300ms
    return [result1, result2, result3];
}

// Parallel (fast)
async function parallel() {
    console.time("Parallel");
    const [result1, result2, result3] = await Promise.all([
        delay(100, "First"),
        delay(100, "Second"),
        delay(100, "Third")
    ]);
    console.timeEnd("Parallel");  // ~100ms
    return [result1, result2, result3];
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
