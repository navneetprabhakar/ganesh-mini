import json
from decimal import Decimal
from pathlib import Path

from scripts.eval.contracts import sha256_object


ROOT = Path(__file__).resolve().parents[2]
CARD = ROOT / "measurement/cuda/gcloud/ATTRIBUTE_REPAIR_A100_RETRY_CARD.json"


def test_attribute_repair_retry_card_is_sealed_a100_only_and_fail_closed() -> None:
    card = json.loads(CARD.read_text(encoding="utf-8"))
    claimed = card.pop("card_sha256")
    assert sha256_object(card) == claimed
    assert card["status"] == "prepared-awaiting-explicit-gcloud-approval"
    assert card["authorization_boundary"]["gcloud_status"] == "not-approved-by-this-card"
    assert "prebuild" not in card
    assert card["qualification"]["maximum_vm_lifetime_seconds"] == 1200
    assert card["qualification"]["main_or_seed_pilot_training_performed_by_this_card"] is False
    assert card["qualification"]["bounded_qualification_training_smoke_performed_by_this_card"] is True
    assert card["source"]["commit"] == "f71007f7f127fc55c8875cd3972bb96c6ccf4111"
    assert set(card["source"]) >= {
        "qualification_runner_sha256",
        "startup_controller_sha256",
        "metadata_wrapper_sha256",
    }
    assert Decimal(str(card["cost"]["cumulative_planned_upper_usd"])) < Decimal(
        str(card["cost"]["absolute_cumulative_ceiling_usd"])
    )
    scope = " ".join(card["authorization_boundary"]["required_explicit_scope"])
    assert "no router, NAT, or external IP" in scope
    sequence = card["mandatory_sequence"]
    assert sequence.index(
        "independently verify the initial terminal backup using two generation-pinned full-object reads"
    ) < sequence.index("stop the A100 VM after the initial terminal backup passes independent verification")
    assert sequence.index(
        "capture stopped VM identity and provider evidence, upload them, and independently verify the complete generation-pinned set"
    ) < sequence.index("pass the deletion gate against the verified terminal backup and stopped provider identity")
    assert "no explicit GCloud approval for this exact card" in card["hard_stops"]
