//// Iterators
// Iterator trait
pub trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
    // ... provided methods (adapters and consumers)
}


/// Iterator Adapters (Lazy), return new iterators, lazy evaluation, Chainable
let numbers = vec![1, 2, 3, 4, 5];

// map - transform each element
let squares = numbers.iter().map(|x| x * x);  // Iterator<i32>

// filter - keep elements matching predicate
let evens = numbers.iter().filter(|&x| x % 2 == 0);  // Iterator<&i32>

// filter_map - filter and map in one step
let maybe_numbers = vec![Some(1), None, Some(3), None, Some(5)];
let numbers_only = maybe_numbers.iter()
    .filter_map(|opt| *opt)  // Skip None, unwrap Some
    .collect::<Vec<i32>>();  // [1, 3, 5]

// take, skip - limit iteration
let first_three = numbers.iter().take(3);
let after_two = numbers.iter().skip(2);

// take_while, skip_while - conditional limits
let until_four = numbers.iter().take_while(|&&x| x < 4);

// enumerate - add indices
for (i, num) in numbers.iter().enumerate() {
    println!("{}: {}", i, num);
}

// chain - combine iterators
let more_numbers = vec![6, 7, 8];
let all_numbers = numbers.iter().chain(more_numbers.iter());

// zip - pair elements from two iterators
let letters = vec!['a', 'b', 'c'];
let pairs = numbers.iter().zip(letters.iter());  // (&1, &'a'), (&2, &'b'), ...

// cycle - repeat iterator endlessly
let repeating = numbers.iter().cycle().take(10);  // 1,2,3,4,5,1,2,3,4,5

// scan - stateful transformation (like fold but yields intermediate values)
let partial_sums = numbers.iter().scan(0, |sum, &x| {
    *sum += x;
    Some(*sum)  // Some to continue, None to stop
});  // 1, 3, 6, 10, 15

// flat_map - flatten nested structures
let matrix = vec![vec![1, 2], vec![3, 4]];
let flattened = matrix.iter().flat_map(|row| row.iter());  // &1, &2, &3, &4

// inspect - debug without consuming (like tap)
let debugged = numbers.iter()
    .inspect(|&x| println!("Before filter: {}", x))
    .filter(|&x| x % 2 == 0)
    .inspect(|x| println!("After filter: {}", x));


/// Iterator Consumers (Eager), consume to produce final value, trigger evaluation on whole chain, can't be chained further
let numbers = vec![1, 2, 3, 4, 5];

// collect - gather into collection
let doubled: Vec<i32> = numbers.iter().map(|&x| x * 2).collect();
let doubled_alt = numbers.iter().map(|&x| x * 2).collect::<Vec<i32>>();

// Partition - split into two collections
let (even, odd): (Vec<i32>, Vec<i32>) = numbers.iter()
    .partition(|&&x| x % 2 == 0);  // ([2, 4], [1, 3, 5])

// fold - accumulate values with initial accumulator
let sum = numbers.iter().fold(0, |acc, &x| acc + x);  // 15
let product = numbers.iter().fold(1, |acc, &x| acc * x);  // 120

// reduce - fold without initial value (returns Option)
let max = numbers.iter().reduce(|a, b| if a > b { a } else { b });  // Some(&5)

// any, all - existential checks
let has_three = numbers.iter().any(|&x| x == 3);  // true
let all_positive = numbers.iter().all(|&x| x > 0);  // true

// find - get first matching element
let first_even = numbers.iter().find(|&&x| x % 2 == 0);  // Some(&2)

// position - find index of first matching element
let pos_of_three = numbers.iter().position(|&x| x == 3);  // Some(2)

// max, min - extremal values (requires Ord trait)
let max_val = numbers.iter().max();  // Some(&5)
let min_val = numbers.iter().min();  // Some(&1)

// count - number of elements
let count = numbers.iter().count();  // 5

// last - final element
let last = numbers.iter().last();  // Some(&5)

// nth - get element at position
let third = numbers.iter().nth(2);  // Some(&3)

// for_each - side effects (like map but consumer)
numbers.iter().for_each(|&x| println!("Number: {}", x));

// sum, product - specialized folds (requires appropriate trait)
let total: i32 = numbers.iter().sum();  // 15
let factorial: i32 = numbers.iter().product();  // 120

// unzip - convert iterator of pairs to pair of collections
let pairs = vec![(1, 'a'), (2, 'b'), (3, 'c')];
let (nums, chars): (Vec<i32>, Vec<char>) = pairs.into_iter().unzip();

