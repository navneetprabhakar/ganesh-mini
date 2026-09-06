#[path = "solution.rs"]
mod solution;

#[test]
fn capacity_overflow_is_reported_not_panicked() {
    let tiles = [solution::Tile { width: 1, height: 1, pixels: vec![7] }];
    assert!(matches!(solution::build_atlas(&tiles, usize::MAX), Err(solution::AtlasError::Overflow)));
}
