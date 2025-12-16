//// Stack vs Heap
// Stack Allocation: Fast (just moves stack pointer), Fixed size, known at compile time, Automatic cleanup (pop off stack), Local variables, function arguments
let x = 5;           // Stack allocated
let y = [0u8; 1024]; // Stack allocated (fixed-size array)

// Heap Allocation: Slower (requires allocation), Dynamic size, unknown at compile time, Manual or RAII-based cleanup, Box<T>, Vec<T>, String, etc.
let boxed = Box::new(5);        // Heap allocated integer
let vector = vec![1, 2, 3];     // Heap allocated vector
let string = String::from("hi"); // Heap allocated string



//// Smart Pointers, Box<T>, Rc<T>, Arc<T>, RefCell<T>, Mutex<T>, RwLock<T>
// Box<T>, Single Ownership Heap Allocation, for large data. Trait: Box<dyn Trait>
// Basic usage
let boxed = Box::new(42);           // Allocate i32 on heap
println!("{}", *boxed);             // Dereference with *

// Recursive types need Box
enum List {
    Cons(i32, Box<List>),           // Fixed size because Box is pointer-sized
    Nil,
}

let list = List::Cons(1, Box::new(List::Cons(2, Box::new(List::Nil))));

// Returning large structs efficiently
fn create_large_struct() -> Box<LargeStruct> {
    Box::new(LargeStruct::new())    // Returns pointer, not whole struct
}

// Dynamically sized types (DSTs)
let boxed_slice: Box<[i32]> = Box::new([1, 2, 3, 4, 5]);
let boxed_trait: Box<dyn std::fmt::Display> = Box::new(42);

// When to use Box:
// 1. Recursive data structures
// 2. Trait objects (dyn Trait)
// 3. Large data you want to move efficiently
// 4. When you need exact heap allocation control


// Rc<T>, Reference Counted Smart Pointer, shared ownership, single-thread only, ref counting
use std::rc::Rc;

// Multiple immutable references to same data
let rc1 = Rc::new("shared data".to_string());
let rc2 = Rc::clone(&rc1);           // Clones the pointer, not data
let rc3 = Rc::clone(&rc1);

println!("Count: {}", Rc::strong_count(&rc1));  // 3

// Access data
println!("Data: {}", *rc1);         // Dereference
println!("Data: {}", rc1.as_str()); // Method access

// Rc is NOT thread-safe!
// let rc_across_threads = rc1.clone();
// std::thread::spawn(move || { println!("{}", rc_across_threads); }); // ERROR

// Weak references to break cycles
let rc = Rc::new("data".to_string());
let weak = Rc::downgrade(&rc);      // Creates Weak<T>

if let Some(strong) = weak.upgrade() {
    println!("Still alive: {}", strong);
}

// When to use Rc:
// 1. Shared ownership in single-threaded contexts
// 2. Graph-like data structures
// 3. When you need multiple owners but only immutable access


// Arc<T>, Atomic Reference Counting, Thread-Safe, slower than Rc
use std::sync::Arc;
use std::thread;

// Thread-safe reference counting
let arc1 = Arc::new("shared across threads".to_string());
let arc2 = Arc::clone(&arc1);

let handle = thread::spawn(move || {
    println!("Thread sees: {}", arc2);
});

handle.join().unwrap();
println!("Main thread: {}", arc1);

// Arc has atomic operations (slower than Rc)
let arc = Arc::new(42);
println!("Count: {}", Arc::strong_count(&arc));

// Arc with Mutex for shared mutable data
use std::sync::Mutex;
let shared_data = Arc::new(Mutex::new(vec![1, 2, 3]));

let handles: Vec<_> = (0..3).map(|i| {
    let data = Arc::clone(&shared_data);
    thread::spawn(move || {
        let mut vec = data.lock().unwrap();
        vec.push(i);
    })
}).collect();

for handle in handles {
    handle.join().unwrap();
}

println!("Final: {:?}", shared_data.lock().unwrap());

// When to use Arc:
// 1. Shared ownership across threads
// 2. Read-only data shared by multiple threads
// 3. Combined with Mutex/RwLock for mutable shared data


// RefCell<T>, Interior Mutability for Single Thread, enforces borrow rules at runtime, panics on violation
use std::cell::RefCell;

// Borrow checking at runtime instead of compile time
let cell = RefCell::new(42);

// Immutable borrow
let read1 = cell.borrow();          // Returns Ref<T>
let read2 = cell.borrow();          // Multiple immutable borrows OK
println!("{}, {}", *read1, *read2);

// Mutable borrow
{
    let mut write = cell.borrow_mut();  // Returns RefMut<T>
    *write += 10;
} // write goes out of scope here

// Now we can borrow again
println!("After: {}", *cell.borrow());

// Runtime panic if rules violated
let cell = RefCell::new(42);
let read = cell.borrow();
// let mut write = cell.borrow_mut();  // PANIC at runtime: already borrowed

// Common pattern: Rc + RefCell for shared mutable data
use std::rc::Rc;
let shared_mut = Rc::new(RefCell::new(vec![1, 2, 3]));

let clone1 = Rc::clone(&shared_mut);
clone1.borrow_mut().push(4);

let clone2 = Rc::clone(&shared_mut);
clone2.borrow_mut().push(5);

println!("{:?}", shared_mut.borrow());  // [1, 2, 3, 4, 5]

// When to use RefCell:
// 1. Interior mutability patterns
// 2. Mocking/testing (mocking immutable interfaces)
// 3. Graph nodes that need to reference each other
// 4. Single-threaded scenarios only


// Mutex<T>, Mutual Exclusion for Threads, thread-safe, blocks on contention
use std::sync::Mutex;
use std::thread;

// Thread-safe interior mutability
let counter = Mutex::new(0);

