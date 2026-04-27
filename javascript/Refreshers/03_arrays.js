/**
 * JAVASCRIPT ARRAYS AND ARRAY METHODS
 * =====================================
 * Comprehensive guide to arrays in JavaScript
 * From basics to advanced array manipulation
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT ARRAYS AND ARRAY METHODS");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. ARRAY BASICS
// ============================================================================

/**
 * Arrays are ordered collections of values
 * - Can contain mixed types (not recommended)
 * - Zero-indexed
 * - Dynamic size
 * - Reference type
 */

// Creating arrays
const arr1 = [1, 2, 3, 4, 5];
const arr2 = new Array(5);  // Creates array with 5 empty slots
const arr3 = new Array(1, 2, 3);  // Creates [1, 2, 3]
const arr4 = Array.of(5);  // Creates [5], not array with 5 slots
const arr5 = Array.from("hello");  // Creates ['h', 'e', 'l', 'l', 'o']

console.log("\n=== Array Creation ===");
console.log("Literal:", arr1);
console.log("new Array(5):", arr2);
console.log("Array.of(5):", arr4);
console.log("Array.from('hello'):", arr5);

// Array length
const fruits = ["apple", "banana", "orange"];
console.log("\n=== Length ===");
console.log("Length:", fruits.length);
fruits.length = 2;  // Truncates array
console.log("After setting length to 2:", fruits);
fruits.length = 4;  // Extends with empty slots
console.log("After setting length to 4:", fruits);


// ============================================================================
// 2. ACCESSING AND MODIFYING ARRAYS
// ============================================================================

const colors = ["red", "green", "blue"];

console.log("\n=== Accessing Elements ===");
console.log("First element:", colors[0]);
console.log("Last element:", colors[colors.length - 1]);
console.log("Last element (at):", colors.at(-1));  // ES2022
console.log("Second to last:", colors.at(-2));

// Modifying elements
colors[1] = "yellow";
console.log("After modification:", colors);

// Adding elements
colors[colors.length] = "purple";  // Add to end
console.log("After adding to end:", colors);


// ============================================================================
// 3. ARRAY METHODS - ADDING/REMOVING
// ============================================================================

console.log("\n=== Adding/Removing Methods ===");

// push() - Add to end (mutates, returns new length)
const nums = [1, 2, 3];
const newLength = nums.push(4, 5);
console.log("After push(4, 5):", nums, "- returned:", newLength);

// pop() - Remove from end (mutates, returns removed element)
const removed = nums.pop();
console.log("After pop():", nums, "- removed:", removed);

// unshift() - Add to beginning (mutates, returns new length)
nums.unshift(0);
console.log("After unshift(0):", nums);

// shift() - Remove from beginning (mutates, returns removed element)
const first = nums.shift();
console.log("After shift():", nums, "- removed:", first);

// splice() - Add/remove at any position (mutates, returns removed elements)
const animals = ["dog", "cat", "bird", "fish"];
const removed2 = animals.splice(2, 1, "rabbit", "hamster");
console.log("After splice(2, 1, 'rabbit', 'hamster'):", animals);
console.log("Removed:", removed2);


// ============================================================================
// 4. ARRAY METHODS - NON-MUTATING
// ============================================================================

console.log("\n=== Non-Mutating Methods ===");

const original = [1, 2, 3, 4, 5];

// slice() - Extract portion (does not mutate)
const sliced = original.slice(1, 4);  // From index 1 to 3 (not including 4)
console.log("slice(1, 4):", sliced);
console.log("Original unchanged:", original);

// concat() - Merge arrays (does not mutate)
const arr6 = [1, 2];
const arr7 = [3, 4];
const merged = arr6.concat(arr7, [5, 6]);
console.log("concat():", merged);

// join() - Create string from array
const words = ["Hello", "World"];
console.log("join(' '):", words.join(" "));
console.log("join('-'):", words.join("-"));

// reverse() - Reverse array (MUTATES!)
const toReverse = [1, 2, 3, 4, 5];
const reversed = toReverse.reverse();
console.log("reverse():", reversed, "- Original:", toReverse);  // Both changed!