/// Comparison
// Adapter chain (lazy - nothing happens yet)
let adapter_chain = numbers.iter()
    .map(|x| x * 2)        // adapter
    .filter(|x| x > &5);   // adapter

// Consumer triggers evaluation
let result: Vec<i32> = adapter_chain.collect();  // consumer
println!("{:?}", result);  // [6, 8, 10]

// Common pattern: adapter chain ending with consumer
let sum_of_squares: i32 = numbers.iter()
    .map(|x| x * x)        // adapter
    .sum();                // consumer

// Chaining mistake - can't chain after consumer
let mut iter = numbers.iter();
let first_even = iter.find(|&&x| x % 2 == 0);  // consumer - consumes up to first even
// iter is partially consumed now!
let next = iter.next();  // Gets element after first even



//// Custom Iterators, useful for Streaming parsing, protocol decoding, traversol, avoiding allocation
/// Using Iterator Trait
struct Counter {
    current: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Self {
        Counter { current: 0, max }
    }
}

impl Iterator for Counter {
    type Item = u32;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            self.current += 1;
            Some(self.current)
        } else {
            None
        }
    }
}

// Using custom iterator
let counter = Counter::new(5);
for num in counter {
    println!("{}", num);  // 1, 2, 3, 4, 5
}

// Can use all iterator methods
let sum: u32 = Counter::new(5).sum();  // 15


/// Using iter, iter_mut, into_iter
struct CustomCollection<T> {
    data: Vec<T>,
}

impl<T> CustomCollection<T> {
    // Borrowing iterator
    fn iter(&self) -> impl Iterator<Item = &T> {
        self.data.iter()
    }
    
    // Mutating iterator
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut T> {
        self.data.iter_mut()
    }
    
    // Owning iterator
    fn into_iter(self) -> impl Iterator<Item = T> {
        self.data.into_iter()
    }
}

// Auto-implement IntoIterator for for-loops
impl<T> IntoIterator for CustomCollection<T> {
    type Item = T;
    type IntoIter = std::vec::IntoIter<T>;
    
    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}

// Now works with for loops
let collection = CustomCollection { data: vec![1, 2, 3] };
for item in collection {
    println!("{}", item);
}

/// Custom Adapter
struct StepBy<I> {
    iter: I,
    step: usize,
    first_take: bool,
}

impl<I> StepBy<I> {
    fn new(iter: I, step: usize) -> Self {
        StepBy { iter, step, first_take: true }
    }
}

impl<I: Iterator> Iterator for StepBy<I> {
    type Item = I::Item;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.first_take {
            self.first_take = false;
            self.iter.next()
        } else {
            // Skip (step - 1) elements
            for _ in 0..(self.step - 1) {
                self.iter.next()?;  // Return None if we run out
            }
            self.iter.next()
        }
    }
}

// Usage
let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
let stepped: Vec<i32> = StepBy::new(numbers.into_iter(), 3).collect();
println!("{:?}", stepped);  // [1, 4, 7, 10]


/// Stateful iterators, owns its state, next is cheap, return none after exhaustion
struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let new_next = self.current.checked_add(self.next)?;
        let result = self.current;
        self.current = self.next;
        self.next = new_next;
        Some(result)
    }
}

// Infinite iterator with take
let first_ten: Vec<u64> = Fibonacci::new().take(10).collect();
// [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] 



//// Closure Traits (Fn, FnMut, FnOnce), Fn ⊂ FnMut ⊂ FnOnce
/// Fn captures by reference, read-only
// Can be called multiple times, cannot mutate state
fn execute<F>(closure: F) 
where
    F: Fn(),
{
    closure();
    closure();  // Can call multiple times
}

let name = "Alice";
let greet = || {
    println!("Hello, {}", name);  // Only reads name
};

execute(greet);
// greet can be called many times

// Common use: passing to map/filter
let numbers = vec![1, 2, 3];
let threshold = 2;
let filtered: Vec<i32> = numbers.iter()
    .filter(|&x| *x > threshold)  // Fn closure
    .cloned()
    .collect();


/// FnMut by mutable reference, can modify
// Can be called multiple times, can mutate state
fn execute_mut<F>(mut closure: F) 
where
    F: FnMut(),
{
    closure();  // Can be called multiple times
    closure();
}

let mut counter = 0;
let mut increment = || {
    counter += 1;  // Mutates captured variable
    println!("Counter: {}", counter);
};

execute_mut(increment);
// increment can still be called

// Using with iterators
let mut nums = vec![1, 2, 3];
nums.iter_mut().for_each(|x| {
    *x *= 2;  // FnMut closure
});

