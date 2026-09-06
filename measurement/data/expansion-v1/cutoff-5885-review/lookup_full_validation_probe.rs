#[path = "solution.rs"]
mod solution;
use solution::{lookup_setting, LookupError};

#[test]
fn conflicting_matches_do_not_skip_required_full_entry_validation() {
    let entries = vec![
        ("key".to_owned(), "first".to_owned()),
        ("KEY".to_owned(), "different".to_owned()),
        ("".to_owned(), "malformed".to_owned()),
    ];
    assert_eq!(lookup_setting(&entries, "key"),
        Err(LookupError::MalformedEntry { index: 2 }));
}
