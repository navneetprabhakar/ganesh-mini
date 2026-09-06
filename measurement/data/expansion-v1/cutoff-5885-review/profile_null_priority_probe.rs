#[path = "solution.rs"]
mod solution;

#[test]
fn forbidden_null_is_first_segment_error() {
    let settings = solution::ParseSettings { allow_missing_required: true, reject_null_required: true };
    assert_eq!(solution::parse_profile("endpoint=null;tracing=bad", settings), Err(solution::ProfileError::NullEndpoint));
}
