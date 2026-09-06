import unittest
from solution import emit_expression


class Probe(unittest.TestCase):
    def test_terminal_newline_is_not_identifier(self):
        with self.assertRaises(ValueError):
            emit_expression(('var', 'name\n'))

    def test_unhashable_operator(self):
        with self.assertRaises(ValueError):
            emit_expression(([], 1, 2))


if __name__ == '__main__':
    unittest.main()
