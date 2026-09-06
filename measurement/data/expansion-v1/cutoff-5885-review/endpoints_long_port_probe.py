import unittest

from solution import check_endpoints


class LongPortTests(unittest.IsolatedAsyncioTestCase):
    async def test_oversized_port_is_unsuccessful_not_global_exception(self):
        called = []

        async def probe(candidate):
            called.append(candidate)
            return True

        result = await check_endpoints(["bad:" + "9" * 5000, "good:80"], probe)
        self.assertEqual(result, ["good:80"])
        self.assertEqual(called, ["good:80"])


if __name__ == "__main__":
    unittest.main()
