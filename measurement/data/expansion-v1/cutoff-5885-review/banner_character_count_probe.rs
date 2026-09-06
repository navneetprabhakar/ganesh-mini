#[path = "solution.rs"]
mod solution;

#[test]
fn below_character_limit_non_ascii_reports_first_rejected_byte() {
    let input = "é".repeat(32768);
    assert_eq!(input.chars().count(), 32768);
    assert_eq!(solution::encode_banner(&input), Err(solution::CellError::NonPrintable { byte_index: 0 }));
}
