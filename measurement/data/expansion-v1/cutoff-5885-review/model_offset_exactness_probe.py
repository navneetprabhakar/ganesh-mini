import unittest
from solution import export_model


class ModelOffsetTests(unittest.TestCase):
    def test_integer_offset_cancellation_precedes_scaling(self):
        objects = [{"name": "x", "vertices": [(2**53 + 1, 0, 0)], "offset": (-2**53, 0, 0)}]
        self.assertEqual(export_model(objects, apply_offsets=True), "MODEL 1\nOBJECT x 1\nV 1 0 0\n")


if __name__ == "__main__":
    unittest.main()
