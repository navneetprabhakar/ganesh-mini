import unittest
from solution import raise_cover_floor

class Probe(unittest.TestCase):
    def test_integer_supplement_of_one(self):
        combined, extra = raise_cover_floor([[2**53+1]], [[2**53]], 1)
        self.assertEqual(extra, [[1]])

if __name__ == '__main__':
    unittest.main()
