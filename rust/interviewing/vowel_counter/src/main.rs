fn vowel_counter(s: &str) -> usize {
    s.chars()
        .filter(|c| matches!(c.to_ascii_lowercase(), 'a' | 'e' | 'i' | 'o' | 'u'))
        .count()
}

fn main() {
    let test_cases = vec![
        ("aeiouw", 5),
        ("hello", 2),
        ("rhythm", 0),
        ("", 0),
        ("aeiou", 5),
        ("AEIOU", 5), // uppercase not counted
        ("Rust Programming", 4),
        ("12345", 0),
        ("a1e2i3o4u5", 5),
        ("the quick brown fox", 5),
        ("bcdfghjklmnpqrstvwxyz", 0),
    ];

    for (input, expected) in test_cases {
        let result = vowel_counter(input);
        println!(
            "Input: {:<25} | Expected: {:<2} | Got: {:<2} | {}",
            format!("\"{}\"", input),
            expected,
            result,
            if result == expected { "PASS" } else { "FAIL" }
        );
    }
}
