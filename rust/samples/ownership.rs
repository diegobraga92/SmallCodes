//// Ownership, things only have one owner at a time
// Prevents garbage colecting, dangling pointers, and double frees
fn main() {
    let s1 = String::from("hello");  // s1 owns the String
    let s2 = s1;                     // Ownership moves to s2
    // println!("{}", s1);           // ERROR: s1 no longer valid
} // s2 goes out of scope → String is dropped



//// Move vs Copy semantics
let v1 = vec![1, 2, 3];
let v2 = v1;        // Move: v1 is now invalid
// println!("{:?}", v1);  // ERROR,

// Copy happens for types that implement Copy (e.g., integers, floats, bool, char, tuples of Copy types)
let x = 5;
let y = x;          // Copy: both x and y are valid
println!("{} {}", x, y);  // OK
// Rule of thumb: Heap data → move. Small, fixed-size data → copy



//// Borrowing (&T, &mut T)
// Immutable Borrows (&T), allow multiple readers, no mutation allowed
let s = String::from("hello");
let r1 = &s;        // OK: immutable borrow
let r2 = &s;        // OK: another immutable borrow
// s.push_str(" world");  // ERROR: cannot mutate while borrowed

// Mutable Borrows (&mut T), only one at a time, cannot coexist with immutable borrows, can mutate value
let mut s = String::from("hello");
let r1 = &mut s;    // OK: mutable borrow
// let r2 = &mut s; // ERROR: second mutable borrow
// let r3 = &s;     // ERROR: immutable borrow during mutable borrow
// Either multiple immutable references OR one mutable reference, References must always be valid (dangling references prevented)



//// Lifetimes, how long references are valid
// 'Elision Rules' are used to infer lifetimes whem possible
fn foo(x: &i32)          // fn foo<'a>(x: &'a i32)
fn foo(x: &i32, y: &i32) // fn foo<'a, 'b>(x: &'a i32, y: &'b i32)

// If there is only one input lifetime, it's assigned to output
fn foo(x: &i32) -> &i32  // fn foo<'a>(x: &'a i32) -> &'a i32

// For methods with &self or &mut self, output lifetime matches self
impl SomeStruct {
    fn method(&self) -> &i32  // fn method<'a>(&'a self) -> &'a i32
}

// When Elision Rules do not apply, then Explicit Lifetimes are needed:
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}



//// Stack vs Heap
// Stack Allocation: Fast (just moves stack pointer), Fixed size, known at compile time, Automatic cleanup (pop off stack), Local variables, function arguments
let x = 5;           // Stack allocated
let y = [0u8; 1024]; // Stack allocated (fixed-size array)

// Heap Allocation: Slower (requires allocation), Dynamic size, unknown at compile time, Manual or RAII-based cleanup, Box<T>, Vec<T>, String, etc.
let boxed = Box::new(5);        // Heap allocated integer
let vector = vec![1, 2, 3];     // Heap allocated vector
let string = String::from("hi"); // Heap allocated string



//// Drop Trait, The Drop trait provides a destructor method called when a value goes out of scope:
struct Resource {
    name: String,
}

impl Drop for Resource {
    fn drop(&mut self) {
        println!("Dropping {}", self.name);
    }
}

fn main() {
    let res1 = Resource { name: String::from("Resource 1") };
    {
        let res2 = Resource { name: String::from("Resource 2") };
        // res2 dropped here, at end of inner scope
    }
    // res1 dropped here, at end of main
}
// Cannot be called manually, Drop order is Last In First Out (LIFO) within scope
// Fields are dropped after struct's drop method
let res = Resource { name: String::from("test") };
// res.drop();  // ERROR: explicit destructor calls not allowed
drop(res);      // OK: std::mem::drop takes ownership