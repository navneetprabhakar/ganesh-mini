#[path = "solution.rs"]
mod solution;
use solution::{check_capacity, Allocation, DistributionError};

#[test]
fn late_allocation_error_precedes_earlier_sum_overflow() {
    let allocations = [
        Allocation { recipient: "a".into(), units: u64::MAX },
        Allocation { recipient: "b".into(), units: 1 },
        Allocation { recipient: "".into(), units: 1 },
    ];
    assert_eq!(check_capacity(u64::MAX, 0, &allocations, 0, 0, 0),
        Err(DistributionError::EmptyRecipient));
}
