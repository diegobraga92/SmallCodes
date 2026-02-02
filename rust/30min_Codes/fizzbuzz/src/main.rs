// 1.  FizzBuzz - Print numbers 1-100, replace multiples of 3 with "Fizz", multiples of 5 with "Buzz", both with "FizzBuzz".

fn main() {
    for i in 1..=100 {
        let mut res: String = "".to_string();
        if i % 3 == 0 {
            res += "Fizz";
        }
        if i % 5 == 0 {
            res += "Buzz";
        }

        if res == "" {
            println!("{}", i);
        } else {
            println!("{}", res);
        }
    }
}
