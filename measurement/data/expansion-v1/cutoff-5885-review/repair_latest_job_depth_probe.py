import unittest
from solution import latest_job_states

class Probe(unittest.TestCase):
    def test_finite_payload(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            latest_job_states(['x'], [{'job_id': 'x', 'state': 'ok', 'value': value}])
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
