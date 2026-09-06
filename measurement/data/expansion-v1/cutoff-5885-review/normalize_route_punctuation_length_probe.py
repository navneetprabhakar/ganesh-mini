import unittest

from solution import normalize_route


class LabelLengthTests(unittest.TestCase):
    def test_punctuation_counts_toward_label_length(self):
        self.assertEqual(normalize_route("a!/c"), "c/a!")


if __name__ == "__main__":
    unittest.main()