// sort() - Sort array (MUTATES!)
const toSort = [3, 1, 4, 1, 5, 9, 2, 6];
toSort.sort();
console.log("sort():", toSort);  // Sorts as strings! ['1', '1', '2', '3', '4', '5', '6', '9']

// Proper numeric sort
const numbers = [3, 1, 4, 1, 5, 9, 2, 6];
numbers.sort((a, b) => a - b);  // Ascending
console.log("sort with comparator:", numbers);


// ============================================================================
// 5. ARRAY ITERATION METHODS
// ============================================================================

console.log("\n=== Iteration Methods ===");

/**
 * MUTATING vs NON-MUTATING METHODS:
 * =================================
 * 
 * CRITICAL DISTINCTION FOR DEBUGGING AND DATA INTEGRITY!
 * 
 * MUTATING (change original array):
 * - push, pop, shift, unshift
 * - splice, reverse, sort
 * - fill, copyWithin
 * - USE CAREFULLY: Can cause unexpected side effects
 * 
 * NON-MUTATING (return new array):
 * - map, filter, reduce
 * - concat, slice
 * - flat, flatMap
 * - toSorted, toReversed, toSpliced (ES2023)
 * - SAFER: Original array unchanged
 * 
 * WHY THIS MATTERS:
 * 
 * MUTATING (unexpected behavior):
 * const original = [1, 2, 3];
 * const sorted = original.sort();  // Mutates original!
 * console.log(original);  // [1, 2, 3] - CHANGED!
 * 
 * NON-MUTATING (predictable):
 * const original = [3, 1, 2];
 * const sorted = original.toSorted();  // ES2023
 * console.log(original);  // [3, 1, 2] - unchanged ✓
 * 
 * BEST PRACTICES:
 * ✓ Prefer non-mutating methods (functional style)
 * ✓ If you must mutate, copy first: [...arr].sort()
 * ✓ Use const for arrays to catch reassignment bugs
 * ✓ Consider immutable data structures for complex apps
 * 
 * PERFORMANCE NOTE:
 * - Mutating is faster (no copy overhead)
 * - But premature optimization = root of evil
 * - Prefer readability and safety first
 */

const values = [1, 2, 3, 4, 5];

// forEach() - Execute function for each element (no return value)
console.log("forEach:");
values.forEach((value, index) => {
    console.log(`  Index ${index}: ${value}`);
});

// map() - Transform each element (returns new array)
const doubled = values.map(x => x * 2);
console.log("map(x => x * 2):", doubled);

// filter() - Keep elements that pass test (returns new array)
const evens = values.filter(x => x % 2 === 0);
console.log("filter(x => x % 2 === 0):", evens);

// reduce() - Reduce to single value
const sum = values.reduce((acc, curr) => acc + curr, 0);
console.log("reduce (sum):", sum);

const product = values.reduce((acc, curr) => acc * curr, 1);
console.log("reduce (product):", product);

// reduceRight() - Reduce from right to left
const reversedStr = ["a", "b", "c"].reduceRight((acc, curr) => acc + curr, "");
console.log("reduceRight:", reversedStr);


// ============================================================================
// 6. ARRAY SEARCH METHODS
// ============================================================================

console.log("\n=== Search Methods ===");

const items = [10, 20, 30, 40, 50];

// indexOf() - First index of element (-1 if not found)
console.log("indexOf(30):", items.indexOf(30));
console.log("indexOf(99):", items.indexOf(99));

// lastIndexOf() - Last index of element
const duplicates = [1, 2, 3, 2, 1];
console.log("lastIndexOf(2):", duplicates.lastIndexOf(2));

// includes() - Check if array contains element (returns boolean)
console.log("includes(30):", items.includes(30));
console.log("includes(99):", items.includes(99));

// find() - First element that passes test
const found = items.find(x => x > 25);
console.log("find(x => x > 25):", found);

// findIndex() - Index of first element that passes test
const foundIndex = items.findIndex(x => x > 25);
console.log("findIndex(x => x > 25):", foundIndex);

