from scripts.data.assess_expansion_pilot import canonical_jsonl, measure_rows, throughput_projection


class Tokenizer:
    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, enable_thinking, return_dict=False):
        text = "|".join(item["content"] for item in messages if item["role"] != "assistant") + "|assistant"
        if messages[-1]["role"] == "assistant":
            text += messages[-1]["content"]
        ids = list(range(len(text)))
        return {"input_ids": ids, "attention_mask": [1] * len(ids)} if return_dict else text


def test_measure_rows_counts_and_binds_ordered_corpus():
    rows = [
        {"id": "a", "lane": "go", "task_type": "generation", "messages": [{"role": "user", "content": "x"}, {"role": "assistant", "content": "yz"}]},
        {"id": "b", "lane": "python", "task_type": "repair", "messages": [{"role": "user", "content": "q"}, {"role": "assistant", "content": "rs"}]},
    ]
    result = measure_rows(Tokenizer(), rows, maximum_length=100)
    assert result["records"] == 2
    assert result["counts_by_lane"] == {"go": 1, "python": 1}
    assert result["counts_by_task_type"] == {"generation": 1, "repair": 1}
    assert result["records_over_sequence_length_by_lane"] == {}
    assert len(result["canonical_jsonl_sha256"]) == 64


def test_throughput_projection_uses_measured_rate_and_conservative_margin():
    run = {"state": {"seen_tokens": 1000, "wall_seconds": 10}}
    phases = {"phases": [{"name": "train-lr-1e-5", "elapsed_seconds": 12}]}
    result = throughput_projection(2000, run, phases)
    assert result["measured_input_tokens_per_second"] == 100
    assert result["projected_training_phase_seconds"]["expected"] == 24
    assert result["projected_training_phase_seconds"]["conservative"] == 32
    assert result["recommended_runtime_ceiling_seconds_including_30m_backup_reserve"] == 21600


def test_canonical_jsonl_is_ordered_and_newline_terminated():
    rows = [{"z": 1, "a": 2}, {"id": "b"}]
    assert canonical_jsonl(rows) == b'{"a":2,"z":1}\n{"id":"b"}\n'
