import unittest
from solution import freeze_report, thaw_report


class Probe(unittest.TestCase):
    def test_freeze_finite_integer(self):
        report = {'title': 'x', 'points': [(10**400, 0)], 'meta': {}}
        self.assertIsInstance(freeze_report(report), bytes)

    def test_thaw_finite_integer(self):
        blob = b'{"title":"x","points":[[' + b'1' + b'0'*400 + b',0]],"meta":{}}'
        self.assertEqual(thaw_report(blob)['points'], [(10**400, 0)])


if __name__ == '__main__':
    unittest.main()
