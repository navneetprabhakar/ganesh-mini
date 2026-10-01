#!/usr/bin/env python3
"""Build the deterministic, training-only V4 production tooling fixture bundle."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_expansion import canonical_json  # noqa: E402
from scripts.data.admit_repair_delta import (  # noqa: E402
    CANONICAL_TEST_PATHS,
    V4_CONTRACT_ID,
    V4_ENVELOPE_SCHEMA,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256  # noqa: E402
from scripts.data.repair_delta_v4_preflight import (  # noqa: E402
    PLAN_SHA256,
    PROOF_SCHEMA,
    WITNESS_SCHEMA,
    load_preflight_config,
)
from scripts.data.run_repair_delta_evidence import seal  # noqa: E402
from scripts.eval.contracts import LANGUAGE_FAMILY, sha256_text  # noqa: E402


SCHEMA = "ganesh-mini-v4-tooling-fixture-bundle/v1"
SEPARATION_CONTRACT_SHA256 = "9" * 64
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
FAMILY_DATASETS = {
    "mceval": "Multilingual-Multimodal-NLP/McEval-Instruct",
    "mdeval": "m-a-p/MdEval-Instruct",
    "commitpackft": "bigcode/commitpackft",
}
FAMILY_BY_LANE = {
    "go": "commitpackft", "java": "mceval", "javascript": "mdeval",
    "typescript": "mceval", "python": "commitpackft", "rust": "mdeval",
}
RUNTIME_IDS = {
    "go": "go-1.22.12", "java": "java-21.0.11",
    "javascript": "javascript-node-22.23.2",
    "typescript": "typescript-5.5.4-node-22", "python": "python-3.11.15",
    "rust": "rust-1.85.0",
}
CANDIDATE_PATHS = {
    "go": "solution.go", "java": "Solution.java", "javascript": "solution.js",
    "typescript": "solution.ts", "python": "solution.py", "rust": "solution.rs",
}
LOGICAL_PATHS = {
    "go": ("primary_test.go", "cross_test.go"),
    "java": ("PrimaryTest.java", "CrossTest.java"),
    "javascript": ("primary.test.js", "cross.test.js"),
    "typescript": ("primary.test.ts", "cross.test.ts"),
    "python": ("test_primary.py", "test_cross.py"),
    "rust": ("primary_test.rs", "cross_test.rs"),
}


def _programs(marker: str) -> dict[str, dict[str, str]]:
    return {
        "go": {
            "reference": '''package solution

import "errors"

func ComputeTotal(values []int) (int, error) {
	if len(values) == 0 { return 0, errors.New("values must not be empty") }
	total := 0
	for _, value := range values { total += value }
	return total, nil
}
''',
            "known_bad": '''package solution

import "errors"

func ComputeTotal(values []int) (int, error) {
	if len(values) == 0 { return 0, errors.New("values must not be empty") }
	maximum := values[0]
	for _, value := range values[1:] { if value > maximum { maximum = value } }
	return maximum, nil
}
''',
            "primary": '''package solution

import "testing"

func TestPrimaryCases(t *testing.T) {
	for _, tc := range []struct{ values []int; want int }{
		{[]int{2, 3}, 5}, {[]int{-4, 3, 2}, 1},
	} {
		got, err := ComputeTotal(tc.values)
		if err != nil || got != tc.want { t.Fatalf("got %d, %v; want %d", got, err, tc.want) }
	}
}
''',
            "cross": '''package solution

import "testing"

func TestMalformedEmpty(t *testing.T) {
	if _, err := ComputeTotal([]int{}); err == nil { t.Fatal("empty input must be rejected") }
}
''',
            "witness": f'''package solution

import (
	"fmt"
	"testing"
)

func TestKnownBadCrossWitness(t *testing.T) {{
	if _, err := ComputeTotal([]int{{}}); err == nil {{ t.Fatal("empty input must be rejected") }}
	fmt.Println("{marker}")
}}
''',
            "support_path": "go.mod", "support": "module ganeshfixture\n\ngo 1.22\n",
        },
        "java": {
            "reference": '''public final class Solution {
    public static int computeTotal(int[] values) {
        if (values == null || values.length == 0) throw new IllegalArgumentException("values required");
        int total = 0;
        for (int value : values) total += value;
        return total;
    }
}
''',
            "known_bad": '''public final class Solution {
    public static int computeTotal(int[] values) {
        if (values == null || values.length == 0) throw new IllegalArgumentException("values required");
        int maximum = values[0];
        for (int value : values) maximum = Math.max(maximum, value);
        return maximum;
    }
}
''',
            "primary": '''public final class SolutionTest {
    public static void main(String[] args) {
        if (Solution.computeTotal(new int[]{2, 3}) != 5) throw new AssertionError("positive sum");
        if (Solution.computeTotal(new int[]{-4, 3, 2}) != 1) throw new AssertionError("signed sum");
    }
}
''',
            "cross": '''public final class SolutionTest {
    public static void main(String[] args) {
        try { Solution.computeTotal(new int[]{}); throw new AssertionError("empty input accepted"); }
        catch (IllegalArgumentException expected) { }
    }
}
''',
            "witness": f'''public final class CrossWitness {{
    public static void main(String[] args) {{
        try {{ Solution.computeTotal(new int[]{{}}); throw new AssertionError("empty input accepted"); }}
        catch (IllegalArgumentException expected) {{ }}
        System.out.println("{marker}");
    }}
}}
''',
        },
        "javascript": {
            "reference": '''"use strict";
function computeTotal(values) {
  if (!Array.isArray(values) || values.length === 0) throw new TypeError("values required");
  return values.reduce((total, value) => total + value, 0);
}
module.exports = { computeTotal };
''',
            "known_bad": '''"use strict";
function computeTotal(values) {
  if (!Array.isArray(values) || values.length === 0) throw new TypeError("values required");
  return Math.max(...values);
}
module.exports = { computeTotal };
''',
            "primary": '''"use strict";
const assert = require("assert");
const { computeTotal } = require("./solution");
assert.strictEqual(computeTotal([2, 3]), 5);
assert.strictEqual(computeTotal([-4, 3, 2]), 1);
''',
            "cross": '''"use strict";
const assert = require("assert");
const { computeTotal } = require("./solution");
assert.throws(() => computeTotal([]), TypeError);
''',
            "witness": f'''"use strict";
const assert = require("assert");
const {{ computeTotal }} = require("./solution");
assert.throws(() => computeTotal([]), TypeError);
console.log("{marker}");
''',
        },
        "typescript": {
            "reference": '''export function computeTotal(values: number[]): number {
  if (!Array.isArray(values) || values.length === 0) throw new TypeError("values required");
  return values.reduce((total, value) => total + value, 0);
}
''',
            "known_bad": '''export function computeTotal(values: number[]): number {
  if (!Array.isArray(values) || values.length === 0) throw new TypeError("values required");
  return Math.max(...values);
}
''',
            "primary": '''import { computeTotal } from "./solution";
function equal(actual: number, expected: number): void { if (actual !== expected) throw new Error(`${actual} != ${expected}`); }
equal(computeTotal([2, 3]), 5);
equal(computeTotal([-4, 3, 2]), 1);
''',
            "cross": '''import { computeTotal } from "./solution";
let rejected = false;
try { computeTotal([]); } catch (error) { rejected = error instanceof TypeError; }
if (!rejected) throw new Error("empty input must be rejected");
''',
            "witness": f'''import {{ computeTotal }} from "./solution";
let rejected = false;
try {{ computeTotal([]); }} catch (error) {{ rejected = error instanceof TypeError; }}
if (!rejected) throw new Error("empty input must be rejected");
console.log("{marker}");
''',
        },
        "python": {
            "reference": '''def compute_total(values):
    if not isinstance(values, list) or not values:
        raise ValueError("values required")
    return sum(values)
''',
            "known_bad": '''def compute_total(values):
    if not isinstance(values, list) or not values:
        raise ValueError("values required")
    return max(values)
''',
            "primary": '''from solution import compute_total
assert compute_total([2, 3]) == 5
assert compute_total([-4, 3, 2]) == 1
''',
            "cross": '''from solution import compute_total
try:
    compute_total([])
except ValueError:
    pass
else:
    raise AssertionError("empty input must be rejected")
''',
            "witness": f'''from solution import compute_total
try:
    compute_total([])
except ValueError:
    pass
else:
    raise AssertionError("empty input must be rejected")
print("{marker}")
''',
        },
        "rust": {
            "reference": '''pub fn compute_total(values: &[i32]) -> Result<i32, &'static str> {
    if values.is_empty() { return Err("values required"); }
    Ok(values.iter().sum())
}
''',
            "known_bad": '''pub fn compute_total(values: &[i32]) -> Result<i32, &'static str> {
    if values.is_empty() { return Err("values required"); }
    Ok(*values.iter().max().unwrap())
}
''',
            "primary": '''mod solution;
#[test]
fn primary_cases() {
    assert_eq!(solution::compute_total(&[2, 3]), Ok(5));
    assert_eq!(solution::compute_total(&[-4, 3, 2]), Ok(1));
}
''',
            "cross": '''mod solution;
#[test]
fn malformed_empty() { assert!(solution::compute_total(&[]).is_err()); }
''',
            "witness": f'''mod solution;
#[test]
fn known_bad_cross_witness() {{
    assert!(solution::compute_total(&[]).is_err());
    println!("{marker}");
}}
''',
        },
    }


def _source(lane: str, family: str, index: int, admission_config: dict[str, Any]) -> dict[str, Any]:
    if family != "commitpackft":
        configured = admission_config["sources"][FAMILY_DATASETS[family]]
        uri = (
            "https://huggingface.co/datasets/Multilingual-Multimodal-NLP/McEval-Instruct"
            if family == "mceval" else "https://huggingface.co/datasets/m-a-p/MdEval-Instruct"
        )
        license_uri = (
            "https://creativecommons.org/licenses/by-sa/4.0/"
            if configured["license"] == "CC-BY-SA-4.0" else "https://opensource.org/license/mit/"
        )
        return {
            "dataset": FAMILY_DATASETS[family], "uri": uri,
            "revision": configured["revision"], "record_id": f"tooling-fixture-{lane}-{index}",
            "license": configured["license"], "license_uri": license_uri,
            "source_record_sha256": f"{index + 1:x}" * 64,
            "transformation": "deterministic training-only V4 tooling fixture",
        }
    configured = admission_config["sources"][FAMILY_DATASETS[family]]
    source_file = f"data/{lane}/data.jsonl"
    pinned = configured["source_files"][source_file]
    return {
        "dataset": FAMILY_DATASETS[family], "uri": configured["uri"],
        "revision": configured["revision"],
        "record_id": f"{source_file}:line-{index + 1:08d}", "license": "MIT",
        "license_uri": "https://opensource.org/license/mit/",
        "source_record_sha256": f"{index + 1:x}" * 64,
        "transformation": "native CommitPackFT fixture; new_contents quarantined",
        "source_file": source_file, "source_file_sha256": pinned["sha256"],
        "source_file_bytes": pinned["bytes"], "raw_line_sha256": "1" * 64,
        "commit": "2" * 40, "old_file": f"src/old.{lane}",
        "new_file": f"src/new.{lane}", "repositories_raw": "owner/repository",
        "repositories": ["owner/repository"], "subject_sha256": "3" * 64,
        "message_sha256": "4" * 64, "old_contents_sha256": "5" * 64,
        "quarantined_record_sha256": "6" * 64, "selection_rank": index + 1,
    }


def _candidate(
    lane: str, family: str, index: int, program: dict[str, str], admission_config: dict[str, Any],
) -> dict[str, Any]:
    identifier = f"v4-tooling-fixture-{lane}"
    prompt = f"Repair compute_total in {lane} so it sums signed integers and rejects empty input."
    primary_path, cross_path = LOGICAL_PATHS[lane]
    files = []
    if lane == "go":
        support = program["support"]
        files.append({"path": program["support_path"], "role": "support", "content": support, "sha256": sha256_text(support)})
    for path, content in ((primary_path, program["primary"]), (cross_path, program["cross"])):
        files.append({"path": path, "role": "test", "content": content, "sha256": sha256_text(content)})
    reference = program["reference"]
    known_bad = program["known_bad"]
    task = {
        "schema_version": "1.0", "task_id": identifier, "surface": "training_admission",
        "language": lane, "family": LANGUAGE_FAMILY[lane], "task_type": "repair",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": CANDIDATE_PATHS[lane], "files": files,
        "runtime_id": RUNTIME_IDS[lane],
        "limits": {
            "timeout_seconds": 120 if lane == "go" else 30,
            "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536,
        },
        "validation": {
            "reference": {"label": "reference", "code": reference, "sha256": sha256_text(reference)},
            "known_bad": [{"label": "selects maximum rather than summing", "code": known_bad, "sha256": sha256_text(known_bad)}],
        },
    }
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": identifier,
        "lane": lane, "task_type": "repair",
        "messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": reference}],
        "source": _source(lane, family, index, admission_config),
        "rights": {name: True for name in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "verification_task": task, "test_origin": "independent_author",
    }


def _envelope(
    lane: str, family: str, index: int, program: dict[str, str], admission_config: dict[str, Any],
    witness_path: str,
) -> dict[str, Any]:
    candidate = _candidate(lane, family, index, program, admission_config)
    task = candidate["verification_task"]
    candidate_sha = canonical_sha256(candidate)
    pretest = copy.deepcopy(candidate)
    pretest["verification_task"]["files"] = [item for item in task["files"] if item["role"] == "support"]
    specification_sha = sha256_text(candidate["messages"][0]["content"])
    known_bad_sha = task["validation"]["known_bad"][0]["sha256"]
    reference_sha = task["validation"]["reference"]["sha256"]
    tests = {item["path"]: item for item in task["files"] if item["role"] == "test"}
    primary_path, cross_path = LOGICAL_PATHS[lane]
    proof = seal({
        "schema_version": PROOF_SCHEMA, "candidate_id": candidate["id"],
        "teacher_candidate_sha256": canonical_sha256(pretest), "queue_record_sha256": "7" * 64,
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "capability_operation": "aggregate all signed integer values",
        "defective_intermediate_or_decision": "selects the maximum rather than accumulating",
        "valid_domain_counterexample": "[2, 3] must produce 5 rather than 3",
        "minimal_capability_specific_patch": "replace maximum selection with signed accumulation",
        "scheduled_dimension_obligation": "reject empty input",
        "known_bad_already_satisfies_scheduled_dimension": True,
        "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True,
        "known_bad_cross_witness": {
            "schema_version": WITNESS_SCHEMA, "valid_domain_input": "empty input collection",
            "scheduled_dimension_assertion": "both implementations reject empty input",
            "path": witness_path, "content": program["witness"],
            "content_sha256": sha256_text(program["witness"]), "valid_domain": True,
            "scheduled_dimension_only": True,
        },
        "teacher_run_evidence_sha256": "8" * 64,
        "visibility": {"source_affinity_card": True, "source_lineage": True, "runtime_contract": True, "evaluation_artifacts_read": 0},
    })
    semantic = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "known_bad_sha256": known_bad_sha, "primary_capability": "numeric_reasoning",
        "assigned_cross_cutting_dimension": "malformed_input",
        "repair_delta_requires_primary_capability": True, "scheduled_dimension_is_concrete_and_secondary": True,
        "known_bad_already_satisfies_scheduled_dimension": True, "cross_dimension_only_patch_cannot_solve": True,
        "capability_remains_substantive_without_cross_clause": True, "generic_boilerplate_is_not_primary": True,
        "visibility": {"specification_visible": True, "embedded_known_bad_visible": True, "assigned_labels_visible": True, "teacher_proof_visible": False, "reference_visible": False, "tests_visible": False, "verifier_outputs_visible": False, "training_stimulus_visible": False, "source_dataset_visible": False, "v2_outcomes_visible": False, "evaluation_artifacts_read": 0},
    })
    roles = [
        {"path": primary_path, "canonical_path": CANONICAL_TEST_PATHS[lane], "file_sha256": tests[primary_path]["sha256"], "role": "primary_discrimination", "case_ids": [f"{lane}-positive", f"{lane}-signed"], "valid_domain_only": True, "scheduled_dimension_only": False},
        {"path": cross_path, "canonical_path": CANONICAL_TEST_PATHS[lane], "file_sha256": tests[cross_path]["sha256"], "role": "cross_cutting", "case_ids": [f"{lane}-empty"], "valid_domain_only": False, "scheduled_dimension_only": True},
    ]
    test_author = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "known_bad_sha256": known_bad_sha, "primary_capability": "numeric_reasoning",
        "assigned_cross_cutting_dimension": "malformed_input", "test_roles": roles,
        "visibility": {"specification_visible": True, "embedded_known_bad_visible": True, "capability_definition_visible": True, "scheduled_dimension_visible": True, "reference_visible": False, "teacher_proof_visible": False, "semantic_review_visible": False, "verifier_outputs_visible": False, "evaluation_artifacts_read": 0},
    })
    delta = seal({
        "candidate_sha256": candidate_sha, "specification_sha256": specification_sha,
        "reference_sha256": reference_sha, "known_bad_sha256": known_bad_sha,
        "primary_capability": "numeric_reasoning", "assigned_cross_cutting_dimension": "malformed_input",
        "independent_semantic_delta_count": 1, "delta_is_capability_specific": True,
        "introduces_multiple_independent_fixes": False,
        "delta_description": "maximum selection is replaced by signed accumulation",
        "visibility": {"specification_visible": True, "embedded_known_bad_visible": True, "reference_visible": True, "assigned_labels_visible": True, "tests_visible": False, "verifier_outputs_visible": False, "teacher_proof_visible": False, "training_stimulus_visible": False, "v2_outcomes_visible": False, "evaluation_artifacts_read": 0},
    })
    separation = seal({
        "candidate_sha256": candidate_sha, "comparison_contract_sha256": SEPARATION_CONTRACT_SHA256,
        "comparison_manifest_sha256": "a" * 64, "exact_training_passed": True,
        "normalized_training_passed": True, "fuzzy_training_passed": True,
        "exact_evaluation_passed": True, "normalized_evaluation_passed": True,
        "fuzzy_evaluation_passed": True, "evaluation_artifacts_read_by_construction": 0,
    })
    return {
        "schema_version": V4_ENVELOPE_SCHEMA, "candidate": candidate,
        "assignment": {"contract_id": V4_CONTRACT_ID, "id": candidate["id"], "cell_id": f"numeric_reasoning/{lane}/repair", "primary_capability": "numeric_reasoning", "primary_capability_definition": "Aggregate signed integer values deterministically.", "assigned_cross_cutting_dimension": "malformed_input"},
        "evidence": {"teacher_proof": proof, "semantic_review": semantic, "test_author": test_author, "delta_audit": delta, "separation": separation},
    }


def build_fixture_bundle(
    admission_config_path: Path = ROOT / "configs/data/expansion_v1.json",
    preflight_config_path: Path = ROOT / "configs/data/gate2_v4_post_teacher_preflight.json",
) -> dict[str, Any]:
    admission_config = json.loads(admission_config_path.read_text(encoding="utf-8"))
    preflight = load_preflight_config(preflight_config_path)
    programs = _programs(preflight["success_marker"])
    fixtures = []
    for index, lane in enumerate(LANES):
        family = FAMILY_BY_LANE[lane]
        fixtures.append({
            "fixture_id": f"positive-{lane}", "provenance_family": family,
            "expected": "admitted",
            "envelope": _envelope(
                lane, family, index, programs[lane], admission_config,
                preflight["lanes"][lane]["witness_path"],
            ),
        })
    negative = copy.deepcopy(fixtures[0])
    negative.update(
        fixture_id="negative-broken-staging", expected="broken-staging-rejected",
        broken_staging={"role": "primary_discrimination", "canonical_path": "wrong_test.go"},
    )
    fixtures.append(negative)
    return {"schema_version": SCHEMA, "contract_id": V4_CONTRACT_ID, "plan_sha256": PLAN_SHA256, "fixtures": fixtures}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admission-config", type=Path, default=ROOT / "configs/data/expansion_v1.json")
    parser.add_argument("--preflight-config", type=Path, default=ROOT / "configs/data/gate2_v4_post_teacher_preflight.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    bundle = build_fixture_bundle(args.admission_config, args.preflight_config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_json(bundle) + b"\n")
    print(json.dumps({"output": str(args.output), "bundle_sha256": canonical_sha256(bundle)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
