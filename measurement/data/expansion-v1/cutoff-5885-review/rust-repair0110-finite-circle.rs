#[path = "solution.rs"]
mod solution;

#[test]
fn finite_large_circle_contains_origin() {
    let world = solution::World {
        actors: vec![solution::Actor { id: 7, x: 1e200, y: 0.0, radius: 2e200 }],
        solids: vec![],
    };
    let hit = solution::cast_ray(&world, (0.0, 0.0), 0.0, 0.0);
    assert_eq!(hit, Some(solution::Hit { kind: solution::HitKind::Actor(7), distance: 0.0 }));
}
