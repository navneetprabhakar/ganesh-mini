#[path = "solution.rs"]
mod solution;
use solution::{BufferEnded, ByteSource, SliceSource};

fn use_declared_generic_method<S: ByteSource + ?Sized>(source: &mut S)
    -> Result<usize, BufferEnded>
{
    source.read_until(&mut Vec::new(), |a, b| a == b)
}

#[test]
fn declared_method_does_not_require_a_sized_implementor() {
    let mut source = SliceSource::new(b"aa");
    assert_eq!(use_declared_generic_method(&mut source), Ok(2));
}
