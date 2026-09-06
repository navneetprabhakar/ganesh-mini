#[path = "solution.rs"]
mod solution;
use solution::{match_segments, Segment};

#[test]
fn qualifying_match_has_an_unrepresentable_required_score() {
    let probe = Segment { first: 0, second: 1, squared_length: 0,
        low_angle: 0, high_angle: 0, orientation: 0, reversed: false };
    let gallery = Segment { squared_length: u64::MAX, low_angle: 1, ..probe };
    // Required sum is u64::MAX + 1. No clamping/wrapping policy is specified.
    // Retaining the qualifying match is required regardless of that design gap.
    assert_eq!(match_segments(&[probe], &[gallery], u64::MAX, 1, false).len(), 1);
}
