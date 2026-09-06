import unittest
from solution import count_payloads

class Probe(unittest.TestCase):
    def test_valid_deep_acyclic_catalog(self):
        catalog = 1
        for _ in range(600):
            catalog = [catalog]
        failed = False
        try:
            result = count_payloads(catalog)
        except RecursionError:
            failed = True
        self.assertFalse(failed, 'Valid acyclic catalog hits interpreter recursion limit')
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
