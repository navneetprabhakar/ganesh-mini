import unittest
from solution import normalize_origin_policy

class Probe(unittest.TestCase):
    def test_malformed_host_with_internal_space(self):
        with self.assertRaises(ValueError):
            normalize_origin_policy(['https://exa mple.com'])

if __name__ == '__main__':
    unittest.main()
