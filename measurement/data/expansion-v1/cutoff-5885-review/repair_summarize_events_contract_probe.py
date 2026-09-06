import unittest
from solution import summarize_events

class LegacyEvents:
    def __getitem__(self, index):
        if index == 0:
            return {'type': 'quit'}
        raise IndexError

class Probe(unittest.TestCase):
    def test_valid_iteration_protocol(self):
        self.assertEqual(summarize_events(LegacyEvents()), ())

    def test_valid_large_coordinate(self):
        self.assertEqual(summarize_events([{'type': 'move', 'x': 10**4999, 'y': 0}]), ('MOVE 1' + '0'*4999 + ',0',))

if __name__ == '__main__':
    unittest.main()
