/*
    JAVASCRIPT BASICS - FUNDAMENTAL CONCEPTS
    Covering: Variables, data types, operators, basic syntax
    
    This file demonstrates the fundamental building blocks of JavaScript programming.
*/

console.log("=== JavaScript Basics Demonstration ===\n");

// ============================================================================
// 1. VARIABLES AND DECLARATIONS
// ============================================================================

console.log("============ VARIABLES ============\n");

/*
    VARIABLE DECLARATIONS:
    
    var: Function-scoped, can be redeclared, hoisted
    let: Block-scoped, cannot be redeclared, not hoisted
    const: Block-scoped, cannot be reassigned or redeclared, not hoisted
    
    BEST PRACTICE: Use const by default, let when you need to reassign, avoid var
*/

// var - old way (avoid in modern JavaScript)
var oldVariable = "I'm a var";
var oldVariable = "I can be redeclared";  // No error
oldVariable = "I can be reassigned";

// let - for variables that will change
let counter = 0;
counter = 1;  // OK
counter += 1; // OK
// let counter = 5; // ERROR: Cannot redeclare

// const - for constants (cannot be reassigned)
const PI = 3.14159;
const MAX_SIZE = 100;
// PI = 3.14; // ERROR: Cannot reassign const

// Important: const objects/arrays can have their properties modified
const person = { name: "Alice" };
person.name = "Bob";  // OK - modifying property
person.age = 30;      // OK - adding property
// person = {};       // ERROR - cannot reassign

const numbers = [1, 2, 3];
numbers.push(4);      // OK - modifying array
// numbers = [];      // ERROR - cannot reassign


// ============================================================================
// 2. DATA TYPES - PRIMITIVES
// ============================================================================

console.log("\n============ PRIMITIVE DATA TYPES ============\n");

/*
    PRIMITIVE TYPES (immutable):
    1. undefined - variable declared but not assigned
    2. null - intentional absence of value
    3. boolean - true or false
    4. number - integers and floats (64-bit)
    5. bigint - arbitrary precision integers (ES2020)
    6. string - text data
    7. symbol - unique identifier (ES6)
*/

// undefined - declared but not assigned
let notAssigned;
console.log("undefined:", notAssigned);  // undefined
console.log("typeof undefined:", typeof notAssigned);  // "undefined"

// null - intentional empty value
let empty = null;
console.log("null:", empty);  // null
console.log("typeof null:", typeof empty);  // "object" (historical bug!)

// boolean - true or false
let isActive = true;
let isCompleted = false;
console.log("boolean:", isActive, isCompleted);

// number - all numbers are 64-bit floating point
let integer = 42;
let float = 3.14159;
let negative = -100;
let exponential = 2.5e6;  // 2,500,000
let binary = 0b1010;      // 10 in decimal
let octal = 0o12;         // 10 in decimal
let hex = 0xFF;           // 255 in decimal

console.log("numbers:", integer, float, negative, exponential);

// Special numeric values
console.log("Infinity:", 1 / 0);        // Infinity
console.log("-Infinity:", -1 / 0);      // -Infinity
console.log("NaN:", 0 / 0);             // NaN (Not a Number)
console.log("isNaN:", isNaN("hello")); // true

// Number properties
console.log("MAX_SAFE_INTEGER:", Number.MAX_SAFE_INTEGER);  // 9007199254740991
console.log("MIN_SAFE_INTEGER:", Number.MIN_SAFE_INTEGER);  // -9007199254740991
console.log("MAX_VALUE:", Number.MAX_VALUE);
console.log("MIN_VALUE:", Number.MIN_VALUE);

// bigint - for numbers larger than MAX_SAFE_INTEGER (ES2020)
const bigNumber = 9007199254740991n;
const anotherBig = BigInt("9007199254740991");
console.log("bigint:", bigNumber + 1n);

// string - text enclosed in quotes
let single = 'single quotes';
let double = "double quotes";
let backtick = `backtick quotes`;  // Template literals (ES6)

// Template literals support multiline and interpolation
let name = "Alice";
let age = 30;
let greeting = `Hello, ${name}!
You are ${age} years old.
Next year you'll be ${age + 1}.`;
console.log("template literal:", greeting);

