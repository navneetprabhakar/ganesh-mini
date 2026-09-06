#[path = "solution.rs"]
mod solution;
use solution::total_column;

#[test]
fn zero_based_maximum_column_index_is_representable() {
    let mut number = usize::MAX as u128 + 1;
    let mut reversed = Vec::new();
    while number > 0 {
        number -= 1;
        reversed.push(b'A' + (number % 26) as u8);
        number /= 26;
    }
    reversed.reverse();
    let label = String::from_utf8(reversed).unwrap();
    assert_eq!(total_column(&[], &label), Ok(Vec::new()));
}
