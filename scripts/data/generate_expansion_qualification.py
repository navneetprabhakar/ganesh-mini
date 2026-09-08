#!/usr/bin/env python3
"""Generate a two-pass Codex CLI qualification tranche with sealed evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import tempfile
from types import SimpleNamespace
from pathlib import Path
from typing import Any

from scripts.eval.contracts import CANDIDATE_PATH, LANGUAGE_FAMILY, sha256_text


ROOT = Path(__file__).resolve().parents[2]
LANES = ("go", "java", "javascript", "typescript", "python", "rust")
RUNTIMES = {
    "go": "go-1.22.12", "java": "java-21.0.11",
    "javascript": "javascript-node-22.23.2", "typescript": "typescript-5.5.4-node-22",
    "python": "python-3.11.15", "rust": "rust-1.85.0",
}
TEST_FILES = {
    "go": "solution_test.go", "java": "SolutionTest.java", "javascript": "solution.test.js",
    "typescript": "solution.test.ts", "python": "test_solution.py", "rust": "solution_test.rs",
}
LANGUAGE_CONTRACTS = {
    "go": "Use package solution. Export the requested API. Do not include package main or a main function.",
    "java": "Use a public final class Solution in Solution.java and expose the requested API as public static methods.",
    "javascript": "Use CommonJS and export exactly the requested API with module.exports. Do not use ESM export syntax.",
    "typescript": "Export the requested API with TypeScript export declarations; compilation uses strict CommonJS targeting ES2022.",
    "python": "Define the requested top-level API in solution.py. Preserve explicitly required aliasing as well as deep-copy semantics.",
    "rust": "Expose the requested API with pub declarations in solution.rs. Do not include a main function.",
}
TEST_CONTRACTS = {
    "go": "Use package solution and the standard testing package. A go.mod support file is supplied separately.",
    "java": "Use a public SolutionTest class with a public static void main and manual assertions; no JUnit.",
    "javascript": "Load the API with require('./solution') and use manual assertions or node:assert; do not require ESM.",
    "typescript": "Import from './solution' and use local manual assertion helpers. Do not import node:test, node:assert, or any Node type declarations.",
    "python": "Use unittest or plain assertions and make the file executable as __main__.",
    "rust": "Use #[path = \"solution.rs\"] mod solution plus #[test] functions. Never construct a value outside a specified numeric bound merely to test the maximum.",
}
TOPICS = (
    "lossless record transformation with malformed-input handling",
    "stable aggregation while preserving first-seen order",
    "bounded state-machine transition processing",
    "nested delimiter parsing with escape handling",
    "deterministic allocation with remainder distribution",
    "interval operations with explicit endpoint semantics",
    "dependency validation and deterministic ordering",
    "stream chunk reconciliation across split boundaries",
    "structured error collection without partial mutation",
    "bounded rolling statistics with invalid-window handling",
)
ARCHITECT_SCHEMA = ROOT / "schemas/data/codex-architect-output.schema.json"
TEST_SCHEMA = ROOT / "schemas/data/codex-test-output.schema.json"
SOURCE_DATASET = "codex-cli/gpt-5.6-sol"
SOURCE_REVISION = "codex-cli-0.144.4:model-alias-gpt-5.6-sol"


class CodexInvocationFailure(RuntimeError):
    """A failed Codex invocation carrying the raw evidence collected so far."""

    def __init__(self, message: str, evidence: dict[str, Any]) -> None:
        super().__init__(message)
        self.evidence = evidence


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def task_type(index: int, total: int) -> str:
    return "generation" if index < math.ceil(total * 0.6) else "repair"


def task_specs(lane: str, per_lane: int) -> list[dict[str, str]]:
    return [
        {
            "id": f"codex-v1-{lane}-{task_type(index, per_lane)}-{index + 1:02d}",
            "task_type": task_type(index, per_lane),
            "topic": TOPICS[index],
        }
        for index in range(per_lane)
    ]


def architect_prompt(lane: str, specs: list[dict[str, str]]) -> str:
    return f"""Create original SFT candidates for a compact coding model. Do not use tools or inspect the filesystem.