// String properties and methods
console.log("string length:", "hello".length);  // 5
console.log("uppercase:", "hello".toUpperCase());  // "HELLO"
console.log("substring:", "hello".substring(0, 2));  // "he"

// symbol - unique identifier (ES6)
const sym1 = Symbol("description");
const sym2 = Symbol("description");
console.log("symbols equal?", sym1 === sym2);  // false (always unique)


// ============================================================================
// 3. DATA TYPES - REFERENCE TYPES
// ============================================================================

console.log("\n============ REFERENCE TYPES ============\n");

/*
    REFERENCE TYPES (mutable):
    - Object
    - Array
    - Function
    - Date
    - RegExp
    - Map, Set, WeakMap, WeakSet (ES6)
*/

// Object - collection of key-value pairs
const user = {
    name: "Alice",
    age: 30,
    email: "alice@example.com",
    isActive: true
};

console.log("object:", user);
console.log("access property:", user.name);     // Dot notation
console.log("access property:", user["email"]); // Bracket notation

// Adding/modifying properties
user.city = "New York";
user.age = 31;

// Nested objects
const company = {
    name: "Tech Corp",
    address: {
        street: "123 Main St",
        city: "San Francisco",
        zip: "94102"
    }
};

console.log("nested:", company.address.city);

// Array - ordered collection
const fruits = ["apple", "banana", "orange"];
const mixed = [1, "two", true, { name: "object" }, [1, 2, 3]];

console.log("array:", fruits);
console.log("access element:", fruits[0]);  // "apple"
console.log("array length:", fruits.length);  // 3

// Array methods
fruits.push("grape");        // Add to end
fruits.pop();                // Remove from end
fruits.unshift("mango");     // Add to beginning
fruits.shift();              // Remove from beginning

// Function - callable object
function greet(name) {
    return `Hello, ${name}!`;
}

const greetArrow = (name) => `Hello, ${name}!`;

console.log("function:", greet("Bob"));
console.log("arrow function:", greetArrow("Carol"));


// ============================================================================
// 4. TYPE CHECKING AND CONVERSION
// ============================================================================

console.log("\n============ TYPE CHECKING ============\n");

// typeof operator
console.log("typeof 42:", typeof 42);                    // "number"
console.log("typeof 'hello':", typeof "hello");          // "string"
console.log("typeof true:", typeof true);                // "boolean"
console.log("typeof undefined:", typeof undefined);      // "undefined"
console.log("typeof null:", typeof null);                // "object" (bug!)
console.log("typeof {}:", typeof {});                    // "object"
console.log("typeof []:", typeof []);                    // "object"
console.log("typeof function:", typeof function() {});   // "function"

// Better array check
console.log("Array.isArray([]):", Array.isArray([]));         // true
console.log("Array.isArray({}):", Array.isArray({}));         // false

// Type conversion (coercion)
console.log("\n--- Type Conversion ---");

/**
 * TYPE COERCION EXPLAINED:
 * =======================
 * 
 * EXPLICIT COERCION:
 * - You manually convert types
 * - String(), Number(), Boolean()
 * - Clear and intentional
 * 
 * IMPLICIT COERCION:
 * - JavaScript auto-converts types
 * - Can be confusing and buggy
 * - Happens in operators (+, -, ==, etc.)
 * 
 * COMMON COERCION RULES:
 * 
 * TO STRING:
 * - Any + string → both become strings
 * - "3" + 2 → "32" (concatenation, not addition!)
 * 
 * TO NUMBER:
 * - Math operators (-, *, /, %) convert to number
 * - "3" - 1 → 2 (subtraction works)
 * - Unary + converts to number
 * 
 * TO BOOLEAN:
 * - if/while/ternary convert to boolean
 * - Falsy: false, 0, "", null, undefined, NaN
 * - Truthy: EVERYTHING else (including "0", "false", [], {})
 * 
 * GOTCHAS:
 * - "3" + 2 → "32" (string concat)
 * - "3" - 2 → 1 (number subtraction)
 * - [] + [] → "" (empty string!)
 * - {} + [] → 0 (number!)
 * - These are confusing - use explicit conversion!
 */

// EXPLICIT STRING CONVERSION
console.log("String(123):", String(123));           // "123" ✓
console.log("(123).toString():", (123).toString()); // "123" ✓

