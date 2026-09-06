#[path = "solution.rs"]
mod solution;
use solution::read_tagged_field;

#[test]
fn matched_non_nested_hyphenated_name_is_preserved() {
    assert_eq!(read_tagged_field("[item-name]exact text[/item-name]", "item-name"),
               Ok(Some("exact text".to_string())));
}
