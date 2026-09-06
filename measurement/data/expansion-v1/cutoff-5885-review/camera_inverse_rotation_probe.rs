#[path = "solution.rs"]
mod solution;
use solution::{Camera2D, Vec2};

#[test]
fn inverse_round_trips_the_returned_view_and_projection() {
    let camera = Camera2D::new(Vec2 { x: 10.0, y: -2.0 }, std::f64::consts::FRAC_PI_2, 2.0, 8.0, 6.0).unwrap();
    let expected = Vec2 { x: 2.0, y: -3.0 };
    let world = camera.world_from_ndc(expected);
    let view = camera.view_matrix();
    let projection = camera.projection_matrix();
    let camera_x = view[0][0] * world.x + view[0][1] * world.y + view[0][2];
    let camera_y = view[1][0] * world.x + view[1][1] * world.y + view[1][2];
    let x = projection[0][0] * camera_x;
    let y = projection[1][1] * camera_y;
    assert!((x - expected.x).abs() < 1e-10 && (y - expected.y).abs() < 1e-10,
        "roundtrip ({x}, {y}) differs from ({}, {})", expected.x, expected.y);
}
