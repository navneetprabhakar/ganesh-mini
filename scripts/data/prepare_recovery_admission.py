"""Prepare an explicit quality-positive recovery selection without sealing training."""

import argparse
import json
import re
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, normalized_sha256, simhash, _tokens, read_jsonl
from scripts.data.generate_versioned_recovery import ROOT, persist
from scripts.data.plan_versioned_recovery import digest
from scripts.data.reconcile_sample_criteria import EXPECTED_SHA

HISTORICAL_HOLDS = {"exp-v1-go-generation-0165", "exp-v1-rust-generation-0161", "exp-v1-rust-generation-0224"}


def check_overlap(candidates, retained, limit=3, minimum_tokens=12):
    seen = [(row["id"], normalized_sha256(row["messages"][0]["content"]),
             simhash(row["messages"][0]["content"]), len(_tokens(row["messages"][0]["content"]))) for row in retained]
    matches = []
    for row in candidates:
        text = row["messages"][0]["content"]
        exact, fuzzy, length = normalized_sha256(text), simhash(text), len(_tokens(text))
        for id, other_exact, other_fuzzy, other_length in seen:
            if exact == other_exact or (min(length, other_length) >= minimum_tokens and (fuzzy ^ other_fuzzy).bit_count() <= limit):
                matches.append({"id": row["id"], "overlap_id": id, "exact": exact == other_exact})
        seen.append((row["id"], exact, fuzzy, length))
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    selected = json.loads(args.selection.read_text())
    if not selected or len({row["id"] for row in selected}) != len(selected):
        raise ValueError("explicit unique nonempty selection required")
    original = ROOT / "datasets/cache/expansion-v1/cutoff-5885/final.candidates.jsonl"
    holds = ROOT / "measurement/data/expansion-v1/cutoff-5885-review/additional-holds.json"
    if digest(original.read_bytes()) != EXPECTED_SHA:
        raise ValueError("original corpus changed")
    held = HISTORICAL_HOLDS | {row["id"] for row in json.loads(holds.read_text())["holds"]}
    originals = read_jsonl(original)
    parents = {row["id"]: row for row in originals}
    candidates = []
    for item in selected:
        if item["quality_decision"] != "main-accepted-seven-criterion-positive":
            raise ValueError("main quality decision required")
        for field in ("candidate", "review", "diagnostic"):
            path = (ROOT / item[field]).resolve()
            if not path.is_relative_to(ROOT) or digest(path.read_bytes()) != item[field + "_sha256"]:
                raise ValueError("selection evidence changed")
        candidate = json.loads((ROOT / item["candidate"]).read_text())
        diagnostic = json.loads((ROOT / item["diagnostic"]).read_text())
        if candidate["id"] != item["id"] or diagnostic["id"] != item["id"] or not diagnostic["directionality_passed"]:
            raise ValueError("candidate lacks exact passing directionality")
        if item["parent_id"] not in held:
            raise ValueError("recovery parent must remain held")
        if re.sub(r"^exp-v1-recovery-r[1-9][0-9]*-", "exp-v1-", candidate["id"]) != item["parent_id"]:
            raise ValueError("selected parent identity mismatch")
        parent = parents[item["parent_id"]]
        expected_source = dict(parent["source"])
        expected_source["transformation"] += f"; versioned recovery {candidate['id']} from {parent['id']} sha256={digest(canonical_json(parent))}"
        if candidate["source"] != expected_source or candidate["rights"] != parent["rights"]:
            raise ValueError("selected parent lineage mismatch")
        reference_evidence = json.loads((ROOT / item["diagnostic"]).with_name(candidate["id"] + "-reference.json").read_text())
        if reference_evidence["candidate_sha256"] != digest(canonical_json(candidate)) or reference_evidence["outcome"] != "passed":
            raise ValueError("reference diagnostic does not bind this candidate")
        candidates.append(candidate)
    retained = [row for row in originals if row["id"] not in held]
    config = json.loads((ROOT / "configs/data/expansion_v1.json").read_text())
    overlaps = check_overlap(candidates, retained,
        config["deduplication"]["prompt_simhash_max_hamming"], config["deduplication"]["minimum_fuzzy_tokens"])
    args.output_dir.mkdir(parents=True, exist_ok=False)
    report = {"status": "overlap-blocked" if overlaps else "prepared-not-admitted",
        "selection_sha256": digest(args.selection.read_bytes()), "original_sha256": EXPECTED_SHA,
        "holds_sha256": digest(holds.read_bytes()), "retained_originals_compared": len(retained),
        "selected": selected, "overlaps": overlaps, "evaluation_separation": "required-by-admit-expansion-next"}
    persist(args.output_dir / "preparation.json", report)
    if overlaps:
        raise ValueError("recovery overlaps retained originals or another selected recovery")
    with (args.output_dir / "candidates.jsonl").open("xb") as handle:
        for row in candidates:
            handle.write(canonical_json(row) + b"\n")
    print(json.dumps({"prepared": len(candidates), "retained_compared": len(retained), "admitted": False}))


if __name__ == "__main__":
    main()
