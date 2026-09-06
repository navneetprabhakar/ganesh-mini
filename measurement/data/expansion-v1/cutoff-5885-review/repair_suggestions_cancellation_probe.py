import unittest
from solution import suggest_items


class ReviewProbe(unittest.TestCase):
    def test_finite_representable_dot_product(self):
        result = suggest_items([1e308, 1e308], [{'id': 'zero', 'features': [2, -2]}], 1)
        self.assertEqual(result, [{'id': 'zero', 'score': 0.0}])


if __name__ == '__main__':
    unittest.main()
