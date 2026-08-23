"""Tokenizer-owned response-only label construction.

The pinned Qwen3.5 template has no Jinja ``generation`` blocks, so the
Transformers-generated assistant mask is all zero. Derive the terminal
completion boundary from two renderings by the same exact tokenizer instead:
the prompt with its generation prefix, and the completed assistant turn.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ResponseOnlyError(ValueError):
    """The tokenizer could not prove one terminal assistant response span."""


@dataclass(frozen=True)
class ResponseOnlyEncoding:
    encoding: Any
    rendered: str
    prompt_token_count: int
    response_token_count: int


def _token_rows(value: Any, *, name: str) -> tuple[list[list[int]], bool]:
    if hasattr(value, "detach") and hasattr(value, "tolist"):
        value = value.detach().cpu().tolist()
    if not isinstance(value, list) or not value:
        raise ResponseOnlyError(f"tokenizer returned invalid {name}")
    if isinstance(value[0], list):
        if len(value) != 1 or not value[0]:
            raise ResponseOnlyError(f"tokenizer returned invalid batched {name}")
        rows, batched = value, True
    else:
        rows, batched = [value], False
    if any(not isinstance(token, int) for token in rows[0]):
        raise ResponseOnlyError(f"tokenizer returned non-integer {name}")
    return rows, batched


def _labels_like(input_ids: Any, prompt_token_count: int) -> Any:
    if hasattr(input_ids, "clone"):
        labels = input_ids.clone()
        if getattr(labels, "ndim", None) == 2:
            if labels.shape[0] != 1:
                raise ResponseOnlyError("batched training examples are not accepted")
            labels[:, :prompt_token_count] = -100
        elif getattr(labels, "ndim", None) == 1:
            labels[:prompt_token_count] = -100
        else:
            raise ResponseOnlyError("tokenizer returned invalid input_ids dimensions")
        return labels
    rows, batched = _token_rows(input_ids, name="input_ids")
    labels = [-100] * prompt_token_count + rows[0][prompt_token_count:]
    return [labels] if batched else labels


def build_response_only_encoding(
    tokenizer: Any,
    messages: list[dict[str, str]],
    *,
    max_length: int | None = None,
    return_tensors: str | None = None,
) -> ResponseOnlyEncoding:
    """Render and label exactly one terminal assistant completion."""
    if not isinstance(messages, list) or len(messages) < 2:
        raise ResponseOnlyError("a prompt and terminal assistant response are required")
    if any(
        not isinstance(message, dict)
        or message.get("role") not in {"system", "user", "assistant"}
        or not isinstance(message.get("content"), str)
        for message in messages
    ):
        raise ResponseOnlyError("text-only role/content messages are required")
    if messages[-1]["role"] != "assistant" or not messages[-1]["content"]:
        raise ResponseOnlyError("record must end with a non-empty assistant response")

    common: dict[str, Any] = {
        "tokenize": True,
        "return_dict": True,
        "enable_thinking": False,
    }
    if return_tensors is not None:
        common["return_tensors"] = return_tensors
    if max_length is not None:
        if max_length <= 0:
            raise ResponseOnlyError("max_length must be positive")

    prompt = tokenizer.apply_chat_template(
        messages[:-1], add_generation_prompt=True, **common
    )
    complete = tokenizer.apply_chat_template(
        messages, add_generation_prompt=False, **common
    )
    prompt_rows, _ = _token_rows(prompt.get("input_ids"), name="prompt input_ids")
    complete_rows, _ = _token_rows(complete.get("input_ids"), name="complete input_ids")
    prompt_ids, complete_ids = prompt_rows[0], complete_rows[0]
    if max_length is not None and len(complete_ids) > max_length:
        raise ResponseOnlyError(
            f"completed turn has {len(complete_ids)} tokens and exceeds max_length={max_length}; "
            "response truncation is forbidden"
        )
    if len(prompt_ids) >= len(complete_ids):
        raise ResponseOnlyError("assistant response is empty")
    if complete_ids[: len(prompt_ids)] != prompt_ids:
        raise ResponseOnlyError("generation prompt is not a token prefix of the completed turn")

    rendered_prompt = tokenizer.apply_chat_template(
        messages[:-1], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    rendered = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False, enable_thinking=False
    )
    if not isinstance(rendered_prompt, str) or not isinstance(rendered, str):
        raise ResponseOnlyError("tokenizer did not return text renderings")
    if not rendered.startswith(rendered_prompt):
        raise ResponseOnlyError("generation prompt is not a text prefix of the completed turn")

    complete["labels"] = _labels_like(complete["input_ids"], len(prompt_ids))
    return ResponseOnlyEncoding(
        encoding=complete,
        rendered=rendered,
        prompt_token_count=len(prompt_ids),
        response_token_count=len(complete_ids) - len(prompt_ids),
    )
