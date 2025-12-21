//// let & mut:
// Immutable by default
let x = 5;
// x = 6; // Error: cannot assign twice to immutable variable

// Mutable with `mut`
let mut y = 10;
y = 20; // Allowed



//// Shadowing:
// Re-declaring a variable with the same name, creating a new binding, can change type
// Often used for transformations (e.g. parsing input), avoiding mut usage, so the compiler can do further improvements, and prevents unwanted changes
// In Rust, values are moved by default, so shadowing does not cause new memory to be allocated (no heap allocation), and does not create copies
let x = 5;
let x = x + 1; // Shadowing creates a new variable
{
    let x = x * 2; // Can shadow in a new scope
    println!("Inner scope x: {}", x); // 12
}
println!("Outer scope x: {}", x); // 6
// Type can change with shadowing
let spaces = "   ";
let spaces = spaces.len(); // String → usize allowed



//// Primitive Types
// Signed integers from i8 to i128, also isize
let a: i32 = -10;
// Unsigned integers, from u8 to u128, also usize
let b: u64 = 42;
// Sizes are useful for len() and indices, since they depend on the architecture, being 32 or 64bits accordingly

// Floating-Point can be f32 or f64
let pi: f64 = 3.1415; // default float type

let is_active: bool = true;

// Char is not the same as String or &str, uses Unicode, up to 4 bytes
let c: char = '🚀'; 



//// Tuples, Arrays, Slices
// Tuples are fixed-size and can have multiple types
let tuple: (i32, f64, char) = (42, 3.14, 'A');
let (x, y, z) = tuple; // Destructuring
let first = tuple.0; // Access by index
let unit = (); // Zero-length tuple (unit type)

// Arrays are fixed size, and same type
let arr: [i32; 5] = [1, 2, 3, 4, 5]; // Fixed size
let same_values = [0; 5]; // [0, 0, 0, 0, 0]
let first = arr[0];
// arr[5] = 6; // Compile-time error: index out of bounds

// Slices are a view into a sequence (borrowed)
let arr = [1, 2, 3, 4, 5];
let slice: &[i32] = &arr[1..4]; // [2, 3, 4]
let full_slice: &[i32] = &arr[..]; // All elements

// String slices
let s = String::from("hello world");
let hello = &s[0..5];
let world = &s[6..11];
// Vec<T> → growable, [T; N] → fixed, &[T] → borrowed view


//// Structs
// Classic
struct User {
    username: String,
    email: String,
    active: bool,
}

let user = User {
    email: String::from("test@example.com"),
    username: String::from("john"),
    active: true,
};

println!("Email: {}", user.email);

// Tuple
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);
let red = black.0; // Access by index

// Unit
struct Marker;
let marker = Marker; // No data, useful for traits/generics

// Update Syntax, create new struct by reusing most fields from an existing instance. The fields that do not implement Copy are moved, not copied
let user2 = User {
    name: "Alice".into(),
    ..user1 // This line basically says "Take all remaining fields from user1". Always come last
};


//// Enums and match
// Basic Enum
enum IpAddrKind {
    V4,
    V6,
}

enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);
let loopback = IpAddr::V6(String::from("::1"));

// match expression
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}

// Match with patterns, must has to be exhaustive if applicable
match some_value {
    1 => println!("one"),
    2 | 3 => println!("two or three"),
    4..=10 => println!("four through ten"),
    _ => println!("something else"), // Default case
}

struct Point {
    x: i32,
    y: i32,
}

let p = Point { x: 0, y: 7 };

match p {
    Point { x, y: 0 } => println!("On the x-axis at {}", x),
    Point { x: 0, y } => println!("On the y-axis at {}", y),
    Point { x, y } => println!("On neither axis: ({}, {})", x, y),
}



//// Pattern Matching
// Destructuring
// Destructuring tuples
let (x, y, z) = (1, 2, 3);

// Destructuring arrays
let arr = [1, 2, 3];
let [a, b, c] = arr;

// Matching ranges
let num = 5;
match num {
    1..=5 => println!("One through five"),
    _ => println!("Other"),
}

// Multiple patterns
match num {
    1 | 2 => println!("One or two"),
    _ => println!("Other"),
}

// Match guards
match num {
    x if x < 5 => println!("Less than five"),
    x if x == 5 => println!("Exactly five"),
    _ => println!("Greater than five"),
}

// @ Bindings. It tests against a pattern, and if it passes, binds the value to a variable
enum Message {
    Hello { id: i32 },
}

let msg = Message::Hello { id: 5 };

match msg {
    Message::Hello { id: id_variable @ 3..=7 } => { // Since value is between 3 and 7, id_variable receives it
        println!("Found an id in range: {}", id_variable)
    }
    Message::Hello { id: 10..=12 } => {
        println!("Found an id in another range")
    }
    Message::Hello { id } => {
        println!("Found some other id: {}", id)
    }
}



//// if let, while let
// if let, matches against a single pattern
let some_value = Some(3);

// Verbose match for one case
match some_value {
    Some(3) => println!("three"),
    _ => (),
}

// Equivalent with if let
if let Some(3) = some_value {
    println!("three");
}

// With else
if let Some(x) = some_value {
    println!("Got value: {}", x);
} else {
    println!("No value");
}

// while let, loop while pattern matches
let mut stack = Vec::new();
stack.push(1);
stack.push(2);
stack.push(3);

// Pop until empty
while let Some(top) = stack.pop() {
    println!("{}", top);
}

// Parsing a stream
let mut values = vec![Some(1), Some(2), None, Some(3)].into_iter();
while let Some(Some(value)) = values.next() {
    println!("Processing: {}", value);
}
