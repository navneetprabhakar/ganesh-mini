import hashlib
import json

from scripts.data.build_capability_corpus_plan import CAPABILITIES, LANES, TASK_TYPES, canonical_sha256, cell_contracts
from scripts.data.build_capability_qualification_queue import build, canonical_json


def write_jsonl(path, rows):
    path.write_bytes(b"".join(canonical_json(row) + b"\n" for row in rows))


def source_row(identifier, lane, task_type, source_id):
    return {
        "id": identifier,
        "lane": lane,
        "task_type": task_type,
        "source": {"dataset": "source", "revision": "rev", "record_id": source_id},
        "stimulus": f"stimulus {identifier}",
    }


def fixture(tmp_path):
    plan_path = tmp_path / "plan.json"
    plan = {
        "schema_version": "ganesh-mini-capability-stratified-corpus-plan/v1",
        "status": "local-contract-sealed-qualification-implementation-next",
        "matrix": {"cells": 120, "cell_contracts": cell_contracts()},
        "qualification": {"drafts": 240},
        "ontology": {"primary_capabilities": CAPABILITIES},
    }
    plan["plan_sha256"] = canonical_sha256(plan)
    plan_path.write_text(json.dumps(plan))
    source_path = tmp_path / "sources.jsonl"
    sources = []
    for lane in LANES:
        for task_type in TASK_TYPES:
            for index in range(25):
                sources.append(source_row(f"{lane}-{task_type}-{index}", lane, task_type, f"{lane}-{task_type}-{index}"))
    write_jsonl(source_path, sources)
    prior_path = tmp_path / "prior.jsonl"
    write_jsonl(prior_path, [source_row("prior", "go", "generation", "go-generation-0")])
    return plan_path, source_path, prior_path


def test_build_is_deterministic_complete_and_excludes_prior_sources(tmp_path) -> None:
    plan, sources, prior = fixture(tmp_path)
    first, manifest = build(plan, sources, prior)
    second, repeated = build(plan, sources, prior)
    assert first == second
    assert manifest == repeated
    assert len(first) == 240
    assert len({row["cell_id"] for row in first}) == 120
    assert len({(row["source"]["dataset"], row["source"]["revision"], row["source"]["record_id"]) for row in first}) == 240
    assert all(row["source"]["record_id"] != "go-generation-0" for row in first)
    assert manifest["selection"]["evaluation_surfaces_read"] == 0
    claimed = manifest.pop("manifest_sha256")
    assert claimed == canonical_sha256(manifest)


def test_queue_hash_binds_canonical_rows(tmp_path) -> None:
    plan, sources, prior = fixture(tmp_path)
    rows, manifest = build(plan, sources, prior)
    payload = b"".join(canonical_json(row) + b"\n" for row in rows)
    assert hashlib.sha256(payload).hexdigest() == manifest["queue_sha256"]


def test_insufficient_sources_fails_closed(tmp_path) -> None:
    plan, sources, prior = fixture(tmp_path)
    rows = [row for row in (json.loads(line) for line in sources.read_text().splitlines()) if row["lane"] != "go"]
    write_jsonl(sources, rows)
    try:
        build(plan, sources, prior)
    except ValueError as exc:
        assert "insufficient unused training sources" in str(exc)
    else:
        raise AssertionError("missing lane sources must fail closed")
