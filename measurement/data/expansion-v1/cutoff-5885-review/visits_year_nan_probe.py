import unittest
from solution import summarize_visits


class VisitsYearNaNTests(unittest.TestCase):
    def row(self, stamp, minutes):
        return dict(started_at=stamp, entrance='A', exit='B', minutes=minutes, membership='m')

    def test_canonical_early_year(self):
        self.assertEqual(summarize_visits([self.row('0001-01-01T00:00', 1)])['count'], 1)

    def test_nan_is_not_nonnegative(self):
        with self.assertRaises(ValueError):
            summarize_visits([self.row('2024-01-01T00:00', float('nan'))])


if __name__ == '__main__':
    unittest.main()
