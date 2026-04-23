/*
    JAVASCRIPT CONTROL FLOW
    Covering: if/else, switch, loops, break/continue, exception handling
    
    Control flow statements determine the order in which code executes.
*/

console.log("=== JavaScript Control Flow ===\n");

// ============================================================================
// 1. CONDITIONAL STATEMENTS - IF/ELSE
// ============================================================================

console.log("============ IF/ELSE STATEMENTS ============\n");

/*
    IF/ELSE SYNTAX:
    if (condition) {
        // executes if condition is truthy
    } else if (anotherCondition) {
        // executes if first condition is falsy and this is truthy
    } else {
        // executes if all conditions are falsy
    }
*/

const age = 25;
const hasLicense = true;

// Simple if
if (age >= 18) {
    console.log("You are an adult");
}

// if...else
if (age >= 21) {
    console.log("You can drink in the US");
} else {
    console.log("You cannot drink in the US");
}

// if...else if...else
if (age < 13) {
    console.log("Child");
} else if (age < 20) {
    console.log("Teenager");
} else if (age < 65) {
    console.log("Adult");
} else {
    console.log("Senior");
}

// Multiple conditions with logical operators
if (age >= 18 && hasLicense) {
    console.log("You can drive");
}

if (age >= 65 || hasLicense === false) {
    console.log("May need special consideration");
}

// Truthy and Falsy values
const value = "";  // Falsy
if (value) {
    console.log("Truthy");
} else {
    console.log("Falsy");  // This executes
}

/*
    FALSY VALUES:
    - false
    - 0
    - "" (empty string)
    - null
    - undefined
    - NaN
    
    Everything else is truthy, including:
    - " " (space)
    - [] (empty array)
    - {} (empty object)
    - "0" (string)
    - "false" (string)
*/


// ============================================================================
// 2. TERNARY OPERATOR
// ============================================================================

console.log("\n============ TERNARY OPERATOR ============\n");

/*
    TERNARY SYNTAX:
    condition ? expressionIfTrue : expressionIfFalse
    
    Good for simple conditions, avoid nesting
*/

const canVote = age >= 18 ? "Yes" : "No";
console.log("Can vote:", canVote);

// Nested ternary (avoid if possible, hard to read)
const ageGroup = age < 13 ? "child" : age < 20 ? "teen" : "adult";
console.log("Age group:", ageGroup);

// Better: use if/else for complex conditions
let ageCategory;
if (age < 13) {
    ageCategory = "child";
} else if (age < 20) {
    ageCategory = "teen";
} else {
    ageCategory = "adult";
}


// ============================================================================
// 3. SWITCH STATEMENT
// ============================================================================

console.log("\n============ SWITCH STATEMENT ============\n");

/*
    SWITCH SYNTAX:
    switch (expression) {
        case value1:
            // code
            break;
        case value2:
            // code
            break;
        default:
            // code if no case matches
    }
    
    Uses strict equality (===) for comparison
    Don't forget break statements!
*/

const day = "Monday";

switch (day) {
    case "Monday":
        console.log("Start of the work week");
        break;
    case "Tuesday":
    case "Wednesday":
    case "Thursday":
        console.log("Midweek");
        break;
    case "Friday":
        console.log("TGIF!");
        break;
    case "Saturday":
    case "Sunday":
        console.log("Weekend!");
        break;
    default:
        console.log("Invalid day");
}

// Switch without break (fall-through)
const grade = "B";
let message;

switch (grade) {
    case "A":
    case "B":
        message = "Great job!";
        break;
    case "C":
        message = "Good";
        break;
    case "D":
        message = "Needs improvement";
        break;
    case "F":
        message = "Failed";
        break;
    default:
        message = "Invalid grade";
}
console.log("Grade message:", message);


// ============================================================================
// 4. FOR LOOP
// ============================================================================

console.log("\n============ FOR LOOP ============\n");

/*
    FOR LOOP SYNTAX:
    for (initialization; condition; increment) {
        // code block
    }
*/

// Basic for loop
console.log("Counting 1-5:");
for (let i = 1; i <= 5; i++) {
    console.log(i);
}

// Looping through array
const fruits = ["apple", "banana", "orange"];
console.log("\nFruits:");
for (let i = 0; i < fruits.length; i++) {
    console.log(`${i}: ${fruits[i]}`);
}

