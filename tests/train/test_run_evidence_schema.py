import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_executed_repaired_recipe_run_matches_current_schema() -> None:
    schema = json.loads((ROOT / "schemas/train/run-evidence.schema.json").read_text())
    run = json.loads((
        ROOT / "measurement/gate3/gcloud/20260827T090603Z/finalization/terminal-download/"
        "output/campaign/training/lr-1e-5/run-evidence.json"
    ).read_text())
    assert schema["$id"] == "ganesh-mini-sft-run/v2"
    assert schema["properties"]["schema_version"]["const"] == run["schema_version"]
    assert set(schema["required"]) <= set(run)
    assert set(run) <= set(schema["properties"])
    assert set(schema["properties"]["identities"]["required"]) <= set(run["identities"])
    assert set(schema["$defs"]["validation"]["required"]) <= set(run["validation_loss_diagnostic"])


def test_obsolete_v1_run_is_not_release_schema_compatible() -> None:
    schema = json.loads((ROOT / "schemas/train/run-evidence.schema.json").read_text())
    assert schema["properties"]["schema_version"]["const"] != "ganesh-mini-sft-run/v1"
