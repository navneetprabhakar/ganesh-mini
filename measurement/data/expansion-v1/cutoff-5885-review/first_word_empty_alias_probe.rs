#[path = "solution.rs"]
mod solution;

#[test]
fn all_whitespace_result_is_a_slice_of_the_original_string() {
    let text = String::from(" \t\u{2003}");
    let word = solution::first_word(&text);
    assert!(word.is_empty());
    let begin = text.as_ptr() as usize;
    let end = begin + text.len();
    let pointer = word.as_ptr() as usize;
    assert!(pointer >= begin && pointer <= end, "empty result does not alias input");
}
