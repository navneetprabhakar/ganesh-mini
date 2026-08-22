import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[2] / "scripts" / "data" / "import_ganesh_v01_seed.py"
SPEC = importlib.util.spec_from_file_location("seed_import", SCRIPT)
seed_import = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(seed_import)


def source_record(record_id="record-1"):
    return {
        "id": record_id,
        "source_record_id": record_id,
        "language": "Python",
        "task_type": "code_generation",
        "messages": [
            {"role": "user", "content": "Write f()."},
            {"role": "assistant", "content": "def f():\n    return 1\n"},
        ],
        "teacher_model": "test",
    }


class SeedImportTests(unittest.TestCase):
    def test_normalization_preserves_messages_and_metadata(self):
        original = source_record()
        normalized = seed_import.normalize_record(
            original,
            lane="python",
            split="train",
            source_path="train.jsonl",
            source_revision="abc",
            source_file_sha256="file-hash",
            line_number=1,
            raw_line=b"source bytes",
        )
        self.assertEqual(normalized["messages"], original["messages"])
        self.assertEqual(normalized["source_metadata"], {"teacher_model": "test"})
        self.assertEqual(normalized["lineage"]["source_record_id"], "record-1")
        self.assertEqual(normalized["lineage"]["source_record_sha256"], seed_import.sha256(b"source bytes"))

    def test_invalid_message_contract_fails_closed(self):
        original = source_record()
        original["messages"].reverse()
        with self.assertRaises(seed_import.ImportFailure):
            seed_import.normalize_record(
                original,
                lane="python",
                split="train",
                source_path="train.jsonl",
                source_revision="abc",
                source_file_sha256="hash",
                line_number=1,
                raw_line=b"source",
            )

    def test_invalid_declared_content_hash_fails_closed(self):
        original = source_record()
        original["prompt_sha256"] = "0" * 64
        with self.assertRaises(seed_import.ImportFailure):
            seed_import.normalize_record(
                original,
                lane="python",
                split="train",
                source_path="train.jsonl",
                source_revision="abc",
                source_file_sha256="hash",
                line_number=1,
                raw_line=b"source",
            )

    def test_import_is_deterministic_and_detects_evaluation_overlap(self):
        blob = seed_import.canonical_json(source_record())
        config = {
            "source": {"repository": "/does/not/matter", "revision": "abc"},
            "sources": [{
                "lane": "python", "split": "train", "path": "train.jsonl",
                "records": 1, "sha256": seed_import.sha256(blob),
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            with mock.patch.object(seed_import, "git_blob", return_value=blob):
                first = seed_import.run_import(config_path, root / "out", root / "manifest.json")
                payload_1 = (root / "out" / "train.jsonl").read_bytes()
                second = seed_import.run_import(config_path, root / "out", root / "manifest.json")
                payload_2 = (root / "out" / "train.jsonl").read_bytes()
                self.assertEqual(payload_1, payload_2)
                self.assertEqual(first["outputs"], second["outputs"])

                evaluation = root / "evaluation.jsonl"
                evaluation.write_text(json.dumps({"prompt": "  WRITE  f(). "}) + "\n", encoding="utf-8")
                with self.assertRaises(seed_import.ImportFailure):
                    seed_import.run_import(config_path, root / "out", root / "manifest.json", [evaluation])

    def test_duplicate_ids_fail_closed(self):
        records = [source_record(), source_record()]
        report = seed_import.duplicate_report([
            seed_import.normalize_record(
                record, lane="python", split="train", source_path="train.jsonl",
                source_revision="abc", source_file_sha256="hash", line_number=index,
                raw_line=seed_import.canonical_json(record).rstrip(b"\n"),
            )
            for index, record in enumerate(records, 1)
        ])
        self.assertEqual(len(report["record_id"]), 1)


if __name__ == "__main__":
    unittest.main()
