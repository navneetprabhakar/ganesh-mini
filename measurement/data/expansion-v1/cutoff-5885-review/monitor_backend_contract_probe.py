import unittest
from solution import MonitorAdapter


class MonitorContractProbe(unittest.TestCase):
    def test_backend_receives_missing_key_semantics_of_original_dictionary(self):
        class Backend:
            def initialize(self, config):
                self.config = config
        backend = Backend()
        MonitorAdapter(backend).initialize({})
        with self.assertRaises(KeyError):
            backend.config['nested']

    def test_close_is_called_at_most_once_even_if_it_raises(self):
        class Backend:
            calls = 0
            def close(self):
                self.calls += 1
                raise RuntimeError('close failed')
        backend = Backend()
        adapter = MonitorAdapter(backend)
        for _ in range(2):
            try:
                adapter.release()
            except RuntimeError:
                pass
        self.assertEqual(backend.calls, 1)


if __name__ == '__main__':
    unittest.main()
