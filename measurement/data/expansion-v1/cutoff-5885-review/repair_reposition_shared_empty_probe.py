import unittest
from solution import reposition

class Probe(unittest.TestCase):
    def test_unaffected_shared_empty_column(self):
        empty = []
        layout = {'source': ['card'], 'target': empty, 'other': empty}
        result = reposition(layout, 'card', 'target', 0)
        self.assertEqual(result, {'source': [], 'target': ['card'], 'other': []})

if __name__ == '__main__':
    unittest.main()
