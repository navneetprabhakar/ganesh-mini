import unittest
from solution import attach_ratings


class RatingsEqualBoundaryTests(unittest.TestCase):
    def test_identical_scores_at_minimum_are_retained(self):
        ratings = [dict(record_id='x', score=0.1) for _ in range(6)]
        result = attach_ratings(ratings, [dict(record_id='x')], minimum=0.1)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
