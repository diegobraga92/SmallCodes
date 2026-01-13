use std::thread;
use std::time::Duration;

#[link(name = "example")]
extern "C" {
    fn run_worker();
}

fn main() {
    unsafe {
        run_worker();
    }

    // Allow background thread to finish
    thread::sleep(Duration::from_secs(5));

    println!("C++ shared library executed");
}