// Sorting with custom comparison (FnMut)
let mut words = vec!["apple", "banana", "cherry"];
words.sort_by(|a, b| a.len().cmp(&b.len()));


/// FnOnce by value, consumes captures values
// Takes ownership of captured variables
fn execute_once<F>(closure: F) -> i32 
where
    F: FnOnce() -> i32,
{
    closure()  // Can only be called once
}

let x = vec![1, 2, 3];
let closure = move || {
    // x moved into closure
    x.len() as i32
    // x cannot be used here anymore
};

let result = execute_once(closure);
// closure cannot be called again - it's consumed

// Another example
let name = String::from("Alice");
let greet = || {
    println!("Hello, {}", name);
    name  // Returns name, consuming it
};  // FnOnce because it moves name out

let name_again = greet();  // Can only call once
// greet();  // Error: cannot call FnOnce twice


/// Determining Closure Traits Automatically:
// Rust infers the trait based on what closure does
let s = String::from("hello");

// Fn - only reads
let print_len = || println!("{}", s.len());
print_len();  // OK
print_len();  // OK - can call multiple times

// FnMut - modifies
let mut count = 0;
let mut increment = || count += 1;
increment();  // OK
// let another = increment;  // Error - would need mut

// FnOnce - consumes
let consume = || drop(s);
consume();  // OK
// consume();  // Error - can't call twice
// println!("{}", s);  // Error - s was moved


/// Explicit Trait Bounds
// Accepting different closure types
struct Processor<F> {
    callback: F,
}

impl<F> Processor<F>
where
    F: FnMut(&str),  // Accepts FnMut and Fn (but not FnOnce)
{
    fn process(&mut self, data: &str) {
        (self.callback)(data);
    }
}

// Storing closures in structs
struct Button<F> {
    on_click: F,
}

impl<F> Button<F>
where
    F: Fn(),  // Only immutable closures
{
    fn click(&self) {
        (self.on_click)();
    }
}

// Returning closures from functions
fn make_multiplier(factor: i32) -> impl Fn(i32) -> i32 {
    move |x| x * factor  // factor captured by move
}

let times_two = make_multiplier(2);
println!("{}", times_two(5));  // 10


/// move Keyword with Closures, forces ownership capture, used in Threads, Async
// Forces closure to take ownership of captured variables
fn create_closures() -> (impl Fn(), impl Fn()) {
    let data = vec![1, 2, 3];
    
    // Without move - borrows data
    let print_len = || println!("Length: {}", data.len());
    
    // With move - takes ownership of data
    let consume_data = move || {
        println!("Consuming data of length: {}", data.len());
        drop(data);  // Now we can drop it
    };
    
    (print_len, consume_data)
}

// Necessary for spawning threads
use std::thread;
let data = vec![1, 2, 3];
thread::spawn(move || {
    println!("Data in thread: {:?}", data);  // data moved into thread
});
// data no longer accessible here



//// Capturing Semantics
/// By reference (default)
let x = 10;
let y = 20;

let add = || x + y;  // Captures x and y by &
println!("{}", add());  // 30
println!("x: {}", x);   // Still accessible

/// By mutable ref
let mut counter = 0;
let mut increment = || {
    counter += 1;  // Upgrades to &mut capture
    counter
};

println!("{}", increment());  // 1
println!("{}", increment());  // 2
// println!("{}", counter);  // Error - borrowed as mutable

/// By move
let data = vec![1, 2, 3];
let consume = move || {
    println!("Data length: {}", data.len());
    // data will be dropped when closure is dropped
};

consume();
// println!("{:?}", data);  // Error - data was moved


/// Capture rules and upgrading
let mut x = 5;
let y = 10;

// Starts as Fn - immutable borrow of x and y
let print_sum = || println!("Sum: {}", x + y);

// Upgrade to FnMut when we need to mutate
let mut increment_x = || {
    x += 1;  // Now captures x as &mut, y as &
    println!("x: {}, y: {}", x, y);
};

// Upgrade to FnOnce when we need ownership
let consume_y = move || {
    let _ = y;  // Takes ownership of y
    // x still borrowed as &mut
    x += 1;
    println!("x: {}", x);
};


/// Partial Capture
struct Data {
    a: i32,
    b: i32,
    c: i32,
}

let mut data = Data { a: 1, b: 2, c: 3 };

// Closure only captures part of struct
let get_a = || data.a;  // Only captures data.a by reference
println!("a: {}", get_a());

// Can still use data.b and data.c
println!("b: {}", data.b);

// But careful with mutable access
let mut inc_b = || data.b += 1;  // Captures data mutably
inc_b();
// println!("a: {}", data.a);  // Error - data is borrowed mutably