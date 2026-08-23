import json
from pathlib import Path

from scripts.release.adjudicate import adjudicate, canonical_sha256


LANES=("go","java","javascript","typescript","python","rust")


def cohort(passed: int) -> dict:
    return {"lanes":{lane:{"passed":passed} for lane in LANES}}


def test_release_gates_fail_closed_and_pass_complete_evidence(tmp_path: Path) -> None:
    comparison={"five_family_macro_delta":{"decimal":0.1},"base":cohort(5),"candidate":cohort(6),"paired":{"lanes":{lane:{"losses":0} for lane in LANES},"cluster_aware":{"bootstrap_ci":{"lower":0.01},"two_sided_permutation_p":0.01}}}
    quant={"base":cohort(10),"candidate":cohort(10)}; laptop={"profiles":{"q8":{"passed":True,"peak_rss_bytes":6*1024**3},"f16":{"passed":True,"peak_rss_bytes":13*1024**3}}}
    manifest={"status":"complete"}; manifest["manifest_sha256"]=canonical_sha256(manifest); path=tmp_path/"manifest.json"; path.write_text(json.dumps(manifest))
    assert adjudicate(comparison,quant,laptop,[path])["status"]=="release-eligible"
    comparison["paired"]["cluster_aware"]["bootstrap_ci"]["lower"]=-0.01
    assert adjudicate(comparison,quant,laptop,[path])["status"]=="release-blocked"
