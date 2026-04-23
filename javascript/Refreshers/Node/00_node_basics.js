/*
    NODE.JS BASICS
    Covering: Node.js runtime, global objects, modules, process, path, events
    
    Node.js is a JavaScript runtime built on Chrome's V8 engine.
    It enables JavaScript to run outside the browser for server-side applications.
*/

console.log("=== Node.js Basics ===\n");

// ============================================================================
// 1. WHAT IS NODE.JS?
// ============================================================================

/*
    NODE.JS:
    - JavaScript runtime environment (not a language or framework)
    - Built on V8 JavaScript engine (from Chrome)
    - Event-driven, non-blocking I/O model
    - Single-threaded with event loop
    - NPM (Node Package Manager) for packages
    
    USE CASES:
    - Web servers and APIs
    - Real-time applications (chat, gaming)
    - Command-line tools
    - Build tools and task runners
    - Microservices
*/


// ============================================================================
// 2. GLOBAL OBJECTS
// ============================================================================

console.log("============ GLOBAL OBJECTS ============\n");

/*
    GLOBAL OBJECTS (available everywhere):
    - global: Global namespace (like window in browser)
    - process: Information about current process
    - console: Console output
    - Buffer: Handle binary data
    - __dirname: Current directory path
    - __filename: Current file path
    - module: Current module info
    - require: Import modules
    - exports: Export from modules
*/

// global object (Node's equivalent of window)
console.log("Global object exists:", typeof global === 'object');

// __dirname and __filename
console.log("Current directory:", __dirname);
console.log("Current file:", __filename);

// Console methods
console.log("Standard output");
console.error("Error output");
console.warn("Warning output");
console.info("Info output");

// Console timing
console.time("operation");
// Some operation
for (let i = 0; i < 1000000; i++) {}
console.timeEnd("operation");

// Console table
const users = [
    { name: 'Alice', age: 30 },
    { name: 'Bob', age: 25 }
];
console.table(users);


// ============================================================================
// 3. PROCESS OBJECT
// ============================================================================

console.log("\n============ PROCESS OBJECT ============\n");

/*
    PROCESS OBJECT:
    - Information about current Node.js process
    - Environment variables
    - Command-line arguments
    - Exit codes
    - Events
*/

// Process info
console.log("Node version:", process.version);
console.log("Platform:", process.platform);  // darwin, linux, win32
console.log("Architecture:", process.arch);  // x64, arm, etc.
console.log("Process ID:", process.pid);
console.log("Working directory:", process.cwd());

// Memory usage
const memUsage = process.memoryUsage();
console.log("Memory (MB):", {
    rss: Math.round(memUsage.rss / 1024 / 1024),
    heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024),
    heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024)
});

// CPU usage
const cpuUsage = process.cpuUsage();
console.log("CPU usage (microseconds):", cpuUsage);

// Uptime
console.log("Uptime (seconds):", process.uptime());

// Environment variables
console.log("Environment variables:");
console.log("NODE_ENV:", process.env.NODE_ENV || 'development');
console.log("PATH:", process.env.PATH?.substring(0, 50) + '...');

// Setting custom environment variable
process.env.CUSTOM_VAR = 'custom_value';
console.log("Custom var:", process.env.CUSTOM_VAR);

// Command-line arguments
// Run: node 00_node_basics.js arg1 arg2 --flag
console.log("\nCommand-line arguments:");
console.log("All args:", process.argv);
console.log("Script args:", process.argv.slice(2));

// Process events
process.on('exit', (code) => {
    console.log(`Process exiting with code: ${code}`);
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught exception:', error);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled rejection:', reason);
});

// Exit process (commented out to continue execution)
// process.exit(0);  // 0 = success, non-zero = error


// ============================================================================
// 4. MODULES (COMMONJS)
// ============================================================================

console.log("\n============ MODULES (COMMONJS) ============\n");

/*
    COMMONJS MODULES:
    - Default module system in Node.js
    - require() to import
    - module.exports or exports to export
    - Synchronous loading
    - Cached after first load
*/

// Built-in modules (no path needed)
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log("Loaded built-in modules: fs, path, os");

// Module info
console.log("Module:", {
    id: module.id,
    filename: module.filename,
    loaded: module.loaded,
    parent: module.parent?.id
});

// Exporting examples (in separate files)
/*
// math.js
module.exports.add = (a, b) => a + b;
module.exports.subtract = (a, b) => a - b;

// Or single export
module.exports = function multiply(a, b) {
    return a * b;
};

// Or shorthand
exports.divide = (a, b) => a / b;
*/

