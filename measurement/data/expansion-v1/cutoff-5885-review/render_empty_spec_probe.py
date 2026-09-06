import unittest
from solution import render_artifacts

class EmptySpecProbe(unittest.TestCase):
    def test_explicit_empty_format_specification_is_forbidden(self):
        with self.assertRaises(ValueError):
            render_artifacts({'name': 'Ada'}, {'a': '{name:}'})

if __name__ == '__main__':
    unittest.main()
