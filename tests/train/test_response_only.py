from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.train.response_only import ResponseOnlyError, build_response_only_encoding


ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "models/qwen3.5-2b-15852e8"
SEED_PATHS = (
    ROOT / "data/seed/ganesh_v01/train.jsonl",
    ROOT / "data/seed/ganesh_v01/validation.jsonl",
)


def _pinned_tokenizer():
    if not (MODEL_DIR / "tokenizer.json").is_file():
        pytest.skip("exact pinned tokenizer is not present")
    transformers = pytest.importorskip("transformers")
    return transformers.AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)


def test_exact_qwen_template_proves_response_boundaries_for_every_seed_row() -> None:
    tokenizer = _pinned_tokenizer()
    checked = 0
    lanes: set[str] = set()
    for path in SEED_PATHS:
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            result = build_response_only_encoding(tokenizer, row["messages"])
            labels = result.encoding["labels"]
            assert labels[: result.prompt_token_count] == [-100] * result.prompt_token_count
            assert labels[result.prompt_token_count :] == result.encoding["input_ids"][result.prompt_token_count :]
            assert result.response_token_count > 0
            assert result.prompt_token_count + result.response_token_count <= 4096
            checked += 1
            lanes.add(row["lane"])
    assert checked == 1449
    assert lanes == {"go", "java", "javascript", "typescript", "python", "rust"}


def test_exact_qwen_tensor_labels_mask_prompt_and_keep_completion() -> None:
    tokenizer = _pinned_tokenizer()
    row = json.loads(SEED_PATHS[0].read_text(encoding="utf-8").splitlines()[0])
    result = build_response_only_encoding(
        tokenizer, row["messages"], max_length=4096, return_tensors="pt"
    )
    labels = result.encoding["labels"]
    assert labels.shape == result.encoding["input_ids"].shape
    assert (labels[:, : result.prompt_token_count] == -100).all()
    assert (labels[:, result.prompt_token_count :] != -100).all()


def test_response_truncation_fails_closed() -> None:
    tokenizer = _pinned_tokenizer()
    row = json.loads(SEED_PATHS[0].read_text(encoding="utf-8").splitlines()[0])
    prompt = tokenizer.apply_chat_template(
        row["messages"][:-1],
        tokenize=True,
        add_generation_prompt=True,
        enable_thinking=False,
        return_dict=True,
    )
    with pytest.raises(ResponseOnlyError, match="response truncation is forbidden"):
        build_response_only_encoding(
            tokenizer, row["messages"], max_length=len(prompt["input_ids"])
        )
