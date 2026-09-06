#[path = "solution.rs"]
mod solution;
use solution::heaviest_route;

#[test]
fn losing_branch_overflow_is_not_hidden_by_subtree_maximum() {
    let edges = [(0, 1, -1), (1, 2, i64::MIN), (1, 3, 0)];
    assert_eq!(heaviest_route(4, 0, &edges), None);
}
