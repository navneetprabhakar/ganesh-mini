#[path = "solution.rs"]
mod solution;

#[test]
fn compact_json_must_not_contain_unescaped_control_bytes() {
    let rendered = solution::render_string_list(&["\0\u{8}\u{c}".into()]);
    assert!(!rendered.bytes().any(|b| b < 0x20), "raw controls in {rendered:?}");
}
