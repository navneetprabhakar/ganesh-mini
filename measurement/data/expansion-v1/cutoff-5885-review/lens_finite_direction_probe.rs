#[path = "solution.rs"]
mod solution;
use solution::{LensCamera, Vec3};

#[test]
fn nonzero_finite_view_direction_can_be_normalized() {
    for z in [-1.0e200, -1.0e-200] {
        let camera = LensCamera::new(
            Vec3 { x: 0.0, y: 0.0, z: 0.0 },
            Vec3 { x: 0.0, y: 0.0, z },
            Vec3 { x: 0.0, y: 1.0, z: 0.0 },
            60.0, 0.0, 1.0, 1, 1,
        ).expect("finite nonzero direction with nonparallel up is valid");
        let rays = camera.rays_for_pixel(0, 0, 1).unwrap();
        assert_eq!(rays.len(), 1);
        assert_eq!(rays[0].0.direction, Vec3 { x: 0.0, y: 0.0, z: -1.0 });
    }
}
