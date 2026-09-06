import unittest
from solution import Document, collect_assets


class Probe(unittest.TestCase):
    def test_finite_dependency_chain(self):
        documents = {str(i): Document(b'x', (str(i + 1),) if i < 1099 else ()) for i in range(1100)}
        error = None
        try:
            result = collect_assets(documents, '0')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)
        self.assertEqual(list(result), [str(i) for i in range(1100)])


if __name__ == '__main__':
    unittest.main()
