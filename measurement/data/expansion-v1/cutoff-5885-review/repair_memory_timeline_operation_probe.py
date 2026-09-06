import unittest
from solution import memory_timeline


class Probe(unittest.TestCase):
    def test_malformed_operation(self):
        with self.assertRaises(ValueError):
            memory_timeline(1, [([], 1)])


if __name__ == '__main__':
    unittest.main()
