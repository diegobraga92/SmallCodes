// Prime Number Check Determine if a number is prime. Optimize (check up to sqrt(n)).
fn prime_check(n: i32) -> bool {
    if n == 2 || n == 3 {
        return true;
    }

    if n < 2 || n % 2 == 0 {
        return false;
    }

    let lim = (n as f32).sqrt() as i32;

    for v in (3..=lim).step_by(2) {
        if n % v == 0 {
            return false;
        }
    }

    true
}

fn main() {
    let numbers = [
        -10, // negative
        0,   // not prime
        1,   // not prime
        2,   // smallest prime
        3,   // prime
        4,   // even, not prime
        5,   // prime
        6,   // even, not prime
        7,   // prime
        9,   // 3 × 3
        11,  // prime
        15,  // 3 × 5
        17,  // prime
        21,  // 3 × 7
        25,  // 5 × 5
        29,  // prime
        49,  // 7 × 7
        97,  // prime
        100, // even, not prime
    ];

    for &n in &numbers {
        println!("{:>4} → {}", n, prime_check(n));
    }
}
