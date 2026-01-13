use std::ffi::c_int;

#[repr(C)]
pub struct Point {
    pub x: f32,
    pub y: f32,
}

#[no_mangle]
pub extern "C" fn add(a: c_int, b: c_int) -> c_int {
    a + b
}

#[no_mangle]
pub extern "C" fn multiply(a: c_int, b: c_int) -> c_int {
    a * b
}

/*
extern "C"
✔ Uses C ABI
✔ Disables name mangling
✔ Required for FFI
❌ Never use Rust ABI (extern "Rust") across languages


#[no_mangle]
✔ Prevents symbol renaming
✔ Required for Rust → C/C++


cdylib vs staticlib
| Type        | Use Case                 |
| ----------- | ------------------------ |
| `cdylib`    | Shared library for C/C++ |
| `staticlib` | Static `.a` / `.lib`     |
| `rlib`      | Rust-only                |


C ABI STABILITY RULES (VERY IMPORTANT)
✅ Safe types
i8/u8/i16/u16/i32/u32/i64/u64
f32/f64
*const T, *mut T
#[repr(C)] struct
bool (with care)
void* / *mut c_void

❌ Unsafe across FFI
String
Vec<T>
HashMap
Result<T, E>
enum (unless #[repr(C)])
trait objects
Box<T> (unless opaque pointer)


| Question                     | Expected Answer       |
| ---------------------------- | --------------------- |
| Why `extern "C"`?            | Stable ABI            |
| Why `unsafe`?                | Rust can’t verify FFI |
| Can Rust ABI change?         | Yes, unstable         |
| Can I pass a `String`?       | No                    |
| Difference cdylib/staticlib? | Linking model         |
| Who owns memory?             | Must be explicit      |
*/