import unittest
from solution import matrix_product


class Probe(unittest.TestCase):
    def test_finite_integer(self):
        self.assertEqual(matrix_product([[10**400]], [[1]]), [[10**400]])


if __name__ == '__main__':
    unittest.main()
