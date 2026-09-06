import unittest
from solution import rank_artifact_submissions


class IntegerScoreProbe(unittest.TestCase):
    def test_finite_arbitrary_precision_integer_score_is_preserved(self):
        score = 10 ** 400
        row = {'team': 'T', 'members': ['A'], 'files': [], 'score': score}
        self.assertEqual(rank_artifact_submissions([row], [])[0]['score'], score)


if __name__ == '__main__':
    unittest.main()
