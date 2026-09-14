#!/usr/bin/env python3
"""Run the local, resumable Gate 2 capability admission campaign."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.data.admit_capability_qualification import (  # noqa: E402
    admit_qualification,
    build_report as build_admission_report,
    load_queue as load_admission_queue,
    verify,
)
from scripts.data.admit_expansion import canonical_json, read_jsonl  # noqa: E402
from scripts.data.build_capability_admission_envelopes import (  # noqa: E402
    ASSEMBLY_SCHEMA,
    SEMANTIC_SCHEMA,
    SEPARATION_SCHEMA,
    build_envelopes,
    load_report,
    load_teacher_candidates,
)
from scripts.data.build_capability_corpus_plan import canonical_sha256, load_sealed  # noqa: E402
from scripts.data.generate_capability_qualification import LANES, load_queue as load_teacher_queue  # noqa: E402
from scripts.data.generate_capability_replacements import MANIFEST_SCHEMA as REPLACEMENT_MANIFEST_SCHEMA  # noqa: E402


CAMPAIGN_SCHEMA = "ganesh-mini-capability-admission-campaign/v1"
EXPECTED_BATCHES = 24


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def discover_batches(candidate_dir: Path, evidence_dir: Path) -> tuple[list[Path], list[Path]]:
    expected = [f"{lane}-{index:03d}" for lane in LANES for index in range(4)]
    candidates = {path.name.removesuffix(".candidates.jsonl"): path for path in candidate_dir.glob("*.candidates.jsonl")}
    evidence = {path.name.removesuffix(".evidence.json"): path for path in evidence_dir.glob("*.evidence.json")}
    if set(candidates) != set(expected) or set(evidence) != set(expected) or len(expected) != EXPECTED_BATCHES:
        raise ValueError("teacher artifact directories must contain exactly the 24 sealed lane batches")
    return [candidates[stem] for stem in expected], [evidence[stem] for stem in expected]


def artifact(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": file_sha256(path)}


def input_bindings(
    *, plan_path: Path, queue_path: Path, queue_manifest_path: Path,
    candidate_paths: list[Path], evidence_paths: list[Path],
    semantic_path: Path, separation_path: Path, config_path: Path, runtime_config_path: Path,
    record_workers: int, verifier_workers: int,
    correction_report_path: Path | None = None,
    replacement_manifest_path: Path | None = None,
) -> dict[str, Any]:
    bindings = {
        "plan": artifact(plan_path), "queue": artifact(queue_path),
        "queue_manifest": artifact(queue_manifest_path),
        "teacher_batches": [
            {"candidates": artifact(candidate), "evidence": artifact(evidence)}
            for candidate, evidence in zip(candidate_paths, evidence_paths, strict=True)
        ],
        "semantic_review": artifact(semantic_path), "separation": artifact(separation_path),
        "admission_config": artifact(config_path), "runtime_config": artifact(runtime_config_path),
        "execution": {"record_workers": record_workers, "verifier_workers_per_record": verifier_workers},
        "evaluation_artifacts_read": 0,
    }
    if correction_report_path is not None:
        correction = json.loads(correction_report_path.read_text(encoding="utf-8"))
        output = correction.get("output") if isinstance(correction, dict) else None
        if not isinstance(output, dict) or not isinstance(output.get("path"), str):
            raise ValueError("correction report lacks its corrected candidate artifact")
        bindings["correction"] = {
            "report": artifact(correction_report_path),
            "corrected_candidates": artifact(Path(output["path"])),
        }
    if replacement_manifest_path is not None:
        replacement_manifest = json.loads(replacement_manifest_path.read_text(encoding="utf-8"))
        queue_output = replacement_manifest.get("queue_output", {}) if isinstance(replacement_manifest, dict) else {}
        if not isinstance(queue_output.get("path"), str):
            raise ValueError("replacement manifest lacks its queue artifact")
        bindings["bounded_replacements"] = {
            "manifest": artifact(replacement_manifest_path),
            "queue": artifact(Path(queue_output["path"])),
        }
    return bindings


def load_replacement_artifacts(
    manifest_path: Path, original_queue: list[dict[str, Any]], semantic: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[Path], list[Path], dict[str, Any]]:
    manifest = load_sealed(manifest_path, "manifest_sha256")
    queue_binding = manifest.get("queue_output")
    if (
        manifest.get("schema_version") != REPLACEMENT_MANIFEST_SCHEMA
        or manifest.get("status") != "replacement-generation-complete-not-reviewed-not-admitted"
        or manifest.get("replacement_attempt") != 1
        or not isinstance(manifest.get("semantic_report_sha256"), str)
        or len(manifest["semantic_report_sha256"]) != 64
        or not isinstance(manifest.get("corrected_admission_report_sha256"), str)
        or len(manifest["corrected_admission_report_sha256"]) != 64
        or not isinstance(manifest.get("correction_report_sha256"), str)
        or len(manifest["correction_report_sha256"]) != 64
        or manifest.get("evaluation_artifacts_read") != 0
        or not isinstance(queue_binding, dict)
        or not isinstance(queue_binding.get("path"), str)
    ):
        raise ValueError("bounded replacement manifest is incomplete or unbound")
    queue_path = Path(queue_binding["path"])
    rows = read_jsonl(queue_path)
    originals = {row["id"]: row for row in original_queue}
    original_sources = {
        (row["source"]["dataset"], row["source"]["revision"], row["source"]["record_id"])
        for row in original_queue
    }
    if (
        queue_binding.get("sha256") != file_sha256(queue_path)
        or manifest.get("records") != len(rows)
        or manifest.get("candidate_ids") != [row.get("id") for row in rows]
        or manifest.get("empty_cells") != [row.get("cell_id") for row in rows]
        or len({row.get("id") for row in rows}) != len(rows)
        or len({row.get("cell_id") for row in rows}) != len(rows)
    ):
        raise ValueError("bounded replacement queue differs from its manifest")
    for row in rows:
        source = row.get("source", {})
        identity = (source.get("dataset"), source.get("revision"), source.get("record_id"))
        parent_ids = row.get("original_queue_ids")
        if (
            row.get("replacement_attempt") != 1
            or row.get("replacement_for_cell_id") != row.get("cell_id")
            or row.get("id") in originals
            or identity in original_sources
            or row.get("disposition_report_sha256") != manifest["corrected_admission_report_sha256"]
            or not isinstance(parent_ids, list) or len(parent_ids) != 2
            or any(parent not in originals or originals[parent]["cell_id"] != row["cell_id"] for parent in parent_ids)
        ):
            raise ValueError("bounded replacement identity, source, or parent binding is invalid")
    batches = manifest.get("batches")
    if not isinstance(batches, list) or sum(item.get("records", 0) for item in batches if isinstance(item, dict)) != len(rows):
        raise ValueError("bounded replacement batch inventory is incomplete")
    candidates = [Path(item["candidates"]) for item in batches]
    evidence = [Path(item["evidence"]) for item in batches]
    if not all(path.is_file() for path in [*candidates, *evidence]):
        raise ValueError("bounded replacement teacher artifacts are absent")
    return rows, candidates, evidence, manifest


def _load_exact_report(path: Path, schema: str) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    body = dict(report)
    claimed = body.pop("report_sha256", None)
    if claimed != canonical_sha256(body) or report.get("schema_version") != schema:
        raise ValueError(f"{path}: invalid report seal or schema")
    return report


def _verify_artifact(binding: Any, expected_path: Path, where: str) -> None:
    if not isinstance(binding, dict) or binding.get("path") != str(expected_path):
        raise ValueError(f"{where}: artifact path binding mismatch")
    data = expected_path.read_bytes()
    if binding.get("bytes") != len(data) or binding.get("sha256") != hashlib.sha256(data).hexdigest():
        raise ValueError(f"{where}: artifact content binding mismatch")


def _assembly_report(
    bindings: dict[str, Any], output_path: Path, envelopes: list[dict[str, Any]],
    teacher_inputs: list[dict[str, Any]], semantic: dict[str, Any], separation: dict[str, Any],
) -> dict[str, Any]:
    payload = output_path.read_bytes()
    report: dict[str, Any] = {
        "schema_version": ASSEMBLY_SCHEMA, "status": "ready-for-executable-admission",
        "records": len(envelopes), "evaluation_artifacts_read": 0,
        "inputs_sha256": canonical_sha256(bindings),
        "teacher_batches": teacher_inputs,
        "semantic_review_report_sha256": semantic["report_sha256"],
        "separation_report_sha256": separation["report_sha256"],
        "output": {"path": str(output_path), "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()},
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def _load_or_build_assembly(
    *, output_path: Path, report_path: Path, bindings: dict[str, Any],
    queue_by_id: dict[str, dict[str, Any]], candidate_paths: list[Path], evidence_paths: list[Path],
    queue_path: Path, queue_manifest: dict[str, Any], semantic: dict[str, Any], separation: dict[str, Any],
    correction_report_path: Path | None = None,
    replacement_manifest_path: Path | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if output_path.exists() or report_path.exists():
        if not output_path.is_file() or not report_path.is_file():
            raise ValueError("partial admission-envelope assembly artifacts exist")
        report = _load_exact_report(report_path, ASSEMBLY_SCHEMA)
        _verify_artifact(report.get("output"), output_path, "assembly")
        if report.get("inputs_sha256") != canonical_sha256(bindings):
            raise ValueError("existing assembly was built from different inputs")
        rows = read_jsonl(output_path)
        if report.get("records") != len(rows):
            raise ValueError("existing assembly record count mismatch")
        return rows, report

    candidates, derived, teacher_inputs = load_teacher_candidates(
        queue_by_id, candidate_paths, evidence_paths,
        queue_file_sha256=file_sha256(queue_path),
        queue_manifest_sha256=queue_manifest["manifest_sha256"],
        correction_report_path=correction_report_path,
    )
    envelopes = build_envelopes(queue_by_id, candidates, derived, semantic, separation)
    output_path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in envelopes))
    report = _assembly_report(bindings, output_path, envelopes, teacher_inputs, semantic, separation)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return envelopes, report


def _load_existing_admission(
    envelope_path: Path, admitted_path: Path, rejected_path: Path, report_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]] | None:
    paths = (admitted_path, rejected_path, report_path)
    if not any(path.exists() for path in paths):
        return None
    if not all(path.is_file() for path in paths):
        raise ValueError("partial executable-admission artifacts exist")
    report = _load_exact_report(report_path, "ganesh-mini-capability-qualification-admission/v1")
    if (
        report.get("mode") != "final"
        or report.get("input", {}).get("path") != str(envelope_path)
        or report.get("input", {}).get("sha256") != file_sha256(envelope_path)
    ):
        raise ValueError("existing admission report does not bind the envelope input")
    _verify_artifact(report.get("outputs", {}).get("admitted"), admitted_path, "admitted")
    _verify_artifact(report.get("outputs", {}).get("rejected"), rejected_path, "rejected")
    admitted = read_jsonl(admitted_path)
    rejected = json.loads(rejected_path.read_text(encoding="utf-8"))
    if report.get("accepted") != len(admitted) or report.get("rejected") != len(rejected):
        raise ValueError("existing admission output counts differ from report")
    return admitted, rejected, report


def _campaign_report(
    bindings: dict[str, Any], assembly_report: dict[str, Any], admission_report: dict[str, Any],
    paths: dict[str, Path], reused_assembly: bool, reused_admission: bool,
) -> dict[str, Any]:
    status = "qualification-passed" if admission_report["status"] == "passed" else "qualification-failed"
    report: dict[str, Any] = {
        "schema_version": CAMPAIGN_SCHEMA, "status": status,
        "inputs": bindings, "evaluation_artifacts_read": 0,
        "resumption": {"assembly_reused": reused_assembly, "admission_reused": reused_admission},
        "assembly_report_sha256": assembly_report["report_sha256"],
        "admission_report_sha256": admission_report["report_sha256"],
        "outputs": {name: artifact(path) for name, path in paths.items() if name != "campaign_report"},
    }
    report["report_sha256"] = canonical_sha256(report)
    return report


def run_campaign(
    *, plan_path: Path, queue_path: Path, queue_manifest_path: Path,
    candidate_dir: Path, evidence_dir: Path, semantic_path: Path, separation_path: Path,
    config_path: Path, runtime_config_path: Path, output_root: Path,
    correction_report_path: Path | None = None,
    replacement_manifest_path: Path | None = None,
    record_workers: int = 4, verifier_workers: int = 2,
    verifier_fn: Callable[[dict[str, Any], str, Path], dict[str, Any]] = verify,
) -> dict[str, Any]:
    if not 1 <= record_workers <= 8 or not 1 <= verifier_workers <= 4 or record_workers * verifier_workers > 16:
        raise ValueError("parallel verifier bounds exceeded")
    candidate_paths, evidence_paths = discover_batches(candidate_dir, evidence_dir)
    plan = load_sealed(plan_path, "plan_sha256")
    if plan.get("schema_version") != "ganesh-mini-capability-stratified-corpus-plan/v1" or plan.get("matrix", {}).get("cells") != 120:
        raise ValueError("unsupported capability qualification plan")
    queue_rows, queue_manifest = load_teacher_queue(queue_path, queue_manifest_path)
    queue_by_id = load_admission_queue(queue_path, queue_manifest_path, plan)
    semantic = load_report(semantic_path, "report_sha256", SEMANTIC_SCHEMA)
    separation = load_report(separation_path, "report_sha256", SEPARATION_SCHEMA)
    if replacement_manifest_path is not None:
        replacement_rows, replacement_candidates, replacement_evidence, _ = load_replacement_artifacts(
            replacement_manifest_path, queue_rows, semantic,
        )
        candidate_paths.extend(replacement_candidates)
        evidence_paths.extend(replacement_evidence)
        for row in replacement_rows:
            if row["id"] in queue_by_id:
                raise ValueError("bounded replacement reuses an existing queue ID")
            queue_by_id[row["id"]] = row
    bindings = input_bindings(
        plan_path=plan_path, queue_path=queue_path, queue_manifest_path=queue_manifest_path,
        candidate_paths=candidate_paths, evidence_paths=evidence_paths,
        semantic_path=semantic_path, separation_path=separation_path,
        config_path=config_path, runtime_config_path=runtime_config_path,
        record_workers=record_workers, verifier_workers=verifier_workers,
        correction_report_path=correction_report_path,
        replacement_manifest_path=replacement_manifest_path,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    paths = {
        "envelopes": output_root / "admission-envelopes.jsonl",
        "assembly_report": output_root / "assembly-report.json",
        "admitted": output_root / "admitted.jsonl",
        "rejected": output_root / "rejected.json",
        "admission_report": output_root / "admission-report.json",
        "campaign_report": output_root / "campaign-report.json",
    }
    if paths["campaign_report"].exists():
        report = _load_exact_report(paths["campaign_report"], CAMPAIGN_SCHEMA)
        if report.get("inputs") != bindings:
            raise ValueError("existing campaign was run from different inputs")
        for name, binding in report.get("outputs", {}).items():
            _verify_artifact(binding, paths[name], f"campaign.{name}")
        assembly_report = _load_exact_report(paths["assembly_report"], ASSEMBLY_SCHEMA)
        admission_report = _load_exact_report(
            paths["admission_report"], "ganesh-mini-capability-qualification-admission/v1",
        )
        expected_status = "qualification-passed" if admission_report.get("status") == "passed" else "qualification-failed"
        if (
            report.get("assembly_report_sha256") != assembly_report["report_sha256"]
            or report.get("admission_report_sha256") != admission_report["report_sha256"]
            or report.get("status") != expected_status
        ):
            raise ValueError("existing campaign does not bind its nested reports")
        return report

    if not {row["id"] for row in queue_rows}.issubset(queue_by_id):
        raise ValueError("teacher and admission queue validation disagree")

    assembly_preexisting = paths["envelopes"].exists() and paths["assembly_report"].exists()
    envelopes, assembly_report = _load_or_build_assembly(
        output_path=paths["envelopes"], report_path=paths["assembly_report"], bindings=bindings,
        queue_by_id=queue_by_id, candidate_paths=candidate_paths, evidence_paths=evidence_paths,
        queue_path=queue_path, queue_manifest=queue_manifest, semantic=semantic, separation=separation,
        correction_report_path=correction_report_path,
    )
    existing = _load_existing_admission(
        paths["envelopes"], paths["admitted"], paths["rejected"], paths["admission_report"],
    )
    if existing is None:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        admitted, rejected = admit_qualification(
            envelopes, plan, queue_by_id, config, runtime_config_path, verifier_fn,
            verifier_workers=verifier_workers, record_workers=record_workers,
        )
        paths["admitted"].write_bytes(b"".join(canonical_json(row) + b"\n" for row in admitted))
        paths["rejected"].write_text(json.dumps(rejected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        admission_report = build_admission_report(
            mode="final", plan=plan, queue_manifest=queue_manifest,
            input_path=paths["envelopes"], output_path=paths["admitted"], rejected_path=paths["rejected"],
            admitted=admitted, rejected=rejected,
            verifier_workers=verifier_workers, record_workers=record_workers,
            queue_by_id=queue_by_id,
        )
        paths["admission_report"].write_text(json.dumps(admission_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        admission_reused = False
    else:
        _, _, admission_report = existing
        admission_reused = True
    report = _campaign_report(
        bindings, assembly_report, admission_report, paths,
        reused_assembly=assembly_preexisting, reused_admission=admission_reused,
    )
    paths["campaign_report"].write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-manifest", type=Path, required=True)
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--teacher-evidence-dir", type=Path, required=True)
    parser.add_argument("--semantic-review", type=Path, required=True)
    parser.add_argument("--separation-report", type=Path, required=True)
    parser.add_argument("--correction-report", type=Path)
    parser.add_argument("--replacement-manifest", type=Path)
    parser.add_argument("--config", type=Path, default=Path("configs/data/expansion_v1.json"))
    parser.add_argument("--runtime-config", type=Path, default=Path("configs/eval/runtimes.json"))
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--record-workers", type=int, default=4)
    parser.add_argument("--verifier-workers", type=int, default=2)
    args = parser.parse_args()
    report = run_campaign(
        plan_path=args.plan, queue_path=args.queue, queue_manifest_path=args.queue_manifest,
        candidate_dir=args.candidate_dir, evidence_dir=args.teacher_evidence_dir,
        semantic_path=args.semantic_review, separation_path=args.separation_report,
        config_path=args.config, runtime_config_path=args.runtime_config,
        correction_report_path=args.correction_report,
        replacement_manifest_path=args.replacement_manifest,
        output_root=args.output_root, record_workers=args.record_workers,
        verifier_workers=args.verifier_workers,
    )
    print(json.dumps({
        "status": report["status"], "report_sha256": report["report_sha256"],
        "outputs": {name: binding["path"] for name, binding in report["outputs"].items()},
    }, sort_keys=True))
    return 0 if report["status"] == "qualification-passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
