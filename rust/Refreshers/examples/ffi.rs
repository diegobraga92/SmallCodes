//// Rust gress to C ABI rules, which define the calling convention
/// extern "C" -- Fixes calling convention
/// #[no_mangle] -- Stable symbol name
/// #[repr(C)] -- Predicatble struct layout
/// unsafe -- Compiler cannot prove safety

//// Exporting Rust as a DLL/Shared Lib
/// In Cargo.toml
/// [lib]
/// crate-type = ["cdylib"]

//// Example
crate-type = ["cdylib", "staticlib"]  # Dynamic and static libraries
// crate-type = ["cdylib"]  # For dynamic library (.dll, .so, .dylib)
// crate-type = ["staticlib"]  # For static library (.lib, .a)
// crate-type = ["lib"]  # For Rust-only usage

[dependencies]
libc = "0.2"  # For precise C type definitions

[profile.release]
lto = true  # Link-time optimization for smaller binaries
codegen-units = 1  # Better optimization
opt-level = 3
strip = true  # Remove symbols (optional)



// C-compatible types
use std::os::raw::{c_void, c_char, c_int, c_long, c_float, c_double};

// Platform-specific types
use std::ffi::{c_void, CString, CStr};
use std::os::raw::{c_uchar, c_ushort, c_uint, c_ulong};

// Opaque pointers for hiding Rust types
pub struct OpaqueRustType {
    // Private fields
    data: Vec<u8>,
}

// Exported as void pointer
type OpaqueHandle = *mut c_void;


//// Exporting Functions
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}


// lib.rs
use std::ffi::{CString, CStr};
use std::os::raw::{c_char, c_int};

// Export a simple function
#[no_mangle] // Preserve function name
pub extern "C" fn add_numbers(a: c_int, b: c_int) -> c_int {
    a + b
}

// Export string processing function
#[no_mangle]
pub extern "C" fn rust_greet(name: *const c_char) -> *mut c_char {
    unsafe {
        if name.is_null() {
            return std::ptr::null_mut();
        }
        
        // Convert C string to Rust string
        let c_str = CStr::from_ptr(name);
        let rust_str = match c_str.to_str() {
            Ok(s) => s,
            Err(_) => return std::ptr::null_mut(),
        };
        
        // Create response
        let response = format!("Hello, {} from Rust!", rust_str);
        
        // Convert back to C string (caller must free!)
        CString::new(response).unwrap().into_raw()
    }
}

// Memory management: free strings allocated by Rust
#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    unsafe {
        if s.is_null() {
            return;
        }
        // Convert back to CString and drop it
        let _ = CString::from_raw(s);
    }
}


//// Exporting Structs:
#[repr(C)]
pub struct Buffer {
    ptr: *mut u8,
    len: usize,
}

use std::os::raw::{c_int, c_float};

// Export a C-compatible struct (must be #[repr(C)])
#[repr(C)]
pub struct Point {
    x: c_float,
    y: c_float,
}

#[repr(C)]
pub struct Rectangle {
    top_left: Point,
    bottom_right: Point,
}

// Opaque handle pattern (hiding Rust implementation details)
pub struct RustCalculator {
    accumulator: f64,
    history: Vec<f64>,
}

#[no_mangle]
pub extern "C" fn calculator_create() -> *mut RustCalculator {
    Box::into_raw(Box::new(RustCalculator {
        accumulator: 0.0,
        history: Vec::new(),
    }))
}

#[no_mangle]
pub extern "C" fn calculator_add(calc: *mut RustCalculator, value: c_double) -> c_double {
    unsafe {
        if calc.is_null() {
            return 0.0;
        }
        let calc = &mut *calc;
        calc.accumulator += value;
        calc.history.push(value);
        calc.accumulator
    }
}

#[no_mangle]
pub extern "C" fn calculator_destroy(calc: *mut RustCalculator) {
    unsafe {
        if calc.is_null() {
            return;
        }
        let _ = Box::from_raw(calc); // Takes ownership and drops
    }
}


//// Returning a Buffer
#[no_mangle]
pub extern "C" fn alloc_buffer(len: usize) -> Buffer {
    let mut v = Vec::with_capacity(len);
    let ptr = v.as_mut_ptr();
    std::mem::forget(v);

    Buffer { ptr, len }
}


//// Free Function
#[no_mangle]
pub extern "C" fn free_buffer(buf: Buffer) {
    unsafe {
        Vec::from_raw_parts(buf.ptr, 0, buf.len);
    }
}


//// Callbacks and Function Pointers
use std::os::raw::{c_int, c_void};

