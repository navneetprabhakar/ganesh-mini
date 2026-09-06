#[path = "solution.rs"]
mod solution;
use solution::build_factories;

#[test]
fn non_ascii_whitespace_is_literal_field_and_capability_data() {
    let factories = build_factories(&["\u{2003}id\u{2003}|title|rev|\u{2003}"]).unwrap();
    assert_eq!(factories[0].descriptor().id, "\u{2003}id\u{2003}");
    assert_eq!(factories[0].descriptor().capabilities, vec!["\u{2003}"]);
}
