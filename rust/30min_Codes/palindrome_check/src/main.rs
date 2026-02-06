// Palindrome Check  Check if a string is a palindrome (ignore case/non-alphanumeric optional extension).

fn pal_check(s: &str) -> bool {
    let clean_s: Vec<char> = s
        .chars()
        .filter(|c| c.is_alphanumeric())
        .map(|c| c.to_ascii_lowercase())
        .collect();

    clean_s.iter().eq(clean_s.iter().rev())
}

fn main() {
    let tests = vec![
        // Basic palindromes
        ("racecar", true),
        ("level", true),
        // Case insensitivity
        ("RaceCar", true),
        ("LeVeL", true),
        // Non-palindromes
        ("hello", false),
        ("rust", false),
        // Ignore non-alphanumeric characters
        ("A man, a plan, a canal: Panama", true),
        ("No 'x' in Nixon", true),
        // Numbers
        ("12321", true),
        ("12345", false),
        // Mixed letters and numbers
        ("1a2b2a1", true),
        ("1a2b3a1", false),
        // Edge cases
        ("", true),     // empty string
        ("a", true),    // single character
        ("!!!", true),  // only non-alphanumeric
        ("a!!!", true), // reduces to "a"
    ];

    for (input, expected) in tests {
        let result = pal_check(input);
        println!("Input: {:?} → {}, expected {}", input, result, expected);
        assert_eq!(result, expected);
    }

    println!("All tests passed!");
}
