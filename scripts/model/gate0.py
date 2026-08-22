#!/usr/bin/env python3
"""Fail-closed Gate 0 checks for the pinned Ganesh Mini upstream model.

This module deliberately uses only the Python standard library. It must remain
usable before the provisional ML dependency matrix is installed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
MATRIX = {
    "torch": ("2.7", "3"),
    "transformers": ("5.9", "6"),
    "peft": ("0.18", "0.21"),
    "ms-swift": ("4.5", "5"),
    "qwen-vl-utils": ("0.0.14", "0.1"),
    "flash-linear-attention": ("0.4.2", "0.6"),
    "causal-conv1d": ("1.5", "2"),
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(value: Any, path: Path | None) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_oid(path: Path) -> str:
    size = path.stat().st_size
    digest = hashlib.sha1(f"blob {size}\0".encode())  # noqa: S324 - Git object identity
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.match(r"^(\d+(?:\.\d+)*)", value)
    return tuple(int(part) for part in match.group(1).split(".")) if match else ()


def version_in_range(value: str, lower: str, upper: str) -> bool:
    current = version_tuple(value)
    return bool(current) and current >= version_tuple(lower) and current < version_tuple(upper)


def check(name: str, passed: bool, detail: str, **evidence: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail, "evidence": evidence}


def validate_contract_inventory(contract: dict[str, Any], inventory: dict[str, Any]) -> list[dict[str, Any]]:
    files = inventory.get("files")
    files = files if isinstance(files, list) else []
    paths = [item.get("path") for item in files if isinstance(item, dict)]
    sizes_known = all(isinstance(item.get("size"), int) and item["size"] >= 0 for item in files)
    calculated_total = sum(item["size"] for item in files) if sizes_known else None
    identities_known = all(
        bool(SHA40.fullmatch(str(item.get("git_oid", ""))))
        and ("sha256" not in item or bool(SHA256.fullmatch(str(item["sha256"]))))
        for item in files
    )
    byte_groups = inventory.get("byte_groups", {})
    groups_known = set(byte_groups) == {
        "model_weights",
        "tokenizer_and_chat_template",
        "vision_processor",
        "repository_metadata",
    } and all(isinstance(value, int) and value >= 0 for value in byte_groups.values())
    required = contract.get("required_files", [])
    threshold = contract.get("download_approval_threshold_bytes")
    return [
        check(
            "model_identity",
            contract.get("model_id") == inventory.get("model_id")
            and contract.get("revision") == inventory.get("revision")
            and bool(SHA40.fullmatch(str(contract.get("revision", "")))),
            "Model ID and immutable 40-hex revision must match.",
            model_id=inventory.get("model_id"),
            revision=inventory.get("revision"),
        ),
        check(
            "license",
            str(contract.get("license", "")).lower() == str(inventory.get("license", "")).lower(),
            "Pinned inventory license must match the contract.",
            license=inventory.get("license"),
        ),
        check(
            "expected_files",
            bool(files) and len(paths) == len(set(paths)) and all(path in paths for path in required),
            "Inventory must be non-empty, unique, and contain every required artifact.",
            file_count=len(paths),
            missing=sorted(set(required) - set(paths)),
        ),
        check(
            "known_download_bytes",
            sizes_known
            and identities_known
            and groups_known
            and calculated_total == inventory.get("total_bytes")
            and sum(byte_groups.values()) == calculated_total,
            "Every file identity and size, the model/processor groups, and exact aggregate must be recorded before download.",
            calculated_total=calculated_total,
            recorded_total=inventory.get("total_bytes"),
            byte_groups=byte_groups,
            identities_known=identities_known,
        ),
        check(
            "download_approval_boundary",
            isinstance(threshold, int)
            and isinstance(calculated_total, int)
            and calculated_total <= threshold,
            "Aggregate bytes above the configured boundary require explicit approval.",
            threshold_bytes=threshold,
            total_bytes=calculated_total,
            approval_required=isinstance(calculated_total, int)
            and isinstance(threshold, int)
            and calculated_total > threshold,
        ),
    ]


def byte_groups(files: list[dict[str, Any]]) -> dict[str, int]:
    tokenizer_files = {"chat_template.jinja", "merges.txt", "tokenizer.json", "tokenizer_config.json", "vocab.json"}
    processor_files = {"preprocessor_config.json", "video_preprocessor_config.json"}
    groups = {
        "model_weights": 0,
        "tokenizer_and_chat_template": 0,
        "vision_processor": 0,
        "repository_metadata": 0,
    }
    for item in files:
        path, size = item["path"], item["size"]
        if path.endswith(".safetensors"):
            groups["model_weights"] += size
        elif path in tokenizer_files:
            groups["tokenizer_and_chat_template"] += size
        elif path in processor_files:
            groups["vision_processor"] += size
        else:
            groups["repository_metadata"] += size
    return groups


def validate_local_files(model_dir: Path, inventory: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in inventory["files"]:
        path = model_dir / item["path"]
        if not path.is_file():
            results.append({"path": item["path"], "passed": False, "reason": "missing"})
            continue
        size_ok = path.stat().st_size == item["size"]
        if item.get("sha256"):
            identity = file_sha256(path)
            identity_ok = identity == item["sha256"]
            method = "sha256"
        else:
            identity = git_blob_oid(path)
            identity_ok = identity == item.get("git_oid")
            method = "git_blob_sha1"
        results.append(
            {
                "path": item["path"],
                "passed": size_ok and identity_ok,
                "size_ok": size_ok,
                "identity_method": method,
                "identity": identity,
            }
        )
    return results


def validate_architecture(config: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    text = config.get("text_config", config)
    layer_types = text.get("layer_types", [])
    observed_counts = dict(Counter(layer_types))
    fields = {
        "outer_model_type": config.get("model_type"),
        "text_model_type": text.get("model_type"),
        "num_hidden_layers": text.get("num_hidden_layers"),
        "vocab_size": text.get("vocab_size"),
        "attention_pattern_counts": observed_counts,
    }
    return {
        "passed": fields == expected,
        "expected": expected,
        "observed": fields,
        "config_sha256": canonical_digest(config),
    }


def package_matrix() -> dict[str, Any]:
    packages: list[dict[str, Any]] = []
    for name, (lower, upper) in MATRIX.items():
        try:
            version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            version = None
        packages.append(
            {
                "name": name,
                "version": version,
                "required": f">={lower},<{upper}",
                "passed": version is not None and version_in_range(version, lower, upper),
            }
        )
    return {
        "python": platform.python_version(),
        "python_passed": (3, 12) <= sys.version_info[:2] < (3, 14),
        "packages": packages,
        "passed": (3, 12) <= sys.version_info[:2] < (3, 14)
        and all(item["passed"] for item in packages),
    }


def inspect_lora(catalog: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    modules = catalog.get("modules", [])
    revision_ok = catalog.get("model_id") == contract["model_id"] and catalog.get("revision") == contract["revision"]
    language_linears = []
    excluded = []
    for module in modules:
        name = str(module.get("name", ""))
        kind = str(module.get("type", ""))
        is_vision = any(part in name.split(".") for part in ("visual", "vision_model", "vision_tower"))
        is_linear = kind in {"Linear", "torch.nn.Linear", "bitsandbytes.nn.Linear4bit"}
        if is_linear and not is_vision and not name.endswith("lm_head"):
            language_linears.append(module)
        elif is_linear:
            excluded.append(module)
    suffix_counts = Counter(str(item["name"]).split(".")[-1] for item in language_linears)
    total = sum(int(item.get("num_parameters", 0)) for item in language_linears)
    targeted = [item for item in language_linears if item.get("lora_targeted") is True]
    trainable = sum(int(item.get("adapter_trainable_parameters", 0)) for item in targeted)
    gradient_coverage_verified = (
        bool(targeted)
        and catalog.get("gradient_probe_passed") is True
        and trainable > 0
        and all(item.get("adapter_gradient_observed") is True for item in targeted)
    )
    return {
        "schema_version": 1,
        "model_id": catalog.get("model_id"),
        "revision": catalog.get("revision"),
        "runtime_verified": revision_ok and catalog.get("source_kind") == "runtime_named_modules",
        "gradient_coverage_verified": gradient_coverage_verified,
        "candidate_target_suffixes": dict(sorted(suffix_counts.items())),
        "language_linear_module_count": len(language_linears),
        "targeted_language_linear_module_count": len(targeted),
        "excluded_linear_module_count": len(excluded),
        "language_linear_parameters": total,
        "lora_trainable_parameters": trainable,
        "catalog_sha256": canonical_digest(catalog),
    }


def evidence_check(name: str, path: Path | None, contract: dict[str, Any]) -> dict[str, Any]:
    if path is None or not path.is_file():
        return check(name, False, "Required executed evidence is absent.", path=str(path) if path else None)
    try:
        value = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return check(name, False, f"Evidence is unreadable: {exc}", path=str(path))
    passed = (
        value.get("passed") is True
        and value.get("model_id") == contract["model_id"]
        and value.get("revision") == contract["revision"]
        and bool(SHA256.fullmatch(str(value.get("evidence_sha256", ""))))
    )
    return check(name, passed, "Evidence must pass, match the pin, and carry a SHA-256 evidence identity.", path=str(path))


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    contract = load_json(args.contract)
    inventory = load_json(args.inventory)
    checks = validate_contract_inventory(contract, inventory)

    if args.model_dir:
        local_results = validate_local_files(args.model_dir, inventory)
        checks.append(check("local_inventory", all(item["passed"] for item in local_results), "All local files must match pinned identities.", files=local_results))
        config_path = args.model_dir / "config.json"
        architecture = validate_architecture(load_json(config_path), contract["architecture"]) if config_path.is_file() else {"passed": False, "reason": "config.json missing"}
        checks.append(check("architecture", architecture["passed"], "Local architecture must match the pinned contract.", result=architecture))
        template_path = args.model_dir / contract["serving_contract"]["chat_template_source"]
        template_ok = template_path.is_file() and bool(template_path.read_text(encoding="utf-8").strip())
        checks.append(check("chat_template", template_ok, "Pinned non-empty upstream chat template must be present.", path=str(template_path), sha256=file_sha256(template_path) if template_ok else None))
    else:
        checks.extend(
            [
                check("local_inventory", False, "No local model directory was supplied."),
                check("architecture", False, "No local model config was supplied."),
                check("chat_template", False, "No local chat template was supplied."),
            ]
        )

    matrix = package_matrix()
    checks.append(check("dependency_matrix", matrix["passed"], "Python and candidate packages must be installed within declared bounds.", matrix=matrix))
    lock_ok = args.lock_file is not None and args.lock_file.is_file() and args.lock_file.stat().st_size > 0
    checks.append(check("exact_dependency_lock", lock_ok, "A non-empty exact dependency lock is required after compatibility is proven.", path=str(args.lock_file) if args.lock_file else None))

    if args.lora_report and args.lora_report.is_file():
        lora = load_json(args.lora_report)
        lora_ok = lora.get("runtime_verified") is True and lora.get("gradient_coverage_verified") is True and lora.get("revision") == contract["revision"]
    else:
        lora, lora_ok = {}, False
    checks.append(check("lora_targets_and_gradients", lora_ok, "Runtime module inspection and a successful gradient probe are required.", report=lora))
    checks.extend(
        [
            evidence_check("text_only_inference_smoke", args.inference_evidence, contract),
            evidence_check("train_save_reload_merge_smoke", args.training_evidence, contract),
            evidence_check("base_gguf_f16_q8_smoke", args.gguf_evidence, contract),
        ]
    )
    ready = all(item["passed"] for item in checks)
    report = {
        "schema_version": 1,
        "gate": 0,
        "status": "ready" if ready else "not_ready",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_id": contract["model_id"],
        "revision": contract["revision"],
        "contract_sha256": canonical_digest(contract),
        "inventory_sha256": canonical_digest(inventory),
        "checks": checks,
        "failed_checks": [item["name"] for item in checks if not item["passed"]],
    }
    report["report_sha256"] = canonical_digest(report)
    return report


def command_inventory(args: argparse.Namespace) -> int:
    contract = load_json(args.contract)
    raw = load_json(args.metadata)
    if isinstance(raw, list):
        files = [
            {
                "path": item.get("path"),
                "size": item.get("size"),
                "git_oid": item.get("oid"),
                **({"sha256": item["lfs"]["oid"]} if isinstance(item.get("lfs"), dict) and item["lfs"].get("oid") else {}),
            }
            for item in raw
            if item.get("type") == "file"
        ]
        inventory = {
            "schema_version": 1,
            "source": args.source,
            "model_id": contract["model_id"],
            "revision": contract["revision"],
            "license": args.license,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "byte_groups": byte_groups(files),
            "files": files,
            "total_bytes": sum(item["size"] for item in files if isinstance(item.get("size"), int)),
        }
    else:
        inventory = raw
    checks = validate_contract_inventory(contract, inventory)
    if not all(item["passed"] for item in checks):
        sys.stderr.write(json.dumps(checks, indent=2) + "\n")
        return 2
    dump_json(inventory, args.output)
    return 0


def command_lora(args: argparse.Namespace) -> int:
    result = inspect_lora(load_json(args.catalog), load_json(args.contract))
    dump_json(result, args.output)
    return 0 if result["runtime_verified"] else 2


def command_report(args: argparse.Namespace) -> int:
    report = build_report(args)
    dump_json(report, args.output)
    return 0 if report["status"] == "ready" else 2


def parser() -> argparse.ArgumentParser:
    root = Path(__file__).resolve().parents[2]
    default_contract = root / "configs/model/qwen3_5_2b.contract.json"
    default_inventory = root / "configs/model/qwen3_5_2b.inventory.json"
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)

    inventory = sub.add_parser("inventory", help="Normalize and validate supplied Hugging Face tree metadata")
    inventory.add_argument("--metadata", type=Path, required=True)
    inventory.add_argument("--contract", type=Path, default=default_contract)
    inventory.add_argument("--source", default="supplied-local-metadata")
    inventory.add_argument("--license", default="apache-2.0")
    inventory.add_argument("--output", type=Path)
    inventory.set_defaults(func=command_inventory)

    lora = sub.add_parser("inspect-lora", help="Inspect a supplied runtime named-module catalog")
    lora.add_argument("--catalog", type=Path, required=True)
    lora.add_argument("--contract", type=Path, default=default_contract)
    lora.add_argument("--output", type=Path)
    lora.set_defaults(func=command_lora)

    report = sub.add_parser("report", help="Write a fail-closed Gate 0 readiness report")
    report.add_argument("--contract", type=Path, default=default_contract)
    report.add_argument("--inventory", type=Path, default=default_inventory)
    report.add_argument("--model-dir", type=Path)
    report.add_argument("--lock-file", type=Path)
    report.add_argument("--lora-report", type=Path)
    report.add_argument("--inference-evidence", type=Path)
    report.add_argument("--training-evidence", type=Path)
    report.add_argument("--gguf-evidence", type=Path)
    report.add_argument("--output", type=Path)
    report.set_defaults(func=command_report)
    return cli


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"gate0: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
