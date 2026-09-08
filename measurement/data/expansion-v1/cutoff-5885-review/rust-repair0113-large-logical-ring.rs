#[path = "solution.rs"]
mod solution;

#[test]
fn previous_handles_large_logical_length_without_allocation() {
    let mut ring = solution::FocusRing::new(usize::MAX);
    ring.next();
    assert_eq!(ring.index(), 1);
    ring.previous();
    assert_eq!(ring.index(), 0);
}
