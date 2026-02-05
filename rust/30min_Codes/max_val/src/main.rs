// Find the Maximum Value in a Slice/Array - Input: &[i32], Output: Option<i32> (handle empty slice).

fn max_val(arr: &[i32]) -> Option<i32> {
    if arr.is_empty() {
        return None;
    }

    let mut max = arr[0];

    for &i in arr {
        if i > max {
            max = i
        }
    }
    Some(max)
}

fn main() {
    println!("{}", max_val(&[1, 1000, 25555, 340]).unwrap());
}
