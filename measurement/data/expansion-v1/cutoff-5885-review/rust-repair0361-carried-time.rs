#[path = "solution.rs"]
mod solution;
use solution::*;

#[test]
fn complete_intervals_preserve_carried_time() {
    let mut grid = FixedGrid::new(1, 1, u64::MAX).unwrap();
    let input = HeldInput::default();
    assert_eq!(grid.advance(u64::MAX - 1, &input), 0);
    assert_eq!(grid.advance(u64::MAX, &input), 1);
    assert_eq!(grid.advance(1, &input), 1);
}
