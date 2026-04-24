/**
 * JAVASCRIPT ES6+ FEATURES
 * ==========================
 * Modern JavaScript features from ES6 (ES2015) onwards
 * Template literals, destructuring, spread/rest, and more
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT ES6+ FEATURES");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. LET AND CONST (ES6)
// ============================================================================

console.log("\n=== let and const ===");

/**
 * let: Block-scoped, can be reassigned
 * const: Block-scoped, cannot be reassigned
 * var: Function-scoped, hoisted (avoid!)
 */

// Block scope
{
    let x = 10;
    const y = 20;
    // var z = 30;  // Function-scoped, leaks out!
}
// console.log(x);  // Error: x is not defined
// console.log(z);  // Would work with var!

// const prevents reassignment
const PI = 3.14159;
// PI = 3.14;  // Error!

// But const doesn't make objects immutable
const obj = { value: 1 };
obj.value = 2;  // OK - modifying property
// obj = {};  // Error - reassigning

console.log("const object:", obj);


// ============================================================================
// 2. TEMPLATE LITERALS (ES6)
// ============================================================================

console.log("\n=== Template Literals ===");

const name = "Alice";
const age = 30;

// Old way
const oldWay = "Hello, " + name + "! You are " + age + " years old.";

// New way - template literals
const newWay = `Hello, ${name}! You are ${age} years old.`;
console.log(newWay);

// Multi-line strings
const multiLine = `
    Line 1
    Line 2
    Line 3
`;
console.log("Multi-line:", multiLine);

// Expressions in template literals
const sum = `2 + 2 = ${2 + 2}`;
console.log(sum);

// Tagged templates
function highlight(strings, ...values) {
    return strings.reduce((result, str, i) => {
        return result + str + (values[i] ? `**${values[i]}**` : '');
    }, '');
}

const highlighted = highlight`Hello, ${name}! Age: ${age}`;
console.log("Tagged:", highlighted);


// ============================================================================
// 3. ARROW FUNCTIONS (ES6)
// ============================================================================

console.log("\n=== Arrow Functions ===");

// Traditional function
function traditionalAdd(a, b) {
    return a + b;
}

// Arrow function
const arrowAdd = (a, b) => a + b;

console.log("Arrow add:", arrowAdd(2, 3));

// Single parameter (parentheses optional)
const double = x => x * 2;
console.log("Double:", double(5));

// No parameters
const greet = () => "Hello!";
console.log(greet());

// Multiple statements (need braces and return)
const complexCalc = (x, y) => {
    const sum = x + y;
    const product = x * y;
    return { sum, product };
};
console.log("Complex:", complexCalc(3, 4));

// Arrow functions don't have their own 'this'
const obj2 = {
    value: 42,
    traditional: function() {
        setTimeout(function() {
            // console.log(this.value);  // undefined - 'this' is lost
        }, 100);
    },
    arrow: function() {
        setTimeout(() => {
            console.log("  Arrow 'this':", this.value);  // 42 - 'this' preserved
        }, 100);
    }
};
obj2.arrow();


// ============================================================================
// 4. DEFAULT PARAMETERS (ES6)
// ============================================================================

console.log("\n=== Default Parameters ===");

function multiply(a, b = 1) {
    return a * b;
}

console.log("With default:", multiply(5));     // 5
console.log("Without default:", multiply(5, 2)); // 10

// Default can be expression
function createUser(name, id = Date.now()) {
    return { name, id };
}

console.log("User:", createUser("Alice"));


// ============================================================================
// 5. REST PARAMETERS (ES6)
// ============================================================================

console.log("\n=== Rest Parameters ===");

// Collect remaining arguments into array
function sum(...numbers) {
    return numbers.reduce((acc, n) => acc + n, 0);
}

console.log("Sum:", sum(1, 2, 3, 4, 5));

// Rest must be last parameter
function log(level, ...messages) {
    console.log(`[${level}]`, ...messages);
}

log("INFO", "User", "logged in");


// ============================================================================
// 6. SPREAD OPERATOR (ES6)
// ============================================================================

console.log("\n=== Spread Operator ===");

// Arrays
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
console.log("Combined:", combined);

// Copy array
const copy = [...arr1];

// Function arguments
const numbers = [1, 5, 3, 9, 2];
console.log("Max:", Math.max(...numbers));

// Objects
const defaults = { theme: "light", lang: "en" };
const userPrefs = { lang: "es" };
const merged = { ...defaults, ...userPrefs };
console.log("Merged:", merged);


