// Fibonacci Sequence Return nth Fibonacci number (iterative or recursive with memoization).
use std::collections::HashMap;

fn fib(n: i32, m: &mut HashMap<i32, i32>) -> i32 {
    if let Some(&res) = m.get(&n) {
        return res;
    }

    let res = match n {
        n if n <= 0 => 0,
        1 => 1,
        _ => fib(n - 1, m) + fib(n - 2, m),
    };

    m.insert(n, res);
    res
}

fn main() {
    let mut memo: HashMap<i32, i32> = HashMap::new();

    // Basic cases
    println!("fib(-1) = {} (expected 0)", fib(-1, &mut memo));
    println!("fib(0)  = {} (expected 0)", fib(0, &mut memo));
    println!("fib(1)  = {} (expected 1)", fib(1, &mut memo));
    println!("fib(2)  = {} (expected 1)", fib(2, &mut memo));

    // Small numbers
    println!("fib(3)  = {} (expected 2)", fib(3, &mut memo));
    println!("fib(4)  = {} (expected 3)", fib(4, &mut memo));
    println!("fib(5)  = {} (expected 5)", fib(5, &mut memo));

    // Medium numbers
    println!("fib(10) = {} (expected 55)", fib(10, &mut memo));
    println!("fib(15) = {} (expected 610)", fib(15, &mut memo));
    println!("fib(20) = {} (expected 6765)", fib(20, &mut memo));

    // Repeated calls (tests memoization)
    println!("fib(20) again = {} (expected 6765)", fib(20, &mut memo));
    println!("fib(15) again = {} (expected 610)", fib(15, &mut memo));
}
