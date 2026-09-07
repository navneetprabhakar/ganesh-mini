#[path = "solution.rs"]
mod solution;

#[test]
fn non_ascii_whitespace_is_not_ascii_trimming() {
    assert_eq!(solution::project_slug("repo\u{2003}"), Some("repo\u{2003}".into()));
}
