#[path = "solution.rs"]
mod solution;
#[test]
fn public_dimension_change_does_not_panic_or_mutate_buffer() {
    let mut canvas = solution::Canvas::new(1, 1, solution::PixelOrder::Rgba, vec![7;4]).unwrap();
    canvas.width = 2;
    let result = canvas.put_pixel(1, 0, [1,2,3,4]);
    assert!(result.is_err());
    assert_eq!(canvas.pixels(), &[7;4]);
}
