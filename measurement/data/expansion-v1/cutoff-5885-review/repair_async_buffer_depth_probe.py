import unittest
from solution import AsyncBuffer

class Probe(unittest.IsolatedAsyncioTestCase):
    async def test_finite_record(self):
        value = []
        for _ in range(600):
            value = [value]
        error = None
        try:
            await AsyncBuffer().stage({'value': value})
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)

if __name__ == '__main__':
    unittest.main()