Language: {lane}
Candidate filename: {CANDIDATE_PATH[lane]}
Runtime contract: {LANGUAGE_CONTRACTS[lane]}
Requested items: {json.dumps(specs, separators=(",", ":"))}

For every item, return its exact id plus problem, reference_code, known_bad_code, and known_bad_label.
Each problem must be self-contained, standard-library-only, specify one exact public API, define empty,
malformed, and boundary behavior, prohibit input mutation where relevant, and avoid network, clock,
randomness, filesystem, external packages, and competitive-programming framing. Code must be a complete
source file. The reference must be correct. The known-bad source must be plausible and contain exactly one
semantic bug described by known_bad_label.

Before returning, audit the reference line by line against every stated requirement, especially identity
preservation, ordering, numeric bounds, malformed-input atomicity, and non-mutation. Do not state a stronger
aliasing or deep-copy contract than the reference actually implements.

For generation items, the problem asks for a new implementation. For repair items, include the complete
known-bad source in the problem and ask for a corrected complete source file; reference_code is the repair
and known_bad_code is the exact buggy source embedded in the problem. Do not include tests in any problem.
Return only the schema-constrained object."""


def test_prompt(lane: str, items: list[dict[str, str]]) -> str:
    visible = [{"id": item["id"], "problem": item["problem"]} for item in items]
    return f"""Act as an independent {lane} behavioral-test author. Do not use tools or inspect the filesystem.
You may see only the task IDs and specifications below. You have not seen any reference implementation,
known-bad implementation, source tests, or architect context.

Candidate filename: {CANDIDATE_PATH[lane]}
Test filename: {TEST_FILES[lane]}
Runtime contract: {TEST_CONTRACTS[lane]}
Tasks: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

For every exact id, return one complete deterministic standard-library-only test file in test_code.
Exercise normal, empty, malformed, boundary, stability, and non-mutation behavior where applicable.
Before returning, audit that every test input is constructible within the specification, every expected value
follows directly from the specification, and the test file compiles in the stated runtime contract.
Do not return Markdown fences or prose. Return only the schema-constrained object."""


def architect_critic_prompt(lane: str, items: list[dict[str, str]]) -> str:
    return f"""Independently audit these {lane} task/reference/known-bad candidates. Do not use tools or inspect the filesystem.
Runtime contract: {LANGUAGE_CONTRACTS[lane]}
Items: {json.dumps(items, separators=(",", ":"), ensure_ascii=False)}

Return every exact id and the same five schema fields. Preserve each problem's intended API and difficulty.
Correct any contradiction between the problem and reference, including descriptor, identity, ordering, aliasing,
numeric-boundary, malformed-input, module, or atomicity semantics. Ensure the known-bad implementation differs
from the corrected reference by exactly one plausible semantic bug and that known_bad_label describes it.
Do not add tests to a problem. Return only the schema-constrained object."""


def critic_test_prompt(lane: str, architecture_items: list[dict[str, str]], test_items: list[dict[str, str]]) -> str:
    problems = {item["id"]: item["problem"] for item in architecture_items}
    visible = [
        {"id": item["id"], "problem": problems[item["id"]], "test_code": item["test_code"]}
        for item in test_items
    ]
    return f"""Independently audit these {lane} behavioral tests. Do not use tools or inspect the filesystem.
You may see only each specification and proposed test file. You have not seen any reference or known-bad implementation.
Runtime contract: {TEST_CONTRACTS[lane]}
Items: {json.dumps(visible, separators=(",", ":"), ensure_ascii=False)}