// Type alias for C callback
type Callback = extern "C" fn(progress: c_int, user_data: *mut c_void);

#[no_mangle]
pub extern "C" fn process_with_callback(
    data: *const c_void,
    len: c_int,
    callback: Callback,
    user_data: *mut c_void,
) -> c_int {
    unsafe {
        // Simulate processing with progress updates
        for i in 0..100 {
            callback(i, user_data);
            // Simulate work
            std::thread::sleep(std::time::Duration::from_millis(10));
        }
        
        // Return success
        0
    }
}

// Callback with context using closures (more Rust idiomatic)
pub struct CallbackContext<F: FnMut(i32)> {
    callback: F,
}

impl<F: FnMut(i32)> CallbackContext<F> {
    pub extern "C" fn trampoline(progress: c_int, user_data: *mut c_void) {
        unsafe {
            let context = &mut *(user_data as *mut Self);
            (context.callback)(progress as i32);
        }
    }
}


//// Error-Handling
#[no_mangle]
pub extern "C" fn do_work(out: *mut i32) -> i32 {
    if out.is_null() {
        return -1;
    }
    unsafe { *out = 42 };
    0
}




//// Using C Libraries
/// Cargo.toml
[build-dependencies]
bindgen = "0.68" // Generate Rust bindings from C headers

// build.rs - Generate bindings at compile time
use std::env;
use std::path::PathBuf;

fn main() {
    // Tell cargo to link the C library
    println!("cargo:rustc-link-lib=someclib");
    
    // Specify library search paths
    println!("cargo:rustc-link-search=native=/usr/local/lib");
    println!("cargo:rustc-link-search=native=./lib");
    
    // Generate bindings
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")  // Your wrapper header
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        .generate()
        .expect("Unable to generate bindings");
    
    // Write bindings to file
    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}

//// Using libc
// Manual FFI declarations (when bindgen not available)
use libc::{c_int, c_void, c_char, size_t};
use std::ffi::CString;
use std::ptr;

// Declare external C functions
extern "C" {
    // From libc (standard C library)
    fn strlen(s: *const c_char) -> size_t;
    fn malloc(size: size_t) -> *mut c_void;
    fn free(ptr: *mut c_void);
    
    // From custom library
    fn some_c_function(arg: c_int) -> c_int;
    fn process_data(data: *const c_void, len: size_t) -> c_int;
}

pub fn call_c_library() {
    unsafe {
        // Call C standard library
        let c_str = CString::new("Hello").unwrap();
        let len = strlen(c_str.as_ptr());
        println!("C string length: {}", len);
        
        // Call custom C function
        let result = some_c_function(42);
        println!("C function returned: {}", result);
        
        // Pass data to C
        let data = vec![1u8, 2, 3, 4, 5];
        let result = process_data(data.as_ptr() as *const c_void, data.len());
        
        // Allocate memory in C, use in Rust
        let ptr = malloc(100) as *mut u8;
        if !ptr.is_null() {
            // Use the memory...
            free(ptr as *mut c_void);
        }
    }
}


//// Safe Wrappers
use libc::{c_int, c_void};
use std::ffi::CString;
use std::marker::PhantomData;
use std::mem::MaybeUninit;

// Safe wrapper for C library with RAII
pub struct SafeCLibrary {
    // Private to prevent direct construction
    _private: (),
}

impl SafeCLibrary {
    pub fn new() -> Result<Self, &'static str> {
        unsafe {
            if init_library() != 0 {
                return Err("Failed to initialize C library");
            }
        }
        Ok(SafeCLibrary { _private: () })
    }
    
    pub fn process(&self, input: &str) -> Result<String, &'static str> {
        let c_input = CString::new(input).map_err(|_| "Invalid input string")?;
        
        let mut output_buf = Vec::with_capacity(1024);
        unsafe {
            let result = process_string(
                c_input.as_ptr(),
                output_buf.as_mut_ptr() as *mut c_char,
                output_buf.capacity() as c_int,
            );
            
            if result < 0 {
                return Err("Processing failed");
            }
            
            // Set actual length
            output_buf.set_len(result as usize);
            
            // Convert to Rust string
            let output = CString::from_vec_unchecked(output_buf)
                .into_string()
                .map_err(|_| "Invalid UTF-8 from C library")?;
            
            Ok(output)
        }
    }
}

impl Drop for SafeCLibrary {
    fn drop(&mut self) {
        unsafe {
            cleanup_library();
        }
    }
}

// Declare C functions
extern "C" {
    fn init_library() -> c_int;
    fn cleanup_library();
    fn process_string(input: *const c_char, output: *mut c_char, output_len: c_int) -> c_int;
}