// findLast() - Last element that passes test (ES2023)
const foundLast = items.findLast?.(x => x > 25);
console.log("findLast(x => x > 25):", foundLast);

// some() - Check if at least one element passes test
const hasLarge = items.some(x => x > 40);
console.log("some(x => x > 40):", hasLarge);

// every() - Check if all elements pass test
const allPositive = items.every(x => x > 0);
console.log("every(x => x > 0):", allPositive);


// ============================================================================
// 7. ARRAY FLATTENING AND MANIPULATION
// ============================================================================

console.log("\n=== Flattening and Manipulation ===");

// flat() - Flatten nested arrays (ES2019)
const nested = [1, [2, 3], [4, [5, 6]]];
console.log("flat():", nested.flat());  // One level
console.log("flat(2):", nested.flat(2));  // Two levels
console.log("flat(Infinity):", nested.flat(Infinity));  // All levels

// flatMap() - Map then flatten (ES2019)
const sentences = ["Hello world", "How are you"];
const allWords = sentences.flatMap(s => s.split(" "));
console.log("flatMap(s => s.split(' ')):", allWords);

// fill() - Fill array with static value (MUTATES!)
const fillArr = [1, 2, 3, 4, 5];
fillArr.fill(0, 2, 4);  // Fill with 0 from index 2 to 3
console.log("fill(0, 2, 4):", fillArr);

// copyWithin() - Copy part of array to another location (MUTATES!)
const copyArr = [1, 2, 3, 4, 5];
copyArr.copyWithin(0, 3);  // Copy from index 3 to index 0
console.log("copyWithin(0, 3):", copyArr);


// ============================================================================
// 8. ARRAY DESTRUCTURING
// ============================================================================

console.log("\n=== Array Destructuring ===");

const point = [10, 20, 30];

// Basic destructuring
const [x, y, z] = point;
console.log("Destructured:", x, y, z);

// Skip elements
const [first2, , third] = point;
console.log("With skip:", first2, third);

// Rest pattern
const [head, ...tail] = [1, 2, 3, 4, 5];
console.log("Head:", head, "Tail:", tail);

// Default values
const [a = 0, b = 0, c = 0, d = 0] = [1, 2];
console.log("With defaults:", a, b, c, d);

// Swapping variables
let var1 = 10, var2 = 20;
[var1, var2] = [var2, var1];
console.log("After swap:", var1, var2);


// ============================================================================
// 9. SPREAD OPERATOR WITH ARRAYS
// ============================================================================

console.log("\n=== Spread Operator ===");

const arr8 = [1, 2, 3];
const arr9 = [4, 5, 6];

// Combining arrays
const combined = [...arr8, ...arr9];
console.log("Combined:", combined);

// Copying array (shallow)
const copy = [...arr8];
console.log("Copy:", copy);
console.log("Are they equal?", copy === arr8);  // false - different references

// Adding elements
const withExtra = [0, ...arr8, 4];
console.log("With extra:", withExtra);

// Spreading in function calls
console.log("Math.max():", Math.max(...arr8));


// ============================================================================
// 10. ADVANCED ARRAY PATTERNS
// ============================================================================

console.log("\n=== Advanced Patterns ===");

// Removing duplicates
const withDuplicates = [1, 2, 2, 3, 3, 3, 4, 5, 5];
const unique = [...new Set(withDuplicates)];
console.log("Remove duplicates:", unique);

// Grouping (simulated - native groupBy coming)
const people = [
    { name: "Alice", age: 25 },
    { name: "Bob", age: 30 },
    { name: "Charlie", age: 25 }
];

const groupedByAge = people.reduce((acc, person) => {
    const key = person.age;
    if (!acc[key]) acc[key] = [];
    acc[key].push(person);
    return acc;
}, {});
console.log("Grouped by age:", groupedByAge);

// Array.from with mapping function
const squares = Array.from({ length: 5 }, (_, i) => (i + 1) ** 2);
console.log("Squares (1-5):", squares);

