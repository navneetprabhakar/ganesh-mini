#[path = "solution.rs"]
mod solution;
use solution::Mask3;
#[test]
fn zero_final_dimension_makes_empty_shape_valid() {
    assert!(Mask3::new(usize::MAX, 2, 0, vec![]).is_ok());
}
