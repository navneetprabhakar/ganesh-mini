import unittest
from solution import PartsCounter


class SharedEntryProbe(unittest.TestCase):
    def test_valid_shared_input_entries_do_not_cross_debit_parts(self):
        entry = {'unit_cost': 1, 'available': 1}
        counter = PartsCounter({'a': entry, 'b': entry})
        counter.set_quantity('a', 1)
        counter.set_quantity('b', 1)
        result = counter.commit()
        self.assertEqual(result['items'], {'a': 1, 'b': 1})
        self.assertEqual(counter.item('a')['available'], 0)
        self.assertEqual(counter.item('b')['available'], 0)
        self.assertEqual(entry['available'], 1)


if __name__ == '__main__':
    unittest.main()