// Nested for loops
console.log("\nMultiplication table (partial):");
for (let i = 1; i <= 3; i++) {
    for (let j = 1; j <= 3; j++) {
        console.log(`${i} x ${j} = ${i * j}`);
    }
}

// For loop with multiple variables
for (let i = 0, j = 10; i < 5; i++, j--) {
    console.log(`i: ${i}, j: ${j}`);
}


// ============================================================================
// 5. WHILE LOOP
// ============================================================================

console.log("\n============ WHILE LOOP ============\n");

/*
    WHILE LOOP SYNTAX:
    while (condition) {
        // code block
        // must update condition to avoid infinite loop
    }
    
    Executes while condition is truthy
*/

let count = 1;
console.log("While loop counting:");
while (count <= 5) {
    console.log(count);
    count++;
}

// While with array
const numbers = [1, 2, 3, 4, 5];
let index = 0;
console.log("\nArray with while:");
while (index < numbers.length) {
    console.log(numbers[index]);
    index++;
}


// ============================================================================
// 6. DO...WHILE LOOP
// ============================================================================

console.log("\n============ DO...WHILE LOOP ============\n");

/*
    DO...WHILE SYNTAX:
    do {
        // code block (executes at least once)
    } while (condition);
    
    Executes code block once, then checks condition
*/

let num = 1;
console.log("Do-while counting:");
do {
    console.log(num);
    num++;
} while (num <= 5);

// Executes at least once, even if condition is false
let x = 10;
do {
    console.log("This runs once:", x);
} while (x < 5);  // Condition is false, but block executed once


// ============================================================================
// 7. FOR...OF LOOP (ES6)
// ============================================================================

console.log("\n============ FOR...OF LOOP ============\n");

/*
    FOR...OF SYNTAX:
    for (const element of iterable) {
        // code block
    }
    
    Iterates over iterable objects (arrays, strings, Maps, Sets, etc.)
    Best for arrays when you don't need the index
*/

const colors = ["red", "green", "blue"];

console.log("Colors with for...of:");
for (const color of colors) {
    console.log(color);
}

// With strings
const text = "Hello";
console.log("\nCharacters:");
for (const char of text) {
    console.log(char);
}

// With destructuring
const users = [
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 }
];

console.log("\nUsers:");
for (const { name, age } of users) {
    console.log(`${name} is ${age} years old`);
}


// ============================================================================
// 8. FOR...IN LOOP
// ============================================================================

console.log("\n============ FOR...IN LOOP ============\n");

/*
    FOR...IN SYNTAX:
    for (const key in object) {
        // code block
    }
    
    Iterates over enumerable properties of an object
    Can also be used with arrays (returns indices as strings)
    Prefer for...of for arrays
*/

const person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

console.log("Object properties:");
for (const key in person) {
    console.log(`${key}: ${person[key]}`);
}

// With arrays (not recommended, use for...of instead)
const arr = ["a", "b", "c"];
console.log("\nArray indices:");
for (const index in arr) {
    console.log(`${index}: ${arr[index]}`);  // index is a string!
}


// ============================================================================
// 9. BREAK AND CONTINUE
// ============================================================================

console.log("\n============ BREAK AND CONTINUE ============\n");

/*
    BREAK: exits the loop immediately
    CONTINUE: skips the current iteration and continues with next
*/

// Break - exit loop when condition is met
console.log("Break example (find first even):");
for (let i = 1; i <= 10; i++) {
    if (i % 2 === 0) {
        console.log("First even number:", i);
        break;  // Exits loop
    }
}

// Continue - skip current iteration
console.log("\nContinue example (skip odd numbers):");
for (let i = 1; i <= 5; i++) {
    if (i % 2 !== 0) {
        continue;  // Skip to next iteration
    }
    console.log("Even number:", i);
}

// Break in nested loops (only breaks inner loop)
console.log("\nBreak in nested loops:");
for (let i = 1; i <= 3; i++) {
    for (let j = 1; j <= 3; j++) {
        if (j === 2) {
            break;  // Only breaks inner loop
        }
        console.log(`i: ${i}, j: ${j}`);
    }
}

// Labels for breaking outer loops
console.log("\nLabeled break:");
outerLoop: for (let i = 1; i <= 3; i++) {
    for (let j = 1; j <= 3; j++) {
        if (j === 2) {
            break outerLoop;  // Breaks outer loop
        }
        console.log(`i: ${i}, j: ${j}`);
    }
}


