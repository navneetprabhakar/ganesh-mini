#[path = "solution.rs"]
mod solution;
use solution::{Transfer, TransferLog};

#[test]
fn moving_a_nul_delimited_boundary_must_be_detected() {
    let mut log = TransferLog::new();
    log.append(Transfer { from: "a\0b".into(), to: "c".into(), units: 1 }).unwrap();
    assert!(log.is_valid());
    log.records[0].transfer.from = "a".into();
    log.records[0].transfer.to = "b\0c".into();
    assert!(!log.is_valid());
}
