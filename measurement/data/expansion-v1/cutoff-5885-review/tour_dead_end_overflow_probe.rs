#[path = "solution.rs"]
mod solution;
use solution::{analyze_tours, Passage};

#[test]
fn incomplete_paths_are_not_otherwise_valid_tours() {
    let passages = vec![
        Passage { from: "A".into(), to: "B".into(), minutes: u64::MAX },
        Passage { from: "B".into(), to: "C".into(), minutes: 1 },
        Passage { from: "D".into(), to: "E".into(), minutes: 1 },
    ];
    assert_eq!(analyze_tours(&passages), Ok(Vec::new()));
}
