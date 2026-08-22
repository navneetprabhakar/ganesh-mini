from __future__ import annotations

import re


EXTRACTOR_ID = "ganesh-code-fence-v1"

LANGUAGE_TAGS = {
    "go": {"go", "golang"},
    "java": {"java"},
    "javascript": {"javascript", "js", "node"},
    "typescript": {"typescript", "ts"},
    "python": {"python", "py"},
    "rust": {"rust", "rs"},
}

_FENCE = re.compile(r"```[ \t]*([^\n`]*)\n(.*?)```", re.DOTALL)
_THINK = re.compile(r"<think>(.*?)</think>", re.DOTALL)


def split_channels(raw_output: str) -> dict[str, str]:
    """Separate explicit Qwen reasoning markup without inventing content."""
    reasoning_parts = [part.strip() for part in _THINK.findall(raw_output)]
    final = _THINK.sub("", raw_output)
    final = final.replace("<|im_end|>", "").replace("<|endoftext|>", "").strip()
    return {"reasoning": "\n\n".join(part for part in reasoning_parts if part), "final": final}


def extract_code(raw_output: str, language: str) -> tuple[str, dict[str, object]]:
    channels = split_channels(raw_output)
    final = channels["final"]
    fences = [(tag.strip().lower(), body.strip()) for tag, body in _FENCE.findall(final)]
    aliases = LANGUAGE_TAGS[language]
    selected_index: int | None = None
    strategy = "plain_final"
    for index, (tag, _) in enumerate(fences):
        parts = tag.split(maxsplit=1)
        if parts and parts[0] in aliases:
            selected_index = index
            strategy = "language_fence"
            break
    if selected_index is None and fences:
        selected_index = 0
        strategy = "first_fence"
    code = fences[selected_index][1] if selected_index is not None else final.strip()
    if code and not code.endswith("\n"):
        code += "\n"
    metadata: dict[str, object] = {
        "extractor_id": EXTRACTOR_ID,
        "strategy": strategy,
        "fence_count": len(fences),
        "selected_fence_index": selected_index,
        "reasoning": channels["reasoning"],
        "final": final,
    }
    return code, metadata