// ============================================================================
// 7. ENHANCED OBJECT LITERALS (ES6)
// ============================================================================

console.log("\n=== Enhanced Object Literals ===");

const x = 10, y = 20;

// Property shorthand
const point = { x, y };  // Same as { x: x, y: y }
console.log("Point:", point);

// Method shorthand
const calc = {
    add(a, b) { return a + b; },  // No 'function' keyword
    subtract(a, b) { return a - b; }
};

// Computed property names
const prop = "dynamicKey";
const obj3 = {
    [prop]: "value",
    [`${prop}2`]: "value2"
};
console.log("Computed:", obj3);


// ============================================================================
// 8. OPTIONAL CHAINING (ES2020)
// ============================================================================

console.log("\n=== Optional Chaining ===");

const user = {
    name: "Alice",
    address: {
        city: "NYC"
    }
};

// Old way
const street = user.address && user.address.street;

// New way
const street2 = user.address?.street;
console.log("Street:", street2);  // undefined, no error

// With arrays
const firstItem = user.items?.[0];

// With functions
const result = user.getName?.();  // undefined if getName doesn't exist


// ============================================================================
// 9. NULLISH COALESCING (ES2020)
// ============================================================================

console.log("\n=== Nullish Coalescing ===");

/**
 * ?? returns right side only if left is null or undefined
 * || returns right side if left is any falsy value (0, '', false, null, undefined)
 */

const value1 = 0;
const value2 = null;

console.log("OR:", value1 || "default");     // "default" (0 is falsy)
console.log("Nullish:", value1 ?? "default"); // 0 (0 is not null/undefined)

console.log("OR:", value2 || "default");     // "default"
console.log("Nullish:", value2 ?? "default"); // "default"

// Useful for optional parameters
function config(options = {}) {
    const timeout = options.timeout ?? 5000;  // 0 is valid timeout
    const retries = options.retries ?? 3;
    return { timeout, retries };
}

console.log("Config:", config({ timeout: 0 }));


// ============================================================================
// 10. FOR...OF LOOP (ES6)
// ============================================================================

console.log("\n=== for...of Loop ===");

const fruits = ["apple", "banana", "orange"];

// for...of (iterates values)
for (const fruit of fruits) {
    console.log(" ", fruit);
}

// for...in (iterates keys/indices)
for (const index in fruits) {
    console.log(" ", index, fruits[index]);
}

// With strings
for (const char of "Hello") {
    console.log(" ", char);
}


// ============================================================================
// 11. SYMBOLS (ES6)
// ============================================================================

console.log("\n=== Symbols ===");

// Unique identifier
const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log("Symbols equal?", sym1 === sym2);  // false - always unique

// Use as object key
const SECRET_KEY = Symbol("secret");
const obj4 = {
    publicProp: "visible",
    [SECRET_KEY]: "hidden"
};

console.log("Public:", obj4.publicProp);
console.log("Symbol:", obj4[SECRET_KEY]);
console.log("Keys:", Object.keys(obj4));  // Doesn't include symbol


// ============================================================================
// 12. SETS (ES6)
// ============================================================================

console.log("\n=== Sets ===");

// Set = collection of unique values
const set = new Set([1, 2, 2, 3, 3, 3]);
console.log("Set:", set);  // Set(3) { 1, 2, 3 }

// Add, delete, has
set.add(4);
set.delete(1);
console.log("Has 2?", set.has(2));
console.log("Size:", set.size);

// Convert to array
const uniqueArray = [...set];
console.log("Array:", uniqueArray);

// Remove duplicates
const duplicates = [1, 2, 2, 3, 3, 3];
const unique = [...new Set(duplicates)];
console.log("Unique:", unique);


// ============================================================================
// 13. MAPS (ES6)
// ============================================================================

console.log("\n=== Maps ===");

// Map = collection of key-value pairs (any type as key)
const map = new Map();
map.set("name", "Alice");
map.set(1, "number key");
map.set(true, "boolean key");

console.log("Get name:", map.get("name"));
console.log("Has key 1?", map.has(1));
console.log("Size:", map.size);

// Iterate
for (const [key, value] of map) {
    console.log(" ", key, "=>", value);
}

// Object as key (advantage over plain objects)
const objKey = { id: 1 };
map.set(objKey, "object value");
console.log("Object key:", map.get(objKey));


// ============================================================================
// 14. WEAK MAP AND WEAK SET (ES6)
// ============================================================================

