#[path = "solution.rs"]
mod solution;
use solution::*;

#[test]
fn invalid_identifier_precedes_duplicate_when_not_all_names_are_valid() {
    let spec = RecordSpec { name: "Valid".into(), fields: vec![
        FieldSpec { name: "same".into(), kind: FieldKind::U8 },
        FieldSpec { name: "same".into(), kind: FieldKind::U8 },
        FieldSpec { name: "bad-name".into(), kind: FieldKind::U8 },
    ] };
    assert_eq!(generate_record(&spec), Err(GenerateError::InvalidIdentifier("bad-name".into())));
}

#[test]
fn reserved_keyword_is_not_a_valid_rust_record_name() {
    let spec = RecordSpec { name: "abstract".into(), fields: vec![] };
    assert_eq!(generate_record(&spec), Err(GenerateError::InvalidIdentifier("abstract".into())));
}
