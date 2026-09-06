#[path = "solution.rs"]
mod solution;
use solution::AppendOnDivisor;

#[test]
fn minimum_integer_is_divisible_by_negative_one_without_overflow() {
    let mut output = String::from("prefix:");
    i64::MIN.append_on_divisor(-1, "yes", &mut output);
    assert_eq!(output, "prefix:yes");
}
