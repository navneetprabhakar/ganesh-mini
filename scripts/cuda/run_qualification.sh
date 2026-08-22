#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "CUDA qualification must run on a Linux NVIDIA host" >&2
  exit 2
fi
if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo "usage: $0 MODEL_DIR RECORDS_JSONL OUTPUT_DIR [bf16-lora-primary-v1|nf4-qlora-fallback-v1]" >&2
  exit 2
fi
: "${GANESH_GPU_HOURLY_USD:?set GANESH_GPU_HOURLY_USD to the effective hourly GPU-host price}"
python3 - "$GANESH_GPU_HOURLY_USD" <<'PY'
from decimal import Decimal, InvalidOperation
import sys
try:
    hourly = Decimal(sys.argv[1])
except InvalidOperation as exc:
    raise SystemExit(f"invalid GANESH_GPU_HOURLY_USD: {exc}")
if hourly <= 0 or hourly * Decimal("0.5") > Decimal("5"):
    raise SystemExit("30-minute qualification would exceed the USD 5 compute ceiling")
PY

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
model_dir="$(realpath "$1")"
records_path="$(realpath "$2")"
output_dir="$(mkdir -p "$3" && realpath "$3")"
recipe="${4:-bf16-lora-primary-v1}"
if [[ "$recipe" != "bf16-lora-primary-v1" && "$recipe" != "nf4-qlora-fallback-v1" ]]; then
  echo "unknown qualification recipe: $recipe" >&2
  exit 2
fi
if [[ "$recipe" == "nf4-qlora-fallback-v1" ]]; then
  : "${GANESH_PRIMARY_QUALIFICATION_EVIDENCE:?fallback requires the prior BF16 primary evidence path}"
  python3 - "$GANESH_PRIMARY_QUALIFICATION_EVIDENCE" <<'PY'
import json, sys
import hashlib
from pathlib import Path
value = json.loads(Path(sys.argv[1]).read_text())
claimed = value.pop("evidence_sha256", None)
actual = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
if claimed != actual:
    raise SystemExit("primary qualification evidence seal is invalid")
if value.get("recipe_id") != "bf16-lora-primary-v1" or value.get("status") not in {"passed", "failed"}:
    raise SystemExit("fallback requires evidence of an attempted BF16 primary qualification")
PY
fi
image="ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1"
started_seconds="$SECONDS"
controller_deadline_epoch="${GANESH_CONTROLLER_DEADLINE_EPOCH:-$(( $(date +%s) + 1800 ))}"
seconds_until_deadline=$((controller_deadline_epoch - $(date +%s)))
if (( seconds_until_deadline <= 0 )); then
  echo "absolute qualification deadline already exhausted" >&2
  exit 2
fi
build_seconds=1200
if (( seconds_until_deadline < build_seconds )); then build_seconds="$seconds_until_deadline"; fi

timeout --signal=TERM --kill-after=30s "$build_seconds" \
  docker build --platform linux/amd64 --pull=false --network=default \
  --file "$repo_dir/containers/cuda/Dockerfile" --tag "$image" "$repo_dir"

remaining_seconds=$((controller_deadline_epoch - $(date +%s)))
if (( remaining_seconds <= 0 )); then
  echo "image build exhausted the 1,800-second total qualification bound" >&2
  exit 2
fi

# The image is built before execution. The qualification itself is offline,
# bounded to one GPU and 30 minutes, and cannot silently download another model.
timeout --signal=TERM --kill-after=30s "$remaining_seconds" \
  docker run --rm --gpus device=0 --network none --cpus 8 --memory 32g \
    --read-only --tmpfs /tmp:rw,noexec,nosuid,size=8g \
    -e HF_HUB_OFFLINE=1 -e TRANSFORMERS_OFFLINE=1 \
    -v "$repo_dir:/workspace:ro" \
    -v "$model_dir:/input/model:ro" \
    -v "$records_path:/input/train.jsonl:ro" \
    -v "$output_dir:/output:rw" \
    "$image" \
    --recipe "$recipe" \
    --model-dir /input/model \
    --records /input/train.jsonl \
    --adapter-dir "/output/adapter-$recipe" \
    --output "/output/qualification-$recipe.json"
