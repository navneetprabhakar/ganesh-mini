from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.repair_delta_v5_contract import (
    BUDGET_ADDENDUM_SHA256,
    CONTRACT_ID,
    EFFECTIVE_MAX_RESERVES,
    PLAN_SHA256,
    SOURCE_ADDENDUM_SHA256,
    UNRESERVED_CELL,
    cohort_binding,
    load_v5_contract,
    validate_terminal_order,
)
from scripts.data.summarize_repair_delta_qualification import (
    FIRST_PASS, cohort_state, file_sha256,
)


ROOT = Path(__file__).resolve().parents[2]
COHORT_ROOT = ROOT / "measurement/gate2/capability-stratified-v5-interface-replay/cohort-v1"
ASSEMBLY_SCHEMA = "ganesh-mini-repair-delta-v5-evidence-assembly/v1"


def contract() -> dict:
    return load_v5_contract(
        plan_path=ROOT / "docs/plans/GATE2_REPAIR_DELTA_V5_INTERFACE_REPLAY_PLAN_20260916.md",
        source_addendum_path=ROOT / "docs/plans/GATE2_V5_SOURCE_FEASIBILITY_ADDENDUM_20260916.md",
        budget_addendum_path=ROOT / "docs/plans/GATE2_V5_BUDGET_CLARIFICATION_ADDENDUM_20260916.md",
        exclusion_path=COHORT_ROOT / "exclusion-ledger.json",
        carry_path=COHORT_ROOT / "carry-manifest.json",
        source_path=COHORT_ROOT / "source-manifest.json",
        cohort_path=COHORT_ROOT / "cohort-manifest.json",
    )


def eligibility(tmp_path: Path, cells: list[str]) -> Path:
    primary_by_cell = {row["cell_id"]: row["candidate_id"] for row in contract()["primary_rows"]}
    value = {
        "schema_version": "ganesh-mini-repair-delta-v5-reserve-eligibility/v1",
        "contract_id": CONTRACT_ID, "plan_sha256": PLAN_SHA256,
        "source_feasibility_addendum_sha256": SOURCE_ADDENDUM_SHA256,
        "budget_clarification_addendum_sha256": BUDGET_ADDENDUM_SHA256,
        "cohort_manifest_sha256": contract()["cohort_manifest_sha256"],
        "source_manifest_sha256": contract()["source_manifest_sha256"],
        "first_pass_thresholds_passed": True,
        "rejected_candidate_ids": [primary_by_cell[cell] for cell in cells],
        "rejected_cell_ids": cells, "reserves_authorized": len(cells),
        "evaluation_artifacts_read": 0,
    }
    value["eligibility_sha256"] = canonical_sha256(value)
    path = tmp_path / "eligibility.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_v5_contract_binds_58_carries_two_fresh_and_59_reserves() -> None:
    loaded = contract()
    primary = cohort_binding(loaded, "primary")
    assert primary["records"] == 60
    assert sum(row["mode"] == "immutable-v4-teacher-carry" for row in loaded["primary_rows"]) == 58
    assert sum(row["mode"] == "fresh-v5-teacher-primary" for row in loaded["primary_rows"]) == 2
    assert len(loaded["reserve_rows"]) == 59
    assert UNRESERVED_CELL not in {row["cell_id"] for row in loaded["reserve_rows"]}
    assert loaded["effective_max_reserves"] == EFFECTIVE_MAX_RESERVES == 5


def test_v5_terminal_accounting_is_exact_and_ordered() -> None:
    binding = cohort_binding(contract(), "primary")
    rows = [{
        "schema_version": ASSEMBLY_SCHEMA, "candidate_id": identifier,
        "status": ("ready-for-admission", "terminal-rejected", "unresolved")[index % 3],
    } for index, identifier in enumerate(binding["ordered_candidate_ids"])]
    validate_terminal_order(rows, binding["ordered_candidate_ids"], ASSEMBLY_SCHEMA)
    with pytest.raises(ValueError, match="exact bound cohort"):
        validate_terminal_order(rows[:-1], binding["ordered_candidate_ids"], ASSEMBLY_SCHEMA)
    rows[0], rows[1] = rows[1], rows[0]
    with pytest.raises(ValueError, match="preserve bound cohort order"):
        validate_terminal_order(rows, binding["ordered_candidate_ids"], ASSEMBLY_SCHEMA)


