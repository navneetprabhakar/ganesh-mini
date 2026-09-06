import unittest
from solution import VentilationMonitor


class MonitorIntegerTests(unittest.TestCase):
    def test_finite_integer_temperature(self):
        monitor = VentilationMonitor(20, 50)
        result = monitor.observe({"temperature": 10 ** 400, "humidity": 0})
        self.assertTrue(result["fan_on"])


if __name__ == "__main__":
    unittest.main()
