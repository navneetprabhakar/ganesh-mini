import unittest
from solution import select_runtime_commands


class Text(str):
    pass


class Probe(unittest.TestCase):
    def test_finite_metadata(self):
        value = []
        for _ in range(600):
            value = [value]
        command = Text('run')
        command.metadata = value
        error = None
        try:
            select_runtime_commands([{'command': command, 'runtime': 'py', 'enabled': True}], 'PY')
        except Exception as exc:
            error = type(exc).__name__
        self.assertIsNone(error)


if __name__ == '__main__':
    unittest.main()