// ============================================================================
// 10. TRY...CATCH...FINALLY
// ============================================================================

console.log("\n============ TRY...CATCH...FINALLY ============\n");

/*
    TRY...CATCH SYNTAX:
    try {
        // code that may throw error
    } catch (error) {
        // handle error
    } finally {
        // always executes (optional)
    }
*/

// Basic try-catch
try {
    const result = riskyOperation();
    console.log("Result:", result);
} catch (error) {
    console.log("Error caught:", error.message);
}

function riskyOperation() {
    throw new Error("Something went wrong!");
}

// Try-catch with finally
try {
    console.log("Trying...");
    // Might throw error
} catch (error) {
    console.log("Caught error:", error.message);
} finally {
    console.log("Finally always runs");
}

// Catching specific errors
try {
    JSON.parse("invalid json");
} catch (error) {
    if (error instanceof SyntaxError) {
        console.log("JSON parsing error:", error.message);
    } else {
        console.log("Other error:", error.message);
    }
}

// Throwing custom errors
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    const result = divide(10, 0);
} catch (error) {
    console.log("Division error:", error.message);
}


// ============================================================================
// 11. ARRAY ITERATION METHODS
// ============================================================================

console.log("\n============ ARRAY ITERATION METHODS ============\n");

/*
    Modern array methods (functional programming style):
    - forEach: executes function for each element
    - map: creates new array with results
    - filter: creates new array with elements that pass test
    - find: returns first element that passes test
    - some: checks if at least one element passes test
    - every: checks if all elements pass test
    - reduce: reduces array to single value
*/

const nums = [1, 2, 3, 4, 5];

// forEach - iterate without return
console.log("forEach:");
nums.forEach((num, index) => {
    console.log(`Index ${index}: ${num}`);
});

// map - transform elements
const doubled = nums.map(num => num * 2);
console.log("\nmap (doubled):", doubled);

// filter - select elements
const evens = nums.filter(num => num % 2 === 0);
console.log("\nfilter (evens):", evens);

// find - first matching element
const firstEven = nums.find(num => num % 2 === 0);
console.log("\nfind (first even):", firstEven);

// some - at least one match
const hasEven = nums.some(num => num % 2 === 0);
console.log("\nsome (has even):", hasEven);

// every - all match
const allPositive = nums.every(num => num > 0);
console.log("\nevery (all positive):", allPositive);

// reduce - accumulate
const sum = nums.reduce((acc, num) => acc + num, 0);
console.log("\nreduce (sum):", sum);


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

console.log("\n============ BEST PRACTICES ============\n");

/*
    CONTROL FLOW BEST PRACTICES:
    
    1. Use === for comparisons (strict equality)
    2. Avoid nested ternary operators
    3. Always use break in switch statements (unless intentional fall-through)
    4. Prefer for...of over for...in for arrays
    5. Use array methods (map, filter, reduce) over traditional loops
    6. Keep loop bodies small and focused
    7. Avoid modifying loop variables inside the loop
    8. Always handle errors with try-catch for risky operations
    9. Use descriptive variable names in loops
    10. Extract complex conditions into functions
*/

// Good: Descriptive loop variable
for (let userIndex = 0; userIndex < users.length; userIndex++) {
    // Process user
}

// Good: Extract complex condition
function isAdult(age) {
    return age >= 18;
}

if (isAdult(age)) {
    console.log("Adult");
}

// Good: Use array methods
const adultUsers = users.filter(user => user.age >= 18);

// Bad: Traditional loop
const adultUsersOld = [];
for (let i = 0; i < users.length; i++) {
    if (users[i].age >= 18) {
        adultUsersOld.push(users[i]);
    }
}


console.log("\n=== Control Flow Complete ===");

/*
    KEY TAKEAWAYS:
    
    1. if/else for conditional execution
    2. switch for multiple specific values
    3. Ternary for simple conditions
    4. for loop for counted iterations
    5. while loop for condition-based iterations
    6. for...of for iterating arrays/iterables
    7. for...in for iterating object properties
    8. break exits loop, continue skips iteration
    9. try-catch for error handling
    10. Array methods (map, filter, reduce) for functional style
*/
