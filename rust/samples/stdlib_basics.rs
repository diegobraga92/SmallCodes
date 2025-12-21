//// Core Collections: Vec<T>, String, HashMap<K, V>
// Vec<T> - Dynamic Array
// Creation
let mut vec1 = Vec::new();
let vec2 = vec![1, 2, 3];  // Macro
let vec3: Vec<i32> = Vec::with_capacity(10);

// Adding elements
vec1.push(10);
vec1.push(20);
vec1.extend([30, 40, 50]);  // Add multiple

// Accessing elements
let first = vec1[0];                // Panics if out of bounds
let first_safe = vec1.get(0);       // Returns Option<&i32>
let last = vec1.last();             // Option<&i32>

// Modifying
vec1[1] = 25;                       // Direct mutation
if let Some(elem) = vec1.get_mut(2) {
    *elem = 35;                     // Mutable reference
}

// Removing
let popped = vec1.pop();            // Option<i32>
vec1.remove(1);                     // Remove at index
vec1.retain(|&x| x > 20);           // Keep only matching elements
vec1.clear();                       // Remove all

// Common operations
let len = vec1.len();
let capacity = vec1.capacity();
vec1.shrink_to_fit();               // Reduce capacity to size
vec1.sort();                        // Sort in-place
vec1.sort_unstable();               // Faster but unstable

// Slicing
let slice: &[i32] = &vec1[1..3];    // Get a slice

// Iteration
for element in &vec1 { /* ... */ }
for (i, element) in vec1.iter().enumerate() { /* ... */ }


// String, String: Heap-allocated, growable, owned. Use when need to modify or own
// &str: String slice, borrowed, view into String or string literal. Use when don't need ownership (like a view)
// Creation
let mut s1 = String::new();
let s2 = "initial".to_string();
let s3 = String::from("hello");
let s4 = format!("Hello, {}!", "world");  // Using format! macro

// Appending
s1.push('H');                       // Add character
s1.push_str("ello");                // Add string slice
s1 += " World!";                    // Append using +=
s1.extend(['!', '!', '!']);         // Add multiple chars

// Concatenation
let s5 = s1 + &s2;                  // Note: s1 is consumed!
let s6 = format!("{}{}", s2, s3);   // Better: doesn't consume
let s7 = s2.clone() + &s3;          // Clone if needed

// Accessing characters
// Strings are UTF-8, so indexing by bytes is unsafe
let first_char = s1.chars().next(); // Option<char>
let chars: Vec<char> = s1.chars().collect();

// Slicing (must be at char boundaries!)
let hello = &s1[0..5];              // "Hello"
// let bad = &s1[0..3];             // PANIC! Invalid char boundary

// Common operations
let len = s1.len();                 // Bytes, not chars!
let char_count = s1.chars().count(); // Actual character count
let is_empty = s1.is_empty();
s1.trim();                          // Returns &str, doesn't modify
let trimmed = s1.trim().to_string(); // Get new String

// Searching
let contains = s1.contains("ell");  // bool
let starts = s1.starts_with("He");
let ends = s1.ends_with('!');
let index = s1.find("lo");          // Option<usize>

// Replacing
let replaced = s1.replace("Hello", "Hi");
let no_spaces = s1.replace(" ", "");

// Splitting
let words: Vec<&str> = "hello world rust".split(' ').collect();
let lines: Vec<&str> = "line1\nline2\nline3".lines().collect();

// Case conversion
let upper = s1.to_uppercase();      // New String
let lower = s1.to_lowercase();      // New String


// HashMap<K, V> - Key-Value Store
use std::collections::HashMap;

// Creation
let mut map1 = HashMap::new();
let map2: HashMap<String, i32> = HashMap::with_capacity(10);

// Insertion
map1.insert("key1".to_string(), 100);
map1.insert("key2".to_string(), 200);
map1.insert("key3".to_string(), 300);

// Access
let value = map1.get("key1");               // Option<&i32>
let value_mut = map1.get_mut("key2");       // Option<&mut i32>
let value_or = map1.get("key4").unwrap_or(&0); // Default value

// Check existence
let has_key = map1.contains_key("key1");    // bool

// Updating
map1.insert("key1".to_string(), 150);       // Overwrites
map1.entry("key4".to_string())
    .or_insert(400);                        // Insert if absent
