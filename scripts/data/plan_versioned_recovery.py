"""Prepare immutable, parent-bound recovery requests; never generate or admit data."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

from scripts.data.admit_expansion import canonical_json
from scripts.data.reconcile_sample_criteria import EXPECTED_SHA


CHANGE_CLASSES = {"reference-fix", "contract-clarification", "oracle-rebuild"}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def make_plan(candidate_bytes: bytes, hold_bytes: bytes, request_bytes: bytes) -> dict:
    """Bind explicit reviewed selections. No inference from hold reason keywords."""
    request = json.loads(request_bytes)
    if request["parent_corpus_sha256"] != digest(candidate_bytes):
        raise ValueError("parent corpus hash mismatch")
    if request["hold_ledger_sha256"] != digest(hold_bytes):
        raise ValueError("hold ledger hash mismatch")
    version = request["version"]
    if not isinstance(version, str) or not re.fullmatch(r"r[1-9][0-9]*", version):
        raise ValueError("version must be r followed by a positive integer")
    rows = [json.loads(line) for line in candidate_bytes.splitlines() if line.strip()]
    by_id = {row["id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("duplicate parent candidate identity")
    holds = json.loads(hold_bytes)["holds"]
    held = {row["id"]: row for row in holds}
    if len(held) != len(holds):
        raise ValueError("duplicate hold identity")
    selections = request["selections"]
    if not isinstance(selections, list) or not selections:
        raise ValueError("explicit nonempty selections required")
    planned, seen = [], set()
    for selection in selections:
        parent_id = selection["parent_id"]
        if parent_id in seen:
            raise ValueError("duplicate recovery selection")
        seen.add(parent_id)
        if parent_id not in by_id or parent_id not in held:
            raise ValueError("selected parent must exist and be held")
        parent = by_id[parent_id]
        parent_sha = digest(canonical_json(parent))
        if selection["parent_candidate_sha256"] != parent_sha:
            raise ValueError("parent candidate hash mismatch")
        if selection["change_class"] not in CHANGE_CLASSES:
            raise ValueError("unsupported change class; trivial padding is not recovery")
        for field in ("rationale", "review_evidence"):
            if not isinstance(selection[field], str) or not selection[field].strip():
                raise ValueError("nonempty rationale and review evidence required")
        evidence_sha = selection.get("review_evidence_sha256", "")
        if not isinstance(evidence_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", evidence_sha):
            raise ValueError("review evidence content hash required")
        if not re.fullmatch(r"exp-v1-(go|java|javascript|typescript|python|rust)-(generation|repair)-[0-9]+", parent_id):
            raise ValueError("unexpected parent identity format")
        derived_id = parent_id.replace("exp-v1-", f"exp-v1-recovery-{version}-", 1)
        if derived_id in by_id:
            raise ValueError("derived identity collides with parent corpus")
        if not all(parent["rights"].get(key) is True for key in
                   ("prompt", "answer", "tests", "redistribution", "model_training")):
            raise ValueError("parent rights do not permit recovery and publication")
        planned.append({
            "id": derived_id, "parent_id": parent_id,
            "parent_candidate_sha256": parent_sha,
            "parent_source": copy.deepcopy(parent["source"]),
            "parent_rights": copy.deepcopy(parent["rights"]),
            "parent_hold": copy.deepcopy(held[parent_id]),
            "lane": parent["lane"], "task_type": parent["task_type"],
            "change_class": selection["change_class"],
            "rationale": selection["rationale"],
            "review_evidence": selection["review_evidence"],
            "review_evidence_sha256": evidence_sha,
            "status": "planned-not-generated-not-admitted",
        })
    plan = {
        "schema_version": "ganesh-mini-versioned-recovery-plan/v1",
        "status": "plan-only-not-quality-seal", "version": version,
        "parent_corpus_sha256": digest(candidate_bytes),
        "hold_ledger_sha256": digest(hold_bytes),
        "request_sha256": digest(request_bytes),
        "required_next_gates": [
            "complete original systematic-quality reconciliation before selection approval",
            "new derived specification/reference/known-bad with immutable teacher evidence",
            "independent tests see only derived ID and specification, never parent tests or answers",
            "fresh pinned sandbox reference pass and all known-bad failures",
            "evaluation separation and deduplication including retained originals",
            "independent quality review, corpus sufficiency and family-token balance",
            "separate admission seal",
        ],
        "records": planned,
    }
    plan["plan_sha256"] = digest(canonical_json(plan))
    return plan


def validate_review_evidence(plan: dict, root: Path) -> None:
    for record in plan["records"]:
        path = (root / record["review_evidence"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError("review evidence must be an existing repository file")
        if digest(path.read_bytes()) != record["review_evidence_sha256"]:
            raise ValueError("review evidence content changed")


def write_plan(output_dir: Path, plan: dict) -> None:
    """Reserve a fresh directory; never reuse an old or partially written run."""
    output_dir.mkdir(parents=True, exist_ok=False)
    with (output_dir / "plan.json").open("x", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--holds", type=Path, required=True)
    parser.add_argument("--requests", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    candidates = args.input.read_bytes()
    if digest(candidates) != EXPECTED_SHA:
        raise ValueError("only the frozen cutoff5885 corpus is supported")
    plan = make_plan(candidates, args.holds.read_bytes(), args.requests.read_bytes())
    validate_review_evidence(plan, Path(__file__).resolve().parents[2])
    write_plan(args.output_dir, plan)
    print(json.dumps({"planned": len(plan["records"]), "plan_sha256": plan["plan_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
