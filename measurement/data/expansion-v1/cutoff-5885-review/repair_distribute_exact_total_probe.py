import unittest
from solution import distribute_tokens

class Probe(unittest.TestCase):
    def test_integer_total_preserved(self):
        total = 2**54 + 3
        self.assertEqual(distribute_tokens(total, {'only': 1}), {'only': total})

if __name__ == '__main__':
    unittest.main()