Return every exact id with a corrected complete test_code. Remove impossible inputs, expectations not required by
the specification, module/type-system incompatibilities, and strict-compiler errors. Preserve strong coverage of
normal, empty, malformed, boundary, stability, and non-mutation behavior. Return only the schema-constrained object."""


def codex_command(
    codex_bin: str,
    config: dict[str, Any],
    schema: Path,
    output: Path,
    working_directory: Path,
    prompt: str,
) -> list[str]:
    return [
        codex_bin, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--sandbox", "read-only", "--skip-git-repo-check", "--json", "-m", config["model"],
        "-c", f'model_reasoning_effort="{config["reasoning_effort"]}"',
        "-c", f'service_tier="{config["service_tier"]}"',
        "--output-schema", str(schema.resolve()), "-o", str(output.resolve()),
        "-C", str(working_directory.resolve()), prompt,
    ]


def parse_events(stdout: str) -> tuple[list[dict[str, Any]], dict[str, Any] | None, list[str]]:
    events: list[dict[str, Any]] = []
    usage: dict[str, Any] | None = None
    disallowed: list[str] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError("Codex JSONL event is not an object")
        events.append(event)
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
        item = event.get("item")
        if isinstance(item, dict):
            item_type = item.get("type")
            if item_type not in {None, "reasoning", "agent_message"}:
                disallowed.append(str(item_type))
    return events, usage, disallowed


def verify_codex_version(codex_bin: str, expected: str) -> str:
    observed = subprocess.run(
        [codex_bin, "--version"], check=True, capture_output=True, text=True, stdin=subprocess.DEVNULL,
    ).stdout.strip()
    match = re.fullmatch(r"codex-cli (\S+)", observed)
    if not match or match.group(1) != expected:
        raise ValueError(f"Codex CLI identity mismatch: expected {expected}, observed {observed!r}")
    return observed


def invoke_codex(
    codex_bin: str,
    config: dict[str, Any],
    schema: Path,
    prompt: str,
    run_kind: str,
    lane: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix=f"ganesh-codex-{run_kind}-{lane}-") as temp_name:
        workdir = Path(temp_name)
        output = workdir / "final.json"
        command = codex_command(codex_bin, config, schema, output, workdir, prompt)
        timed_out = False
        try:
            result = subprocess.run(
                command, cwd=workdir, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                timeout=config["execution"].get("timeout_seconds", 1800), check=False,
            )
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            def decoded(value):
                return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
            result = SimpleNamespace(returncode=None, stdout=decoded(exc.stdout), stderr=decoded(exc.stderr))
        event_parse_error: str | None = None
        try:
            events, usage, disallowed = parse_events(result.stdout)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            events, usage, disallowed = [], None, []
            event_parse_error = str(exc)
        final_text = output.read_text(encoding="utf-8") if output.is_file() else ""
        run_evidence = {
            "run_kind": run_kind, "lane": lane, "command_identity": command[:-1],
            "prompt": prompt, "prompt_sha256": sha256_text(prompt), "returncode": result.returncode,
            "stdout_jsonl": result.stdout, "stdout_sha256": sha256_text(result.stdout),
            "stderr": result.stderr, "stderr_sha256": sha256_text(result.stderr),
            "final_output": final_text, "final_output_sha256": sha256_text(final_text),
            "events": events, "usage": usage, "disallowed_tool_item_types": disallowed,
            "event_parse_error": event_parse_error,
            "timed_out": timed_out,
        }
        if timed_out:
            raise CodexInvocationFailure(f"Codex {run_kind}/{lane} timed out", run_evidence)
        if result.returncode != 0:
            raise CodexInvocationFailure(
                f"Codex {run_kind}/{lane} failed with exit {result.returncode}", run_evidence,
            )
        if event_parse_error is not None:
            raise CodexInvocationFailure(
                f"Codex {run_kind}/{lane} emitted invalid JSONL: {event_parse_error}", run_evidence,
            )
        if disallowed:
            raise CodexInvocationFailure(
                f"Codex {run_kind}/{lane} used disallowed tools: {sorted(set(disallowed))}", run_evidence,
            )
        if usage is None:
            raise CodexInvocationFailure(
                f"Codex {run_kind}/{lane} emitted no terminal usage", run_evidence,
            )
        try:
            payload = json.loads(final_text)
        except json.JSONDecodeError as exc:
            raise CodexInvocationFailure(
                f"Codex {run_kind}/{lane} final output is not JSON: {exc}", run_evidence,
            ) from exc
        if not isinstance(payload, dict):
            raise ValueError("Codex final structured output is not an object")
        return payload, run_evidence


def exact_items(payload: dict[str, Any], expected_ids: list[str], fields: set[str]) -> list[dict[str, str]]:
    items = payload.get("items")
    if not isinstance(items, list) or len(items) != len(expected_ids):
        raise ValueError("structured output item count differs from request")
    by_id: dict[str, dict[str, str]] = {}
    for item in items:
        if not isinstance(item, dict) or set(item) != fields:
            raise ValueError("structured output item keys differ from contract")
        if any(not isinstance(value, str) or not value.strip() for value in item.values()):
            raise ValueError("structured output contains an empty/non-string value")
        if item["id"] in by_id:
            raise ValueError("structured output contains duplicate IDs")
        by_id[item["id"]] = item
    if set(by_id) != set(expected_ids):
        raise ValueError("structured output IDs differ from request")
    return [by_id[item_id] for item_id in expected_ids]


def build_candidate(
    lane: str,
    record_id: str,
    row_task_type: str,
    architecture: dict[str, str],
    tests: str,
    source_revision: str = SOURCE_REVISION,
    source: dict[str, str] | None = None,
) -> dict[str, Any]:
    required = {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"}
    if set(architecture) != required or architecture["id"] != record_id:
        raise ValueError("architect item does not match the requested record")
    if any(not isinstance(architecture[key], str) or not architecture[key].strip() for key in required):
        raise ValueError("architect item contains empty/non-string values")
    problem = architecture["problem"].strip() + "\n\nReturn only the complete source file; do not include Markdown fences or prose."
    reference = architecture["reference_code"].strip() + "\n"
    known_bad = architecture["known_bad_code"].strip() + "\n"
    test_source = tests.strip()
    if test_source.startswith("```"):
        lines = test_source.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        test_source = "\n".join(lines).strip()
    test_source += "\n"
    files = [{"path": TEST_FILES[lane], "role": "test", "content": test_source, "sha256": sha256_text(test_source)}]
    if lane == "go":
        go_mod = "module ganesh.invalid/expansion\n\ngo 1.22\n"
        files.insert(0, {"path": "go.mod", "role": "support", "content": go_mod, "sha256": sha256_text(go_mod)})
    task = {
        "schema_version": "1.0", "task_id": record_id, "surface": "training_admission",
        "language": lane, "family": LANGUAGE_FAMILY[lane], "task_type": row_task_type,
        "prompt": {"text": problem, "sha256": sha256_text(problem)},
        "rendered_prompt": {"text": problem, "sha256": sha256_text(problem)},
        "candidate_path": CANDIDATE_PATH[lane],
        "files": files,
        "runtime_id": RUNTIMES[lane],
        "limits": {"timeout_seconds": 60, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
        "validation": {
            "reference": {"label": "codex-teacher-reference", "code": reference, "sha256": sha256_text(reference)},
            "known_bad": [{"label": architecture["known_bad_label"], "code": known_bad, "sha256": sha256_text(known_bad)}],
        },
    }
    source_hash = hashlib.sha256(canonical_json(architecture)).hexdigest()
    lineage = source or {
        "dataset": SOURCE_DATASET, "uri": "https://learn.chatgpt.com/docs/non-interactive-mode",
        "revision": source_revision, "record_id": record_id, "license": "user-owned-output",
        "license_uri": "https://openai.com/policies/terms-of-use/",
        "source_record_sha256": source_hash,
        "transformation": "two-pass Codex CLI synthesis; independent test pass saw specification only",
    }
    return {
        "schema_version": "ganesh-mini-expansion-candidate/v1", "id": record_id,
        "lane": lane, "task_type": row_task_type,
        "messages": [{"role": "user", "content": problem}, {"role": "assistant", "content": reference}],
        "source": lineage,
        "rights": {key: True for key in ("prompt", "answer", "tests", "redistribution", "model_training")},
        "verification_task": task, "test_origin": "independent_teacher",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_teacher.json"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--per-lane", type=int, default=1)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--lane", action="append", choices=LANES, help="limit generation to one or more lanes")
    parser.add_argument("--architect-critic", action="store_true")
    parser.add_argument("--test-critic", action="store_true")
    args = parser.parse_args()
    if args.per_lane < 1 or args.per_lane > len(TOPICS):
        raise ValueError(f"per-lane must be between 1 and {len(TOPICS)}")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    cli_identity = verify_codex_version(args.codex_bin, config["codex_cli_version"])
    candidates: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    selected_lanes = tuple(args.lane or LANES)
    for lane in selected_lanes:
        specs = task_specs(lane, args.per_lane)
        expected_ids = [spec["id"] for spec in specs]
        try:
            architecture_payload, architecture_evidence = invoke_codex(
                args.codex_bin, config, ARCHITECT_SCHEMA, architect_prompt(lane, specs), "architect", lane,
            )
            runs.append(architecture_evidence)
            architecture_items = exact_items(
                architecture_payload, expected_ids,
                {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
            )
            if args.architect_critic:
                critic_payload, critic_evidence = invoke_codex(
                    args.codex_bin, config, ARCHITECT_SCHEMA,
                    architect_critic_prompt(lane, architecture_items), "architect-critic", lane,
                )
                runs.append(critic_evidence)
                architecture_items = exact_items(
                    critic_payload, expected_ids,
                    {"id", "problem", "reference_code", "known_bad_code", "known_bad_label"},
                )
            tests_payload, tests_evidence = invoke_codex(
                args.codex_bin, config, TEST_SCHEMA, test_prompt(lane, architecture_items), "test-author", lane,
            )
            runs.append(tests_evidence)
            test_items = exact_items(tests_payload, expected_ids, {"id", "test_code"})
            if args.test_critic:
                critic_payload, critic_evidence = invoke_codex(
                    args.codex_bin, config, TEST_SCHEMA,
                    critic_test_prompt(lane, architecture_items, test_items), "test-critic", lane,
                )
                runs.append(critic_evidence)
                test_items = exact_items(critic_payload, expected_ids, {"id", "test_code"})
            tests_by_id = {item["id"]: item["test_code"] for item in test_items}
            types_by_id = {spec["id"]: spec["task_type"] for spec in specs}
            for architecture in architecture_items:
                record_id = architecture["id"]
                candidates.append(build_candidate(
                    lane, record_id, types_by_id[record_id], architecture, tests_by_id[record_id],
                ))
        except (json.JSONDecodeError, KeyError, OSError, RuntimeError, subprocess.SubprocessError, TypeError, ValueError) as exc:
            if isinstance(exc, CodexInvocationFailure):
                runs.append(exc.evidence)
            failures.append({"lane": lane, "reason": str(exc)})
    payload = b"".join(canonical_json(row) + b"\n" for row in candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    evidence = {
        "schema_version": "ganesh-mini-expansion-teacher-run/v2", "teacher": config,
        "cli_identity": cli_identity, "selected_lanes": list(selected_lanes),
        "architect_critic": args.architect_critic, "test_critic": args.test_critic,
        "requested": len(selected_lanes) * args.per_lane,
        "generated": len(candidates), "candidate_output_sha256": hashlib.sha256(payload).hexdigest(),
        "failures": failures, "runs": runs,
    }
    evidence["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"requested": evidence["requested"], "generated": len(candidates), "failures": len(failures)}, sort_keys=True))
    return 0 if len(candidates) == evidence["requested"] and not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
