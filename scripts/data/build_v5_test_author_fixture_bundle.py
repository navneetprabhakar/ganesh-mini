#!/usr/bin/env python3
"""Build sealed V5 strict test-author fixtures without invoking a model."""

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

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.run_repair_delta_evidence import V5_CONTRACT_ID
from scripts.eval.contracts import sha256_text


PLAN_SHA256 = "132501466e58e88b6aaebc412aac37e561b103ae8df8f50a9ac43d3aab7cc04b"
SCHEMA = "ganesh-mini-v5-test-author-fixture-bundle/v1"
LANES = ("go", "java", "javascript", "typescript", "python", "rust")


def _candidate(lane: str) -> dict[str, Any]:
    support_content = f"fixture support for {lane}\n"
    return {
        "id": f"v5-test-author-positive-{lane}",
        "lane": lane,
        "messages": [{"role": "user", "content": f"Repair the {lane} fixture."}],
        "verification_task": {
            "files": [{
                "path": "fixture-support.txt", "role": "support",
                "content": support_content, "sha256": sha256_text(support_content),
            }],
            "validation": {"known_bad": [{"sha256": sha256_text(f"known-bad-{lane}")}]},
        },
    }


def _assignment(candidate: dict[str, Any]) -> dict[str, Any]:
    lane = candidate["lane"]
    return {
        "id": candidate["id"], "contract_id": V5_CONTRACT_ID,
        "cell_id": f"numeric_reasoning/{lane}/repair",
        "primary_capability": "numeric_reasoning",
        "primary_capability_definition": "Correct numeric results on at least two valid inputs.",
        "assigned_cross_cutting_dimension": "malformed_input",
    }


def _positive_responses() -> dict[str, dict[str, Any]]:
    return {
        "go": {
            "primary_discrimination": {
                "path": "primary_solution_test.go",
                "content": "package solution\nimport \"testing\"\nfunc TestPrimary(t *testing.T) { t.Run(\"positive\", func(t *testing.T) {}); t.Run(\"signed\", func(t *testing.T) {}) }",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "cross_solution_test.go",
                "content": "package solution\nimport \"testing\"\nfunc TestMalformed(t *testing.T) { defer func() { _ = recover() }(); ComputeTotal(nil) }",
                "case_ids": ["nil-input"],
            },
        },
        "java": {
            "primary_discrimination": {
                "path": "PrimarySolutionTest.java",
                "content": "class SolutionTest { static void main(String[] args) { int[] cases = {1, -1}; if (cases.length != 2) throw new AssertionError(); } }",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "CrossSolutionTest.java",
                "content": "class SolutionTest { static void main(String[] args) { try { Solution.computeTotal(null); } catch (RuntimeException expected) { } } }",
                "case_ids": ["null-input"],
            },
        },
        "javascript": {
            "primary_discrimination": {
                "path": "primary_solution.test.js",
                "content": "'use strict';\nconst cases = [1, -1];\nif (cases.length !== 2) throw new Error('fixture');",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "cross_solution.test.js",
                "content": "'use strict';\ntry { require('./solution.js').computeTotal(null); } catch (expected) { void expected; }",
                "case_ids": ["null-input"],
            },
        },
        "typescript": {
            "primary_discrimination": {
                "path": "primary_solution.test.ts",
                "content": "import { computeTotal } from './solution';\nconst inputs: number[] = [1, -1];\nif (inputs.length !== 2) throw new Error(String(computeTotal));",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "cross_solution.test.ts",
                "content": "import { computeTotal } from './solution';\ntry { computeTotal(null as never); } catch (expected) { void expected; }",
                "case_ids": ["null-input"],
            },
        },
        "python": {
            "primary_discrimination": {
                "path": "primary_test_solution.py",
                "content": "def test_cases_exist():\n    cases = [1, -1]\n    assert len(cases) == 2",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "cross_test_solution.py",
                "content": "def test_malformed_invocation():\n    try:\n        compute_total(None)\n    except Exception:\n        pass",
                "case_ids": ["none-input"],
            },
        },
        "rust": {
            "primary_discrimination": {
                "path": "primary_solution_test.rs",
                "content": "#[test]\nfn primary_cases() { let cases = [1_i64, -1_i64]; assert_eq!(cases.len(), 2); }",
                "case_ids": ["positive", "signed"],
            },
            "cross_cutting": {
                "path": "cross_solution_test.rs",
                "content": "#[test]\nfn malformed_invocation() { let _ = solution::compute_total(&[]); }",
                "case_ids": ["empty-input"],
            },
        },
    }


