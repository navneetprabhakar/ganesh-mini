#[path = "solution.rs"]
mod solution;
#[test]
fn finite_max_sigma_has_representable_positive_density_at_zero() {
    let bell = solution::make_bell(f64::MAX, None).ok().unwrap();
    let expected = (1.0 / f64::MAX) / (2.0 * std::f64::consts::PI).sqrt();
    assert!(expected > 0.0 && expected.is_finite());
    let actual = bell(0.0);
    assert!(actual > 0.0 && actual.is_finite(), "density {actual:?}, expected {expected:?}");
}
