#[path = "solution.rs"]
mod solution;

#[test]
fn two_isolated_extreme_cubes_have_twelve_exterior_faces() {
    let cells = [(i32::MIN, 0, 0), (i32::MAX, 0, 0)];
    assert_eq!(solution::exterior_faces(&cells), 12);
}
