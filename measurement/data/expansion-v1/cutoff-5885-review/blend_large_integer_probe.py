import unittest

from solution import recurrent_blend


class LargeIntegerTests(unittest.TestCase):
    def test_empty_signals_copy_finite_integer(self):
        initial = {"x": [10 ** 400]}
        result = recurrent_blend(initial, [], 0)
        self.assertEqual(result, [initial])
        self.assertIsNot(result[0]["x"], initial["x"])


if __name__ == "__main__":
    unittest.main()
