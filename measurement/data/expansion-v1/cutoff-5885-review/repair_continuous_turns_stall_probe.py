import signal
import unittest
from solution import continuous_turns


class Probe(unittest.TestCase):
    def test_finite_input_makes_progress(self):
        def expired(signum, frame):
            raise TimeoutError('two-second probe deadline')
        previous = signal.signal(signal.SIGALRM, expired)
        signal.setitimer(signal.ITIMER_REAL, 2)
        error = None
        try:
            result = continuous_turns([0.0, float(2**60)], 1.0)
        except Exception as exc:
            error = type(exc).__name__
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
        self.assertIsNone(error)
        self.assertEqual(result, [0.0, 0.0])


if __name__ == '__main__':
    unittest.main()
