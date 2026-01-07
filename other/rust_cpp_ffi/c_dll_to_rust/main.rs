use std::ffi::c_int;

#[link(name = "mathlib")]
extern "C" {
    fn add(a: c_int, b: c_int) -> c_int;
    fn multiply(a: c_int, b: c_int) -> c_int;
}

fn main() {
    unsafe {
        println!("add: {}", add(2, 3));
        println!("multiply: {}", multiply(4, 5));
    }
}

/*
Why unsafe?

Rust cannot verify:
ABI correctness
Memory safety
Thread safety
*/