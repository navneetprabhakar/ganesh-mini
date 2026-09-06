import unittest
from solution import decode_query


class Probe(unittest.TestCase):
    def test_non_json_number_rejected(self):
        for body in ('{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(body=body):
                self.assertEqual(decode_query('GET', 'application/json', body), (400, None))

    def test_finite_json_depth(self):
        body = '{"x":'*600 + '0' + '}'*600
        error = None
        try:
            result = decode_query('GET', 'application/json', body)
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(result[0], 200)


if __name__ == '__main__':
    unittest.main()
