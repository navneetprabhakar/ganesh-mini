import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "measurement/cuda/gcloud/20260823T152838Z"


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def test_l4_v3_result_is_sealed_failed_and_torn_down() -> None:
    result = json.loads((RUN / "run-result.json").read_text())
    claimed = result.pop("evidence_sha256")
    assert claimed == canonical_sha256(result)
    assert result["status"] == "failed-memory-capacity"
    assert result["claims"] == {
        "gate0b_passed": False,
        "optimizer_steps": 0,
        "training_records_started": 0,
        "training_complete": False,
    }
    assert result["primary"]["vision_cuda_bytes_released"] == 662833664
    assert result["fallback"]["vision_cuda_bytes_released"] == 190087680
    assert result["resource"]["compute_cost_upper_usd"] < 0.7
    assert all(result["teardown"][key] for key in (
        "instance_absent", "disk_absent", "subnet_absent", "network_absent"
    ))


def test_l4_v3_terminal_backup_and_absence_proofs_are_sealed() -> None:
    manifest = json.loads((RUN / "terminal-backup-manifest.json").read_text())
    manifest_claim = manifest.pop("evidence_sha256")
    assert manifest_claim == canonical_sha256(manifest)
    assert manifest["status"] == "verified"
    assert manifest["object_count"] == 32
    assert all(row["verified"] for row in manifest["objects"])

    absence = json.loads((RUN / "postdelete-absence-proof.json").read_text())
    absence_claim = absence.pop("evidence_sha256")
    assert absence_claim == canonical_sha256(absence)
    assert absence["status"] == "passed"
    assert [row["result_count"] for row in absence["queries"]] == [0, 0, 0, 0]


def test_3072_envelope_covers_every_prepared_record_without_truncation() -> None:
    observed_lanes = set()
    maximum = 0
    record_count = 0
    input_tokens = 0
    for name in ("prepared-train.jsonl", "prepared-validation.jsonl"):
        path = ROOT / "artifacts/train/seed-pilot" / name
        for line in path.read_text().splitlines():
            row = json.loads(line)
            length = len(row["input_ids"])
            assert length <= 3072
            maximum = max(maximum, length)
            observed_lanes.add(row["lane"])
            if name == "prepared-train.jsonl":
                record_count += 1
                input_tokens += length
    assert observed_lanes == {"go", "java", "javascript", "typescript", "python", "rust"}
    assert (record_count, input_tokens, maximum) == (2155, 636093, 2938)
