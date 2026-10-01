import json

from scripts.data.build_capability_corpus_plan import canonical_sha256
from scripts.data.retry_capability_scale_delta_transport import transport_only_failure


def test_transport_failure_is_retryable_only_with_terminal_output_and_no_tool() -> None:
    events = [
        {"type": "item.completed", "item": {"type": "error", "message":
            "Falling back from WebSockets to HTTPS transport. unexpected status 403 Forbidden"}},
        {"type": "item.completed", "item": {"type": "agent_message", "text": "{}"}},
        {"type": "turn.completed", "usage": {"input_tokens": 1}},
    ]
    failure = {
        "returncode": 0,
        "timed_out": False,
        "event_parse_error": None,
        "disallowed_tool_item_types": ["error"],
        "usage": {"input_tokens": 1},
        "final_output": "{}",
        "stdout_jsonl": "\n".join(json.dumps(row) for row in events),
        "events": events,
    }
    artifact = {"status": "invocation-failed", "failure": failure,
                "failure_sha256": canonical_sha256(failure)}
    assert transport_only_failure(artifact)
    failure["final_output"] = ""
    artifact["failure_sha256"] = canonical_sha256(failure)
    assert not transport_only_failure(artifact)
    failure["final_output"] = "{}"
    failure["events"][0]["item"]["message"] = "Tool execution failed"
    failure["stdout_jsonl"] = "\n".join(json.dumps(row) for row in failure["events"])
    artifact["failure_sha256"] = canonical_sha256(failure)
    assert not transport_only_failure(artifact)