// IMPLICIT STRING CONVERSION (CONCATENATION)
console.log("123 + '':", 123 + "");                 // "123" (+ with string = concat!)
console.log("'Value: ' + 42:", "Value: " + 42);    // "Value: 42"

// EXPLICIT NUMBER CONVERSION
console.log("Number('123'):", Number("123"));       // 123 ✓
console.log("+'123':", +"123");                     // 123 (unary plus trick)
console.log("parseInt('123px'):", parseInt("123px"));  // 123 (stops at non-digit)
console.log("parseFloat('3.14'):", parseFloat("3.14"));  // 3.14

// IMPLICIT NUMBER CONVERSION (MATH OPERATORS)
console.log("'3' - 1:", "3" - 1);                   // 2 (- coerces to number)
console.log("'3' * 2:", "3" * 2);                   // 6
console.log("'10' / '2':", "10" / "2");             // 5

// EXPLICIT BOOLEAN CONVERSION
console.log("Boolean(1):", Boolean(1));             // true ✓
console.log("Boolean(0):", Boolean(0));             // false ✓
console.log("Boolean(''):", Boolean(""));           // false ✓
console.log("Boolean('hi'):", Boolean("hi"));       // true ✓

// IMPLICIT BOOLEAN CONVERSION (if/while/ternary)
if (1) console.log("  1 is truthy");                // Executes
if (0) console.log("  Won't print");                // Doesn't execute
if ("") console.log("  Won't print");               // Doesn't execute
if ("0") console.log("  '0' is truthy!");           // Executes! (non-empty string)

/**
 * FALSY VALUES (only 6 in JavaScript):
 * 1. false
 * 2. 0 (and -0)
 * 3. "" (empty string)
 * 4. null
 * 5. undefined
 * 6. NaN
 * 
 * TRUTHY VALUES (EVERYTHING else):
 * - "0" (non-empty string, even "false")
 * - [] (empty array)
 * - {} (empty object)
 * - function() {} (functions)
 * - All other values
 * 
 * COMMON MISTAKE:
 * if (myArray.length) { }  // ✓ Good: 0 is falsy
 * if (myObject) { }        // ❌ Bad: {} is truthy even when empty!
 * 
 * BETTER:
 * if (Object.keys(myObject).length) { }  // ✓ Check key count
 */


// ============================================================================
// 5. OPERATORS
// ============================================================================

console.log("\n============ OPERATORS ============\n");

// Arithmetic operators
let a = 10, b = 3;
console.log("Addition:", a + b);        // 13
console.log("Subtraction:", a - b);     // 7
console.log("Multiplication:", a * b);  // 30
console.log("Division:", a / b);        // 3.3333...
console.log("Modulo:", a % b);          // 1
console.log("Exponentiation:", a ** b); // 1000 (ES7)

// Increment/Decrement
let x = 5;
console.log("x++:", x++);  // 5 (returns then increments)
console.log("x:", x);      // 6
console.log("++x:", ++x);  // 7 (increments then returns)
console.log("x:", x);      // 7

// Assignment operators
let y = 10;
y += 5;   // y = y + 5
y -= 3;   // y = y - 3
y *= 2;   // y = y * 2
y /= 4;   // y = y / 4
y %= 3;   // y = y % 3
console.log("after operations:", y);

// Comparison operators
/**
 * == vs === - THE MOST IMPORTANT DISTINCTION:
 * ===========================================
 * 
 * == (LOOSE EQUALITY):
 * - Performs type coercion before comparing
 * - Can lead to unexpected results
 * - Generally considered bad practice
 * 
 * === (STRICT EQUALITY):
 * - No type coercion
 * - Compares both value AND type
 * - ALWAYS use this (with rare exceptions)
 * 
 * WHY === IS BETTER:
 * - Predictable behavior
 * - Catches type bugs
 * - No hidden coercion surprises
 * 
 * WEIRD == BEHAVIOR:
 * 0 == false → true (both coerce to 0)
 * "" == false → true (both coerce to 0)
 * null == undefined → true (special case)
 * "0" == 0 → true (string coerces to number)
 * 
 * RULE: Always use === and !== (strict equality)
 * EXCEPTION: Checking for null/undefined together (x == null)
 */

