fn sum_multiples_3_or_5(range: &[i32]) -> i32 {
    
    match range.split_first() {
        None => 0,
        Some((&first, rest)) => {
            if first % 3 == 0 || first % 5 == 0 {
                first + sum_multiples_3_or_5(rest)
            } else {
                sum_multiples_3_or_5(rest)
            }
        }
    }
}

fn main() {
    let num = 29999;
    let range: Vec<i32> = (1..=num).collect();
    
    println!("Sum of multiples of 3 or 5: {}", sum_multiples_3_or_5(&range));
}