let mut handles = vec![];

for _ in 0..10 {
    let counter = Mutex::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();  // Returns MutexGuard
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());  // 10

// Poisoning: If a thread panics while holding lock
let mutex = Mutex::new(42);

let result = std::panic::catch_unwind(|| {
    let mut data = mutex.lock().unwrap();
    *data = 100;
    panic!("Oops!");
});

if result.is_err() {
    // Mutex is poisoned
    match mutex.lock() {
        Ok(guard) => println!("Not poisoned: {}", *guard),
        Err(poisoned) => {
            let guard = poisoned.into_inner();
            println!("Recovered from poison: {}", *guard);
        }
    }
}

// When to use Mutex:
// 1. Shared mutable state across threads
// 2. When you need exclusive write access
// 3. Simpler than RwLock but less concurrent


// RwLock<T>, Read-Write Lock, Multiple reader OR one writer, better for heavy IO
use std::sync::Mutex;
use std::thread;

// Thread-safe interior mutability
let counter = Mutex::new(0);

let mut handles = vec![];

for _ in 0..10 {
    let counter = Mutex::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();  // Returns MutexGuard
        *num += 1;
    });
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("Result: {}", *counter.lock().unwrap());  // 10

// Poisoning: If a thread panics while holding lock
let mutex = Mutex::new(42);

let result = std::panic::catch_unwind(|| {
    let mut data = mutex.lock().unwrap();
    *data = 100;
    panic!("Oops!");
});

if result.is_err() {
    // Mutex is poisoned
    match mutex.lock() {
        Ok(guard) => println!("Not poisoned: {}", *guard),
        Err(poisoned) => {
            let guard = poisoned.into_inner();
            println!("Recovered from poison: {}", *guard);
        }
    }
}

// When to use Mutex:
// 1. Shared mutable state across threads
// 2. When you need exclusive write access
// 3. Simpler than RwLock but less concurrent



//// Exterior and Interior Mutability
// Exterior (Default), mutation requires &mut T
// Mutability is part of the reference type
let mut x = 42;                // Variable is mutable
let y = &mut x;                // Mutable reference
*y += 1;

// Functions declare mutability in signature
fn modify_exterior(value: &mut i32) {
    *value += 10;
}

// Compile-time checking
let mut data = vec![1, 2, 3];
let ref1 = &data;              // Immutable borrow
// let ref2 = &mut data;       // ERROR: cannot borrow as mutable


// Interior, mutation through &T
use std::cell::RefCell;

// Mutability is part of the data, not the reference
let cell = RefCell::new(42);   // Cell itself is immutable
let borrowed = cell.borrow();  // Can borrow mutably from immutable cell
let mut borrowed_mut = cell.borrow_mut();
*borrowed_mut += 1;

// Common patterns:

// 1. Mutable data behind shared reference
struct Cache {
    data: RefCell<HashMap<String, String>>,
}

impl Cache {
    fn get(&self, key: &str) -> Option<String> {
        self.data.borrow().get(key).cloned()
    }
    
    fn insert(&self, key: String, value: String) {
        self.data.borrow_mut().insert(key, value);
    }
}

// 2. Mock objects
trait Database {
    fn query(&self, sql: &str) -> Vec<String>;
}

struct MockDb {
    calls: RefCell<Vec<String>>,
    responses: RefCell<Vec<Vec<String>>>,
}

impl Database for MockDb {
    fn query(&self, sql: &str) -> Vec<String> {
        self.calls.borrow_mut().push(sql.to_string());
        self.responses.borrow_mut().pop().unwrap_or_default()
    }
}

// 3. Graph structures
struct Node {
    value: i32,
    neighbors: RefCell<Vec<Rc<Node>>>,  // Need RefCell to modify neighbors
}

// When to use interior mutability:
// 1. Implementation details shouldn't affect API
// 2. Mocking immutable traits
// 3. Graph/cyclic structures
// 4. Caching/lazy initialization



//// Smart Pointer Traits (Deref, Drop)
/// Deref, allow smart pointers to behave like references, enable 'deref coercion', which automatically converts the ref to a compatible type
use std::ops::Deref;

// Implementing Deref for custom smart pointer
struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> Self {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;
    
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Usage
let x = 5;
let y = MyBox::new(x);

assert_eq!(5, *y);           // * uses Deref::deref
assert_eq!(5, *(y.deref())); // Equivalent

// Deref coercion - automatic conversion
fn hello(name: &str) {
    println!("Hello, {}!", name);
}

let m = MyBox::new(String::from("Rust"));
hello(&m);  // Works because:
// &MyBox<String> -> &String (via Deref)
// &String -> &str (via String's Deref)

// Multiple levels of Deref coercion
let m = MyBox::new(MyBox::new(String::from("Nested")));
hello(&m);  // &MyBox<MyBox<String>> -> &MyBox<String> -> &String -> &str

// When to implement Deref:
// 1. Smart pointers
// 2. Newtype patterns
// 3. Wrapper types



/// Drop, custom destructor
impl Drop for MyBox {
    fn drop(&mut self) {
        println!("Dropping!");
    }
}



//// Cell<T> for Copy Types, implements Interior mutability for Copy types, no borrowing or references
use std::cell::Cell;

// Cell provides interior mutability for Copy types
let cell = Cell::new(42);

// Get value (copies because T must implement Copy)
let value = cell.get();       // Returns T, not &T
println!("Value: {}", value);

// Set value
cell.set(100);                // No borrowing required!
println!("New value: {}", cell.get());

// Multiple cells can be modified
let x = Cell::new(1);
let y = Cell::new(2);

x.set(x.get() + y.get());     // Read both, write x
println!("x = {}, y = {}", x.get(), y.get());

// No runtime borrowing checks needed
// Because get() returns a copy, not a reference