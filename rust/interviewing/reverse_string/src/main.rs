// Reverse a String - Input: &str, Output: String (reversed). Handle UTF-8 correctly.

fn reverse_string(s: &str) -> String {
    s.chars().rev().collect::<String>()
}

fn main() {
    let word: String = "Teste".to_string();
    let res: String = reverse_string(&word);

    println!(
        "{} == {}, {}",
        word,
        res,
        word.chars().rev().collect::<String>() == res
    );
}
