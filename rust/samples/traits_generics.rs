//// Traits, define shared behavior through singatures
// Defining Traits
trait Drawable {
    fn draw(&self);  // Required method
    fn area(&self) -> f64;  // Another required method
}
// Traits can contain required methods and default methods

// Implementing Traits
struct Circle { radius: f64 }

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle with radius {}", self.radius);
    }
    
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
}
// Traits can only be implemented if the trait or the type is local (cannot add external trait to an external type)



//// Trait Bounds, specify the traits needed by the generic type
// Inline Bounds
fn process<T: Display + Clone>(item: T) -> String {
    format!("{}", item.clone())
}

// Where Clauses, cleaner and better readability
fn process<T, U>(item: T, extra: U) -> String
where
    T: Display + Clone,
    U: Debug + Default,
{
    format!("{} + {:?}", item.clone(), U::default())
}
// Also allow bounds on associated types
where
    T: Into<U>,
    U: Display,

/// Blanket Implementations
// Define a simple trait
trait Printable {
    fn print(&self);
}

// Blanket implementation for all types that implement Display
impl<T: std::fmt::Display> Printable for T {
    fn print(&self) {
        println!("{}", self);
    }
}

// Now any Display type gets Printable for free
fn main() {
    42.print();        // Works because i32 implements Display
    "hello".print();   // &str implements Display
    true.print();      // bool implements Display
}

// Often used in libraries
impl<T: ?Sized> From<T> for Arc<T> // ?Sized means it can be sized or unsized
where
    T: Clone,




//// Lifetime Bounds
// T must outlive 'a
struct Ref<'a, T: 'a> {
    data: &'a T,
}

// Higher-ranked trait bounds (for closures)
fn call_with_ref<F>(f: F)
where
    F: for<'a> Fn(&'a i32),  // Works for any lifetime 'a
{
    let value = 10;
    f(&value);
}



//// Default Trait Methods, provide a default implementation, which implementators can use or override
trait Logger {
    fn log(&self, message: &str);  // Required
    
    fn warn(&self, message: &str) {  // Default implementation
        self.log(&format!("WARNING: {}", message));
    }
    
    fn error(&self, message: &str) {
        self.log(&format!("ERROR: {}", message));
    }
}

struct ConsoleLogger;

impl Logger for ConsoleLogger {
    fn log(&self, message: &str) {
        println!("{}", message);
    }
    // Can override warn/error if needed
}

/// Calling Default from Override
impl Logger for Firewall {
    fn log(&self, msg: &str) {
        println!("Firewall:");
        Logger::log(self, msg);
    }
}



//// Associated Types vs Generics
/// Associated Types, implementator has one logical output type. Use when there is a single correct type per implementation
trait Iterator {
    type Item;  // Associated type
    
    fn next(&mut self) -> Option<Self::Item>;
}

impl Iterator for Counter {
    type Item = u32;  // Fixed for this implementation
    
    fn next(&mut self) -> Option<Self::Item> {
        // ...
    }
}

/// Generic Traits, when a type can implement the trait for multiple types
trait Container<T> {  // Type parameter
    fn contains(&self, item: &T) -> bool;
}

impl Container<i32> for Vec<i32> {
    fn contains(&self, item: &i32) -> bool {
        // ...
    }
}

impl Container<String> for Vec<String> {
    // Different implementation for different T
    fn contains(&self, item: &String) -> bool {
        // ...
    }
}



//// dyn Trait vs impl Trait (Dispatch Strategy and Abstraction)
/// Dispatch is how Rust decided which implementation will be called when a method is invoked

/// dyn Trait (Dynamic Dispatch), runtime dispatch, slight overheads, allows heterogeneity. Trait must be 'object safe'
/// A Trait os 'object safe' if all its methods use a receiver (take &self, &mut self, Box<Self>), do not return self, no generic methods
// Heap allocation, runtime polymorphism
let shapes: Vec<Box<dyn Drawable>> = vec![
    Box::new(Circle { radius: 5.0 }),
    Box::new(Square { side: 3.0 }),
];

// Function accepting any Drawable (dynamic dispatch)
fn draw_all(items: &[Box<dyn Drawable>]) {
    for item in items {
        item.draw();
    }
}

/// impl Trait (Static Dispatch/Inferred Type)
// Compile-time monomorphization, no heap allocation, compile-time dispatch, monomorphized, faster, Type is hidden but fixed
fn get_drawable() -> impl Drawable {
    Circle { radius: 5.0 }
}

// As parameter (simpler than generic + bounds)
fn draw(item: impl Drawable) {
    item.draw();
}
// Equivalent to:
fn draw<T: Drawable>(item: T) { ... }



//// Marker Traits, zero-sized traits with no methods, impose compile-time constraints
trait MyMarker {}

// Send and Sync are Marker Traits, and Copy and Sized
fn spawn<T: Send>(t: T) { /* ... */ }

#[derive(Copy, Clone)]
struct Flags(u8);

fn foo<T: Sized>(t: T) {}
fn bar<T: ?Sized>(t: &T) {}



//// Auto Traits, are implemented automatically if all fields satisfy them
// Auto traits are automatically implemented by the compiler
// based on the fields of a type

// The main auto traits:
// - Send
// - Sync  
// - Unpin
// - UnwindSafe
// - RefUnwindSafe

// Auto traits are automatically derived if all fields implement them
struct MyStruct {
    a: i32,
    b: String,
    c: Vec<u8>,
}
// MyStruct automatically gets Send, Sync, etc. because all fields have them

// Opting out of auto traits
struct NotSend {
    data: std::rc::Rc<i32>,  // Rc<i32> is !Send
}
// NotSend is !Send (not Send) because it contains !Send field

// Explicitly opting out (unstable)
#![feature(negative_impls)]
struct MyType {
    // ...
}

impl !Send for MyType {}    // Explicitly not Send
impl !Sync for MyType {}    // Explicitly not Sync

// Negative impls specify that a type DOES NOT implement a trait
// Currently unstable but important concept

#![feature(negative_impls)]

// Example from standard library (conceptual)
// impl<T: ?Sized> !Send for *const T {}
// impl<T: ?Sized> !Sync for *const T {}
// impl<T: ?Sized> !Send for *mut T {}
// impl<T: ?Sized> !Sync for *mut T {}

// Why negative impls matter: They help with coherence
trait SpecialTrait {}

// Without negative impls, this would be ambiguous
impl<T> SpecialTrait for T {}  // Blanket impl for all T

// But we want to exclude certain types
struct SpecialType;

// With negative impls:
impl !SpecialTrait for SpecialType {}  // SpecialType doesn't get the blanket impl

// This allows specialization-like behavior
fn process<T: SpecialTrait>(value: T) {
    // Uses blanket impl
}

fn process_special(value: SpecialType) {
    // Different handling for SpecialType
}