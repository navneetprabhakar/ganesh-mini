#[path = "solution.rs"]
mod solution;
use solution::parse_profile_card;

#[test]
fn non_ascii_value_whitespace_is_literal() {
    let card = parse_profile_card("code=c\nlabel=\u{2003}value\u{2003}\nsummary=s\ncategory=k\n").unwrap();
    assert_eq!(card.label, "\u{2003}value\u{2003}");
}

#[test]
fn non_ascii_prefix_does_not_turn_unknown_key_into_required_key() {
    assert!(parse_profile_card("\u{2003}code=c\nlabel=l\nsummary=s\ncategory=k\n").is_err());
}
