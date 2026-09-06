#[path = "solution.rs"]
mod solution;
use solution::{emit_rust_models, GenerationError, Model, ModelType, Property};
#[test]
fn first_models_property_error_precedes_later_model_error() {
    let models = vec![
        Model { name: "First".into(), properties: vec![Property {
            name: "bad-name".into(), model_type: ModelType::Text, required: true,
        }] },
        Model { name: "2Later".into(), properties: vec![] },
    ];
    assert_eq!(emit_rust_models(&models), Err(GenerationError::InvalidIdentifier("bad-name".into())));
}
