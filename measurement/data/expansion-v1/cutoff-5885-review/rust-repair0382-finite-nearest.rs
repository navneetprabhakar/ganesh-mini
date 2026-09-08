#[path = "solution.rs"]
mod solution;
use solution::*;

#[test]
fn finite_distinct_distances_do_not_become_a_tie() {
    let mut store = SampleStore::new();
    store.train("m", &[
        TrainingSample { outcome: 2.0, features: vec![2e200] },
        TrainingSample { outcome: 1.0, features: vec![1e200] },
    ]).unwrap();
    assert_eq!(store.predict("m", &[vec![0.0]]).unwrap(), vec![1.0]);
}
