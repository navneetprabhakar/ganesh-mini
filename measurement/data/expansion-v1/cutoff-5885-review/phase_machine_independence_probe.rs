#[path = "solution.rs"]
mod solution;
use solution::{Phase, PhaseMachine};

#[test]
fn equal_warmups_retain_their_own_active_durations() {
    let _first = PhaseMachine::new(10, 20);
    let mut second = PhaseMachine::new(10, 30);
    assert_eq!(second.advance(10), vec![Phase::Active]);
    assert_eq!(second.remaining_ms, 30);
}

#[test]
fn cloned_machine_keeps_transition_state_after_original_advances() {
    let mut original = PhaseMachine::new(11, 21);
    let mut copied = original.clone();
    assert_eq!(original.advance(11), vec![Phase::Active]);
    assert_eq!(copied.advance(11), vec![Phase::Active]);
    assert_eq!(copied.remaining_ms, 21);
}
