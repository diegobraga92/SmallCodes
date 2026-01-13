//// Unsafe
/// unsafe allows running operations that the compiler cannot verify as safe. When it's OK to use unsafe
/// Interfacing with hardware, OS or C Libraries
/// Implementing low-level data structures
/// Implementing safe abstractions
let x = 5;
let raw = &x as *const i32;
let value = unsafe { *raw }; // Valid: raw points to valid i32


unsafe fn dangerous() { /* ... */ }

// Caller must ensure preconditions
unsafe { dangerous(); }


/// Raw Pointers and FFI (Foreign Function Interface), allows Rust to call code from other languages, mostly C
// Creating from references (safe)
let x = 10;
let ptr: *const i32 = &x;
let mut_ptr: *mut i32 = &mut 10 as *mut i32;

// Working with FFI
extern "C" {
    fn c_function(ptr: *const i8);
}

let ptr: *const i32 = &x;
unsafe {
    println!("{}", *ptr);
}



//// Undefined Behavior (UB)
/// Avoid at all costs, worse than panics
/// Data races, Dereferencing invalid/null/dangling pointers, Breaking type invariants (e.g., creating invalid bool)



//// Writing Safe Abstractions Over Unsafe Code
/// unsafe code is private, public API is safe, invariants are enforced at construction time
pub struct SafeWrapper {
    raw: *mut libc::c_void,
}

impl SafeWrapper {
    pub fn new() -> Result<Self, Error> {
        let raw = unsafe { libc::malloc(100) };
        if raw.is_null() {
            return Err(Error::AllocationFailed);
        }
        Ok(Self { raw })
    }
    
    // Safe method that uses unsafe internally
    pub fn write_data(&mut self, data: &[u8]) {
        unsafe {
            std::ptr::copy_nonoverlapping(
                data.as_ptr(),
                self.raw as *mut u8,
                data.len()
            );
        }
    }
}

impl Drop for SafeWrapper {
    fn drop(&mut self) {
        unsafe { libc::free(self.raw) };
    }
}



//// Invariants and Safety Contracts, every unsafe block relies on assumed invariants
/// Type invariants: Properties that must hold for all values of a type
/// Safety invariants: Properties that must hold to use unsafe safely
/// Validity invariants: Properties required for a value to exist at all

/// Safety Contracts are a documentation

/// # Safety
/// - `ptr` must be non-null
/// - `ptr` must point to a valid `T` for its entire lifetime
/// - `ptr` must not be aliased by other mutable references
unsafe fn process<T>(ptr: *mut T) { /* ... */ }

unsafe fn get_unchecked(v: &[i32], i: usize) -> &i32 {
    // SAFETY: caller guarantees i < v.len()
    v.get_unchecked(i)
}



//// Send and Sync Invariants, implementing those manually requires 'unsafe'
/// Send: Type can be transferred across thread boundaries
/// Sync: Type can be shared between threads (&T is Send)
struct MyPtr(*mut i32);

// SAFETY: We ensure exclusive access through synchronization
unsafe impl Send for MyPtr {}
unsafe impl Sync for MyPtr {}



//// Foreign Function Interface (FFI) Patterns, ffi functions are unsafe by default
/// Safe Abstraction over C APIs:
mod ffi {
    extern "C" {
        pub fn c_create() -> *mut c_void;
        pub fn c_use(ptr: *mut c_void) -> i32;
        pub fn c_destroy(ptr: *mut c_void);
    }
}

pub struct ForeignResource {
    ptr: *mut std::ffi::c_void,
}

impl ForeignResource {
    pub fn new() -> Result<Self, Error> {
        let ptr = unsafe { ffi::c_create() };
        if ptr.is_null() {
            Err(Error::CreationFailed)
        } else {
            Ok(Self { ptr })
        }
    }
    
    pub fn use_resource(&self) -> i32 {
        unsafe { ffi::c_use(self.ptr) }
    }
}

impl Drop for ForeignResource {
    fn drop(&mut self) {
        unsafe { ffi::c_destroy(self.ptr) };
    }
}



//// std::mem Operations
/// transmute - Extreme caution required
// SAFETY: Must ensure size and alignment match
let bytes: [u8; 4] = [0x12, 0x34, 0x56, 0x78];
let value: u32 = unsafe { std::mem::transmute(bytes) };

/// zeroes and uninitialized
// zeroed - creates zeroed memory (all bits 0)
// SAFETY: Zero must be valid for the type
let x: i32 = unsafe { std::mem::zeroed() };