// Importing examples
/*
const math = require('./math');
console.log(math.add(5, 3));

const multiply = require('./math');
console.log(multiply(5, 3));

const { add, subtract } = require('./math');
console.log(add(5, 3));
*/

// Module caching
console.log("Loaded modules:", Object.keys(require.cache).length);


// ============================================================================
// 5. PATH MODULE
// ============================================================================

console.log("\n============ PATH MODULE ============\n");

/*
    PATH MODULE:
    - Cross-platform path manipulation
    - Join, resolve, normalize paths
    - Extract path components
    - Handle different OS path separators
*/

// Path separator (\ on Windows, / on Unix)
console.log("Path separator:", path.sep);
console.log("Path delimiter:", path.delimiter);

// Joining paths
const fullPath = path.join(__dirname, 'files', 'data.txt');
console.log("Joined path:", fullPath);

// Resolving paths (absolute)
const absolutePath = path.resolve('files', 'data.txt');
console.log("Resolved path:", absolutePath);

// Path components
const filePath = '/home/user/documents/file.txt';
console.log("\nPath components for:", filePath);
console.log("Directory:", path.dirname(filePath));    // /home/user/documents
console.log("Basename:", path.basename(filePath));    // file.txt
console.log("Extension:", path.extname(filePath));    // .txt
console.log("Name:", path.basename(filePath, '.txt')); // file

// Parse path
const parsed = path.parse(filePath);
console.log("\nParsed path:", parsed);
/*
{
    root: '/',
    dir: '/home/user/documents',
    base: 'file.txt',
    ext: '.txt',
    name: 'file'
}
*/

// Format path (opposite of parse)
const formatted = path.format({
    dir: '/home/user/documents',
    base: 'newfile.txt'
});
console.log("Formatted path:", formatted);

// Normalize path (resolve .. and .)
const messy = '/home/user/../user/./documents/../documents/file.txt';
console.log("Normalized:", path.normalize(messy));

// Relative path
const from = '/home/user/documents';
const to = '/home/user/pictures/photo.jpg';
console.log("Relative path:", path.relative(from, to));

// Check if path is absolute
console.log("Is absolute:", path.isAbsolute(filePath));
console.log("Is absolute:", path.isAbsolute('./relative'));


// ============================================================================
// 6. OS MODULE
// ============================================================================

console.log("\n============ OS MODULE ============\n");

/*
    OS MODULE:
    - Operating system information
    - CPU, memory, network info
    - System uptime
    - Home directory, temp directory
*/

// Platform info
console.log("Platform:", os.platform());      // linux, darwin, win32
console.log("Architecture:", os.arch());      // x64, arm
console.log("OS type:", os.type());          // Linux, Darwin, Windows_NT
console.log("Release:", os.release());
console.log("Hostname:", os.hostname());

// CPU info
const cpus = os.cpus();
console.log("\nCPU info:");
console.log("CPU count:", cpus.length);
console.log("CPU model:", cpus[0].model);
console.log("CPU speed (MHz):", cpus[0].speed);

// Memory info
const totalMem = os.totalmem();
const freeMem = os.freemem();
console.log("\nMemory info:");
console.log("Total (GB):", (totalMem / 1024 / 1024 / 1024).toFixed(2));
console.log("Free (GB):", (freeMem / 1024 / 1024 / 1024).toFixed(2));
console.log("Used (%):", ((1 - freeMem / totalMem) * 100).toFixed(2));

// System uptime
console.log("\nUptime (hours):", (os.uptime() / 3600).toFixed(2));

// User info
console.log("\nUser info:", os.userInfo());

// Directories
console.log("\nHome directory:", os.homedir());
console.log("Temp directory:", os.tmpdir());

// Network interfaces
const networks = os.networkInterfaces();
console.log("\nNetwork interfaces:", Object.keys(networks));

// EOL (End of Line) character
console.log("EOL character:", JSON.stringify(os.EOL));


// ============================================================================
// 7. TIMERS
// ============================================================================

console.log("\n============ TIMERS ============\n");

/*
    TIMERS:
    - setTimeout: Run once after delay
    - setInterval: Run repeatedly at intervals
    - setImmediate: Run after current event loop
    - process.nextTick: Run before next event loop
*/

// setTimeout
console.log("Setting timeout...");
const timeoutId = setTimeout(() => {
    console.log("Timeout executed (1 second)");
}, 1000);

// Clear timeout (if needed)
// clearTimeout(timeoutId);

