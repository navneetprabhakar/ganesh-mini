import unittest
from solution import sum_measurements


class ExactMeasurementTests(unittest.TestCase):
    def test_large_integer_sum_stays_exact(self):
        n = 10**400
        self.assertEqual(sum_measurements(n, 7), n + 7)


if __name__ == "__main__":
    unittest.main()
