import unittest
from solution import paint_schedule


class SequenceSpanTests(unittest.TestCase):
    def test_range_is_a_three_item_sequence(self):
        self.assertEqual(paint_schedule([["a", "b", "c"]], [range(3)]), [["a", "<", ">"]])


if __name__ == "__main__":
    unittest.main()
