import unittest

from solution import CallablePipeline


class FiniteRealTests(unittest.TestCase):
    def test_large_integer_reaches_identity_model(self):
        rows = [[10 ** 400]]
        result = CallablePipeline(model=lambda data: data).predict(rows)
        self.assertEqual(result, rows)
        self.assertIsNot(result[0], rows[0])


if __name__ == "__main__":
    unittest.main()