map1.entry("key5".to_string())
    .and_modify(|v| *v += 10)               // Modify if exists
    .or_insert(500);                        // Insert if doesn't

// Remove
let removed = map1.remove("key1");          // Option<i32>
let removed_entry = map1.remove_entry("key2"); // Option<(String, i32)>

// Iteration
for (key, value) in &map1 {
    println!("{}: {}", key, value);
}

for key in map1.keys() { /* ... */ }
for value in map1.values() { /* ... */ }
for value in map1.values_mut() {
    *value *= 2;                            // Modify in-place
}

// Conversion from vector of tuples
let vec = vec![("a", 1), ("b", 2), ("c", 3)];
let map3: HashMap<_, _> = vec.into_iter().collect();

// Hash requirements: Keys must implement Eq and Hash traits
// Use custom types as keys by deriving/implementing these traits
#[derive(Debug, Hash, Eq, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

let mut point_map = HashMap::new();
point_map.insert(Point { x: 1, y: 2 }, "origin");



//// Iterators: map, filter, collect. 
/// Iterators are lazy (nothing happens until consumed with for, collect, next, etc) and zero-cost (no overhead compared to hand-written lllop)

// Basics
// All collections are iterable
let vec = vec![1, 2, 3, 4, 5];

// Three types of iterators:
let iter = vec.iter();           // Borrows elements: Iterator<Item = &T>
let iter_mut = vec.iter_mut();   // Mutable borrow: Iterator<Item = &mut T>
let into_iter = vec.into_iter(); // Consumes: Iterator<Item = T> (moves)

// Common adapter methods (return new iterators)
let doubled: Vec<i32> = vec.iter()
    .map(|&x| x * 2)              // Transform each element
    .collect();

let evens: Vec<&i32> = vec.iter()
    .filter(|&&x| x % 2 == 0)     // Keep only matching elements
    .collect();

// Chaining multiple adapters
let result: Vec<i32> = vec.iter()
    .filter(|&&x| x > 2)          // Keep > 2
    .map(|&x| x * 3)              // Multiply by 3
    .filter(|&x| x < 20)          // Keep < 20
    .collect();                   // [9, 12, 15]

// Common methods
.map(|x| x * 2)                    // Transform
.map(|(i, x)| (i, x * 2))          // With index (from enumerate)
.flat_map(|x| x.iter())            // Flatten nested iterators
.flatten()                         // Same, specialized

.filter(|x| x > 5)                 // Keep if true
.filter_map(|x| {                  // Filter and map simultaneously
    if x > 0 { Some(x * 2) } else { None }
})
.skip(3)                           // Skip first n elements
.take(5)                           // Take only n elements
.skip_while(|x| *x < 10)           // Skip while condition true
.take_while(|x| *x < 20)           // Take while condition true

.collect()                         // Collect into collection
.collect::<Vec<_>>()               // Specify type explicitly
.count()                           // Count elements
.sum()                             // Sum elements (requires Numeric)
.product()                         // Product of elements
.min() / .max()                    // Min/max (requires Ord)
.find(|&x| x == 5)                 // Find first matching element
.position(|x| *x == 5)             // Find position of element
.any(|x| x > 10)                   // True if any element matches
.all(|x| x < 10)                   // True if all elements match
.nth(3)                            // Get nth element
.last()                            // Get last element
.fold(0, |acc, x| acc + x)        // Accumulate result
.reduce(|acc, x| acc + x)         // Fold without initial value
.for_each(|x| println!("{}", x))  // Execute for each



//// for loops vs Iterators
// for, better for mutability, better for breaks or continues
let vec = vec![1, 2, 3, 4, 5];

// Basic loop
for element in &vec {
    println!("{}", element);
}

// With index
for (i, element) in vec.iter().enumerate() {
    println!("Index {}: {}", i, element);
}

// Range-based
for i in 0..10 {
    println!("{}", i);
}

// Over HashMap
let mut map = HashMap::new();
map.insert("a", 1);
map.insert("b", 2);

for (key, value) in &map {
    println!("{}: {}", key, value);
}

// Mutating elements
let mut numbers = vec![1, 2, 3];
for num in &mut numbers {
    *num *= 2;  // Double each element
}


