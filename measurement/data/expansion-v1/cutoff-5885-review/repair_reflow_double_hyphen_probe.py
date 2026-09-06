import unittest
from solution import reflow_lines


class Probe(unittest.TestCase):
    def test_only_single_hyphen_is_removed(self):
        self.assertEqual(reflow_lines(['word--', 'next']), 'word-- next')


if __name__ == '__main__':
    unittest.main()