console.log("5 == '5':", 5 == "5");    // true (coerces "5" to 5) ❌ Confusing!
console.log("5 === '5':", 5 === "5");  // false (different types) ✓ Clear!

console.log("5 != '5':", 5 != "5");    // false (loose inequality)
console.log("5 !== '5':", 5 !== "5");  // true (strict inequality) ✓ Use this!

// Weird == examples (why you should avoid it)
console.log("0 == false:", 0 == false);           // true ❌
console.log("'' == false:", "" == false);         // true ❌
console.log("null == undefined:", null == undefined); // true (only case where == is useful)
console.log("'0' == 0:", "0" == 0);              // true ❌
console.log("'\\n' == 0:", "\n" == 0);           // true ❌ (whitespace coerces to 0!)

// === never has these issues
console.log("0 === false:", 0 === false);        // false ✓
console.log("'' === false:", "" === false);      // false ✓
console.log("null === undefined:", null === undefined); // false ✓

/**
 * WHEN TO USE == (rare):
 * Only when checking for null OR undefined:
 * 
 * if (x == null) { }  // Catches both null and undefined
 * // Equivalent to:
 * // if (x === null || x === undefined) { }
 * 
 * This is the ONLY acceptable use of ==
 */

// Other comparison operators
console.log("10 > 5:", 10 > 5);        // true
console.log("10 >= 10:", 10 >= 10);    // true
console.log("5 < 10:", 5 < 10);        // true
console.log("5 <= 5:", 5 <= 5);        // true

// String comparison (lexicographic/alphabetical)
console.log("'b' > 'a':", "b" > "a");           // true
console.log("'abc' < 'abd':", "abc" < "abd");   // true

// Logical operators
console.log("true && false:", true && false);  // false (AND)
console.log("true || false:", true || false);  // true (OR)
console.log("!true:", !true);                  // false (NOT)

// Short-circuit evaluation
let result1 = false && console.log("not executed");  // false (doesn't run console.log)
let result2 = true || console.log("not executed");   // true (doesn't run console.log)

// Nullish coalescing operator (ES2020)
let value1 = null ?? "default";      // "default"
let value2 = undefined ?? "default"; // "default"
let value3 = 0 ?? "default";         // 0 (0 is not null/undefined)

console.log("nullish coalescing:", value1, value2, value3);

// Optional chaining (ES2020)
const obj = { a: { b: { c: 42 } } };
console.log("optional chain:", obj?.a?.b?.c);     // 42
console.log("optional chain:", obj?.x?.y?.z);     // undefined (no error!)

// Ternary operator
let status = age >= 18 ? "adult" : "minor";
console.log("ternary:", status);

// typeof operator
console.log("typeof operator:", typeof 42, typeof "hello", typeof true);


// ============================================================================
// 6. STRING OPERATIONS
// ============================================================================

console.log("\n============ STRING OPERATIONS ============\n");

let str = "Hello, World!";

// Common string methods
console.log("charAt:", str.charAt(0));              // "H"
console.log("indexOf:", str.indexOf("World"));      // 7
console.log("includes:", str.includes("Hello"));    // true
console.log("startsWith:", str.startsWith("Hello"));  // true
console.log("endsWith:", str.endsWith("!"));        // true
console.log("slice:", str.slice(0, 5));             // "Hello"
console.log("substring:", str.substring(7, 12));    // "World"
console.log("toLowerCase:", str.toLowerCase());     // "hello, world!"
console.log("toUpperCase:", str.toUpperCase());     // "HELLO, WORLD!"
console.log("trim:", "  hello  ".trim());           // "hello"
console.log("replace:", str.replace("World", "JavaScript"));  // "Hello, JavaScript!"
console.log("split:", str.split(", "));             // ["Hello", "World!"]
console.log("repeat:", "ha".repeat(3));             // "hahaha"
console.log("padStart:", "5".padStart(3, "0"));     // "005"
console.log("padEnd:", "5".padEnd(3, "0"));         // "500"


// ============================================================================
// 7. NUMBER OPERATIONS
// ============================================================================

console.log("\n============ NUMBER OPERATIONS ============\n");

