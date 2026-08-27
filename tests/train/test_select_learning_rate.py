from scripts.train.select_learning_rate import select


LANES=("go","java","javascript","typescript","python","rust")


def result(task_id: str, lane: str, passed: bool) -> dict:
    return {"task_id":task_id,"language":lane,"passed":passed,"result_sha256":task_id.encode().hex().ljust(64,"0")[:64]}


def cohort() -> list[dict]:
    return [result(f"task-{index:03d}",LANES[index%6],False) for index in range(180)]


def run(lr: float) -> dict:
    return {"status":"complete","identities":{"phase":"lr-candidate","learning_rate":str(lr)},"state":{"seen_tokens":400000},"evidence_sha256":str(lr).encode().hex().ljust(64,"0")[:64]}


def test_higher_lr_requires_gain_and_no_lane_regression() -> None:
    low=cohort(); high=[dict(row) for row in low]; high[0]["passed"]=True
    assert select(low,high,run(0.0001),run(0.0002))["selected_learning_rate"]==0.0002
    high[0]["passed"]=False; high[1]["passed"]=True; low[2]["passed"]=True
    assert select(low,high,run(0.0001),run(0.0002))["selected_learning_rate"]==0.0001


def test_conservative_v2_learning_rates_and_budget_are_bound() -> None:
    low=cohort(); high=[dict(row) for row in low]; high[0]["passed"]=True
    low_run=run(0.00001); high_run=run(0.00003)
    low_run["state"]["seen_tokens"]=high_run["state"]["seen_tokens"]=461235
    selected=select(low,high,low_run,high_run,low_lr=0.00001,high_lr=0.00003,minimum_seen_tokens=461235,rule="v2-rule")
    assert selected["schema_version"]=="ganesh-mini-lr-selection/v2"
    assert selected["selected_learning_rate"]==0.00003
    assert selected["minimum_seen_tokens"]==461235
    assert set(selected["candidates"])=={"1e-05","3e-05"}
