#[path = "solution.rs"]
mod solution;
use solution::{Ledger, Transfer};

#[test]
fn exact_maximum_balance_is_not_overflow() {
    let mut ledger = Ledger::new("rich".to_string(), u64::MAX).unwrap();
    ledger.add_account("sender".to_string()).unwrap();
    ledger.apply(&Transfer { from: "rich".into(), to: "sender".into(), amount: 1 }).unwrap();
    assert_eq!(ledger.apply(&Transfer { from: "sender".into(), to: "rich".into(), amount: 1 }), Ok(()));
    assert_eq!(ledger.balance("rich"), Some(u64::MAX));
}
