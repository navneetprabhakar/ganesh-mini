import csv
import io
import unittest
from solution import TimingLedger


class TimingCSVFieldsTests(unittest.TestCase):
    def test_csv_quotes_valid_text_fields(self):
        ledger = TimingLedger()
        ledger.add('read,scan', 'engine', 'json', 1, 2)
        rows = list(csv.reader(io.StringIO(ledger.csv_report())))
        self.assertEqual(rows[1], ['read,scan', 'engine', 'json', '1', '1', '2.000000'])

    def test_equal_finite_duration_average(self):
        ledger = TimingLedger()
        for engine in ('first', 'second'):
            ledger.add('read', engine, 'json', 1, 1e308)
            ledger.add('read', engine, 'json', 1, 1e308)
        row = ledger.comparison_series('read', 'json', 'first', 'second')[0]
        self.assertEqual(row['first_average'], 1e308)
        self.assertEqual(row['ratio'], 1.0)


if __name__ == '__main__':
    unittest.main()
