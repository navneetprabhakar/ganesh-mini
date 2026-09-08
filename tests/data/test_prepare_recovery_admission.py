from scripts.data.prepare_recovery_admission import check_overlap


def row(id, prompt):
    return {"id": id, "messages": [{"content": prompt}]}


def test_retained_and_selected_overlap_are_not_ignored():
    candidates = [row("new1", "Same prompt"), row("new2", "Other prompt"), row("new3", "Other prompt")]
    results = check_overlap(candidates, [row("original", "same PROMPT")])
    assert results == [{"id": "new1", "overlap_id": "original", "exact": True},
                       {"id": "new3", "overlap_id": "new2", "exact": True}]


def test_disjoint_short_prompts_do_not_fuzzy_collide():
    assert check_overlap([row("new", "Alpha")], [row("old", "Beta")]) == []
