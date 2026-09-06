import unittest
from solution import choose_groups

class Probe(unittest.TestCase):
    def test_single_full_size_combination(self):
        error = None
        try:
            choose_groups(list(range(1200)), 1200)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
