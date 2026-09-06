import unittest
from solution import reschedule


class ReviewProbe(unittest.TestCase):
    def test_only_matching_time_changes(self):
        time = {'hour': 1, 'minute': 2}
        entries = [{'id': 'a', 'time': time}, {'id': 'b', 'time': time}]
        result = reschedule(entries, 'a', 3, 4)
        self.assertEqual(result[0]['time'], {'hour': 3, 'minute': 4})
        self.assertEqual(result[1]['time'], {'hour': 1, 'minute': 2})
        self.assertEqual(time, {'hour': 1, 'minute': 2})


if __name__ == '__main__':
    unittest.main()
