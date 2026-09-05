"""Bind the user-approved cutoff to original executable candidates and review inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, validate_candidate
from scripts.data.build_expansion_quality_sample import build_sample, read_jsonl

CUTOFF_SHA = "3ca9209b51d36b9137d65f6f0424bfc369a662bd5af7f99666f4ecc60ee24e92"
CUTOFF_COUNTS = {
    "go": {"generation": 627, "repair": 458},
    "java": {"generation": 720, "repair": 480},
    "javascript": {"generation": 360, "repair": 240},
    "typescript": {"generation": 360, "repair": 240},
    "python": {"generation": 720, "repair": 480},
    "rust": {"generation": 720, "repair": 480},
}


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def matches(row: dict, candidate: dict) -> bool:
    return (
        candidate.get("id") == row["id"]
        and candidate.get("lane") == row["lane"]
        and candidate.get("task_type") == row["task_type"]
        and candidate.get("messages") == row["messages"]
        and candidate.get("source") == row["lineage"]
        and candidate.get("rights") == row["rights"]
        and digest(canonical_json(candidate.get("verification_task"))) == row["verification"]["task_sha256"]
    )


def assemble(rows: list[dict], paths: list[Path], config: dict) -> tuple[list[dict], list[dict]]:
    wanted = {r["id"]: r for r in rows}
    if len(wanted) != len(rows):
        raise ValueError("duplicate corpus ID")
    found, origins = {}, {}
    for path in sorted(paths):
        payload = path.read_bytes()
        for line, candidate in enumerate(read_jsonl(path), 1):
            identifier = candidate.get("id")
            if identifier not in wanted or not matches(wanted[identifier], candidate):
                continue
            validate_candidate(candidate, config)
            if identifier in found and found[identifier] != candidate:
                raise ValueError(f"ambiguous candidate identity: {identifier}")
            if identifier not in found:
                found[identifier] = candidate
                origins[identifier] = {"id": identifier, "path": str(path), "line": line,
                                       "file_sha256": digest(payload),
                                       "candidate_sha256": digest(canonical_json(candidate))}
    missing = sorted(wanted.keys() - found.keys())
    if missing:
        raise ValueError(f"missing exact executable candidates: {missing[:10]} ({len(missing)} total)")
    return [found[r["id"]] for r in rows], [origins[r["id"]] for r in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError("cutoff output directory already exists; preserve existing evidence")
    cache = Path("datasets/cache/expansion-v1")
    corpus = cache / "production/admitted.jsonl"
    state_path = cache / "production/state.json"
    payload = corpus.read_bytes()
    state = json.loads(state_path.read_text())
    rows = read_jsonl(corpus)
    actual = Counter((r["lane"], r["task_type"]) for r in rows)
    expected = {(lane, task): n for lane, tasks in CUTOFF_COUNTS.items() for task, n in tasks.items()}
    if digest(payload) != CUTOFF_SHA or state["corpus_sha256"] != CUTOFF_SHA:
        raise ValueError("corpus differs from user-approved cutoff")
    if dict(actual) != expected or state["counts"] != CUTOFF_COUNTS or state["aggregation_rejections"]:
        raise ValueError("cutoff count/integrity mismatch")
    config_path = Path("configs/data/expansion_v1.json")
    config = json.loads(config_path.read_text())
    candidates, origins = assemble(rows, list(cache.rglob("*candidates.jsonl")), config)
    config["target_records"] = len(rows)
    config["lane_targets"] = {lane: sum(tasks.values()) for lane, tasks in CUTOFF_COUNTS.items()}
    config["task_type_targets"] = dict(Counter(r["task_type"] for r in rows))
    selected, review = build_sample(rows, CUTOFF_SHA, 300)
    by_id = {r["id"]: r for r in candidates}
    sample = [by_id[r["id"]] for r in selected]
    files = {
        "admitted.snapshot.jsonl": payload,
        "production-state.snapshot.json": state_path.read_bytes(),
        "final.candidates.jsonl": b"".join(canonical_json(r) + b"\n" for r in candidates),
        "quality-sample.candidates.jsonl": b"".join(canonical_json(r) + b"\n" for r in sample),
        "cutoff.config.json": json.dumps(config, indent=2, sort_keys=True).encode() + b"\n",
    }
    review["sample_sha256"] = digest(files["quality-sample.candidates.jsonl"])
    review["sample_format"] = "original executable candidates matched to admitted corpus"
    review["report_sha256"] = digest(canonical_json(review))
    files["quality-review.json"] = json.dumps(review, indent=2, sort_keys=True).encode() + b"\n"
    manifest = {
        "schema_version": "ganesh-mini-expansion-cutoff/v1",
        "authorization": "Navneet approved stopping at 5,885 admitted rows on 2026-09-05 and proceeding to validation",
        "status": "prepared-pending-final-execution-and-quality-review",
        "corpus_sha256": CUTOFF_SHA, "counts": CUTOFF_COUNTS,
        "original_config_sha256": digest(config_path.read_bytes()),
        "excluded_unfinished_batches": [b.get("name") for b in state["batches"] if b.get("status") in {"running", "failed"}],
        "files": {name: {"sha256": digest(data), "bytes": len(data)} for name, data in files.items()},
        "candidate_origins": origins,
        "training_balance": "20% supervised-token objective per product family; no row duplication",
    }
    manifest["manifest_sha256"] = digest(canonical_json(manifest))
    files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    args.output_dir.mkdir(parents=True)
    for name, data in files.items():
        (args.output_dir / name).write_bytes(data)
    print(json.dumps({"status": manifest["status"], "rows": len(rows), "sample": len(sample),
                      "manifest_sha256": manifest["manifest_sha256"]}))


if __name__ == "__main__":
    main()
