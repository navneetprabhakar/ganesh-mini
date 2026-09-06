#[path = "solution.rs"]
mod solution;
use solution::{evaluate, EvalError};
#[test]
fn balanced_parentheses_with_extra_operand_report_offending_byte() {
    assert_eq!(evaluate("(1 2)"), Err(EvalError::UnexpectedToken(3)));
}
