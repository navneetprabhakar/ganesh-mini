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
: "${GANESH_CUMULATIVE_COST_USD:?set GANESH_CUMULATIVE_COST_USD to all prior and prebuild cost}"
: "${GANESH_SUPPORT_RESERVE_USD:?set GANESH_SUPPORT_RESERVE_USD}"
: "${GANESH_ABSOLUTE_CUMULATIVE_CEILING_USD:?set the card-bound absolute cumulative ceiling}"
: "${GANESH_MAX_VM_LIFETIME_SECONDS:?set the card-bound VM lifetime}"
python3 - "$GANESH_GPU_HOURLY_USD" "$GANESH_CUMULATIVE_COST_USD" "$GANESH_SUPPORT_RESERVE_USD" "$GANESH_ABSOLUTE_CUMULATIVE_CEILING_USD" "$GANESH_MAX_VM_LIFETIME_SECONDS" <<'PY'
from decimal import Decimal, InvalidOperation
import sys
try:
    hourly, cumulative, reserve, ceiling, lifetime = map(Decimal, sys.argv[1:])
except InvalidOperation as exc:
    raise SystemExit(f"invalid cost input: {exc}")
projected = cumulative + hourly * lifetime / Decimal(3600) + reserve
if hourly <= 0 or cumulative < 0 or reserve < 0 or ceiling <= 0 or lifetime <= 0 or projected >= ceiling:
    raise SystemExit(f"qualification would reach or exceed the card-bound cumulative ceiling {ceiling}: {projected}")
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
  : "${GANESH_FALLBACK_TRIGGER:?fallback requires a declared measured trigger}"
  python3 - "$GANESH_PRIMARY_QUALIFICATION_EVIDENCE" "$GANESH_FALLBACK_TRIGGER" <<'PY'
import json, sys
import hashlib
from pathlib import Path
value = json.loads(Path(sys.argv[1]).read_text())
trigger = sys.argv[2]
claimed = value.pop("evidence_sha256", None)
actual = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
if claimed != actual:
    raise SystemExit("primary qualification evidence seal is invalid")
if value.get("recipe_id") != "bf16-lora-primary-v1" or value.get("status") != "failed":
    raise SystemExit("fallback requires a failed BF16 primary qualification")
allowed = {
    "primary_cuda_oom": value.get("error_type") in {"OutOfMemoryError", "CUDAOutOfMemoryError"} or "out of memory" in value.get("error", "").lower(),
    "primary_peak_vram_exceeded": value.get("error_type") == "PeakVramExceeded" and isinstance(value.get("peak_vram_failure"), dict),
}
if trigger not in allowed or not allowed[trigger]:
    raise SystemExit(f"fallback trigger is not supported by sealed BF16 evidence: {trigger}")
PY
fi
: "${GANESH_CUDA_IMAGE_REF:?set GANESH_CUDA_IMAGE_REF to the preloaded immutable qualification image tag}"
: "${GANESH_CUDA_IMAGE_ID:?set GANESH_CUDA_IMAGE_ID to the sealed docker image ID}"
image="$GANESH_CUDA_IMAGE_REF"
observed_image_id="$(docker image inspect --format '{{.Id}}' "$image")"
if [[ "$observed_image_id" != "$GANESH_CUDA_IMAGE_ID" ]]; then
  echo "preloaded image identity mismatch: expected=$GANESH_CUDA_IMAGE_ID observed=$observed_image_id" >&2
  exit 43
fi
controller_deadline_epoch="${GANESH_CONTROLLER_DEADLINE_EPOCH:-$(( $(date +%s) + 1800 ))}"
seconds_until_deadline=$((controller_deadline_epoch - $(date +%s)))
if (( seconds_until_deadline <= 0 )); then
  echo "absolute qualification deadline already exhausted" >&2
  exit 2
fi
# The sealed image is loaded before this controller starts. Execution is
# offline, pull-disabled, bounded to one GPU, and cannot build or download.
timeout --signal=TERM --kill-after=30s "$seconds_until_deadline" \
  docker run --rm --pull=never --gpus device=0 --network none --cpus 12 --memory 72g \
    --read-only --tmpfs /tmp:rw,noexec,nosuid,size=8g \
    --tmpfs /var/cache/triton:rw,exec,nosuid,nodev,size=1g \
    -e HF_HUB_OFFLINE=1 -e TRANSFORMERS_OFFLINE=1 \
    -e TRITON_CACHE_DIR=/var/cache/triton \
    -e GANESH_ATTEMPT_ID="${GANESH_ATTEMPT_ID:?GANESH_ATTEMPT_ID is required}" \
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