def build_v5_test_author_fixture_bundle() -> dict[str, Any]:
    responses = _positive_responses()
    positives = []
    for lane in LANES:
        candidate = _candidate(lane)
        positives.append({
            "fixture_id": f"v5-test-author-positive-{lane}", "lane": lane,
            "candidate": candidate, "assignment": _assignment(candidate),
            "response": responses[lane], "run_sha256": sha256_text(f"run-{lane}"),
        })

    python_candidate = _candidate("python")
    java_candidate = _candidate("java")
    ts_candidate = _candidate("typescript")
    go_candidate = _candidate("go")
    negatives = [
        {
            "fixture_id": "reject-legacy-three-file-array", "lane": "python",
            "candidate": python_candidate, "assignment": _assignment(python_candidate),
            "response": {"files": [
                {"path": f"legacy-{index}.py", "content": "pass", "case_ids": [str(index)]}
                for index in range(3)
            ]},
            "expected_error": "exactly two named role objects",
        },
        {
            "fixture_id": "reject-java-entrypoint", "lane": "java",
            "candidate": java_candidate, "assignment": _assignment(java_candidate),
            "response": {
                "primary_discrimination": {
                    "path": "Primary.java", "content": "class WrongTest { static void main(String[] args) {} }",
                    "case_ids": ["one", "two"],
                },
                "cross_cutting": copy.deepcopy(responses["java"]["cross_cutting"]),
            },
            "expected_error": "SolutionTest with static void main",
        },
        {
            "fixture_id": "reject-typescript-node-test-import", "lane": "typescript",
            "candidate": ts_candidate, "assignment": _assignment(ts_candidate),
            "response": {
                "primary_discrimination": {
                    "path": "primary.ts",
                    "content": "import test from 'node:test';\nimport assert from 'node:assert/strict';\nvoid test; void assert;",
                    "case_ids": ["one", "two"],
                },
                "cross_cutting": copy.deepcopy(responses["typescript"]["cross_cutting"]),
            },
            "expected_error": "self-contained without unavailable typings",
        },
        {
            "fixture_id": "reject-primary-dependent-cross-test", "lane": "go",
            "candidate": go_candidate, "assignment": _assignment(go_candidate),
            "response": {
                "primary_discrimination": copy.deepcopy(responses["go"]["primary_discrimination"]),
                "cross_cutting": {
                    "path": "cross_solution_test.go",
                    "content": "package solution\nimport \"testing\"\nfunc TestCross(t *testing.T) { got := ComputeTotal(nil); if got != 0 { t.Fatal(got) } }",
                    "case_ids": ["nil-input"],
                },
            },
            "expected_error": "cross-cutting test asserts primary behavior",
        },
    ]
    for row in negatives:
        row["run_sha256"] = sha256_text(row["fixture_id"])

    bundle = {
        "schema_version": SCHEMA, "contract_id": V5_CONTRACT_ID,
        "plan_sha256": PLAN_SHA256, "lanes": list(LANES),
        "positive_fixtures": positives, "negative_fixtures": negatives,
        "evaluation_artifacts_read": 0,
    }
    bundle["bundle_sha256"] = canonical_sha256(bundle)
    return bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = build_v5_test_author_fixture_bundle()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "bundle_sha256": bundle["bundle_sha256"],
        "positive_fixtures": len(bundle["positive_fixtures"]),
        "negative_fixtures": len(bundle["negative_fixtures"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
