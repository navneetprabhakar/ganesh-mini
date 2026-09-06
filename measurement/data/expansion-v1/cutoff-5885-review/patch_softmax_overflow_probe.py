import unittest
from solution import PatchClassifier


class ExtremeScoreTests(unittest.TestCase):
    def test_single_class_probability_remains_one(self):
        classifier = PatchClassifier([[[1e308]]], [0])
        self.assertEqual(classifier.predict_proba([[2.0]]), [1.0])


if __name__ == "__main__":
    unittest.main()
