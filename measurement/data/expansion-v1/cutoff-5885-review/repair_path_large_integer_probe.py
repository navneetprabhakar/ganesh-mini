import unittest
from solution import collapse_path

class Probe(unittest.TestCase):
    def test_contract(self):
        self.assertEqual(collapse_path([[10**400, 0]]), [(10**400, 0)])

if __name__ == '__main__':
    unittest.main()