let num = 3.14159;

// Number methods
console.log("toFixed:", num.toFixed(2));            // "3.14" (string)
console.log("toPrecision:", num.toPrecision(4));    // "3.142" (string)
console.log("toString:", num.toString());           // "3.14159" (string)
console.log("toExponential:", num.toExponential()); // "3.14159e+0"

// Math object
console.log("Math.round:", Math.round(3.7));        // 4
console.log("Math.ceil:", Math.ceil(3.2));          // 4
console.log("Math.floor:", Math.floor(3.9));        // 3
console.log("Math.abs:", Math.abs(-5));             // 5
console.log("Math.max:", Math.max(1, 5, 3));        // 5
console.log("Math.min:", Math.min(1, 5, 3));        // 1
console.log("Math.pow:", Math.pow(2, 3));           // 8
console.log("Math.sqrt:", Math.sqrt(16));           // 4
console.log("Math.random:", Math.random());         // 0-1 (random)

// Random integer between min and max
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
console.log("random 1-10:", randomInt(1, 10));


// ============================================================================
// 8. VARIABLE SCOPE
// ============================================================================

console.log("\n============ VARIABLE SCOPE ============\n");

/*
    SCOPE TYPES:
    1. Global scope - accessible everywhere
    2. Function scope - var is function-scoped
    3. Block scope - let/const are block-scoped
*/

// Global scope
let globalVar = "I'm global";

function demonstrateScope() {
    // Function scope
    let functionVar = "I'm function-scoped";
    
    if (true) {
        // Block scope
        let blockVar = "I'm block-scoped";
        var functionScopedVar = "var is function-scoped, not block-scoped";
        
        console.log("Inside block:", blockVar);  // OK
    }
    
    // console.log(blockVar);  // ERROR: blockVar not defined
    console.log("Outside block:", functionScopedVar);  // OK (var is function-scoped)
}

demonstrateScope();


// ============================================================================
// 9. HOISTING
// ============================================================================

console.log("\n============ HOISTING ============\n");

/*
    HOISTING:
    Variable and function declarations are moved to the top of their scope
    
    - var declarations are hoisted (initialized to undefined)
    - function declarations are hoisted (fully)
    - let/const declarations are NOT accessible before declaration (TDZ)
*/

// This works (var is hoisted)
console.log("hoisted var:", hoistedVar);  // undefined
var hoistedVar = "I'm hoisted";

// This would error (let not accessible before declaration)
// console.log(hoistedLet);  // ReferenceError: Cannot access before initialization
// let hoistedLet = "Not hoisted";

// Function declarations are fully hoisted
console.log("hoisted function:", hoistedFunction());  // Works!
function hoistedFunction() {
    return "I'm hoisted!";
}


// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

console.log("\n============ BEST PRACTICES ============\n");

/*
    BEST PRACTICES:
    
    1. Use const by default, let only when reassignment needed
    2. Never use var (use let/const instead)
    3. Use === and !== instead of == and !=
    4. Use template literals for string interpolation
    5. Use descriptive variable names (camelCase)
    6. Declare variables at the top of their scope
    7. Initialize variables when declaring
    8. One variable per line for readability
    9. Use strict mode ('use strict') for safer code
    10. Avoid global variables when possible
*/

// Good naming conventions
const maxRetries = 3;              // camelCase for variables
const API_KEY = "secret";          // UPPER_CASE for constants
const userName = "alice";          // descriptive names
const isActive = true;             // boolean prefix: is, has, can
const getUserData = () => {};      // functions: verb + noun

// Bad naming conventions
// let x = 3;                      // Not descriptive
// let MAXRETRIES = 3;             // Wrong case for variable
// let user_name = "alice";        // snake_case (not JS convention)


console.log("\n=== Basics Complete ===");

/*
    KEY TAKEAWAYS:
    
    1. JavaScript is dynamically typed (types determined at runtime)
    2. Use const by default, let when needed, never var
    3. 7 primitive types: undefined, null, boolean, number, bigint, string, symbol
    4. Reference types: object, array, function
    5. === for strict equality (no type coercion)
    6. Template literals for string interpolation
    7. let/const are block-scoped, var is function-scoped
    8. Hoisting moves declarations to top of scope
*/
