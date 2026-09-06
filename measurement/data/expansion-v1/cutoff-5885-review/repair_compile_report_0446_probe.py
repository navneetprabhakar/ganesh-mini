import unittest
from solution import compile_report


class Probe(unittest.TestCase):
    def test_finite_integer(self):
        rows = [{'key': 'a', 'score': 10**400}]
        self.assertEqual(compile_report(rows, 'score', 1), rows)


if __name__ == '__main__':
    unittest.main()
