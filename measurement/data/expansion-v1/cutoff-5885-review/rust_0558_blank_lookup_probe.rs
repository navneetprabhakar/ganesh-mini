#[path = "solution.rs"]
mod solution;
use solution::{dispatch, Command, Reply, Workshop};

#[test]
fn blank_lookup_is_invalid_name() {
    let mut workshop = Workshop::default();
    assert_eq!(dispatch(&mut workshop, Command::Zone(" \t".into())), Reply::Invalid);
}
