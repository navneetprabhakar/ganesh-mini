import unittest
from solution import PanelState


class FalseyChildren:
    def __bool__(self):
        return False

    def __iter__(self):
        yield {'x': 1}


class Probe(unittest.TestCase):
    def test_valid_falsey_iterable(self):
        self.assertEqual(PanelState('x', FalseyChildren()).snapshot()['children'], [{'x': 1}])


if __name__ == '__main__':
    unittest.main()
