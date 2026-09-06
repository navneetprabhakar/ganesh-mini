import unittest
from solution import Symbol, TokenSequence


class SymbolStorageProbe(unittest.TestCase):
    def test_stored_symbol_is_immutable_or_independently_captured(self):
        symbol = Symbol('kept')
        sequence = TokenSequence(symbol)
        try:
            symbol.name = 'changed'
        except (AttributeError, TypeError):
            pass
        self.assertEqual(bytes(sequence), b'{@kept}')


if __name__ == '__main__':
    unittest.main()
