#[path = "solution.rs"]
mod solution;

#[test]
fn all_kinds_are_validated_before_summing() {
    let readings = [
        solution::Reading { value: u128::MAX, kind: "n".into() },
        solution::Reading { value: 1, kind: "n".into() },
        solution::Reading { value: 0, kind: "wrong".into() },
    ];
    assert!(matches!(solution::aggregate_readings(&readings, "n"),
        Err(solution::AggregateError::UnexpectedKind { expected, found }) if expected == "n" && found == "wrong"));
}
