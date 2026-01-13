// Procedural Macro
use proc_macro;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}

// Regular Macro
#[macro_export]
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

fn main() {
    println!("Hello, world!");
}
