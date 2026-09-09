from scripts.inference.build_capacity_probe_gcloud_proposal import build, canonical_sha256


def test_builds_bounded_non_executable_proposal() -> None:
    proposal = build()
    claimed = proposal.pop("proposal_sha256")
    assert claimed == canonical_sha256(proposal)
    assert proposal["status"] == "pending-explicit-execution-approval"
    assert proposal["cost"]["absolute_cost_ceiling_usd"] == "2.25"
    assert proposal["cost"]["provider_upper_usd"] == "1.762043024"
    assert proposal["resource"]["maximum_vm_lifetime_seconds"] == 7200
    assert proposal["experiment"]["full_development_tasks"] == 0
    assert len(proposal["inputs"]) == 9
    assert proposal["approval"]["approved"] is False