// MaybeUninit - preferred over mem::uninitialized
use std::mem::MaybeUninit;
let mut x = MaybeUninit::<i32>::uninit();
unsafe { x.as_mut_ptr().write(42) };
let x = unsafe { x.assume_init() };



//// Custom Smart Pointers
use std::ops::{Deref, DerefMut};
use std::ptr::NonNull;

pub struct MyBox<T> {
    ptr: NonNull<T>,  // Non-null raw pointer
    _marker: std::marker::PhantomData<T>,  // For drop check
}

impl<T> MyBox<T> {
    pub fn new(value: T) -> Self {
        // Allocate on heap
        let boxed = Box::new(value);
        
        // Convert to raw pointer then NonNull
        let ptr = Box::into_raw(boxed);
        
        // SAFETY: Box::into_raw never returns null
        Self {
            ptr: unsafe { NonNull::new_unchecked(ptr) },
            _marker: std::marker::PhantomData,
        }
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;
    
    fn deref(&self) -> &Self::Target {
        // SAFETY: ptr is valid, non-null, and properly aligned
        unsafe { self.ptr.as_ref() }
    }
}

impl<T> DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        // SAFETY: ptr is valid, non-null, and properly aligned
        unsafe { self.ptr.as_mut() }
    }
}

impl<T> Drop for MyBox<T> {
    fn drop(&mut self) {
        // Reconstruct Box to run destructor
        // SAFETY: ptr came from Box, hasn't been used since
        unsafe {
            let _ = Box::from_raw(self.ptr.as_ptr());
        }
    }
}



//// Intrusive Data Structures
/// What Makes a Data Structure "Intrusive"
/// Nodes contain data (not data contains nodes)
/// Allocation controlled by user, not container
/// Single allocation per element
/// No indirection between element and node
use std::marker::PhantomPinned;
use std::pin::Pin;

struct ListNode<T> {
    value: T,
    next: Option<NonNull<ListNode<T>>>,
    prev: Option<NonNull<ListNode<T>>>,
    _pin: PhantomPinned,  // Prevent moving after insertion
}

pub struct IntrusiveList<T> {
    head: Option<NonNull<ListNode<T>>>,
    tail: Option<NonNull<ListNode<T>>>,
    len: usize,
}

impl<T> IntrusiveList<T> {
    pub fn new() -> Self {
        Self {
            head: None,
            tail: None,
            len: 0,
        }
    }
    
    /// # Safety
    /// - `node` must be pinned and not already in a list
    /// - `node` must outlive the list
    pub unsafe fn push_back(&mut self, node: Pin<&mut ListNode<T>>) {
        let node_ptr = NonNull::from(node.get_unchecked_mut());
        
        match self.tail {
            Some(mut tail) => {
                // SAFETY: tail is valid (we maintain this invariant)
                unsafe {
                    tail.as_mut().next = Some(node_ptr);
                    node_ptr.as_mut().prev = Some(tail);
                }
                self.tail = Some(node_ptr);
            }
            None => {
                // First element
                self.head = Some(node_ptr);
                self.tail = Some(node_ptr);
            }
        }
        
        self.len += 1;
    }
    
    pub unsafe fn remove(&mut self, node: Pin<&mut ListNode<T>>) {
        let node_ptr = NonNull::from(node.get_unchecked_mut());
        
        // SAFETY: node_ptr is valid (in our list)
        let (prev, next) = unsafe {
            let node_ref = node_ptr.as_mut();
            (node_ref.prev, node_ref.next)
        };
        
        match prev {
            Some(mut prev_ptr) => unsafe {
                prev_ptr.as_mut().next = next;
            },
            None => {
                // Was head
                self.head = next;
            }
        }
        
        match next {
            Some(mut next_ptr) => unsafe {
                next_ptr.as_mut().prev = prev;
            },
            None => {
                // Was tail
                self.tail = prev;
            }
        }
        
        // Clear node's pointers
        unsafe {
            node_ptr.as_mut().prev = None;
            node_ptr.as_mut().next = None;
        }
        
        self.len -= 1;
    }
}

// Usage
fn main() {
    let mut list = IntrusiveList::new();
    
    // Nodes must be heap-allocated and pinned
    let node1 = Box::pin(ListNode {
        value: 1,
        next: None,
        prev: None,
        _pin: PhantomPinned,
    });
    
    let node2 = Box::pin(ListNode {
        value: 2,
        next: None,
        prev: None,
        _pin: PhantomPinned,
    });
    
    unsafe {
        list.push_back(Pin::as_mut(&node1));
        list.push_back(Pin::as_mut(&node2));
        
        // Later remove
        list.remove(Pin::as_mut(&node1));
    }
}
