#[path = "solution.rs"]
mod solution;

#[test]
fn finite_weights_do_not_make_valid_distribution_absent() {
    let actual = solution::weighted_decay_cdf(&[(f64::MAX, 1.0), (f64::MAX, 1.0)], 1.0);
    let expected = 1.0 - (-1.0f64).exp();
    assert!(actual.is_some(), "valid finite component weights returned None");
    assert!((actual.unwrap() - expected).abs() < 1e-14);
}

#[test]
fn finite_interval_interpolation_avoids_intermediate_overflow() {
    let actual = solution::interval_cdf(-f64::MAX, f64::MAX, 0.0).unwrap();
    assert!((actual - 0.5).abs() < 1e-14, "midpoint was {actual}");
}
