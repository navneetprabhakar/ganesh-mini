#[path = "solution.rs"]
mod solution;
use solution::*;

#[test]
fn finite_large_velocity_has_representable_positive_motion_limit() {
    let samples = [BodySample { velocity: [1e200, 0.0],
        gradient: [[0.0; 2]; 2], damaged: true, material: 0 }];
    let materials = [MaterialRule { use_motion_limit: true, deformation_limit: None }];
    let actual = stable_step(1.0, &CellGrid { cell_width: 1.0 }, &samples, &materials).unwrap();
    assert!((actual / 1e-200 - 1.0).abs() < 1e-12, "actual={actual:?}");
}
