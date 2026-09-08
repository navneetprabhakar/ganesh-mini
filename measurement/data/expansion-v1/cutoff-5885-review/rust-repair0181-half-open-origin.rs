#[path = "solution.rs"]
mod solution;
#[test]
fn finite_small_camera_keeps_origin_strictly_negative() {
    let rect = solution::tile_rect(solution::Size { width: 1.0, height: 1.0 }, 1.0,
        solution::Point { x: f32::MIN_POSITIVE, y: 0.0 }).unwrap();
    assert!(rect.x >= -1.0 && rect.x < 0.0, "origin {:?}", rect.x);
}
