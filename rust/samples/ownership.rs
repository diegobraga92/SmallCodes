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
// Copy: Should be implemented for types that are: Small, Cheap to copy, Don't own heap data. Don't need custom cleanup (Drop trait)


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
// Struct with lifetime parameter
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn new(text: &'a str) -> Self {
        let first_sentence = text.split('.').next().unwrap();
        Excerpt { part: first_sentence }
    }
    
    fn get_part(&self) -> &str {
        self.part
    }
}
// Static Lifetime ('static)
// 'static lives for entire program duration
let s: &'static str = "I live forever";
static NUM: i32 = 42;  // Static variable

// Functions can return 'static
fn get_static() -> &'static str {
    "hello"
}

// But be careful - not everything is static
fn not_static(s: String) -> &'static str {
    // &s  // ERROR: s doesn't live long enough
    Box::leak(s.into_boxed_str())  // Dangerous!
}



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



//// Lifetime Variance and Subtyping, when a lifetime can be substituted by another
/// Four Variance Types:
/// Covariant ('long can be used where 'short is expected): &'a T or Box<T>
/// Contravariant ('short can be used where 'long is expected): fn(T)
/// Invariant (exact match required): &'a mut T
/// Bivariant (any lifetime works) - rare in Rust
// &'a T is covariant over 'a and T
fn covariant_example<'long: 'short, 'short>() {
    let long: &'long str = "hello";
    let short: &'short str = long;  // OK: covariance
    
    // &'a mut T is covariant over 'a but invariant over T
    let mut x = 5;
    let long_mut: &'long mut i32 = &mut x;
    // let short_mut: &'short mut i32 = long_mut;  // Would be OK for 'a
}

// Function pointers have complex variance
type FnPtr = fn(&str) -> &str;

// Subtyping, a 'bigger' lifetime type can be used where a shorter is expected: &'long T  →  &'short T  (allowed)
// 'long is a subtype of 'short when 'long: 'short (lives at least as long)
fn subtyping<'long: 'short, 'short>(long: &'long str) -> &'short str {
    long  // OK: can use longer lifetime where shorter is expected
}

struct Container<'a> {
    data: &'a str,
}

fn use_container<'long: 'short, 'short>(
    long: Container<'long>
) -> Container<'short> {
    // Container<'long> is a subtype of Container<'short>
    long
}
