import json
from decimal import Decimal
from pathlib import Path

from scripts.eval.contracts import sha256_object

ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/REPAIRED_GATE0B_EXECUTION_CARD.json"


def test_repaired_gate0b_card_is_sealed_bounded_and_fail_closed() -> None:
    card = json.loads(CARD.read_text(encoding="utf-8"))
    claimed = card.pop("card_sha256")
    assert sha256_object(card) == claimed == "6853e7e07b39c00383ebb4f9c3ee34180ee032aa9b5f589fefb4b86698ddca21"
    assert card["status"] == "prepared-awaiting-explicit-gcloud-approval"
    assert card["authorization_boundary"]["gcloud_status"] == "not-approved-by-this-card"
    assert card["prebuild"]["maximum_vm_lifetime_seconds"] == 3600
    assert card["qualification"]["maximum_vm_lifetime_seconds"] == 1200
    assert card["qualification"]["training_performed_by_this_card"] is False
    assert Decimal(str(card["cost"]["cumulative_planned_upper_usd"])) < Decimal(
        str(card["cost"]["absolute_cumulative_ceiling_usd"])
    )
    sequence = card["mandatory_sequence"]
    assert sequence.index("independently verify the complete GCS prebuild inventory") < sequence.index(
        "stop and delete the CPU VM; remove NAT and router"
    )
    assert sequence.index("independently verify the terminal GCS inventory") < sequence.index(
        "stop and delete the A100 VM, then delete subnet and VPC"
    )
    assert "no explicit GCloud approval for this card" in card["hard_stops"]
