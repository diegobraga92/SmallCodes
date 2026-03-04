/*
Custom Iterator Implementation
--------------------------------------------------------
Example:

pub struct EvenNumbers { ... }

Implement Iterator.

Senior signal:
- State ownership
- Iterator trait mastery
- Lifetimes if borrowing
*/
pub struct EvenNumbers {
    current: u32,
    max: u32,
}

impl EvenNumbers {
    pub fn new(max: u32) -> Self {
        Self { current: 0, max }
    }
}

impl Iterator for EvenNumbers {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        self.current += 2;

        if self.current > self.max {
            return None;
        }

        Some(self.current)
    }
}

fn main() {
    let evens = EvenNumbers::new(10);

    for n in evens {
        println!("{n}");
    }
}
