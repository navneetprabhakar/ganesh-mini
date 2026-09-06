#[path = "solution.rs"]
mod solution;
use solution::{create_rule, update_rule, Channel, RuleError, RulePatch};

#[test]
fn entire_proposed_result_includes_public_base_fields() {
    let mut rule = create_rule(1, vec![Channel::Email], "valid".to_string()).unwrap();
    rule.id = 0;
    let original = rule.clone();
    let outcome = update_rule(&mut rule, RulePatch {
        expires_after: Some(Some(30)), tags: None,
    });
    assert_eq!(outcome, Err(RuleError::InvalidId));
    assert_eq!(rule, original);
}
