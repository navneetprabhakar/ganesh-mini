import unittest
from solution import sum_measurements


class Probe(unittest.TestCase):
    def test_valid_long_integer(self):
        error = None
        try:
            total, count = sum_measurements(['1' * 5000])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual((total % 10, count), (1, 1))


if __name__ == '__main__':
    unittest.main()
