import unittest
from solution import simulate_cart


class FrameSequenceTests(unittest.TestCase):
    def test_range_is_valid_three_item_sequence(self):
        self.assertEqual(simulate_cart([range(1, 4)], ["F"], 1),
                         {"alive": True, "steps": 1, "checkpoints": 0})


if __name__ == "__main__":
    unittest.main()
