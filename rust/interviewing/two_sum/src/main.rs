// Two Sum Given slice &[i32] and target i32, return indices of two numbers that add to target (Option<(usize, usize)>).

use std::collections::HashMap;

fn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {
    let mut m: HashMap<i32, usize> = HashMap::with_capacity(nums.len());

    for (idx, &n) in nums.iter().enumerate() {
        let res = target - n;

        match m.get(&res) {
            Some(&res_idx) => return Some((res_idx, idx)),
            None => {
                m.insert(n, idx);
            }
        };
    }

    None
}

fn main() {
    let tests = [
        (&[1, 2, 3, 4, 5, 6][..], 4, Some((0, 2))), // 1 + 3
        (&[2, 7, 11, 15][..], 9, Some((0, 1))),     // classic example
        (&[3, 2, 4][..], 6, Some((1, 2))),          // unordered
        (&[3, 3][..], 6, Some((0, 1))),             // duplicates
        (&[1, 2, 3][..], 10, None),                 // no solution
        (&[][..], 0, None),                         // empty slice
        (&[5][..], 5, None),                        // single element
    ];

    for (i, (nums, target, expected)) in tests.iter().enumerate() {
        let result = two_sum(nums, *target);

        println!(
            "Test {} | nums={:?}, target={} -> {:?} {}",
            i + 1,
            nums,
            target,
            result,
            if &result == expected {
                "✅ PASS"
            } else {
                "❌ FAIL"
            }
        );
    }
}
