#[path = "solution.rs"]
mod solution;
use solution::*;
use std::collections::BTreeSet;

#[test]
fn non_ascii_whitespace_is_part_of_repository_identity() {
    assert_eq!(normalize_repository("\u{2003}Org/Repo"), Some("\u{2003}org/repo".into()));
}

#[test]
fn unicode_whitespace_alias_does_not_gain_authorization() {
    let policy = TrustPolicy {
        organizations: BTreeSet::new(),
        repositories: BTreeSet::from(["org/repo".into()]),
    };
    assert!(!is_authorized(&policy, "\u{2003}org/repo"));
}
