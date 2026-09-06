#[path = "solution.rs"]
mod solution;
use solution::decode_flips;
use std::collections::BTreeSet;

#[test]
fn compound_path_obeys_the_declared_axial_deltas() {
    // (1,0)+(1,-1)+(0,-1)+(0,1)+(-1,1) = (1,0).
    assert_eq!(decode_flips("ruruldrdl"), Ok(BTreeSet::from([(1, 0)])));
}
