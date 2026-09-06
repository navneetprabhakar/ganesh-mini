import unittest
from solution import summarize_readings

class ReadingsNumericProbe(unittest.TestCase):
    def test_large_integer_is_finite(self):
        value = 10 ** 400
        result = summarize_readings('c', [{'day': 1, 'value': value}])
        self.assertEqual(result['points'][0]['value'], value)

    def test_representable_percent_change_avoids_intermediate_overflow(self):
        result = summarize_readings('c', [{'day': 1, 'value': -1e308}, {'day': 2, 'value': 1e308}])
        self.assertEqual(result['percent_change'], 200.0)

if __name__ == '__main__':
    unittest.main()
