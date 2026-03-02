/*
Streaming Median
--------------------------------------------------------
Insert numbers one-by-one and return current median.

Senior signal:
- Two-heap solution
- Complexity analysis
- Ownership modeling
*/
use std::cmp::Reverse;
use std::collections::BinaryHeap;

pub struct MedianFinder {
    lower: BinaryHeap<i32>,
    upper: BinaryHeap<Reverse<i32>>,
}

impl MedianFinder {
    pub fn new() -> Self {
        Self {
            lower: BinaryHeap::new(),
            upper: BinaryHeap::new(),
        }
    }

    pub fn insert(&mut self, num: i32) {
        self.lower.push(num);

        if let Some(max_lower) = self.lower.pop() {
            self.upper.push(Reverse(max_lower));
        }

        if self.upper.len() > self.lower.len() {
            if let Some(Reverse(min_upper)) = self.upper.pop() {
                self.lower.push(min_upper);
            }
        }
    }

    pub fn median(&self) -> f64 {
        if self.lower.len() > self.upper.len() {
            return *self.lower.peek().unwrap() as f64;
        }
        let a = *self.lower.peek().unwrap() as f64;
        let b = self.upper.peek().unwrap().0 as f64;
        (a + b) / 2.0
    }
}

fn main() {
    println!("Running streaming median tests...");

    // Test 1: Simple increasing sequence
    let mut mf = MedianFinder::new();
    mf.insert(1);
    assert_eq!(mf.median(), 1.0);

    mf.insert(2);
    assert_eq!(mf.median(), 1.5);

    mf.insert(3);
    assert_eq!(mf.median(), 2.0);

    mf.insert(4);
    assert_eq!(mf.median(), 2.5);

    println!("Test 1 passed.");

    // Test 2: Unsorted input
    let mut mf2 = MedianFinder::new();
    let input = vec![5, 15, 1, 3];
    let expected = vec![5.0, 10.0, 5.0, 4.0];

    for (i, val) in input.iter().enumerate() {
        mf2.insert(*val);
        assert_eq!(mf2.median(), expected[i]);
    }

    println!("Test 2 passed.");

    // Test 3: Negative numbers
    let mut mf3 = MedianFinder::new();
    let input = vec![-5, -10, -3];
    let expected = vec![-5.0, -7.5, -5.0];

    for (i, val) in input.iter().enumerate() {
        mf3.insert(*val);
        assert_eq!(mf3.median(), expected[i]);
    }

    println!("Test 3 passed.");

    println!("All tests passed successfully.");
}