def test_v5_reserve_binding_enforces_budget_and_unreserved_exception(tmp_path: Path) -> None:
    loaded = contract()
    eligible_cells = [row["cell_id"] for row in loaded["reserve_rows"][:5]]
    binding = cohort_binding(loaded, "reserve", eligibility(tmp_path, eligible_cells))
    assert binding["records"] == 5
    assert binding["absolute_terminal_candidate_budget"] == 65
    assert binding["absolute_new_teacher_generation_budget"] == 7

    with pytest.raises(ValueError, match="amended budgets"):
        cohort_binding(
            loaded, "reserve",
            eligibility(tmp_path, [row["cell_id"] for row in loaded["reserve_rows"][:6]]),
        )
    with pytest.raises(ValueError, match="amended budgets"):
        cohort_binding(loaded, "reserve", eligibility(tmp_path, [UNRESERVED_CELL]))


def test_v5_qualification_accounting_reconciles_rejected_and_unresolved(tmp_path: Path) -> None:
    loaded = contract()
    expected = {}
    assemblies = []
    rejected = []
    unresolved = []
    for index, row in enumerate(loaded["primary_rows"]):
        expected[row["candidate_id"]] = {
            "id": row["candidate_id"], "cell_id": row["cell_id"],
            "lane": row["lane"], "primary_capability": row["primary_capability"],
            "assigned_cross_cutting_dimension": row["assigned_cross_cutting_dimension"],
            "task_type": "repair", "cohort": FIRST_PASS, "contract_id": CONTRACT_ID,
        }
        status = "unresolved" if index == 0 else "terminal-rejected"
        artifact = {
            "schema_version": ASSEMBLY_SCHEMA, "status": status,
            "candidate_id": row["candidate_id"], "cell_id": row["cell_id"],
            "evaluation_artifacts_read": 0,
        }
        artifact["artifact_sha256"] = canonical_sha256(artifact)
        assemblies.append(artifact)
        target = unresolved if status == "unresolved" else rejected
        target.append({"id": row["candidate_id"]})
    envelope_path = tmp_path / "terminal.jsonl"
    envelope_path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in assemblies),
        encoding="utf-8",
    )
    admitted_path = tmp_path / "admitted.jsonl"; admitted_path.write_text("")
    rejected_path = tmp_path / "rejected.json"; rejected_path.write_text(json.dumps(rejected))
    unresolved_path = tmp_path / "unresolved.json"; unresolved_path.write_text(json.dumps(unresolved))
    report = {
        "schema_version": "ganesh-mini-repair-delta-v5-admission-report/v1",
        "status": "failed", "contract_id": CONTRACT_ID,
        "input": {"path": str(envelope_path), "sha256": file_sha256(envelope_path),
                  "bytes": envelope_path.stat().st_size},
        "runtime_config_sha256": "1" * 64, "admission_config_sha256": "2" * 64,
        "sandbox_contract_sha256": "3" * 64, "separation_contract_sha256": "4" * 64,
        "accepted": 0, "rejected": 59, "unresolved": 1, "counts_by_lane": {},
        "evaluation_artifacts_read": 0,
        "outputs": {
            "admitted": {"path": str(admitted_path), "sha256": file_sha256(admitted_path),
                         "bytes": admitted_path.stat().st_size},
            "rejected": {"path": str(rejected_path), "sha256": file_sha256(rejected_path),
                         "bytes": rejected_path.stat().st_size},
            "unresolved": {"path": str(unresolved_path), "sha256": file_sha256(unresolved_path),
                           "bytes": unresolved_path.stat().st_size},
        },
    }
    report["v5_cohort_binding"] = cohort_binding(loaded, "primary")
    report["report_sha256"] = canonical_sha256(report)
    report_path = tmp_path / "report.json"; report_path.write_text(json.dumps(report))
    state, dispositions, _ = cohort_state(
        envelope_path, report_path, expected, FIRST_PASS, "v5",
        loaded["ordered_primary_ids"],
    )
    assert state["generated"] == 60
    assert state["rejected"] == 59
    assert state["unresolved"] == 1
    assert len(dispositions) == 60
