fn sum_even_fibonacci(f0: u64, f1: u64, sum: u64) -> u64 {

    if f1 >= 1_000_000_000 {
        return sum;
    }

    if f1 % 2 == 0 {
        return sum_even_fibonacci(f1, f0 + f1, sum + f1);
    }

    sum_even_fibonacci(f1, f0 + f1, sum)
}

fn print_output() {
    
    print!("Sum of Even Fibonacci Numbers: ");

    let result = sum_even_fibonacci(1, 2, 0);

    println!("{}", result);
}

fn main() {
    print_output();
}