// setInterval
let count = 0;
const intervalId = setInterval(() => {
    count++;
    console.log(`Interval ${count}`);
    
    if (count >= 3) {
        clearInterval(intervalId);
        console.log("Interval cleared");
    }
}, 500);

// setImmediate (after I/O operations)
setImmediate(() => {
    console.log("Immediate executed");
});

// process.nextTick (before next event loop iteration)
process.nextTick(() => {
    console.log("Next tick executed");
});

console.log("Synchronous code");

// Execution order:
// 1. Synchronous code
// 2. process.nextTick
// 3. setImmediate
// 4. setTimeout/setInterval


// ============================================================================
// 8. BUFFER
// ============================================================================

console.log("\n============ BUFFER ============\n");

/*
    BUFFER:
    - Handle binary data
    - Fixed-size chunk of memory
    - Like arrays of integers (0-255)
    - Used for file I/O, network operations
*/

// Create buffer from string
const buf1 = Buffer.from('Hello');
console.log("Buffer from string:", buf1);
console.log("Buffer content:", buf1.toString());

// Create empty buffer
const buf2 = Buffer.alloc(10);  // 10 bytes, filled with 0
console.log("Empty buffer:", buf2);

// Create unsafe buffer (uninitialized, faster)
const buf3 = Buffer.allocUnsafe(10);
console.log("Unsafe buffer:", buf3);

// Buffer methods
console.log("\nBuffer methods:");
console.log("Length:", buf1.length);
console.log("toString():", buf1.toString());
console.log("toString('hex'):", buf1.toString('hex'));
console.log("toString('base64'):", buf1.toString('base64'));
console.log("toJSON():", buf1.toJSON());

// Write to buffer
buf2.write('Node.js');
console.log("After write:", buf2.toString());

// Buffer concatenation
const buf4 = Buffer.concat([buf1, buf2]);
console.log("Concatenated:", buf4.toString());

// Compare buffers
console.log("Compare:", Buffer.compare(buf1, buf2));  // -1, 0, or 1


// ============================================================================
// 9. EVENT LOOP
// ============================================================================

console.log("\n============ EVENT LOOP ============\n");

/*
    EVENT LOOP:
    - Heart of Node.js asynchronous programming
    - Single-threaded but non-blocking
    - Phases: timers → I/O callbacks → idle → poll → check → close
    
    Execution order:
    1. Synchronous code
    2. process.nextTick callbacks
    3. Microtasks (Promise callbacks)
    4. Timer callbacks (setTimeout, setInterval)
    5. I/O callbacks
    6. setImmediate callbacks
*/

console.log("1. Synchronous");

setTimeout(() => console.log("2. setTimeout"), 0);

setImmediate(() => console.log("3. setImmediate"));

process.nextTick(() => console.log("4. nextTick"));

Promise.resolve().then(() => console.log("5. Promise"));

console.log("6. Synchronous");


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

console.log("\n============ BEST PRACTICES ============\n");

/*
    NODE.JS BEST PRACTICES:
    
    1. Use async/await over callbacks
    2. Handle errors properly (try-catch, error events)
    3. Use environment variables for configuration
    4. Never block the event loop
    5. Use streams for large files
    6. Implement proper logging
    7. Use process managers (PM2) in production
    8. Monitor memory usage
    9. Use clustering for multi-core systems
    10. Keep dependencies updated
    11. Use ESLint for code quality
    12. Write tests (Jest, Mocha)
    13. Use TypeScript for type safety
    14. Implement rate limiting
    15. Validate and sanitize user input
*/

// Good: Non-blocking
const asyncOperation = async () => {
    const result = await Promise.resolve(42);
    return result;
};

// Bad: Blocking the event loop
// let sum = 0;
// for (let i = 0; i < 10000000000; i++) {
//     sum += i;  // Blocks event loop!
// }

// Good: Error handling
process.on('uncaughtException', (error) => {
    console.error('Fatal error:', error);
    process.exit(1);
});

// Good: Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    // Close connections, finish operations
    process.exit(0);
});


console.log("\n=== Node.js Basics Complete ===");

/*
    KEY TAKEAWAYS:
    
    1. Node.js is a JavaScript runtime, not a language
    2. Global objects: global, process, __dirname, __filename
    3. Process object for environment, args, events
    4. CommonJS modules with require/exports
    5. Path module for cross-platform paths
    6. OS module for system information
    7. Timers: setTimeout, setInterval, setImmediate, nextTick
    8. Buffer for binary data
    9. Event loop enables non-blocking I/O
    10. Always handle errors and avoid blocking operations
*/
