from __future__ import annotations

import unittest

from scripts.inference.extract import extract_code, split_channels


class ExtractionTests(unittest.TestCase):
    def test_prefers_matching_language_fence(self) -> None:
        raw = "Explanation\n```text\nignore\n```\n```python\ndef add(a,b): return a+b\n```<|im_end|>"
        code, metadata = extract_code(raw, "python")
        self.assertEqual("def add(a,b): return a+b\n", code)
        self.assertEqual("language_fence", metadata["strategy"])

    def test_first_fence_fallback_is_deterministic(self) -> None:
        code, metadata = extract_code("```\nexports.add=(a,b)=>a+b;\n```", "javascript")
        self.assertEqual("exports.add=(a,b)=>a+b;\n", code)
        self.assertEqual("first_fence", metadata["strategy"])

    def test_plain_final_and_thinking_are_separated(self) -> None:
        raw = "<think>private chain</think>\npub fn add(a:i32,b:i32)->i32 {a+b}<|im_end|>"
        channels = split_channels(raw)
        code, metadata = extract_code(raw, "rust")
        self.assertEqual("private chain", channels["reasoning"])
        self.assertNotIn("private chain", code)
        self.assertEqual("plain_final", metadata["strategy"])


if __name__ == "__main__":
    unittest.main()
