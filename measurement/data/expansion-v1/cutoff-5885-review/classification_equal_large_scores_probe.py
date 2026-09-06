import unittest
from solution import summarize_classification


class ClassificationEqualLargeScoresTests(unittest.TestCase):
    def test_equal_finite_scores_have_half_confidence(self):
        result = summarize_classification({'a': 1e308, 'b': 1e308}, {'a': None, 'b': None})
        self.assertEqual(result['confidence'], 50.0)


if __name__ == '__main__':
    unittest.main()
