#[path = "solution.rs"]
mod solution;

define_record! {
    #[cfg(any())]
    pub struct DisabledRecord {
        pub value: u32,
    }
}

define_record! {
    pub struct EnabledRecord {}
}

#[test]
fn conditional_outer_attribute_can_disable_a_record() {
    assert_eq!(EnabledRecord::field_names(), &[] as &[&str]);
}
