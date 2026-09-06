#[path = "solution.rs"]
mod solution;
use solution::{Sample, Segment, SegmentSet};
#[test]
fn newly_added_sample_wins_even_when_its_boundary_sorts_first() {
    let mut set = SegmentSet::new();
    set.add(Segment::new(5, 10, vec![Sample { position: 6, value: 1 }]).unwrap());
    set.add(Segment::new(0, 8, vec![Sample { position: 6, value: 2 }]).unwrap());
    assert_eq!(set.segments()[0].samples[0].value, 2);
}
