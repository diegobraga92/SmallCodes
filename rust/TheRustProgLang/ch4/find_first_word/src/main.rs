// Given an string with multiple words separated by spaces, find the first word.
fn first_word(s: &String) -> &str {
    let string_in_bytes = s.as_bytes();

    for (idx, &chr) in string_in_bytes.iter().enumerate() {
        if chr == b' ' {
            return &s[0..idx]
        }
    }

    &s[..]
}

fn main() {
    let s = String::from("hello world");

    let word = first_word(&s);

    println!("the first word is: {}", word);
}