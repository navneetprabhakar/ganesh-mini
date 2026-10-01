#!/usr/bin/env python3
"""Run the content-free V7 schema admission and local-validation smoke."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.generate_expansion_qualification import verify_codex_version
from scripts.data.repair_delta_v7_readiness import (
    CONTRACT_ID, inject_controller_paths, response_schema, test_author_prompt,
    validate_response,
)
from scripts.data.run_repair_delta_evidence import IsolatedCodexAdapter


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--codex-config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.codex_config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    projection = {
        "id": "v7-live-schema-smoke",
        "specification": "Repair a JavaScript normalize(value) export. Trim surrounding ASCII spaces; null throws TypeError.",
        "lane": "javascript",
        "embedded_known_bad": "'use strict'; function normalize(value) { if (value === null) throw new TypeError('value'); return value; } module.exports = { normalize };",
        "primary_capability": "string_and_unicode",
        "primary_capability_definition": "transform strings according to an explicit text contract",
        "assigned_cross_cutting_dimension": "malformed_input",
        "cross_cutting_dimension_definition": "exercise only rejection of malformed input; the visible known-bad already satisfies it",
        "canonical_candidate_filename": "solution.js",
        "canonical_test_filename": "solution.test.js",
        "execution_commands": [["node", "--test", "solution.test.js"]],
        "required_local_binding": "require('./solution.js') only",
    }
    adapter = IsolatedCodexAdapter("test_author", config, args.codex_bin, args.run_dir, cli_identity, "v7")
    response = adapter(projection)
    run_sha256 = response.pop("_run_sha256")
    validate_response(response)
    injection = inject_controller_paths("javascript", response)
    report = {
        "schema_version": "ganesh-mini-gate2-v7-live-schema-smoke/v1",
        "contract_id": CONTRACT_ID,
        "status": "passed",
        "plan_sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(),
        "provider_schema_sha256": canonical_sha256(response_schema()),
        "prompt_sha256": hashlib.sha256(test_author_prompt(projection).encode()).hexdigest(),
        "projection_sha256": canonical_sha256(projection),
        "response_sha256": canonical_sha256(response),
        "controller_role_order": [row["role"] for row in injection["roles"]],
        "injection_sha256": injection["injection_sha256"],
        "run_evidence_sha256": run_sha256,
        "cli_identity": cli_identity,
        "evaluation_artifacts_read": 0,
    }
    report["report_sha256"] = canonical_sha256(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "report_sha256": report["report_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
