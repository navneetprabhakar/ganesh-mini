import unittest
from solution import advance_shipments

class Probe(unittest.TestCase):
    def test_one_transition_per_occurrence(self):
        item = dict(status='draft', packages=2, holds=0)
        result = advance_shipments([item, item])
        self.assertEqual([row['status'] for row in result], ['queued', 'queued'])

if __name__ == '__main__':
    unittest.main()
