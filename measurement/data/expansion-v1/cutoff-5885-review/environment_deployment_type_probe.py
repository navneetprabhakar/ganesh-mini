import unittest
from solution import build_environment


class EnvironmentDeploymentTypeTests(unittest.TestCase):
    def test_malformed_deployment_raises_value_error_before_loader(self):
        calls = []
        config = dict(view_root='v', deployment=[], diagnostics={}, datastore={}, route_modules=[])
        with self.assertRaises(ValueError):
            build_environment(config, lambda names: calls.append(names) or [])
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