console.log("\n=== WeakMap and WeakSet ===");

/**
 * WeakMap/WeakSet:
 * - Keys must be objects
 * - No iteration methods
 * - Allow garbage collection
 * - Use for private data, caching
 */

const weakMap = new WeakMap();
let obj5 = { id: 1 };
weakMap.set(obj5, "metadata");

console.log("WeakMap:", weakMap.get(obj5));

// When obj5 is no longer referenced, it can be garbage collected
// Even if still in WeakMap!


// ============================================================================
// 15. LOGICAL ASSIGNMENT (ES2021)
// ============================================================================

console.log("\n=== Logical Assignment ===");

let a = 1;
let b = 0;
let c = null;

// Logical OR assignment (||=)
b ||= 10;  // b = b || 10
console.log("OR assignment:", b);  // 10 (0 is falsy)

// Logical AND assignment (&&=)
a &&= 5;  // a = a && 5
console.log("AND assignment:", a);  // 5 (1 is truthy)

// Nullish coalescing assignment (??=)
c ??= 20;  // c = c ?? 20
console.log("Nullish assignment:", c);  // 20 (null is nullish)


// ============================================================================
// 16. NUMERIC SEPARATORS (ES2021)
// ============================================================================

console.log("\n=== Numeric Separators ===");

// Use _ for readability
const billion = 1_000_000_000;
const bytes = 0b1010_0001;
const hex = 0xFF_00_FF;

console.log("Billion:", billion);
console.log("Bytes:", bytes);
console.log("Hex:", hex);


// ============================================================================
// 17. BIGINT (ES2020)
// ============================================================================

console.log("\n=== BigInt ===");

// For integers larger than Number.MAX_SAFE_INTEGER
const bigNumber = 9007199254740991n;  // n suffix
const bigFromConstructor = BigInt("9007199254740991");

console.log("BigInt:", bigNumber);
console.log("Addition:", bigNumber + 1n);

// Can't mix BigInt with Number
// console.log(bigNumber + 1);  // Error!
console.log("Mixed:", bigNumber + BigInt(1));


// ============================================================================
// 18. STRING METHODS (ES6+)
// ============================================================================

console.log("\n=== String Methods ===");

const str = "Hello World";

// startsWith, endsWith (ES6)
console.log("Starts with 'Hello':", str.startsWith("Hello"));
console.log("Ends with 'World':", str.endsWith("World"));

// includes (ES6)
console.log("Includes 'Wor':", str.includes("Wor"));

// repeat (ES6)
console.log("Repeat:", "Ha".repeat(3));

// padStart, padEnd (ES2017)
console.log("Pad start:", "5".padStart(3, "0"));  // "005"
console.log("Pad end:", "5".padEnd(3, "0"));      // "500"

// trimStart, trimEnd (ES2019)
const padded = "  text  ";
console.log("Trim start:", padded.trimStart());
console.log("Trim end:", padded.trimEnd());

// replaceAll (ES2021)
const text = "foo foo foo";
console.log("Replace all:", text.replaceAll("foo", "bar"));


// ============================================================================
// 19. ARRAY METHODS (ES6+)
// ============================================================================

console.log("\n=== Array Methods ===");

// Array.from (ES6)
const arrayLike = { 0: "a", 1: "b", 2: "c", length: 3 };
const realArray = Array.from(arrayLike);
console.log("Array.from:", realArray);

// Array.of (ES6)
const arr = Array.of(1, 2, 3);
console.log("Array.of:", arr);

// find, findIndex (ES6)
const numbers2 = [1, 5, 3, 9, 2];
console.log("find:", numbers2.find(n => n > 5));
console.log("findIndex:", numbers2.findIndex(n => n > 5));

// flat, flatMap (ES2019)
const nested = [1, [2, 3], [4, [5, 6]]];
console.log("flat:", nested.flat(2));

// at (ES2022)
const arr3 = [1, 2, 3];
console.log("at(-1):", arr3.at(-1));  // Last element


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Use let/const instead of var");
console.log("2. Template literals for string interpolation");
console.log("3. Arrow functions for concise syntax");
console.log("4. Spread (...) for copying and merging");
console.log("5. Rest (...) for collecting arguments");
console.log("6. Destructuring for extracting values");
console.log("7. Optional chaining (?.) for safe access");
console.log("8. Nullish coalescing (??) for default values");
console.log("9. Set/Map for specialized collections");
console.log("10. Modern array/string methods");
console.log("=".repeat(80));