// Iterator Style, best for data transformations, no performance penalty, lazy until consumed
let vec = vec![1, 2, 3, 4, 5];

// Equivalent operations
let mut sum = 0;
for &num in &vec {
    if num % 2 == 0 {
        sum += num * 2;
    }
}

// VS iterator chain
let sum: i32 = vec.iter()
    .filter(|&&x| x % 2 == 0)
    .map(|&x| x * 2)
    .sum();



//// println! and Formatting Macros
// println! and print!
// Basic printing
println!("Hello, world!");          // With newline
print!("Hello, ");                  // Without newline
println!("World!");

// Positional arguments
println!("{0}, {1}, {0}", "Alice", "Bob");  // "Alice, Bob, Alice"

// Named arguments
println!("{name} is {age} years old", 
         name = "Alice", 
         age = 30);

// Formatting specifiers
let x = 42;
println!("Decimal: {}", x);         // 42
println!("Hex: {:x}", x);           // 2a
println!("Hex: {:X}", x);           // 2A
println!("Octal: {:o}", x);         // 52
println!("Binary: {:b}", x);        // 101010
println!("Debug: {:?}", x);         // 42 (debug format)

// Width and alignment
println!("Right align: {:>10}", x);     // "        42"
println!("Left align: {:<10}", x);      // "42        "
println!("Center: {:^10}", x);          // "    42    "
println!("Zero pad: {:010}", x);        // "0000000042"

// Precision for floats
let pi = 3.1415926535;
println!("{:.2}", pi);                 // 3.14
println!("{:.5}", pi);                 // 3.14159
println!("{:10.2}", pi);               // "      3.14"

// Scientific notation
println!("{:e}", 1000.0);              // 1e3
println!("{:E}", 1000.0);              // 1E3


// format!
// Creates a String instead of printing
let s = format!("Hello, {}!", "world");
let name = "Alice";
let age = 30;
let message = format!("{name} is {age} years old");

// Complex formatting
let table = format!("{:<10} {:>10} {:>10}", "Name", "Age", "Score");
let row1 = format!("{:<10} {:>10} {:>10.2}", "Alice", 30, 95.5);

// Reuse format specifiers
let template = "{:>10}";
let formatted = format!(template, 42);  // "        42"


// eprintln1 and eprint!
// Print to stderr (for errors)
eprintln!("Error: File not found!");
eprint!("Warning: ");
eprintln!("Disk space low");


// Debug formatting {:?} and {:#?}
#[derive(Debug)]
struct Person {
    name: String,
    age: u8,
}

let alice = Person {
    name: "Alice".to_string(),
    age: 30,
};

println!("Debug: {:?}", alice);  
// Output: Debug: Person { name: "Alice", age: 30 }

println!("Pretty: {:#?}", alice);
// Output:
// Pretty: Person {
//     name: "Alice",
//     age: 30,
// }


// Custom Formatting with Display and Debug traits
use std::fmt;

struct Point {
    x: i32,
    y: i32,
}

// Implement Display for user-friendly output
impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// Debug can be derived
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

let p = Point { x: 5, y: 10 };
let r = Rectangle { width: 30, height: 50 };

println!("Point: {}", p);        // Uses Display: "Point: (5, 10)"
println!("Rect: {:?}", r);       // Uses Debug: "Rect: Rectangle { width: 30, height: 50 }"


// Advanced Formatting
// Sign display
println!("Always show sign: {:+}", 42);    // "+42"
println!("Always show sign: {:+}", -42);   // "-42"

// Different bases with prefix
println!("With prefix: {:#x}", 42);        // "0x2a"
println!("With prefix: {:#X}", 42);        // "0x2A"
println!("With prefix: {:#b}", 42);        // "0b101010"
println!("With prefix: {:#o}", 42);        // "0o52"

// Thousands separator
use separator::Separatable;
println!("{}", 1000000.separated_string());  // "1,000,000" (with separator crate)

// Padding with custom characters
println!("{:*>10}", "hi");      // "********hi"
println!("{:*<10}", "hi");      // "hi********"
println!("{:*^10}", "hi");      // "****hi****"

// Combining formatting
let value = 1234.5678;
println!("{:>15.2}", value);    // "        1234.57"
println!("{:<15.2}", value);    // "1234.57        "