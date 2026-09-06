import unittest
from solution import MatrixCatalog, MatrixKind


class MatrixIntegerTests(unittest.TestCase):
    def test_finite_integer_vector_is_preserved(self):
        n = 10**400
        catalog = MatrixCatalog(MatrixKind.DENSE, [[n]], ["a"])
        self.assertEqual(catalog.vectors, [[n]])
        self.assertEqual(catalog.width, 1)


if __name__ == "__main__":
    unittest.main()
