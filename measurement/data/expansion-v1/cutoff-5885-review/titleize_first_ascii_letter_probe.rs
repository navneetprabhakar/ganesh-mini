#[path = "solution.rs"]
mod solution;
use solution::titleize;

#[test]
fn capitalizes_first_ascii_letter_not_only_first_character() {
    assert_eq!(titleize("123alpha.txt"), "123Alpha");
}
