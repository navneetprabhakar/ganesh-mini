#[path = "solution.rs"]
mod solution;
use solution::Overlap;
#[test]
fn public_overlap_scores_avoid_intermediate_integer_overflow() {
    let overlap = Overlap { both_set: usize::MAX, both_clear: 0, left_only: 1, right_only: 0 };
    let scores = overlap.scores();
    assert!(scores.dice.is_finite() && scores.jaccard.is_finite());
    assert!((scores.jaccard - 1.0).abs() < 1e-10);
}
