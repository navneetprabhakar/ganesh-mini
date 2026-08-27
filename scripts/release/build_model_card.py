#!/usr/bin/env python3
"""Build the final Hugging Face model card strictly from sealed release evidence."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from scripts.release.adjudicate import LANES, QWEN_MODEL_ID, QWEN_REVISION, comparison_contract
from scripts.release.publish_huggingface import load_sealed, verified_release_inputs


DISPLAY = {
    "go": "Go",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "python": "Python",
    "rust": "Rust",
}


def require_check(decision: dict[str, Any], name: str) -> dict[str, Any]:
    rows = [row for row in decision.get("checks", []) if row.get("name") == name]
    if len(rows) != 1 or rows[0].get("passed") is not True:
        raise ValueError(f"release decision is missing passed check: {name}")
    return rows[0]


def validate_inputs(
    *,
    decision_path: Path,
    artifact_manifest_path: Path,
    export_equivalence_path: Path,
    qwen_comparison_path: Path,
    ganesh_v01_comparison_path: Path,
    quant_comparison_path: Path,
    laptop_path: Path,
) -> tuple[dict[str, Any], ...]:
    decision, artifacts, export = verified_release_inputs(
        decision_path, artifact_manifest_path, export_equivalence_path
    )
    comparisons = [
        load_sealed(qwen_comparison_path, "report_sha256"),
        load_sealed(ganesh_v01_comparison_path, "report_sha256"),
        load_sealed(quant_comparison_path, "report_sha256"),
    ]
    if not all(comparison_contract(value)[0] for value in comparisons):
        raise ValueError("model card comparison does not satisfy the final decision contract")
    laptop = load_sealed(laptop_path, "evidence_sha256")
    comparison_check = require_check(decision, "sealed_complete_decision_comparisons")["evidence"]
    expected = [
        comparison_check["qwen"]["report_sha256"],
        comparison_check["ganesh_v01"]["report_sha256"],
        comparison_check["quantization"]["report_sha256"],
    ]
    if [value["report_sha256"] for value in comparisons] != expected:
        raise ValueError("model card comparisons are not bound by the release decision")
    laptop_check = require_check(decision, "laptop_evidence_and_artifacts_bound")
    if laptop_check["evidence"].get("laptop_evidence_sha256") != laptop["evidence_sha256"]:
        raise ValueError("model card laptop evidence is not bound by the release decision")
    qwen, v01, quant = comparisons
    if (
        qwen["base_model"].get("model_id") != QWEN_MODEL_ID
        or qwen["base_model"].get("revision") != QWEN_REVISION
        or qwen["candidate_model"] != v01["candidate_model"]
    ):
        raise ValueError("model card model identities are inconsistent")
    return decision, artifacts, export, qwen, v01, quant, laptop


def percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def gib(value: int) -> str:
    return f"{value / 1024**3:.2f} GiB"


def render_model_card(
    decision: dict[str, Any],
    artifacts: dict[str, Any],
    export: dict[str, Any],
    qwen: dict[str, Any],
    v01: dict[str, Any],
    quant: dict[str, Any],
    laptop: dict[str, Any],
) -> str:
    rows = []
    for lane in LANES:
        base = qwen["base"]["lanes"][lane]
        candidate = qwen["candidate"]["lanes"][lane]
        rows.append(f"| {DISPLAY[lane]} | {base['passed']}/60 | {candidate['passed']}/60 | {candidate['passed'] - base['passed']:+d} |")
    qwen_macro = qwen["base"]["five_family_macro"]["decimal"]
    mini_macro = qwen["candidate"]["five_family_macro"]["decimal"]
    v01_macro = v01["base"]["five_family_macro"]["decimal"]
    paired = qwen["paired"]
    aggregate = paired["aggregate"]
    cluster = paired["cluster_aware"]
    merged_solved = sum(quant["base"]["lanes"][lane]["passed"] for lane in LANES)
    q8_solved = sum(quant["candidate"]["lanes"][lane]["passed"] for lane in LANES)
    retention = q8_solved / merged_solved if merged_solved else 1.0
    release_artifacts = artifacts["artifacts"]
    q8 = laptop["profiles"]["q8"]
    f16 = laptop["profiles"]["f16"]
    v01_relation = (
        f"Ganesh v0.1 remains ahead by {percent(v01_macro - mini_macro)} on the five-family macro."
        if v01_macro > mini_macro
        else f"Ganesh Mini is ahead of Ganesh v0.1 by {percent(mini_macro - v01_macro)} on the five-family macro."
        if mini_macro > v01_macro
        else "Ganesh Mini and Ganesh v0.1 tie on the five-family macro."
    )
    return "\n".join([
        "---",
        "library_name: transformers",
        "license: apache-2.0",
        f"base_model: {QWEN_MODEL_ID}",
        "base_model_relation: finetune",
        "pipeline_tag: image-text-to-text",
        "tags:",
        "- code",
        "- text-only",
        "- go",
        "- java",
        "- javascript",
        "- typescript",
        "- python",
        "- rust",
        "- gguf",
        "---",
        "",
        "# Ganesh Mini 1.0",
        "",
        "Ganesh Mini 1.0 is a text-only, non-thinking coding specialization of",
        f"`{QWEN_MODEL_ID}` at revision `{QWEN_REVISION}`. It targets Go, Java,",
        "JavaScript, TypeScript, Python, and Rust with an 8,192-token serving contract.",
        "",
        "## Artifacts",
        "",
        f"- Merged BF16 Hugging Face checkpoint: `{release_artifacts['merged_bf16_hf']['sha256']}`",
        f"- GGUF F16: {gib(release_artifacts['gguf_f16']['bytes'])}, `{release_artifacts['gguf_f16']['sha256']}`",
        f"- GGUF Q8_0: {gib(release_artifacts['gguf_q8']['bytes'])}, `{release_artifacts['gguf_q8']['sha256']}`",
        "",
        "## Frozen decision evaluation",
        "",
        "The private decision suite contains 360 execution-verified tasks: 60 per compiler lane.",
        "JavaScript and TypeScript each receive half-weight in the five-family macro.",
        "",
        "| Lane | Qwen base | Ganesh Mini | Delta |",
        "|---|---:|---:|---:|",
        *rows,
        "",
        f"Five-family macro: {percent(qwen_macro)} base → {percent(mini_macro)} Ganesh Mini ({percent(mini_macro - qwen_macro)} delta).",
        f"Paired outcomes: {aggregate['wins']} wins, {aggregate['losses']} losses, {aggregate['ties']} ties of {aggregate['denominator']} tasks.",
        f"Cluster-aware 95% bootstrap interval: [{cluster['bootstrap_ci']['lower']:.4f}, {cluster['bootstrap_ci']['upper']:.4f}]; two-sided sign-permutation p={cluster['two_sided_permutation_p']:.6f}.",
        "",
        "## Ganesh v0.1 reference",
        "",
        f"Fresh identical-harness five-family macro: {percent(v01_macro)} for Ganesh v0.1 versus {percent(mini_macro)} for Ganesh Mini. {v01_relation}",
        "Ganesh v0.1 uses a different 12B backbone and resource envelope, so it is a reference competitor rather than the causal baseline.",
        "",
        "## Quantization and laptop certification",
        "",
        f"Q8_0 retained {q8_solved}/{merged_solved} solved decision tasks ({percent(retention)}).",
        f"The 8 GB Q8 profile passed at 8,192 context with peak RSS {gib(q8['peak_rss_bytes'])} (7 GiB ceiling).",
        f"The 16 GB F16 profile passed at 8,192 context with peak RSS {gib(f16['peak_rss_bytes'])} (14 GiB ceiling).",
        f"Six-lane BF16/F16/Q8 export equivalence passed under evidence seal `{export['evidence_sha256']}`.",
        "",
        "## Training and provenance",
        "",
        "The authorized Ganesh v0.1 corpus is the preserved seed dataset. Exact source revision,",
        "record lineage, compatibility, evaluation-separation, prepared-data, execution-card,",
        "selected-run, comparison, artifact, and laptop seals are included under `evidence/`.",
        "Private evaluation prompts, tests, raw outputs, and generated code are intentionally not published.",
        "",
        "## Limitations",
        "",
        "- The release claim covers text-only, non-thinking inference at 8,192 context; vision and the upstream 262k context are not certified.",
        "- Results measure single-task executable coding correctness on the frozen six-lane harness, not repository-scale agent performance.",
        f"- {v01_relation}",
        "- Generated code may be incorrect or insecure and must be reviewed and sandboxed before execution.",
        "",
        "## Evidence identity",
        "",
        f"Release decision: `{decision['evidence_sha256']}`  ",
        f"Artifact manifest: `{artifacts['manifest_sha256']}`  ",
        f"Export equivalence: `{export['evidence_sha256']}`",
        "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-decision", type=Path, required=True)
    parser.add_argument("--artifact-manifest", type=Path, required=True)
    parser.add_argument("--export-equivalence", type=Path, required=True)
    parser.add_argument("--qwen-comparison", type=Path, required=True)
    parser.add_argument("--ganesh-v01-comparison", type=Path, required=True)
    parser.add_argument("--quant-comparison", type=Path, required=True)
    parser.add_argument("--laptop-certification", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values = validate_inputs(
        decision_path=args.release_decision,
        artifact_manifest_path=args.artifact_manifest,
        export_equivalence_path=args.export_equivalence,
        qwen_comparison_path=args.qwen_comparison,
        ganesh_v01_comparison_path=args.ganesh_v01_comparison,
        quant_comparison_path=args.quant_comparison,
        laptop_path=args.laptop_certification,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_model_card(*values), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
