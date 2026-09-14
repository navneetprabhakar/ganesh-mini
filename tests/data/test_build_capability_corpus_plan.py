import hashlib
import json

from scripts.data.build_capability_corpus_plan import (
    CAPABILITIES,
    LANES,
    TASK_TYPES,
    build,
    canonical_sha256,
    cell_contracts,
)


def sealed(path, value, field):
    value[field] = canonical_sha256(value)
    path.write_text(json.dumps(value))


def evidence(tmp_path):
    diversity = tmp_path / "diversity.json"
    campaign = tmp_path / "campaign.json"
    sealed(diversity, {
        "schema_version": "ganesh-mini-training-corpus-diversity-audit/v1",
        "status": "complete-non-evaluation-audit",
        "scope": {"evaluation_surfaces_read": 0},
        "corpus": {"records": 3225},
        "selected_probe": {"records": 640},
    }, "report_sha256")
    sealed(campaign, {
        "schema_version": "ganesh-mini-expansion-campaign-result/v1",
        "status": "completed-gradient-audit-no-conflict",
    }, "evidence_sha256")
    return diversity, campaign


def test_matrix_covers_every_capability_lane_and_type_once() -> None:
    cells = cell_contracts()
    assert len(cells) == len(CAPABILITIES) * len(LANES) * len(TASK_TYPES) == 120
    assert len({cell["cell_id"] for cell in cells}) == 120
    assert all(cell["qualification_drafts"] == 2 for cell in cells)
    assert all(cell["pilot_minimum_admitted"] == 6 for cell in cells)


def test_build_seals_non_executable_contract(tmp_path) -> None:
    diversity, campaign = evidence(tmp_path)
    plan = build(diversity, campaign)
    claimed = plan.pop("plan_sha256")
    assert claimed == canonical_sha256(plan)
    assert plan["matrix"]["cells"] == 120
    assert plan["qualification"]["drafts"] == 240
    assert plan["pilot_corpus_target"]["total_records"] == 900
    assert plan["status"] == "local-contract-sealed-qualification-implementation-next"
    assert plan["gcloud_authority"] == "none"
    assert plan["training_authority"] == "none"


def test_tampered_evidence_fails_closed(tmp_path) -> None:
    diversity, campaign = evidence(tmp_path)
    value = json.loads(diversity.read_text())
    value["corpus"]["records"] = 1
    diversity.write_text(json.dumps(value))
    try:
        build(diversity, campaign)
    except ValueError as exc:
        assert "invalid report_sha256" in str(exc)
    else:
        raise AssertionError("tampered evidence must fail closed")
