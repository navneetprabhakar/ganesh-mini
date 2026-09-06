#[path = "solution.rs"]
mod solution;

#[test]
fn unknown_option_before_command_is_unexpected() {
    assert_eq!(solution::parse_invocation(&["--unknown"]), Err(solution::ParseError::Unexpected("--unknown".into())));
}
