struct TextFinder<'a> {
    text: &'a str,
}

impl<'a> TextFinder<'a> {
    fn new(text: &'a str) -> Self {
        TextFinder {text}
    }

    fn find_first(&self, keyword: &str) -> Option<&'a str> {
        self.text
        .find(keyword)
        .map(|idx| &self.text[idx..idx + keyword.len()])
    }

    fn find_many(&self, keyword: &str) -> Vec<&'a str> {
        self.text
        .match_indices(keyword)
        .map(|(_idx, m)| m)
        .collect()
    }
}

fn main() {
    let s = String::from("the quick brown fox jumps over the lazy dog");

    let finder = TextFinder::new(&s);

    let first = finder.find_first("the");
    let all_the = finder.find_many("the");

    drop(finder);

    assert_eq!(first, Some("the"));
    assert_eq!(all_the, vec!["the", "the"]);
    println!("first = {:?}, all = {:?}", first, all_the);
}
