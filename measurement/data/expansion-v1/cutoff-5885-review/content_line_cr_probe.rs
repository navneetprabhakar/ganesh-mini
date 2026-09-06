#[path = "solution.rs"]
mod solution;

#[test]
fn unterminated_trailing_cr_is_preserved() {
    assert_eq!(solution::first_content_line("x\r"), Some("x\r"));
}

#[test]
fn crlf_terminator_is_removed_even_with_an_earlier_isolated_cr() {
    assert_eq!(solution::first_content_line("\r x \r\n"), Some("\r x "));
}
