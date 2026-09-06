#[path = "solution.rs"]
mod solution;
use solution::*;

#[test]
fn single_point_center_is_itself_even_at_max_finite_coordinate() {
    let input = vec![Mesh { group: "g".into(), vertices: vec![Point3 {
        x: f64::MAX, y: 0.0, z: 0.0,
    }] }];
    let result = transform_meshes(&input, TransformOptions {
        center_on_origin: true, snap_to_ground: false, analyze_groups: false,
    }).unwrap();
    assert_eq!(result.meshes[0].vertices[0], Point3 { x: 0.0, y: 0.0, z: 0.0 });
}
