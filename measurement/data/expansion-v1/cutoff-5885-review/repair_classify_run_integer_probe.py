import unittest
from solution import classify_run


class Probe(unittest.TestCase):
    def test_finite_singleton(self):
        self.assertEqual(classify_run([10**400]), 'constant')


if __name__ == '__main__':
    unittest.main()
