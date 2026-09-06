import unittest
from solution import split_compound


class CompoundDepthTests(unittest.TestCase):
    def test_long_input_with_only_one_split(self):
        self.assertEqual(split_compound("a" * 1200, ["a"]), [("a",) * 1200])


if __name__ == "__main__":
    unittest.main()
