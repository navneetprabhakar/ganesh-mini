import unittest
from solution import update_registry

class RegistryIdProbe(unittest.TestCase):
    def test_unhashable_change_remove_ids_raise_value_error(self):
        for action in ['change', 'remove']:
            operation = {'action': action, 'id': []}
            if action == 'change':
                operation['label'] = 'X'
            with self.subTest(action=action), self.assertRaises(ValueError):
                update_registry([], [operation])

if __name__ == '__main__':
    unittest.main()
