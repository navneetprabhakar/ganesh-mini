import unittest
from solution import decode_options


class SpacedFloatTests(unittest.TestCase):
    def test_surrounding_whitespace_preserves_string(self):
        self.assertEqual(decode_options([["x", " 1.5 "]]), {"x": " 1.5 "})


if __name__ == "__main__":
    unittest.main()
