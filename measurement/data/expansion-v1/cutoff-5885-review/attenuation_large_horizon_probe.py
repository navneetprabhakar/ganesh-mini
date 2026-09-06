import unittest
from solution import attenuation

class Probe(unittest.TestCase):
    def test_linear_origin_is_one(self):
        self.assertEqual(attenuation(0, 10**400, 'linear'), 1.0)

if __name__ == '__main__':
    unittest.main()
