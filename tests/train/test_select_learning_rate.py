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