// Chunking array
function chunk(array, size) {
    return Array.from(
        { length: Math.ceil(array.length / size) },
        (_, i) => array.slice(i * size, i * size + size)
    );
}
console.log("Chunked:", chunk([1, 2, 3, 4, 5, 6, 7], 3));

// Finding intersection
const arr10 = [1, 2, 3, 4];
const arr11 = [3, 4, 5, 6];
const intersection = arr10.filter(x => arr11.includes(x));
console.log("Intersection:", intersection);

// Finding difference
const difference = arr10.filter(x => !arr11.includes(x));
console.log("Difference:", difference);


// ============================================================================
// 11. ARRAY-LIKE OBJECTS
// ============================================================================

console.log("\n=== Array-like Objects ===");

// Arguments object (in non-arrow functions)
function oldFunction() {
    console.log("Arguments:", arguments);
    console.log("Is array?", Array.isArray(arguments));  // false
    
    // Convert to array
    const argsArray = Array.from(arguments);
    console.log("Converted:", argsArray, Array.isArray(argsArray));
}
oldFunction(1, 2, 3);

// NodeList, HTMLCollection (in browsers)
// const divs = document.querySelectorAll('div');  // NodeList
// const divsArray = Array.from(divs);


// ============================================================================
// 12. PERFORMANCE CONSIDERATIONS
// ============================================================================

console.log("\n=== Performance Tips ===");

/**
 * PERFORMANCE TIPS:
 * 
 * 1. Use appropriate methods:
 *    - forEach: When you just need side effects
 *    - map: When transforming all elements
 *    - filter: When selecting subset
 *    - find: When searching (stops at first match)
 *    - some: When checking existence (stops at first match)
 * 
 * 2. Avoid:
 *    - Modifying array during iteration
 *    - Using delete (leaves holes)
 *    - Excessive array copying
 * 
 * 3. Prefer:
 *    - forEach over for...in for arrays
 *    - for...of for simple iteration
 *    - Traditional for loop for best performance
 * 
 * 4. Array vs Set:
 *    - Use Set for uniqueness and fast lookups
 *    - Use Array for ordered collections
 */

// Example: find vs filter
const largeArray = Array.from({ length: 1000000 }, (_, i) => i);

console.time("find");
const found2 = largeArray.find(x => x === 500000);
console.timeEnd("find");  // Stops at match

console.time("filter");
const filtered = largeArray.filter(x => x === 500000);
console.timeEnd("filter");  // Checks all elements


// ============================================================================
// 13. COMMON ARRAY PITFALLS
// ============================================================================

console.log("\n=== Common Pitfalls ===");

// 1. Arrays are reference types
const original2 = [1, 2, 3];
const reference = original2;
reference.push(4);
console.log("Original changed:", original2);  // [1, 2, 3, 4]

// 2. Shallow copy issue
const nested2 = [[1, 2], [3, 4]];
const shallowCopy = [...nested2];
shallowCopy[0].push(99);
console.log("Original nested changed:", nested2);  // [[1, 2, 99], [3, 4]]

// 3. sort() mutates and sorts as strings
const nums2 = [10, 2, 30, 1];
const sorted = nums2.sort();
console.log("Sorted wrong:", sorted);  // [1, 10, 2, 30]

// 4. Sparse arrays
const sparse = [1, , , 4];  // Has empty slots
console.log("Length:", sparse.length);  // 4
console.log("Element at 1:", sparse[1]);  // undefined

// 5. Array length is writable
const arr12 = [1, 2, 3];
arr12.length = 0;  // Clears array!
console.log("After length = 0:", arr12);


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Arrays are reference types (mutable)");
console.log("2. Many methods mutate (push, pop, splice, sort, reverse)");
console.log("3. Many methods don't mutate (map, filter, slice, concat)");
console.log("4. Use spread [...] for shallow copies");
console.log("5. Use proper comparator for sort()");
console.log("6. Choose right method for performance");
console.log("7. Be aware of shallow vs deep copying");
console.log("8. Use Array.isArray() to check for arrays");
console.log("=".repeat(80));
