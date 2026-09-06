from solution import box_iou

box = (0.0, 0.0, 1e200, 1e200)
actual = box_iou(box, box)
assert actual == 1.0, f"identical positive-area boxes IoU: {actual!r}"
