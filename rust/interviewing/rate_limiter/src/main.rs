/*
Generic Rate Limiter (Token Bucket)
--------------------------------------------------------
pub struct RateLimiter { ... }

pub fn allow(&mut self) -> bool

Senior signal:
- Time handling
- Instant vs SystemTime
- Edge cases
- Deterministic testing discussion
*/
use std::thread::sleep;
use std::time::{Duration, Instant};

pub struct RateLimiter {
    capacity: f64,
    tokens: f64,
    refill_rate: f64,
    last_refill: Instant,
}

impl RateLimiter {
    pub fn new(capacity: u32, refill_rate: f64) -> Self {
        Self {
            capacity: capacity as f64,
            tokens: capacity as f64,
            refill_rate,
            last_refill: Instant::now(),
        }
    }

    pub fn allow(&mut self) -> bool {
        self.refill();

        if self.tokens >= 1.0 {
            self.tokens -= 1.0;
            return true;
        }

        false
    }

    fn refill(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_refill);
        let elapsed_secs = elapsed.as_secs_f64();
        let new_tokens = elapsed_secs * self.refill_rate;

        if new_tokens > 0.0 {
            self.tokens = (self.tokens + new_tokens).min(self.capacity);
            self.last_refill = now;
        }
    }
}

fn main() {
    println!("Running RateLimiter tests...");

    // Test 1: Initial burst allowed
    {
        let mut limiter = RateLimiter::new(3, 1.0);

        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(!limiter.allow());

        println!("✓ Test 1 passed: burst behavior");
    }

    // Test 2: Refill after 1 second
    {
        let mut limiter = RateLimiter::new(1, 1.0);

        assert!(limiter.allow());
        assert!(!limiter.allow());

        sleep(Duration::from_secs(1));

        assert!(limiter.allow());

        println!("✓ Test 2 passed: refill works");
    }

    // Test 3: Capacity is never exceeded
    {
        let mut limiter = RateLimiter::new(2, 10.0);

        // Drain
        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(!limiter.allow());

        // Wait long enough to overflow capacity
        sleep(Duration::from_secs(2));

        // Should refill only up to capacity (2)
        assert!(limiter.allow());
        assert!(limiter.allow());
        assert!(!limiter.allow());

        println!("✓ Test 3 passed: capacity cap enforced");
    }

    // Test 4: Partial refill behavior
    {
        let mut limiter = RateLimiter::new(1, 2.0); // 2 tokens/sec

        assert!(limiter.allow());
        assert!(!limiter.allow());

        sleep(Duration::from_millis(500)); // 0.5 sec → 1 token

        assert!(limiter.allow());
        assert!(!limiter.allow());

        println!("✓ Test 4 passed: fractional refill works");
    }

    println!("All tests passed.");
}
